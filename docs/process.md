# Working process

```
Issue (acceptance criteria) → branch → agent builds + tests → PR → CI green → merge → auto-deploy
```

1. **Specify first.** A feature starts as a GitHub Issue with acceptance criteria (see `docs/spec.md`).
2. **Branch** `feat/<issue-number>-<slug>`.
3. **Test first when the rule is pure.** New rule → unit test in `tests/test_logic.py`, then code in `app/logic.py`.
   New endpoint → integration test in `tests/test_api.py`.
4. **Pull request** references the issue (`Closes #n`). CI runs the tests and builds the Docker image.
5. **Human review** by the product owner before merge. Agents never merge their own PR.
6. **Deploy.** Render deploys `main` automatically once CI checks pass.
7. **Rollback.** Redeploy the previous successful deploy from the Render dashboard (see `docs/deployment.md`).

## Definition of done
Acceptance criteria met · tests added and green · docs updated if behaviour changed · no personal data in logs.
