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
>
> Status: COMPLETED. Detailed history moved to: [./archives/tasks_archive_2026-04-14.md]

## 🟡 NEXT SESSION: Relational Pipeline Stress Testing & Gallery Submission

- [ ] **Relational Row-Explosion Audit**: Stress test the Tier 2 Join logic using the ST22 manifest to ensure no unintended Cartesian products across curiosity branches.
- [x] **Gallery Submission Pipeline**: Implement the reactive backend for `btn_gallery_open_submission` to allow for formal result preservation.
  - [x] [HEADLESS] Implement `GalleryManager` for folder-based persistence (libs/viz_gallery).
  - [x] [HEADLESS] Create `@verify` debugger (debug_gallery_submission.py) and materialize to tmp/.
  - [x] [UI] Bind backend to `server.py` and enforce Gatekeeper constraints.
- [ ] **UI Performance Benchmark**: Optimize the reactive `is_feature_enabled` helper to ensure zero-latency persona switching during live sessions.

## ⚪ Phase 3 (DEFERRED)

- [ ] **Plotly Interactivity:** [DEFERRED] move native interactivity to Post-Prototype phase.
- [ ] **Mode B API:** [DEFERRED] BioBlend/Galaxy dynamic connector.
- [ ] **Advanced Error Handling:** Malformed Data gatekeeping.
- [ ] **Decision Metadata Hash:** (ADR-024 refinement) Embed SHA-256 fingerprints in Parquet branch metadata.

---

**STATUS:** UI Architectural Baseline Hardened. 🧱🔗
**Archive Pointer:** Detailed history for all tiered wrangling refactors is located in [./.antigravity/tasks/archives/tasks_archive_2026-04-10.md].
