---
name: cv-translate-de
description: >
  Rebuild an English resume/CV into professional, natively-written German
  (Lebenslauf) while preserving the original .docx file's exact visual
  format — fonts, colors, bold/italic placement, bullet and tab layout, and
  page count. This is a full native rebuild, not a literal or machine
  translation: sentence logic, verb choice, and register are reconstructed
  the way a German native would actually write them, while every fact,
  number, tool name, employer, date, and claim stays identical to the
  source. Use this whenever the user wants their resume/CV/Lebenslauf
  translated, converted, or rebuilt from English into German, wants a
  German version of an existing CV for a DACH job application, or asks to
  "translate my resume to German" — even if they don't mention formatting,
  since preserving the original layout is a hard requirement here, not an
  optional nice-to-have. Do not use this for tailoring a resume's content
  to a specific job posting, or for cover letters — those are separate
  concerns.
---

# CV translate: English → German (format-preserving rebuild)

## What this skill is, and isn't

This produces a German Lebenslauf that reads as if a German native wrote it
from scratch, using the same underlying facts as the English original, laid
out in the exact same .docx file. It is not a tailoring skill (reordering
content for a specific job posting) and not a cover-letter skill. It only
rebuilds the language of an existing resume.

Read this file fully before starting. Load the reference files as follows:

| When | Read |
|---|---|
| Before writing any German sentence | `references/native-german-style.md` |
| Deciding what to translate vs. keep as-is (tool names, job titles, degree titles, company names) | `references/terminology-and-facts.md` |
| Rebuilding the summary/positioning paragraph at the top of the resume | `references/summary-writing.md` — read this before touching that paragraph specifically; it is not translated the same way a bullet is |
| Doing the actual docx rewrite, checking page count, handling overflow | `references/format-pipeline.md` |

## The two things that make this hard, and how this skill handles them

1. **Sounding native, not translated.** A literal translation reads as
   foreign syntax with German words even when every word is technically
   correct. `native-german-style.md` is the concrete checklist (typography,
   banned stock phrases, sentence structure, register, grammar traps) built
   from research into what actually marks German text as machine-translated
   or AI-generated versus native.
2. **Format has to survive the fact that German is longer.** German
   commonly runs 20-35% longer than English for the same content, more for
   short strings like bullets and titles. The source document may already
   be at its page limit. `format-pipeline.md` gives the exact procedure
   (inspect → draft → build a run-level rewrite plan → apply → validate →
   render and check real page count → compress in a defined order if
   needed → lint → look at it) so format-preservation is verified, not
   assumed.

## Process

1. **Get the input file and confirm scope.** Ask for the source .docx if not
   given. Confirm: is this a full rebuild of the whole document, or specific
   sections? What is the target page count (default: match the source
   exactly)? Is there a specific German-titled degree/certificate wording to
   use (see `terminology-and-facts.md` on degree titles) rather than
   guessing?
2. **Inspect the source structure** with `scripts/docx_inspect.py` — don't
   skip this even for a document you've already read visually. The visual
   read tells you what it says; the structural inspect tells you exactly
   which runs carry which formatting, which is what you need to reproduce it.
3. **Draft the German content as plain text first**, paragraph by paragraph,
   applying `native-german-style.md` and `terminology-and-facts.md`. Keep a
   running awareness of length: if a bullet is visibly much longer in German
   than the English original, that is exactly the expansion risk the format
   pipeline warns about — look for a tighter native phrasing now rather than
   discovering an overflow at the end.
4. **Build the rewrite plan and apply it**, following
   `format-pipeline.md` steps 3 onward: build `plan.json`, run
   `docx_rewrite.py`, validate, render, check the real page count against
   the source, compress in the defined order if it overflowed (spacing
   adjustment via `scale_spacing.py` only once the user has agreed to it —
   never shrink font size, and don't give up on a moderate factor: real
   overflows have needed values well below 0.5), lint with
   `lint_german.py --plan plan.json` (always pass `--plan`, so untouched
   original-language titles aren't flagged as German mistakes), check
   ATS-readability on the exported PDF with `check_ats.py`, look at the
   actual rendered pages.
5. **Save both the `.docx` and the exported `.pdf`** to a separate output
   folder — never next to or over the source file — named
   `<original-filename>-DE.docx` / `-DE.pdf`. See "Output location and file
   naming" in `format-pipeline.md`.
6. **Report back**: what was translated, what was deliberately kept
   untouched and why (tool names, company names, degree title, etc.), the
   page-count check result, and anything you flagged for the user to
   confirm (an ambiguous job title, an uncertain degree title wording, a
   paragraph that wouldn't fit without cutting a fact).

## Rules that never bend

- Never invent, drop, or alter a fact, number, date, employer, tool, or
  claim. This is a language rebuild, not a content edit.
- Never guess a degree title, institution name, or job title translation
  when it might not match the person's actual certificate or contract —
  ask instead.
- Never silently shrink font size or margins to solve a page-overflow
  problem — that's a formatting decision for the user, not a default.
- Never write output over the source file or into the source file's folder.
- Never use real content from any user's resume as an example when editing
  this skill's own instructions — keep this file and its references
  generic.

## Verifying your own output

Before calling this done: run `scripts/lint_german.py --plan plan.json` on the result, check
the rendered page count matches the source, and actually look at the
exported PDF side-by-side with the source PDF. If anything is only "probably
fine", it isn't verified — check it.
