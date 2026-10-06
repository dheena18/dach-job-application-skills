"""
ATS-readability check for a generated resume PDF.

This does not simulate any specific vendor (Workday, Greenhouse, Personio,
SAP SuccessFactors, ...). What it checks is the small set of things that are
genuinely known to break parsing across most of them: text has to actually
extract (not be a scanned image with no text layer), it has to extract in
top-to-bottom reading order (multi-column layouts get scrambled by many
parsers), contact details have to be findable as plain text, and nothing
should extract as replacement/control characters (a font-encoding problem
that breaks parsing even though the PDF looks fine to a human).

A clean result here is a necessary check, not a guarantee — no tool can
fully simulate a closed-source ATS's parser. It catches the mechanical
failure modes; it does not evaluate keyword match or content quality (that's
a job-tailoring concern, not a translation/format concern).

Usage:
    python check_ats.py <file.pdf> --email you@example.com --phone "+49..." [--name "Firstname Lastname"] [--expect-pages 2] [--headings-in-order H1 H2 H3 ...]
"""
import argparse
import re
import sys

from pypdf import PdfReader


def extract_text(path):
    reader = PdfReader(path)
    pages = [page.extract_text() or "" for page in reader.pages]
    return pages


def check(path, email=None, phone=None, name=None, expect_pages=None, headings=None):
    findings = []
    pages = extract_text(path)
    full_text = "\n".join(pages)

    if not full_text.strip():
        findings.append("CRITICAL: no extractable text at all — this would look like a scanned image to an ATS parser.")
        return findings

    if len(full_text.strip()) < 200:
        findings.append(f"WARNING: only {len(full_text.strip())} characters extracted — suspiciously little for a resume.")

    if "�" in full_text:
        count = full_text.count("�")
        findings.append(f"CRITICAL: {count} Unicode replacement character(s) (U+FFFD) found — a font/encoding problem that will also break real ATS parsers, not just this check.")

    pua_chars = [c for c in full_text if 0xE000 <= ord(c) <= 0xF8FF]
    if pua_chars:
        findings.append(
            f"CRITICAL: {len(pua_chars)} Private-Use-Area character(s) found — a known Word/PDF bug where a bullet or "
            "symbol glyph extracts as a private-use codepoint instead of its real character (e.g. U+2022 for a bullet). "
            "Distinct from U+FFFD; text search/parsing silently fails on these characters without visibly looking wrong."
        )

    if expect_pages is not None and len(pages) != expect_pages:
        findings.append(f"WARNING: extracted {len(pages)} page(s), expected {expect_pages}.")

    if email and email not in full_text:
        findings.append(f"CRITICAL: email '{email}' not found in extracted text — contact info may not be machine-readable.")

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
                    f"CRITICAL: reading order broken — '{h2}' extracts before or at the same position as '{h1}'. "
                    "This is the classic multi-column-layout failure mode: the parser is not reading top-to-bottom."
                )

    return findings


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf")
    parser.add_argument("--email")
    parser.add_argument("--phone")
    parser.add_argument("--name")
    parser.add_argument("--expect-pages", type=int)
    parser.add_argument("--headings-in-order", nargs="*")
    args = parser.parse_args()

    results = check(
        args.pdf,
        email=args.email,
        phone=args.phone,
        name=args.name,
        expect_pages=args.expect_pages,
        headings=args.headings_in_order,
    )
    if results:
        print(f"{len(results)} finding(s):")
        for r in results:
            print(" -", r)
        sys.exit(1)
    print("No ATS-readability issues found.")
    sys.exit(0)
