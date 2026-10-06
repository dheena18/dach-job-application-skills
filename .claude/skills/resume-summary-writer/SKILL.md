---
name: resume-summary-writer
description: >
  Write, rewrite, or critique the summary/profile section at the top of a
  resume or CV — the 2-6 line block under the contact info, sometimes called
  a professional summary, positioning statement, or (in German) Kurzprofil.
  Handles both English (US/international) and German (DACH) market
  conventions, which genuinely differ in register, not just language. Use
  this whenever the user asks to write, fix, tighten, or get feedback on a
  resume/CV summary, opening paragraph, Kurzprofil, or "About me" section on
  a resume specifically — even if they don't use the word "summary", e.g.
  "does my resume intro sound okay", "my CV opener feels weak", "write a
  Kurzprofil for me". Also use it when asked for an honest opinion on
  whether an existing resume summary is any good. Do not use this for the
  rest of the resume (experience bullets, skills, education) or for cover
  letters — this skill is scoped to the summary block only.
---

# Resume summary writer

A resume summary is a distinct genre from the rest of the resume, and from
a cover letter. Most of what makes one bad isn't grammar — it's writing
cover-letter content (personal reflection, aspiration, "what I want") into
a slot that's supposed to be a fast, evidence-backed positioning statement.
Most of what makes a German Kurzprofil bad specifically is carrying over
the more narrative, enthusiastic American convention instead of the more
sachlich German one — read `references/german-kurzprofil.md` before writing
one in German, it is not just a translated version of the English rules.

## What to read

| Task | Read |
|---|---|
| Writing or rewriting in English | `references/writing-the-summary.md` |
| Writing or rewriting in German (DACH) | `references/german-kurzprofil.md` (in addition to the English file — the 4-part formula is shared, the register and length norms differ) |
| Only critiquing an existing summary, not rewriting | Either file, matched to the target market — same rules apply to a critique as to a rewrite |

## Process

1. **Establish what you're working with.** Do they have an existing summary
   to critique or rewrite, or are they starting from nothing? What's the
   target market/language (English, German, or both)? If starting from
   nothing, you need: their role/title, years of experience, domain, and at
   least one quantified achievement — ask for what's missing rather than
   inventing it. If they have a full resume, its bullets are usually the
   best source for a real proof point instead of asking them to summarize
   one from memory.

2. **If critiquing an existing summary**, check it against the relevant
   reference file's named mistakes (buzzword adjectives, narrative/cover-
   letter register, objective-statement framing, restated job title with no
   result, wrong length) and give a direct verdict — good, mediocre, or
   weak — with the specific sentence-level reason, not just "could be
   stronger." A vague critique is exactly the kind of imprecision this skill
   exists to eliminate elsewhere.

3. **If writing or rewriting**, apply the 4-part formula (identity + years +
   domain → specialization → quantified proof → optional targeting line),
   in the register and length the target market's reference file specifies.
   Produce the summary text directly — don't hand back a template with
   blanks.

4. **Check your own output before delivering it:**
   - Word count in range (40-80 English, 50-100 German).
   - Every sentence has either a fact or a specific claim behind it — none
     of them would be equally true of another candidate with no edit.
   - No buzzword adjectives asserting a trait instead of showing it.
   - No cover-letter content: no reflection on what the person personally
     cares about, feels, or hopes for — only what's true about their
     experience and what they're targeting, stated as fact.
   - German output: sachlich register, no unresolved "Ich möchte..., weil
     es mir am Herzen liegt"-style aspiration.

5. **Never invent a metric, employer, date, or achievement.** If the 4-part
   formula's proof-point slot has nothing real to put in it, say so and ask,
   rather than filling it with something plausible-sounding.

6. **If the source material has an internal inconsistency** (for example, a
   stated total years-of-experience figure that doesn't reconcile with a
   stated start date elsewhere), don't silently pick an interpretation and
   move on — flag it to the user. That's a question about their actual
   career history, not a wording decision this skill should make for them.

## Relationship to other skills

If the task is translating/rebuilding an entire resume from English to
German (not just the summary), that's the `cv-translate-de` skill — it has
its own, shorter summary-handling reference tuned for that pipeline context.
Use this skill instead when the summary is the actual focus: writing one
from scratch, fixing a weak one, or getting a direct opinion on whether an
existing one is good.

## Output style

Give the summary text itself first, plain, ready to paste. Then a short
note on what you did and why (or, for a critique, the verdict and the
specific fix). No em dashes, no filler adverbs, no stock phrases — the
summary itself is being held to that standard, hold your own explanation of
it to the same standard.
