# Tasks (SOLE SOURCE OF TRUTH)

# Workspace ID: SPARMVET_VIZ

# Last Updated: 2026-04-14 by @dasharch

## 🟣 Global Tiered Migration & Documentation Lock (COMPLETED)
>
> Status: COMPLETED. Detailed history moved to: [./.antigravity/tasks/archives/tasks_archive_2026-04-10.md]

## 🟢 2026-04-10 Session Progress (COMPLETED)
>
> Status: COMPLETED. Detailed history moved to: [./.antigravity/tasks/archives/tasks_archive_2026-04-10.md]

## 🟢 2026-04-14 Session: UI Forensic Audit & Persona Hardening (COMPLETED)

- [x] **Audit Gatekeeper**: Implemented mandatory comment-based node annotation to gate the 'Apply' execution pipeline. Verified for both standard and join nodes. (ADR-026)
- [x] **Persona Masking Architecture**: Standardized persona-based feature masking across all UI components (Tabs, Sidebars, Plotting) based on the Persona Reactivity Matrix.
- [x] **Comparison Theater Refactor**: Re-implemented the Analysis Theater as a 2x2 Quadrant Grid (Ref/Active) with position-aware maximization logic. (ADR-029a)
- [x] **Headless UI Verification**: Developed `app/tests/test_ui_persona_masking.py` to prove Silicon-Gate compliance for all five persona templates.
- [x] **Agnostic Discovery Verification**: Confirmed all manifest-defined plots are correctly registered and discoverable in the groups via the `group_stats` calc.

## 🟡 NEXT SESSION: Relational Pipeline Stress Testing & Gallery Submission

- [ ] **Relational Row-Explosion Audit**: Stress test the Tier 2 Join logic using the ST22 manifest to ensure no unintended Cartesian products across curiosity branches.
- [ ] **Gallery Submission Pipeline**: Implement the reactive backend for `btn_gallery_open_submission` to allow for formal result preservation.
- [ ] **UI Performance Benchmark**: Optimize the reactive `is_feature_enabled` helper to ensure zero-latency persona switching during live sessions.

## ⚪ Phase 3 (DEFERRED)

- [ ] **Plotly Interactivity:** [DEFERRED] move native interactivity to Post-Prototype phase.
- [ ] **Mode B API:** [DEFERRED] BioBlend/Galaxy dynamic connector.
- [ ] **Advanced Error Handling:** Malformed Data gatekeeping.
- [ ] **Decision Metadata Hash:** (ADR-024 refinement) Embed SHA-256 fingerprints in Parquet branch metadata.

---

**STATUS:** UI Architectural Baseline Hardened. 🧱🔗
**Archive Pointer:** Detailed history for all tiered wrangling refactors is located in [./.antigravity/tasks/archives/tasks_archive_2026-04-10.md].
