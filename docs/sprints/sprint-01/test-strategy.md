---
gse:
  type: test
  sprint: 1
  branch: gse/sprint-01/integration
  traces:
    derives_from: [PLN-001]
    implements: []
    decided_by: []
  status: approved
  created: "2026-04-23"
  updated: "2026-04-23"
---

# Test strategy — Sprint 1

## Test strategy

- **Domain:** web
- **Pyramid target:** Unit 85% / Integration 15% / E2E 0% / Policy 0% (Lightweight sprint 1)
- **Framework:** pytest + Flask `test_client`

## Unit tests

### TST-001 — Same-day aggregation sums quantity

- **level:** unit
- **Implements:** REQ-002
- **Maps to:** `tests/test_engine.py::test_aggregate_same_day`

### TST-002 — Different days stay separate lots

- **level:** unit
- **Implements:** REQ-002
- **Maps to:** `tests/test_engine.py::test_aggregate_different_days`

### TST-003 — Classification May 2024 example

- **level:** unit
- **Implements:** REQ-003
- **Maps to:** `tests/test_engine.py::test_classify_req003_may24`

### TST-004 — Classification Jan 31 end-of-month

- **level:** unit
- **Implements:** REQ-003
- **Maps to:** `tests/test_engine.py::test_classify_req003_jan31`

### TST-005 — Deposits ignored; Market buy parsed

- **level:** unit
- **Implements:** REQ-001, REQ-001 (criterion 3)
- **Maps to:** `tests/test_engine.py::test_parse_ignores_deposit`

### TST-006 — Missing columns rejected

- **level:** unit
- **Implements:** REQ-001
- **Maps to:** `tests/test_engine.py::test_parse_rejects_bad_header`

### TST-007 — Price column not in classified output

- **level:** unit
- **Implements:** REQ-001 (privacy), REQ-101
- **Maps to:** `tests/test_engine.py::test_build_never_exposes_price_in_output`

## Integration tests

### TST-010 — Upload CSV; results page has no price leak

- **level:** integration
- **Implements:** REQ-001, REQ-004 (sections + fields), REQ-101
- **Maps to:** `tests/test_app.py::test_upload_shows_sections_without_price_in_html`

### TST-011 — Ephemeral session path (no server-side file write)

- **level:** integration
- **Implements:** REQ-102
- **Maps to:** `tests/test_app.py::test_upload_uses_session_not_filesystem`

## Manual / deferred

- **REQ-103** (Chrome smoke): Should priority — manual this sprint.
- **REQ-102** full disk audit: partial via TST-011; full manual per REQ measurement.
- **REQ-005**: documentation — verified at deliver.
