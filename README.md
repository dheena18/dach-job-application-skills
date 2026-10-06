# DACH Job Application Skills for Claude

🇬🇧 English · [🇩🇪 Deutsch](README.de.md)

A set of [Claude Code](https://claude.com/claude-code) skills that help you build and tailor job applications **for the German-speaking market (DACH: Germany, Austria, Switzerland)**: resumes (*Lebenslauf*), cover letters (*Anschreiben*) and ATS checks, in English and German.

> **Primary target: Germany / DACH.** Conventions differ from the US/UK: register, structure, *Muss-/Kann-Kriterien*, the fragmented German ATS landscape (Personio, SAP SuccessFactors, Softgarden, …), `ss` instead of `ß` in Switzerland, and so on. The skills are built around these differences.

## What's inside

| Skill | What it does |
|---|---|
| `resume-matcher` | Given a job posting, picks the best-fitting resume variant from your set (or says none fits), with visible reasoning. |
| `resume-tailor` | Tailors an existing resume to a specific posting by reordering and rewording *real* content. Never invents skills, titles, dates or metrics. |
| `cv-translate-de` | Rebuilds an English resume as a natively written German *Lebenslauf* while preserving the `.docx` layout exactly. |
| `cover-letter-writer` | Writes a posting-specific cover letter / *Anschreiben* (EN or DE) as a `.docx` styled to match your resume. |
| `resume-summary-writer` | Writes or critiques the summary block (*Kurzprofil*) using DACH vs. international conventions. |
| `ats-resume-check` | Checks whether a `.docx`/PDF resume will parse correctly in common ATS systems. |

All skills live in [`skills/`](skills/). Each has its own `SKILL.md` and `README.md`.

## Usage

1. Clone this repo, or copy `skills/` and `AGENTS.md` into your own project, then run `setup.ps1` (Windows) or `./setup.sh` (macOS/Linux). This links `skills/` into `.claude/skills` and `.agents/skills` so Claude Code, Codex and similar agents discover the skills automatically.
2. Put **your own** resumes in the project (e.g. `job-resume/EN/`, `job-resume/DE/`). They are git-ignored here on purpose.
3. For `resume-matcher`, edit `references/resume-profiles.md` and `RESUME_PROFILES` in `scripts/compare_resumes.py` to describe your resume set (the eight profiles are examples).
4. Open the project in any AI coding agent (Claude Code, Codex, Cursor, Gemini CLI, Copilot, …). They read [`AGENTS.md`](AGENTS.md), which lists the skills and the folder layout. Then ask, e.g. *"Which resume fits this posting?"*, *"Tailor my resume to this job"*, *"Write a German Anschreiben for this role"*.

The Python scripts need `python-docx` (and LibreOffice for PDF export / page checks where noted in each skill).

## Privacy

This repository contains **no personal data**. `.gitignore` excludes `*.docx`, `*.pdf`, `Resume/`, `job-resume/` and `output/`. Keep your own documents local and check `git status` before every push.

## Inspiration & credits

This project was inspired by, and builds on ideas from:

- [tharun-kumar-korinepalli/job-application-claude-skills](https://github.com/tharun-kumar-korinepalli/job-application-claude-skills): a merged job-application skill kit (MIT).
- [usr1243/claude-bewerbung-skill](https://github.com/usr1243/claude-bewerbung-skill): Swiss/German CV and *Anschreiben* skill.

Those projects in turn credit, among others: [hgrosche95/job-application-skill](https://github.com/hgrosche95/job-application-skill), [jezweb/claude-skills](https://github.com/jezweb/claude-skills), [dabydat/resume-builder-skill](https://github.com/dabydat/resume-builder-skill), [Faizee-Asad/job-seeker-claude-skills](https://github.com/Faizee-Asad/job-seeker-claude-skills), [Paramchoudhary/ResumeSkills](https://github.com/Paramchoudhary/ResumeSkills), [olegvg/resume-tailor-plugin](https://github.com/olegvg/resume-tailor-plugin), [proficientlyjobs/proficiently-claude-skills](https://github.com/proficientlyjobs/proficiently-claude-skills), plus German sources such as Karrierebibel, Stepstone, Bundesagentur für Arbeit and DIN 5008.

The skills in this repo are independently written and extended for the DACH market (native German rebuild, format-preserving `.docx` pipeline, resume routing).

## License

[MIT](LICENSE)
