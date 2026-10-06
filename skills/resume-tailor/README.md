# resume-tailor

An agent skill that tailors an existing resume/CV to a specific job
posting — for English and German markets — while keeping the document's
exact visual format and never inventing a qualification.

## What it does

- Extracts a job posting's real requirements and splits must-have from
  nice-to-have (Muss-/Kann-Kriterien for German postings).
- Builds an honest fit table against your actual experience — including
  telling you plainly when a posting is a stretch, not just when it's a
  good match.
- Reorders and rewords real content so the most relevant experience leads,
  using the posting's true terminology where it's already true of your
  background.
- Never invents a skill, tool, title, date, or metric to close a gap.
- Guards specifically against the "obviously AI-tailored" tell — a
  suspiciously perfect keyword match, mirroring every required skill in
  the posting's own order, listing a tool with no evidence of how it was
  used, or every bullet suddenly echoing the same verb the posting used.
  These are documented, recruiter-recognized signatures distinct from
  generic "sounds like AI" writing.
- Preserves the document's exact format by reassigning content across the
  resume's existing paragraph slots rather than physically moving anything
  in the file — the safer, well-supported approach (see
  `references/format-pipeline.md` for why the alternative is genuinely
  fragile).
- Checks the tailored result for ATS-parseability before calling it done.

## What it does not do

- Translate a resume between languages — that's `cv-translate-de`.
- Check ATS-compatibility as a standalone task with no tailoring involved
  — that's `ats-resume-check` (this skill calls the same check internally).
- Write a cover letter.
- Fabricate anything. If a requirement isn't met, the fit table says so.

## How to use it

Give your agent your resume and a job posting (paste the text, a link, or a
file) and ask to tailor it — or just paste a posting and your resume
together and ask why you're not hearing back from applications like it.

You'll be asked which file is your master/base resume if that's not clear
— tailoring always works from a designated master, and produces a new file
per application rather than editing that master or re-tailoring an
already-tailored file.

## Output

Both `.docx` and `.pdf`, named to identify the target application (e.g.
`Firstname_Lastname_Resume-Acme.docx`), saved separately from your master
resume so multiple tailored versions never collide.

## Requirements

Same as `cv-translate-de`, plus `simplemma` (small, pure-Python, zero heavy
dependencies — used for basic English/German lemmatization in the keyword
matcher, e.g. recognizing "system" and "systems" as the same word):
Python 3 with `python-docx`, `pywin32`, `simplemma`,
`defusedxml`, and `pypdf` installed; Microsoft Word for accurate page-count
checking (Windows-only for that specific step).

## Files

```
resume-tailor/
├── SKILL.md
├── references/
│   ├── fit-and-keywords.md            Extraction/matching methodology,
│   │                                  the fit table, the ATS reality check
│   ├── avoiding-ai-tailored-tells.md  The tailoring-specific guardrails
│   ├── german-tailoring.md            Muss/Kann, bilingual mirroring,
│   │                                  DACH ATS landscape
│   └── format-pipeline.md             Fixed-slot reassignment strategy,
│                                      master-resume principle
└── scripts/
    ├── keyword_audit.py       Deterministic keyword diff (docx-aware,
    │                          bilingual EN/DE), adapted from the
    │                          job-application-kit reference project
    ├── docx_inspect.py        (shared design with cv-translate-de)
    ├── docx_rewrite.py        (shared design with cv-translate-de)
    ├── check_pages.py         (shared design with cv-translate-de)
    └── check_ats.py           (shared design with ats-resume-check)
```

These scripts are copied rather than cross-referenced from the other
skills, so `resume-tailor` works standalone even if the others aren't
installed. If you improve one copy, consider updating the others.
