"""
Standalone ATS-readability check for a resume, given as a .docx and/or the
PDF exported from it. This does not simulate any specific vendor — it
checks the small set of things genuinely known to break parsing across
most systems: layout structure that scrambles reading order, a missing
text layer, unreadable contact info, and encoding corruption.

Two independent check families:

1. DOCX STRUCTURAL CHECK (check_docx_structure): inspects the .docx's own
   XML directly for the known layout risk factors — real tables, multi-
   column sections, headers/footers, embedded images/text boxes/drawings.
   This is the more authoritative check, since it looks at the document's
   actual structure rather than inferring it from how one particular PDF
   renderer's text extraction happened to come out.

2. PDF TEXT CHECK (check_pdf_text): extracts text from the exported PDF and
   checks it actually exists, is in the right reading order (headings
   extract top-to-bottom), contact info is present as plain text, and
   nothing extracted as a replacement or Private-Use-Area character (a
   real, silent bullet/glyph-corruption bug distinct from visibly broken
   text).

A clean result from both is a necessary check, not a guarantee of any
specific vendor's behavior — see references/what-ats-actually-do.md for
why "beat the ATS" is largely oversold, and why some real systems (e.g.
HackerRank's 2026 open-source ATS) score on criteria (Open Source /
Projects sections) that have nothing to do with parsing at all.

Usage:
    python check_ats.py docx <file.docx>
    python check_ats.py pdf <file.pdf> [--email E] [--phone P] [--name N] [--expect-pages N] [--headings-in-order H1 H2 ...]
    python check_ats.py both <file.docx> <file.pdf> [...same pdf options]
"""
import argparse
import re
import sys

import docx
from docx.oxml.ns import qn
from pypdf import PdfReader

W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def check_docx_structure(path):
    findings = []
    d = docx.Document(path)
    body = d.element.body

    tables = body.findall(qn("w:tbl"))
    if tables:
        findings.append(
            f"CRITICAL: {len(tables)} table(s) found in the document. Tables are the single "
            "most-documented cause of ATS parsers reading a resume out of order (row/cell "
            "concatenation, section-header misidentification). A tab-stop-aligned single "
            "paragraph is the safe alternative for a title/date line."
        )

    for sect_pr in body.findall(qn("w:sectPr")) + [
        p._p.find(qn("w:pPr") + "/" + qn("w:sectPr")) for p in d.paragraphs
    ]:
        if sect_pr is None:
            continue
        cols = sect_pr.find(qn("w:cols"))
        if cols is not None and cols.get(qn("w:num")) not in (None, "1"):
            findings.append(
                f"CRITICAL: multi-column section layout found ({cols.get(qn('w:num'))} columns). "
                "Column layouts are read column-by-column by many parsers, interleaving unrelated "
                "content out of order."
            )

    for header_footer_tag in ("w:headerReference", "w:footerReference"):
        refs = body.findall(f".//{{http://schemas.openxmlformats.org/wordprocessingml/2006/main}}{header_footer_tag.split(':')[1]}")
        if refs:
            findings.append(
                f"WARNING: {len(refs)} {header_footer_tag.split(':')[1]}(s) referenced. Content in "
                "headers/footers is dropped entirely by several ATS parsers — never put contact "
                "info or content that must be read there."
            )

    drawings = body.findall(".//" + qn("w:drawing"))
    if drawings:
        findings.append(
            f"WARNING: {len(drawings)} image/drawing object(s) found (icons, photos, logos, "
            "text boxes, skill-bar graphics). Any text inside these is usually invisible to a "
            "parser, and the object itself can disrupt reading order."
        )

    return findings


def _extract_pdf_pages(path):
    reader = PdfReader(path)
    return [page.extract_text() or "" for page in reader.pages]


def check_pdf_text(path, email=None, phone=None, name=None, expect_pages=None, headings=None):
    findings = []
    pages = _extract_pdf_pages(path)
    full_text = "\n".join(pages)

    if not full_text.strip():
        findings.append("CRITICAL: no extractable text at all — this would look like a scanned image to an ATS parser.")
        return findings

    if len(full_text.strip()) < 200:
        findings.append(f"WARNING: only {len(full_text.strip())} characters extracted — suspiciously little for a resume.")

    if "�" in full_text:
        findings.append(f"CRITICAL: {full_text.count(chr(0xFFFD))} Unicode replacement character(s) (U+FFFD) — a font/encoding problem.")

    pua_chars = [c for c in full_text if 0xE000 <= ord(c) <= 0xF8FF]
    if pua_chars:
        findings.append(
            f"CRITICAL: {len(pua_chars)} Private-Use-Area character(s) — a bullet/symbol glyph likely "
            "extracted as a private-use codepoint instead of its real character. Invisible to the eye, "
            "silently breaks text search/parsing."
        )

    if expect_pages is not None and len(pages) != expect_pages:
        findings.append(f"WARNING: extracted {len(pages)} page(s), expected {expect_pages}.")

    if email and email not in full_text:
        findings.append(f"CRITICAL: email '{email}' not found in extracted text.")

    if phone:
        digits_only = re.sub(r"\D", "", phone)
        text_digits = re.sub(r"\D", "", full_text)
        if digits_only not in text_digits:
            findings.append(f"CRITICAL: phone number '{phone}' not found (digit-for-digit) in extracted text.")

    if name and name not in full_text:
        findings.append(f"WARNING: name '{name}' not found verbatim in extracted text.")

    if headings:
        positions = []
        for h in headings:
            idx = full_text.find(h)
            if idx == -1:
                findings.append(f"WARNING: expected section heading '{h}' not found in extracted text.")
            else:
                positions.append((h, idx))
        for (h1, p1), (h2, p2) in zip(positions, positions[1:]):
            if p2 <= p1:
                findings.append(
                    f"CRITICAL: reading order broken — '{h2}' extracts before or at the same position "
                    f"as '{h1}'. Classic multi-column-layout scrambling signature."
                )

    return findings


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["docx", "pdf", "both"])
    parser.add_argument("path", help="docx path (mode=docx), pdf path (mode=pdf)")
    parser.add_argument("pdf_path", nargs="?", help="pdf path, only for mode=both")
    parser.add_argument("--email")
    parser.add_argument("--phone")
    parser.add_argument("--name")
    parser.add_argument("--expect-pages", type=int)
    parser.add_argument("--headings-in-order", nargs="*")
    args = parser.parse_args()

    all_findings = []
    if args.mode in ("docx", "both"):
        all_findings += check_docx_structure(args.path)
    if args.mode == "pdf":
        all_findings += check_pdf_text(args.path, args.email, args.phone, args.name, args.expect_pages, args.headings_in_order)
    if args.mode == "both":
        if not args.pdf_path:
            print("mode=both requires both a docx path and a pdf path", file=sys.stderr)
            sys.exit(2)
        all_findings += check_pdf_text(args.pdf_path, args.email, args.phone, args.name, args.expect_pages, args.headings_in_order)

    if all_findings:
        print(f"{len(all_findings)} finding(s):")
        for f in all_findings:
            print(" -", f)
        sys.exit(1)
    print("No ATS-readability issues found.")
    sys.exit(0)
