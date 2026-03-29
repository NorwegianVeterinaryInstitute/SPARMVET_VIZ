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
### 🎨 Viz Factory: Geoms Implementation Tracker (geoms/) 
#### Phase 1: Core Fundamentals
- [x] geom_point: Basic scatter plots.
- [x] geom_line: Path/Time-series data.
- [x] geom_bar 
- [x] geom_col: Categorical distributions and totals.
- [x] geom_histogram: Continuous frequency distributions.

#### Phase 2: Statistical & Distributional
- [x] geom_boxplot: Quartile summaries (requires stat_boxplot).
- [x] geom_violin: Density summaries (requires stat_ydensity).
- [x] geom_smooth: Regression lines and CI ribbons.
- [x] geom_density: 1D Kernel density estimation.

#### Phase 3: Specialized Visuals
- [x] geom_errorbar 
- [x] geom_pointrange: Uncertainty visualization (point + range).
- [x] geom_tile: Discrete heatmaps.
- [x] geom_raster: Continuous heatmaps.
- [x] geom_text 
- [x] geom_label: Data annotation (with boxes).
- [x] geom_jitter: Avoiding overplotting.

### 🎨 Viz Factory: Scale Implementation Tracker
#### 1. Color & Fill Scales (Continuous)
- [x] `scale_color_gradient`: Two-color gradient (low-high)
- [x] `scale_color_gradient2`: Diverging three-color gradient (low-mid-high)
- [x] `scale_color_distiller`: ColorBrewer sequential/diverging palettes for continuous data
- [x] `scale_color_viridis_c`: Matplotlib Viridis/Magma/Inferno palettes (Perceptually Uniform)
- [x] `scale_color_cmap`: Any Matplotlib Colormap by name

#### 2. Color & Fill Scales (Discrete)
- [x] `scale_color_discrete`: Default categorical color scale
- [x] `scale_color_brewer`: ColorBrewer palettes (Set1, Dark2, etc.) for categories
- [x] `scale_color_manual`: User-defined hex code mapping
- [x] `scale_color_viridis_d`: Discrete Viridis palettes

#### 3. X & Y Axis Scales
> Ok - Some of those use same dataset for testing - fine
- [x] `scale_x_continuous` 
- [x] `scale_y_continuous`
- [x] `scale_x_discrete`
- [x] `scale_y_discrete`
- [x] `scale_x_log10`
- [x] `scale_y_log10`
- [x] `scale_x_reverse`
- [x] `scale_y_reverse`
- [x] `scale_x_datetime`
- [x] `scale_y_datetime`

#### 4. Size, Shape, and Alpha Scales
- [x] `scale_size_continuous`: Map data values to point size or line width
- [x] `scale_size_discrete`: Different sizes for categories
- [x] `scale_shape_discrete`: Mapping different point shapes to categories
- [x] `scale_alpha_continuous`: Variable transparency based on values
- [x] `scale_alpha_discrete`: Transparency levels for categories

#### 5. Linetype Scales
- [x] `scale_linetype_discrete`: Different dash/line patterns for categories

#### 6. Identity Scales (Direct Value Use)
- [x] `scale_color_identity`: Use data column strings as colors directly
- [x] `scale_alpha_identity`: Use data column values as transparency directly
- [x] `scale_fill_identity`: Use data column strings as fill colors directly
- [x] `scale_size_identity`: Use data column numeric values as sizes directly
- [x] `scale_shape_identity`: Use data column string values as shapes directly
- [x] `scale_linetype_identity`: Use data column values as linetypes directly



### 🎨 Viz Factory: Themes Implementation Tracker (themes/) 
#### Phase 1: Core Plotnine/Ggplot2 Standards
- [x] `theme_gray`: The default Plotnine theme (gray background, white gridlines).
- [x] `theme_bw`: White background with a thin black border.
- [x] `theme_linedraw`: Black lines on a white background.
- [x] `theme_light`: Light gray gridlines on a white background.
- [x] `theme_minimal`: No background annotations, minimal gridlines.
- [x] `theme_classic`: Axis lines with no gridlines.
- [x] `theme_void`: A completely empty theme.
- [x] `theme_dark`: Dark background for high-contrast data visualization.

#### Phase 2: SPARMVET_VIZ Branding & Customization
- [x] `theme_dashboard`: Optimized for Shiny integration (high-contrast, legible font scaling).
- [x] `theme_publication`: Journal-ready theme with specific DPI and font-weight presets.

#### Phase 3: High-Level UI Components
- [x] `element_text`: Component for modifying text aesthetics (color, size, angle, etc.) via `theme_custom`.
- [x] `element_line`: Component for modifying axis lines and gridline aesthetics via `theme_custom`.
- [x] `element_rect`: Component for plot/panel backgrounds and borders via `theme_custom`.
- [x] `theme_legend_position`: Registered component to toggle legend placement (top, bottom, left, right, none).
- [x] BLOCKER: USER MUST VERIFY THAT ALL THEMES IMPLEMENTED AND TESTED - AND THAT EACH PRODUCE A PLOT 


### 🎨 Viz Factory: Facets Implementation Tracker (facets/) 

#### Phase 1: Core Layout Components
- [x] `facet_wrap`: 1D ribbon of panels wrapped into 2D (Standard categorical splitting).
- [x] `facet_grid`: 2D grid of panels formed by the intersection of two variables.
- [x] `facet_null`: The default single-panel display (Internal reference).

#### Phase 2: Facet Configuration & Scaling
- [x] `facet_scales`: Implementation of 'free', 'free_x', and 'free_y' scale behaviors.
- [x] `facet_space`: Support for 'fixed' vs 'free' panel sizing in grids.
- [x] `facet_labeller`: Integration of custom label formatting (inherited from Plotnine).

#### Phase 3: Advanced Layouts
- [x] `facet_rows`: Shortcut component for vertical-only stacking.
- [x] `facet_cols`: Shortcut component for horizontal-only stacking.
- [x] `facet_margins`: Logic for displaying marginal totals in grid layouts.


### 🎨 Viz Factory: Coordinates Implementation Tracker (coords/) 

#### Phase 1: Cartesian & Linear Systems
- [x] `coord_cartesian`: The default Cartesian coordinate system (Standard x-y).
- [x] `coord_flip`: Cartesian coordinates with x and y flipped (Essential for horizontal bar charts).
- [x] `coord_fixed`: Cartesian coordinates with a fixed aspect ratio (Ensures 1 unit on x = 1 unit on y).

#### Phase 2: Non-Linear & Polar Systems
- [x] `coord_polar`: [DEFERRED - FEATURE NOT YET IMPLEMENTED IN PLOTNINE] Not in current source build.
- [x] `coord_trans`: Cartesian coordinates with arbitrary transformations (e.g., log, square root) applied to the axes.

#### Phase 3: Specialized Visual Mapping
- [x] `coord_equal`: Shortcut for `coord_fixed` with a 1:1 ratio.
- [x] `coord_lims`: Component for strictly enforcing axis limits at the coordinate level (prevents data clipping seen in scales).

### 🎨 Viz Factory: Positions Implementation Tracker (positions/) 
#### Phase 1: Overlapping & Stacking Logic
- [x] `position_identity`: Default positioning; places objects exactly where the data dictates (may cause overlapping).
- [x] `position_stack`: Stacks objects on top of each other (Essential for stacked bar charts).
- [x] `position_fill`: Stacks objects and standardizes height to 100% (Essential for proportional bar charts).

#### Phase 2: Separation & Jittering
- [x] `position_dodge`: Places objects side-by-side (Essential for grouped bar charts).
- [x] `position_dodge2`: Enhanced dodging for variable widths (Works with boxplots).
- [x] `position_jitter`: Adds a small amount of random noise to points to reveal overplotted data.
- [x] `position_jitterdodge`: Combines jittering and dodging (Ideal for points overlaid on boxplots).

#### Phase 3: Adjustment & Offsets
- [x] `position_nudge`: Shifts points by a specific fixed distance (Useful for moving text labels away from points).


### 🎨 Viz Factory: Guides Implementation Tracker (guides/) 


#### Phase 1: Legend & Key Logic
- [x] `guide_legend`: Standard discrete legend for scales (color, fill, shape, etc.).
- [x] `guide_colorbar`: Continuous color scale display (also known as `guide_colourbar`).
- [x] `guide_none`: Component to explicitly suppress a specific guide.

#### Phase 2: Guide Customization & Aesthetics
- [x] `guide_title`: Implementation for overriding scale titles and alignment within the guide.
- [x] `guide_label`: Support for toggling labels, setting rotation, and defining fonts.
- [x] `guide_direction`: Logic for 'horizontal' vs 'vertical' guide orientation.
- [x] `guide_reverse`: Functionality to reverse the order of items or the colorbar direction.

#### Phase 3: Advanced Layout & Styling
- [x] `guide_nrow` Controls for wrapping legend items into rows.
- [x] `guide_ncol`: Controls for wrapping legend items into columns.
- [x] `guide_bins`: [DEFERRED - FEATURE NOT YET IMPLEMENTED IN PLOTNINE] Not in current source build.
- [x] `guide_ticks`: [DEFERRED - FEATURE NOT YET IMPLEMENTED IN PLOTNINE] Not in current source build.

### 🎨 Viz Factory: Stats Implementation Tracker (geoms/)
- [x] Important stats are implemented in the geoms directory: We do not want to create complex stats logic / it simplifies the manifest and respect ggplot2 (R) grammar of graphics: Add this to documentaiton. (and a special rules for stats that must go into geoms directory) 

#### Phase 1: Common Statistical Summaries
- [x] `stat_count`: Calculates the number of cases at each x position (Essential for bar charts).
- [x] `stat_bin`: Bins continuous data into ranges and counts cases (Essential for histograms).
- [x] `stat_identity`: Leaves the data as is (Default for many geoms like `geom_point`).
- [x] `stat_summary`: Summarizes y values at unique x values (e.g., mean, median, min, max).

#### Phase 2: Distributional & Smoothing Stats
- [x] `stat_boxplot`: Computes the components of a standard boxplot (quartiles, whiskers, outliers).
- [x] `stat_ydensity`: Computes a 1D kernel density estimate (Essential for violin plots).
- [x] `stat_smooth`: Aids in seeing patterns in the presence of overplotting (Regression/LOESS).
- [x] `stat_density`: Computes 1D kernel density estimates for area plots.

#### Phase 3: Specialized & Comparative Stats
- [x] `stat_qq`: Calculates values for quantile-quantile plots.
- [x] `stat_ecdf`: Computes the empirical cumulative distribution function.
- [x] `stat_unique`: Removes duplicate observations (Useful for cleaning data at the plot level).
- [x] `stat_function`: Computes y values from a user-defined function across an x range.

### 🎨 Viz Factory: LAST CHECK
- [x] **FAILED VERIFICATIONS - RESOLVED:**
  - `scale_color_cmap`: Fixed - manifest updated to use continuous (y) column.
  - `facet_labeller`: Fixed - handler updated to use `setattr` for compatibility.
  - `stat_ecdf`: Fixed - `geom_step` registered in `geoms/core.py`, manifest updated.
  - `stat_function`: Fixed - `stat_function` handler evaluates string lambdas via `eval()`.
- [x] **DEFERRED CONFIRMED (NOT IN PLOTNINE BUILD):**
  - `coord_polar`: Not present in current source at `/home/evezeyl/Downloads/plotnine/`.
  - `guide_bins`: Not present in current source.
  - `guide_ticks`: Not present in current source.
- [x] Layer omission defaults implemented in `VizFactory (viz_factory.py)`:
  - `theme_bw` (default theme if none specified)
  - `coord_cartesian` (default coord if none specified)
  - `facet_null` (default facet if none specified)
  - Position & Stats: ggplot2 geom-level defaults; no VizFactory injection needed.
- [x] `bulk_debug_viz_factory_layers.py` created at `libs/viz_factory/tests/`.
- [x] Documentation updated: `developer_how_to.qmd` now documents both bulk and single runners.
- [x] Documentation updated: `visualisation_factory.qmd` and `viz_factory_rationale.qmd` updated with DEFERRED items.
- [ ] [TASK BLOCKER] USER WANTS YOU TO STOP YOUR ACTIVITIES HERE

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
