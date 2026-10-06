#!/usr/bin/env python3
"""Compare a job posting against all of this candidate's resume variants and
report which ones share the posting's *specialized* vocabulary, not just its
shared-tool noise (Python, Docker, AWS appear on all eight variants and tell
you nothing — see references/matching-methodology.md for why this script
reports specialized-term overlap as the primary number, not overall
keyword-match percentage).

This is a deterministic, mechanical starting point, exactly like
keyword_audit.py is for resume-tailor: a necessary input to the matching
decision, not the decision itself. The actual verdict (clear match / needs
tailoring / weak signal / no match) requires reading the posting's
responsibility language and applying references/role-family-signals.md —
see SKILL.md for the full process. Research backing this design (CareerBERT
naming "closely related roles" as the documented hard case; a purpose-built
3-class fit classifier barely beating chance; uncalibrated percentage-bucket
match scores being flagged as unvalidated marketing, not data) is in
references/matching-methodology.md.

Usage:
    python compare_resumes.py --job posting.txt
    python compare_resumes.py --job posting.txt --lang de
    python compare_resumes.py --job posting.txt --exclude "Acme Corp,Berlin"
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from keyword_audit import (
    contains_term,
    extract_terms,
    normalize,
    prepare,
    read_text,
)

# Project-specific paths. Adapt these to your own resume set; this skill is a
# template, not a generic reusable tool — hardcoded paths here are
# intentional, unlike the other skills in this project, which
# stay generic because they're meant to work on anyone's documents.
def _find_project_root() -> Path:
    # Walk up to the repo root (marked by AGENTS.md), so the script works
    # from skills/, .claude/skills/ or .agents/skills/ alike.
    for parent in Path(__file__).resolve().parents:
        if (parent / "AGENTS.md").exists():
            return parent
    return Path.cwd()


PROJECT_ROOT = _find_project_root()
RESUME_DIR_EN = PROJECT_ROOT / "job-resume" / "EN"
RESUME_DIR_DE = PROJECT_ROOT / "job-resume" / "DE"

# Each resume's real, distinguishing specialized vocabulary — the terms that
# are NOT shared across all eight variants (Python/Docker/AWS/CI/CD/Git
# appear almost everywhere and are deliberately excluded here; see
# matching-methodology.md's specialized-vs-shared-skill distinction, based
# on Lightcast's "specialized skills" vs "software skills" split). Built
# from this skill's own resume-profiles.md — keep the two in sync if a
# resume's content changes.
RESUME_PROFILES: dict[str, dict] = {
    "AI_LLM": {
        "file_en": "Firstname_Lastname_AI_LLM.docx",
        "file_de": "Firstname_Lastname_AI_LLM-DE.docx",
        "role_family": "LLM / Agentic AI Engineer (GenAI)",
        "research_track": False,
        "specialized_terms": {
            "rag", "retrieval-augmented generation", "langchain", "langgraph",
            "crewai", "agentic", "multi-agent", "agent systems",
            "prompt engineering", "fine-tuning", "lora", "qlora", "llm",
            "llms", "large language models", "guardrails", "hallucination",
            "vector database", "vector search", "mlops", "tool calling",
            "function calling", "semantic search",
        },
    },
    "AI_Research": {
        "file_en": "Firstname_Lastname_AI_Research.docx",
        "file_de": "Firstname_Lastname_AI_Research-DE.docx",
        "role_family": "AI/ML Research Engineer / Research Scientist track",
        "research_track": True,
        "specialized_terms": {
            "diffusion", "gans", "publications", "peer-reviewed", "phd",
            "reinforcement learning", "generative", "bayesian optimization",
            "gaussian process", "eval", "evaluation", "llm-as-judge",
            "computer vision", "fine-tuning",
        },
    },
    "Backend_SoftwareEngineer": {
        "file_en": "Firstname_Lastname_Backend_SoftwareEngineer.docx",
        "file_de": "Firstname_Lastname_Backend_SoftwareEngineer-DE.docx",
        "role_family": "Backend Software Engineer",
        "research_track": False,
        "specialized_terms": {
            "c#", "backend", "api design", "microservices", "rest",
            "rest api", "graphql", "grpc", "ownership", "code review",
            "system design", "architecture", "node.js", "spring boot",
        },
    },
    "Cloud_Engineer": {
        "file_en": "Firstname_Lastname_Cloud_Engineer.docx",
        "file_de": "Firstname_Lastname_Cloud_Engineer-DE.docx",
        "role_family": "Cloud Engineer / Infrastructure",
        "research_track": False,
        "specialized_terms": {
            "terraform", "ansible", "aws", "azure", "gcp", "google cloud",
            "vmware", "proxmox", "k8s", "kubernetes",
        },
    },
    "DataEngg_AI": {
        "file_en": "Firstname_Lastname_DataEngg_AI.docx",
        "file_de": "Firstname_Lastname_DataEngg_AI-DE.docx",
        "role_family": "Data Engineer (with AI extension)",
        "research_track": False,
        "specialized_terms": {
            "etl", "elt", "data pipeline", "data pipelines", "data warehouse",
            "airflow", "dbt", "spark", "pyspark", "kafka", "hadoop",
            "snowflake", "bigquery", "redshift", "databricks", "tableau",
            "power bi", "looker",
        },
    },
    "DevOps_Engineer": {
        "file_en": "Firstname_Lastname_DevOps_Engineer.docx",
        "file_de": "Firstname_Lastname_DevOps_Engineer-DE.docx",
        "role_family": "DevOps Engineer",
        "research_track": False,
        "specialized_terms": {
            "ci/cd", "github actions", "gitlab", "jenkins", "ansible",
            "terraform", "docker", "kubernetes", "k8s", "helm",
        },
    },
    "MLOps_Platform_AI": {
        "file_en": "Firstname_Lastname_MLOps_Platform_AI.docx",
        "file_de": "Firstname_Lastname_MLOps_Platform_AI-DE.docx",
        "role_family": "MLOps / AI Platform Engineer",
        "research_track": False,
        "specialized_terms": {
            "mlops", "mlflow", "fine-tuning", "cuda", "agentic",
            "multi-agent", "kubernetes", "k8s", "terraform", "grafana",
            "prometheus",
        },
    },
    "Vision_AI": {
        "file_en": "Firstname_Lastname_Vision_AI.docx",
        "file_de": "Firstname_Lastname_Vision_AI-DE.docx",
        "role_family": "Computer Vision Engineer / Industrial AI",
        "research_track": False,
        "specialized_terms": {
            "computer vision", "opencv", "yolo", "onnx", "tensorrt", "cuda",
            "embedded", "plc", "sensor fusion",
        },
    },
}

_DE_MARKERS = {
    "und", "mit", "für", "der", "die", "das", "ist", "sind", "wir", "sie",
    "ihre", "eine", "einen", "auch", "nicht", "werden", "wird", "sowie",
}
_EN_MARKERS = {
    "and", "with", "for", "the", "is", "are", "we", "you", "your", "will",
    "not", "that", "this", "team",
}


def detect_language(text: str) -> str:
    words = normalize(text).split()
    de_hits = sum(1 for w in words if w in _DE_MARKERS)
    en_hits = sum(1 for w in words if w in _EN_MARKERS)
    return "de" if de_hits > en_hits else "en"


_PHD_PATTERN = re.compile(
    r"\b(phd|ph\.d|doctorate|doktortitel|promotion|first-author|peer-reviewed|"
    r"peer reviewed|publication record|begutachtete publikation)\b"
)


def mentions_research_credential(job_text: str) -> bool:
    return bool(_PHD_PATTERN.search(job_text.lower()))


def compare(job_text: str, lang: str, extra: set[str], exclude: set[str]) -> dict:
    job_search = prepare(job_text)
    job_terms = extract_terms(job_text, extra, exclude)
    job_term_set = {t for t, _ in job_terms}

    results = []
    for key, profile in RESUME_PROFILES.items():
        resume_dir = RESUME_DIR_DE if lang == "de" else RESUME_DIR_EN
        filename = profile["file_de"] if lang == "de" else profile["file_en"]
        resume_path = resume_dir / filename
        if not resume_path.exists():
            results.append({"key": key, "profile": profile, "error": f"not found: {resume_path}"})
            continue

        resume_text = read_text(str(resume_path))
        resume_search = prepare(resume_text)

        matched = [t for t, n in job_terms if contains_term(resume_search, t)]
        overall_pct = round(100 * len(matched) / len(job_terms)) if job_terms else 0

        specialized_hits = sorted(job_term_set & profile["specialized_terms"])
        specialized_asked_but_missing = sorted(
            t for t in profile["specialized_terms"]
            if t in job_term_set and not contains_term(resume_search, t)
        )
        specialized_not_asked = sorted(profile["specialized_terms"] - job_term_set)

        results.append({
            "key": key,
            "profile": profile,
            "overall_pct": overall_pct,
            "specialized_hits": specialized_hits,
            "specialized_asked_but_missing": specialized_asked_but_missing,
            "specialized_not_asked_count": len(specialized_not_asked),
        })

    results.sort(key=lambda r: len(r.get("specialized_hits", [])), reverse=True)
    return {
        "language": lang,
        "research_credential_mentioned": mentions_research_credential(job_text),
        "results": results,
    }


def render(data: dict) -> str:
    lines = [
        "# Resume comparison (deterministic starting point, not a verdict)",
        "",
        f"Detected posting language: {data['language']}",
        f"PhD / first-author-publication language detected: {data['research_credential_mentioned']}",
        "",
        "Ranked by specialized-term overlap (the posting's distinguishing vocabulary",
        "actually present in each resume), NOT by overall keyword-match percentage —",
        "overall percentage is reported for reference only, since shared tools",
        "(Python, Docker, AWS, CI/CD) inflate it almost identically across all eight",
        "variants and are not a role-family signal. See references/matching-methodology.md.",
        "",
    ]
    for r in data["results"]:
        profile = r["profile"]
        lines.append(f"## {r['key']} — {profile['role_family']}")
        if "error" in r:
            lines.append(f"  SKIPPED: {r['error']}")
            lines.append("")
            continue
        lines.append(f"- Specialized-term hits: {len(r['specialized_hits'])} — {', '.join(r['specialized_hits']) or 'none'}")
        if r["specialized_asked_but_missing"]:
            lines.append(f"- Posting asks for these (in this resume's specialty) but they're not in the resume text: {', '.join(r['specialized_asked_but_missing'])}")
        lines.append(f"- Overall keyword overlap (reference only, not diagnostic): {r['overall_pct']}%")
        lines.append("")
    lines += [
        "## Required next step",
        "",
        "This table is a starting point, not the verdict. Read the posting's actual",
        "responsibility language against references/role-family-signals.md before",
        "naming a match — a high specialized-term count still needs the qualitative",
        "check (responsibility verbs, seniority/scope language, contradictory signals,",
        "PhD/publication gate). Never report a bare percentage as the answer.",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--job", required=True, help=".docx, .txt, or .md")
    ap.add_argument("--lang", default="auto", choices=["auto", "en", "de"])
    ap.add_argument("--extra", default="", help="comma-separated extra terms to look for")
    ap.add_argument("--exclude", default="", help="comma-separated company name/location terms to ignore")
    ap.add_argument("--output", help="write Markdown report here instead of stdout")
    args = ap.parse_args()

    job_text = read_text(args.job)
    lang = detect_language(job_text) if args.lang == "auto" else args.lang
    extra = {t.strip().lower() for t in args.extra.split(",") if t.strip()}
    exclude = {normalize(t.strip()) for t in args.exclude.split(",") if t.strip()}

    report = render(compare(job_text, lang, extra, exclude))
    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
        print(f"wrote {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
