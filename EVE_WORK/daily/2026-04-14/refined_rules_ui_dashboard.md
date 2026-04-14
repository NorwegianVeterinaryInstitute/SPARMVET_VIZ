---
trigger: always_on
---

## 1. UI Orchestration & Aesthetics (ADR-027–030)

- **Library Sovereignty:** UI MUST NOT duplicate logic; it MUST call libraries in `./libs/`.
- **Dynamic discovery:** Tabs and column filters MUST be derived from manifests and Polars schemas at runtime, not hardcoded.
- **Recipe Inheritance:** Tier 3 Sidebar MUST pre-fill with Tier 2 logic nodes as editable components inside a **SINGLE** stack (Violet nodes for inherited, Yellow nodes for user-added).
- **Aesthetic Lock:** Sidebars use **#f8f9fa**. Tooltips use Light Yellow/Green.
- **Panel Contrast:** Side panels (Left/Right) MUST use **#f8f9fa** to create a visual "recess" from the bright white Central Theater.
- **WrangleStudio Tooltips:** Help popups for action syntax must use a "Soft Note" aesthetic: **#fff9c4** (Light Yellow) for warnings/logic or **#e8f5e9** (Light Green) for success/usage examples.
- **Typography:** Titles must use standard Sans-Serif (Standard Dashboard font). Do not apply 'Deep Violet' branding to UI headers.
- **State Feedback:** When a plot is "In-Calculation" (re-running Tier 1 to 3), the UI must use a dimming overlay rather than a blank screen. A "recalculating" message should be visible.

## 2. The Theater Layout & Data Sandbox

- **Layout Grid Config**: The layout defaults to a 1x2 configuration (Reference mode), shifting to a full 2x2 grid (Comparison Mode) only if the active persona grants access to the Tier 3 active sandbox. If Tier 3 is restricted (e.g., pipeline-static), it remains a static 1x2 view.
- **Tab Minimization**: Maximizing a theater pane shrinks the other three into tabs at the edges for easy one-click restoration.
- **Tier 3 Bifurcation**: Effectively segregates `t3_recipe_prefill` (wide data exploration *before* T2 blueprint steps are applied) and `t3_recipe_complete` (final plotting data including T2 aggregations).
- **Column Pickers & Filtering Boundaries**: 
  - Tier 1 & Tier 2 pickers/filters are strictly visual (they do not alter underlying data logic). 
  - Tier 3 pickers/filters actually add new transformation steps (e.g. drop column) to the audit recipe when modified.

## 3. Persona Reactivity Matrix (Component Masking)

The UI dynamically alters component availability based on the active persona profile. The templates in `config/ui/templates/` MUST conform mapping exactly to the 5 primary definitions in `ui_reactivity_persona.md`:
1. **Pipeline-static**: Navigation panel disabled for other pipelines; only pre-configured Reference modes activated; Tier 3 Active Pane / Wrangling Stack fully masked/hidden.
2. **Pipeline-Exploration-simple**: Basic exploration features without access to advanced logic builders. Tier 3 is toggleable/collapsible.
3. **Pipeline-Exploration-advanced**: Advanced filtering, full active plots, and wrangling enabled; Session Management enabled.
4. **Project-independent**: Total functional independence for modifying inputs/outputs and accessing imports.
5. **Developer-mode**: Full sandbox + Schema validation / Manifest upload / Gallery interactions exposed.

## 4. Coding Standards & Mandatory Audit Gate

- **State Management**: Use a single `reactive.Value` for the `t3_recipe` list. Adding steps above a violet node applies pre-transformation; removing/adding below applies post-transformation.
- **Advanced Filtering**: The UI MUST support complex advanced filters (e.g., mathematical expressions, filtering by intervals/ranges) beyond simple dropdowns.
- **The Gatekeeper**: The `btn_apply` MUST NOT trigger recalculation unless all user-modifications to the recipe contain a mandatory valid string in the `comment_field`.
- **The Pipeline Builder**: Implement a function `build_polars_pipeline(df, recipe)` that iterates through the nodes and applies `.filter()`, `.select()`, etc., based on the node type and disabled/strikethrough state.
- **CSS Layer**: The `violet` (#f3e5f5) and `yellow` (#fffde7) classes must be strictly applied in the UI to maintain the visual contract.
