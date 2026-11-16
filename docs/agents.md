# Agent team

One AI coding assistant plays four roles in separate phases, each with a narrow brief. The human is
the product owner and the only one who merges and deploys.

| Role | Responsibility | Inputs | Output | Must not |
|---|---|---|---|---|
| **Spec writer** | Turns an idea into issues with testable acceptance criteria | Product owner's goal | Issues, `docs/spec.md` | Write code |
| **Builder** | Implements one issue | Issue + `AGENTS.md` | Code on a feature branch | Change CI or deploy config; skip tests |
| **Tester** | Writes/extends unit and integration tests from the acceptance criteria | Issue + code | Tests; failing-case list | Weaken a test to make it pass |
| **Reviewer** | Reads the diff against the criteria, the conventions and the "no personal data in logs" rule | PR diff | Review comments | Merge |

## Hand-offs
Spec writer → (issue) → Builder ⇄ Tester (until green) → (PR) → Reviewer → Product owner merges.

## Context
Every role starts from `AGENTS.md`, which points to the modular docs in `docs/`.

## Honest note
In this project the roles were played by one assistant (Claude) in successive prompts, not by
autonomous parallel agents. The separation exists to keep each step reviewable.
