# Product specification

## User
One job seeker managing their own applications and contacts. No accounts, single-user, by design for v1.

## Entities
`Entry`: `kind` (application | contact), `name`, `organization`, `status`, `last_contact` (date, nullable),
`followup_days` (1..365, default 7), `notes`.

Statuses: `to_contact`, `waiting`, `interview` (active); `closed`, `rejected`, `accepted` (closed).

## Rules
1. `next_followup = last_contact + followup_days`; `None` if never contacted.
2. An entry is **due** if its status is active AND (never contacted OR `next_followup <= today`).
3. Closed entries are never due.
4. "Contacted today" sets `last_contact = today`; `to_contact` becomes `waiting`.

## API
| Method | Path | Behaviour |
|---|---|---|
| GET | `/health` | 200 `{"status":"ok"}` if the DB answers |
| GET | `/api/entries?due_only=` | list with `next_followup` and `due` |
| POST | `/api/entries` | create, 201; 422 on invalid input |
| PUT | `/api/entries/{id}` | full update; 404 if unknown |
| POST | `/api/entries/{id}/contacted` | rule 4; 404 if unknown |
| DELETE | `/api/entries/{id}` | 204; 404 if unknown |

## Acceptance criteria
Tracked as GitHub Issues (created by `scripts/create_issues.sh`), each with its own criteria.
They map one-to-one to tests in `tests/`.

## Out of scope (v1)
Authentication, multi-user, email/push reminders, import/export.
