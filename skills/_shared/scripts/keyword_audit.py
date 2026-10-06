#!/usr/bin/env python3
"""Compare a resume against a job posting and list matched and missing terms.

Adapted from the job-application-kit reference skill's keyword_audit.py,
made docx-aware (the original only read .txt/.md). python-docx plus
simplemma (a small, pure-Python, zero-heavy-dependency lemmatizer covering
German and English) — no spaCy/NLTK/embedding models. The output is a
starting point for a human decision, not a score to optimise. A term in
the "missing" list should only be added to the resume if the candidate
actually has that experience — see skills/resume-tailor/references/fit-and-keywords.md for how
to sort missing terms into "true but forgotten" / "true but worded
differently" / "not true", and for why ~75-85% is the target, not 100%.

Usage:
    python keyword_audit.py --resume resume.docx --job posting.txt
    python keyword_audit.py --resume resume.docx --job posting.txt --output audit.md
    python keyword_audit.py --resume resume.docx --job posting.txt --extra "ros2,gazebo"
    python keyword_audit.py --resume resume.docx --job posting.txt --exclude "Acme Corp,Berlin"
"""
from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path

STOPWORDS = {
    # english
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "has", "have",
    "in", "into", "is", "it", "of", "on", "or", "our", "that", "the", "their",
    "this", "to", "we", "with", "you", "your", "will", "work", "working", "role",
    "team", "teams", "candidate", "candidates", "experience", "skills", "ability",
    "strong", "using", "use", "used", "responsibilities", "requirements",
    "preferred", "must", "nice", "plus", "including", "across", "within", "about",
    "help", "support", "years", "year", "who", "what", "how", "also", "other",
    "such", "like", "new", "well", "good", "great", "join", "looking", "ideally",
    "etc", "all", "any", "can", "more", "than", "not", "but", "they", "them",
    "company", "job", "position", "offer", "benefits", "apply", "application",
    # generic filler that repeats often in postings but names no skill —
    # found by hand after two rounds of real audits kept surfacing these as
    # "missing" noise. Company/location names are NOT handled here (they
    # vary per posting) — pass --exclude for those instead.
    "remote", "professional", "modern", "knowledge", "scalable", "comparable",
    "develop", "develops", "developing",
    # german
    "und", "oder", "der", "die", "das", "ein", "eine", "einen", "einer", "mit",
    "für", "von", "bei", "im", "in", "zu", "zur", "zum", "auf", "aus", "wir",
    "sie", "ihre", "ihr", "uns", "unser", "unsere", "sowie", "als", "auch",
    "sind", "ist", "haben", "hast", "bringst", "bringen", "bieten", "suchen",
    "aufgaben", "profil", "anforderungen", "wünschenswert", "vorteil",
    "kenntnisse", "erfahrung", "jahre", "gute", "sehr", "idealerweise",
    "sowohl", "über", "nach", "durch", "werden", "wird", "dich", "dein", "deine",
    "vergleichbare", "vergleichbarer", "technischen", "technischer",
    "praktische", "praktischer", "praktischen", "digitale", "digitalen",
}

# Terms that matter and that plain tokenising would miss or split.
KNOWN_TERMS = {
    # languages
    "python", "java", "c++", "c#", "go", "golang", "rust", "typescript",
    "javascript", "sql", "r", "scala", "kotlin", "swift", "matlab", "bash",
    # ml / ai
    "machine learning", "deep learning", "pytorch", "tensorflow", "keras",
    "scikit-learn", "sklearn", "hugging face", "transformers", "llm", "llms",
    "large language models", "rag", "retrieval-augmented generation", "nlp",
    "natural language processing", "computer vision", "opencv", "yolo",
    "reinforcement learning", "mlops", "mlflow", "langchain", "llamaindex",
    "langgraph", "crewai", "autogen", "semantic kernel", "neo4j", "graph database",
    "vector database", "vector search", "embeddings", "fine-tuning", "lora", "qlora",
    "prompt engineering", "xgboost", "lightgbm", "onnx", "tensorrt", "cuda",
    "diffusion", "gans", "bayesian optimization", "gaussian process",
    "agentic", "agent systems", "multi-agent", "tool calling", "function calling",
    "guardrails", "eval", "evaluation", "llm-as-judge", "a/b testing",
    "semantic search", "hybrid search", "ranking", "reranking",
    # data
    "spark", "pyspark", "airflow", "dbt", "kafka", "hadoop", "snowflake",
    "bigquery", "redshift", "databricks", "pandas", "numpy", "postgresql",
    "postgres", "mysql", "mongodb", "redis", "elasticsearch", "etl", "elt",
    "data pipeline", "data pipelines", "data warehouse", "tableau", "power bi",
    "looker", "excel", "statistics", "forecasting",
    # infra
    "docker", "kubernetes", "k8s", "terraform", "ansible", "helm", "aws",
    "azure", "gcp", "google cloud", "linux", "ci/cd", "github actions",
    "gitlab", "jenkins", "git", "proxmox", "vmware", "grafana", "prometheus",
    "rest", "rest api", "graphql", "grpc", "fastapi", "flask", "django",
    "spring boot", "react", "node", "node.js", "microservices", "pydantic",
    # robotics / embedded
    "ros", "ros2", "gazebo", "slam", "lidar", "embedded", "plc", "can bus",
    "simulink", "robotics", "autonomous driving", "sensor fusion",
    # methods / roles
    "agile", "scrum", "kanban", "jira", "confluence", "tdd", "code review",
    "system design", "architecture", "stakeholder management",
    "project management", "product management", "leadership", "mentoring",
    "cross-functional", "communication", "presentation", "documentation",
    "publications", "peer-reviewed", "phd", "master", "bachelor",
    "ownership", "backend", "api design",
    # certs
    "pmp", "aws certified", "cka", "ckad", "itil", "six sigma",
    # languages (spoken)
    "german", "english", "deutsch", "englisch", "french", "spanish",
    "b1", "b2", "c1", "c2", "verhandlungssicher", "fließend",
}

# Generic role-nouns that regularly stand in for each other after the same
# specific technical qualifier ("RAG solutions" / "RAG systems" / "RAG
# pipelines" are the same real thing). Only applied when a 2-word extracted
# term's second word is one of these — narrow enough to not misfire on
# unrelated bigrams. This is a documented, standard pre-embedding technique
# (manually maintained synonym tables); the tradeoff is the same as
# SYNONYMS below — accurate but needs updating as new cases turn up.
GENERIC_NOUN_GROUP = {
    "solution", "solutions", "system", "systems", "pipeline", "pipelines",
    "platform", "platforms", "tool", "tools", "application", "applications",
    "framework", "frameworks", "service", "services",
}

# Compound-vs-two-words spelling variants for terms that get written
# inconsistently across resumes and postings. A resume that genuinely has
# "MongoDB" shouldn't be marked as missing it just because a posting wrote
# "Mongo DB" (or vice versa) — that's a spelling difference, not a real gap.
# Checked symmetrically (job text and resume text both get every variant
# tried), so it doesn't matter which side chose which spelling. Add to this
# list as new mismatches turn up; it's a curated map, not a generic fuzzy
# matcher, so it never introduces a false match on unrelated terms.
SYNONYMS = {
    "mongodb": ["mongo db"],
    "postgresql": ["postgres sql"],
    "javascript": ["java script"],
    "typescript": ["type script"],
    "tensorflow": ["tensor flow"],
    "graphql": ["graph ql"],
    "github": ["git hub"],
    "gitlab": ["git lab"],
    "devops": ["dev ops"],
    "mlops": ["ml ops"],
    "llmops": ["llm ops"],
    "openai": ["open ai"],
    "backend": ["back end", "back-end"],
    "frontend": ["front end", "front-end"],
    "fullstack": ["full stack", "full-stack"],
    "microservice": ["micro service"],
    "microservices": ["micro services"],
    "database": ["data base"],
    "dataset": ["data set"],
    "workflow": ["work flow"],
    "framework": ["frame work"],
    "codebase": ["code base"],
    "node.js": ["nodejs", "node js"],
    "llm": ["llms"],
    "large language models": ["large language model"],
}


def _bidirectional(synonyms: dict) -> dict:
    """SYNONYMS is written as canonical -> [variants], but KNOWN_TERMS
    sometimes lists both a term and its own variant separately (e.g. both
    "llm" and "llms" are their own KNOWN_TERMS entries) — so a one-directional
    map misses the case where the variant is the one being looked up. Build
    both directions once at import time rather than requiring every entry to
    be duplicated by hand in both directions."""
    combined: dict[str, set[str]] = {}
    for key, variants in synonyms.items():
        combined.setdefault(key, set()).update(variants)
        for v in variants:
            combined.setdefault(v, set()).add(key)
    return combined


_SYNONYMS_BIDIRECTIONAL = _bidirectional(SYNONYMS)


def normalize(text: str) -> str:
    text = text.lower().replace("&", " and ")
    text = re.sub(r"[^a-z0-9äöüß+#./\-\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def lemmatize_text(text_norm: str) -> str:
    """Lemmatize each alphabetic token (English or German, auto-tried in
    that order) and return them space-joined. Used to build a second search
    surface alongside the literal text, so "systems"/"System" and similar
    inflected forms match a term written in its base form without needing
    every grammatical variant hand-declared. Domain jargon/acronyms (LLM,
    RAG) generally aren't in the lemmatizer's dictionary and pass through
    unchanged — those are handled by the explicit SYNONYMS entries instead.
    Fails soft (returns "") if simplemma isn't installed, since this is an
    accuracy improvement, not a hard requirement for the script to run."""
    try:
        import simplemma
    except ImportError:
        return ""
    out = []
    for tok in text_norm.split():
        if tok.isalpha() and len(tok) > 2:
            try:
                out.append(simplemma.lemmatize(tok, lang=("en", "de")).lower())
            except Exception:
                pass
    return " ".join(out)


def prepare(text: str) -> str:
    """The literal normalized text plus its lemmatized form appended. Every
    matching function searches this combined string, so a term matches
    whether the source used the exact inflection or not, while every
    existing literal match still works unchanged (this only adds a second
    chance to match, never removes the first)."""
    norm = normalize(text)
    lemma = lemmatize_text(norm)
    return f"{norm} {lemma}" if lemma else norm


def _word_match(text_norm: str, term_norm: str) -> bool:
    if any(ch in term_norm for ch in "+#/.-"):
        return term_norm in text_norm
    return re.search(rf"(?<![a-z0-9äöüß]){re.escape(term_norm)}(?![a-z0-9äöüß])", text_norm) is not None


def contains_term(text_norm: str, term: str) -> bool:
    term_norm = normalize(term)
    if not term_norm:
        return False
    if _word_match(text_norm, term_norm):
        return True
    # A bare technology name ("React") should also match its common "JS"-suffixed
    # spelling ("ReactJS") — a spelling variant, not a real gap.
    if _word_match(text_norm, term_norm + "js"):
        return True
    for variant in _SYNONYMS_BIDIRECTIONAL.get(term_norm, []):
        if _word_match(text_norm, normalize(variant)):
            return True
    words = term_norm.split()
    if len(words) == 2 and words[1] in GENERIC_NOUN_GROUP:
        for noun in GENERIC_NOUN_GROUP:
            if noun != words[1] and _word_match(text_norm, f"{words[0]} {noun}"):
                return True
    return False


def _is_excluded(term_norm: str, exclude_norms: set[str]) -> bool:
    return any(ex and (ex in term_norm or term_norm in ex) for ex in exclude_norms)


def tokens(text: str) -> list[str]:
    out = []
    for tok in normalize(text).split():
        tok = tok.strip(".,;:()[]{}")
        if len(tok) >= 3 and tok not in STOPWORDS and not tok.isdigit():
            out.append(tok)
    return out


def bigrams(words: list[str]) -> list[str]:
    return [f"{a} {b}" for a, b in zip(words, words[1:])]


def _word_count(text_norm: str, term_norm: str) -> int:
    if any(ch in term_norm for ch in "+#/.-"):
        return text_norm.count(term_norm)
    return len(re.findall(rf"(?<![a-z0-9äöüß]){re.escape(term_norm)}(?![a-z0-9äöüß])", text_norm))


def count_term(text_norm: str, term: str) -> int:
    """Word-boundary-aware occurrence count, including spelling variants (see
    SYNONYMS and the "JS"-suffix rule in contains_term). Do not use
    str.count() for the base case — it does substring counting, which
    silently breaks for short terms (a single-letter term like the language
    "R" would count every literal letter "r" anywhere in the text, wildly
    overcounting)."""
    term_norm = normalize(term)
    if not term_norm:
        return 0
    total = _word_count(text_norm, term_norm)
    total += _word_count(text_norm, term_norm + "js")
    for variant in _SYNONYMS_BIDIRECTIONAL.get(term_norm, []):
        total += _word_count(text_norm, normalize(variant))
    return total


def extract_terms(job_text: str, extra: set[str], exclude: set[str], max_terms: int = 60) -> list[tuple[str, int]]:
    job_search = prepare(job_text)
    found: Counter[str] = Counter()

    for term in KNOWN_TERMS | extra:
        if _is_excluded(term, exclude):
            continue
        if contains_term(job_search, term):
            found[term] += count_term(job_search, term)

    words = tokens(job_text)
    for w, n in Counter(words).most_common():
        if n >= 2 and len(w) > 3 and w not in found and not _is_excluded(w, exclude):
            found[w] = n
    for bg, n in Counter(bigrams(words)).most_common():
        if n >= 2 and bg not in found and not _is_excluded(bg, exclude):
            found[bg] = n

    return found.most_common(max_terms)


def audit(resume_text: str, job_text: str, extra: set[str], exclude: set[str] | None = None) -> dict[str, list]:
    resume_search = prepare(resume_text)
    terms = extract_terms(job_text, extra, exclude or set())
    matched, missing = [], []
    for term, n in terms:
        (matched if contains_term(resume_search, term) else missing).append((term, n))
    return {"matched": matched, "missing": missing}


def render(result: dict[str, list], resume_path: str, job_path: str) -> str:
    matched, missing = result["matched"], result["missing"]
    total = len(matched) + len(missing)
    pct = round(100 * len(matched) / total) if total else 0
    lines = [
        "# Keyword audit",
        "",
        f"Resume: {resume_path}",
        f"Posting: {job_path}",
        f"Terms found in posting: {total}. Present in resume: {len(matched)} ({pct} percent).",
        "",
        "This is a word overlap, not a fit score. Add a missing term only if it is true.",
        f"Target ~75-85%, the range career-advice tools that publish guidance actually",
        "recommend — not 100%. See skills/resume-tailor/references/avoiding-ai-tailored-tells.md.",
        "",
        "## Matched",
        "",
    ]
    lines += [f"- {t} (x{n} in posting)" for t, n in matched] or ["- none"]
    lines += ["", "## Missing from resume", ""]
    lines += [f"- {t} (x{n} in posting)" for t, n in missing] or ["- none"]
    lines += [
        "",
        "## Next step",
        "",
        "Sort the missing list into: true but forgotten (add with context), true but",
        "worded differently (reword), not true (leave out, address in the letter if it matters).",
        "If a company name or location is showing up here, rerun with --exclude.",
    ]
    return "\n".join(lines) + "\n"


def read_text(path: str) -> str:
    p = Path(path)
    if p.suffix.lower() == ".docx":
        import docx
        d = docx.Document(str(p))
        return "\n".join(para.text for para in d.paragraphs)
    return p.read_text(encoding="utf-8", errors="ignore")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--resume", required=True, help=".docx, .txt, or .md")
    ap.add_argument("--job", required=True, help=".docx, .txt, or .md")
    ap.add_argument("--output", help="write Markdown report here instead of stdout")
    ap.add_argument("--extra", default="", help="comma-separated extra terms to look for")
    ap.add_argument("--exclude", default="", help="comma-separated company name/location terms to never treat as a missing keyword")
    args = ap.parse_args()

    resume_text = read_text(args.resume)
    job_text = read_text(args.job)
    extra = {t.strip().lower() for t in args.extra.split(",") if t.strip()}
    exclude = {normalize(t.strip()) for t in args.exclude.split(",") if t.strip()}

    report = render(audit(resume_text, job_text, extra, exclude), args.resume, args.job)
    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
        print(f"wrote {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
