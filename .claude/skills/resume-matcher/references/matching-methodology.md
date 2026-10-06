# How this skill decides, and why it's built this way

## Read this first: the honest difficulty of this task

Picking the right one of several pre-built, already-specialized resumes for
a posting is not a solved problem. A purpose-built classifier trained
specifically for this 3-way task (good fit / potential fit / no fit, on a
labeled dataset of ~8,000 resume-JD pairs) reached only 50.2% accuracy
against a 33% random baseline — barely better than chance. A 2025 paper on
resume-to-occupation matching (CareerBERT) names the exact failure mode
this skill has to deal with directly: the matcher "struggles with closely
related roles with different skill requirements (such as Data Scientists
versus Data Warehouse Developers)" — which is structurally the same problem
as telling apart this candidate's DevOps, MLOps, and Cloud Engineer resumes.

This doesn't mean the task is hopeless. It means: **don't build (or trust)
a tool that outputs a confident single number.** The right shape for this
tool is a transparent, reasoned recommendation that shows exactly which
signals drove it, so a human can sanity-check the reasoning — not a
black-box score. Every verdict this skill gives must be traceable to
specific phrases in the posting, not just a percentage.

## Why overall keyword-match percentage is the wrong primary signal

All eight resumes share a large, genuine vocabulary: Python, Docker, AWS,
Azure, CI/CD, Git, M.Sc. AI & ML, THWS. A posting that mentions any of
these will show broadly similar overall match percentages across most or
all eight resumes — not because they're all equally good fits, but because
the overlap is coming from shared infrastructure vocabulary, not from the
thing that actually makes each resume different.

The actionable fix (from Lightcast's commercial skills taxonomy, which
splits detected skills into "specialized skills" — occupation-specific,
e.g. feature-store design, dimensional modeling — versus "software
skills" — named tools everyone lists, e.g. Docker, Kubernetes): **the
differentiator is the specialized, non-shared vocabulary, not the shared
tool list.** `scripts/compare_resumes.py` implements exactly this split —
see `references/resume-profiles.md` for each resume's specialized term set
— and ranks by specialized-term overlap, reporting overall percentage only
as reference context, never as the primary number.

## Uncalibrated percentage-bucket "match scores" are not evidence

Commercial tools that bucket match quality into ranges (e.g. 90-100%
excellent, 80-89% good) do not publish validation against real hiring
outcomes anywhere found during research for this skill — they're vendor
convention, not measured thresholds. Don't invent one here either. State
the verdict in words, backed by the specific signals that produced it.

The two rubric-based percentages this skill does produce — the
contradiction tie-break lean and the tailoring-load fraction, both in
SKILL.md — are not exceptions to this finding, they're a different kind of
number. A vendor match score is opaque: a black-box model outputs 87% and
nobody can check the arithmetic. These two numbers are the opposite: every
point in the tie-break rubric traces to a named, checkable signal (PhD
gate, verb-cluster count, specialized-term count, seniority fit), and the
tailoring fraction is a rollup of a visible, itemized requirement list. The
user can recompute either by hand from what's shown. That auditability is
the actual bar — not whether a number appears at all.

## The three real signals, in priority order

1. **PhD / first-author-publication requirement.** This is the single most
   reliable, nearly-binary signal found in research for this project —
   stronger than any keyword or verb. If a posting requires a PhD and/or
   first-author publications at recognized venues, that's a strong pull
   toward the AI_Research resume regardless of what tools are listed.
   Absence of this requirement, even in a title containing "Research," is
   evidence *against* the research track, not neutral — see
   `role-family-signals.md`'s research-vs-applied section.
2. **Responsibility verbs and the artifact they describe, not job title.**
   Title is measurably unreliable: a labor-economics study (Indeed Hiring
   Lab) found ~33% title-level mismatch even against a curated 6,065-entry
   normalized title taxonomy. "AI Engineer" and "ML Engineer" specifically
   are documented as umbrella terms with no consistent meaning across
   companies — never route on these titles alone. Read what the posting
   says the person will actually *do*, and classify that against
   `role-family-signals.md`'s verb-to-family mapping.
3. **Specialized (non-shared) skill/technology overlap**, via
   `scripts/compare_resumes.py`. A supporting, mechanical signal — run it,
   but never report its percentage as the verdict on its own.

Two secondary checks, applied after the above:

- **Seniority/scope language**, independent of role family. Task-execution
  verbs (assist, compile, maintain, support) versus management/oversight
  verbs (delegate, direct, lead, supervise) versus strategic verbs (advance,
  formulate, drive) indicate a different level than what a resume targets,
  even within the right family. "Right family, wrong level" is a different
  verdict (needs tailoring, or genuinely not a fit) than "wrong family."
- **Required-vs-nice-to-have clustering.** A posting's *required* section
  tool cluster is a better signal of core identity than tools mentioned
  only as a bonus.

## Handling contradictory or weak signal: say so, don't guess

If a posting mixes incompatible signals — e.g. both "on-call rotation,
SLA ownership" (production) and "publish at NeurIPS, collaborate with
academic partners" (research) in the same listing — that's a genuine
anomaly, not noise to average out. Flag it for the user rather than
forcing a pick.

This has a real precedent: Lightcast's own production seniority-tagging
system explicitly declines to classify a posting's seniority when the
signal is weak, stating plainly that it prioritizes precision over always
producing an answer ("not all senior or junior postings will be tagged").
Do the same here. A forced wrong answer is worse than an honest "the
signal here doesn't clearly point one way."

## What "no match" actually means

Say there's no match when the posting's core responsibility isn't any of
the eight role families at all — a Product Manager posting, a pure
frontend/mobile role, a sales-engineer role. Don't stretch the
closest-sounding resume to cover a role family it was never built for.
This is the same discipline `resume-tailor` already applies to a weak
posting fit ("this posting is a stretch" is worth more than forcing a
tailoring pass that was never going to be competitive) — applied one level
up, to resume *selection* instead of resume *editing*.

## Relationship to resume-tailor

This skill selects which resume to use. It does not edit content. Once a
resume is chosen and the verdict is "needs tailoring," name the specific
gaps (using the same noise / true-but-reworded / real-gap classification
`resume-tailor` already uses) and hand off to `resume-tailor` by name —
don't duplicate its tailoring logic here.
