---
gse:
  sprint: 3
  artefact_type: requirements
  status: approved
  created: "2026-04-24"
---

# Sprint S03 — Requirements (UI v2)

## Goal

Ship **website interface v2** with a deliberate **2007 Apple design language** (Mac OS X **Leopard** / **Aqua**: glossy chrome, pinstripes, unified title bars, Lucida-style typography). Preserve **all functional behavior** (upload, results, bubbles, deploy gate, no buy prices in UI).

## REQ-301 — Baseline v1 preserved

**Priority:** must  
**Acceptance:** Given the repository, when a developer runs `git show website-v1:static/style.css` (or opens `static/style-v1-baseline.css`), then the pre-v2 stylesheet is available for comparison or rollback.

## REQ-302 — Visual language

**Priority:** must  
**Acceptance:** Given any app page (upload, results, deploy), when rendered in a browser, then:

- Page uses a **blue gradient title bar** treatment for the main title (Aqua-style header).
- Content areas use **brushed / metal panel** framing (border + inset highlight), not flat Material cards.
- Primary actions use **glossy rounded** button styling (Aqua pill buttons).
- Body background suggests **subtle pinstripe** texture (CSS; no image asset required).
- Typography stacks to **Lucida Grande / Helvetica Neue** first.

## REQ-303 — No functional regression

**Priority:** must  
**Acceptance:** Existing pytest suite passes; CSV upload still omits buy prices from HTML; bubble timeline and deploy gate behave unchanged.

## REQ-304 — Version label

**Priority:** should  
**Acceptance:** Footer or equivalent on each page notes **Interface v2** and Leopard/Aqua (2007) inspiration for operator clarity.
