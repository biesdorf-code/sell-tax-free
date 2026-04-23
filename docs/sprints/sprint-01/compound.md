# Sprint S01 — Capitalization

## Patterns

- **Ephemeral uploads + session-only facts:** Parse CSV in memory; store only `{ticker, lot_date, quantity, tax_free, eligible_on, days_until}` in Flask session — keeps REQ-101/102 simple.
- **Flask root paths:** `template_folder` / `static_folder` anchored to repo root avoids `TemplateNotFound` when the package lives under `sell_tax_free/`.
- **Calendar six-month rule:** `dateutil.relativedelta(months=6)` + `R > anniversary` matches REQ-003 examples; unit tests lock edge cases (e.g. Jan 31).

## Lessons learned

- **Lightweight + no formal review:** Delivery relied on pytest + integration tests; acceptable for solo scope, but sprint 2 should keep **TCP-** campaigns when adding UI (bubbles).
- **REQ→TST before deliver:** Sprint 1 deliver needed explicit `test-strategy.md` + `TCP-001`; do the same early in sprint 2 for FR-005.

## Best practices confirmed

- **Test-driven reqs:** REQ-003 acceptance dates translated directly into `test_engine.py` cases.
- **Single integration merge:** All work on one integration branch then merge to `main` matched small-team velocity.

## Technical debt

- **REQ-103:** Chrome smoke still manual — add a note in sprint 2 or accept as Should.
- **FR-005:** One bubble per lot vs per ticker — resolve in sprint 2 REQs before PRODUCE.

## Methodology (Axe 2 — brief)

- First sprint completed plan → reqs → produce → deliver without formal `/gse:review`; methodology friction was low. Consider review for sprint 2 if TASK-007 (deploy) touches secrets.

**Closure:** Proceed to sprint 2 planning (PLN-002).
