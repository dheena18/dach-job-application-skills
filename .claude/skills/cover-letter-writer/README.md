# cover-letter-writer

A Claude Code skill that writes a cover letter / Anschreiben for a specific
job posting, in English or German, built from your real resume and the
posting's actual requirements — styled to match the resume it's paired
with.

## What it does

- Selects 2-3 achievements by relevance to the posting, not comprehensiveness.
- Elaborates each with the Context-Action-Result framework, connecting it
  forward to what the employer actually needs — never a prose rerun of the
  resume.
- Matches tone to company culture: sachlich-but-specific for German
  corporates and Mittelstand, more direct for startups in either language
  — see `references/tone-and-culture-calibration.md`.
- Follows the same ask-before-deciding policy as `resume-tailor` for any
  crucial requirement the posting names that isn't fully met.
- Lints the draft against a real banned-phrase/AI-tell list in both
  languages before calling it done.
- Builds a `.docx` that inherits the resume's actual font, name-heading
  style, and accent color, so the resume and letter read as one
  application package instead of two separately-styled documents.
- Enforces the one-page rule using real Word rendering, not an assumption.

## What it does not do

- Tailor the resume itself — that's `resume-tailor`.
- Check ATS-parseability — that's `ats-resume-check`.
- Fabricate an achievement, number, or skill. If the fit is weak on a
  requirement, that gets flagged to you, not papered over.

## How to use it

Give Claude the job posting and the resume you're submitting for that
application (prefer an already-tailored version if one exists) and ask for
a cover letter, in English or German. You'll be asked how to handle any
crucial gap the posting names as a hard requirement, same as
`resume-tailor`.

## Output

Both `.docx` and `.pdf`, named
`<original-filename>-CoverLetter-<Company>-<YYYY-MM-DD>.docx`, saved
separately from the resume and from letters for other applications.

## Requirements

Python 3 with `python-docx` and `pywin32` installed; Microsoft Word for
accurate page-count checking (Windows-only for that specific step).

## Files

```
cover-letter-writer/
├── SKILL.md
├── references/
│   ├── letter-structure-en.md          English layout, 4-paragraph shape,
│   │                                    openers, tone-by-company table
│   ├── letter-structure-de.md          DIN 5008 layout, the 4 Absätze,
│   │                                    sachlich register
│   ├── persuasion-and-evidence.md      CAR framework, achievement
│   │                                    selection, why genericness is the
│   │                                    real memorability killer
│   ├── tone-and-culture-calibration.md EN/DE register contrast, reading
│   │                                    the posting's own signal
│   ├── gap-and-weakness-framing.md     When and how to address a named
│   │                                    hard-requirement gap
│   ├── banned-phrases-de-en.md         The mechanical AI-tell checklist,
│   │                                    both languages
│   └── visual-consistency.md           Extracting a style profile from
│                                        the resume, why this skill builds
│                                        a fresh docx instead of reassigning
│                                        content like the other skills do
└── scripts/
    ├── docx_inspect.py            (shared design with cv-translate-de /
    │                              resume-tailor, plus font-name extraction)
    ├── build_cover_letter_docx.py Builds a new styled docx from a content
    │                              plan + extracted style profile
    ├── lint_letter.py             Mechanical banned-phrase/word-count lint
    └── check_pages.py             (shared design with cv-translate-de)
```

These scripts are copied rather than cross-referenced from the other
skills, so `cover-letter-writer` works standalone even if the others
aren't installed. If you improve one copy, consider updating the others.
