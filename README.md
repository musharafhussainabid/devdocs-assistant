# devdocs-assistant

> A multi-tenant RAG product for searching open-source software documentation.
> Built on **PostgreSQL + pgvector** with a hybrid retrieval pipeline, served via **FastAPI + NVIDIA Triton**.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![PostgreSQL 16](https://img.shields.io/badge/postgres-16-336791.svg?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![pgvector](https://img.shields.io/badge/pgvector-0.8+-success.svg)](https://github.com/pgvector/pgvector)
[![Last Commit](https://img.shields.io/github/last-commit/musharafhussainabid/devdocs-assistant.svg)](https://github.com/musharafhussainabid/devdocs-assistant/commits/main)

## What This Is

A working repository of production patterns for PostgreSQL + pgvector in RAG systems. Built incrementally against a [structured roadmap](./ROADMAP.md), with every concept implemented in code and every milestone tagged as a release. Daily engineering notes live in [`LEARNING_LOG.md`](./LEARNING_LOG.md).

The end product — **DevDocs Assistant** — answers technical questions over open-source documentation (FastAPI, PostgreSQL, LangChain, Docker, React, and more). Each tenant is a workspace with its own selected doc collections, isolated via row-level security and served through a hybrid retrieval pipeline (semantic + full-text + structured filters + reranking).

## Stack

| Layer | Technology |
|---|---|
| Database | PostgreSQL 16 + pgvector 0.8+ |
| Embeddings  | `BAAI/bge-small-en-v1.5` (INT8-quantized via ONNX) |
| Reranker | `BAAI/bge-reranker-v2-m3` |
| Inference serving | NVIDIA Triton (CPU/GPU, ONNX Runtime backend) |
| Orchestration | LangChain |
| API | FastAPI |
| Cache | Redis |
| Migrations | Alembic |
| Containerization | Docker Compose |
| Deployment | Self-hosted (primary) + Supabase (alternative) |

## Repository Structure

```
devdocs-assistant/
├── README.md
├── ROADMAP.md              # the engineering plan
├── LEARNING_LOG.md         # daily engineering notes
├── docker/                 # docker-compose for the local stack
├── docs/                   # concept notes & blog drafts
├── scripts/                # reusable utilities
├── phase-01-foundations/
├── phase-02-advanced-sql/
├── phase-03-reliability/
├── phase-04-pgvector/
├── phase-05-ai-integration/
├── phase-06-production/
└── capstone/               # the deployed DevDocs Assistant
```

## Progress

- [ ] **Phase 0** — Bootstrap (`v0.0-bootstrap`)
- [ ] **Phase 1** — PostgreSQL Foundations (`v0.1-foundations`)
- [ ] **Phase 2** — Advanced SQL & Performance (`v0.2-advanced-sql`)
- [ ] **Phase 3** — Reliability & Schema Design for AI (`v0.3-reliability`)
- [ ] **Phase 4** — pgvector & Hybrid Retrieval (`v0.4-pgvector`)
- [ ] **Phase 5** — AI Integration Layer (`v0.5-ai-integration`)
- [ ] **Phase 6** — Production Concerns (`v0.6-production`)
- [ ] **Phase 7** — Capstone: DevDocs Assistant (`v1.0-capstone`)

## Branching Model

- `main` — protected, stable, only updated at phase completions via PR from `develop`
- `develop` — integration branch
- `feature/phase-N-<topic>` — working branches

All commits follow [Conventional Commits](https://www.conventionalcommits.org/): `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`.

## Quickstart

_The local stack will be runnable after Phase 0.2._

```bash
# Coming after Phase 0.2:
# docker compose up -d
# python scripts/verify.py
```

## Engineering Notes (Medium series)

Articles published alongside the build:

- _"Why Postgres + pgvector for production RAG in 2026"_ — _coming after Phase 4_
- _"Hybrid search in pure SQL: combining vector, full-text, and filters"_ — _coming after Phase 4_
- _"Choosing a chunking strategy: an empirical comparison"_ — _coming after Phase 5_
- _"From notebook to production: operating a RAG system on a budget"_ — _coming after Phase 6_
- _"DevDocs Assistant: building a multi-tenant RAG product end-to-end"_ — _coming after Phase 7_

## License

[MIT](./LICENSE)
