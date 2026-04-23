# Sell Tax Free — Living requirements

This file is the **working specification** for the product. Update it whenever scope or behavior changes. Formal traceability to implementation lives in sprint `reqs.md` under Lightweight workflow; this document stays readable for humans first.

**Intent:** [INT-001](./intent.md)

---

## Functional requirements

### FR-001 — CSV import

- The user can **upload a CSV** whose structure matches the **project sample** (see Open Questions in intent until the sample is pinned).
- **Buy prices** (or any field that reveals cost basis) **must not appear** anywhere in the UI.

### FR-002 — Same-day / same-ticker aggregation

- Rows with the **same ticker** and the **same calendar day** are **combined into one entry** for display and logic, even when underlying buys differ in price or quantity.

### FR-003 — Luxembourg six-month rule

- A position is **tax-free to sell** if it has been held **> 6 months** relative to the **reference date** (default: **today**; confirm in REQS if “as of” date is user-configurable).
- Positions **not** past the threshold appear in the **waiting** bucket with **visibility of time until** they become tax-free.

### FR-004 — View: Tax-free / waiting list

- **Section A:** holdings that are **already tax-free** under the rule.
- **Section B:** holdings **still waiting**, each with a **timeline** (or equivalent) showing **how long until** tax-free eligibility.

### FR-005 — View: Shared bubble timeline

- **One** timeline showing **all tickers** as **bubbles**.
- **Bubble area** (or diameter) is **proportional to share count**.
- **Hover:** show **ticker details** (exact fields TBD in REQS; **no buy price**).
- **Click:** trigger a **confetti** animation.

---

## Non-functional requirements

### NFR-001 — Platform

- **Local Python web app**, used in **Google Chrome** on the **same machine** as the server.

### NFR-002 — Privacy

- **Buy prices** must **never** be shown in the UI (see FR-001).

### NFR-003 — Documentation

- This **living requirements** file is **maintained** as specs evolve (changelog via git history; optional dated “Changes” section below).

---

## Changes (optional log)

| Date       | Summary |
|------------|---------|
| 2026-04-23 | Initial capture from intent INT-001. |
