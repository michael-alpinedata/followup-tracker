.PHONY: up test dev
up:      ## full stack (app + Postgres) in Docker
	docker compose up --build
test:    ## unit + integration tests (in-memory SQLite, no Docker needed)
	python -m pytest -q
dev:     ## local run with SQLite
	uvicorn app.main:app --reload
