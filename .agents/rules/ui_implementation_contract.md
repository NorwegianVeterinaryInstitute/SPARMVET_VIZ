**Status:** FINALIZED / ARCHITECTURAL LOCK

# UI Implementation contract

## 1. The Tier 3 "Branching & Blueprint" Logic

Tier 3 is a sandbox branch of Tier 1. It pre-populates by copying the Tier 2 "Blueprint" recipe.

- **Node Inheritance**: Copied T2 nodes are **Violet** (#f3e5f5). New user nodes are **Yellow** (#fffde7).
- **Position Awareness**:
  - Nodes dragged **ABOVE** Violet nodes = Pre-transform (Wide Data/T1 filters).
  - Nodes dragged **BELOW** Violet nodes = Post-transform (Long Data/T2 filters).
- **The Deletion & Deactivation Protocol**:
  - **Disable (Strikethrough)**: A "Power" icon allows the user to toggle a node off. The node remains in the UI with a strikethrough effect but is ignored by the Polars engine.
  - **Trash (Permanent)**: A trash icon allows for removal. If the node is **Violet**, a modal triggers: _"CRITICAL: Removing a blueprint step may break the intended visualization. Are you sure?"_

- **The Revert Protocol**: The **btn_revert** performs a **Full Wipe**. It clears all user nodes and restores the Tier 3 stack to the exact state of the Tier 2 blueprint.
- **Direct Pass-Through**: If the T2 manifest contains zero transformation steps (T2=T1), the T3 recipe starts **Empty**.

## 2. Shell Architecture (The 3-Zone Navigator) — Updated ADR-043/ADR-044 (2026-04-23)

The UI implements a high-density **3-column nested shell** to maximize screen real estate. The right column (Pipeline Audit) is **persona-gated** and suppressed entirely for lower personas (see ADR-044):

- **Project Navigator (Left)**: Persistent controls for project selection and **context-reactive filter widgets** (scoped to the active plot sub-tab's `plot_spec` aesthetics). Uses a Dark Grey (#c0c0c0) background.
- **Home Theater (Center)**: The primary workspace. Structure (post-ADR-043):
  - Top-level tabs are **exclusively** driven by manifest `analysis_groups` — no hardcoded tabs (Inspector removed).
  - Each group tab contains `navset_underline` sub-tabs (one per declared plot), wrapped in a **collapsible accordion panel**.
  - A **separate collapsible accordion panel** below shows the data preview (T1/T2 table or T3 sandbox table).
  - A **Tier Toggle** radio-button strip (T1 / T2 / T3-Wrangle / T3-Plot, persona-gated) controls which tier is displayed.
  - Uses a Neutral Grey (#d1d1d1) background.
- **Pipeline Audit (Right)**: Audit trail for T2 blueprint and T3 sandbox transitions. **Visible only for ≥ `pipeline_exploration_advanced`**. When hidden, the theater column expands to fill the full layout width — the layout element itself is excluded, not merely hidden via CSS. Uses a Dark Grey (#c0c0c0) background.

**Manifest-Driven Tab Rule**: Home tabs and sub-tabs MUST derive exclusively from `analysis_groups` in the active manifest. No hardcoded tab names or fallback tabs are permitted (ADR-003/ADR-004 compliance).

**Tier Toggle Strip** (replaces `ref_tier_switch` + `view_toggle`):

| Button | Plot Pane | Data Pane | Persona Gate |
|---|---|---|---|
| **T1 Raw** | T2 Reference Plot (read-only) | T1 Anchor table (read-only) | All |
| **T2 Reference** | T2 Reference Plot (read-only) | T2 Branch table (read-only) | All |
| **T3 Wrangling** | T3 Active Plot (Apply-gated) | T3 post-wrangling table (sandbox) | ≥ `pipeline_exploration_advanced` |
| **T3 Plot** | T3 Active Plot (Apply-gated) | T3 post-plot data slice | ≥ `pipeline_exploration_advanced` |

**Comparison Mode** (Option A — Separate Toggle, Persona-Gated, ≥ `pipeline_exploration_advanced`):

- When **ON**: theater splits into a 2-column layout — left = T1/T2 reference (per Tier Toggle), right = T3 Active.
- When **OFF**: single-pane view driven by the Tier Toggle alone.
- Replaces the previous `is_comparison` + `is_triple` flag system.

**Collapsibility Rules**:

- Plot accordion panel: default **expanded**. User-collapsible. Collapse state MUST persist across sub-tab navigation.
- Data accordion panel: default **expanded**. User-collapsible. Collapse state MUST persist across sub-tab navigation.
- Column picker (T3 sandbox): MUST span `width: 100%`, `flex: 1 1 100%`. MUST NOT wrap to multiple rows.

## 3. The Mandatory Audit Gatekeeper (The Gate)

Reactivity in the Active Leaf (Right side) is strictly gated by documentation to ensure scientific reproducibility

- **Logic**: Every user action (Filter, Column Drop, Node Addition in Tier 3) generates a node that **MUST** have a comment.
- **Comment Mandate**: Every Yellow node (and modified Violet node) MUST have a non-empty string in its `comment_field`.
- **Execution Rule**: The **btn_apply** state is disabled if:
 	- **Disabled (Grey)**:
  1. No changes detected/made OR comments are missing (`recipe_pending == False`).
  2. Any node in the stack (excluding disabled ones / and ones inherited by tier 2) has an empty comment field.  
  - **Active (Orange/Green)**: Changes detected AND all nodes have comments.
- **Calculation Scope**: Clicking **btn_apply** executes the 3-stage Polars pipeline and updates only the **Active Leaf** (Right) panes.
- **Visualization**: Until **btn_apply** is pressed, the **Active Plot** remains in a "Pending" state (e.g., blurred or overlayed with an orange "Recalculate" badge).

## 4. Interaction & Event Mapping

| **UI Event**                 | **Resulting Action**               | **Audit Entry**         |
| ---------------------------- | ---------------------------------- | ----------------------- |
| **Brush on Active T3 Plot**     | Filter rows in T3 data.            | Automatic Yellow Node   |
| **Col Drop in Active T3 Table** | `df.drop_columns()` in T3.         | Automatic Yellow Node   |
| **(Advanced Filter) in active T3 Table**        | Filter cols in T3 data. | Automatic Yellow Node   |
| **Drag Node**                | Reorder Polars operation sequence. | Update `recipe_pending` |
| **Ref Table Filter** in Tier 1 or Tier 2 Table         | Visual-only filter for inspection. | **NONE** (Transient)    |
| **Ref Table Drop**  in Tier 1 or Tier 2 Table              | Visual-only drop for inspection. | **NONE** (Transient) |                             |                                    |                         |

## 5. The Theater Layout Model (Updated ADR-043, 2026-04-23)

The theater layout is controlled by two independent controls: the **Tier Toggle** and **Comparison Mode**.

**Single-Pane Mode** (Comparison Mode OFF — all personas):

| Tier Toggle State | Plot Area | Data Area |
|---|---|---|
| T1 Raw | T2 Reference Plot (read-only) | T1 Anchor table (read-only, collapsible) |
| T2 Reference | T2 Reference Plot (read-only) | T2 Branch table (read-only, collapsible) |
| T3 Wrangling* | T3 Active Plot (Apply-gated) | T3 wrangling table (sandbox, collapsible) |
| T3 Plot* | T3 Active Plot (Apply-gated) | T3 plot slice table (sandbox, collapsible) |

*T3 states hidden for personas < `pipeline_exploration_advanced`.

**Comparison Mode** (ON — ≥ `pipeline_exploration_advanced`):

```
┌──────────────────────┬──────────────────────┐
│  T2 Reference Plot   │  T3 Active Plot       │  ← Plot accordion (collapsible)
├──────────────────────┼──────────────────────┤
│  T1/T2 Data (R/O)   │  T3 Sandbox Data      │  ← Data accordion (collapsible)
└──────────────────────┴──────────────────────┘
```

- Left column tier (T1 or T2) is driven by the Tier Toggle.
- Both plot and data rows are independently collapsible via accordion panels.
- The previous `theater_grid` toggle, `btn_max_plot`, `btn_max_table`, and `btn_reset_theater` controls are **removed** (superseded by this model).

## 6. Component Interaction Matrix

|**Zone**|**ID**|**Reactive Behavior**|
|---|---|---|
|**Table Ref**|`table_ref`|**Visual Only**: Filtering here updates the table view but creates NO audit nodes and does NOT trigger the Apply button.|
|**Table Active**|`table_active`|**Recipe Driver**: "Brush" events or column de-selections automatically generate a new **Yellow Node** in the Audit Stack.|
|**Audit Stack**|`audit_stack`|**Order Matters**: Drag-and-drop reordering of nodes marks `recipe_pending = True`.|

## 7. Session Management vs. Global Export

To ensure a clean separation between "Working State" and "Final Provenance," the UI distinguishes between these two actions:

- **Session Save/Import (Left Sidebar):**
  - **Function:** Persists the current `t3_recipe`, all `comment_fields`, and the `theater_grid` layout state.
  - **Format:** Lightweight `.json` stored in `./.antigravity/sessions/`.
  - **Use Case:** A user is halfway through a complex wrangling session and needs to resume tomorrow.
- **Global Export (Right Sidebar):**
  - **Function:** Generates the full scientific artifact (Plot + Parquet + Audit PDF + Manifest).
  - **Format:** Versioned `.zip` for external sharing.
  
# UI configuration dependencies

## Save locations

Defined in connector manifests:  `config/connectors/<dir>/<name>.yaml` (for local testing use `config/connectors/local/local_connector.yaml` )

## Persona

Defined in ui manifests: `config/ui/<dir>/<name>.yaml` (for local testing use: `config/ui/templates/<selected_persona.yaml`)

## User preferences [Implementation defered]

Saving location defined in connector manifests (Location 4, name user-preferences.yaml) (for local testing use:  
`config/user_preferences/template.yaml`)

Overwrite other settings (priority rule)
Not implemented yet
