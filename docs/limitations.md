# Limitations (deliberate)

Scope was kept small on purpose. Not implemented:

- **Observability beyond logs**: no metrics, traces or dashboard. Logs are structured and carry a request id.
- **Alerting on user impact**: none. A natural first alert: error rate on `POST /api/entries/{id}/contacted`.
- **On-call agent**: none.
- **Separate dev/prod environments** with manual promotion: single environment.
- **Auth / multi-user**: none; do not expose personal data publicly without adding it.
- **Schema migrations**: `create_all` only (additive). Alembic would be the next step.
