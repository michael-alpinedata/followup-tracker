# Deployment

Target: **Render** (web service from the Dockerfile) + **Neon** (free managed PostgreSQL).

## First deploy
1. Neon: create a project and copy the connection string (`postgresql://…?sslmode=require`).
2. Render: *New → Blueprint* on this repo (`render.yaml`), or *New → Web Service → Docker*.
3. Set the env var `DATABASE_URL` to the Neon string. Health check path: `/health`.
4. Tables are created at app startup. Open the Render URL and add `/health` to check.
5. Put the public URL in the README.

## Continuous delivery
`render.yaml` sets `autoDeployTrigger: checksPass`: each push to `main` deploys only if the GitHub CI checks pass.

## Rollback
Render dashboard → service → *Events/Deploys* → pick the last good deploy → *Rollback*.
Data is untouched (schema is additive: `create_all` never drops or alters tables).

## Config
| Variable | Meaning |
|---|---|
| `DATABASE_URL` | PostgreSQL URL. Defaults to local SQLite when unset. `postgres://` is accepted and rewritten. |
| `PORT` | Set by Render; defaults to 8000. |

## Known caveat
Render's free tier sleeps after inactivity: the first request can take ~30 s.
