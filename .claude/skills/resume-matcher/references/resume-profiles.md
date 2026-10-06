# The eight resume profiles

This file is a **template**: edit it to describe your own resume set. It
names example filenames on purpose, because that's what this skill routes
between. Each resume
exists in English (in `job-resume/EN/`) and German (in `job-resume/DE/`,
`-DE` suffix). Keep this file and `scripts/compare_resumes.py`'s
`RESUME_PROFILES` dict in sync if a resume's content changes.

## AI_LLM — `Firstname_Lastname_AI_LLM.docx`
**Role family**: LLM / Agentic AI Engineer (GenAI).
**Specialized vocabulary**: RAG, LangChain, LangGraph, CrewAI, agentic/
multi-agent systems, prompt engineering, LLM fine-tuning (LoRA/QLoRA),
vector databases, guardrails/hallucination mitigation, LLMOps.
**Seniority signal**: <fill in your own, e.g. years of experience / level>.
**Research track**: No — the resume explicitly targets "production LLM
reliability and evaluation" roles, not a research-scientist track, even if
the history contains a publication.
**Best fit for**: postings centered on integrating LLMs/agents into product
features, RAG pipelines, prompt engineering, LLM evaluation/reliability.

## AI_Research — `Firstname_Lastname_AI_Research.docx`
**Role family**: AI/ML Research Engineer / Research Scientist track.
**Specialized vocabulary**: diffusion models, generative architectures,
reinforcement learning, benchmarking/ablation methodology, competition
participation.
**Research track**: Yes, strongly — lists first-author publications and
explicitly targets "research engineer, applied scientist, and PhD
opportunities." This is the resume for any posting with
a PhD or first-author-publication requirement.
**Best fit for**: postings with explicit research framing, publication
requirements, or research-institution collaboration language.

## Backend_SoftwareEngineer — `Firstname_Lastname_Backend_SoftwareEngineer.docx`
**Role family**: Backend Software Engineer.
**Specialized vocabulary**: C#/.NET backend, API/microservice design,
integration test gates, end-to-end service ownership (API design through
deploy and on-call).
**Research track**: No.
**Best fit for**: postings centered on API/service/schema/database work
with no model-training or data-pipeline ownership as the core ask.

## Cloud_Engineer — `Firstname_Lastname_Cloud_Engineer.docx`
**Role family**: Cloud Engineer / Infrastructure.
**Specialized vocabulary**: Terraform authorship, VNet/subnet/network
security design, Key Vault/secrets architecture, cost optimization as a
named metric, bastion hosts, multi-cloud (Azure + AWS).
**Research track**: No.
**Best fit for**: postings where the cloud environment itself — not an
application running on it — is the accountable artifact.

## DataEngg_AI — `Firstname_Lastname_DataEngg_AI.docx`
**Role family**: Data Engineer, with an AI extension.
**Specialized vocabulary**: ETL/ELT, dimensional modeling (star/snowflake
schema), Airflow/dbt, data warehousing (Snowflake/Redshift), BI dashboards
(Power BI/Tableau), data lineage/quality.
**Research track**: No.
**Best fit for**: postings where data movement/storage/quality is the core
ask, even if AI/ML appears in the title — model-building is a secondary
extension on this resume, not the core.

## DevOps_Engineer — `Firstname_Lastname_DevOps_Engineer.docx`
**Role family**: DevOps Engineer.
**Specialized vocabulary**: CI/CD pipeline authorship across multiple
tools, Ansible automation, disaster-recovery/backup process, release
process discipline (four-eyes sign-off, GitOps, changelogs), shared
on-call rotation as an explicit identity.
**Research track**: No.
**Best fit for**: postings centered on deployment-pipeline ownership and
release process for other teams, not the cloud environment or the model
lifecycle specifically.

## MLOps_Platform_AI — `Firstname_Lastname_MLOps_Platform_AI.docx`
**Role family**: MLOps / AI Platform Engineer.
**Specialized vocabulary**: model registry/experiment tracking (MLflow,
DVC), automated retraining loops, multi-tenant governance (RBAC, Entra
ID), GPU cluster as shared infrastructure for multiple researchers,
feedback-driven retraining.
**Research track**: No.
**Best fit for**: postings centered on the model's production lifecycle —
drift, retraining, versioning — especially where the platform serves
multiple teams rather than one product.

## Vision_AI — `Firstname_Lastname_Vision_AI.docx`
**Role family**: Computer Vision Engineer / Industrial AI.
**Specialized vocabulary**: YOLO and vision-specific models, image
acquisition pipelines (GigE Vision), annotation/active learning (CVAT),
edge inference optimization (TensorRT/ONNX), manufacturing-line/industrial
deployment context.
**Research track**: No (some research-adjacent work may appear in one
role, but the resume overall is framed as applied
industrial AI, not a research track).
**Best fit for**: postings with a specific vision modality and a
manufacturing/industrial/edge deployment context.

## Quick disambiguation table

| If the posting's core ask is... | Route to |
|---|---|
| Integrating LLMs/agents/RAG into product features | AI_LLM |
| Publishing research, PhD required, novel methods | AI_Research |
| API/service/database backend, no model or data-pipeline ownership | Backend_SoftwareEngineer |
| Cloud architecture, IaC, networking, cost | Cloud_Engineer |
| Data pipelines, warehousing, BI, data quality | DataEngg_AI |
| CI/CD and release process for other teams | DevOps_Engineer |
| Model production lifecycle, retraining, multi-team ML platform | MLOps_Platform_AI |
| Vision-specific modality, industrial/manufacturing deployment | Vision_AI |
