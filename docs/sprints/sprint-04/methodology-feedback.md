# Sprint S04 — Methodology feedback

**Sprint:** 4 · **Date:** 2026-04-26 · **Route:** local export only

## Summary

Two observations from S04. The sprint itself ran smoothly (docs-only, lightweight mode, single session). The main methodology signal is about inter-sprint changes that fall outside formal sprint tracking.

## Observations

### Theme 1: Inter-sprint hotfix tracking

| Field | Value |
|-------|-------|
| Observation | The v1 UI rollback (retiring Leopard v2) happened between S03 compound and S04 plan. It was committed (`d76fc09`) and deployed but not tracked by any TASK. The changelog entry in `requirements.md` was only added retroactively during S04 TASK-010. |
| Source | conversation, S04 produce |
| Severity | LOW |
| Proposed improvement | For ad-hoc fixes between sprints, either (a) create a hotfix TASK in the backlog with `sprint: N` and close it immediately, or (b) add a `## Hotfixes` section to the next sprint's `release.md`. This keeps traceability without adding ceremony. |

### Theme 2: Docs-only sprint ergonomics

| Field | Value |
|-------|-------|
| Observation | A sprint with only documentation/process tasks completed plan→reqs→produce→deliver in one session with no friction. The lightweight mode workflow fits well. |
| Source | activity flow, S04 plan-summary |
| Severity | none (positive) |
| Effective practice | Lightweight mode is well-suited for housekeeping sprints. No methodology change needed. |
