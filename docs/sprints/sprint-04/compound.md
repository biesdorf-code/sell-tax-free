# Sprint S04 — Capitalization

**Plan:** PLN-004 · **Mode:** lightweight · **Budget:** 3/3 pts consumed

Sources: `docs/sprints/sprint-04/reqs.md`, `release.md`, `plan-summary.md`, `.gse/plan.yaml`, `.gse/backlog.yaml`.

## Patterns

- **Retroactive TCP is viable:** When a sprint ships without a test campaign file, a later sprint can reconstruct it from activity notes and pytest inventories (TCP-S02). The format stays the same — what changes is the `note:` field documenting the reconstruction.
- **"Verify and close" as a task type:** TASK-009 required no code changes — the artefacts already existed. Explicitly scheduling a verification task in a sprint clears debt visibly rather than leaving it as an eternal "could" in the pool.
- **Living requirements as a sync point:** `docs/requirements.md` serves as a human-readable overview while sprint `reqs.md` files hold formal REQ entries. Periodic sync (like TASK-010) prevents drift between the two.

## Lessons learned

- **Pool debt clears fast when prioritized:** TASK-008..010 lingered for two sprints (S03 compound flagged it). Once pulled into S04, all three closed in one lightweight session. Prevention: always pull at least one pool item per sprint, or explicitly defer with a DEC entry.
- **Docs-only sprints fit lightweight mode well:** No code changes, no review findings, no test regressions. The plan→reqs→produce→deliver flow completed in a single session with no friction.
- **Ad-hoc changes between sprints need tracking:** The v1 UI rollback (between S03 compound and S04 plan) was an operational fix, not a sprint deliverable. It was committed and deployed but not formally tracked by any TASK. For future ad-hoc fixes: consider a hotfix TASK or a changelog note in `requirements.md` (which was done in S04 sync).

## Best practices confirmed

- **TCP at deliver:** Having TCP-S04 at deliver (not just "tests pass") gives a traceable artefact for each sprint, even docs-only ones.
- **Empty pool after sprint:** S04 leaves the backlog pool empty — a clean state for the next planning session.

## Technical debt

- No new debt introduced. S02 debt is fully cleared.
- **Remaining consideration:** Sprint directories are accumulating (S01–S04 under `docs/sprints/`). Archival of older sprints (S01–S02) to `docs/archive/` is recommended per the compound spec but deferred to user preference.

## Methodology (Axe 2)

- **Observations:** 2 — (1) ad-hoc v1 rollback between sprints lacked formal task tracking; (2) docs-only sprint completed with zero friction in lightweight mode.
- **Themes:** (1) **inter-sprint hotfix tracking**.
- **Route:** Local only — `docs/sprints/sprint-04/methodology-feedback.md`; no `github.upstream_repo` configured.

## Competency (Axe 3)

- **Practiced:** Living documentation maintenance, test campaign traceability, retroactive process compliance.
- **Growth signal:** User is now comfortable with the full GSE lifecycle (plan→reqs→produce→deliver→compound) across 4 sprints, including both code and docs sprints.
- **No new LEARN items** — S04 was documentation housekeeping with no new technical concepts.
