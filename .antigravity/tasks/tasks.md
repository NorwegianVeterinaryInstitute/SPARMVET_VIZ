# Tasks (SOLE SOURCE OF TRUTH)
# Workspace ID: SPARMVET_VIZ
# Last Updated: 2026-03-26 by @dasharch

## 🟢 Infrastructure & Recovery (100% DONE)
- [x] **Browser Access Fix:** Restored external accessibility.
- [x] **Workspace Root Indexing Configuration:** Configured `.aiignore`.
- [x] **Antigravity Mirror Initialization:** Implemented `./.antigravity/` hierarchy.
- [x] **Active Prototype Identification:** Isolated `./config/manifests/pipelines/` as source of truth.
- [x] **Dot-prefix Normalization:** Renamed `aiignore` to `.aiignore`.
- [x] **History Mapping:** Mapped session `5f6e2848-32c4-4ed2-bf50-24a3144ee29a` to conversations.
- [x] **Dot-venv Initialization:** Initialized `.venv` using `ADR-009` monorepo strategy.
- [x] **Independent Package Sync:** Created `pyproject.toml` for all core library paths.
- [x] **Outdated Directory Cleanup:** [DONE] Delete `config/manifests/species/` and `templates/`.

## 🟡 Backend & 'Decorator-First' (ACTIVE FOCUS)
- [x] **Implement 'drop_duplicates' Action:** Created decorator in `libs/transformer/core/`.
- [x] **Implement 'summarize' Action:** Created decorator in `libs/transformer/core/`.
- [ ] **Phase 1: Sequential Decorator Verification:**
  - [x] **Action Audit: 'fill_nulls'** (Core)
  - [x] **Action Audit: 'drop_nulls'** (Core)
  - [x] **Action Audit: 'replace_values'** (Core)
  - [x] **Action Audit: 'rename'** (Core)
  - [x] **Action Audit: 'drop_duplicates'** (Core)
  - [x] **Action Audit: 'summarize'** (Core)
  - [x] **Action Audit: 'split_and_explode'** (Advanced)
  - [x] **Action Audit: 'derive_categories'** (Advanced)
- [ ] **Phase 2: Adding supplementary decorators and testing**
  - [x] **Action Audit: 'unique_rows'** (Core)
  - [x] **Action Audit: 'keep_columns'** (Core)
  - [x] **Action Audit: 'strip_whitespace'** (Core)
  - [x] **Action Audit: 'split_column'** (Core)
  - [x] **Action Audit: 'Identity Logic'** (ADR-014) [DONE]
  - [x] **USER Check:** Validated APEC Virulence dataset with Identity Transformation.
      - [x] **Manifest creation - external virulence genes**
      - [x] **Manifest creation - VIGAS-P VirulenceFinder - incl. wrangling**
      - [x]  **Manifest creation - Abromics MLST - incl. wrangling**
      - [x]  **Manifest creation - metadata  - no wrangling necessary**
- [ ] **Phase 3: Atomic Layer Optimization (ACTIVE)**
  - [x] **Implement 'unique_rows' Action:** Complete core logic in `data_wrangler.py` (Registered in `duplicates.py`).
  - [x] **implemented join actions incl. join_filter**
  - [x] **Verify Atomic Contract:** Confirm Wrangler stays join-free.
  - [x] **Decorator Test Automation:** Created `test_decorator_suite.py`.
  - [x] **Naming Law Implementation:** Enforced 1:1:1 Naming Law (Action:Manifest:Data).
  - [x] **Source Standardization:** Audit 17/17 manifests in `./libs/transformer/tests/data/`.
  - [x] **Documentation Mirroring:** Updated conventions and created `decorator_testing.qmd`.
- [x] **Phase 4: The Assembly Factory (DONE)**
  - [x] **Ingestion Logic Adaptation:** Support ADR-015 source blocks.
  - [x] **Batch Validation Test:** Connectivity Table verified.
  - [x] **Modular Integrity Audit:** Verified "Clear Lines" Policy across all libs.
  - [x] **Phase 4 orchestrator: Implement DataAssembler** to join MLST_results and metadata_schema.
  - [x] **Relational Actions:** Implement `@register_action("join")` and `"join_filter"`.
  - [x] **Assembly Debugger:** Created `libs/transformer/tests/assembler_debug.py`.
  - [x] **Verification:** Verified full pipeline with AR1 assembly recipe. result: 8-column schema, 0 rows (expected intersection on dummy data).
- [ ] **Test Data Integration:** Use `assets/scripts/` to generate ST22 dummy data.
- [x] **Verification Testing:** Run `libs/transformer/tests/wrangler_debug.py` on implemented actions.

## BLOCKER IMPORTANT DO THIS BEFORE ANYTHING ELSE !!
- [x] Review structure and instruction agent rules and knowledge and sanitized - but backup before (might be too long) -> recheck the workspace rules _ I could not see it so I added a copy in my EVE folder and made sure it was updated - compare those files 
- [x] Enusre that the viz_factory that is started will use those rules 


## VIZ_FACTORY IMPLEMENTATION 
- [x] Directory creation for each layer and README.md 
### 🎨 Viz Factory: Geoms Implementation Tracker
#### Phase 1: Core Fundamentals
- [x] geom_point: Basic scatter plots.
- [ ] geom_line: Path/Time-series data.
- [ ] geom_bar / geom_col: Categorical distributions and totals.
- [ ] geom_histogram: Continuous frequency distributions.

#### Phase 2: Statistical & Distributional
- [ ] geom_boxplot: Quartile summaries (requires stat_boxplot).
- [ ] geom_violin: Density summaries (requires stat_ydensity).
- [ ] geom_smooth: Regression lines and CI ribbons.
- [ ] geom_density: 1D Kernel density estimation.

#### Phase 3: Specialized Visuals
- [ ] geom_errorbar / geom_pointrange: Uncertainty visualization.
- [ ] geom_tile / geom_raster: Heatmaps and grids.
- [ ] geom_text / geom_label: Data annotation.
- [ ] geom_jitter: Avoiding overplotting.

### 🎨 Viz Factory: Scale Implementation Tracker

#### 1. Color & Fill Scales (Continuous)
- [ ] `scale_color_gradient`: Two-color gradient (low-high)
- [ ] `scale_color_gradient2`: Diverging three-color gradient (low-mid-high)
- [ ] `scale_color_distiller`: ColorBrewer sequential/diverging palettes for continuous data
- [ ] `scale_color_viridis_c`: Matplotlib Viridis/Magma/Inferno palettes (Perceptually Uniform)
- [ ] `scale_color_cmap`: Any Matplotlib Colormap by name

#### 2. Color & Fill Scales (Discrete)
- [ ] `scale_color_discrete`: Default categorical color scale
- [ ] `scale_color_brewer`: ColorBrewer palettes (Set1, Dark2, etc.) for categories
- [ ] `scale_color_manual`: User-defined hex code mapping
- [ ] `scale_color_viridis_d`: Discrete Viridis palettes

#### 3. X & Y Axis Scales
- [ ] `scale_x_continuous` / `scale_y_continuous`: Standard linear axes
- [ ] `scale_x_log10` / `scale_y_log10`: Logarithmic transformations
- [ ] `scale_x_reverse` / `scale_y_reverse`: Inverted axes
- [ ] `scale_x_discrete` / `scale_y_discrete`: Categorical/Factor axes
- [ ] `scale_x_datetime` / `scale_y_datetime`: Date/Time handling

#### 4. Size, Shape, and Alpha Scales
- [ ] `scale_size_continuous`: Map data values to point size or line width
- [ ] `scale_size_manual`: Explicitly set sizes for categories
- [ ] `scale_shape_discrete`: Map categories to different symbols (circle, square, etc.)
- [ ] `scale_shape_manual`: User-defined symbol mapping
- [ ] `scale_alpha_continuous`: Map data to transparency levels

#### 5. Binned Scales (New in Plotnine)
- [ ] `scale_color_binned`: Binned continuous color mapping
- [ ] `scale_size_binned`: Binned area/size mapping

#### 6. Identity Scales (Direct Value Use)
- [ ] `scale_color_identity`: Use data column strings as colors directly
- [ ] `scale_alpha_identity`: Use data column values as transparency directly

### Themes layer implementation (themes/) 

### Facets layer implementation (facets/) 


## 🔴 Frontend & Visualisation (ACTIVE)
- [x] **Replace viz_factory placeholders with Plotnine decorator logic:** Converted hardcoded logic to `@register_plot_component`.
- [x] **Prototype Polars-to-Plotnine data handoff:** Implemented ADR-010 LazyFrame collection in `VizFactory (viz_factory.py)`.
- [ ] **Reactive State Management:** Implement ADR-021 (Anchor vs. Filter) state hand-off.
- [ ] **Shiny App Implementation:** Populating `app/src/ui.py` and `app/src/server.py`.
- [ ] **Four-Pillar Integration:** Link `app/modules/help_registry.py` into dashboard.
 
## 📘 Documentation Recovery (DONE)
- [x] **Mermaid Sync & Relocation:** Moved `.mmd` files to local directories.
- [x] **Broken Link Reconciliation:** Fixed `guide/` into `workflows/` paths.
- [x] **Aesthetic Overhaul:** Standardized high-contrast technical theme for all diagrams.
- [x] **Quarto Master Alignment:** Updated `_quarto.yml` with full chapter list.


## ⚪ Deferred & Phase 3
- [ ] **Plotly Interactivity:** [DEFERRED] Move native interactivity to Post-Prototype phase.
- [ ] **Mode B API:** [DEFERRED] BioBlend/Galaxy dynamic connector.
- [ ] **Advanced Error Handling:** [DEFERRED] Malformed Data gatekeeping.
- [ ] **JSON term Cleanup:** [PENDING] Scrub `./docs/` for 'JSON' mentions.
