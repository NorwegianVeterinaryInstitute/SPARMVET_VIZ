# Handoff — Blueprint Architect Phase 18-B (Rail click wiring) → 18-D

**Date:** 2026-04-20
**Last active agent:** @dasharch (Claude Sonnet 4.6)
**Branch:** dev

---

## What Was Done This Session

### Phase 18-A — Final Fixes

- `_build_sibling_map` hashability crash fixed: inline `{"inline": val}` dicts are no longer used as ctx dict keys. Guard `_reg_if_file()` only registers `str` rel-paths.
- Assembly role mis-classification fixed: wrangling/recipe files inside `assembly_manifests` now get `role="assembly"` (was `"wrangling"`). Verified: ST22 manifest → `{input_fields:11, output_fields:13, wrangling:10, assembly:8, plot_spec:7}`.
- `_build_schema_registry()` added: schema-ID keyed structural index, parallel to file-path-keyed `_build_sibling_map`.
- `_schema_registry: reactive.Value` wired in `_update_dataset_pipelines`.

### Phase 18-C — 3-Column Panel (COMPLETED)

- Old `input_fields_viewer_ui` / `output_fields_viewer_ui` removed.
- 7 new render outputs: `lineage_rail_ui`, `upstream_label_ui`, `lineage_upstream_ui`, `component_label_ui`, `lineage_component_ui`, `downstream_label_ui`, `lineage_downstream_ui`.
- `active_component_info`, `active_upstream`, `active_downstream`, `active_lineage_chain` reactive values in `WrangleStudio.__init__`.
- Full role dispatch in `_handle_manifest_import` Mode A for all 5 roles.
- `wrangle_studio.define_server()` call gets `get_schema_registry` and `get_includes_map` lambdas.

### Phase 18-B — Lineage Rail (PARTIAL)

- `_build_lineage_chain(selected_rel, ctx_map)` added to `server.py` (module-level).
- Rail rendered as clickable `<button>` chain; JS `onclick` → hidden `lineage_node_rel` input → `handle_lineage_node_click` effect.
- Chain populated in `_handle_manifest_import` for every load.

---

## Next Step — Immediate (Rail click → full load)

**File:** `app/modules/wrangle_studio.py`
**Function:** `handle_lineage_node_click` (~line 589)

Current state: updates selector, shows notification. Does NOT trigger `btn_import_manifest`.

Fix: use `ui.js_eval` (or `session.send_custom_message`) to programmatically click the import button after updating the selector. In Shiny for Python, the cleanest approach is:

```python
@reactive.Effect
@reactive.event(input.lineage_node_rel)
def handle_lineage_node_click():
    rel = input.lineage_node_rel()
    if not rel:
        return
    ui.update_select("dataset_pipeline_selector", selected=rel)
    # Programmatically fire the import button
    ui.js_eval("document.getElementById('btn_import_manifest').click();")
```

If `ui.js_eval` is not available in the installed Shiny version, use:
```python
session.send_custom_message("click_btn", {"id": "btn_import_manifest"})
```
with a matching JS handler in `ui.py` or a `www/` script.

**Then:** After the full click-to-load is wired, the Rail becomes fully navigable.

---

## After Rail Click Wiring — Proceed to Phase 18-D

**Phase 18-D: Per-plot wrangling support**

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

Implementation steps:
1. Extend `_build_sibling_map` `analysis_groups` loop to register `pre_plot_wrangling` !include paths with `role="plot_wrangling"`.
2. Extend `_build_lineage_chain` for `plot_spec` to prepend the `pre_plot_wrangling` node when present.
3. Add `"plot_wrangling"` branch to `_handle_manifest_import` role dispatch.
4. In `lineage_component_ui`: when `pre_plot_wrangling` slot is absent, show "➕ Add plot wrangling" button.

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

---

## Conflict Resolution

If instructions in chat conflict with this file: HALT and request `@sync`.
