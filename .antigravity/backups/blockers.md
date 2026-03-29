# Blockers & Technical Debt (SPARMVET_VIZ)
# Last Updated: 2026-03-24 by @dasharch

## 🧱 Blocker: Data Orchestration - Lazy vs. Eager
**Category:** Implementation Logic | **Priority:** HIGH
**Context:** Polars operations use LazyFrames, but Plotnine requires in-memory DataFrames.
**Decision Needed:** Should the Orchestrator (Server) or the Viz Factory call `.collect()`?
**Current Status:** Undecided. Pending Phase B prototype.


## 🧱 Blocker: Multi-Dataset Phonotype Validation
**Category:** Algorithmic | **Priority:** MEDIUM
**Context:** Extending the "Explode-Join-Collapse" logic for complex AMR mappings beyond ResFinder.
**Status:** ACTIVE in Phase B/C.

## 🧱 Blocker: Metadata Constant Extraction
**Category:** Implementation Logic | **Priority:** MEDIUM
**ID:** ST22-001
**Context:** Need to extract unique values from columns (e.g., 'Scheme' in MLST data: `ecoli_achtman_4`) to be used as global information for plots or methods.
**Status:** [OPEN] Deferred solution needed.
