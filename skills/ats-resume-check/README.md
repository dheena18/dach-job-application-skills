# ats-resume-check

A standalone agent skill: checks whether a resume will parse
correctly in an Applicant Tracking System, independent of any translation
or tailoring work. Read-only — it reports, it never edits your file.

## Why this is separate from the translation/tailoring skills

Both `cv-translate-de` and `resume-tailor` need to verify their own output
is ATS-safe, and both call this same check as part of their pipeline. But
"is my resume ATS-friendly" is also a question worth asking on its own —
about a resume you haven't changed at all, or right before submitting one
you built by hand. This skill exists so you can ask that question directly
without running a full translation or tailoring pass first.

## What it checks

- **Document structure** (from the actual `.docx`): real tables, multi-
  column layouts, header/footer content, embedded images/text boxes —
  the layout patterns genuinely documented to break parsing across most
  ATS vendors.
- **Extracted text** (from the PDF): a text layer actually exists, contact
  info is present as plain readable text, section headings extract in
  correct top-to-bottom order (the fingerprint of a scrambled multi-column
  layout), and nothing extracted as a corrupted/replacement character.

## What it deliberately does not do

- It doesn't simulate Workday, Greenhouse, or any specific vendor's actual
  parser — no tool can, without a live tenant to test against.
- It doesn't score keyword/content match against a job posting — that's
  `resume-tailor`'s job.
- It doesn't rewrite anything. Findings only.

## How to use it

Ask your AI agent something like: *"check if my resume is ATS-friendly"*, *"will
Workday parse this correctly"*, *"scan this CV for ATS issues"*. Give it
your `.docx` (and a PDF if you have one exported already — otherwise it'll
ask you to export one, since the structural check specifically needs the
source document).

## On specific platforms

Real ATS behavior is more fragmented than most resume advice implies —
some platforms (Greenhouse) don't algorithmically score resumes at all;
others (iCIMS) do. See `references/what-ats-actually-do.md` for what's
actually documented per platform, including a genuinely interesting one:
HackerRank's 2026 open-source ATS scores heavily on Open Source
Contributions and Personal Projects sections specifically — and has
documented scoring inconsistency (the same unchanged resume scored 66 to
99 across repeated runs), so treat any score from it as noisy, not
authoritative.

## Files

```
ats-resume-check/
├── SKILL.md
├── references/
│   ├── what-ats-actually-do.md   Real per-vendor behavior vs. the
│   │                             "universal ATS algorithm" myth
│   └── mechanical-checks.md      Exactly what's checked, and the check's
│                                 own honest blind spots
```

Scripts live in `skills/_shared/scripts/`: `check_ats.py` (docx structural
check + PDF text check), `ats_score.py` (Workday/HackerRank-style scoring
estimates) and `keyword_audit.py`.

## Requirements

Python 3 with the packages in the repo's `requirements.txt` (`pip install -r requirements.txt`).
