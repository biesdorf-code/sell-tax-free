# Sprint S01 — Release notes

**Sprint:** 1 · **Date:** 2026-04-23 · **Branch:** merged to `main` (integration branch removed)

## Delivered

| Task | Type | Description | Complexity |
|------|------|-------------|------------|
| TASK-001 | requirement | CSV import pipeline; no buy prices in UI | 2 |
| TASK-002 | code | Same-day lots + Luxembourg 6-month classification | 3 |
| TASK-003 | code | Tax-free / waiting list UI | 3 |
| TASK-005 | doc | Requirements doc alignment | 1 |

## Review summary

- Formal `/gse:review` not run (Lightweight). Automated tests + integration tests passed.

## Test summary

- Campaign: [TCP-001](./test-reports/TCP-001.md)
- Tests run: 9 (pytest)
- Passed: 9 · Failed: 0

## How to run

See `docs/requirements.md` — **Sprint 1 implementation (dev)**.

## Next

- Sprint 2 candidates: TASK-004 (bubbles), TASK-006 (Docker), TASK-007 (Hetzner `/gse:deploy`)
- Optional: `/gse:compound` per GSE LC03
