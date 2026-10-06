---
name: cover-letter-writer
description: >
  Write a cover letter / Anschreiben for a specific job posting, in English
  or German, built from the candidate's real resume and the posting's actual
  requirements — never a rerun of the resume in prose, and never a generic
  template with just the company name swapped in. Selects 2-3 achievements
  by relevance to the posting and elaborates each with the context and
  reasoning a resume bullet can't hold (Context-Action-Result), matches tone
  to the company's culture (sachlich-but-specific for German corporates and
  Mittelstand, more direct for startups in either language), and outputs a
  .docx styled to match the candidate's resume (same font, name treatment,
  accent color) so the two documents read as one application package. Use
  this whenever the user asks for a cover letter, Anschreiben, or motivation
  letter for a specific job, alongside a resume and a posting. Does not
  tailor the resume itself (that's `resume-tailor`) and does not check
  ATS-parseability (that's `ats-resume-check`).
---

# Cover letter writer

A cover letter earns its place by saying something the resume format
cannot: the context behind a result, the reasoning behind a choice, and one
detail that proves this letter was written for this company. Read
`references/persuasion-and-evidence.md` before drafting anything —
it explains why restating the resume in prose is the single most common
failure mode. For the actual layout, read `references/letter-structure-en.md`
or `references/letter-structure-de.md` depending on target language. For
German output, also read `references/tone-and-culture-calibration.md` before
choosing register. **Correct structure is not the same as good prose** —
read `references/sentence-flow-and-hooks.md` before drafting sentences, not
just paragraphs: a letter with the right paragraphs in the right order can
still read like an email if the sentences inside each paragraph just list
facts instead of arguing a case. For styling the output file, read
`references/visual-consistency.md`. Before finalizing any letter, read
`references/fact-and-claim-discipline.md` — every item in it is a mistake a
verification pass actually caught in a real test letter (an invented
causal claim, a company fact that turned out to be wrong, a timeframe
claim stretched past what the resume evidences), not a hypothetical, and
they keep being the kind of thing that's easy to miss on a single read-
through.

## Process

1. **Get the inputs.** The full posting text, the resume actually being
   submitted for this application (prefer an already-tailored version for
   this posting if `resume-tailor` produced one; otherwise the master),
   the target language, and anything the posting gives you: a named
   contact, a reference number (Kennziffer), a salary or start-date
   question to answer.
2. **Select 2-3 achievements**, chosen for relevance to this posting's top
   requirements, not comprehensiveness. If a fit table already exists for
   this posting (from `resume-tailor`), use it; otherwise do the match by
   hand. Never pick more than 3 — see `persuasion-and-evidence.md`.
3. **Read the posting's register** and pick where this letter sits on the
   sachlich-to-personable (DE) or measured-to-direct (EN) spectrum — see
   `references/tone-and-culture-calibration.md`. Company type, the
   language the posting itself uses, and any "Du"/"Sie" signal all matter.
4. **Draft** following `letter-structure-en.md` or `letter-structure-de.md`:
   a hook tied to one specific, checkable fact about the company or role
   (never a generic opener), 2-3 CAR-framed proof points each ending with a
   forward connector to what this employer needs, a fit paragraph naming
   one concrete detail about the company, a close with availability/notice
   period/salary-if-asked and a plain invitation to talk. While drafting,
   apply `sentence-flow-and-hooks.md` at the sentence level: subordinate
   supporting facts to the claim they support instead of listing them as
   separate same-weight sentences, use a causal/consequential connector
   (not just "and"/"also"/a semicolon) at least once per achievement
   paragraph, and vary sentence length within each paragraph.
5. **Handle any crucial gap the posting names as a hard requirement** using
   the same ask-the-user-first policy `resume-tailor` uses for gaps —
   do not decide unilaterally whether or how to address it. If addressing
   one, follow `references/gap-and-weakness-framing.md`: brief, factual,
   immediate pivot to readiness. Never manufacture a confession for
   something the posting never asked about.
6. **Extract the resume's style** by running `skills/_shared/scripts/docx_inspect.py` on
   the actual resume file being submitted for this application — see
   `visual-consistency.md` for what to pull out (heading font/color, accent
   color, body font/size, dates color if used).
7. **Build the plan and generate the docx**: write the letter content as a
   plan (see the docstring in `skills/cover-letter-writer/scripts/build_cover_letter_docx.py`) and run
   it against the extracted style profile.
8. **Lint it**: run `skills/cover-letter-writer/scripts/lint_letter.py <de|en> <file.txt or plan.json>`
   against `references/banned-phrases-de-en.md`. Fix everything flagged —
   don't just note it and move on.
9. **Check length**: `python skills/_shared/scripts/check_pages.py pages <file.docx>` (uses Word on Windows if present, otherwise LibreOffice; needs `pip install -r requirements.txt`) must report
   1. Word count should land inside the target range given in the relevant
   `letter-structure-*.md` file — longer is not more convincing.
10. **Run the genericness test** (this cannot be scripted): read the
    finished letter and ask whether it could go to a different company with
    only the name swapped. If yes, find the detail that makes that false
    and add it.
11. **Run the fact-and-claim-discipline checklist** from
    `references/fact-and-claim-discipline.md` against the finished draft —
    every causal claim, every company fact, every timeframe scope, every
    present-tense claim against the resume's actual dates, the closing
    line's voice (active, not passive). This is a separate pass from the
    genericness test: genericness asks whether the letter is specific
    enough, this asks whether everything specific in it is actually true.
12. **Save the output**, never overwriting the resume or a cover letter
    already written for a different application: see "Output naming" below.
13. **Report back**: which achievements were chosen and why, the tone
    decision, any gap addressed and how, word/page count, and the verify
    list from `letter-structure-en.md`/`letter-structure-de.md` (contact
    name spelling, company legal name, job title exactly as posted,
    reference number, every number in the letter, the date).

## Output location and naming

Always save the finished letter (`.docx` and matching `.pdf`) into this
project's `output/cover-letter-writer/` folder — never into the resume's
own folder, the project root, or a scratch/temp directory, and never just
hand back an in-conversation draft without writing the files. Create the
folder if it doesn't exist yet.

Name the files `<original-filename>-CoverLetter-<Company>-<YYYY-MM-DD>.docx`
and the matching `.pdf`, using the date the letter is generated, in ISO
format so filenames sort correctly and the German/English date-format
ambiguity never comes up in a filename (e.g.
`output/cover-letter-writer/Firstname_Lastname_Resume-CoverLetter-Acme-2026-09-27.docx`).
Never overwrite the resume or a cover letter already written for a
different application.

## Rules that never bend

- Never invent an achievement, number, or fact that isn't already true and
  evidenced — on the resume, or explicitly given by the user in
  conversation.
- Never restate a resume bullet near-verbatim. Elaborate with context or
  reasoning the resume format can't hold, or leave it out.
- Never use a banned opener, closer, or filler phrase from
  `banned-phrases-de-en.md`, in either language.
- Never exceed one page.
- Never guess a hiring manager's name or a reference number that wasn't
  given — ask, or fall back to the generic salutation.
- German default register is sachlich. Do not add American-style
  superlatives to a German letter even if the English letter for the same
  posting is written more directly.
- Never use real content from any user's resume as an example when editing
  this skill's own instructions — keep this file and its references
  generic.

## Verifying your own output

Before calling this done: `lint_letter.py` and `check_pages.py` both pass,
the genericness test and the `fact-and-claim-discipline.md` checklist were
both actually run (not skipped), every claim traces to real evidence, and
the verify list was produced for the user.
