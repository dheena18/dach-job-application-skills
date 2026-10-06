# What to translate, what to leave alone, and what to never change

All examples below are invented placeholders — never copy a real user's
resume content into this file.

## Never touch these, under any circumstance

These have to match the underlying certificates, contracts and public
record exactly. Changing wording here isn't a translation choice, it's
turning a true document into a false one:

- Person's name.
- Company / employer names, university / institution names.
- The literal degree title as conferred (see "Degree titles" below).
- Dates, durations, grades, percentages, and every other number.
- Job titles that were the actual, contractual title — see "Job titles"
  below for how to present (not alter) these.
- **Any titled work**, as one category: publication titles, DOIs, thesis
  titles, competition/award names, and a personal or open-source project's
  own name. These all have the same property — a title that exists as a
  fixed string somewhere outside this document (a submitted thesis, a
  published paper, a competition's own name, a repo name) — so the same
  rule applies to all of them: never translate or reword the title itself,
  only the descriptive sentence around it. Don't split hairs about which of
  these sub-categories a given line falls into; if it names a specific
  piece of work, it's protected.

If something here looks wrong, awkward, or non-standard, flag it to the user
instead of silently "fixing" it. It may be exactly correct on the actual
document.

## The self-authored header tagline

Some resumes have a line under the name that isn't a contractual job title
but a self-written positioning tagline (e.g. "AI Engineer | LLM & Agentic
Systems | Cloud Deployment"). Treat it the same way as a job title: default
to keeping it in English, for the same market-usage reason (see "Job
titles" below). It's the person's own branding, not a fact tied to a
document, so this is a lower-stakes default than the protected categories
above — if the user has a preference, follow it.

## Skills-section category labels

A skills section groups tools under labels ("Languages:", "Models:", "Cloud &
DevOps:"). Translate a label only when it's a plain common noun with an
obvious, unforced German word: "Languages" → "Sprachen", "Models" →
"Modelle", "Vector & Data Stores" → "Vektor- & Datenspeicher". Leave a label
in English when it's itself a compound technical/methodology term with no
natural unforced German equivalent: "Cloud & DevOps", "Backend & APIs", "LLM
& Agentic AI", "ML & Experiment Tracking" — forcing these into German produces jargon nobody uses
("Agentische KI") and reads worse than leaving them alone. Apply this
distinction consistently across every category label in the same document;
translating some plain ones and leaving the jargon ones in English is
correct, but it must be the same rule applied everywhere, not a per-label
guess — a reader will notice an inconsistent pattern even if each individual
choice was defensible on its own.

## Tools, frameworks, product names, certifications

Keep in their original form. A German IT/AI job market uses these names in
English natively — translating "Kubernetes" or a certification name into
German would be both wrong and would break keyword matching against the
posting/ATS. This includes programming languages, libraries, cloud service
names, methodology names (Scrum, CI/CD), and file formats.

This is about names, not every English concept-word in a sentence. When you
need a common noun *around* those names — describing a system, a workflow,
a team of agents — and German already has a natural, established compound
for it, use the German compound rather than bolting the English word onto a
German suffix with a hyphen: "Agentensysteme", not "Agentic-Systeme";
"Kontexterhalt", not "Kontext-Retention". Reach for an English-root hybrid
only when the concept genuinely has no natural German compound (the way
"Fine-Tuning" or "Context Engineering" do, which is why those stay as
English loan-terms rather than getting a forced translation) — don't default
to the hybrid just because the source sentence used the English word.

Related: if an English compound resists a clean German rendering either way
(a calque sounds stilted, a bare English loan sounds bolted-on — "pass/fail
basis" is a real example of this), don't force a compound noun at all.
Restructure as a plain clause instead: "bewertet jedes Bild als bestanden
oder nicht bestanden" reads better than either "Pass/Fail-Basis" or a
calqued "Bestehen-oder-Nichtbestehen-Prinzip".

## Job titles

German tech postings commonly use English role titles verbatim (e.g. a
"Backend Engineer" posting is written that way, not "Rückend-Ingenieur").
Default: keep an English job title in English. Two exceptions:

1. The posting/target market for this specific application uses a German
   title convention — ask the user rather than guessing, this is a
   market-usage judgment call, not a hard rule.
2. The role's own institutional term is already German. Some employment
   categories in Germany are legally/institutionally named in German even on
   an English CV (a classic example: a university-affiliated part-time
   research role during study). If the original CV already used the correct
   German institutional term, keep that term as-is — it does not need
   translating into an English equivalent or vice versa.

## Degree titles

Translate the *narrative around* a degree (thesis description, coursework)
but not the conferred title itself unless the user confirms the institution
issues it under a different official name. If unsure which is correct,
ask: "Does your certificate say this exact title, or a German-language
title? I don't want to print a credential name that doesn't match your
Zeugnis." Where a foreign (non-German) degree needs a German-market
equivalence note, add it in brackets after the original, don't replace it:
"B.Tech Informatik (entspricht Bachelor of Engineering)".

## Country and location names

Common nouns like the country name do get localized in a German document:
"Germany" → "Deutschland", "India" → "Indien". This is different from
translating a proper noun like a company name — a country name is a
descriptive term, not an identifier that has to match a legal document.

## Fact-preservation rule for the rewrite itself

The output must contain exactly the same claims as the input: same
employers, same dates, same metrics, same tools, same number of bullets
making the same points. Only the wording and grammar change to read as
native German. If compressing a sentence to fit the page would require
dropping a specific number or tool name to shorten it, don't — shorten the
connective tissue around it instead, and if it still doesn't fit, say so to
the user rather than quietly cutting the fact (see
`references/format-pipeline.md` for the compression order to try first).

## Language-level lines

If the CV lists a language proficiency (e.g. "German: B1"), leave the CEFR
level exactly as given. This is one of the modules of information most
scrutinized in a DACH hiring process — never round it up.

A source CV often lists some languages with a CEFR level and others with a
plain English word instead (e.g. "Tamil: Native", "Hindi: Intermediate") —
CEFR doesn't really apply to a native language, and a non-CEFR self-rating
is still a proficiency claim, so it needs the same care. Unambiguous
mappings are safe to apply directly: "Native" → "Muttersprache", "Fluent" →
"Fließend". A word like "Intermediate" is genuinely ambiguous — it could
reasonably become "Grundkenntnisse", "Gute Kenntnisse", or "Fortgeschritten"
depending on what the person actually means by it, and picking wrong
quietly misrepresents a screened fact. Confirm with the user rather than
picking a mapping for them.

On the foreign-degree equivalence note (see "Degree titles" above): if you
don't have a confirmed anabin/ZAB wording to put in the brackets, omit the
bracketed note entirely rather than invent one. Omitting it is a safe
default; a fabricated equivalence claim is not.
