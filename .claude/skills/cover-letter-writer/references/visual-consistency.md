# Matching the resume's visual style

Hiring managers notice a mismatched cover letter and resume — different
fonts or colors read as two separately-assembled documents, not one
coordinated application. This skill builds the letter to inherit the
resume's actual styling rather than using a fixed, generic look.

## Why this skill builds fresh instead of reassigning content

`cv-translate-de` and `resume-tailor` never physically move or create
paragraph structure in the .docx they work on — they reassign content into
an existing document's fixed paragraph slots, because moving XML in a
document that already has established formatting, bullet numbering, and
section layout is fragile (see those skills' `format-pipeline.md` files).

A cover letter has no such pre-existing document to protect: there is
nothing to preserve because nothing exists yet. A business letter's
structure is also simple — plain paragraphs, no bullet lists, no numbering,
no tables. So this skill is the one place in the project where authoring a
new `.docx` from scratch is the right call, not a shortcut.

## Extracting the style profile

Run `scripts/docx_inspect.py <resume.docx>` on the actual resume file
being submitted for this application (the master or the already-tailored
version, whichever is going out with this letter). From the output,
identify:

- **Heading/name style** — the font family, size, color, and bold state
  used for the candidate's name/header line. Apply this to the sender's
  name line in the letter.
- **Accent color** — a distinct color the resume uses for emphasis (e.g. a
  tech-stack line or subtitle color), if one exists. Use sparingly, if at
  all — a business letter reads oddly with heavy color use. The subject
  line is the only place bolding/color from the resume's heading style
  usually belongs.
- **Body font** — apply the exact family throughout the letter body; this
  is the single biggest driver of the "matching package" impression and
  should never be substituted.
- **Body size** — start from the resume's real extracted size. A dense
  two-page resume often runs smaller (9-10pt) than is comfortable for a
  one-page letter meant to be read differently; scaling up a point or two
  for readability is fine, but make it a deliberate, stated decision, not
  a default guess in place of looking at what the resume actually uses.
- **Heading size** — unlike body size, match the resume's real extracted
  heading size exactly. There's no readability reason to change it, and a
  side-by-side reading will catch it if it doesn't match.
- **A muted/grey tone**, if the resume uses one for dates or metadata —
  useful for a small enclosures line at the bottom, matching how the
  resume treats secondary information.

Do not guess these values or hardcode any specific font/color into this
skill's own files — always extract them fresh from the real resume being
used for the specific application, since different users' resumes will use
different fonts and palettes entirely.

## Building the file

Feed the extracted style profile plus the letter's content into
`scripts/build_cover_letter_docx.py` (see its docstring for the exact plan
format). Run `scripts/check_pages.py both` afterward the same way every
other docx-producing skill in this project does — verify the real page
count and get a PDF for a final visual check, rather than assuming
python-docx's output renders the way the JSON plan implies.
