---
name: ats-resume-check
description: >
  Check whether a resume/CV (.docx and/or the PDF exported from it) will
  parse correctly in an Applicant Tracking System — Workday, Greenhouse,
  Personio, SAP SuccessFactors, Softgarden, iCIMS, HackerRank's resume
  scoring, and similar. This is a standalone format/parseability check,
  independent of translating or tailoring a resume. Use this whenever the
  user asks to check, scan, or verify a resume for ATS-compatibility,
  asks "will this parse correctly in Workday", "is my resume ATS-friendly",
  or wants to know if a document's layout (tables, columns, headers,
  graphics) is safe before submitting it to job applications — even if
  they don't name a specific ATS. Do not use this to rewrite, translate, or
  tailor the resume's content — this skill only checks and reports; for
  content changes use `cv-translate-de` (English→German) or `resume-tailor`
  (matching a job posting) instead, though both of those call this same
  check internally as part of their own pipelines.
---

# ATS resume check

A standalone, non-destructive check. It reads a resume and reports
findings; it never edits the file. If the user wants something fixed, tell
them what's wrong and point at the skill that would actually fix it —
`cv-translate-de` or `resume-tailor` for content, or fix the layout
yourself if it's a one-off formatting issue they want handled directly.

Read `references/what-ats-actually-do.md` first if you haven't already in
this session — it corrects the "beat the ATS algorithm" framing most
resume advice assumes, and explains why the check here is about structural
parseability, not a universal match score (there isn't one). Read
`references/mechanical-checks.md` for exactly what the script checks and,
just as important, what it doesn't.

## Process

1. **Get the file(s).** Ask for the `.docx` if you only have a PDF — the
   structural check (tables, columns, headers, images) needs the source
   document, not just its rendered output. If there's no `.docx` available,
   run the PDF-only check and say plainly that the structural pass was
   skipped.
2. **Run both checks:**
   ```
   python scripts/check_ats.py both <file.docx> <file.pdf> \
     --email <email> --phone <phone> --name <full name> \
     --expect-pages <n> --headings-in-order <SECTION1> <SECTION2> ...
   ```
   If you don't have a PDF yet, export one first (Word/LibreOffice, or
   reuse `cv-translate-de`'s `check_pages.py` pattern if that skill is
   present) — don't skip the PDF pass just because it takes an extra step.
3. **Report findings plainly**, split into what's a real parsing risk
   (table, multi-column layout, header/footer content, missing text layer,
   broken reading order, encoding corruption) versus what's a softer,
   system-specific consideration (a non-English section name possibly not
   mapping to a structured-autofill field; HackerRank's specific scoring
   rubric rewarding an Open Source/Projects section, which is a
   scoring-criteria note, not a parsing defect).
4. **Never overstate a clean result.** "No findings" means the mechanical
   failure modes are ruled out — it does not mean "this will score well,"
   "this will pass Workday," or anything about content quality or job fit.
   Say that explicitly rather than letting a clean report read as a
   guarantee.

## Output style

Lead with a plain verdict (safe / has real issues), then the specific
findings, then anything worth knowing that isn't a defect (the autofill-
mapping caveat, the HackerRank rubric note) clearly separated from the
actual findings.
