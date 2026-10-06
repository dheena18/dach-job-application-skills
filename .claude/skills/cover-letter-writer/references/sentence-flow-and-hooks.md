# Sentence-level flow and hook craft

A letter can have correct structure (hook/proof/fit/close, DIN 5008 layout,
real achievements, no banned phrases) and still read like an email. This
file is about the layer underneath structure: how the sentences themselves
connect. Read it after `persuasion-and-evidence.md` and the relevant
`letter-structure-*.md`, before finalizing any draft.

## The diagnostic: parataxis vs. hypotaxis

The technical difference between "reads like an email" and "reads like an
argument" is **parataxis** (facts placed side by side as equal, independent
clauses — joined by "and," "also," a semicolon, or nothing at all) versus
**hypotaxis** (one clause is grammatically subordinated to another, so the
sentence itself states the logical relationship between the facts: cause,
consequence, concession, purpose).

Test: if you can swap the order of two sentences without losing meaning,
they're paratactic. If a sentence only makes sense in its logical relation
to the next one, it's hypotactic. An email's job is to convey facts fast
with no argued relationship between them, so it defaults to parataxis. A
cover letter's job is to argue a case, so it needs hypotaxis.

Paratactic (email-register): "I built a RAG pipeline. It handled 100
documents a week. I also eliminated manual triage."

Hypotactic (argued): "I built a RAG pipeline that handled 100 documents a
week, which eliminated manual triage."

German sources: Ludwig Reiners (*Stilkunst*) states this as "Hauptsachen in
Hauptsätze, Nebensachen in Nebensätze" — the claim that matters goes in the
main clause, the supporting fact goes in a subordinate clause, which is
what creates hierarchy instead of a flat list. Wolf Schneider (*Deutsch für
Profis*) adds: prefer verbs to nominalizations, avoid passive voice, vary
sentence length deliberately.

## Connect, don't list

Before: "Ich bin kommunikativ, belastbar und übernehme gerne Verantwortung."
(a bare self-assessment list, no reasoning — see
`banned-phrases-de-en.md`'s self-assessment-without-evidence rule)

After (subordinating a personal fact to the claim it supports): "Da ich
innerhalb des Studiums zwei Semester in England studiert habe, spreche ich
fließend Englisch."

The same mechanism in English: "I managed the launch. The budget was $2M.
The team was 6 people." (paratactic, three unconnected facts) versus "I
managed the $2M launch with a six-person team." (one hypotactic statement,
subject carried through — Williams calls this a consistent "topic string").

## Known-new chaining

A sentence should open with information the reader already has (from the
previous sentence) and end with new information. The next sentence then
opens with that new information. This is what makes paragraphs read as one
continuous thought instead of a list of separate statements.

Disjointed: "The collapse of a dead star into a very small point creates a
black hole." Flowing: "A black hole is created when a dead star collapses
into a very small point" — the next sentence can now open with "This
collapse..." because that's where the previous one ended.

Applied to a cover letter: don't open the next sentence with a fact
unrelated to what the previous sentence just established. Close each
sentence on the idea the next one will pick up.

## Causal/consequential connectives, not "and-then" chains

A sequence of facts linked only by addition ("I did X. I also did Y. I
also did Z.") reads as inert chronology. The same facts linked by
causation read as an argument: "Because I owned the migration end-to-end,
I was the one who managed the vendor relationship when the timeline
slipped — which is why leadership asked me to present the recovery plan."

**Ban as a default move**: paragraph-opening "Additionally," "Also," "In
addition" in English; "außerdem," "zusätzlich," "und" as the *only*
connector in a German sentence. These are addition-connectives — they
just append another fact. At least one sentence per achievement paragraph
needs a connective that states cause, consequence, purpose, or concession
instead.

**German Konnektoren, by function** (use at least one per achievement
paragraph, not just a single weak one tacked onto the end):

| Function | Connectors |
|---|---|
| Kausal (reason) | weil, da, denn, zumal |
| Begründung (mid-sentence) | deshalb, deswegen, daher, darum, weshalb, aufgrund + Gen. |
| Konsekutiv (consequence) | sodass, folglich, infolgedessen, somit |
| Konzessiv (despite) | trotz + Gen., obwohl, dennoch |
| Final (purpose) | um...zu, damit |
| Instrumental (action → result, in one sentence) | dadurch, wodurch, indem, mittels + Gen. |
| Inferential (explicit "this is why I fit") | aus diesem Grund, vor diesem Hintergrund |

`wodurch`/`dadurch`/`indem` are specifically the right tool for
Context-Action-Result sentences: "Ich habe X eingeführt, wodurch das Team Y
erreichen konnte" fuses the action and result into one sentence with the
mechanism stated explicitly — stronger than two sentences joined by a
semicolon. "Trotz X... aus diesem Grund..." is the right pairing for
turning a Beleg into an explicit Passung claim: state a fact, then
explicitly draw the inference connecting it to the job.

**English equivalents**: because, which meant, as a result, so that,
which is why, given that. Natalie Canavor's example: "They never came. We
just sat there." (flat) versus "Waiting all morning cost us a lot of
time, and as a result, we are at risk of missing the deadline." (connected).

## Sentence-length variation

Uniform sentence length is itself an email-register tell — three or four
similar-length declaratives in a row reads as a status update regardless
of content. Gary Provost's rule: mix a short sentence for emphasis with
longer ones that build. One German source's framing of the same idea:
uniform length is "kein Welle, nur ein Laufband" (no wave, just a
conveyor belt). Check each paragraph for this before finalizing — if every
sentence is roughly the same length, vary at least one deliberately,
usually by making the punchline shorter, not longer.

## Hook/opening-line craft: the open-loop mechanism

"Mention something specific about the company" is necessary but not
sufficient. What actually makes an opening pull a reader in is structuring
it as incomplete information that creates forward pull — an implicit
question the rest of the letter answers.

**English techniques** (with real examples; invent the specifics,
never copy these verbatim):
- Scene/mid-story opener: "After about three years of trying out different
  roles..." (implies a journey the letter will resolve)
- Unexpected-twist/delayed-specificity: set up a small surprise before the
  real point
- Anticipating the reader's objection (prolepsis): "You might be wondering
  what a [N]-year veteran of [X] is doing applying for [Y]..." — names the
  likely doubt before the reader forms it
- Contrast/declaration: state what you're *not*, to make the actual claim
  land harder by contrast
- Concrete/sensory detail instead of an abstract enthusiasm claim

**German techniques** (karrierebibel.de, with worked examples):
- Wertealignment: "Nachhaltigkeit ist Ihre Mission – meine ist es auch!"
- Konkrete Unternehmensfakten: cite a real, checkable number or decision
  the company made (see `fact-and-claim-discipline.md` — verify it first)
- Emotionaler/rhetorischer Kontrast: set up a negated expectation, then
  resolve it
- A one-word sentence fragment for deliberate rhythm break, used sparingly

**German confidence calibration, stated precisely**: the register is "die
Noblesse von jemandem, der es nicht nötig hat" — the composure of someone
who doesn't need to shout about it. The mechanism is specificity and
evidentiary density, not intensifiers: "Ich bin davon überzeugt, dass ich
die nötigen Fähigkeiten mitbringe" (stated as personal conviction) is the
German-register equivalent of "I am certain that I have the necessary
skills" (flat assertion) — understatement is a grammatical move (davon
überzeugt, dass...), not just fewer adjectives. Never use superlatives
("stets," "absolut," "einzigartig," "der Beste") — these are a named,
specific recruiter red flag, not just generically risky.

**Unreliable claim, do not cite**: a widely-repeated "HBR analysis of
2,400 hiring managers found the strongest cover letters are exactly 247
words" statistic could not be verified anywhere and has the signature of
fabricated SEO content. Don't use it.

## Negative example: don't model sentence style on job-board templates

Major job board "official" sample letters (StepStone's published templates
were checked directly) are reliable for macro layout but routinely
paratactic at the sentence level — flat fact-listing with at best one weak
connector tacked onto the end of a paragraph, sometimes still using
Konjunktiv ("würde...reizen") that every style guide warns against. Use
`letter-structure-de.md`/`letter-structure-en.md` for layout, not for
sentence craft — a structurally-correct template is not evidence of good
prose, and this is exactly how a letter ends up sounding like an email
despite having the right paragraphs in the right order.

## Paragraph-to-paragraph bridges

Each paragraph's opening sentence should pick up a word or idea from the
previous paragraph's closing sentence (an explicit callback), not announce
a new topic cold. At least one paragraph transition in the letter should
be causal or consequential ("That experience is exactly why...") rather
than merely additive ("In my last role, I also...").
