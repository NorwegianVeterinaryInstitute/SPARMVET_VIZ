---
trigger: always_on
deps:
  provides: [rule:ui_orchestration, rule:theatre_layout, rule:sidebar_law]
  documents: [app/handlers/home_theater.py, libs/utils/src/utils/blueprint_mapper.py]
  consumed_by: [.antigravity/knowledge/dependency_index.md]
---

## 1. UI Orchestration & Aesthetics (ADR-027–030)

- **Library Sovereignty:** UI MUST NOT duplicate logic; it MUST call libraries in `./libs/`.
- **Dynamic discovery:** Tabs and column filters MUST be derived from manifests and Polars schemas at runtime.
- **T3 = Publication Finisher (§12, ui_implementation_contract.md):** Tier 3 scope is **permanently locked** to row filters, row exclusions, column visibility, and aesthetic overrides. It is NOT a wrangling sandbox — no action-picker UI. Wrangling belongs in T1/T2 manifests.
- **T3 Recipe IS the Audit Trace:** There is no separate FILTERS.txt for T3. The T3 YAML recipe (list of RecipeNode dicts) is the complete audit trail. `aesthetic_override` nodes are stored separately as `t3_plot_overrides` but are included in the export report.
- **Two Ghost Save Slots:** (1) T1/T2 Ghost (`_autosave_assembly.json`) — written on assembly, refreshed on manifest/data change. (2) T3 Ghost (`_autosave_t3.json`) — written on every `btn_apply` AND on every panel switch away from Home.
- **State Feedback:** When a plot is "In-Calculation" (recalc ONLY applies to Tier 3 since Tiers 1/2 are immutable Parquet caches), the UI must use a dimming overlay with a "recalculating" message.

## 2. Left vs Right Panel Behaviors

- **Left Panel (Navigation & Context)**: Content is **panel-context-dependent** — the left sidebar renders different content depending on which top-level panel is active. Switching panels physically replaces the left sidebar DOM (not CSS-hide). See `ui_implementation_contract.md §11` for the full panel → sidebar content map.

  **Home mode left sidebar:**
  - **Filter Recipe Builder** (Phase 21-F): Add N filter rows `{column, op, value}`. `_pending_filters` staging → `applied_filters` committed on Apply. Affects both plots and data preview. Ops: `in`/`not_in` for discrete/categorical; `eq`/`ne`/`gt`/`ge`/`lt`/`le` for numeric. Scoped to active plot sub-tab columns only.
  - **System Tools** (persona-gated contents):
    - **Export Bundle** (`export_bundle_download`, ADR-047): Zip with plots (SVG/PNG), T1+T2 data (T3 for advanced+T3 active), YAML recipes, T3 YAML audit recipe (IS the audit trace — no separate FILTERS.txt), Quarto `.qmd` report, README.txt. Label field renamed to "Bundle label / name".
    - **Export Audit Report** (≥ `pipeline_exploration_advanced`): HTML report via Quarto — manifest SHA256 hash, auto-generated Methods section (plain English per node type), embedded figures, raw T3 recipe YAML. Second "Export PDF/DOCX" button calls Pandoc. See `ui_implementation_contract.md §12f`.
    - **Export Active Graph** (≥ `pipeline_exploration_simple` with T3 access): Single-plot export — plot file + recipe fragment. Deferred Phase 22.
    - **Metadata Ingestion** (≥ `pipeline_exploration_advanced`, `metadata_ingestion_enabled`): Upload replacement metadata TSV → MetadataValidator gate → T1 rebuild. Provenance filename recorded in bundle. Deferred Phase 22.
    - **Data Ingestion + Excel Converter** (`import_helper_enabled`): Multi-file upload with schema association; Excel sheet → TSV conversion via `ExcelHandler`. Deactivatable per deployment profile. Deferred Phase 22.
    - **Session Save / Import** (`session_management_enabled`): Named session `.json` files in Location 4; ghost save to `_autosave.json`. Multiple sessions per user (different pipeline runs). Deferred Phase 22.

  **Blueprint Architect mode left sidebar:** Manifest/component navigation (dataset pipeline selector, TubeMap node selector). No filter widgets.

  **Gallery mode left sidebar:** Focus Mode (ADR-038) — operation controls hidden; gallery search/filter only.

  **Dev Studio mode left sidebar:** TBD — deferred until Dev Studio is finalized.
- **Right Panel (The Active Blueprint Stack)**: In **Blueprint Architect** mode, the right panel is the authoritative workspace for the **Active Component Logic Stack**. In **Home** mode (post-ADR-043/ADR-044), visibility is persona-gated: hidden entirely for `pipeline_static` and `pipeline_exploration_simple`; full audit stack for ≥ `pipeline_exploration_advanced`. When hidden, the theater center column expands to fill the full width.
- **The Focus Mode (ADR-038)**: Global Navigation (Far-Left Sidebar) MUST programmatically hide "Operation" controls (Import/Session) when "Discovery" tabs (Gallery) are active to maximize screen utility and reduce cognitive load.
- **The Gatekeeper**: Modifications on the UI triggers no calculations until the user presses `btn_apply`. The apply action is locked unless every user-made recipe node contains a valid `comment_field` entry. The gatekeeper is only rendered when the right sidebar is visible (≥ `pipeline_exploration_advanced`).

## 3. Persona Reactivity Matrix (Component Masking)

The UI dynamically alters component availability based on the templates in `config/ui/templates/`. Below is the authoritative component mapping (updated ADR-043/ADR-044, 2026-04-23):

| Persona | Filters | Tier Toggle | Right Sidebar | Comparison | Export Bundle | Export Graph | Metadata Ingest | Data Ingest | Sessions |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1. pipeline-static** | Read-only, sub-tab scoped. | T1 / T2. | **Hidden**. | Hidden. | ✅ | — | — | — | — |
| **2. pipeline-exploration-simple** | Read-only, sub-tab scoped. | T1 / T2. | **Hidden**. | Hidden. | ✅ | — | — | — | — |
| **3. pipeline-exploration-advanced** | Full filter builder + T3. | T1/T2/T3. | **Visible** (Violet+Yellow). | ✅ | ✅ | ✅ | ✅ | — | ✅ |
| **4. project-independent** | Full filter + import helper. | T1/T2/T3. | **Visible** (full sandbox). | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **5. developer** | Full filter. Dev studio + Gallery. | All tiers. | **Visible** (full + registry). | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

**Persona template flags** (in `config/ui/templates/<persona>_template.yaml`):
`interactivity_enabled`, `developer_mode_enabled`, `gallery_enabled`, `comparison_mode_enabled`, `session_management_enabled`, `import_helper_enabled`, `export_bundle_enabled`, `metadata_ingestion_enabled`, `data_ingestion_enabled`.

**Data ingestion deactivation:** `data_ingestion_enabled` can also be set to `false` in the deployment profile (ADR-048) for deployments where data is always pushed automatically by a pipeline — the System Tools ingestion section is suppressed regardless of persona.

**Note on T3 for lower personas**: For personas 1 and 2, the T3 recipe silently pre-fills from T2 to protect plot formatting. The rendered output is functionally identical to T2. The right sidebar is suppressed — the layout element is excluded (not CSS-hidden) to reclaim the full screen width.

## 4. Coding Standards & Execution

- **Home Module State Object** (`home_state`): A single `reactive.Value` dict holding navigation state, filter state, T3 recipe, pending T3 nodes, and plot overrides. Full schema in `ui_implementation_contract.md §13`. Survives all panel switches. `t3_recipe` (wrangling audit nodes) and `t3_plot_overrides` (aesthetic changes per plot sub-tab) are **separate fields** within it. Changes only apply upon `btn_apply`.
- **The Pipeline Builder Scope**: `build_polars_pipeline(df, recipe)` must dynamically translate nodes. In simpler personas, this relies on basic filter mappings. In **Developer/Advanced** personas, this must proxy directly out to the unified `@register_action` registry defined in the Transformer layer to support any arbitrary Python execution payload.
- **Unified Home Theater (ADR-043)**: The "Analysis Theater / Viz" nav mode is **eliminated**. Home is the sole results mode. Manifest-defined `analysis_groups` are the primary tab structure of Home. Plot sub-tabs (`navset_underline`) are wrapped in a **collapsible accordion panel**; data preview panes are in a **separate collapsible accordion panel below**. Both default to expanded. Collapse state is user-driven and must not reset on sub-tab navigation.
- **Hierarchical Visualization**: Home MUST organize manifest-defined plots into **Sub-Tabs** (navset_underline) within their respective category tabs to prevent vertical scrolling clutter. These sub-tabs are wrapped in a collapsible accordion as per ADR-043.
- **CSS Layer (The High-Density Shell)**:
  - **Background**: Body and Theater background MUST use **Neutral Grey (#d1d1d1)** for premium white-card contrast.
  - **Sidebars**: MUST use **Dark Grey (#c0c0c0)** sidebar backgrounds for visual symmetry.
  - **Gaps**: All structural gaps (between sidebars, theater, and cards) MUST be standardized at **10px** to balance breathing room with screen utility.
  - **Density Optimization**: Navigation sidebars MUST use collapsible accordions and ultra-high-density inputs (uppercase labels, <4px margins) to minimize vertical scrolling.
  - **Alignment**: Primary module headers (e.g., "Pipeline Audit") and theater titles (e.g., "SPARMVET Home") MUST be perfectly centered via flex-alignment.
  - **Buttons**: Action buttons (e.g., "Reset Sync", "Apply") MUST use the standard **SPARMVET Blue (#0d6efd)** `btn-primary` class unless specifically designated as destructive.
  - **Nodes**: The `violet` (#f3e5f5) inherited rows and `yellow` (#fffde7) sandbox rows must strictly maintain the visual standard.
  - **ID Sanitation**: ALL major theater components MUST use dynamic IDs based on the active sidebar module (ADR-036) to ensure complete DOM clearing during module context switches.

## 5. Architectural Invariants (Gallery & Caching)

- **Gallery Isolation Boundary (TBD-03)**: The Gallery (`gallery_viewer.py`) MUST strictly operate as a static reference browser. It is explicitly forbidden from generating dynamic Polars materializations or calculating Plotnine objects at runtime.
  - The Gallery MUST serve pre-rendered `.png` assets, YAML manifests, and JSON metadata exclusively from `assets/gallery_data/`.
  - The ONLY permitted interactive functionality is the transplantation (cloning) of a pure YAML string into the Tier 3 active sandbox.
- **Hierarchical Asset Caching (TBD-02)**: The Bootloader MUST implement a single source of truth static dict for all materialized/parsed assets natively at runtime to prevent repetitive file-IO overhead.
  - Cache Hierarchy Contract: `_asset_cache[project_id][dataset_id][plot_id][asset_type]`
- **Gallery Taxonomy & Indexing (ADR-037)**: The Gallery UI MUST NOT perform direct filesystem scans or YAML parsing for filtering.
  - Filtering logic MUST rely exclusively on the pre-computed `gallery_index.json` (Pivot-Index).
  - The UI is responsible for performing set-intersections against the pivot IDs to provide zero-latency responses.
  - The index MUST be maintained via the `refresh_gallery.py` utility located in the library assets.

## 6. The Blueprint Architect Invariants (ADR-039)

The Blueprint Architect provides a "Flight Deck" for manifest design.

- **The Central Vertical Stack (The Theater)**:
  1. **Top Header**: The **Interactive TubeMap** (DAG). Must be collapsible to maximize workspace.
  2. **Central Body**: The **Live Visualization** (Plot).
  3. **Bottom Footer**: The **Live Data Glimpse** (Table).
- **The Right Sidebar (The Logic)**: Focuses exclusively on the internal transformation steps of the component selected in the Map.
- **Logic Sync**: Any modification in the Right Sidebar MUST trigger a reactive update of the Central Stack (Plot & Table) for immediate verification.
