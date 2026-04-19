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

## 🟢 Phase 16: Gallery Taxonomy & Scaling (COMPLETED 2026-04-19)

- [x] **Metadata Harmonization**: Extracted taxonomy from `recipe_meta.md` into YAML `info` blocks.
- [x] **Pivot-Index Engine**: Implemented `GalleryIndexer` and `gallery_index.json` structure (ADR-037).
- [x] **Governance Wrapper**: Implemented `libs/viz_gallery/assets/refresh_gallery.py` for audit & indexing.
- [x] **UI logic Activation**: Switched `server.py` to use high-performance Set Intersections for all gallery filtering.
- [x] **Ergonomic Polish**: Promoted selector to top of sidebar, added Play-style Apply button, and restored previews.
- [ ] **Taxonomy Data Audit**: [DEFERRED] Verify and correct the tags for the taxonomy classification (Family/Pattern/Difficulty) in gallery assets manifests (`assets/gallery_data/*/recipe_manifest.yaml`).

## 🟢 Phase 17: Contextual UI Masking & Focus Mode (COMPLETED 2026-04-19)

- [x] **Contextual Masking (ADR-038)**: Implemented server-side reactive reification in `server.py` to mask redundant tools.
- [x] **Global Nav Persistence**: Promoted Home/Gallery selector to a persistent header in the left sidebar.
- [x] **Seamless Switch signaling**: Implemented Home-tab focus mode when cloning from gallery.

## 🟢 Phase 18: Blueprint Architect — Bidirectional Lineage Navigation (ACTIVE)

**Objective**: Transform the Blueprint Architect into a full bidirectional manifest development environment. A scientist can start from a desired plot output and trace backwards to find where a missing field must be added (reverse lineage), or build forward from source to plot (forward lineage). Full design rationale in ADR-040.

### Phase 18-A: Field Materialization & Component Context Map (IN PROGRESS 2026-04-19)

- [x] Move `normalize_manifest_fields.py` to `app/assets/` with importable `normalize_file()` API.
- [x] Add `btn_normalize_fields` ("⚙️ Fix Format") button to Interface (Fields) tab in `wrangle_studio.py`.
- [x] Wire `btn_normalize_fields` handler in `server.py` — writes file in-place with `.bak` backup, reloads workspace.
- [x] Fix `_parse_fields_safe` to handle rich `{col: {type, label, ...}}` dict format.
- [x] Fix `_normalize_fields` to handle rich dict format (extracts `type`/`label` instead of `str(v)`).
- [x] Add `_build_sibling_map()` module-level helper — parses master YAML without resolving `!include`, maps each component rel_path to `{role, schema_id, schema_type, siblings}`.
- [x] Add `_load_fields_file()` helper — unwraps redundant wrapper keys (ADR-014 parity).
- [x] Add `_component_ctx_map` reactive value; populate from `_build_sibling_map` on manifest selection.
- [x] Rewrite field-loading in `_handle_manifest_import` to be role-aware: `input_fields` file → left panel; `output_fields` file → right panel; `wrangling` Tier 1 → both panels from siblings.
- [ ] **Extend `_build_sibling_map`** to capture `ingredients` list (assembly blocks) and `target_dataset` (plot specs). [NEXT]
- [ ] **Assembly upstream display**: Render multi-ingredient accordion in left panel — one section per ingredient with its output_fields.
- [ ] **Plot node display**: Resolve `target_dataset` → parent assembly → final_contract for plot left panel.

### Phase 18-B: Lineage Rail UI (Component Chain View)

- [ ] **Tab B in TubeMap accordion**: "Component Lineage Rail" — renders linear chain for selected node from raw source to terminal plot.
- [ ] **Branch selector**: When assembly branches to N plots, show branch tabs so user can select which downstream path to trace.
- [ ] Wire Rail node clicks to populate the 3-column Interface panel below.

### Phase 18-C: 3-Column Interface Panel (replaces flat tab-3)

- [ ] **Left — Upstream Contract**: Fields arriving at selected node. Tier 1 wrangling → input_fields table. Assembly → multi-ingredient accordion. Plot → parent assembly final_contract.
- [ ] **Center — Active Component**: Wrangling recipe / plot spec / field schema. Editable. The existing Logic Stack lives here.
- [ ] **Right — Downstream Contract**: Fields leaving selected node. Tier 1 wrangling → output_fields. Assembly → final_contract. Plot → "Plot terminal — no output schema."

### Phase 18-D: Per-Plot Wrangling Support

- [ ] **Manifest key `pre_plot_wrangling`**: Optional `!include` in plot block for dataset-specific transforms (wide/long pivots, aggregations, plot-level filters).
- [ ] **Lineage Rail node**: `pre_plot_wrangling` appears as an intermediate node between assembly output and plot spec.
- [ ] **"➕ Add plot wrangling" affordance**: If the slot is absent, offer a button to scaffold the file.

### Phase 18-E: Reverse Navigation ("I want field X")

- [ ] **Field Gap Analysis tool**: Enter a desired field name → the tool walks the lineage backwards and shows which pipeline step is the earliest point where the field can be added or computed.
- [ ] **Forward propagation hint**: After identifying the insertion point, highlight which output_fields and final_contract files need to be updated to carry the field forward to the plot.

### Phase 18-F: Interactive TubeMap Engine (ADR-039, original scope)

- [ ] **Interactive TubeMap (ADR-039)**: Full Mermaid/SVG DAG with clickable nodes driving the Lineage Rail.
- [ ] **Action Registry Parity**: Map the complete `@register_action` library (175+ actions) to the Architect.
- [ ] **Visual Forking**: Select a node and initiate a new branch, producing YAML additions to the manifest.

## 🟡 NEXT SESSION

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
  - [ ] [HEADLESS] Retest & Fix deferred components: `scale_x_timedelta`, `scale_y_timedelta` (dtype mismatch), `geom_map` (requires spatial data). [DEFERRED] Decorators commented out in `scales/core.py` and `geoms/core.py`.
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

# USER TESTING [DEFERRED]

- [ ] Gallery:_ Test The Clone to sandbox functionality (can only be done when more advanced in other modes for development wrangling)

# IMPROVEMENETS IDEAS [DEFERRED]

- [ ] Gallery thumbnails for finding faster the plots we want to look at ?

---

**STATUS:** UI Architectural Baseline Hardened. 🧱🔗
**Archive Pointer:** Detailed history for all tiered wrangling refactors is located in [./.antigravity/tasks/archives/tasks_archive_2026-04-10.md].
