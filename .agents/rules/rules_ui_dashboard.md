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
- **Recipe Inheritance:** Tier 3 Sidebar MUST pre-fill with Tier 2 logic nodes as editable components inside a **SINGLE** stack.
- **State Feedback:** When a plot is "In-Calculation" (recalc ONLY applies to Tier 3 since Tiers 1/2 are immutable Parquet caches), the UI must use a dimming overlay with a "recalculating" message.

## 2. Left vs Right Panel Behaviors

- **Left Panel (Navigation & Context)**: Contains Project/Persona selectors, Import Helpers, **Filter Recipe Builder** (Phase 21-F), **System Tools** (Export Bundle — ADR-047, Phase 21-I), and Session Management. This defines the user's high-level workflow state.
  - **Filter Recipe Builder**: Add N filter rows `{column, op, value}`. `_pending_filters` staging → `applied_filters` committed on Apply. Affects both plots and data preview. Ops: `in`/`not_in` for discrete/categorical; `eq`/`ne`/`gt`/`ge`/`lt`/`le` for numeric.
  - **Export Bundle** (`export_bundle_download`): Zip with plots (SVG/PNG), T1+T2 data (T3 for advanced+T3 active), YAML recipes, Quarto `.qmd` report, FILTERS.txt (No Trace No Export), README.txt.
  - **Filter widgets** are always context-reactive to the active sub-tab (see ADR-043): when the user navigates to a different plot sub-tab, the left panel regenerates filters scoped to that plot's declared `plot_spec` aesthetics only — never the full schema.
- **Right Panel (The Active Blueprint Stack)**: In **Blueprint Architect** mode, the right panel is the authoritative workspace for the **Active Component Logic Stack**. In **Home** mode (post-ADR-043/ADR-044), visibility is persona-gated: hidden entirely for `pipeline_static` and `pipeline_exploration_simple`; full audit stack for ≥ `pipeline_exploration_advanced`. When hidden, the theater center column expands to fill the full width.
- **The Focus Mode (ADR-038)**: Global Navigation (Far-Left Sidebar) MUST programmatically hide "Operation" controls (Import/Session) when "Discovery" tabs (Gallery) are active to maximize screen utility and reduce cognitive load.
- **The Gatekeeper**: Modifications on the UI triggers no calculations until the user presses `btn_apply`. The apply action is locked unless every user-made recipe node contains a valid `comment_field` entry. The gatekeeper is only rendered when the right sidebar is visible (≥ `pipeline_exploration_advanced`).

## 3. Persona Reactivity Matrix (Component Masking)

The UI dynamically alters component availability based on the templates in `config/ui/templates/`. Below is the authoritative component mapping (updated ADR-043/ADR-044, 2026-04-23):

| Persona Profile | Left Panel Filters | Tier Toggle Options | Right Sidebar (Audit Stack) | Comparison Mode |
| :--- | :--- | :--- | :--- | :--- |
| **1. Pipeline-static** | Context-reactive to active sub-tab (read-only). | T1 / T2 only. | **Hidden** (theater expands full width). | Hidden. |
| **2. Pipeline-Exploration-simple** | Context-reactive to active sub-tab (read-only). | T1 / T2 only. | **Hidden** (theater expands full width). | Hidden. |
| **3. Pipeline-Exploration-advanced** | Context-reactive to active sub-tab + T3 sandbox filters. | T1 / T2 / T3-Wrangle / T3-Plot. | **Visible**: Violet (T2 blueprint) + Yellow (T3 sandbox) nodes. | Available. |
| **4. Project-independent** | Full filter access + External Import helper. | T1 / T2 / T3-Wrangle / T3-Plot. | **Visible**: Full sandbox + audit trail. | Available. |
| **5. Developer-mode** | Full filter access. Dev studio + Gallery browser. | All tiers. | **Visible**: Full sandbox + complete `@register_action` registry. | Available. |

**Note on T3 for lower personas**: For personas 1 and 2, the T3 recipe silently pre-fills from T2 to protect plot formatting. The rendered output is functionally identical to T2. There is nothing for the user to inspect or act on, so the right sidebar is suppressed (not merely hidden with CSS — the layout element itself must be excluded to reclaim the screen column).

## 4. Coding Standards & Execution

- **Transient Tier 3**: `t3_recipe` exists as a `reactive.Value`. Changes only apply upon `btn_apply`.
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
