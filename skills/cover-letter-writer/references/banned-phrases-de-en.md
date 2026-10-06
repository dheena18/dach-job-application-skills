# Banned phrases and AI-writing tells

Recruiters read a high volume of AI-written letters and recognize the shape
fast. This list is what `skills/cover-letter-writer/scripts/lint_letter.py` checks mechanically; read
it before drafting, not just after.

## Universal (both languages)

1. **"Not X, but Y."** "I am not just a coder, I am a problem solver."
   State the claim instead: "I fix the problems that show up between teams."
2. **No one-line dramatic closer.** "That is what I bring." "And that is
   the difference." Cut the line.
3. **No sayings that sound deep.** "At its core," "what really matters,"
   "the real question is." State the fact.
4. **No staged run-up.** "Let me be direct." "Here's the thing." "I'll be
   honest." Just say it.
5. **No arguing with nobody.** "I'm not saying I'm perfect, but..." Delete
   the imagined objection.
6. **No forced triads.** "Fast, reliable, and scalable." If there are two
   things, say two.
7. **No em dashes.** None. A comma, a full stop, or brackets instead.
   Hyphens only inside words. (Same rule `cv-translate-de` enforces on
   resumes — keep the two skills' output consistent.)
8. **No self-assessment without evidence.** "I'm a fast learner with
   excellent communication skills." Show it instead, with a specific fact.
9. **No bold labels, headings, or bullet lists inside the letter body.**
   Prose only.
10. **No paragraphs that all open the same way.** Vary sentence structure
    and length; let one paragraph be shorter than the others.
11. **First person, active voice.** "I built," not "the system was built."

## English-specific banned openers/closers

- "I am writing to express my interest in the position of..."
- "I am excited to apply for..."
- "Please find attached my resume for..."
- "With great enthusiasm..."
- "As a passionate [role]..." / "As a [role], I..."
- "I hope this message finds you well."
- "Thank you for considering my application."
- "I look forward to the opportunity to discuss..."

## English inflated-claims wordlist

Replace with a plain word or a fact: "proven track record," "extensive
experience," "deep expertise," "passionate about," "thrilled," "delighted,"
"honoured," "leverage," "synergy," "cutting-edge," "state-of-the-art,"
"world-class," "seamless," "robust," "holistic," "dynamic," "innovative,"
"impactful," "spearheaded," "empower," "elevate," "unlock," "navigate,"
"landscape," "journey," "tapestry," "testament," "delve," "foster,"
"cultivate," "harness," "underscore," "pivotal," "crucial," "vital,"
"game-changer," "in today's fast-paced world," "ever-evolving." Filler
adverbs to cut: "genuinely," "truly," "really," "highly," "extremely,"
"incredibly," "successfully."

## German-specific banned phrases

- "Hiermit bewerbe ich mich um..."
- "Mit großem Interesse habe ich Ihre Anzeige gelesen."
- "Ich bin ein motivierter Teamplayer."
- "hochmotiviert," "Teamplayer," "belastbar," "flexibel,"
  "kommunikationsstark," "zielorientiert"
- "Ich bringe Leidenschaft mit."
- "Ihr Unternehmen ist ein Global Player."
- "Ich bin überzeugt, dass ich die ideale Besetzung bin."
- "spannende Herausforderung," "mit großem Interesse"

German AI text also over-uses "nicht nur ... sondern auch" and "sowohl ...
als auch" — treat both like the "not X but Y" and forced-triad rules above.

## The test, either language

Read the letter aloud, then ask:

- Could this go to a different company with only the name swapped? If yes,
  it isn't done.
- Would the candidate say these sentences out loud in an interview without
  embarrassment? If no, rewrite.
- Is there one line only this candidate could have written? If no, add one.
- Is there any sentence that signals enthusiasm without saying anything
  concrete? Cut it.
