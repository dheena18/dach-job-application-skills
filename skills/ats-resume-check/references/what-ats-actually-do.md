# What an ATS actually does (and doesn't)

Researched across Greenhouse's own support docs, iCIMS product pages, SAP
help portal, Softgarden support docs, and independent HR-tech reporting.
The "resume optimization" industry has a strong incentive to make ATS
behavior sound uniform and menacing (score, reject, filtered into a black
hole). Real behavior is fragmented and, for several major platforms, much
less algorithmic than the marketing implies.

## The real, fragmented picture

- **Greenhouse**: does not algorithmically score or auto-reject resumes.
  It parses a resume into a candidate profile and routes it to a human
  reviewer via "Scorecards." The only automatic rejection path is an
  explicit knockout question (e.g. work authorization) — not resume
  content matching.
- **iCIMS**: markets a real AI ranking feature ("Role Fit"/SmartMatch) that
  scores and ranks candidates for the recruiter. This is a genuine
  algorithmic layer, unlike Greenhouse.
- **Personio** (dominant in German SMEs): no semantic CV-to-job matching by
  default — screening is rule-based via the application form's knockout
  questions. An optional "AI talent screening agent" add-on exists but is
  opt-in, not the default behavior.
- **SAP SuccessFactors**: resume parsing supports German among ~15
  languages. Documented search behavior prioritizes structured Candidate
  Profile fields first, falling back to resume body text only after that —
  so a filled-in profile can outrank a well-written resume the system
  never reads as closely.
- **Softgarden**: parses via a licensed Textkernel module (must be enabled),
  extracting name/contact/experience/education; the vendor's own docs say
  accuracy "varies depending on formatting, language, and CV structure."
- **HackerRank's 2026 open-source ATS**: a genuinely different animal from
  a resume parser — it's a scoring rubric that weighs **Open Source
  Contributions (35 pts)** and **Self/Personal Projects (30 pts)** heavily,
  with Technical Skills a comparatively small slice. Documented, real
  controversy: an unchanged resume scored anywhere from 66 to 99 across
  repeated runs of the same tool — if a company sets an 85 cutoff, roughly
  two-thirds of runs on the identical resume would fail it. Treat this
  system's scoring as inherently noisy, not as a hard yes/no signal, and
  as a data point for a specific piece of advice, not a parsing safety
  check: a resume with a clearly labeled Open Source / Personal Projects
  section is structurally favored by this particular rubric in a way that
  has nothing to do with parsing correctness.

## What this means for a check (or a skill) built around ATS behavior

- Don't build or advise around a single universal "ATS score." It doesn't
  exist across vendors — some don't score at all, some do, and the ones
  that do disagree on what to weight.
- The "75% of resumes are rejected by robots" line traces to an
  unsubstantiated ~2013 startup claim, repeated endlessly since. Treat any
  specific rejection-rate statistic you encounter with the same skepticism
  unless it names a real, checkable source.
- The genuinely well-documented risk is not "the algorithm doesn't like my
  keywords" — it's **structural**: tables, multi-column layouts, headers/
  footers, and embedded graphics are the things that reliably break
  parsing across nearly every vendor, regardless of whether that vendor
  also does keyword scoring. That's what this skill's mechanical check
  actually verifies (see `mechanical-checks.md`) — it's the part that's
  actually testable and actually true across the fragmented landscape.
- Keyword/content matching is a real concern for some systems and not
  others, but it's a *content* concern (does the resume's language overlap
  with the posting's), which is the `resume-tailor` skill's job, not this
  one. This skill checks whether the document is even readable — a
  necessary condition, not a match-quality score.
