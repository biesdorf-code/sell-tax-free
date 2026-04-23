# Sell Tax Free — Living requirements

This file is the **working specification** for the product. Update it whenever scope or behavior changes. Formal traceability to implementation lives in sprint `reqs.md` under Lightweight workflow; this document stays readable for humans first.

**Intent:** [INT-001](./intent.md)

---

## Functional requirements

### FR-001 — CSV import

- The user can **upload a CSV** with the column layout from `transactions.csv`:
  `Action`, `Time`, `ISIN`, `Ticker`, `Name`, `Notes`, `ID`, `No. of shares`, `Price / share`, `Currency (Price / share)`, `Exchange rate`, `Result`, `Currency (Result)`, `Total`, `Currency (Total)`, `Withholding tax`, `Currency (Withholding tax)`, `Transaction fee`, `Currency conversion fee`, `Currency (Currency conversion fee)`, `Currency (Transaction fee)`.
- **Relevant rows:** only rows where `Action` is `Market buy` are processed as holdings.
- **Fields used:** `Time` (→ lot date), `Ticker`, `No. of shares`.
- **Fields excluded from UI (privacy):** `Price / share`, `Total`, `Result`, `Exchange rate`, and all currency/fee columns.

### FR-002 — Same-day / same-ticker aggregation

- Rows with the **same ticker** and the **same calendar day** are **combined into one lot** (single quantity for that ticker on that day), even when underlying buys differ in price or quantity.

### FR-002a — Lots across days (per-ticker)

- A **lot**’s identity is its **acquisition date** after FR-002: each **(ticker, calendar day)** is one lot.
- The **same ticker** may have **multiple lots** (one per day on which a buy occurred). Lots **do not** merge across days.
- **Six-month eligibility** (FR-003) is computed **per lot**, from that lot’s date to the **reference date** — not once per ticker across all lots.

### FR-003 — Luxembourg six-month rule

- A lot is **tax-free to sell** if it has been held **> 6 months** from its **lot acquisition date** to the **reference date** (default: **today**; confirm in REQS if “as of” date is user-configurable — OQ-003).
- Lots **not** past the threshold appear in the **waiting** bucket with **visibility of time until** they become tax-free.

### FR-004 — View: Tax-free / waiting list

- **Section A:** holdings that are **already tax-free** under the rule.
- **Section B:** holdings **still waiting**, each with a **timeline** (or equivalent) showing **how long until** tax-free eligibility.

### FR-005 — View: Shared bubble timeline

- **One** timeline showing holdings as **bubbles** (how **multiple lots for one ticker** are represented — e.g. one bubble per lot vs aggregated — **TBD in REQS**).
- **Bubble area** (or diameter) is **proportional to share count** for the unit each bubble represents.
- **Hover:** show **Ticker**, **quantity (No. of shares)**, **lot buy date**, **days until tax-free** (or "Tax-free" if already eligible). No buy price or cost basis.
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
| 2026-04-23 | OQ-002 resolved: lots defined by buy date; same ticker, multiple lots; six months per lot (FR-002a). |
| 2026-04-23 | OQ-001 resolved: CSV columns locked from transactions.csv; used fields: Action, Time, Ticker, No. of shares. |
| 2026-04-23 | OQ-003 resolved: reference date is always system date. |
| 2026-04-23 | OQ-004 resolved: hover shows Ticker, quantity, lot buy date, days until tax-free — no price data. |
