"""
Produces two labeled, transparent proxy scores for a resume. Neither
simulates a real vendor's actual proprietary algorithm — no vendor
publishes one in enough detail to replicate, and see
references/what-ats-actually-do.md for why a single "beat the ATS" score
is largely a myth to begin with. What this script computes instead:

1. KEYWORD-MATCH SCORE (labeled "Workday-style" because this — percentage
   keyword overlap against a specific posting, gated by structural safety
   — is what most commercial "ATS score" checkers actually compute and
   market under that name, including tools that claim to simulate Workday
   specifically. It is not Workday's real internal algorithm, which is not
   public.

2. HACKERRANK-RUBRIC SCORE: HackerRank's 2026 open-source ATS scores four
   categories worth 120 points total; only three are publicly documented
   with their point values (Open Source Contributions 35, Self/Personal
   Projects 30, Technical Skills 10 — the fourth category's exact criteria
   and point value were not found in public documentation). This script
   scores only those three documented categories via heuristics on the
   resume's actual section content, out of a 75-point documented subtotal,
   and says so explicitly rather than inventing the missing category.
   HackerRank's own tool has documented scoring inconsistency (the same
   unchanged resume scored 66-99 across repeated runs) — treat any number
   from this heuristic, or from the real tool, as a rough signal only.

Usage:
    python ats_score.py workday <resume.docx> <job_posting.txt> [--structural-findings N]
    python ats_score.py hackerrank <resume.docx>
    python ats_score.py both <resume.docx> <job_posting.txt>
"""
import argparse
import re
import sys
from pathlib import Path

import docx

sys.path.insert(0, str(Path(__file__).parent))
from keyword_audit import audit  # noqa: E402


def _full_text(path):
    d = docx.Document(path)
    return "\n".join(p.text for p in d.paragraphs)


def _sections(path):
    """Split into (heading, body_text) by finding bold/colored short all-caps paragraphs."""
    d = docx.Document(path)
    sections = {}
    current = None
    for p in d.paragraphs:
        text = p.text.strip()
        is_heading = (
            text
            and text.upper() == text
            and len(text) < 40
            and any(r.font.bold for r in p.runs if r.font.bold is not None)
        )
        if is_heading:
            current = text
            sections[current] = []
        elif current:
            sections[current].append(text)
    return {k: "\n".join(v) for k, v in sections.items()}


def workday_style_score(resume_path, job_path, structural_critical=0, structural_warning=0, exclude=None):
    resume_text = _full_text(resume_path)
    job_text = Path(job_path).read_text(encoding="utf-8", errors="ignore")
    result = audit(resume_text, job_text, set(), exclude or set())
    matched, missing = result["matched"], result["missing"]
    total = len(matched) + len(missing)
    raw_pct = round(100 * len(matched) / total) if total else 0

    score = raw_pct
    notes = []
    if structural_critical:
        score = min(score, 40)
        notes.append(f"{structural_critical} CRITICAL structural finding(s) present — score capped at 40 regardless of keyword match, since a parser that mis-reads the layout may not even reach the keyword-matching stage.")
    if structural_warning:
        score = max(0, score - 10 * structural_warning)
        notes.append(f"{structural_warning} structural WARNING(s) — 10 points deducted each.")

    return {
        "label": "Keyword-match proxy score (labeled 'Workday-style' — see script docstring for why)",
        "raw_keyword_match_pct": raw_pct,
        "score": score,
        "matched_terms": len(matched),
        "total_terms": total,
        "notes": notes,
        "missing_terms": [t for t, _n in missing],
        "REQUIRED_NEXT_STEP": (
            "Do not report the score above without also sorting every term in "
            "missing_terms into: noise (company name / generic filler / bigram "
            "artifact), true-but-differently-worded (resume already supports this "
            "— reword and say so), or a real gap (say so plainly, do not add the "
            "word without the substance behind it). A bare percentage is not a "
            "finished answer."
        ),
    }


def hackerrank_rubric_score(resume_path):
    sections = _sections(resume_path)
    findings = []

    # --- Open Source Contributions (documented weight: 35) ---
    # Heading and contribution-language matching is bilingual (EN/DE) so a
    # translated resume describing the identical real contribution doesn't
    # score lower purely because the heuristic only knew English words.
    os_section = next((v for k, v in sections.items() if "OPEN SOURCE" in k), None)
    os_points = 0
    if os_section:
        entries = [line for line in os_section.split("\n") if line.strip()]
        os_points += 10
        if re.search(r"github\.com|gitlab\.com|\brepo\b", os_section, re.I):
            os_points += 10
        else:
            findings.append("Open Source section has no repo URL or explicit 'repo' mention — HackerRank's rubric rewards demonstrable OSS, not just a labeled section.")
        if re.search(r"contribut|beitrag|beigetragen|pull request|\bPR\b|merged|maintainer|stars|sterne", os_section, re.I):
            os_points += 10
        else:
            findings.append("No contribution-mechanics language (contributed/Beitrag, merged PR, maintainer, stars) found — entries may read as employer/institutional work relabeled 'OSS' rather than clear public contribution.")
        if len(entries) >= 3:
            os_points += 5
    else:
        findings.append("No 'OPEN SOURCE' section found at all.")
    os_points = min(os_points, 35)

    # --- Self / Personal Projects (documented weight: 30) ---
    proj_section = next((v for k, v in sections.items() if "PERSONAL PROJECT" in k or "PROJECTS" in k or "PROJEKTE" in k), None)
    proj_points = 0
    if proj_section:
        entries = [line for line in proj_section.split("\n") if line.strip()]
        proj_points += 15
        if len(entries) >= 4:
            proj_points += 10
        if re.search(r"\d", proj_section):
            proj_points += 5
    else:
        findings.append("No 'PERSONAL PROJECTS' section found.")
    proj_points = min(proj_points, 30)

    # --- Technical Skills (documented weight: 10) ---
    skills_section = next((v for k, v in sections.items() if "SKILL" in k or "KENNTNISSE" in k), "")
    category_count = len(re.findall(r"^\S.*?:", skills_section, re.M))
    skills_points = min(10, category_count * 2)

    documented_total = 75
    score = os_points + proj_points + skills_points

    return {
        "label": "HackerRank documented-rubric proxy (3 of 4 categories; 4th category's weight/criteria not public)",
        "open_source_points": f"{os_points}/35",
        "personal_projects_points": f"{proj_points}/30",
        "technical_skills_points": f"{skills_points}/10",
        "documented_subtotal": f"{score}/{documented_total}",
        "findings": findings,
        "caveat": "HackerRank's own tool scored an unchanged resume 66-99 across repeated runs. Treat this number, and that one, as a rough signal only, not a verdict.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["workday", "hackerrank", "both"])
    parser.add_argument("resume")
    parser.add_argument("job", nargs="?")
    parser.add_argument("--structural-critical", type=int, default=0)
    parser.add_argument("--structural-warning", type=int, default=0)
    parser.add_argument("--exclude", default="", help="comma-separated company name/location terms to never treat as a missing keyword")
    args = parser.parse_args()

    if args.mode in ("workday", "both"):
        if not args.job:
            print("workday mode requires a job posting path", file=sys.stderr)
            sys.exit(2)
        from keyword_audit import normalize
        exclude = {normalize(t.strip()) for t in args.exclude.split(",") if t.strip()}
        result = workday_style_score(args.resume, args.job, args.structural_critical, args.structural_warning, exclude)
        print("=== Workday-style keyword-match proxy ===")
        for k, v in result.items():
            print(f"{k}: {v}")
        print()

    if args.mode in ("hackerrank", "both"):
        result = hackerrank_rubric_score(args.resume)
        print("=== HackerRank documented-rubric proxy ===")
        for k, v in result.items():
            print(f"{k}: {v}")
