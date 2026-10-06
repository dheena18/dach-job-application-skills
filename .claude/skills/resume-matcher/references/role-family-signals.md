# Telling the eight role families apart

This file is the classification logic: what distinguishes each role family
in a posting's actual language, independent of title and independent of
shared tools. Read this after running `scripts/compare_resumes.py`, before
naming a verdict.

## Why title doesn't work here

A labor-economics study (Indeed Hiring Lab, Gimbel & Sinclair) measured
~33% title-level mismatch even against a curated, large-scale normalized
title taxonomy. "AI Engineer" and "ML Engineer" specifically are documented
across multiple independent industry sources as umbrella terms applied
inconsistently — the same title can mean LLM-application work, model-
training work, or research work depending entirely on the company. A
posting titled "AI Engineer" or "ML Engineer" should trigger mandatory
responsibility-text disambiguation, never title-based routing.

## The verb-to-family mapping

Built on the same logic O*NET itself uses to construct its occupational
taxonomy: classify by generalizing from the actual task verbs used, never
from the job title. A posting's responsibility clauses, mapped:

| Verbs / phrases in the posting | Points toward |
|---|---|
| research, publish, investigate, propose novel, advance state of the art, peer-reviewed | **AI_Research** |
| operate, maintain, monitor, respond to incidents, on-call, SLO/SLA | Production/ops family (DevOps, Cloud, MLOps — disambiguate further below) |
| design pipelines, ensure data quality, lineage, warehouse, ingest, ETL/ELT | **DataEngg_AI** |
| train models, deploy models, monitor drift, retrain, feature store, model registry | **MLOps_Platform_AI** |
| integrate LLM, RAG, prompt, agent, evaluate model outputs, orchestrate agents, hallucination | **AI_LLM** |
| API, service, schema, endpoint — with no model/data-pipeline language | **Backend_SoftwareEngineer** |
| image/video pipeline, annotation, inference optimization for a specific modality, manufacturing/industrial line | **Vision_AI** |
| cloud architecture, IaC, multi-account/region, cost optimization, network design | **Cloud_Engineer** |
| CI/CD pipeline ownership, release process, deployment automation for other teams | **DevOps_Engineer** |

## Disambiguating inside the production/ops cluster

DevOps, Cloud Engineer, and MLOps/AI Platform Engineer share enormous tool
overlap (Docker, Kubernetes, Terraform) and are the hardest trio to tell
apart. The distinguishing question is **what's the primary accountable
artifact**, not which tools are listed:

- **DevOps_Engineer**: the CI/CD pipeline and deployment automation that
  lets *any* software team ship repeatedly and safely. Failure mode =
  broken build/release process.
- **Cloud_Engineer**: the cloud infrastructure itself — provisioning, IAM,
  networking, multi-account/region architecture, cost. Often
  provider-specific (an AWS/Azure cert requirement is a real signal here
  specifically).
- **MLOps_Platform_AI**: the model lifecycle in production — the things
  with no analog in plain DevOps: feature stores, model/data versioning,
  training-serving skew, drift detection, automated retraining. One clean
  test: a DevOps engineer deploys a service that runs identically forever;
  an MLOps engineer deploys a model that degrades the moment real-world
  data shifts. A posting mentioning drift, retraining triggers, or
  experiment tracking as a named responsibility is MLOps, not DevOps, even
  if the tool list looks identical.
- Org placement is a secondary tell: reporting into Platform/Infra
  leadership and building reusable infrastructure for multiple teams skews
  MLOps_Platform_AI; embedded in one product team doing that team's CI/CD
  skews DevOps_Engineer.

## Data Engineer vs. AI/LLM Engineer vs. ML Engineer

- **DataEngg_AI**: owns data movement/storage/quality, full stop. A
  posting that talks about SQL/ETL/warehouse/lineage/data-quality
  monitoring but never mentions model training, evaluation, or serving is
  a Data Engineer role even if "AI" or "ML" appears in the title or stack
  list. Data engineers are explicitly *not* model builders — this is a
  well-supported, checkable tell.
- **MLOps_Platform_AI**: owns the model's production lifecycle — training
  infra, serving, versioning, monitoring. Accountable for the *model's*
  reliability, not the data's.
- **AI_LLM**: owns integration of existing/pretrained models into product
  features — RAG, prompt engineering, agent orchestration, LLM API glue.
  Explicitly *not* training infrastructure and *not* data pipelines. A
  useful framing: data engineers build the highway system, AI/LLM
  engineers build the vehicles that drive on it. If a posting never
  mentions fine-tuning/training infrastructure and centers on "integrating
  LLM APIs," "RAG," "agents," "evaluating model outputs," "prompt
  iteration" — that's AI_LLM, not MLOps_Platform_AI.

## Backend_SoftwareEngineer vs. AI_LLM

Both ship backend services. The differentiator is how much of the role
owns **non-deterministic failure modes** that don't exist in plain backend
work: handling LLM call retries, streaming responses, output-quality
evaluation, hallucination handling, prompt/context versioning. A posting
that never mentions evaluating model-output quality or handling
non-deterministic behavior, and centers on API/service/schema/database
work, is Backend_SoftwareEngineer even if an LLM API appears somewhere in
the stack list.

## Vision_AI

The modality is the tell: image/video ingestion, annotation workflows,
augmentation, accuracy on vision-specific benchmarks, edge/real-time
inference optimization, and — distinctively for this resume — a
manufacturing/industrial deployment context (PCB inspection, defect
detection, a physical production line). A posting about vision work with
no modality-specific pipeline language and no industrial/edge-deployment
context may fit AI_LLM or MLOps_Platform_AI better depending on what it's
actually asking the person to own.

## Research vs. applied: the cleanest axis, use it deliberately

This is the best-evidenced distinction in the whole classification scheme.

- **The PhD/first-author-publication requirement is the strongest single
  checkable field**, more reliable than title. Per a recognized ML-hiring
  reference (Chip Huyen's *ML Interviews Book*): "the research scientist
  role typically requires a PhD and/or first-author papers at top-tier
  conferences, while the research engineer role doesn't." Frontier labs
  increasingly post combined "Research Scientist / Research Engineer"
  reqs with the real differentiation happening at interview stage, not in
  the posting — when you see this combined framing, the credential
  requirement is still the deciding field to check, not the title string.
- Research-track language clusters: "design and conduct experiments,"
  "publish findings," "peer-reviewed," "secure research funding,"
  "collaborate with academic institutions," "novel architectures," "state
  of the art."
- Production-track language clusters: "on-call," "SLA/SLO," "incident
  response," "runbooks," "post-incident review," "ship," "customer-facing."
- These two clusters essentially never co-occur legitimately in one
  posting. A posting mentioning both "on-call rotation" and "publish at
  NeurIPS" is a genuine anomaly — flag it for manual review rather than
  picking one (see `matching-methodology.md` on contradictory signals).

## Seniority/scope, as a separate axis from role family

Three tiers, from established job-leveling/scope taxonomies used in real
compensation/HR practice:

1. **Task execution**: assist, compile, deliver, maintain, support.
2. **Management/oversight**: delegate, direct, lead, manage, supervise.
3. **Strategic leadership**: advance, align, drive, formulate.

A posting whose role family matches a resume well but whose scope language
sits clearly in tier 2 or 3, when the resume's actual experience sits in
tier 1, is a seniority mismatch — a different verdict than a role-family
mismatch. Name it as such rather than folding it into a generic "needs
tailoring."

## Common misclassification traps

- **Title inflation**: titles get upgraded without responsibility or
  comp keeping pace. Don't infer seniority or role family from
  "Senior"/"Lead" in the title alone.
- **"AI Engineer" / "ML Engineer" as umbrella titles**: treat these titles
  as a trigger for mandatory responsibility-text disambiguation, never as
  self-sufficient routing signal.
- **DevOps-titled-but-actually-sysadmin, Cloud-titled-but-actually-
  networking**: when a "DevOps" or "Cloud" posting's actual responsibility
  text reads as narrow infrastructure maintenance with no deployment-
  pipeline or application-delivery language, don't assume the title's
  family is correct — re-derive from the verbs.
