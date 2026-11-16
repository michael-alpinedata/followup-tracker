#!/usr/bin/env bash
# Creates the public task tracker (GitHub Issues) with acceptance criteria.
# Usage: gh auth login && ./scripts/create_issues.sh   (run from the repo root)
set -euo pipefail

issue() { gh issue create --title "$1" --body "$2" --label "${3:-feature}" >/dev/null && echo "created: $1"; }
gh label create feature --color 0ea5e9 --force >/dev/null
gh label create infra --color 8b5cf6 --force >/dev/null
gh label create docs --color 64748b --force >/dev/null

issue "Add an entry (application or contact)" "As a job seeker I add an application or a contact so that I can track it.

**Acceptance criteria**
- POST /api/entries creates an entry and returns 201 with an id
- name is required; status and kind are validated (422 otherwise); followup_days is 1..365
- The entry is still there after an app restart (stored in the database)
- The web form adds an entry and the list refreshes"

issue "List entries and show only the ones due for follow-up" "As a job seeker I see what needs a follow-up today so that nothing slips.

**Acceptance criteria**
- GET /api/entries returns every entry with next_followup and due
- GET /api/entries?due_only=true returns only due entries
- Never contacted + active status => due; last_contact + followup_days <= today => due
- closed, rejected and accepted entries are never due
- The UI has a 'Due today' tab (default) and an 'All' tab"

issue "One-click 'Contacted today'" "As a job seeker I mark an entry as followed up in one click.

**Acceptance criteria**
- POST /api/entries/{id}/contacted sets last_contact to today
- status 'to_contact' becomes 'waiting'; other statuses are unchanged
- The entry leaves the 'Due today' list; unknown id => 404"

issue "Edit and delete an entry" "**Acceptance criteria**
- PUT /api/entries/{id} updates all fields with the same validation as creation
- DELETE /api/entries/{id} returns 204 and the entry is gone
- Unknown id => 404 for both"

issue "Structured logs with a request id" "**Acceptance criteria**
- Every request emits one JSON log line: request_id, method, path, status, ms
- x-request-id is reused when sent, generated otherwise, and returned in the response
- Logs contain entry ids only, never names, organizations or notes (personal data)" infra

issue "Docker Compose: whole stack in one command" "**Acceptance criteria**
- 'docker compose up --build' starts Postgres + the app
- The app waits for a healthy database; GET /health returns 200
- Data survives 'docker compose restart'" infra

issue "CI on every pull request" "**Acceptance criteria**
- GitHub Actions runs unit + integration tests on every PR and on main
- The Docker image build is checked
- A failing test makes the check red" infra

issue "Deploy to Render + Neon with a rollback path" "**Acceptance criteria**
- Public URL serves the UI and /health
- Deploys happen automatically from main once CI is green
- Rollback documented in docs/deployment.md (redeploy previous Render deploy)" infra

issue "Project docs: README, AGENTS.md, process, agent team" "**Acceptance criteria**
- README states the problem, behaviour, run/test/deploy commands
- AGENTS.md points to modular docs in docs/
- The agent team and its working process are described" docs
