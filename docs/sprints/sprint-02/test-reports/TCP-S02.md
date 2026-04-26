---
gse:
  id: TCP-S02
  type: test-campaign
  sprint: 2
  branch: main
  traces:
    implements:
      - REQ-201
      - REQ-202
      - REQ-203
    derives_from: [TASK-004, TASK-006, TASK-007]
  created: "2026-04-26"
  note: "Retroactive TCP produced by TASK-008 (S04) — S02 shipped without a formal campaign file."
---

# Test campaign TCP-S02 — Sprint 2 (retroactive)

## Summary

- Executed: 12 tests (7 engine, 5 integration) at S02 deliver
- Passed: 12 (100%)
- Failed: 0
- Command: `python -m pytest tests/ -v`
- Verified at deliver: 2026-04-23
- **Note:** This TCP was not produced at S02 deliver time. It is reconstructed from activity notes and pytest output during S04 (TASK-008) to close the documentation gap flagged in S02 compound.

## Requirements coverage

| REQ ID  | Tests / evidence                  | Status |
|---------|-----------------------------------|--------|
| REQ-201 | `test_bubble_timeline_one_row_per_lot_same_day_two_tickers` + upload integration tests | pass |
| REQ-202 | Dockerfile builds, `docker run -p 8080:8080` serves on `/` | pass (manual) |
| REQ-203 | `test_deploy_gate_and_not_now`, `test_deploy_yes_shows_coolify_steps` | pass |

## Test inventory at S02 deliver

| # | Test | REQs |
|---|------|------|
| 1 | `test_same_day_merge` | REQ-002 |
| 2 | `test_different_days_separate_lots` | REQ-002 |
| 3 | `test_tax_free_classification` | REQ-003 |
| 4 | `test_waiting_classification` | REQ-003 |
| 5 | `test_non_market_buy_excluded` | REQ-001 |
| 6 | `test_missing_fields` | REQ-001 |
| 7 | `test_empty_csv` | REQ-001 |
| 8 | `test_upload_shows_sections_without_price_in_html` | REQ-004, REQ-101 |
| 9 | `test_bubble_timeline_one_row_per_lot_same_day_two_tickers` | REQ-201 |
| 10 | `test_deploy_gate_and_not_now` | REQ-203 |
| 11 | `test_deploy_yes_shows_coolify_steps` | REQ-203 |
| 12 | `test_upload_uses_session_not_filesystem` | REQ-102 |

## Notes

- Container verification (REQ-202) was manual: `docker build` + `docker run` + browser check.
- No load testing or security testing performed (out of scope for lightweight mode).
