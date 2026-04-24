# Sprint S03 — Release notes

**Plan:** PLN-003 · **Mode:** lightweight · **Date:** 2026-04-24

## Delivered

| Task | Type | Description | Complexity |
|------|------|-------------|------------|
| TASK-011 | code | Website UI v1 baseline (`website-v1` tag + `style-v1-baseline.css`) and Leopard/Aqua v2 theme (templates + `style.css`, brushed metal) | 2 |

## Summary

- **v1 preserved:** annotated Git tag **`website-v1`** on pre–UI-v2 commit; archived stylesheet under `static/style-v1-baseline.css`; restore notes in `ui-v1-restore.md`.
- **v2 shipped on `main`:** Aqua title bars, brushed aluminum panels, glossy controls, `theme-leopard` shell; footer labels **Interface v2** / Leopard–Aqua (2007).
- **Follow-up commit:** stronger brushed-metal layering on chrome (post–initial v2 drop).

## Tests

- **pytest:** 15 passed (`tests/test_app.py`, `tests/test_engine.py`).
- **REQ traceability:** `test_req301_*`, `test_req302_*`, `test_req304_*` cover S03 reqs alongside existing TST-010/011 behaviour.

## Review

- Formal `/gse:review` artefact not run for this lightweight sprint; no RVW log.

## Next

- **`/gse:compound`** then **`/gse:integrate`** to close the lifecycle.
- Pool: **TASK-008..010** (S02 debt) remain open for a future sprint.
