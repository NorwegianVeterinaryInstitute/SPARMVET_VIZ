# Tasks (SOLE SOURCE OF TRUTH)

**Workspace ID:** SPARMVET_VIZ
**Last Updated:** 2026-04-17 by @dasharch

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
  - [x] [HEADLESS] Create `debug_relational_audit.py` to stress test ST22 joins and verify relational integrity.
  - [x] [HEADLESS] Materialize Tier 2 results to `tmp/Manifest_test/ST22_audit/`.
  - [x] [HEADLESS] Validate row counts (Input Anchor vs Joined Result) and output `df.glimpse()`.
- [x] **Gallery Submission Pipeline**: Implement the reactive backend for `btn_gallery_open_submission` to allow for formal result preservation.
  - [x] [HEADLESS] Implement `GalleryManager` for folder-based persistence (libs/viz_gallery).
  - [x] [HEADLESS] Create `@verify` debugger (debug_gallery_submission.py) and materialize to tmp/.
  - [x] [UI] Bind backend to `server.py` and enforce Gatekeeper constraints.
- [x] **UI Performance Benchmark**: Optimize the reactive `is_feature_enabled` helper to ensure zero-latency persona switching during live sessions.
  - [x] [HEADLESS] Create `debug_ui_performance.py` to target persona switching latency and YAML IO overhead.
  - [x] [HEADLESS] Implement template caching in `Bootloader (bootloader.py)` to eliminate redundant disk reads.
  - [x] [HEADLESS] Verify latency reduction and materialize benchmark report to `tmp/ui_perf_audit.txt`.

## 🟢 Phase 3 (REFINED)

- [x] **Advanced Error Handling:** Malformed Data gatekeeping (ADR-034).
  - [x] [HEADLESS] Implement `MetadataValidator (metadata_validator.py)`.
  - [x] [HEADLESS] Integrate schema validation loop in `DataOrchestrator`.
  - [x] [HEADLESS] Verify typo-correction suggestions via `debug_phase3_refinements.py`.
- [x] **Decision Metadata Hash:** (ADR-024 refinement) Embed SHA-256 fingerprints in Parquet branch metadata.
  - [x] [HEADLESS] Implement deterministic recipe hashing in `utils.hashing`.
  - [x] [HEADLESS] Update `DataAssembler` to verify logic integrity before short-circuiting.
  - [x] [HEADLESS] Embed fingerprints in Parquet metadata via `pyarrow`.
- [ ] **Plotly Interactivity:** [DEFERRED] move native interactivity to Post-Prototype phase.
- [ ] **Mode B API:** [DEFERRED] BioBlend/Galaxy dynamic connector.
- [x] **Automated Element & Decorator Audit (Master Suite):**
  - [x] [HEADLESS] Create `ingestion_integrity_suite.py` (Verified 4/4 cases).
  - [x] [HEADLESS] Complete `transformer_integrity_suite.py` (Verified 37/37 actions).
  - [x] [HEADLESS] Run `viz_factory_integrity_suite.py` (Verified 123/125 components).

## 🟢 Phase 4: Artist Expansion (API Parity)

- [x] **Registry Expansion**: Achieved 1:1 parity with Plotnine 0.14.0 components (175 total registered).
  - [x] [HEADLESS] Implement 30+ missing geoms and stats (geoms/core.py).
  - [x] [HEADLESS] Implement math, date, and stroke scales (scales/core.py).
  - [x] [HEADLESS] Implement 3rd-party themes (538, Seaborn, XKCD) (themes/core.py).
- [x] **Integrity Audit**: Verified registry expansion via `viz_factory_integrity_suite.py`.
- [x] **Documentation Sync**: Updated Gallery and README to reflect new capabilities.
  - [ ] Workspace hygienne: remove all temporary tests from tmp/ Evaluate if existing scripts can be reused in library or assets for a general purpose (if so verify existance of similar script and eventually merge) otherwise if scripts were ment to be for unique usage - dispose of those. [DEFERRED]
  - [ ] Verify completness of transformer: layer verify that all wrangling, tidying and assembly elements/decorators (with associated options) that are  available in polars library are implemented in the transformer layer
  - [ ] Automatic adjustment labels size, origentation and space to write those for plots [DEFERRED]

---

**STATUS:** UI Architectural Baseline Hardened. 🧱🔗
**Archive Pointer:** Detailed history for all tiered wrangling refactors is located in [./.antigravity/tasks/archives/tasks_archive_2026-04-10.md].
