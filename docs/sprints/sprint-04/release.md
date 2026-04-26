---
gse:
  id: REL-004
  type: release
  sprint: 4
  status: done
  created: "2026-04-26"
  traces:
    derives_from: [PLN-004, TASK-008, TASK-009, TASK-010]
---

# Sprint 4 — Release notes

**Goal:** Clear S02 housekeeping debt (documentation and process only — no code changes).

## Delivered

| TASK | Type | Description | Pts |
|------|------|-------------|-----|
| TASK-010 | requirement | Synced `docs/requirements.md` with FR-005 bubble timeline details and deploy NFR-005/006 updates | 1 |
| TASK-008 | process | Retroactive `TCP-S02.md` (12-test campaign) + `TCP-S04.md` at deliver | 1 |
| TASK-009 | docs | Verified Coolify logs script and docs are complete — no changes needed | 1 |

**Budget:** 3/3 pts consumed.

## Changes

- **`docs/requirements.md`**: Added sprint 3+4 REQ links; NFR-005 now references `scripts/learner_coolify_deploy.py` and post-deploy log streaming; NFR-006 clarifies Coolify as the orchestration platform on Hetzner; two changelog entries added (S03 UI sprint, S04 sync).
- **`docs/sprints/sprint-02/test-reports/TCP-S02.md`**: New file — retroactive test campaign for S02, reconstructed from activity notes and pytest inventory (12 tests, 100% pass).
- **`docs/sprints/sprint-04/test-reports/TCP-S04.md`**: New file — S04 test campaign (15 tests, 100% pass, artefact-inspection coverage for REQ-401..403).

## Test evidence

- `python -m pytest -q` → **15 passed** (no regressions)
- TCP-S04: REQ-401..403 verified by artefact inspection

## No code changes

This sprint touched only documentation and process artefacts. No application code, templates, stylesheets, or tests were modified.
