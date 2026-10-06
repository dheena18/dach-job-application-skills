# resume-summary-writer

An agent skill for the single hardest paragraph on a resume: the
summary/profile block at the top. Writes one from scratch, rewrites a weak
one, or gives an honest critique of an existing one — for English (US/
international) or German (DACH/Kurzprofil) conventions.

## Why this is its own skill

A resume summary is a distinct genre, not just "a short paragraph." Most
weak summaries aren't badly written sentence-by-sentence — they're writing
cover-letter content (personal reflection, aspiration, "what I want to
bring") into a slot that's supposed to be a fast, evidence-backed
positioning statement. German convention adds a second layer: it's
explicitly more sachlich (factual, reserved) than the more narrative
American convention, so a straight translation of an English summary often
reads as unprofessional in German even when every sentence is grammatically
correct.

This came out of building a separate resume-translation skill
(`cv-translate-de`) and finding, on review, that the summary section needed
real rework, not just translation — different enough from the rest of that
skill's job to deserve its own focused tool.

## What it does

- Writes a new summary from your role, years of experience, domain, and a
  real quantified achievement — never invents one.
- Rewrites an existing summary that's too long, too vague, or drifting into
  cover-letter/narrative territory.
- Gives a direct, specific verdict on an existing summary: good, mediocre,
  or weak, and exactly why — not vague encouragement.
- Applies the right register and length for the target market: 40-80 words
  for English, 50-100 words for German, with the structural and tonal
  differences between the two documented in its reference files.
- Flags factual inconsistencies in your source material (e.g. a stated
  years-of-experience figure that doesn't reconcile with a stated start
  date) instead of silently picking an interpretation for you.

## How to use it

Ask your AI agent something like: *"write me a resume summary"*, *"is my CV's
opening paragraph any good?"*, *"my Kurzprofil sounds off, can you fix
it"*, or paste an existing summary and ask for feedback or a rewrite.

You'll be asked for whatever's missing: your role/title, years of
experience, domain, at least one real number to prove it, target market
(English/German), and what you're targeting next — or just point your agent at
your full resume and it'll pull a proof point from your actual bullets
instead of asking you to remember one.

## Files

```
resume-summary-writer/
├── SKILL.md                          Entry point: process and self-check before delivering
└── references/
    ├── writing-the-summary.md        The core formula, precise-vs-vague mechanism,
    │                                 named mistakes, summary-vs-objective (market-general)
    └── german-kurzprofil.md          German-specific structure, register, length,
                                      and how it genuinely differs from the American style
```

No scripts, no external dependencies — this is a writing/review skill, not
a document-formatting one.

## Relationship to cv-translate-de

`cv-translate-de` rebuilds a whole resume from English into German,
including its own lighter-weight summary-handling rule. Use this skill
instead when the summary itself is the actual task — writing one from
scratch, fixing a weak one before it goes anywhere, or getting a real
opinion on whether an existing one works.
