# Writing German that reads as native, not translated

This file is the checklist to run every rebuilt sentence against. All examples
below are invented for illustration — never copy real content from a user's
resume into this file.

## Why this matters more than it looks

German recruiters read hundreds of applications. A CV that is correct but
reads like a translation (right words, foreign sentence logic) gets the same
reaction as an obviously AI-written one: skimmed faster, trusted less. The
goal is not "grammatically valid German" — it is "a German IT professional
wrote this."

## Typography (documented convention, not style preference)

- **No em dash (—).** German professional typography doesn't use it. It has
  become a specifically documented tell of English-trained AI output leaking
  into German text. Where the English source uses one for an aside or a
  before/after contrast, restructure: split into two sentences, use a colon,
  or use a comma.
  - English: "Manual batches took two weeks — now three hours."
  - Not: "Manuelle Stapel dauerten zwei Wochen — jetzt drei Stunden."
  - Instead: "Manuelle Stapel dauerten zuvor zwei Wochen, heute drei Stunden."
- **German quotation marks**: „…" (or »…« in some house styles), never "…".
- **Numbers (DIN 1333/5008)**: comma as the decimal separator, a period or
  space as the thousands separator, a space before %. "50,000 users" →
  "50.000 Nutzer"; "3.8% improvement" → "3,8 % Verbesserung".
- **Dates**: MM.JJJJ or DD.MM.JJJJ, never spelled-out English month names in
  the CV body.
- **En dash for ranges** ("03.2022–09.2023") is fine and standard; that is
  different from the em dash rule above.

## The stock phrases that give away a translation or an AI pass

Cut these on sight and replace with the actual fact:

- "In der heutigen [schnelllebigen] Welt/Zeit…"
- "…spielt eine [entscheidende/wichtige] Rolle"
- "…ist ein integraler Bestandteil von…"
- "Es ist wichtig zu beachten, dass…"
- "…bietet vielfältige Möglichkeiten"
- "Ich bin überzeugt, dass…"
- "nicht nur X, sondern auch Y" — a documented mechanical tic. If there are
  two true things, state them as two plain clauses.
- Forced rule-of-three lists where the source only supports one or two points.
- Empty verbs that avoid committing to a claim: "bietet", "ermöglicht",
  "stellt dar" used in place of a real verb. "Das Tool bietet eine Reduktion
  der Bearbeitungszeit" → "Das Tool reduzierte die Bearbeitungszeit."

## Sentence structure for CV bullets specifically

- CV bullets in German are **verb-first fragments**, not narrated sentences
  and not addressed with "Sie" (that register is for the Anschreiben, not
  the Lebenslauf). Drop the subject pronoun.
  - Not: "Ich habe eine Pipeline entwickelt, die..."
  - Instead: "Entwickelte eine Pipeline, die..."
- Keep sentences short. If a sentence needs three commas, split it. Long
  subordinate-clause chains (Schachtelsätze) are a translation tell, not a
  sign of sophistication, in a CV specifically (this is different from
  formal essay-register German, where nominal/subordinate density is
  normal — a CV is terser than that).
- Match the English source's fragment style where it already uses one
  (most modern resume bullets start with a past-tense verb, e.g.
  "Built...", "Reduced...", "Deployed..."). That structure maps naturally
  onto German verb-first fragments; don't add scaffolding that wasn't there.
- **Separable verbs are a real trap for verb-first bullets.** A German verb
  like "durchführen" or "anpassen" splits, and its prefix has to land at the
  true end of the clause ("Führte X anhand von Y durch"), which can drag a
  meaningless grammatical particle to the far end of a long bullet just to
  satisfy word order. When that happens, prefer a noun-phrase opener instead
  ("Durchführung von X anhand von Y" / "Anpassung von X an Y..."). This is
  not a deviation from CV register — noun-phrase-led fragments are just as
  native to German CVs as verb-first ones (German formal/business writing
  leans nominal generally), so pick whichever avoids the awkward split
  rather than forcing a verb-first structure that fights the language.

## Register: sachlich, not promotional

German CV culture reports facts and lets the numbers argue the case. American
resume conventions lean on evaluative language layered on top of the fact.
Strip the evaluative layer, keep the fact and the number:

- English: "Successfully delivered an outstanding 40% reduction in latency."
- Not: "Erfolgreich eine herausragende Reduktion der Latenz um 40 % erzielt."
- Instead: "Reduzierte die Latenz um 40 %."

This is not about removing confidence — the number still lands. It is about
not adding a layer of self-praise around it, which reads as amateurish
("Eigenlob") to a German reader in a way it doesn't to a US one.

Words to cut on sight (self-assessment / inflated claims, in either
language): "passionate", "extensive experience", "proven track record",
"leverage", "seamless", "cutting-edge", "hochmotiviert", "Teamplayer",
"belastbar", "Leidenschaft", "spannende Herausforderung",
"kommunikationsstark". If the claim is true, the achievement bullet itself
already proves it — no adjective needed on top.

## Grammar traps specific to EN→DE technical rebuilds

- **Compound nouns (Komposita)**: German compounds close (one word), and the
  gender follows the head (last) noun, not the first. Getting the head noun
  wrong flips the gender and the article. When in doubt, look up the
  compound rather than gender-guessing by analogy with a similar word.
- **Fugenzeichen** (linking letters like -s-, -en- inside a compound) have no
  single fixed rule; check rather than assume "no linking letter" is always
  safe.
- **Case (Akkusativ/Dativ)**: technical prepositions carry a fixed case
  ("mit" always Dativ, "für" always Akkusativ, etc.) — a wrong case on a
  tool/object noun is one of the fastest tells of non-native German, because
  it survives even when the vocabulary is perfect.
- Do a final self-check pass reading each rewritten sentence purely for
  gender/case agreement, separate from the pass that checks meaning. Doing
  both at once is how agreement errors slip through.

## Read-aloud test before delivering

- Would a German native colleague say this sentence, in this shape, out loud?
- Does any sentence exist only to sound impressive rather than to state a
  fact? Cut it.
- Is the em dash gone, are the numbers in German format, are the quotation
  marks German?

None of this is about sounding stiff. Plain, factual, well-formed German is
the native register for a CV — it isn't a downgrade from the more expressive
English version, it's the correct register for this document in this market.
