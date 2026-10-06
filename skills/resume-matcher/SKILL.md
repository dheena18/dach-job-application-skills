---
name: resume-matcher
description: >
  Given a pasted job posting, determine which of this candidate's eight
  specialized resume variants (AI_LLM, AI_Research, Backend_SoftwareEngineer,
  Cloud_Engineer, DataEngg_AI, DevOps_Engineer, MLOps_Platform_AI, Vision_AI
  — each in English and German) is the best fit, if any. Reports one of four
  verdicts with visible reasoning: a clear match, a match that needs
  tailoring (naming the specific gaps), a weak/contradictory signal worth
  the user's own judgment, or no match at all. Use this whenever the user
  pastes or references a job posting and asks which resume to use, whether
  a posting fits any of their resumes, or wants to route a posting before
  deciding whether to apply. Does not tailor content (that's
  `resume-tailor`), translate (`cv-translate-de`), check ATS-parseability
  (`ats-resume-check`), or write a cover letter (`cover-letter-writer`) —
  this skill only answers "which resume, and how well does it fit."
---

# Resume matcher

This is a genuinely hard, not-fully-solved problem — a purpose-built
classifier for exactly this 3-way task barely beat chance in testing (see
`references/matching-methodology.md`). Read that file before anything else;
it explains why this skill never outputs a bare score, why overall
keyword-match percentage is the wrong primary signal, and what a defensible
verdict actually looks like. Read `references/role-family-signals.md`
before classifying a posting's role family, and
`references/resume-profiles.md` for what each of the eight resumes actually
specializes in.

## Process

1. **Get the posting.** Full text, not a summary. Detect its language
   (German or English) — the verdict must compare against the
   language-matched resume set, since each of the eight resumes exists in
   both languages.
2. **Run `skills/resume-matcher/scripts/compare_resumes.py --job <posting>`**, passing
   `--exclude` with the company name and location so they don't pollute the
   term extraction. This gives a deterministic specialized-term-overlap
   table across all eight resumes, ranked by specialized overlap, not raw
   percentage. Treat this as a starting point — it's necessary, not
   sufficient.
   - **Read the actual resume files, not just `resume-profiles.md`'s
     summaries, for every candidate still in play after this table.** The
     profiles file is a human-written summary and can miss or understate
     real content. Directly check the resume text (e.g. via
     `keyword_audit.read_text`) for the posting's specific named
     requirements (a tool, a domain word, a framework) before ruling a
     resume in or out on that requirement. This has reversed a verdict
     before: a role-family verb-cluster test pointed to one resume, but
     that resume had zero actual content for the posting's single most-
     repeated named requirement, while the alternate candidate did — the
     practical recommendation followed the verified text, not the abstract
     classification. Don't let a plausible-sounding family match stand in
     for checking what's actually on the page.
3. **Read the posting's actual responsibility language** and classify it
   against `role-family-signals.md`'s verb-to-family mapping. This is the
   primary signal, not the script's output. Specifically check:
   - Does the posting require a PhD or first-author publications? If yes,
     that's a strong, near-binary pull toward AI_Research regardless of
     what the script's term overlap shows for other resumes.
   - What's the posting's core accountable artifact (the thing someone in
     this role ships or owns)? Use this to pick between adjacent families
     that share tools (DevOps vs. Cloud vs. MLOps; Data Engineer vs.
     AI/LLM Engineer vs. ML Engineer) — see the disambiguation sections in
     `role-family-signals.md`.
   - What's the scope/seniority language (task-execution vs. management vs.
     strategic verbs)? This is a separate axis from role family — a
     same-family, wrong-level posting gets a different verdict than a
     wrong-family one.
4. **Check for contradictory signals** (e.g. both on-call/SLA language and
   publish-at-a-conference language in the same posting). If present, don't
   force a single family — name the contradiction and ask the user, or
   present the top two candidates with the reasoning for each.
5. **Decide the verdict** — one of:
   - **Clear match**: name the resume, name the specific signals that
     aligned (responsibility language, specialized terms, PhD-gate result,
     seniority fit). No invented confidence number.
   - **Match, needs tailoring**: name the resume, then classify every real
     gap into noise / true-but-reworded / real gap, the same discipline
     `resume-tailor` already uses for its fit table. Say explicitly what
     `resume-tailor` should do next — don't do the tailoring here.
   - **Weak or contradictory signal**: say so plainly, show the conflicting
     evidence, and let the user decide rather than guessing for them.
   - **No match**: say so plainly if the posting's core responsibility
     isn't any of the eight families — don't stretch the closest-sounding
     resume to cover a role it was never built for.
6. **Report back**: the verdict, the specific posting language that drove
   it, the `compare_resumes.py` table for reference, and (if "needs
   tailoring") a clear handoff note naming what `resume-tailor` should
   address.
7. **Always state which language variant to send** — EN or DE — as an
   explicit, separate line in the verdict, not just an implicit side effect
   of which resume directory was compared against. Base it on the
   posting's own detected language (step 1) unless the user says otherwise
   (e.g. an English posting from a company that's visibly DACH-based and
   consulting-formal might still warrant asking, rather than assuming).
   This is a standing instruction, not optional: the user should never have
   to ask "EN or DE?" separately after a verdict.

## When two resumes genuinely contradict: a tie-break lean, not a score

If step 4 finds two resumes that both have real, legitimate support (this is
the "weak or contradictory signal" case with two live candidates, not a
clear winner) — give a lean as a percentage split, but only ever as a
**rubric total**, never a vibe. Score each candidate resume on these four
checkable signals and show the arithmetic:

| Signal | Points |
|---|---|
| PhD/publication gate matches this resume's track | ±40 |
| Responsibility-verb/family alignment (count of role-family-signals.md verb clusters this resume's family actually matches) | ±30 |
| Specialized-term overlap count from `compare_resumes.py` | ±20 |
| Seniority/scope fit (task-execution vs. management vs. strategic, matched to the resume's actual level) | ±10 |

Normalize the two totals to a percentage split (e.g. "62% / 38% toward
AI_LLM over MLOps_Platform_AI") and always show the per-row scoring next to
it — the split is a summary of the rubric, not a replacement for it. This is
an auditable tie-break weighting the user can check and disagree with line
by line, which is exactly what makes it different from the uncalibrated
percentage-bucket scores `matching-methodology.md` warns against. Only use
this when there are genuinely two live candidates after the qualitative
read — don't compute it as a matter of course for every posting, and never
use it to manufacture a confident single pick when the honest answer is
"these two are close and here's why."

## When tailoring is needed: how much, as a fraction of requirements

For a "needs tailoring" verdict, quantify the tailoring load as:

```
tailoring % = (requirements classified "true-but-reworded" + "real gap")
              ÷ (total distinct requirements/signals checked from the posting)
```

List every requirement counted and which bucket it landed in (noise /
true-but-reworded / real gap) before computing the fraction — the
percentage is a rollup of that visible list, never a standalone number. Report
it as "X of Y requirements need rework (~N%)," not as a bare percentage.
This tells the user and `resume-tailor` both the scale of the work and
exactly which items make it up.

## Rules that never bend

- Never output a bare match percentage as the verdict. A number may appear
  in the supporting table, or as the two rubric-based percentages above
  (contradiction tie-break, tailoring load) — but only ever alongside the
  visible scoring/requirement list that produced it, never standing alone.
- Never route primarily on job title. Title is a weak prior — see
  `role-family-signals.md` for why.
- Never force a confident single verdict when signals genuinely conflict.
  Say so instead.
- Never invent a specialized skill for a resume it doesn't actually have,
  and never claim a posting requirement is met when the resume doesn't
  support it.
- This skill selects; it does not edit. Hand off to `resume-tailor` for any
  actual content change.

## Verifying your own output

Before calling this done: the verdict traces to specific posting language
you can quote, the PhD/publication gate was explicitly checked (not
skipped), contradictory signals were actually looked for, and the
`compare_resumes.py` table was run and used as a starting point rather than
the final word.
