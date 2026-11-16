# Follow-up Tracker

A small full-stack app that tells a job seeker **who to follow up with today**.

## The problem

During a job search (and any career change), applications and networking contacts pile up. Replies
take weeks, and the real cost is the follow-up you forget to send. A spreadsheet doesn't tell you
what is overdue; it just grows.

## What it does

- Track **applications** and **contacts** (name, organization, status, notes).
- Each entry has a **follow-up interval** (default 7 days).
- The home screen shows **"Due today"**: active entries never contacted, or whose
  `last_contact + interval` is today or past.
- **"Contacted today"** (one click) resets the clock and moves `to_contact` → `waiting`.
- `closed`, `rejected` and `accepted` entries are never due.

Full behaviour and acceptance criteria: [docs/spec.md](docs/spec.md).

## Stack

FastAPI (backend) · SQLAlchemy · PostgreSQL · vanilla HTML/JS frontend served by the API ·
Docker Compose · GitHub Actions · Render + Neon (deployment).

## Run it

```bash
# Full stack (app + Postgres), one command → http://localhost:8000
docker compose up --build

# Tests (unit + integration), one command, no Docker needed
pip install -r requirements-dev.txt && python -m pytest -q

# Local dev with SQLite
make dev
```

## Tests

- `tests/test_logic.py`: **unit** tests of the follow-up rules (pure functions).
- `tests/test_api.py`: **integration** tests: HTTP → FastAPI → SQLAlchemy → database
  (in-memory SQLite in tests, PostgreSQL in Docker/production).

## CI/CD and deployment

- CI (`.github/workflows/ci.yml`): tests + Docker build on every pull request and on `main`.
- CD: Render deploys `main` automatically once checks pass (`render.yaml`).
- Rollback and setup: [docs/deployment.md](docs/deployment.md).
- Live URL: [https://followup-tracker.onrender.com/](https://followup-tracker.onrender.com/)

## Observability

Every request emits one structured JSON log line (`request_id`, method, path, status, duration).
`x-request-id` is echoed in the response. Logs contain ids only, never names, organizations or notes.
Metrics, traces, dashboards and alerting are **not** implemented (see [docs/limitations.md](docs/limitations.md)).

## How it was built

Specified first, then built with an AI coding assistant working in defined roles, with the human
as product owner. See [AGENTS.md](AGENTS.md), [docs/agents.md](docs/agents.md) and
[docs/process.md](docs/process.md). Tasks and acceptance criteria live in the GitHub Issues of this repo.

## Project layout

```
app/        FastAPI app (main.py), rules (logic.py), models, schemas, static/index.html
tests/      unit + integration tests
docs/       spec, process, agent team, deployment, limitations
scripts/    create_issues.sh (creates the public task tracker)
```
