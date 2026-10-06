# resume-matcher

An agent skill that reads a pasted job posting and recommends which of
this candidate's eight specialized resume variants fits best — or says
plainly if none of them do, or if a posting needs tailoring first.

## What it does

- Runs a deterministic specialized-skill-overlap comparison across all
  eight resumes (`skills/resume-matcher/scripts/compare_resumes.py`), ranking by the posting's
  distinguishing vocabulary rather than raw keyword-match percentage, since
  shared tools (Python, Docker, AWS) inflate every resume's overlap almost
  identically and tell you nothing about fit.
- Classifies the posting's actual responsibility language against a
  researched verb-to-role-family mapping, since job titles are documented
  as unreliable (~33% mismatch even in curated taxonomies) and "AI
  Engineer"/"ML Engineer" specifically are umbrella terms with no
  consistent meaning.
- Checks for a PhD/first-author-publication requirement as a near-binary
  gate for the AI_Research resume specifically.
- Separately checks seniority/scope language from role-family language, so
  "right family, wrong level" gets a different verdict than "wrong family."
- Flags contradictory signals (e.g. on-call language and publish-at-a-
  conference language in the same posting) instead of forcing a guess.
- Reports one of four verdicts — clear match, match needing tailoring
  (with named gaps), weak/contradictory signal, or no match — always with
  the specific posting language behind it, never a bare percentage.

## What it does not do

- Tailor resume content — that's `resume-tailor`, which this skill hands
  off to by name when a match needs edits.
- Translate between languages — that's `cv-translate-de`.
- Check ATS-parseability — that's `ats-resume-check`.
- Write a cover letter — that's `cover-letter-writer`.
- Claim more certainty than the task supports. This is a documented,
  genuinely hard classification problem (see
  `references/matching-methodology.md`) — the skill is built to show its
  reasoning transparently, not to act as an oracle.

## How to use it

Paste the job posting (or a file/link to it) and ask which resume fits, or
whether any of your resumes fit it at all.

## Output

A verdict in words, backed by quoted posting language and the
`compare_resumes.py` comparison table — never a bare match score.

## Requirements

Python 3 with the packages in the repo's `requirements.txt`.

## Files

```
resume-matcher/
├── SKILL.md
├── references/
│   ├── matching-methodology.md   Why this is hard, why overall % is the
│   │                             wrong primary signal, the reject-option
│   │                             design, no-bare-score rule
│   ├── role-family-signals.md    Verb-to-family mapping, role-pair
│   │                             disambiguation, research-vs-applied axis,
│   │                             seniority/scope axis, misclassification traps
│   └── resume-profiles.md        This candidate's real eight resume
│                                 profiles — the one reference file in this
│                                 project that's intentionally personal
│                                 rather than generic, since that's the
│                                 whole point of this skill
└── scripts/
    └── compare_resumes.py     Runs specialized-term overlap across all
                               eight resumes in the detected language
```

`compare_resumes.py` expects your resumes in `job-resume/EN/` and
`job-resume/DE/` under the eight example filenames (`Firstname_Lastname_*.docx`).
Edit `RESUME_PROFILES` in the script and `references/resume-profiles.md` to
match your own resume set — this skill is a template, not a generic tool.
