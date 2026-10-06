# Fit analysis and keyword matching

## What tailoring actually is

Documented consensus, not opinion: tailoring is **extract → match → reorder
→ reword**, never invent.

1. Extract the posting's real requirements — split must-have from nice-to-
   have (see below).
2. Match them against the candidate's actual, existing experience.
3. Reorder: the most relevant bullet within a job entry moves to the top;
   the most relevant skill category leads; an older, less relevant role's
   bullets get trimmed rather than kept at full length.
4. Reword using the posting's own terminology, but only where it's already
   true of the person's real experience. "User research" for what they
   called "customer discovery" is fine if they did that work. Calling
   something "user research" they never did is not tailoring, it's
   fabrication.

Never: invent a skill, tool, employer, title, date, or metric. Never change
a job title to match the posting's title. If a requirement genuinely isn't
met, it stays unmet — say so in the fit table, don't paper over it.

## The fit table

Produce this before touching the resume, and show it to the user:

```
Requirement (from posting)        Evidence (from candidate)              Status
---------------------------------  --------------------------------------  --------
5+ yrs Python                      6 yrs across 3 roles                    strong
Production LLM/RAG systems         Built RAG platform, 5 enterprise clients strong
A/B testing on search systems       none                                    gap
Top-tier CS degree                  TH Würzburg-Schweinfurt (not listed)    gap
```

Split must-have from nice-to-have. Postings usually put must-haves first,
in phrases like "required," "you have," "Sie bringen mit," "Voraussetzung."
Nice-to-have shows up as "bonus," "ideally," "wünschenswert," "von Vorteil."

Sort each requirement's evidence into: **matched** (already true, in
similar words), **rephrase** (true, but worded differently on the resume —
fix the wording), **missing but true** (the person has it, resume forgot
it — add it, with real context), **missing and unsupported** (they don't
have it — leave it out, address honestly in a cover letter if it matters
enough to explain).

Give an honest overall verdict: strong fit, worth a tailored application; a
real gap that a letter should address; or a stretch not worth the time.
Being honest here — including telling the user a posting is a poor fit —
is more valuable than forcing every application to look strong.

## The actual target: ~75-85%, not 90%+

Jobscan — the largest vendor in this exact space — explicitly recommends
aiming for around 80% match, stating 75% often succeeds too, and warning
that pushing higher risks a resume that "sounds awkward and robotic" from
over-optimization. Treat that as the real target. A resume sitting at
70-80% match after honest tailoring is working correctly, not falling
short — the remaining gap is normally a mix of measurement noise (see
below) and genuine, honestly-left gaps, not a sign more keywords are
needed. Never treat 90%+ as something to chase.

## Reading a "missing terms" list correctly

`keyword_audit.py`'s missing-term list is not a list of gaps — it's a list
of candidates that need triage, and a large fraction of it is usually noise
from the extraction method itself, not real content gaps:

- **Company name and location.** The posting's own company name and city
  will often appear in the "missing" list purely because it's mentioned
  repeatedly in the posting — obviously not a skill. Always pass
  `--exclude "Company Name,City"` with the actual posting's company and
  location; don't manually filter these out of the output by eye every time.
- **Generic filler words** ("remote", "professional", "modern",
  "scalable") — the stopword list filters the most common repeat offenders,
  but new ones will surface. If a "missing" term isn't a real skill/tool/
  requirement, it's noise — say so and move on, don't force it into a bullet.
- **Inflected forms** ("LLM" vs "LLMs", "system" vs "systems") are handled
  automatically via lemmatization (English and German) plus explicit
  acronym-plural entries in `SYNONYMS` — these shouldn't appear as separate
  missing terms anymore, but if a new one turns up, that's a real matcher
  gap worth fixing, not a resume gap.
- **Near-synonym paraphrases** ("RAG solutions" vs. resume's "RAG systems")
  are handled for a small set of interchangeable generic role-nouns
  (solution/system/pipeline/platform/tool/application/framework/service) —
  if a posting's phrasing still shows as missing despite the resume saying
  the equivalent thing with a different word, that's exactly the kind of
  case a real semantic-matching ATS wouldn't penalize; note it as
  "already covered, different wording" rather than rewording the resume to
  chase it.

After noise and inflection/synonym artifacts are excluded, whatever's left
is the real fit-table job: sort it into true-but-forgotten, true-but-
differently-worded, or a real gap (see the process above).

## ATS reality check before you start

Don't tailor as if there's one universal scoring algorithm to beat — there
isn't (see `ats-resume-check`'s `references/what-ats-actually-do.md` for
the documented, fragmented reality: some platforms don't score resumes at
all, others do, and they don't agree on what to weight). Tailor for the
actual human reader first — a recruiter skimming for 5-10 seconds — and let
keyword accuracy follow from describing real experience precisely, not from
gaming a mechanism that may not exist for this particular posting's
platform.

## Spelling and spacing variants in the matcher

`keyword_audit.py` treats a term as present regardless of common spelling
variants — "MongoDB" matches "Mongo DB", "ReactJS" matches "React", and so
on — via a curated synonym map (`SYNONYMS` in the script) plus a generic
"JS" suffix rule. This matters because a resume that genuinely lists a
skill shouldn't score as missing it just because a posting spelled it
differently; that's a matcher gap, not a candidate gap. Add a new entry to
`SYNONYMS` whenever a real mismatch like this turns up — it's a small,
auditable dictionary by design, not a fuzzy matcher, so it never risks a
false match on an unrelated term. Note this doesn't guarantee a score
change on any specific posting: it only helps when that posting's own
wording actually happens to hit one of the covered variants.

## Keyword-matching mechanics

- Exact match still matters for older/simpler parsers; expect some
  semantic/synonym matching on newer platforms, but no vendor publishes
  their actual algorithm — don't assume more sophistication than you can
  verify.
- Spell out acronyms once with the acronym in parentheses ("retrieval-
  augmented generation (RAG)") — some systems and some human searchers only
  match one form.
- Natural repetition (a true term appearing 2-3 times across summary,
  skills, and a bullet) is fine and normal. Mechanical repetition — forcing
  the same exact phrase in an unnatural number of places — is detectable
  by modern NLP-based parsers and reads as stuffing to a human. See
  `avoiding-ai-tailored-tells.md`.
- Keywords carry more weight in a skills section and in job titles/
  headlines than buried deep in a narrative bullet. A required hard skill
  that's completely absent from the resume is a bigger risk than one that
  only appears once.

## How much tailoring is enough

No rigorous study sets a number, but the repeated convention across
career-coaching sources is roughly 10-15 minutes of focused work once a
strong base resume exists — most of the value comes from the first pass
(promote the 2-3 most relevant things, cut what's irrelevant), with sharply
diminishing returns after that. If tailoring is taking much longer than
that, either the base resume is weak (fix the master, don't re-litigate it
per application) or the posting is a poor enough fit that no amount of
rewording will make it a strong one.
