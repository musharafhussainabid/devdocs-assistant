# Engineering Notes

> One paragraph per working day. What I built, what I had to figure out, what's next.
> Append-only. The rough edges stay — they're the record of how the system was actually built.

---

## 2026-04-16 — Phase 0.1 & 0.2 — Repository Bootstrap & Docker Stack

**Built:** Initialized the `devdocs-assistant` repository on GitHub. Set up `main` and `develop` branches, configured branch protection ruleset on `main` (require PR, block force pushes, require linear history, restrict deletions). Added README, ROADMAP, LICENSE, .gitignore, and this engineering log. Then built the Docker Compose stack — PostgreSQL 16 with pgvector 0.8.2, pgAdmin 4, and Redis 7. All three services running and verified healthy.

**Figured out:** GitHub rulesets don't enforce on private repos with free accounts — had to make the repo public first. The `pgvector/pgvector:pg16` image ships pgvector pre-compiled so no manual build needed. pgAdmin's latest version now validates emails strictly — `admin@devdocs.local` was rejected because `.local` isn't a real TLD, switched to `admin@devdocs.dev`. Docker Compose `version` key is now obsolete and throws a warning — removed it. Existing Docker containers from other projects don't conflict as long as port mappings are different — changed Postgres to 5433 and Redis to 6380 to avoid clashes.

**Next:** Python project setup and stack verification script.

---

## 2026-04-17 — Phase 0.3 & 0.4 — Python Tooling & Verification Script

**Built:** Set up the Python project with uv as the package manager. Configured pyproject.toml with psycopg3 and python-dotenv as core dependencies, ruff + sqlfluff + pre-commit + pytest as dev dependencies. Installed pre-commit hooks that run automatically on every commit — trailing whitespace, end-of-file fixer, YAML/JSON validation, large file blocker, ruff linting/formatting, and SQL linting. Then wrote `scripts/verify.py` — a health-check script that tests Postgres connectivity, confirms pgvector extension, runs a vector similarity search with cosine distance, and pings Redis. Tagged `v0.0-bootstrap`.

**Figured out:** Windows sometimes strips the leading dot from `.pre-commit-config.yaml` — had to create the file via terminal. First pre-commit run auto-fixed trailing whitespace and missing newlines in existing files, which is expected — hooks modify files and abort the commit so you re-add and commit again. Root `.env` needs port numbers matching the Docker Compose config (5433/6380 not the defaults) — got a connection timeout before fixing this. The `<=>` operator is pgvector's cosine distance — used it in verify.py to prove similarity search works with 3D test vectors. Never merge into `main` locally — always use GitHub PRs. The branch protection ruleset blocks local pushes that contain merge commits.

**Next:** Phase 1 — PostgreSQL foundations. Data types, DDL, DML, joins, aggregations, and the Document Library mini-project.

---
