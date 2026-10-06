"""
Deterministic guard rail for the rebuilt German document: catches the
mechanical, unambiguous mistakes so the model's own judgment is spent on
the things that actually need it (grammar, tone, fact fidelity).

This is not a substitute for reading the document. It only catches the
class of error that is objectively checkable: English typography habits
(em dash, English number grouping) and stock AI-German filler phrases
documented as translation/AI-writing tells. A clean run does not mean the
German is good; a flagged run means something specific needs a look.

By default this scans every paragraph in the file. Pass --plan <plan.json>
(the same rewrite plan given to docx_rewrite.py) to scan only the
paragraphs that were actually rewritten into German. Use --plan whenever
the source document has paragraphs deliberately left untouched in their
original language — a project title, a competition name, a publication
title kept in English on purpose. Without --plan, an em dash or other
"violation" sitting in one of those untouched paragraphs is correctly
flagged as *present in the file*, but it is not a German-prose mistake and
should not be mistranslated or edited just to silence this script — check
whether the flagged text falls inside a paragraph you actually rewrote
before treating a finding as something to fix.

Usage:
    python lint_german.py <file.docx> [--plan plan.json]

Exit code 0 = no findings, 1 = findings printed to stdout.
"""
import argparse
import json
import re
import sys

import docx

# Phrases documented (see references/native-german-style.md) as stock
# AI-generated or translation-interference German, specific to prose/CV
# register. Matched case-insensitively as substrings.
BANNED_PHRASES = [
    "in der heutigen",
    "in der heutigen zeit",
    "spielt eine entscheidende rolle",
    "spielt eine wichtige rolle",
    "ist ein integraler bestandteil",
    "es ist wichtig zu beachten",
    "nicht zuletzt aufgrund",
    "bietet vielfältige möglichkeiten",
    "auf das nächste level heben",
    "ich bin überzeugt, dass",
    "nicht nur",  # nearly always paired with "sondern auch" — flag either half
    "sondern auch",
    "hochmotiviert",
    "teamplayer",
    "leidenschaft",
    "spannende herausforderung",
]


def _paragraph_texts(path, plan_path=None):
    d = docx.Document(path)
    indices = None
    if plan_path:
        with open(plan_path, encoding="utf-8") as f:
            plan = json.load(f)
        indices = {entry["index"] for entry in plan}
    for i, p in enumerate(d.paragraphs):
        if indices is not None and i not in indices:
            continue
        yield i, p.text


def _lint_paragraph(idx, text, findings):
    if "—" in text:
        findings.append(f"[para {idx}] em dash (—) present — not native German typography; rewrite with comma, colon, or a new sentence")

    if "--" in text:
        findings.append(f"[para {idx}] literal double hyphen '--' present — replace with proper punctuation")

    if '"' in text:
        findings.append(f'[para {idx}] straight double quote (") present — German uses „…" (or »…«); check every instance')

    for m in re.finditer(r"\b\d{1,3},\d{3}(\.\d+)?\b", text):
        findings.append(f"[para {idx}] English-style thousands separator: '{m.group()}' — German uses a period or space (e.g. 50.000)")

    for m in re.finditer(r"\b\d+\.\d+%", text):
        findings.append(f"[para {idx}] English decimal point before %: '{m.group()}' — German uses a comma (e.g. 3,8 %)")

    lowered = text.lower()
    for phrase in BANNED_PHRASES:
        if phrase in lowered:
            findings.append(f"[para {idx}] stock AI/filler phrase found: '{phrase}'")


def lint(path, plan_path=None):
    findings = []
    for idx, text in _paragraph_texts(path, plan_path):
        _lint_paragraph(idx, text, findings)
    return findings


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("docx")
    parser.add_argument("--plan", help="rewrite plan.json — restrict the scan to only these paragraph indices")
    args = parser.parse_args()

    results = lint(args.docx, args.plan)
    if results:
        print(f"{len(results)} finding(s):")
        for r in results:
            print(" -", r)
        sys.exit(1)
    print("No mechanical issues found.")
    sys.exit(0)
