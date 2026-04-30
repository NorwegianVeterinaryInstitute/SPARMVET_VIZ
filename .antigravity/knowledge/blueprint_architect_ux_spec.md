# Blueprint Architect — UX & Visual Specification

**Authority:** ADR-039, ADR-040  
**Last updated:** 2026-04-20 (Session 5)  
**Status:** Partially implemented — core layout DONE, TubeMap migrated to Cytoscape.js (Session 5), Interface Fields vertical layout DONE (Session 6)

---

## 1. Layout: The "Flight Deck" (3-Zone Shell)

The Blueprint Architect occupies the full central theater. It is structured as a **vertical stack** of three zones, rendered inside `wrangle_studio.py` → `render_ui()`:

```
┌─────────────────────────────────────────────────┐
│  Zone A: TubeMap (collapsible accordion)        │  ~300px fixed height
├─────────────────────────────────────────────────┤
│  Zone B: Tri-tab work area                      │  flex-grow (fills remaining)
│    Tab 1 — Focus (Logic)                        │
│    Tab 2 — Interface (Fields)                   │
│    Tab 3 — YAML (Raw Source)                    │
├─────────────────────────────────────────────────┤
│  Zone C: Permanent bottom card (50/50 split)    │  fixed height
│    Left: Plot Preview  │  Right: Live Data      │
└─────────────────────────────────────────────────┘
```

**Key invariants:**
- Zone C is **always visible** — not a tab. The plot and data table are visible simultaneously as the user edits in Zone B.
- Zone A is collapsible (accordion) so users can maximise Zone B when the TubeMap is not needed.
- The left sidebar contains the Target Blueprint Component selector and Import button (deferred for removal once TubeMap navigation is reliable).
- The right sidebar (Audit Stack) shows the Lineage Rail — the horizontal chain of nodes for the currently selected component.

---

## 2. Zone A — TubeMap Specification

### 2.1 Purpose
Primary navigation surface. Clicking any node in the DAG drives the entire UI: loads the component into Zone B, highlights the clicked node, populates the Lineage Rail in the right sidebar, and optionally materialises data for Zone C.

### 2.2 Established Visual Language (node colours)

| Role | Shape (Mermaid) | Colour | Notes |
|---|---|---|---|
| `trunk` — raw data source | `([...])` rounded rect | `#0d6efd` (Bootstrap blue) | One per `data_schemas` entry |
| `wrangle` — wrangling step | `[...]` rect | `#ffc107` (amber) | `schema_id__wrn` composite ID |
| `ref` — additional dataset | `([...])` rounded rect | `#6c757d` (grey) | `additional_datasets_schemas` |
| `meta` — metadata schema | `([...])` rounded rect | `#fd7e14` (orange) | `metadata_schema` singleton |
| `branch` — assembly | `{...}` rhombus | `#9c27b0` (purple) | `assembly_manifests` entries |
| `plot` — terminal plot | `[[...]]` stadium | `#198754` (green) | Per-plot nodes in subgraphs |
| `activeNode` overlay | dashed border | stroke `#212529` 4px | Applied on top of base class; also on `__wrn` sub-node |
| `info` — missing target | `[...]` rect | `#e3f2fd` / `#1976d2` | Warning node when `target_dataset` unset |

Plots are grouped into named **subgraphs** corresponding to `analysis_groups` keys. The subgraph label uses the group name (e.g. "Quality Control", "Results").

### 2.3 Full Chain Rule
Every schema renders as a **mini-chain**, never as a single node:
```
[Source] ──► [Wrangling] ──► {Assembly} ──► {Assembly Wrangling} ──► [[Plot]]
```
Wrangling nodes have composite IDs: `{safe_schema_id}__wrn`. Click events on `__wrn` nodes emit the parent `schema_id` (not the composite ID) so the Shiny bridge resolves correctly.

### 2.4 Click Bridge

```
TubeMap node click
  → mermaidClick(schema_id)          [JS global, defined before mermaid.initialize]
  → Shiny.setInputValue("blueprint_node_clicked", schema_id, {priority:'event'})
  → _sync_selector_from_node_click   [server.py @reactive.event]
    → reverse-lookup _component_ctx_map: safe(schema_id) == safe(entry.schema_id)
    → role priority: assembly(0) > wrangling(1) > plot_spec(2) > plot_wrangling(3) > output_fields(4) > input_fields(5)
    → ui.update_select("dataset_pipeline_selector", selected=best_rel)
    → ui.js_eval("document.getElementById('btn_import_manifest').click()")
  → _handle_manifest_import          [server.py @reactive.event]
    → Mode A (file path) or Mode B (inline schema_id)
    → sets: logic_stack, active_fields, active_component_info,
            active_upstream, active_downstream, active_lineage_chain,
            active_manifest_path, active_anchor_path (if materialisation needed)
    → regenerates TubeMap with active_node=schema_id (activeNode highlight)
```

**Critical:** `securityLevel: 'loose'` MUST be set in `mermaid.initialize()`. Without it, Mermaid 10 silently drops all `click ... call` directives.

### 2.5 Current Implementation: Cytoscape.js + dagre (Session 5 migration)

Mermaid.js was replaced with **Cytoscape.js 3.29.2** + **cytoscape-dagre 2.5.0** for proper hierarchical DAG layout with native pan/zoom/click.

- `BlueprintMapper.generate_cy_elements()` → JSON string of Cytoscape elements array
- `active_tubemap_mermaid` reactive (name kept to avoid server.py churn) stores Cytoscape JSON
- `initCyTubeMap(elementsJson, containerId)` defined in `ui.py` JS block — creates Cytoscape instance with `dagre` LR layout
- Click bridge: `cy.on('tap','node', ...) → Shiny.setInputValue('blueprint_node_clicked', schema_id)`
- Active node highlight: `border-width:3px, border-color:#212529, border-style:dashed`
- Toolbar: `cyZoomIn()`, `cyZoomOut()`, `cyFit()` global functions
- Viewport: `320px` height, `position:relative`, tooltip div `#cy_tooltip`
- CDN scripts in `ui.py`: `cytoscape@3.29.2`, `dagre@0.8.5`, `cytoscape-dagre@2.5.0`

**Node shapes by role:**
- `trunk` / `ref` / `meta`: ellipse
- `wrangle` / `plot`: round-rectangle
- `branch` (assembly): diamond

**DEFERRED:** Aesthetic refinement to tighter rail/tube look; rename 'ref' label to 'Add' (Additional Dataset).

### 2.6 Click → Interface Fields Bridge (Session 5–6)

TubeMap click drives all three Interface (Fields) panels via `_sync_selector_from_node_click`:

```
cy.tap(node)
  → Shiny.setInputValue("blueprint_node_clicked", schema_id)
  → _sync_selector_from_node_click  [server.py @reactive.event]
    → builds inc_map/ctx_map if empty (first click before manifest selector fires)
    → reverse-lookup: safe(schema_id) → best_rel via _PRIORITY dict
    → calls _do_load_component(master_path, best_rel_or_schema_id, inc_map, ctx_map) directly
    → no js_eval round-trip (previously unreliable)
```

`_do_load_component` sets: `logic_stack`, `active_fields`, `active_component_info`, `active_upstream`, `active_downstream`, `active_lineage_chain`, `active_manifest_path`, `active_anchor_path`, `active_tubemap_mermaid` (with active node highlight), `active_viz_id` (for plots).

---

## 3. Zone B Tab 1 — Focus (Logic)

**Left card — Plan & Actions:** Action selector dropdown + parameter fields (column, value, etc.) + Add Node button. Join action shows secondary dataset selector.

**Right card — Logic Stack:** Scrollable vertical list of wrangling step cards. Each card shows action name, parameters summary, optional comment field, reorder arrows, delete button. Stack can be cleared. Export-to-YAML button at bottom.

**Behaviour:** `logic_stack` reactive value drives this view. For `wrangling`/`plot_wrangling` roles, `apply_logic` is called in `processed_data_surgical` to show live preview. For other roles, the stack displays the declared steps but does not re-transform.

---

## 4. Zone B Tab 2 — Interface (Fields)

**Vertical 3-card layout** (Session 6 — was horizontal, changed to reduce horizontal scroll):

```
┌─────────────────────────────────────────────┐
│  Lineage Rail (horizontal scrollable)        │
├─────────────────────────────────────────────┤
│  Upstream Contract  (what arrives)           │  max-height: 260px, scrollable
├─────────────────────────────────────────────┤
│  Active Component   (this component)         │  max-height: 200px, scrollable
├─────────────────────────────────────────────┤
│  Downstream Contract (what leaves)           │  max-height: 260px, scrollable
└─────────────────────────────────────────────┘
```

Above the cards: the **Lineage Rail** — a horizontal scrollable chain of role-badged buttons showing the full path from raw source to plot. The active node is highlighted (filled background, bold border).

**Upstream Contract variants by role:**

| Role | Upstream content |
|---|---|
| `input_fields` | Empty ("Raw source — no upstream") |
| `wrangling` | `input_fields` from sibling file or inline dict |
| `assembly` | Accordion: one panel per ingredient showing its `output_fields` |
| `plot_spec` | `target_dataset` output resolved via `_resolve_fields_for_schema` (see §4.1 below) |
| `plot_wrangling` | Same as `plot_spec` — parent assembly/dataset `output_fields` |

### 4.1 Upstream Backtracking for Plot Nodes

For `plot_spec` and `plot_wrangling`, upstream = what physically enters the plot = `target_dataset` output. Resolution chain:

```
plot.spec.target_dataset  →  assembly.final_contract        (if declared)
                          →  assembly.output_fields (inline) (if declared)
                          →  union of assembly ingredient output_fields (if no assembly output)
                          →  each ingredient's output_fields → falls to input_fields if absent
```

**Critical:** `target_dataset` is at `plot_spec["spec"]["target_dataset"]` (under the `spec:` wrapper), NOT at `plot_spec["target_dataset"]`. Both levels must be checked.

**Implementation:** `_resolve_fields_for_schema(target_dataset_id, ctx_map, inc_map)` in `server.py` handles this recursion. For Mode B (inline manifests), the fallback also reads directly from `raw_config["assembly_manifests"][target_ds].get("output_fields")`.

**Materialization for plot preview:** `orchestrator.materialize_tier1(collection_id=target_dataset_id)` — NOT `plot_id`. The parquet is stored as `anchors/{target_dataset_id}.parquet`.

**Active Component card:** Shows `schema_id`, `role`, `schema_type`, `ingredients` list (for assembly), wrangling presence indicator. For `plot_spec` without `pre_plot_wrangling`: shows "➕ Add plot wrangling" button.

**Downstream Contract variants:**

| Role | Downstream content |
|---|---|
| `output_fields` | The fields themselves |
| `wrangling` | `output_fields` from sibling file or inline dict |
| `assembly` | Assembly `output_fields` / `final_contract` |
| `plot_spec` / `plot_wrangling` | "Plot terminal — no output schema" |

**Fields table columns:** `field` (slug), `type`, `description`. Rendered by `_parse_fields_safe` which handles Rich Dict (`{slug: {type, label, ...}}`), simple dict (`{slug: type}`), and list-of-dict formats. Legacy format triggers a warning badge.

**Fix Format button (⚙️):** Runs `normalize_manifest_fields.py` on the active file in-place, enforcing ADR-041 Rich Dict format. Shows diff count in notification.

---

## 5. Zone B Tab 3 — YAML (Raw Source)

Collapsible YAML tree rendered by `_render_yaml_tree`: Bootstrap accordion panels per key, with 🎯 Focus buttons that navigate the Rail to the matching component. Code is also shown as raw `<pre>` block with syntax highlight CSS.

---

## 6. Zone C — Permanent Bottom Card

Always visible, 50/50 horizontal split:

**Left — Plot Preview (`architect_active_plot`):**
- Renders the active plot spec using `ConfigManager(active_manifest_path).raw_config` + `active_viz_id`
- Data source: `processed_data_surgical` (surgical parquet from `active_anchor_path`)
- Falls back to `processed_data()` (base project anchor) if surgical data unavailable
- Shows spinner / "Select a plot component to preview" when `active_viz_id` is None

**Right — Live Data Glimpse (`architect_data_status_ui` + data table):**
- Shows `✅ schema_id — N rows × M cols (filename.parquet)` status line when data loaded
- Shows scrollable `DataGrid` of the first N rows
- Status message when `active_anchor_path` is empty: "Materialization pending — select a component"

**Materialization rules (when `active_anchor_path` is set):**

| Role selected | What is materialised | `apply_logic` in calc? |
|---|---|---|
| `wrangling` | Source ingredient for that schema | YES — apply current logic_stack |
| `plot_wrangling` | Parent assembly output | YES — apply wrangling steps |
| `assembly` | Full assembled output (all ingredients joined) | NO — parquet IS the output |
| `plot_spec` | Parent assembly output | NO — parquet IS the input to plot |
| `output_fields` / `input_fields` | Not materialised | N/A |

Parquets are cached in `user_sessions/anchors/{schema_id}.parquet`. If the file already exists, it is not recomputed. To force refresh: delete the file.

---

## 7. Lineage Rail (Right Sidebar)

Horizontal scrollable list rendered by `lineage_rail_ui`. Each node is a `<button>` styled with:
- Background: role colour (blue/amber/purple/green etc.) when active, light grey when inactive
- Border: `3px solid #212529` when active, `2px solid {role_colour}` when inactive
- Clicking dispatches JS event on hidden `<input id="lineage_node_rel">` → `handle_lineage_node_click` → same import flow as TubeMap click

**Rail chain contents per role:**

| Selected role | Chain shown |
|---|---|
| `wrangling` | `[input_fields?] → [wrangling★] → [assembly?] → [output_fields?]` |
| `assembly` | `[ingredient_wranglings...] → [assembly★] → [output_fields?]` |
| `plot_spec` | `[ancestor chain] → [pre_plot_wrangling?] → [plot_spec★]` |
| `plot_wrangling` | `[plot_wrangling★] → [plot_spec]` |
| `output_fields` | `[wrangling/assembly chain] → [output_fields★]` |
| inline schemas | Single node `[schema_id★]` (no file siblings to walk) |

---

## 8. Colour Palette Summary

All colours defined in `CSS_THEME` in `app/src/ui.py` and `classDef` blocks in `BlueprintMapper`:

| Element | Colour | Token |
|---|---|---|
| Page background | `#d1d1d1` | — |
| Sidebar background | `#c0c0c0` | — |
| Central theater | transparent (inherits grey) | — |
| Active buttons | `#0d6efd` | Bootstrap primary |
| Source nodes (TubeMap) | `#0d6efd` | Bootstrap primary |
| Wrangling nodes (TubeMap) | `#ffc107` | Bootstrap warning |
| Assembly nodes (TubeMap) | `#9c27b0` | Material purple |
| Plot nodes (TubeMap) | `#198754` | Bootstrap success |
| Ref/Additional nodes | `#6c757d` | Bootstrap secondary |
| Metadata node | `#fd7e14` | Bootstrap orange |
| Active node ring | `#212529` dashed 4px | Bootstrap dark |
| Accordion headers | `#a0a0a0` | — |
| Assembly breadcrumb pill | Bootstrap `info` (`#0dcaf0`) | — |
