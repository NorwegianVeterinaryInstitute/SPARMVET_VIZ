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

## Next Step — Phase 18-D: Per-Plot Wrangling Support

**Design spec:**

Add optional `pre_plot_wrangling: !include` key in the plot block of a manifest:

```yaml
analysis_groups:
  Quality Control:
    plots:
      mlst_bar:
        target_dataset: MLST_with_metadata
        pre_plot_wrangling: !include 'plots/mlst_bar_wrangling.yaml'  # optional
        spec: !include 'plots/mlst_bar.yaml'
```

**Implementation steps:**
1. Extend `_build_sibling_map` `analysis_groups` loop to register `pre_plot_wrangling` `!include` paths with `role="plot_wrangling"`.
2. Extend `_build_lineage_chain` for `plot_spec` to prepend the `pre_plot_wrangling` node when present.
3. Add `"plot_wrangling"` branch to `_handle_manifest_import` role dispatch.
4. In `lineage_component_ui`: when `pre_plot_wrangling` slot is absent, show "➕ Add plot wrangling" button.

---

## Deferred Items (do not start until 18-D complete)

- **Plot spec chain enrichment**: Walk `target_dataset` at chain-build time to prepend assembly node in `_build_lineage_chain` for `plot_spec` role. Currently chain shows only the plot node.
- **Branch selector**: One assembly → N plots; show branch tabs on Rail. Deferred to 18-F.
- **Phase 18-E**: Field Gap Analysis ("I want field X" reverse navigation).
- **Phase 18-F**: Full interactive TubeMap (Mermaid/SVG DAG with clickable nodes).

---

## Conflict Resolution

If instructions in chat conflict with this file: HALT and request `@sync`.
