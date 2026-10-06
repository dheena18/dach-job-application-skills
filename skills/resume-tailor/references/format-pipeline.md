# Tailoring the .docx without breaking its format

## The technical approach: reassign content, never move paragraphs

Tailoring needs to reorder content — promote a bullet to the top, reorder
which skill category leads. The naive way to do that is to physically move
paragraph XML elements around in the document. Don't do that: it's
documented as fragile, unsupported territory in python-docx (no built-in
API for it; Microsoft's own Open XML engineering guidance calls the
operation "daunting" because paragraphs can carry markup — comments,
bookmarks, section properties — that spans or depends on position).

There's a much safer approach, and it's already implemented:
**`docx_rewrite.py` (copied from `cv-translate-de`) already treats
"paragraph slot" and "content assigned to that slot" as independent.** A
rewrite plan entry says "paragraph index N gets these segments" — it never
says anything about where N is relative to other paragraphs. So "reorder"
is achieved purely by deciding *which bullet's text-and-formatting* goes
into *which slot*, never by moving anything. Promoting bullet 3 to the top
of its job entry means: slot 1 (originally bullet 1's position) gets bullet
3's text and bold-emphasis pattern in the plan; slot 3 gets what used to be
in slot 1, or gets emptied if there are now fewer bullets worth keeping for
that entry. Nothing about the paragraph's position, numbering, or list
membership ever changes.

This works because bold/color emphasis in a bullet is a property of the
achievement being described — the metric, the key phrase — not of the slot
it happens to sit in. When you relocate a bullet's content to a new slot,
carry its own bold-segment pattern with it; don't try to reuse the
destination slot's original bold pattern for different content.

## Trimming vs. inserting

- **Trimming** (a job entry needs fewer bullets after tailoring, because an
  irrelevant one is being cut): give that slot's plan entry a single empty-
  text segment. An empty paragraph is a blank line — safe, matches how the
  original document likely already uses blank paragraphs as section
  spacers, and doesn't corrupt anything.
- **Needing more bullets than slots exist** for a given entry: this is the
  one case the fixed-slot approach doesn't solve for free. Don't reach for
  paragraph insertion to solve it — instead, reconsider whether promoting
  content from elsewhere (a different job entry, if genuinely relevant) or
  trimming a different bullet to make room within the same entry gets you
  there. If neither works, say so to the user rather than inserting a new
  paragraph — that reopens exactly the fragility this approach exists to
  avoid.

## Bullet-list safety

Confirmed safe to reassign freely: plain glyph bullets with a single static
list style (what a resume normally uses). The real hazard the research
flagged is auto-numbered lists (sequential counting, not just a bullet
glyph) — those track position via `numId`/`ilvl` in `numbering.xml`, and
moving content across numbering boundaries can visibly renumber siblings.
Check with `docx_inspect.py` whether the source document's bullets are
plain (no numbering restart behavior) before assuming this is a non-issue;
it will be for the overwhelming majority of resumes, which use plain
bullets, but verify rather than assume.

## The master-resume principle

Always tailor from one designated master/base resume file — never re-
tailor an already-tailored output. Successive tailoring passes on a
tailored file compound drift (a bullet trimmed for posting A might be
exactly the one posting B needs) and make it easy to lose track of what the
"real," complete version of the resume actually says. Ask which file is the
master if it's not obvious, and produce a new, separately-named tailored
file per application — never overwrite the master.

## Full pipeline per tailoring pass

1. `docx_inspect.py` on the master — get the exact paragraph/run structure,
   same as any docx work.
2. `keyword_audit.py --resume <master.docx> --job <posting text or file>` —
   deterministic keyword diff, a starting point for the fit table, not a
   verdict.
3. Build the fit table by hand (`fit-and-keywords.md`) — human judgment on
   top of the deterministic diff.
4. Decide the reassignment plan: which bullet's content moves to which
   slot, which get trimmed to empty, whether any rewording is needed to
   mirror true posting language. Apply `avoiding-ai-tailored-tells.md` and,
   for German output, `german-tailoring.md` plus `cv-translate-de`'s
   `native-german-style.md` while drafting the actual wording.
5. `docx_rewrite.py <master.docx> plan.json <output.docx>` — apply it.
6. Validate the XML (the `anthropic-skills:docx` skill's `validate.py`, if
   installed — locate its path same as `cv-translate-de` does).
7. `check_pages.py both` — check real page count. Tailoring should rarely
   change page count much (you're reordering/trimming, not translating into
   a longer language), but verify rather than assume.
8. `check_ats.py both` — the same standalone check `ats-resume-check` uses;
   a copy lives in this skill's own `scripts/` for self-containment.
9. Look at the rendered PDF side by side with the master's — same
   discipline as any docx-editing skill: formatting bugs show up here, not
   in the plan JSON.

## Output location and naming

Never overwrite the master resume or write into its folder. Save tailored
output to the project's output location for generated application
documents, named to identify the target: `<original-filename>-<Company>.docx`
and the matching `.pdf` (e.g. `Firstname_Lastname_Resume-Acme.docx`), so
multiple tailored versions for different applications don't collide or get
confused with each other or with the master.
