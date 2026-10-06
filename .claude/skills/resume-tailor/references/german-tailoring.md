# Tailoring for the German/DACH market

## Reading a German posting

German postings often (not always, this is convention not standard) split
requirements into two implicit tiers:

- **Muss-Kriterien** (must-have): phrased definitively — "zwingend
  erforderlich ist," "Voraussetzung ist," "Sie verfügen nachweislich über,"
  "Sie bringen mit." Usually listed first.
- **Kann-Kriterien** (nice-to-have): phrased tentatively — "wünschenswert,"
  "von Vorteil," "idealerweise," "zusätzlich freuen wir uns über." Usually
  listed after the must-haves.

This split is a documented, widely-used convention, not a rule postings are
obligated to follow — the fit-table exercise still requires judgment about
which requirement is actually load-bearing, the same as in English.

## Keyword mirroring is explicitly endorsed, not just tolerated

Unlike some English-language advice that hedges on keyword mirroring,
German career-advice sources are direct about it: reuse the posting's own
terms "möglichst wortgleich" (as close to word-for-word as possible). A
specific, documented practice: list both the German and English term for a
skill or role where the posting or market uses both, e.g. "EDV-Kenntnisse
(IT-Kenntnisse)" — because an ATS or a human search may only recognize one
variant. This is treated as diligence and thoroughness in German hiring
culture, not as gaming the system — as long as it's true.

The same authenticity line still applies as anywhere else: German sources
explicitly warn that keywording skills the candidate doesn't have reads as
"unauthentisch oder übertrieben" (inauthentic or exaggerated), and warn
against keyword-stuffing "ohne Substanz" as a credibility risk with both
software and human readers. Mirror accurately; don't stuff.

## The German ATS landscape is genuinely fragmented

No single dominant platform — SAP SuccessFactors, Personio, Softgarden, and
rexx systems each hold a meaningful share of the German market (all above
5% per the ICR Heidelberg market survey), with no one system covering a
majority. Don't tailor or format around the assumption of one specific
platform's known behavior unless the posting or company is confirmed to use
it. See `ats-resume-check`'s `references/what-ats-actually-do.md` for what's
actually documented per platform.

## Language-matching mechanics: genuine uncertainty here

Whether any specific German ATS stems compound words correctly (does
matching "Datenanalyse" also match "Datenanalyst"?) or normalizes umlaut
variants (ä/ö/ü vs. ae/oe/ue) is **not documented** by any vendor found in
research — this is a real evidence gap, not a confirmed negative. Given
that gap, the safe default is to write the term the way a human reader
would expect it (with proper umlauts, standard spelling) and, where the
posting or the market commonly uses both a German and an English term for
the same thing, include both rather than relying on the system to equate
them.

## What doesn't change from the general tailoring approach

The core rule (`fit-and-keywords.md`) and the anti-tell guardrails
(`avoiding-ai-tailored-tells.md`) apply exactly the same way in German —
no 95-100% match, no mirroring the posting's own requirement order, no
listing a tool with no evidence behind it, no cross-bullet verb echo. And
any bullet actually being reworded still has to sound native, not
translated — apply `cv-translate-de`'s `native-german-style.md` rules to
any German sentence you write or rewrite during tailoring.
