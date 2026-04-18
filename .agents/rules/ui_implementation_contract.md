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

## 2. Shell Architecture (The 3-Zone Navigator)

The UI implements a high-density **3-column nested shell** to maximize screen real estate:

- **Project Navigator (Left)**: Persistent controls for project selection and agnostic filtering. Uses a Dark Grey (#c0c0c0) background.
- **Analysis Theater (Center)**: The primary workspace. Organizes analysis groups into top-level tabs, with individual plots nested inside **Sub-Tabs (navset_underline)** to prevent scrolling. Uses a Neutral Grey (#d1d1d1) background.
- **Pipeline Audit (Right)**: Persistent audit trail for Tier 2/3 transitions. Uses a Dark Grey (#c0c0c0) background.

**Grid & Maximization Logic**:
The theater manages four panes in a 2x2 grid when in **Comparison Mode**.

- **Layout Configuration**:
  - **Top-Left**: Reference Plot (T2).
  - **Bottom-Left**: Reference Data (T1/T2 Toggle).
  - **Top-Right**: Active Plot (T3 Sandbox).
  - **Bottom-Right**: Active Data (T3 Sandbox Toggle).

- **The "Minimized Tab" Behavior**:
  - When a user clicks **Maximize** on any pane (e.g., Active Data), that pane fills the entire theater.
  - The other three panes shrink into **small vertical/horizontal tabs** at the edges of the theater frame.
  - Clicking a minimized tab restores the 2x2 grid or switches the maximization to that pane.

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

## 5. The 4-Pane Theater Grid

The Theater supports three primary visual states controlled by the `theater_grid` toggle.

| **Grid State**  | **Layout Description**                                                        | **Persona Availability** |
| --------------- | ----------------------------------------------------------------------------- | ------------------------ |
| **Ref-Only**    | Full-width vertical stack: **Plot Ref** (Top) / **Table Ref** (Bottom).       | All                      |
| **Active-Only** | Full-width vertical stack: **Plot Active** (Top) / **Table Active** (Bottom). | Exploration / Dev        |
| **Comparison**  | 2x2 Grid. Left = Reference (T1/T2); Right = Active (T3 Sandbox).              | Exploration / Dev        |

**Maximization Logic:** When a user clicks "Maximize" on any pane:

1. The selected pane fills the central theater.
2. The other three panes shrink to **Minimized Tabs** (labeled icons) at the respective edges of the theater for quick one-click restoration.

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
