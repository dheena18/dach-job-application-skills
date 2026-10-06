# Format-preservation pipeline

The point of this pipeline: the output .docx must look, to the pixel, like
the input .docx opened in the same font — same colors, same bold/italic
placement, same bullet/tab layout, same page count — with only the language
of the words changed. Nothing here decides *what* the German should say;
that's the model's job, guided by `native-german-style.md` and
`terminology-and-facts.md`. This file is about not breaking the document
while doing it.

## Why English → German is a real risk to the layout, not a theoretical one

German runs longer than English for the same content — commonly 20-35% for
normal prose, but short strings (which is exactly what a resume bullet or a
job-title line is) can expand 60-100%+. A resume that is already tight at
its page limit in English is not guaranteed to fit in German. Budget for
this explicitly instead of discovering it after the fact.

## Step by step

### 1. Inspect before writing anything

```
python skills/_shared/scripts/docx_inspect.py <input.docx> structure.json
```

Read `structure.json`. For every paragraph you plan to rewrite, note:
- Its exact current text (this is the content to translate).
- Whether it's a bullet (`is_bullet`), has a right-aligned tab (a
  title/date line), or is plain body text.
- The `bold` / `color` / `size_pt` pattern of its runs. This is the palette
  you must reuse — do not invent new colors or sizes.

A paragraph with multiple runs of different formatting (e.g. plain text with
one bold phrase in the middle, or a bold role/company segment followed by a
bold-grey date segment after a tab) is telling you where the emphasis and
the tab boundary go. Preserve that structure in the German version: if the
English bullet bolds the key metric, the German version bolds the
translated key metric, at the equivalent position.

### 2. Draft the German content, in full, before touching the docx

Write out every rewritten paragraph as plain text first (in chat or a scratch
file), applying `native-german-style.md` and `terminology-and-facts.md`.
Get this right before it becomes a formatting exercise — it's much easier to
fix wording as text than after it's embedded in a run-segment plan.

### 3. Build the rewrite plan

Turn the drafted German text into `plan.json`: one entry per paragraph index,
each with a `segments` list carrying the exact same bold/color/size pattern
you recorded in step 1 for that paragraph, just with the new German text (see
`skills/_shared/scripts/docx_rewrite.py` docstring for the exact schema).

Where a bullet's English version bolds a phrase mid-sentence, split your
German segments the same way: normal-run, bold-run, normal-run — matching
positions, not necessarily matching word-for-word boundaries, since German
word order will differ.

### 4. Apply it

```
python skills/_shared/scripts/docx_rewrite.py <input.docx> plan.json <output.docx>
```

This only touches the runs inside the paragraphs listed in the plan. Every
other paragraph, and every paragraph-level property (alignment, tab stops,
bullet numbering, spacing), is untouched because the script never edits
`<w:pPr>`.

### 5. Validate the XML didn't get corrupted

```
python skills/_shared/scripts/validate_docx.py <output.docx>
```

(Portable check shipped with this repo: valid zip, required parts present,
every XML part well-formed, opens in python-docx.) A clean validation means
the file is structurally sound; it says nothing about content or page count.

### 6. Check the page count against reality

python-docx cannot compute layout, so the page count has to come from an
actual rendering engine. This environment has Microsoft Word installed but
not LibreOffice, so use Word via COM automation:

```
python skills/_shared/scripts/check_pages.py both <output.docx> <output.pdf>
```

Compare the printed `pages=` value against the original document's page
count (get it the same way, on the original file). They must match — this
skill's whole promise is "same format", and page count is part of format.

### 7. If it overflows

Try these in order. Steps 1-2 are always fine to do on your own judgment.
Step 3 changes the document's visual density (even though it never touches
font size), so only do it once the user has said spacing adjustments are
okay — don't assume it's pre-approved for a document you haven't discussed
this with the user on. Never reach for step 4 silently either:

1. **Tighten phrasing, not content.** German CV fragments are naturally
   terser than narrated English corporate bullets (no "I", no filler verbs,
   no subordinate clauses) — this is real, available slack, not a
   compromise. Re-read every rewritten bullet for a shorter way to say the
   exact same fact before touching anything else. Prefer verb-first
   fragments matching the source's own structure (see
   native-german-style.md) — they also tend to run shorter than the
   noun-phrase alternative, so getting the grammar register right and
   getting the length down usually point the same direction.
2. **Drop redundant articles/connectors where grammatically valid** in
   fragment-style bullets (a documented, industry-standard compression
   technique for exactly this length-expansion problem). Never drop a word
   that carries an actual quantity, qualifier, or fact — "over 100" losing
   its "over" is a fact change, not a compression.
3. **Scale down paragraph spacing, once the user has agreed to it** — use
   `skills/cv-translate-de/scripts/scale_spacing.py <in> <factor> <out>` with a factor like 0.75.
   This only touches the gaps between paragraphs and around headings, never
   font size. The font must stay exactly as readable as the source; if
   spacing alone can't close the gap, that's a signal to go back to the
   user, not a reason to shrink text.

   Don't assume a moderate factor is "aggressive enough" and give up early.
   The script only scales explicit paragraph space-before/after — it never
   touches line height or font — so even a small overflow (a couple of
   lines spilling onto an otherwise-empty extra page) can genuinely need a
   surprisingly low factor before the page count actually flips: real runs
   of this pipeline have needed anywhere from 0.5 down to 0.25 to close a
   gap that looked minor. Binary-search downward and re-check the actual
   page count after each try (page count is a step function here, not a
   smooth curve — 0.4 and 0.65 can report the identical page count right up
   until the factor that finally crosses the threshold), rather than
   concluding at 0.65 or 0.5 that spacing "isn't working" and escalating to
   step 4. Only escalate once you've actually tried well below 0.5 and it
   still doesn't close the gap.
4. **Stop and report** exactly which paragraph(s) are pushing the page count
   over, with the specific line lengths involved, so the user can decide
   whether to shorten the underlying content, accept a longer document, or
   handle that section differently. Never quietly drop a bullet, a metric,
   or a tool name to make the page count work.

### 8. Run the mechanical lint

```
python skills/cv-translate-de/scripts/lint_german.py <output.docx> --plan plan.json
```

Always pass `--plan` with the same plan you gave `docx_rewrite.py`. Without
it, the lint scans the entire document, including paragraphs you
deliberately left untouched — a project title, a competition name, a
publication title kept in its original English on purpose (see
terminology-and-facts.md on titled works). A pre-existing em dash inside one
of those is correctly flagged as *present in the file*, but it isn't a
German-prose mistake, and mistranslating or otherwise altering that
untouched title just to silence the linter would itself be a violation of
"never touch a protected title." `--plan` restricts the check to only the
paragraphs you actually rewrote, which is what you actually want verified.

This catches em dashes, English number formatting, straight quotes, and the
stock AI/filler phrase list. A clean run doesn't certify good German — it
only rules out the mechanically checkable mistakes. Read the actual PDF
render from step 6 for everything else (does the layout look right, does
the German actually read well, is anything visually off).

### 9. Check ATS-readability on the exported PDF

```
python skills/_shared/scripts/check_ats.py pdf <output.pdf> --email <email> --phone <phone> --name <name> --expect-pages <n> --headings-in-order <SECTION1> <SECTION2> ...
```

This doesn't simulate Workday, Personio, SAP SuccessFactors or any other
specific system — it catches the mechanical failure modes that break
parsing across most of them: no extractable text layer, contact details not
present as plain text, replacement/encoding characters where a special
character should be, and — the check worth taking seriously — whether
section headings extract in top-to-bottom order. A heading extracting out
of sequence is the signature of a multi-column layout getting scrambled by
a parser that reads column-by-column; since this skill only ever produces
single-column output, a clean result here is expected, not a coincidence.
A clean run is a necessary check, not a guarantee of any specific vendor's
behavior.

Know its actual blind spots rather than treating a clean run as more than it
is: the heading-order check only validates the specific headings you pass
in, not everything between them, so a scrambled two-column body between two
correctly-ordered headings would still pass; it tests pypdf's extraction
only, and a different vendor's parser (Workday-class systems often license
one from Textkernel/Sovren or similar) can order or structure text
differently on the identical PDF; and it can't simulate a "resume upload →
autofill structured fields" flow at all — that's the single most
Workday-specific failure class and genuinely can't be checked offline. A
non-English section name (Publikationen, Persönliche Projekte) is also
likely to land in an autofill system's generic/other bucket rather than a
matching field — that's a property of having those sections at all, not a
defect this pipeline introduces or can fix, and is worth one line of
disclosure to the user rather than silence.

### 10. Look at it

Read the exported PDF (from step 6) the same way you'd read any PDF —
visually compare it against the original's PDF, page by page. Formatting
bugs (a run that lost its color, a bullet that lost its bold phrase, text
that wrapped differently than expected) show up here, not in the JSON.

## Output location and file naming

Never write the translated file back into the same folder as the source
resume, and never overwrite the source file. Save it to the project's
`output/cv-translate-de/` folder (see AGENTS.md for the folder layout).

Deliver both the `.docx` and a `.pdf` exported from it (step 6 already
produces the PDF — keep it, don't regenerate it separately). Name both
files after the original source file with a `-DE` suffix before the
extension: `Firstname_Lastname_Resume.docx` → `Firstname_Lastname_Resume-DE.docx`
and `Firstname_Lastname_Resume-DE.pdf`. Keep the original filename's casing
and separators exactly; only append the suffix.
