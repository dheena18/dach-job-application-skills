# Rebuilding the summary section (Kurzprofil)

The summary/positioning paragraph at the top of a resume is not translated
the same way a bullet is. A bullet is a factual achievement statement, so
its content carries over directly. A summary is a genre with its own rules
that differ by market — American resume-summary convention and German
Kurzprofil convention actually disagree on what belongs in this section, not
just on which language to use. Rebuilding it into German means applying the
German genre's rules, not the American ones with German words.

## Why this section gets special treatment

Documented, multiply-corroborated German career-advice consensus: German
Kurzprofil writing is explicitly more sachlich (factual, reserved) than
American resume-summary writing, which tends toward a more enthusiastic,
narrative register. A summary translated word-for-word carries that
American narrative tone straight into a document a German recruiter will
read as unprofessional or self-indulgent — not because the German is wrong,
but because the genre is wrong.

## What to cut, regardless of what the English source does

- **Personal reflection, feelings, or aspiration about the work itself.**
  "This is the piece of work I care about most" or "what I want to bring to
  a new team" is cover-letter content, not summary content, in both German
  and English convention — German sources are especially explicit that this
  reads as unprofessional self-focus ("wirkt fehl am Platz"). Cut it
  entirely; it carries no fact worth preserving.
- **Value judgments presented as credentials.** "The harder half of the
  job" is an opinion, not a proof point. If the underlying fact (focus area,
  specialization) is real, state it plainly without the editorializing.
- **Soft-skill or character adjectives with no evidence behind them**
  ("motiviert", "teamfähig", "dynamic", "results-driven"). If it's true, an
  achievement bullet already proves it — the summary doesn't need to assert
  it separately.
- **An objective-statement framing** ("seeking a role where I can grow...").
  For anyone beyond entry-level, German and English convention agree: this
  is outdated. State what you've done and what you're specialized in, not
  what you're hoping to get out of it.

## What must survive, unedited

Every number, date, client count, latency figure, and named specialization
in the source summary is a fact and stays exactly as accurate as the
source — cutting the narrative framing around a fact is not the same as
cutting the fact. If the source summary's facts don't actually add up (for
example, a stated total years-of-experience figure that doesn't reconcile
with a stated start year elsewhere in the same paragraph), do not silently
resolve the ambiguity by picking an interpretation — flag it to the user.
That is a content question about their career history, not a translation
decision.

## Structure to rebuild into

Documented 4-part shape, consistent across German and English sources:

1. **Identity + years + domain** — role, how many years, what field. This
   is almost always already the source's strongest sentence; keep its
   facts, tighten its wording.
2. **Specialization or focus, stated as fact** — what they've concentrated
   on, phrased as a fact about their work, not a feeling about it.
3. **One concrete proof point with a number**, if not already folded into
   sentence 1.
4. **Optional: a plain, factual targeting line** — what kind of role or
   focus they're aiming for next, stated as fact, not aspiration ("Sucht
   eine Position, die diesen Fokus vertieft" — not "möchte diesen Fokus
   einbringen, weil es mir am Herzen liegt").

If the user wants deeper work on the summary specifically — writing one
from scratch, fixing a weak English original before translating it, or an
honest opinion on whether an existing summary is any good — that's a
separate, more thorough capability: the `resume-summary-writer` skill. This
file covers just enough to rebuild the summary correctly as part of a full
resume translation.

## Register and length

- Sachlich, full short sentences (Fließtext) — not bullet fragments here,
  unlike the rest of the CV.
- No "Sie"-address (that's Anschreiben register). Grammatical "Ich"/implied
  first person is fine and standard; reflective or emotional first-person
  content is what's actually being avoided, not the pronoun itself.
- **Length: 50-100 words, 3-6 sentences.** A summary this section's own
  source material often runs long (Kurzprofil is meant to be skimmed in
  seconds); if the source is already this tight, don't pad it out to hit a
  minimum.
