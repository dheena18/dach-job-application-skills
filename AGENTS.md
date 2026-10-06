# AGENTS.md

Instructions for any AI coding agent (Claude Code, Codex, Cursor, Gemini CLI, Copilot, …) working in this repo.
This repo is a set of job-application skills for the German-speaking market (DACH). Respond in the user's language (English or German).

## Skills

Each skill is a folder in [`skills/`](skills/) with a `SKILL.md` (instructions), optional `references/` and `scripts/`.
When a task matches a skill, **read its `SKILL.md` first and follow it**.

| Task | Skill |
|---|---|
| Which resume fits this posting? | `skills/resume-matcher/SKILL.md` |
| Tailor a resume to a posting | `skills/resume-tailor/SKILL.md` |
| English resume → German Lebenslauf | `skills/cv-translate-de/SKILL.md` |
| Cover letter / Anschreiben | `skills/cover-letter-writer/SKILL.md` |
| Write or critique the summary / Kurzprofil | `skills/resume-summary-writer/SKILL.md` |
| ATS parseability check | `skills/ats-resume-check/SKILL.md` |

Agents with native skill discovery (Claude Code: `.claude/skills/`, Codex and others: `.agents/skills/`) get the skills via `setup.ps1` / `setup.sh`. Agents without it just read the files above.

## Folder layout

```
skills/                     Skills (committed)
job-resume/EN/              Master resumes, English        (private, git-ignored)
job-resume/DE/              Master resumes, German (-DE)   (private, git-ignored)
job-resume/tailored/        Posting-specific resumes       (private, git-ignored)
Resume/                     Legacy flat copy of resumes    (private, git-ignored)
output/<skill-name>/        Everything a skill generates   (private, git-ignored)
```

Output files are named `<Name>_<Variant>[-DE]-<Company>[-YYYY-MM-DD].docx` (+ `.pdf`). Never write generated files next to the master resumes.

## Rules

- **Never commit personal data.** Resumes, cover letters, `.docx`, `.pdf`, `job-resume/`, `Resume/`, `output/` are git-ignored; keep it that way. Check `git status` before any commit or push.
- **Never invent facts.** No skills, titles, employers, dates or metrics that are not in the user's source resume.
- Preserve `.docx` formatting (fonts, colours, bullets, page count) when editing resumes; use the scripts in each skill's `scripts/`.
- Scripts need Python 3 and `python-docx`; PDF export / page checks need LibreOffice (`soffice`) where noted in the skill.
- Commit as the repo's configured git identity (GitHub noreply email); do not change it.
