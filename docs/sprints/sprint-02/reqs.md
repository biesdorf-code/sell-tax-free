# Sprint S02 — Requirements (lightweight)

**Plan:** PLN-002 — Docker (TASK-006), bubble timeline (TASK-004), deploy gate later (TASK-007).

**Living spec:** [requirements.md](../../requirements.md)

---

## REQ-201 — FR-005: one bubble per lot

- **Decision:** Each **lot** (after FR-002 same-day merge) is **exactly one bubble**. Same ticker on **different** calendar days → **multiple** bubbles. Same calendar day, **multiple** tickers → multiple bubbles at the same horizontal position, **stacked vertically**.
- **Size:** Bubble **area** scales with **quantity** (implementation: radius ∝ √quantity vs max quantity on the chart).
- **Hover:** Ticker, quantity, lot buy date, days until tax-free or “Tax-free”. **No** price or cost fields.
- **Click:** Confetti animation (client-side; `canvas-confetti` from CDN).

## REQ-202 — TASK-006: container

- Single image runs Flask on **0.0.0.0:8080**; `docker run -p 8080:8080 …` matches NFR-001.

---

## Approval

| REQ    | Status     |
|--------|------------|
| REQ-201 | Approved (2026-04-23) |
| REQ-202 | Approved (2026-04-23) |
