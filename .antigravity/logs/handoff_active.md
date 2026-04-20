# Handoff — Blueprint Architect Phase 18-B-fixes → Phase 18-D

**Date:** 2026-04-20 (Session 2)
**Last active agent:** @dasharch (Claude Sonnet 4.6)
**Branch:** dev

---

## What Was Done This Session (Session 2)

### Live Testing Bug Fixes (all COMPLETED)

**Issue 4 — Sidebar selector display labels** (`server.py` `_update_dataset_pipelines`):

- `display = abs_path.name` → `display = f"{ctx_entry['schema_id']} — {ctx_entry['role']}"` using sibling map.
- Fallback to `abs_path.name` when rel_path not in sibling map.

**Issue 2 — Plot spec upstream contract empty** (`server.py` `_handle_manifest_import`):

- Root cause: `target_dataset` in plot spec files (e.g. `"FastP"`) matches `data_schemas`, not `assembly_manifests`.
- Fix: `role == "plot_spec"` upstream lookup now tries (in order):
  1. `schema_type == "assembly_manifests"` + `role == "output_fields"` for `target_ds`
  2. Any `schema_type` + `role == "output_fields"` for `target_ds`
  3. Any `schema_type` + `role == "input_fields"` for `target_ds` (fallback)

**Phase 18-B — Rail click full load** (`wrangle_studio.py` `handle_lineage_node_click`):

- Added `ui.js_eval("document.getElementById('btn_import_manifest').click();")` after `ui.update_select`.
- Rail is now fully navigable.

**Issue 3 — Live View plot preview** (`wrangle_studio.py`, `server.py`):

- Added `self.active_manifest_path = reactive.Value("")` to `WrangleStudio.__init__`.
- `_handle_manifest_import` sets `wrangle_studio.active_manifest_path.set(master_path)` on every load.
- When `role == "plot_spec"`, also sets `wrangle_studio.active_viz_id.set(schema_id)`.
- `architect_active_plot` now uses `ConfigManager(active_manifest_path.get()).raw_config` for the full resolved config, replacing the broken `yaml.safe_load(active_raw_yaml)` (component fragment only).

**Issue 1 — TubeMap node click full load** (`server.py` `_sync_selector_from_node_click`):

- Added `ui.js_eval("document.getElementById('btn_import_manifest').click();")` after `ui.update_select`.

---

## Active Reactive Values Summary

### `server.py` module-level

- `_includes_map`: `{rel_path: abs_path_str}`
- `_component_ctx_map`: `{rel_path: {role, schema_id, schema_type, siblings, ingredients}}`
- `_schema_registry`: `{schema_id: {schema_type, input_fields, wrangling, output_fields, ...}}`

### `WrangleStudio` instance

- `active_component_info`: `{role, schema_id, schema_type, ingredients, wrangling}`
- `active_upstream`: `[] | list[fields] | list[{id, fields}]` (assembly accordion)
- `active_downstream`: `[] | list[fields]`
- `active_lineage_chain`: `list[{rel, schema_id, role, label, is_active}]`
- `active_manifest_path`: `str` — master manifest path (set on every import)
- `active_viz_id`: `str | None` — plot schema_id (set only when role == "plot_spec")
- `active_raw_yaml`: `str` — raw text of the loaded component file (fragment)

---

## ✅ COMPLETED — Phase 18-D: Per-Plot Wrangling Support

**Date:** 2026-04-20 (Session 4)
**Agent:** @dasharch (Claude Sonnet 4.6)

**What was implemented in `app/src/server.py`:**

1. **`_build_sibling_map`**: Restored `pre_plot_wrangling` `!include` registration.
   - `plot_spec` entry: `siblings["wrangling"] = pre_wrn_rel` (or None if absent).
   - `plot_wrangling` entry: `role="plot_wrangling"`, `siblings["wrangling"] = spec_rel`.

2. **`_build_lineage_chain`**: Restored `plot_wrangling` and `plot_spec` branches.
   - `plot_wrangling`: chain = `[plot_wrangling(active), plot_spec]`
   - `plot_spec`: chain = `[pre_plot_wrangling, plot_spec(active)]` if wrangling present, else just `[plot_spec(active)]`

3. **`_handle_manifest_import`** role dispatch: Added `elif role == "plot_wrangling":` branch.
   - Upstream: assembly `output_fields` for `target_dataset` (single-pass lookup).
   - Logic: parses `wrangling`/`recipe`/`tier1` keys from file content.
   - Downstream: empty (plot spec is terminal).

**`wrangle_studio.py` required no changes** — UI stubs for `plot_wrangling` were already present (role colors, icons, `lineage_component_ui`, `downstream_label_ui`, `btn_add_plot_wrangling`).

**Manifest support:**
```yaml
analysis_groups:
  Quality Control:
    plots:
      mlst_bar:
        target_dataset: MLST_with_metadata
        pre_plot_wrangling: !include 'plots/mlst_bar_wrangling.yaml'  # optional
        spec: !include 'plots/mlst_bar.yaml'
```

**All 4 implementation steps DONE.** (Step 4 — `lineage_component_ui` button — was already present in `wrangle_studio.py`.)

---

## ✅ COMPLETED — Phase 18-F: Full Clickable TubeMap

**Date:** 2026-04-20 (Session 4 continued)
**Agent:** @dasharch (Claude Sonnet 4.6)

### Root Cause (why TubeMap clicks did nothing)

Two bugs:

**Bug 1 — Plot nodes had no `click` directives** (`libs/utils/src/utils/blueprint_mapper.py`):
Plot nodes are added to `subgraphs` dict (not `self.nodes`), so the old click-directive loop (iterating `self.nodes`) skipped all plots. Added `_clickable: list` populated alongside each node section (trunk, ref, meta, branch, **and plot**). Click directive loop now iterates `_clickable`.

**Bug 2 — ID mismatch: safe_schema_id ≠ rel_path** (`app/src/server.py` `_sync_selector_from_node_click`):
TubeMap emits node IDs as `safe_schema_id` (e.g. `FastP`, `AR1_Assembly`, `mlst_bar`). The selector `dataset_pipeline_selector` uses `rel_path` strings (e.g. `schemas/fastp_wrangling.yaml`). The old code tried `ui.update_select(..., selected=node_id)` directly → no match → nothing loaded.

**Fix:** Reverse-lookup `_component_ctx_map` for entries where `schema_id.replace(" ","_").replace("-","_") == node_id`. Pick best `rel_path` by role priority: assembly → wrangling → plot_spec → plot_wrangling → output_fields → input_fields.

### Files Changed
- `libs/utils/src/utils/blueprint_mapper.py` — `_clickable` list, click directives cover all node types
- `app/src/server.py` — `_sync_selector_from_node_click` rewritten with schema_id→rel_path bridge

---

## ✅ COMPLETED — Session 5: TubeMap Reactivity, Assembly Data, Zoom/Pan

**Files changed:** `app/src/server.py`, `app/modules/wrangle_studio.py`, `app/src/ui.py`

### Fixes

1. **Assembly role "category column missing" error** (`processed_data_surgical` in `wrangle_studio.py`):
   - Root cause: `apply_logic` was applying the assembly's recipe steps on top of the already-assembled parquet.
   - Fix: Only apply `logic_stack` when `active_component_info.role` is `"wrangling"` or `"plot_wrangling"`. For `assembly`, `plot_spec`, etc., serve the parquet as-is.

2. **Assembly role doesn't show Live Data Glimpse** (`server.py` Mode A `assembly` handler):
   - Root cause: Assembly role handler never called `materialize_tier1` or set `active_anchor_path`.
   - Fix: Added materialization block to assembly role (same as plot_spec pattern).

3. **Assembly inline ingredient fields** (`server.py` Mode A `assembly` handler):
   - Added inline sentinel fallback for ingredient field lookup (when no `!include` files).

4. **Mode B (inline manifests) missing all reactive state** (`server.py`):
   - Added: `active_component_info`, `active_upstream`, `active_downstream`, lineage chain, TubeMap highlight, assembly materialization.
   - Rich field dicts (not just key lists) passed to `active_upstream`/`active_downstream` for type display.

5. **TubeMap zoom/pan** (`ui.py`, `wrangle_studio.py`):
   - Added `svg-pan-zoom@3.6.1` from CDN.
   - `initTubeMapPanZoom()` called after mermaid render (via `shiny:visualchange` event + 300ms delay and inline `<script>` tag per render).
   - Zoom controls toolbar (＋ / － / ⊡ fit) added above TubeMap viewport.
   - Viewport height: 300px fixed, `overflow: hidden` — pan/zoom handles navigation.

## Next Steps

- **Plot spec chain enrichment**: Walk `target_dataset` at chain-build time to prepend assembly node in `_build_lineage_chain` for `plot_spec` role.
- **Phase 18-E**: Field Gap Analysis ("I want field X" reverse navigation).

---

---

## Session 3 — 2026-04-20 (Unified Manifest Standard)

**Last active agent:** @dasharch (Claude Sonnet 4.6)
**Session focus:** ADR-041 Implementation (Structural Hygiene & Normalizer Upgrade)

### Accomplishments

1. **ADR-041 (Unified Manifest Standard)**:
    - Formally registered the "Keyed-Schema & Ordered-Logic" standard.
    - Fields (`input_fields`, `output_fields`) **MUST** follow the **Rich Dictionary** format (`slug: {props}`).
    - Logic (`wrangling`) **MUST** follow the **Tiered Sequential List** format (`tier1: [...]`).
2. **Structural Hygiene**:
    - **Flattened fragments**: Removed redundant `input_fields:`/`output_fields:` top-level keys from included YAML files (e.g., `Detailed_summary_input_fields.yaml`, `Quality_metrics_input_fields.yaml`) to prevent logic unnesting issues.
    - **README created**: Added the authoritative `config/manifests/README.md` documenting these choices.
3. **Normalizer Upgrade**:
    - Rewrote **`app/assets/normalize_manifest_fields.py`** to enforce ADR-041.
    - Added **Fragment Unwrapping**: Automatically strips redundant anchoring headers on save.
    - Added **Polymorphic Mapping**: Handles legacy list-of-dicts, simple `{col: type}`, and rich `{col: {props}}` conversions.
    - Added **Tier Enforcement**: Wraps flat wrangling lists into `tier1/tier2` structures.

### Impact on Blueprint Architect

The "Fix Format" (⚙️) button in Wrangle Studio is now fully compliant with the backend Polars engines. Contract viewers and Field tables should now be stable across all manifest types.

---

## Conflict Resolution

If instructions in chat conflict with this file: HALT and request `@sync`.

### Handoff: 2026-03-07 @dasharch
**State**: Pipeline Assemblies fully stabilized and verified against ST22 master manifest.
**Accomplishments**:
- Resolved the 'bool' attribute error in DataAssembler/DataWrangler caused by unquoted YAML 'on' reserved word. The codebase is now resilient to boolean keys in recipes (ADR-042).
- Fixed recode_values type-safety by adding defensive String casting.
- Corrected case-sensitivity and contract mismatches in the AR1 assembly.
- Enhanced the assembly debugger to auto-resolve original_name → alias mappings in contract guards.
**Status**: ALL 3 major assemblies in '1_test_data_ST22_dummy.yaml' materialize successfully. Evidence logs in 'tmp/assembler_full_run_v5.log'.
**Next Steps**: Proceed with Phase 18-E/F (Reverse Lineage & Interactive TubeMap) or Phase 12-B (Position-Aware Sandbox Controls).
