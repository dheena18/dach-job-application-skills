# DACH-Bewerbungs-Skills für Claude

[🇬🇧 English](README.md) · 🇩🇪 Deutsch

Eine Sammlung von [Claude-Code](https://claude.com/claude-code)-Skills, die beim Erstellen und Anpassen von Bewerbungen **für den deutschsprachigen Raum (DACH: Deutschland, Österreich, Schweiz)** helfen: Lebenslauf, Anschreiben und ATS-Prüfung, jeweils auf Deutsch und Englisch.

> **Hauptzielmarkt: Deutschland / DACH.** Die Konventionen unterscheiden sich von den USA/UK: Sprachregister, Aufbau, Muss-/Kann-Kriterien, die fragmentierte deutsche ATS-Landschaft (Personio, SAP SuccessFactors, Softgarden, …), „ss“ statt „ß“ in der Schweiz usw. Die Skills sind genau darauf ausgelegt.

## Inhalt

| Skill | Was er macht |
|---|---|
| `resume-matcher` | Wählt zu einer Stellenanzeige die passendste Lebenslauf-Variante aus deinem Set (oder sagt, dass keine passt), mit nachvollziehbarer Begründung. |
| `resume-tailor` | Passt einen bestehenden Lebenslauf an eine Stelle an, durch Umsortieren und Umformulieren *echter* Inhalte. Erfindet nie Skills, Titel, Daten oder Kennzahlen. |
| `cv-translate-de` | Baut einen englischen Lebenslauf als muttersprachlich formulierten deutschen Lebenslauf neu auf, bei exakt erhaltenem `.docx`-Layout. |
| `cover-letter-writer` | Schreibt ein stellenspezifisches Anschreiben (DE oder EN) als `.docx`, passend zum Layout deines Lebenslaufs. |
| `resume-summary-writer` | Schreibt oder bewertet das Kurzprofil, mit DACH- bzw. internationalen Konventionen. |
| `ats-resume-check` | Prüft, ob ein Lebenslauf (`.docx`/PDF) in gängigen ATS-Systemen korrekt gelesen wird. |

Alle Skills liegen in [`skills/`](skills/). Jeder hat eine eigene `SKILL.md` und `README.md`.

## Nutzung

1. Repo klonen oder `skills/` und `AGENTS.md` in ein eigenes Projekt kopieren, dann `setup.ps1` (Windows) bzw. `./setup.sh` (macOS/Linux) ausführen. Das verlinkt `skills/` nach `.claude/skills` und `.agents/skills`, damit Claude Code, Codex und ähnliche Agenten die Skills automatisch finden.
2. **Eigene** Lebensläufe ins Projekt legen (z. B. `job-resume/EN/`, `job-resume/DE/`). Sie sind hier bewusst per `.gitignore` ausgeschlossen.
3. Für `resume-matcher`: `references/resume-profiles.md` und `RESUME_PROFILES` in `scripts/compare_resumes.py` an das eigene Lebenslauf-Set anpassen (die acht Profile sind Beispiele). Lebenslauf-Dateien werden über den Variantennamen gefunden, z. B. `<Name>_Cloud_Engineer.docx` und `<Name>_Cloud_Engineer-DE.docx`; eigene Dateinamen funktionieren also.
4. Projekt in einem beliebigen KI-Coding-Agenten öffnen (Claude Code, Codex, Cursor, Gemini CLI, Copilot, …). Sie lesen [`AGENTS.md`](AGENTS.md) mit Skill-Übersicht und Ordnerstruktur. Dann z. B. fragen: *„Welcher Lebenslauf passt zu dieser Anzeige?“*, *„Passe meinen Lebenslauf an diese Stelle an“*, *„Schreibe ein deutsches Anschreiben für diese Rolle“*.

Abhängigkeiten einmalig mit `pip install -r requirements.txt` installieren. Seitenzahl und PDF-Export nutzen unter Windows Microsoft Word (falls vorhanden), sonst LibreOffice (jedes Betriebssystem). Skripte, die mehrere Skills nutzen, liegen in [`skills/_shared/`](skills/_shared/).

## Datenschutz

Dieses Repository enthält **keine personenbezogenen Daten**. Die `.gitignore` schließt `*.docx`, `*.pdf`, `Resume/`, `job-resume/` und `output/` aus. Eigene Unterlagen bleiben lokal; vor jedem Push `git status` prüfen.

## Inspiration & Quellen

Dieses Projekt wurde von folgenden Projekten inspiriert und baut auf deren Ideen auf:

- [tharun-kumar-korinepalli/job-application-claude-skills](https://github.com/tharun-kumar-korinepalli/job-application-claude-skills): zusammengeführtes Bewerbungs-Skill-Kit (MIT).
- [usr1243/claude-bewerbung-skill](https://github.com/usr1243/claude-bewerbung-skill): Skill für Schweizer/deutsche Lebensläufe und Anschreiben.

Diese Projekte nennen wiederum u. a.: [hgrosche95/job-application-skill](https://github.com/hgrosche95/job-application-skill), [jezweb/claude-skills](https://github.com/jezweb/claude-skills), [dabydat/resume-builder-skill](https://github.com/dabydat/resume-builder-skill), [Faizee-Asad/job-seeker-claude-skills](https://github.com/Faizee-Asad/job-seeker-claude-skills), [Paramchoudhary/ResumeSkills](https://github.com/Paramchoudhary/ResumeSkills), [olegvg/resume-tailor-plugin](https://github.com/olegvg/resume-tailor-plugin), [proficientlyjobs/proficiently-claude-skills](https://github.com/proficientlyjobs/proficiently-claude-skills) sowie deutsche Quellen wie Karrierebibel, Stepstone, Bundesagentur für Arbeit und DIN 5008.

Die Skills in diesem Repo sind eigenständig geschrieben und für den DACH-Markt erweitert (muttersprachlicher deutscher Neuaufbau, layouterhaltende `.docx`-Pipeline, Lebenslauf-Routing).

## Lizenz

[MIT](LICENSE)
