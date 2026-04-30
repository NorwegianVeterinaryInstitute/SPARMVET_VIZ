# Tasks

## 🟣 System Alignment & Architectural Reconciliation

- [x] Read all PATHS_INITIATION.md mandated files.
- [x] Check `libs/transformer`, `libs/viz_factory` etc for Editable Mode (pyproject.toml/sys.path usage).
- [x] Discrepancy checks for Phase 11/12 (`app/src/ui.py` and `server.py`).
- [x] Check `t3_recipe` logic in `wrangle_studio.py` vs Tiered Data Lifecycle (ADR-024) and hashing.
- [x] Documentation Integrity checks (`README.md` and docs for Violet Law).
- [x] Provide Audit Report in Table format.

## 🟡 Technical Debt & Stability (Pending)

- [x] Fix ADR-016 Defiance: Remove `sys.path.insert`/`sys.path.append` across all `libs/*/tests/` and `app/tests/`.
- [x] Inject Strict Header Ban Warning into all converted tests.
- [x] Retest Libraries: Run wrapper scripts (`transformer_integrity_suite.py`, etc.) natively to ensure stability.
- [x] UI Performance: Add hierarchical caching (`project->dataset->plot`) for schemas/datasets within `Bootloader` and Server.
- [x] Gallery Refinement: Refactor Gallery (Location 5) to serve static `.png` and YAML exclusively for rapid transitions, and fix Dev persona pre-loading.
- [x] Rulebook Update: Append Cache Architecture logic and Gallery boundaries to `rules_ui_dashboard.md`.
