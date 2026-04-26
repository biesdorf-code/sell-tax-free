---
gse:
  type: requirement
  sprint: 4
  branch: main
  elicitation_summary: "S02 housekeeping debt: sync living requirements doc, create TCP template for deploy sprints, close Coolify logs docs task."
  traces:
    derives_from: [PLN-004]
    decided_by: []
  status: approved
  created: "2026-04-26"
  updated: "2026-04-26"
---

# Requirements — Sprint 4

**Plan:** PLN-004 — S02 debt clearance (docs/process only, no code changes).

## REQ-401 — Sync requirements.md with FR-005 and deploy NFRs

- **Type:** functional (documentation)
- **Task:** TASK-010
- **Priority:** Should
- **Acceptance criteria:**
  1. **Given** `docs/requirements.md` FR-005 section, **when** compared to the implemented bubble timeline (REQ-201), **then** it documents: one bubble per lot, vertical stacking for same-day lots, hover payload (ticker, quantity, lot date, days-until / Tax-free), confetti on click, and bubble area scaling.
  2. **Given** `docs/requirements.md` NFR-005 and NFR-006 sections, **when** compared to the actual deploy setup, **then** they reflect: `/deploy` gate behavior, Coolify/Hetzner as v1 target, `docs/deploy/coolify-hetzner.md` reference, and the learner deploy script path.
  3. **Given** the changelog table at the bottom of `requirements.md`, **when** S04 deliver closes, **then** a new row records the sync performed.

## REQ-402 — TCP template for deployment-path sprints

- **Type:** process
- **Task:** TASK-008
- **Priority:** Should
- **Acceptance criteria:**
  1. **Given** S02 shipped Docker/deploy without a TCP, **when** this task completes, **then** a retroactive `docs/sprints/sprint-02/test-reports/TCP-S02.md` exists documenting the test evidence that was actually collected (pytest results, manual checks) in the TCP-001 format.
  2. **Given** S04 itself is a docs-only sprint, **when** deliver closes, **then** a `docs/sprints/sprint-04/test-reports/TCP-S04.md` exists covering REQ-401..403 with pass/fail summary.

## REQ-403 — Coolify deployment logs docs closure

- **Type:** functional (documentation)
- **Task:** TASK-009
- **Priority:** Could
- **Acceptance criteria:**
  1. **Given** `scripts/coolify_fetch_logs.py` exists and is importable from `learner_coolify_deploy.py`, **when** a reviewer reads `docs/deploy/coolify-hetzner.md`, **then** the log-fetching path is documented (env vars, standalone usage command).
  2. **Given** the current state of the repo, **when** checked against TASK-009 acceptance criteria ("repo docs or a script point to a repeatable API-based fetch path"), **then** the task can be closed — or any small gap is filled.

## Approval

| REQ     | Status                |
|---------|-----------------------|
| REQ-401 | Approved (2026-04-26) |
| REQ-402 | Approved (2026-04-26) |
| REQ-403 | Approved (2026-04-26) |
