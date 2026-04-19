# Tasks (SOLE SOURCE OF TRUTH)

**Workspace ID:** SPARMVET_VIZ
**Last Updated:** 2026-04-17 by @dasharch

## 🟣 Global Tiered Migration & Documentation Lock (COMPLETED)
>
> Status: COMPLETED. Detailed history moved to: [./.antigravity/tasks/archives/tasks_archive_2026-04-10.md]

## 🟢 2026-04-10 Session Progress (COMPLETED)
>
> Status: COMPLETED. Detailed history moved to: [./.antigravity/tasks/archives/tasks_archive_2026-04-10.md]

## 🟢 2026-04-18 Session: Layout stabilization, Hierarchical Navigation & Aesthetic polish (COMPLETED)
>
> Status: COMPLETED. Detailed history moved to: [./.antigravity/logs/audit_2026-04-18.md]

## 🟢 2026-04-18 Session (Cont.): Structural Repair & UI Integrity (COMPLETED)
>
> Status: COMPLETED. Detailed history available in: [./.antigravity/logs/audit_2026-04-18.md]

## 🟣 UI Infrastructure & Integrity (BASELINE LOCK)
>
> Status: COMPLETED. The Analysis Theater satisfies all forensic alignment and ID sanitation requirements.

## 🟡 NEXT SESSION

- [ ] Continue UI improvement - User will give instructions

## 🟡 2d NEXT SESSION: Relational Pipeline Stress Testing & Gallery Submission

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
  - [x] [HEADLESS] Implement 3rd-party themes (538, Seaborn, XKCD, Tufte) (themes/core.py).
- [x] **Integrity Audit & Test Coverage**:
  - [x] [HEADLESS] Generate test manifests and TSV data for all 175 components.
  - [x] [HEADLESS] Verify 98.3% integrity coverage via `viz_factory_integrity_suite.py` (172/175 PASSED).
  - [ ] [HEADLESS] Retest & Fix deferred components: `scale_x_timedelta`, `scale_y_timedelta` (dtype mismatch), `geom_map` (requires spatial data). [DEFERRED]
- [x] **Documentation Sync**:
  - [x] Updated `libs/viz_factory/README.md` with pass rates.
  - [x] Updated `docs/appendix/viz_factory_components.qmd` with gallery examples for all major component groups.
- [x] **Transformer completeness check**: Verified all primary Polars actions are implemented (Added `mutate` for arbitrary expressions).
- [ ] Workspace hygiene: remove temporary tests from tmp/ and dispose of unique scripts. [PENDING]
- [ ] Automatic adjustment labels size, orientation and space for plots [DEFERRED]

## 🟢 Phase 6: Analytical Engine Hardening (Polars Parity) (COMPLETED)

- [x] **Window & Sequential Logic**:
  - [x] Implement `window_agg` (Grouped Rolling Aggregations).
  - [x] Implement `shift` / `lag` (Time-series inter-row comparison).
  - [x] Implement `fill_nulls_direction` (Forward/Backward Fill).
- [x] **Temporal Intelligence**:
  - [x] Implement `date_extract` (Year, Month, Week splitting).
  - [x] Implement `date_truncate` & `date_offset`.
- [x] **List & Struct Engineering**:
  - [x] Implement `list_slice`, `list_join`, and `is_in` logic.
- [x] **Analytical Core**:
  - [x] Implement `sort` (Multi-key deterministic ordering).
  - [x] Implement `sample` (Percentage-based data reduction).
  - [x] Implement `cum_sum` / `cum_count` (Running totals).
  - [x] Implement `z_score` and `percentile` normalization.
- [x] **Exhaustive Parity (Final Tier)**:
  - [x] Implement `select_by_pattern` (Regex column selection).
  - [x] Implement `str_replace_regex` and `null_if`.
  - [x] Implement `value_counts` and `describe_stats` generators.
- [x] **Niche/Horizontal Logic**:
  - [x] Implement `horizontal_stats`, `any_horizontal`, `all_horizontal`.
  - [x] Implement `interpolate`.

# IMPROVEMENETS IDEAS [DEFERRED]

- [ ] Gallery thumbnails for finding faster the plots we want to look at ?

---

**STATUS:** UI Architectural Baseline Hardened. 🧱🔗
**Archive Pointer:** Detailed history for all tiered wrangling refactors is located in [./.antigravity/tasks/archives/tasks_archive_2026-04-10.md].
