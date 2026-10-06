# _shared

Not a skill (no `SKILL.md`). Scripts used by several skills, kept in one place so they cannot drift apart.
Run them from the repo root, e.g. `python skills/_shared/scripts/check_pages.py pages <file.docx>`.

| Script | Used by | Purpose |
|---|---|---|
| `docx_inspect.py` | cv-translate-de, resume-tailor, cover-letter-writer | Dump a `.docx`'s paragraph/run structure (incl. font) as JSON |
| `docx_rewrite.py` | cv-translate-de, resume-tailor | Apply a rewrite plan while preserving formatting |
| `validate_docx.py` | cv-translate-de, resume-tailor | Portable structural check after scripted edits |
| `check_pages.py` | cv-translate-de, resume-tailor, cover-letter-writer | Page count + PDF export (Word on Windows, else LibreOffice) |
| `check_ats.py` | ats-resume-check, cv-translate-de, resume-tailor | ATS parseability: `docx`, `pdf` or `both` |
| `ats_score.py` | ats-resume-check | Workday / HackerRank-style score estimates |
| `keyword_audit.py` | resume-tailor, resume-matcher, ats-resume-check | Keyword diff between resume and posting (EN/DE) |

Install dependencies once: `pip install -r requirements.txt`.
