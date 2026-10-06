"""
Deterministic lint pass for a drafted cover letter, checking the mechanical
subset of `references/banned-phrases-de-en.md`: banned phrases/openers,
em dashes, "not X but Y" / "nicht nur ... sondern auch" constructions,
paragraphs that all open with the same word, and word count against the
target range. This catches the checkable tells; it does not replace the
genericness read-aloud test, which needs a human judgment call.

Usage:
    python lint_letter.py <de|en> <plan.json|letter.txt>

Accepts either a build_cover_letter_docx.py plan (text is pulled from the
subject, salutation, body, and closing_phrase blocks) or a plain text file
(the whole file is treated as body text).
"""
import json
import re
import sys

UNIVERSAL_BANNED = [
    "at its core", "what really matters", "the real question is",
    "let me be direct", "here's the thing", "here is the thing",
    "i'll be honest", "i will be honest",
    "i'm not saying", "i am not saying",
    "proven track record", "extensive experience", "deep expertise",
    "passionate about", "thrilled", "delighted", "honoured", "honored",
    "leverage", "synergy", "cutting-edge", "state-of-the-art",
    "world-class", "seamless", "robust", "holistic", "dynamic",
    "innovative", "impactful", "spearheaded", "empower", "elevate",
    "unlock", "navigate", "landscape", "journey", "tapestry", "testament",
    "delve", "foster", "cultivate", "harness", "underscore", "pivotal",
    "crucial", "vital", "game-changer", "fast-paced world", "ever-evolving",
]

EN_BANNED = [
    "i am writing to express my interest",
    "i am excited to apply",
    "please find attached my resume",
    "with great enthusiasm",
    "as a passionate",
    "i hope this message finds you well",
    "thank you for considering my application",
    "i look forward to the opportunity to discuss",
]

DE_BANNED = [
    "hiermit bewerbe ich mich",
    "mit großem interesse habe ich ihre anzeige gelesen",
    "mit grossem interesse habe ich ihre anzeige gelesen",
    "ich bin ein motivierter teamplayer",
    "hochmotiviert", "teamplayer", "belastbar", "kommunikationsstark",
    "zielorientiert",
    "ich bringe leidenschaft mit",
    "ihr unternehmen ist ein global player",
    "ich bin überzeugt, dass ich die ideale besetzung bin",
    "spannende herausforderung",
    "mit großem interesse", "mit grossem interesse",
]

NOT_X_BUT_Y = [
    re.compile(r"\bnot (just|only)\b.{0,60}\bbut\b", re.IGNORECASE),
    re.compile(r"\bnicht nur\b.{0,60}\bsondern auch\b", re.IGNORECASE),
    re.compile(r"\bsowohl\b.{0,60}\bals auch\b", re.IGNORECASE),
]

WORD_COUNT_RANGE = {"en": (200, 350), "de": (250, 400)}


def _extract_from_plan(plan):
    parts = []
    body_paragraphs = []
    for block in plan.get("blocks", []):
        role = block["role"]
        if role in ("subject", "salutation", "closing_phrase"):
            parts.append(block["text"])
        elif role == "body":
            text = "".join(seg.get("text", "") for seg in block["segments"])
            parts.append(text)
            body_paragraphs.append(text)
    return "\n\n".join(parts), body_paragraphs


def lint(lang, text, body_paragraphs=None):
    findings = []

    if "—" in text:
        findings.append("Em dash (—) found — banned in every letter, use a comma or full stop instead.")

    for pat in NOT_X_BUT_Y:
        if pat.search(text):
            findings.append(f'"Not X but Y" / triad-style construction found: matches pattern {pat.pattern!r}')

    lowered = text.lower()
    for phrase in UNIVERSAL_BANNED:
        if phrase in lowered:
            findings.append(f'Banned phrase found: "{phrase}"')

    lang_list = EN_BANNED if lang == "en" else DE_BANNED
    for phrase in lang_list:
        if phrase in lowered:
            findings.append(f'Banned {lang.upper()} phrase found: "{phrase}"')

    if body_paragraphs and len(body_paragraphs) >= 3:
        first_words = [p.strip().split(" ", 1)[0].lower() for p in body_paragraphs if p.strip()]
        for w in set(first_words):
            if first_words.count(w) >= 3:
                findings.append(f'{first_words.count(w)} body paragraphs all open with "{w}" — vary sentence structure.')

    word_count = len(text.split())
    lo, hi = WORD_COUNT_RANGE[lang]
    if word_count < lo:
        findings.append(f"Word count {word_count} is below the {lo}-{hi} target range for {lang.upper()} — may read as thin.")
    elif word_count > hi:
        findings.append(f"Word count {word_count} is above the {lo}-{hi} target range for {lang.upper()} — longer is not more convincing.")

    return findings, word_count


def main():
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    lang = sys.argv[1].lower()
    if lang not in ("de", "en"):
        print("Language must be 'de' or 'en'.", file=sys.stderr)
        sys.exit(2)
    path = sys.argv[2]

    if path.endswith(".json"):
        with open(path, encoding="utf-8") as f:
            plan = json.load(f)
        text, body_paragraphs = _extract_from_plan(plan)
    else:
        with open(path, encoding="utf-8") as f:
            text = f.read()
        body_paragraphs = [p for p in text.split("\n\n") if p.strip()]

    findings, word_count = lint(lang, text, body_paragraphs)

    print(f"Word count: {word_count} (target {WORD_COUNT_RANGE[lang][0]}-{WORD_COUNT_RANGE[lang][1]} for {lang.upper()})")
    if not findings:
        print("No mechanical issues found. Still run the genericness read-aloud test by hand.")
    else:
        print(f"{len(findings)} issue(s) found:")
        for f_ in findings:
            print(f"  - {f_}")
        sys.exit(1)


if __name__ == "__main__":
    main()
