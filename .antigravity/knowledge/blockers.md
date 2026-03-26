# Blockers & Technical Debt (SPARMVET_VIZ)
# Last Updated: 2026-03-24 by @dasharch

## 🧱 Blocker: Data Orchestration - Lazy vs. Eager
**Category:** Implementation Logic | **Priority:** HIGH
**Context:** Polars operations use LazyFrames, but Plotnine requires in-memory DataFrames.
**Decision Needed:** Should the Orchestrator (Server) or the Viz Factory call `.collect()`?
**Current Status:** Undecided. Pending Phase B prototype.

## 🧱 Blocker: Outdated Directory Confusion
**Category:** Project Structure | **Priority:** MEDIUM
**Context:** Legacy folders (`config/manifests/species`, `templates`) follow an older architecture.
**Status:** [PENDING] Cleanup in Phase D.

## 🧱 Blocker: Multi-Dataset Phonotype Validation
**Category:** Algorithmic | **Priority:** MEDIUM
**Context:** Extending the "Explode-Join-Collapse" logic for complex AMR mappings beyond ResFinder.
**Status:** ACTIVE in Phase B/C.

## 🧱 Blocker: Wrangling Documentation (Cheatsheet)
**Category:** Documentation | **Priority:** LOW
**Status:** DEFERRED to Phase D. Ensuring YAML syntax examples for non-programmer maintainers.
