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
- **Right Panel (Audit Stack & Execution)**: The sandbox builder for Tier 3. Contains the actual `t3_recipe` stack, the `btn_revert` (to reset Tier 3 to the baseline Tier 2 blueprint), and the critical `btn_apply`.
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
- **CSS Layer**: Standard Sidebars use `#f8f9fa`. The `violet` (#f3e5f5) inherited rows and `yellow` (#fffde7) sandbox rows must strictly maintain the visual standard.
