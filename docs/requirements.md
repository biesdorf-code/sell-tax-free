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

- A lot is **tax-free to sell** if it has been held **> 6 months** from its **lot acquisition date** to the **reference date** (**system date** — `date.today()`; no user-configurable as-of date).
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

- The app is packaged as a **single Docker container** (Python-based). No external services (database, cache, broker) are required; everything runs inside one image.
- The container exposes an HTTP port and is started locally (e.g. `docker run -p 8080:8080 sell-tax-free`).
- The user accesses the app in **Google Chrome** on the **same machine** running the container.
- No `docker-compose` is required for v1 (single container, no orchestration needed).

### NFR-004 — CSV handling (ephemeral)

- Uploaded CSV files are processed **in-memory per request** and **never persisted** to disk or any storage layer inside the container.
- No persistent volume is mounted; the container is fully ephemeral — restarting it loses no data because it stores none.

### NFR-005 — Production deployment gate

- After local testing is validated by the user, a **deployment gate** is presented: "Deploy to production? (yes / not now)".
- If yes, deployment follows **NFR-006** (v1 default: **Hetzner**). The **`/gse:deploy`** command is used when the project is ready for that step (after a working container and user sign-off).
- If not now, the app continues to run locally; the gate can be re-triggered at any time.

### NFR-006 — Production target options

- **Chosen for v1 — Hetzner VPS:** Docker on Linux; deployment exercised via **`/gse:deploy`** in this project. Fixed monthly cost (~€5–20/mo for a CX21/CX31). AWS remains documented below as a deferred alternative.
- **Deferred — AWS:** see "AWS deployment advice" section below if the target changes later.
- Both paths use the **same container image**; no app code changes are required between local and production.

### NFR-002 — Privacy

- **Buy prices** must **never** be shown in the UI (see FR-001).

### NFR-003 — Documentation

- This **living requirements** file is **maintained** as specs evolve (changelog via git history; optional dated “Changes” section below).

---

## AWS deployment advice

For a **single Python container with no database**, the options ranked by simplicity:

| Option | Effort | Cost | Notes |
|--------|--------|------|-------|
| **AWS App Runner** | Lowest | ~$5–15/mo (+ idle) | Point at an ECR image; handles HTTPS, scaling, zero infrastructure. Best fit for this project. |
| **ECS Fargate** | Low-medium | Similar to App Runner | More control (VPC, IAM, task definitions); overkill for a personal app but standard in teams. |
| **EC2 + Docker** | Medium | ~$5–15/mo (t3.micro) | Closest to Hetzner; you manage the OS and Docker yourself. Familiar if you already know VPS ops. |
| **Elastic Beanstalk** | Medium | Similar to EC2 | Older managed platform; Docker support exists but adds abstraction that rarely helps solo projects. |

**Recommendation for this project:** **AWS App Runner** is the easiest path:
1. Build and push the image to **Amazon ECR** (Elastic Container Registry) — one `docker push`.
2. Create an **App Runner service** pointing at that ECR image — done in the AWS console or one CLI command.
3. App Runner handles the HTTPS URL, restarts, and (optional) auto-scaling.
4. No servers, no SSH, no Nginx config.

**Hetzner vs AWS trade-off:**
- Hetzner is **cheaper and simpler** if you are comfortable with SSH and Linux. A CX21 (2 vCPU, 4 GB, €4.51/mo) runs Docker fine.
- AWS App Runner is **zero-ops** but has a per-vCPU/memory pricing model that can surprise you if you forget to pause it.
- For a **personal portfolio tool** used infrequently, Hetzner is probably the better default; AWS App Runner is a good choice if you want to practice AWS deployments (aligned with your learning goals).

---

## Changes (optional log)

| Date       | Summary |
|------------|---------|
| 2026-04-23 | Initial capture from intent INT-001. |
| 2026-04-23 | OQ-002 resolved: lots defined by buy date; same ticker, multiple lots; six months per lot (FR-002a). |
| 2026-04-23 | OQ-001 resolved: CSV columns locked from transactions.csv; used fields: Action, Time, Ticker, No. of shares. |
| 2026-04-23 | OQ-003 resolved: reference date is always system date. |
| 2026-04-23 | OQ-004 resolved: hover shows Ticker, quantity, lot buy date, days until tax-free — no price data. |
| 2026-04-23 | NFR-001 updated: platform is now a single Docker container (Python); accessed via Chrome on the same machine. |
| 2026-04-23 | NFR-004 added: CSV is ephemeral (in-memory per request, never persisted). |
| 2026-04-23 | NFR-005/006 added: post-testing production deployment gate; targets are Hetzner VPS or AWS App Runner. |
| 2026-04-23 | NFR-006: production target for v1 locked to **Hetzner**; `/gse:deploy` at delivery gate; AWS deferred. |
