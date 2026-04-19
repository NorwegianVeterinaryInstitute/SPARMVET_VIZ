---
trigger: always_on
---

## 1. UI Orchestration & Aesthetics (ADR-027–030)

- **Library Sovereignty:** UI MUST NOT duplicate logic; it MUST call libraries in `./libs/`.
- **Dynamic discovery:** Tabs and column filters MUST be derived from manifests and Polars schemas at runtime.
- **Recipe Inheritance:** Tier 3 Sidebar MUST pre-fill with Tier 2 logic nodes as editable components inside a **SINGLE** stack.
- **State Feedback:** When a plot is "In-Calculation" (recalc ONLY applies to Tier 3 since Tiers 1/2 are immutable Parquet caches), the UI must use a dimming overlay with a "recalculating" message.

## 2. Left vs Right Panel Behaviors

- **Left Panel (Navigation & Context)**: Contains Project/Persona selectors, Import Helpers, Session Management, and Global Export. This defines the user's high-level workflow state and interacts heavily with system storage.
- **Right Panel (The Active Blueprint Stack)**: In **Blueprint Architect** mode, the right panel is the authoritative workspace for the **Active Component Logic Stack**. It displays the atomic transformation nodes for the component currently selected in the TubeMap. In **Home/Viz** mode, it retains its role as the Tier 3 Audit Stack.
- **The Focus Mode (ADR-038)**: Global Navigation (Far-Left Sidebar) MUST programmatically hide "Operation" controls (Import/Session) when "Discovery" tabs (Gallery) are active to maximize screen utility and reduce cognitive load.
- **The Gatekeeper**: Modifications on the UI triggers no calculations until the user presses `btn_apply`. The apply action is locked unless every user-made recipe node contains a valid `comment_field` entry.

## 3. Persona Reactivity Matrix (Component Masking)

The UI dynamically alters component availability based on the templates in `config/ui/templates/`. Below is the authoritative component mapping:

| Persona Profile | Left Panel Elements | Tier 3 (Right Panel) / App UI | Advanced Filters / Registry |
| :--- | :--- | :--- | :--- |
| **1. Pipeline-static** | Only basic loading & export allowed. | Fully Hidden / Disabled. View is locked to 1x2 grid (Ref modes only). | None |
| **2. Pipeline-Exploration-simple** | Project loader, basic Session. | Tier 3 is toggleable/collapsible. Revert enabled. | Basic schema pickers and simple dropdown filters. |
| **3. Pipeline-Exploration-advanced** | Standard left panel features. | Full active plotting, Tier 3 recipe wrangling enabled. | Includes Mathematical Expressions & Interval ranges. |
| **4. Project-independent** | Full Nav + External Import helper. | Full active plotting + Sandbox. | Same as advanced. |
| **5. Developer-mode** | Dev studio mode, Gallery browser. | Full sandbox exposed. | Complete access to every `@register_action` in the codebase. |

## 4. Coding Standards & Execution

- **Transient Tier 3**: `t3_recipe` exists as a `reactive.Value`. Changes only apply upon `btn_apply`.
- **The Pipeline Builder Scope**: `build_polars_pipeline(df, recipe)` must dynamically translate nodes. In simpler personas, this relies on basic filter mappings. In **Developer/Advanced** personas, this must proxy directly out to the unified `@register_action` registry defined in the Transformer layer to support any arbitrary Python execution payload.
- **Hierarchical Visualization**: Analysis Theater MUST organize manifest-defined plots into **Sub-Tabs** (navset_underline) within their respective category tabs to prevent vertical scrolling clutter.
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
