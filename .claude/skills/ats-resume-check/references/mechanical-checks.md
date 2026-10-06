# What the check actually verifies, and its real blind spots

## Two independent passes, run both

1. **DOCX structural check** (`check_ats.py docx <file>`) — inspects the
   document's own XML directly: real tables, multi-column sections,
   header/footer references, embedded images/drawings/text boxes. This is
   the more authoritative pass, because it looks at the actual structure
   rather than inferring it from how one PDF renderer's text extraction
   happened to come out.
2. **PDF text check** (`check_ats.py pdf <file> [options]`) — exports (or
   is given) a PDF, extracts its text, and checks: a text layer exists at
   all (not a scanned image), contact info (name/email/phone) is present
   as plain extractable text, no Unicode replacement or Private-Use-Area
   characters (silent bullet/glyph corruption — invisible to the eye,
   breaks parsing anyway), and — if you pass `--headings-in-order` — that
   section headings extract in top-to-bottom order, which is the
   fingerprint check for a scrambled multi-column read.

Run `check_ats.py both <docx> <pdf> [pdf-options]` to do both in one call.

## Known blind spots — know these, don't oversell a clean result

- **The heading-order check only validates the headings you pass in**, not
  everything between them. A scrambled two-column body between two
  correctly-ordered headings would still pass. It's a fingerprint check,
  not an exhaustive reading-order proof.
- **It tests one PDF extraction library's output** (`pypdf`). A different
  vendor's parser — Workday-class systems often license one from
  Textkernel/Sovren or similar — can order or structure text differently
  on the identical PDF. A pass here is evidence, not a guarantee for every
  vendor.
- **It cannot simulate a "resume upload → autofill structured fields"
  flow at all.** That's arguably the single most consequential failure
  mode for platforms like Workday that auto-populate application forms
  from a parsed resume, and it genuinely can't be checked offline without
  a live tenant.
- **Non-English or non-standard section names** (e.g. German headings like
  "Persönliche Projekte", or a creative heading like "What I'm About")
  are likely to land in a structured-autofill system's generic/other
  bucket rather than a matching field, even when the text itself parses
  perfectly fine. That's a property of the section name, not something a
  mechanical check catches or something this skill can fix — it's worth
  one line of disclosure to the user rather than silence.
- **A clean result is a necessary check, not a quality or match score.**
  It tells you the document won't break on the mechanical failure modes.
  It says nothing about whether the content is a good fit for a posting —
  that's `resume-tailor`'s job — or whether the writing sounds native and
  human — that's `cv-translate-de` / `resume-summary-writer`'s job.

## Layout patterns, confirmed safe vs. confirmed risky

- **Safe**: single column, tab-stop-aligned title/date lines (a plain
  paragraph with a right-aligned tab stop, not a table), plain glyph
  bullets (not auto-numbered lists), no headers/footers, no images.
- **Confirmed by direct XML inspection, worth knowing**: a resume section
  heading (e.g. "WORK EXPERIENCE") that's just a bolded, colored, capitalized
  run — not a Word heading style (`pStyle`) — is fine for the text-heuristic
  parsing most ATS actually do, but invisible to any parser that specifically
  looks for semantic heading styles rather than reading plain text. Not
  disqualifying, and probably not worth restructuring a resume's whole
  styling over, but worth disclosing rather than assuming a bolded run and
  an actual Heading style are equally recognized.
- **Risky**: any real table (including one used only for layout, like a
  two-column title/date row), a multi-column section layout, content
  placed in a header or footer, icons/skill-bar graphics/photos, and
  auto-numbered lists if content ever gets reordered or partially deleted
  (numbering can shift or restart unexpectedly).
