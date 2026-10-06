---
name: resume-tailor
description: >
  Tailor an existing resume/CV to a specific job posting — reordering and
  rewording real content so the strongest, most relevant experience leads,
  using the posting's own true terminology where it applies — without
  inventing a skill, title, date, or metric that isn't already true. Works
  for both English and German (DACH) resumes and postings; German-market
  conventions (Muss-/Kann-Kriterien, bilingual keyword mirroring, the
  fragmented German ATS landscape) get their own handling. Preserves the
  resume's exact visual format (fonts, colors, bullet/tab layout, page
  count) the same way the whole document was originally built. Use this
  whenever the user pastes or references a job posting alongside their
  resume, asks to tailor/customize/target their CV for a specific role or
  company, or asks why they're "not getting interviews" for particular
  applications. Do not use this to translate a resume between languages
  (that's `cv-translate-de`) or to check ATS-parseability in isolation
  (that's `ats-resume-check`, which this skill also calls internally) or to
  write a cover letter.
---

# Resume tailor

Tailoring is reordering and rewording real content to fit a specific
posting — not a rewrite, and never an invention. Read
`references/fit-and-keywords.md` before analyzing any posting;
`references/avoiding-ai-tailored-tells.md` before writing or reordering
anything, in either language — over-tailoring has its own specific,
recognizable failure signature, distinct from generic AI-writing tells.
For German output, also read `references/german-tailoring.md` and
`cv-translate-de`'s `native-german-style.md`. For the actual docx mechanics,
read `references/format-pipeline.md` — it explains why this reuses
`cv-translate-de`'s safe fixed-slot content-reassignment approach instead
of physically reordering paragraphs.

## Process

1. **Get the master resume and the posting.** Ask which resume file is the
   master/base version if more than one exists — always tailor from the
   master, never re-tailor an already-tailored file (see the master-resume
   principle in `format-pipeline.md`). Get the full posting text, not just
   a summary of it.
2. **Build the fit table.** Run `skills/_shared/scripts/keyword_audit.py --exclude "Company
   Name,City"` (always pass the posting's actual company name and location —
   otherwise they show up in the output as "missing keywords," which they
   are not) as a starting point, then do the actual must-have/nice-to-have/
   gap analysis by hand. Target ~75-85% on the resulting score, not 90%+ —
   see `fit-and-keywords.md` for why higher is not better.
   Show the fit table to the user before touching the resume — including
   an honest verdict if the fit is weak. This is the point where telling
   the user "this posting is a stretch" is worth more than tailoring
   something that was never going to be competitive.

   Never report a keyword-match score without also showing the classified
   missing-term breakdown that produced it — a bare percentage answers
   nothing about what to actually do next, which is the point of running
   this in the first place. Every term keyword_audit.py lists as missing
   gets sorted into exactly one bucket, out loud, before or alongside any
   score: **noise** (the posting's own company name, generic filler words
   like "modern"/"scalable", bigram artifacts from two adjacent listed
   items), **true but differently worded** (the resume already supports
   this — say what change you're making and why, then make it), or
   **a real gap** (say so plainly, and don't close it by adding the word
   without the substance). Skipping straight to "the score is X%" and
   stopping there is an incomplete job even if the number itself is
   accurate.
3. **Inspect the master's structure** with `skills/_shared/scripts/docx_inspect.py` — you
   need the exact paragraph/run/formatting map before deciding which
   content goes where.
4. **Decide the reassignment**: which bullet's content (with its own bold-
   emphasis pattern) moves to which paragraph slot, which slots get
   trimmed to empty, what wording changes to mirror true posting language.
   Check every proposed change against `avoiding-ai-tailored-tells.md` —
   no perfect keyword-order matching, no tool listed with no evidence, no
   verb suddenly echoed across every bullet because the posting used it,
   no chase for a suspiciously perfect overall match.
5. **Apply and verify**, following `format-pipeline.md` steps 5 onward:
   build the plan, run `docx_rewrite.py`, validate, check real page count,
   run `skills/_shared/scripts/check_ats.py both` (the same check `ats-resume-check`
   performs standalone), look at the rendered PDF beside the master's.
6. **Save the tailored file** to `output/resume-tailor/`, named to identify the
   target application, never overwriting the master. See "Output location
   and naming" in `format-pipeline.md`.
7. **Report back**: the fit table, what was reordered and why, what was
   reworded and why (with the true evidence it's based on), what gaps
   remain unaddressed and whether they're worth a cover letter mentioning,
   and the verification results.

## Rules that never bend

- Never add a skill, tool, employer, title, date, or metric that isn't
  already true of the candidate. Tailoring reorders and rewords real
  content; it does not invent qualifications.
- Never change a job title to match the posting's title.
- Never chase a 100% or near-100% keyword match — a real resume has
  natural gaps, and a suspiciously perfect match is a named red flag to
  recruiters, not a win condition.
- Never physically reorder paragraph XML — reassign content across the
  existing fixed slots instead (see `format-pipeline.md`).
- Never overwrite the master resume, or tailor from an already-tailored
  file instead of the master.
- Never use real content from any user's resume as an example when editing
  this skill's own instructions — keep this file and its references
  generic.

## Verifying your own output

Before calling this done: the fit table was shown to the user, every added
or emphasized claim traces to real evidence, `check_ats.py` and page-count
checks pass, and a read-aloud pass confirms the resume would make sense to
someone who has never seen the job posting — not just to someone holding
the two documents side by side.
