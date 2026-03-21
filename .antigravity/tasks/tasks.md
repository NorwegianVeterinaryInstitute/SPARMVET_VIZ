# Tasks (The Source of Truth)
# Workspace ID: SPARMVET_VIZ
# Last Updated: 2026-03-21 by @dasharch

## 🟢 Infrastructure & Recovery (MIRROR COMPLETE)
- [x] **Browser Access Fix:** Restored external and tool-set accessibility.
- [x] **Workspace Root Indexing Configuration:** Configured `.aiignore` and directory standard.
- [x] **Antigravity Mirror Initialization:** Implemented `./.antigravity/` hierarchy.

## 🟡 Backend Architecture & Guardrails
- [x] **ConfigManager Implementation:** Robust YAML `!include` strategy confirmed.
- [x] **Transformer Plugin Refactor:** Monolithic `registry.py` replaced by decorator-driven `actions/`.
- [x] **Wrangling Documentation:** Quarto cheatsheet created at `docs/cheatsheets/wrangling_actions.qmd`.
- [ ] **Schema Progress Audit:** [HIGH PRIORITY] Scan `./config/schemas/` to identify JSON validation state.
- [ ] **Verification Testing:** Run `libs/transformer/tests/test_wrangler.py` to validate plugin execution.

## 🔴 Frontend Scaffolding (CURRENT BLOCKER)
- [ ] **Shiny App Implementation:** Populating `app/src/ui.py` and `app/src/server.py` (Functional layout).
- [ ] **Four-Pillar Integration:** Link `app/modules/help_registry.py` into dashboard.
- [ ] **Interactive Visualization:** Connect Plotly/D3 wrappers from `libs/viz_factory`.

## ⚪ Deferred & Phase 3
- [ ] **Mode B API:** [DEFERRED] BioBlend/Galaxy dynamic connector logic.
- [ ] **Advanced Error Handling:** [DEFERRED] "Malformed Data" ingestion gatekeeping.
- [ ] **Dashboard Assembly:** Finalize reactive state management.
