# Phase 12-A: Comparison Theater — FINAL Plan

## Core Architecture: Position-Aware Recipe Pipeline

Tier 3 is a **fork/copy of Tier 1** with Tier 2 inherited steps **pre-filled** into the
right-panel recipe. The user then adds their own steps. The **position** of each step
in the recipe determines the transform stage it applies to:

```
Tier 1 (wide Parquet anchor)
        │
        ├─── [User steps placed ABOVE inherited Tier 2 steps]
        │     → Pre-transform: filter/select on wide-format data
        │     (e.g., exclude outliers, filter by year/country)
        │
        ├─── [Inherited Tier 2 steps — pre-filled, colored violet]
        │     → Viz transforms: long-format, aggregation
        │     (required for VizFactory — warning if removed)
        │
        ├─── [User steps placed BELOW inherited Tier 2 steps]
        │     → Post-transform: select/filter on long/aggregated data
        │     (e.g., keep only certain categories or gene names)
        │
        ▼
  VizFactory → Tier 3 Plot
```

**Apply Changes button** — the pipeline is NOT recalculated on every edit.
The user builds their recipe, then clicks **"▶ Apply"** to trigger recalculation.
This prevents UI thrashing on large datasets.

---

## Theater Layout

### Left Column — Reference Sandbox (`#f8f9fa` recessed)

| Element | Spec |
|---|---|
| `plot_reference` | Tier 2 reference plot — **never** touched by user recipe |
| `ref_tier_switch` | `Tier 1 (wide)` ↔ `Tier 2 (viz-transformed)` — reference table view only |
| `table_reference` | Read-only exploration table. Full filter/column-pick for inspection ONLY. No writes, no persistence. |
| Warning | `"⚠️ Inspection only — changes here are not saved"` |

Toggling `ref_tier_switch` lets the user inspect:
- **Tier 1** = wide format, all metadata columns accessible → "which samples are from France, 2002?"
- **Tier 2** = viz-transformed (long/aggregated) → "what does the plot actually see?"

### Right Column — Active Pane (theater white)

| Element | Spec |
|---|---|
| [plot_leaf](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/app/src/server.py#275-303) | Tier 3 plot — renders after **▶ Apply** is clicked |
| **Right Recipe Panel** | Ordered list of steps with drag-to-reorder. Inherited Tier 2 steps pre-filled (violet bg). User steps (yellow bg). |
| `view_toggle` | `Wide (Tier 1)` ↔ `Long/Aggregated (Tier 3')` — table view only, hints at filter stage |
| [table_leaf](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/app/src/server.py#309-313) | Shows wide or transformed data based on `view_toggle` |
| **▶ Apply Button** | Triggers full recipe execution → updates [plot_leaf](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/app/src/server.py#275-303) and [table_leaf](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/app/src/server.py#309-313) |

**Right Recipe Panel — Step ordering rules:**
- Steps dragged **above** inherited Tier 2 nodes → applied to Tier 1 (pre-transform)
- Steps dragged **below** inherited Tier 2 nodes → applied after viz transforms (post-transform)
- Removing an inherited Tier 2 step → `ui.modal` warning: "This may break the plot. Restore available."

---

## Comparison Mode

- **OFF (default):** Single right-column only (active pane, full width)
- **ON:** Left sandbox + Right active panes side by side
- **Persona gate:** `comparison_mode_enabled: false` in `config/ui/<persona>_template.yaml` hides the toggle entirely

---

## Proposed Changes

### Governance

#### [MODIFY] architecture_decisions.md — ADR-029a

Add: Dual-Column Theater specs, position-aware recipe rule, Apply button mandate.

#### [MODIFY] implementation_plan_master.md — Phase 12-B

Add: **"Data Safety Sandbox"** — immutable reference pane + position-aware recipe pipeline standard.

---

### app/src/ui.py

- Gated `comparison_mode` toggle (persona-configurable)
- Left: `plot_reference` + `ref_tier_switch` + `table_reference` + warning
- Right: [plot_leaf](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/app/src/server.py#275-303) + Recipe Panel (pre-filled Tier 2 nodes) + `view_toggle` + [table_leaf](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/app/src/server.py#309-313) + **▶ Apply** button

### app/src/server.py

**`tier_reference()`** — reference render (read-only, no user filters):
```python
# Shows Tier 1 OR Tier 2 based on ref_tier_switch. Never affected by user recipe.
```

**[tier3_leaf()](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/app/src/server.py#226-263)** — position-aware two-stage pipeline (triggered by Apply button):
```python
# 1. Apply user's pre-transform steps (above inherited nodes in recipe)
# 2. Apply inherited Tier 2 viz transforms (if enabled)
# 3. Apply user's post-transform steps (below inherited nodes in recipe)
# → hand to VizFactory
```

**New reactive:**
- `recipe_pending` state — tracks if unsaved changes exist → enables **▶ Apply** button
- `@reactive.event(input.btn_apply)` — triggers [tier3_leaf()](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/app/src/server.py#226-263) recalculation

---

## Verification Plan

```bash
./.venv/bin/python -m shiny run app/src/main.py --reload
```

| Test | Expected Result |
|---|---|
| Comparison OFF | Single right pane, full width |
| Comparison ON | Left (grey sandbox) + Right (white active) |
| Ref Tier 1 toggle | Reference table shows wide format; plot unchanged |
| Ref Tier 2 toggle | Reference table shows long/aggregated format; plot unchanged |
| Add pre-transform step (above Tier 2 nodes) → Apply | Tier 3 plot filters Tier 1 data first, then re-aggregates |
| Add post-transform step (below Tier 2 nodes) → Apply | Tier 3 plot filters the already-transformed data |
| Remove inherited Tier 2 node | Warning modal shown |
| Reference table filter (year=2002) | View updates; plot_leaf unchanged |
| Click ▶ Apply with no changes | No recalculation |
