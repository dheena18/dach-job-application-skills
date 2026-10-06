# Fact and claim discipline

Every item here is a mistake a verification agent actually caught in a real
test letter, not a hypothetical. Read this before finalizing any letter's
factual claims — it catches a different failure mode than
`banned-phrases-de-en.md` (which is about *tone*, not *truth*).

## Don't invent reasoning, even plausible reasoning

A CAR-framed achievement needs Context, but "context" means a fact that's
actually in the resume or that the user has confirmed — not a plausible-
sounding backstory invented to make the achievement land better. A letter
once stated "weil Standardprompts bei unternehmensspezifischen Anfragen zu
inkonsistenten Antworten führten" as the reason a system was built — this
read as confident, documented fact, but nothing in the resume said that was
the actual problem. It's plausible, which is exactly what makes it
dangerous: a recruiter who asks "how do you know that was the cause?" finds
daylight between the letter and what's documented. If the real motivation
isn't stated anywhere, use goal-oriented framing instead ("um die
Genauigkeit zu verbessern", "to improve accuracy") — a goal directly implied
by a measured result is a much safer claim than an invented causal history.

## Verify company facts before citing them as a hook

A letter's hook is supposed to be the one thing that makes it non-generic,
but a generic-sounding claim that happens to be specific is worse than no
claim at all if it's wrong. A letter once described a B2B systems
integrator as running its parent telecom brand's own consumer network for
"millions of end customers" — invented to sound impressive, and it directly
contradicted both the posting's own "Über uns" text and the letter's own
opening paragraph. Before using any fact about the target company as a
hook, confirm it's actually true of *that specific legal entity*, not just
plausible-sounding about the brand it's associated with. If the fact isn't
already given by the posting or the user, a quick web search for a real,
current, named product/initiative is worth doing — a correct specific fact
beats an incorrect specific fact every time, and beats a generic one too.

## Check temporal accuracy against the resume's own dates

Compare any "currently" / "aktuell" claim against the actual dates on the
resume relative to today's date. A letter once said "aktuell forsche ich
an..." for a research role the resume itself dated as having ended several
months earlier. Before writing any present-tense claim about an ongoing
activity, check the date range it's based on.

## Scope timeframe claims to exactly what's evidenced

If an achievement type applies to only part of a stated time range, don't
extend the claim to the whole range. A letter once said "for the past two
years, the work I've built has been for exactly that kind of client" when
the specific client type (regulated/financial-legal documents) was
actually true of a five-month engagement within that two-year window, not
the whole window. Say "one of the systems I built was for exactly that
kind of client," not "two years of my work has been for exactly that kind
of client," unless the whole range genuinely supports it.

## Don't hedge a gap disclosure by arguing with an objection nobody raised

When naming a gap per `gap-and-weakness-framing.md`, state the fact and
stop. A letter once added "...and wanted to be upfront about where that
stands rather than have it come up later" after disclosing a language
level below the posting's requirement — this is the "arguing with nobody"
pattern from `banned-phrases-de-en.md` rule 5, and it draws more attention
to the gap than the plain fact does. Also avoid leaning on a weak inference
about the employer (e.g. "your multiple office locations suggest English
is fine") to argue a stated hard requirement away — if the employer wrote
a specific level requirement, a guess about their internal language mix
doesn't resolve it. A concrete fact already true of the candidate (e.g.
"the systems I built process German documents daily") is a much stronger,
more honest pivot than an inference about the employer's possible leniency.

## Don't blur achievements from different employers together

A proof paragraph often needs 2-3 achievements, and the natural way to add
the second one is "... habe ich außerdem ..." / "I also ..." — but if that
second achievement is from a *different* employer or a different, non-
overlapping timeframe than the one just named, stitching it on with
"außerdem"/"also" implies it happened in the same engagement. This
happened independently in two separate letters: a university research
role's evaluation pipeline got folded into a sentence about "einem
Unternehmenskunden" from a different, earlier job, and (separately) framed
with reasoning borrowed from the posting's own "vor der Kundenübergabe"
language that had no basis in that research context at all. Before adding
a second achievement to a paragraph, check which employer and which dates
it actually belongs to — if they don't match the paragraph's existing
frame, give it its own sentence or its own paragraph with its own honest
context ("In an earlier internship...", "In der anschließenden
Forschung..."), not a stitched-on "außerdem."

## Active voice, including in the closing line

This has been violated independently in both the German and English test
rounds, always in the closing paragraph specifically — it seems to be the
easiest place to slip into passive construction ("...wie diese Systeme
abgesichert... gehalten werden" / "Manual triage was eliminated...").
Check the closing sentence for passive voice specifically; it's the one
place this keeps recurring.

## Extract real style values, don't guess

Run `docx_inspect.py` on the actual resume being submitted for this
specific application and use its real heading size exactly — don't pick a
round number that looks about right. See `visual-consistency.md` for the
full rule (body size can be deliberately adjusted for readability; heading
size should not be).
