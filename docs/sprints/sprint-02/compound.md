# Sprint S02 — Capitalization

**Plan:** PLN-002 · **Mode:** lightweight · **Budget:** 7/7 pts consumed

Sources: `docs/sprints/sprint-02/reqs.md`, `.gse/plan.yaml`, `.gse/backlog.yaml`, `.gse/status.yaml` activity notes. Formal `review.md` / `release.md` / `plan-summary.md` for S02 were not present in-repo (lightweight path); process lesson captured below.

## Patterns

- **One bubble per lot on a shared time axis:** REQ-201 locks layout (stack same-day different tickers vertically; radius ∝ √quantity vs chart max) — reduces ambiguity before UI work.
- **Production-shaped container early:** `PORT` + Gunicorn in Dockerfile matches Coolify/Hetzner expectations; same image works locally with `docker run -p 8080:8080`.
- **Deploy gate in-app:** `/deploy` defers production until the user explicitly confirms; operator steps and secrets stay out of git (`docs/deploy/coolify-hetzner.md`).
- **Learner Coolify API script:** When full `gse-one` tooling is absent, a small script can set FQDN (including Traefik load-balancer port) and trigger redeploy via Coolify API — repeatable without dashboard clicking.

## Lessons learned

- **PaaS health checks vs slim images:** Coolify’s HTTP health check runs `curl`/`wget` *inside* the container. `python:*-slim` may omit both → failing health check even when Gunicorn is fine. **Prevention:** install `curl` (or `wget`) in the image, or disable/adjust the health check in Coolify.
- **Traefik / published port:** If the app listens on 8080 and the edge expects that port in the URL, the configured FQDN may need `:8080` so routing matches the load-balancer port. Document per environment.
- **Sprint artefact gap:** S02 shipped without archived `review.md`, `release.md`, or `plan-summary.md` under `docs/sprints/sprint-02/`. **Prevention:** run `/gse:review` and `/gse:deliver` artefact steps next sprint, or accept explicit “docs-light” risk in plan.

## Best practices confirmed

- **Reqs before bubbles:** REQ-201/202/203 approved in `reqs.md` before PRODUCE avoided rework on bubble semantics.
- **Pytest for new UI:** REQ-201 covered by tests (bubble HTML + upload path) alongside existing suite (12/12 noted in status).
- **No secrets in repo:** `.env` gitignored; deployment docs reference env vars only.

## Technical debt

- **Formal TCP for S02:** No `test-reports/TCP-*` campaign file for sprint 2 like S01’s TCP-001 — consider a short TCP when adding deployment paths.
- **Runtime log ergonomics:** Optional follow-up: document or commit `scripts/coolify_fetch_logs.py` (API-based deployment logs) next to `learner_coolify_deploy.py`.
- **requirements.md sync:** Confirm `docs/requirements.md` fully reflects FR-005 / NFR deploy entries post-merge (TASK-005 pattern).

## Methodology (Axe 2)

- **Observations collected:** 4 (artefact gap, health check + slim image, Traefik port/FQDN, API scripting).
- **Themes:** 2 — (1) **documentation & review hygiene**, (2) **container/PaaS integration sharp edges**.
- **Route:** Local export only → `docs/sprints/sprint-02/methodology-feedback.md` (`github.upstream_repo` not configured; ticket proposals omitted).
- **Workflow ledger:** No `workflow_observations[]` entries for sprint 2 in `.gse/status.yaml` — nothing to condense.

## Competency (Axe 3)

- **Practiced:** Docker packaging, Gunicorn, environment-based `PORT`, first production path via Coolify, reading deployment logs.
- **LEARN ideas (optional):** “Health checks in container platforms”, “Traefik labels and published ports”, “Minimal attack surface for small web apps”.

## Integration (2026-04-24)

- **Axe 1:** `review.custom_checks` in `.gse/config.yaml`; technical debt → `TASK-008`–`TASK-010` in `.gse/backlog.yaml` (pool).
- **Axe 2:** No `.gse/compound-tickets-draft.yaml` (local export only per above; no upstream GitHub routing).
- **Axe 3:** `docs/learning/deployments-and-containers.md`; `profile.yaml` learning goals + competency map updated.
