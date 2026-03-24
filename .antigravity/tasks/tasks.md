# Tasks (SOLE SOURCE OF TRUTH)
# Workspace ID: SPARMVET_VIZ
# Last Updated: 2026-03-24 by @dasharch

## 🟢 Infrastructure & Recovery (100% DONE)
- [x] **Browser Access Fix:** Restored external accessibility.
- [x] **Workspace Root Indexing Configuration:** Configured `.aiignore`.
- [x] **Antigravity Mirror Initialization:** Implemented `./.antigravity/` hierarchy.
- [x] **Active Prototype Identification:** Isolated `./config/manifests/pipelines/` as source of truth.
- [x] **Dot-prefix Normalization:** Renamed `aiignore` to `.aiignore`.
- [x] **History Mapping:** Mapped session `5f6e2848-32c4-4ed2-bf50-24a3144ee29a` to conversations.
- [x] **Dot-venv Initialization:** Initialized `.venv` using `ADR-009` monorepo strategy.
- [x] **Independent Package Sync:** Created `pyproject.toml` for all core library paths.
- [ ] **Outdated Directory Cleanup:** [PENDING] Delete `config/manifests/species/` and `templates/`.

## 🟡 Backend & 'Decorator-First' (ACTIVE FOCUS)
- [x] **Implement 'drop_duplicates' Action:** Created decorator in `libs/transformer/core/`.
- [x] **Implement 'summarize' Action:** Created decorator in `libs/transformer/core/`.
- [ ] **Phase 1: Sequential Decorator Verification:**
  - [ ] **Action Audit: 'fill_nulls'** (Core)
  - [ ] **Action Audit: 'drop_nulls'** (Core)
  - [ ] **Action Audit: 'replace_values'** (Core)
  - [ ] **Action Audit: 'rename'** (Core)
  - [ ] **Action Audit: 'drop_duplicates'** (Core)
  - [ ] **Action Audit: 'summarize'** (Core)
  - [ ] **Action Audit: 'split_and_explode'** (Advanced)
  - [ ] **Action Audit: 'derive_categories'** (Advanced)
- [ ] **Test Data Integration:** Use `assets/scripts/` to generate ST22 dummy data.
- [ ] **Verification Testing:** Run `libs/transformer/tests/test_wrangler.py` on implemented actions.

## 🔴 Frontend & Visualisation (CURRENT BLOCKER)
- [x] **Replace viz_factory placeholders with Plotnine decorator logic:** Converted hardcoded logic to `@register_plot`.
- [ ] **Prototype Polars-to-Plotnine data handoff:** Detect Lazy vs Eager state for collection.
- [ ] **Shiny App Implementation:** Populating `app/src/ui.py` and `app/src/server.py`.
- [ ] **Four-Pillar Integration:** Link `app/modules/help_registry.py` into dashboard.

## ⚪ Deferred & Phase 3
- [ ] **Plotly Interactivity:** [DEFERRED] Move native interactivity to Post-Prototype phase.
- [ ] **Mode B API:** [DEFERRED] BioBlend/Galaxy dynamic connector.
- [ ] **Advanced Error Handling:** [DEFERRED] Malformed Data gatekeeping.
- [ ] **JSON term Cleanup:** [PENDING] Scrub `./docs/` for 'JSON' mentions.
