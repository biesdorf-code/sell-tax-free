---
gse:
  type: requirement
  sprint: 1
  branch: gse/sprint-01/integration
  elicitation_summary: "Solo investor uploads broker CSV; app shows per-lot Luxembourg 6-month tax-free vs waiting list without ever showing buy prices. CSV stays in memory only."
  traces:
    derives_from: [PLN-001, INT-001]
    decided_by: []
  status: approved
  created: "2026-04-23"
  updated: "2026-04-23"
---

# Requirements — Sprint 1

**Plan:** PLN-001 · **Out of scope this sprint:** FR-005 (bubble timeline) → TASK-004 in pool.

## Functional requirements

### REQ-001 — CSV upload and Market buy parsing

- **Type:** functional
- **Actor:** Solo user in Chrome
- **Capability:** Upload a CSV matching the broker export layout; extract `Market buy` lots using `Time`, `Ticker`, `No. of shares`
- **Rationale:** Foundation for all views; must match `transactions.csv` header contract
- **Priority:** Must
- **Traces:** TASK-001 | FR-001
- **Acceptance criteria:**
  1. **Given** a CSV whose header matches `docs/requirements.md` FR-001 column list, **when** the user uploads it, **then** every row with `Action` = `Market buy` is parsed and invalid rows (missing ticker, time, or non-positive quantity) are rejected with a clear error message.
  2. **Given** a parsed `Market buy` row, **when** any processing or rendering runs, **then** no value from `Price / share`, `Total`, `Result`, `Exchange rate`, or any fee/withholding column appears in the HTML response or browser DOM for that session.
  3. **Given** rows with `Action` other than `Market buy` (e.g. `Deposit`, `Interest on cash`), **when** the file is processed, **then** those rows are ignored for lot construction.

### REQ-002 — Same-day aggregation into lots

- **Type:** functional
- **Actor:** System
- **Capability:** Merge same ticker + same calendar day into one lot (sum shares)
- **Rationale:** FR-002; one lot per (ticker, local calendar day)
- **Priority:** Must
- **Traces:** TASK-002 | FR-002
- **Acceptance criteria:**
  1. **Given** two `Market buy` rows with the same `Ticker` and `Time` on the same local calendar day (date from `Time`), **when** aggregation runs, **then** they become a single lot with quantity = sum of `No. of shares`.
  2. **Given** two `Market buy` rows with the same `Ticker` on **different** calendar days, **when** aggregation runs, **then** two distinct lots remain (FR-002a).

### REQ-003 — Luxembourg six-month classification per lot

- **Type:** functional
- **Actor:** System (user sees outcome in REQ-004)
- **Capability:** Classify each lot as tax-free or waiting using **calendar** six-month math and **system date** as reference
- **Rationale:** FR-003; OQ-003 — reference date = `date.today()` in the server’s timezone (document choice in code)
- **Priority:** Must
- **Traces:** TASK-002 | FR-003
- **Acceptance criteria:**
  1. **Definition:** Let `E = D + 6 calendar months` (same day-of-month rule as `dateutil.relativedelta(months=6)`, with end-of-month clamping if needed). The lot is **tax-free** iff `R > E`; otherwise **waiting** (strict **greater than** six months after the purchase calendar day).
  2. **Given** lot date `D = 2024-05-24` and reference `R = 2024-11-25`, **when** classification runs, **then** the lot is **tax-free**.
  3. **Given** `D = 2024-05-24` and `R = 2024-11-24`, **when** classification runs, **then** the lot is **waiting** (not strictly after six calendar months).
  4. **Given** `D = 2024-01-31` and `R = 2024-07-31`, **when** classification runs, **then** the lot is **waiting**; **given** `R = 2024-08-01`, **then** **tax-free** (illustrates end-of-month handling — align with `relativedelta` behavior in tests).

### REQ-004 — Tax-free / waiting list UI

- **Type:** functional
- **Actor:** Solo user
- **Capability:** See two sections: tax-free lots and waiting lots with time-until-tax-free
- **Rationale:** FR-004
- **Priority:** Must
- **Traces:** TASK-003 | FR-004
- **Acceptance criteria:**
  1. **Given** classified lots, **when** the user opens the list view after upload, **then** they see a **Tax-free** section and a **Waiting** section with no empty misleading labels (sections may show “None” if empty).
  2. **Given** a waiting lot, **when** it is displayed, **then** the UI shows **ticker**, **quantity**, **lot buy date**, and either **days until tax-free** or a clear **eligible on** calendar date (no prices).
  3. **Given** a tax-free lot, **when** it is displayed, **then** the UI shows **ticker**, **quantity**, **lot buy date**, and an explicit **Tax-free** (or equivalent) state — no prices.
  4. **Given** the rendered page, **when** the user searches the visible text or inspects DOM for known CSV price columns, **then** no buy price, total, or fee strings from the upload appear.

### REQ-005 — Living requirements doc sync

- **Type:** functional
- **Actor:** Maintainer / agent
- **Capability:** Keep `docs/requirements.md` aligned with sprint 1 behavior
- **Rationale:** NFR-003 + TASK-005
- **Priority:** Should
- **Traces:** TASK-005
- **Acceptance criteria:**
  1. **Given** sprint 1 delivery merges to integration branch, **when** `docs/requirements.md` is reviewed, **then** it references **REQ-003** six-month calendar rule (or points to this `reqs.md`) so readers know how eligibility is computed.
  2. **Given** any scope change during PRODUCE, **when** the sprint ends, **then** `docs/requirements.md` changelog table has a new row or the open question is recorded.

## Non-functional requirements

### REQ-101 — Privacy (no prices in UI)

- **Type:** non-functional
- **Metric:** Exposure of cost / price fields
- **Target:** Zero price or cost-basis fields in HTTP responses and DOM for upload flows
- **Measurement:** Manual test with sample CSV containing distinctive price values; confirm they never appear in UI or “View source” of dynamic content
- **Priority:** Must
- **Traces:** TASK-001, TASK-003 | NFR-002

### REQ-102 — Ephemeral CSV handling

- **Type:** non-functional
- **Metric:** Persistence of upload payload
- **Target:** No CSV bytes written to disk or DB by the app
- **Measurement:** Code review + manual test: upload, then confirm no new files under app data dir; restart container does not restore prior upload
- **Priority:** Must
- **Traces:** TASK-001 | NFR-004

### REQ-103 — Chrome on same machine

- **Type:** non-functional
- **Metric:** Browser support
- **Target:** Primary support is latest Chrome on the same host as the server (local or container port forward)
- **Measurement:** Smoke test in Chrome only for sprint 1
- **Priority:** Should
- **Traces:** PLN-001 | NFR-001

## Traceability matrix

| Req ID  | Tasks        | FR / NFR   | Status   |
|---------|--------------|------------|----------|
| REQ-001 | TASK-001     | FR-001     | approved |
| REQ-002 | TASK-002     | FR-002     | approved |
| REQ-003 | TASK-002     | FR-003     | approved |
| REQ-004 | TASK-003     | FR-004     | approved |
| REQ-005 | TASK-005     | NFR-003    | approved |
| REQ-101 | TASK-001,003 | NFR-002    | approved |
| REQ-102 | TASK-001     | NFR-004    | approved |
| REQ-103 | TASK-003     | NFR-001    | approved |

## Deferred (Sprint 2+)

- **FR-005** / TASK-004 — Bubble timeline, hover, confetti
- **Docker** / TASK-006, **Deploy** / TASK-007
