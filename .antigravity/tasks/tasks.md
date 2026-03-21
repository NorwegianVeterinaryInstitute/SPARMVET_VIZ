# Tasks (The Source of Truth)
# Workspace ID: SPARMVET_VIZ
# Last Updated: 2026-03-21 by @dasharch

## 🟢 Infrastructure & Recovery (MIRROR COMPLETE)
- [x] **Browser Access Fix:** Restored external accessibility.
- [x] **Workspace Root Indexing Configuration:** Configured `.aiignore`.
- [x] **Antigravity Mirror Initialization:** Implemented `./.antigravity/` hierarchy.
- [ ] **Outdated Directory Cleanup:** [PENDING] Delete `config/manifests/species/` and `templates/`.

## 🟡 Backend & 'Decorator-First' (ACTIVE FOCUS)
- [ ] **Implement 'drop_duplicates' Action:** [TOP PRIORITY] Create decorator in `libs/transformer/core/`.
- [ ] **Implement 'summarize' Action:** [TOP PRIORITY] Create decorator in `libs/transformer/core/`.
- [ ] **Test Data Integration:** Use `assets/scripts/` to generate ST22 dummy data.
- [ ] **Verification Testing:** Run `libs/transformer/tests/test_wrangler.py` on implemented actions.

## 🔴 Frontend Scaffolding (CURRENT BLOCKER)
- [ ] **Shiny App Implementation:** Populating `app/src/ui.py` and `app/src/server.py`.
- [ ] **Four-Pillar Integration:** Link `app/modules/help_registry.py` into dashboard.

## ⚪ Deferred & Phase 3
- [ ] **Mode B API:** [DEFERRED] BioBlend/Galaxy dynamic connector.
- [ ] **Advanced Error Handling:** [DEFERRED] Malformed Data gatekeeping.
- [ ] **JSON term Cleanup:** [PENDING] Scrub `./docs/` for 'JSON' mentions.
