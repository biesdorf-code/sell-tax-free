---
id: INT-001
artefact_type: intent
title: "Sell Tax Free — Project Intent"
sprint: 0
status: approved
created: "2026-04-23"
author: pair
traces:
  derives_from: []
---

# Sell Tax Free — Project Intent

## Description (verbatim user statement)

> **Functional Requirements**
>
> **Input:** User uploads a CSV file (same structure as the provided sample — do not show buy prices anywhere in the UI).
>
> **Data rule:** Group transactions of the same ticker on the same day into one entry (even if bought at different prices/quantities).
>
> **Two views:**
>
> 1. **Tax-Free / Waiting list** — Two clear sections: stocks already tax-free to sell, and stocks still in the waiting period showing a timeline of how long until they become tax-free.
> 2. **Shared bubble timeline** — One timeline with all tickers as bubbles. Bubble size proportional to share count. Hovering shows ticker details; clicking triggers a confetti animation.
>
> **Business rule:** Under Luxembourg tax law, stocks held **>6 months** from today are exempt from capital gains tax; those held <=6 months are not.
>
> **Non-Functional Requirements**
>
> - **Platform:** Local Python webapp, accessible via Chrome on the same machine.
> - **Privacy:** Buy prices must never appear in the UI.
> - **Documentation:** Maintain a living requirements file updated as specs evolve.

## Reformulated understanding

- You want a **local Python web app** (used in **Chrome** on the same computer) where you **upload a CSV** of trades. The file format matches a **sample** you have in mind; **purchase prices must never be shown** in the interface (privacy).
- **Aggregation:** rows that share the same **ticker** and the same **calendar day** are **merged into one lot** (one combined quantity for that day), even when buys had different prices or sizes.
- **Lots:** a **lot** is defined by acquisition after that merge: **each calendar day** (per ticker) is its own lot. The **same ticker** can therefore have **many lots** when there were buys on **different days**. The **>6 months** rule is evaluated **per lot**, from that lot's **buy date** to the **reference date** (system date).
- **Tax rule (Luxembourg):** each lot is **tax-free to sell** when it has been held **longer than six months** from its lot date to the reference date; otherwise that lot is **waiting** until the threshold.
- **View 1 — Tax-free / waiting:** two clear areas: what is already **tax-free**, and what is **still waiting**, each with a **timeline** of **time until tax-free** where applicable.
- **View 2 — Bubble timeline:** a **single timeline** with **all tickers** as **bubbles**; **bubble size reflects share count**; **hover** shows allowed details; **click** plays a **confetti** animation.
- **Specs:** keep a **living requirements** document that evolves with the product (see `docs/requirements.md`).

## Users

Single investor using the app **solo** on their **own machine** (no shared accounts or multi-user product scope for now).

## Boundaries (explicit out-of-scope)

- **Not tax or legal advice** — the app applies a stated rule (>6 months) for planning / visualization only; you remain responsible for compliance and professional advice where needed.
- **No buy price in the UI** — any price fields in CSV are input-only for logic if needed; they must not be rendered.
- **Browser scope** — Chrome on the same machine is the target for v1; other browsers are not required.
- **Deployment** — local app only; no requirement to host a public server or sync data to the cloud as part of v1.

## Open Questions

- **OQ-001** — What is the **exact CSV column layout** (and where is the sample file in the repo or attached)? Without it we cannot lock parsers or tests.
  - resolves_in: REQS
  - impact: scope-shaping
  - status: resolved
  - raised_at: INT-001
  - resolution: "Column order from transactions.csv header: Action, Time, ISIN, Ticker, Name, Notes, ID, No. of shares, Price / share, Currency (Price / share), Exchange rate, Result, Currency (Result), Total, Currency (Total), Withholding tax, Currency (Withholding tax), Transaction fee, Currency conversion fee, Currency (Currency conversion fee), Currency (Transaction fee). Fields used by the app: Action (filter to Market buy), Time (lot date), Ticker, No. of shares. Fields explicitly excluded from UI: Price / share, Total, Result, Exchange rate, all currency and fee fields. Recorded 2026-04-23."

- **OQ-002** — After **grouping same ticker + same day**, how do we compute "held since" for the six-month rule when multiple days of buys exist?
  - resolves_in: REQS
  - impact: behavioral
  - status: resolved
  - raised_at: INT-001
  - resolution: "Buy date defines the lot. After same-day aggregation, each (ticker, calendar day) lot keeps that day as its acquisition date. The same ticker has separate lots for different buy days; six months is computed independently per lot from that date. Recorded 2026-04-23."

- **OQ-003** — Should today always be the system date, or should the user pick an as-of date (e.g. for planning)?
  - resolves_in: REQS
  - impact: behavioral
  - status: resolved
  - raised_at: INT-001
  - resolution: "Reference date is always the system date (date.today()). No user-configurable as-of date required. Recorded 2026-04-23."

- **OQ-004** — On hover in the bubble view, which details are allowed while still excluding any buy price or cost basis?
  - resolves_in: REQS
  - impact: cosmetic
  - status: resolved
  - raised_at: INT-001
  - resolution: "Hover payload: Ticker, quantity (No. of shares), lot buy date, days until tax-free (or Tax-free if already eligible). No price, cost basis, or fee data. Recorded 2026-04-23."
