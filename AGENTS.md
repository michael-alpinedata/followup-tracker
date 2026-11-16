# AGENTS.md

Follow-up Tracker: FastAPI + SQLAlchemy + PostgreSQL + vanilla HTML/JS. Read this first, then the doc you need.

## Commands
- Run everything: `docker compose up --build` (http://localhost:8000)
- Tests: `python -m pytest -q` (must pass before any commit)
- Dev server: `make dev` (SQLite)

## Architecture in 5 lines
- `app/logic.py`: pure business rules (follow-up due logic). **No I/O here.**
- `app/main.py`: routes + request logging middleware. Time comes from the `today()` dependency (overridable in tests).
- `app/models.py` / `app/schemas.py`: DB model / validation.
- `app/static/index.html`: the whole frontend, calls `/api/*`.
- `tests/`: `test_logic.py` (unit), `test_api.py` (integration).

## Conventions
- Behaviour changes start from a GitHub Issue with acceptance criteria. Commits reference it (`Closes #n`).
- Every behaviour change ships with a test. Business rules go in `logic.py` and get a unit test.
- Never log personal data (names, organizations, notes). Log ids only.
- No new dependency without a reason written in the PR.

## Boundaries
- Never commit secrets; `DATABASE_URL` comes from the environment.
- Do not touch `.github/workflows` or `render.yaml` without human approval.

## Modular docs
- Product behaviour and acceptance criteria → [docs/spec.md](docs/spec.md)
- How work flows (issue → branch → PR → CI → deploy) → [docs/process.md](docs/process.md)
- Agent roles and hand-offs → [docs/agents.md](docs/agents.md)
- Deploy, config, rollback → [docs/deployment.md](docs/deployment.md)
- What is deliberately not done → [docs/limitations.md](docs/limitations.md)
