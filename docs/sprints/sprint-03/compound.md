# Sprint S03 — Capitalization

**Plan:** PLN-003 · **Mode:** lightweight · **Budget:** 2/2 pts consumed

Sources: `docs/sprints/sprint-03/reqs.md`, `release.md`, `plan-summary.md`, `.gse/plan.yaml`, `.gse/backlog.yaml`. No formal `review.md` (lightweight path).

## Patterns

- **Tag + file twin for UI rollback:** Git tag `website-v1` plus `static/style-v1-baseline.css` gives two recovery paths (`git show` vs copy), matching REQ-301.
- **CSS variables for metal layers:** `--bg-brushed`, `--panel-brushed`, `--titlebar-brushed` keep Leopard chrome consistent and tweakable without hunting literals.
- **REQ-shaped pytest hooks:** Small tests keyed to REQ-301/302/304 make deliver guardrails honest without a full S03 `test-strategy.md`.
- **Template shell contract:** `theme-leopard`, `page-titlebar`, `aqua-window` give tests a stable structural contract for “v2 is loaded”.

## Lessons learned

- **Retro visual design is still testable:** Structure and copy (footer, classes) can be asserted in pytest; full pixel fidelity stays manual.
- **Follow-up polish after “done”:** Brushed-metal refinement landed in a second commit — acceptable if release notes mention it or scope is time-boxed.
- **Pool tasks linger:** TASK-008..010 (S02 debt) unchanged through S03; **prevention:** pull at least one pool item into the next plan or explicitly defer with a DEC.

## Best practices confirmed

- **Deliver before compound:** `release.md` + `plan-summary.md` made capitalization factual, not reconstructed from memory.
- **Branch-only sprint:** Single stream on `main` stays compatible with GSE deliver when scope is one TASK.

## Technical debt

- **No TCP for S03:** UI-only sprint; optional `docs/sprints/sprint-03/test-reports/TCP-S03.md` if methodology requires parity with S01.
- **Visual regression:** No screenshot / Playwright baseline; future drift only caught by structural tests or manual QA.
- **requirements.md:** TASK-010 still open — FR-005 / deploy NFR sync not updated this sprint.

## Methodology (Axe 2)

- **Observations:** 3 — pool neglect, optional TCP for small UI sprint, requirements.md gap.
- **Themes:** (1) **backlog hygiene across sprints**, (2) **lightweight test artefacts**.
- **Route:** Local only — `docs/sprints/sprint-03/methodology-feedback.md` (no `github.upstream_repo`); no `compound-tickets-draft.yaml`.

## Competency (Axe 3)

- **Practiced:** Historical UI styling (Aqua/Leopard), layered CSS gradients, design–test traceability for non-functional reqs.
- **LEARN ideas (optional):** “CSS-only texture limits vs image assets”, “Visual regression testing for Flask/Jinja”.

## Integration

- Run **`/gse:integrate`** next to route Axe 1–3 into config, backlog, and learning notes.
