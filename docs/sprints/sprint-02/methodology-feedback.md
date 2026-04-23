# Sprint S02 — Methodology feedback

**Summary:** Lightweight sprint 2 delivered scope efficiently but skipped some formal sprint artefacts. Container deployment surfaced platform-specific health-check and routing details worth folding into future checklists or upstream GSE deploy guidance.

---

## Theme A — Documentation and review hygiene

| Observation | Source | Severity |
|-------------|--------|----------|
| `docs/sprints/sprint-02/` lacks `review.md`, `release.md`, and `plan-summary.md` while S01 had richer artefacts. | COMPOUND scan vs S01 layout | MEDIUM |
| COMPOUND had to rely on `plan.yaml`, `reqs.md`, and backlog notes instead of a closed review record. | Process | LOW |

**Friction:** Harder to trace review findings or release notes per sprint without consistent files.

**Improvement proposal:** For each sprint, either (1) generate the usual sprint docs during `/gse:deliver`, or (2) explicitly mark the plan as “docs-light” and store a one-paragraph summary in `compound.md` at deliver time.

---

## Theme B — Container and PaaS integration

| Observation | Source | Severity |
|-------------|--------|----------|
| Coolify health check failed until `curl` existed in the image; logs showed `curl: not found`. | Session / deployment debugging | HIGH |
| Traefik/Coolify needed FQDN with `:8080` for correct routing in learner setup. | Session | MEDIUM |
| API-based deploy + log fetch scripts helped when interactive `gse-one` paths were not available. | Session | LOW |

**Effective practices:** Single Dockerfile for local + prod; `/deploy` gate; operator doc without secrets.

**Improvement proposal:** Extend deploy preflight templates (or docs) with: “If health check uses HTTP GET, ensure `curl` or `wget` in image or disable check.” Optionally document “published port in FQDN” for Traefik edge cases.

---

_Shareable as-is for manual feedback to GSE-One or internal retro._
