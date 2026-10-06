# cv-translate-de

An agent skill that rebuilds an English resume (.docx) into professional,
natively-written German — while keeping the original file's exact visual
format: fonts, colors, bold/italic placement, bullet and tab layout, and page
count.

## What this is, in one sentence

Not a translation. A full German-native rebuild of the same facts, in the
same document, with the same look.

## What it does

- Reads the structure of your resume's `.docx` file (every paragraph, every
  run, its exact color/bold/size) so it knows precisely what formatting to
  reproduce.
- Rewrites the content into German that reads as written by a native German
  speaker for the German job market — correct grammar, correct register
  (sachlich, not American-style self-promotion), no machine-translation
  tells (no em dashes, no stock AI phrases, correct DIN number/date
  formatting).
- Keeps every fact identical: employers, dates, metrics, tool names, degree
  titles. Only the language and sentence construction change.
- Decides what to translate and what to leave alone: tool/framework names,
  certifications, and common English job titles stay in English (the German
  tech market uses them natively); country names and generic descriptive
  words become German; degree titles, institution names, and dates are
  never altered.
- Verifies its own output: validates the file isn't corrupted, checks the
  real page count by actually opening it in Word, lints for mechanical
  German-typography mistakes, and checks the exported PDF for the kind of
  problems that break ATS parsers (Workday, Personio, SAP SuccessFactors,
  etc.) — missing text layer, broken reading order, unreadable contact
  info.
- If the German text doesn't fit the original page count (it usually runs
  20-35%+ longer than English), it tightens phrasing first, and only
  touches paragraph spacing — never font size — if you've said that's okay.

## What it does not do

- It doesn't tailor content to a specific job posting (that's a separate,
  future skill).
- It doesn't write cover letters.
- It doesn't invent, drop, or improve on any fact, claim, or number from
  your original resume.

## How to use it

Ask your AI agent something like: *"translate my resume to German"*, *"I need a
German Lebenslauf version of this CV for a job in Munich"*, or paste/point
to your `.docx` and say you need the German version. The skill triggers on
resume/CV/Lebenslauf + English→German context, even if you don't mention
formatting — preserving the layout is a hard requirement here, not optional.

You'll be asked for (if not already given):
- The source `.docx` file.
- Confirmation of your target page count (default: match the source).
- Confirmation of any ambiguous degree-title wording (so it matches your
  actual certificate, not a guess).

## Output

Both a `.docx` and a `.pdf`, saved to `output/cv-translate-de/` (never next
to or over your source file), named after your original file with a `-DE`
suffix: `YourResume.docx` → `YourResume-DE.docx` and `YourResume-DE.pdf`.

## Requirements

- Microsoft Word installed (used via COM automation for accurate page-count
  checking and PDF export — this is more accurate than a generic converter
  since it's the same rendering engine you'd actually open the file in).
- Python 3 with `python-docx`, `pywin32`, `defusedxml`, and `pypdf`
  installed (`pip install python-docx pywin32 defusedxml pypdf`).
- Windows (the page-count/PDF-export step uses Word COM automation, which
  is Windows-only; the rest of the pipeline is platform-independent).

## Files in this skill

```
cv-translate-de/
├── SKILL.md                          Entry point: process, rules, when to load what
├── references/
│   ├── native-german-style.md        Sounding native, not translated: typography,
│   │                                 grammar traps, banned AI/translation phrases
│   ├── terminology-and-facts.md      What to translate vs. keep untouched
│   └── format-pipeline.md            The technical docx/page-count/ATS pipeline,
│                                     step by step, including overflow handling
└── scripts/
    ├── docx_inspect.py               Dumps a docx's exact paragraph/run structure
    ├── docx_rewrite.py               Applies a rewrite plan, preserving formatting
    ├── scale_spacing.py              Approved-only spacing compression (never font)
    ├── check_pages.py                Real page count + PDF export via Word COM
    ├── lint_german.py                Mechanical German-typography/AI-tell scan
    └── check_ats.py                  ATS-readability check on the exported PDF
```

## Known limitations

- The ATS check catches mechanical failure modes (no text layer, broken
  reading order, encoding corruption) — it cannot simulate any specific
  vendor's parser or a "resume upload → autofill fields" flow. A clean
  result is a necessary check, not a guarantee for every ATS.
- Non-English section names (e.g. "Persönliche Projekte") may not map to a
  structured-autofill system's fixed fields even when the text itself
  parses fine — a property of having those sections at all, not something
  this skill can avoid.
- Built and tested on Windows with Microsoft Word available. The Word-COM
  dependency in `check_pages.py` would need a LibreOffice-based substitute
  on macOS/Linux.
