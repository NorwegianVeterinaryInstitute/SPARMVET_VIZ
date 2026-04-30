### 🎨 The "High Theater" Layout Specifications

The layout will be split into two primary functional columns within the **Central Theater**:

|**Feature**|**Left Column: The Reference**|**Right Column: The Active Leaf**|
|---|---|---|
|**Top (Plot)**|**Tier 2 Plot**: Shows the "Gold Standard" view with all inherited branch logic applied.|**Tier 3 Plot**: Reacts instantly to UI filters and outlier selections.|
|**Middle (Toggle)**|**Data Tier Switch**: Toggle between **Tier 1 (Raw)** and **Tier 2 (Summarized)**.|**Inheritance Switch**: Toggle "Apply Tier 2 Formatting" (Long-format logic).|
|**Bottom (Table)**|**Immutable Inspection**: Scrollable, filterable table. Label: _View-only: For inspection and PK discovery._.|**Wrangle Studio Active**: The interactive table where selections directly drive the Tier 3 Plot.|

---

### 🛡️ Implementation Strategy: Protecting the Plot Logic

To ensure that user filters in **Tier 3** do not "break" the plot (e.g., by removing columns required for the Plotnine mapping), we will implement **Predicate Pushdown** that only affects the _rows_ and _non-essential columns_, while locking the aesthetic mappings defined in the manifest.

---

### 🚀 High-Precision Prompt for @dasharch

Copy and paste this into the IDE to execute the refined **Phase 12-A** layout:

Plaintext

--> added the plan for implementation


Summary from implementation :
## Phase 12-A: Comparison Theater — MATERIALIZED

All changes are in. Here's the evidence loop summary:

### Changes Applied

|File|What Changed|
|---|---|
|`architecture_decisions.md` (ADR-029a)|Full Comparison Theater spec added: dual-column layout, position-aware recipe rules, Apply button mandate, reference pane constraint|
|`implementation_plan_master.md`|Phase 12-A updated (active), Phase 12-B "Data Safety Sandbox" added with 3 formal tasks|
|`app/src/ui.py`|New CSS (`.reference-pane`, `.active-pane`, `.apply-btn-container`, `.recipe-pending-badge`); theater header now routes comparison toggle through `output_ui("comparison_mode_toggle_ui")`; `dynamic_tabs` builds dual-column layout when comparison_mode is ON|
|`app/src/server.py`|`_safe_input`, `_apply_tier2_transforms` helpers; `tier_reference()` reactive (read-only sandbox, never touched by user recipe); corrected `tier3_leaf()` with `@reactive.event(input.btn_apply)` gate + position-aware 3-stage pipeline; `recipe_pending` + `snapshot_recipe` state; `plot_reference`, `table_reference`, `recipe_pending_badge_ui` render outputs|

### Key Architecture Notes for @verify

1. **`tier3_leaf()` is gated by `btn_apply`** — no recalculation on every edit
2. **`tier_reference()` is strictly decoupled** — zero dependency on user recipe or sidebar filters
3. **`_apply_tier2_transforms()`** is currently a stub (identity) — the real dispatch to transformer library is Phase 12-B work
4. **Persona gate**: Comparison Mode toggle only appears if `bootloader.is_enabled("comparison_mode_enabled")` returns True
