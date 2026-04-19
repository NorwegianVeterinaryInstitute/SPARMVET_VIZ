# Handoff — Blueprint Architect Phase 18-A → 18-B

**Date:** 2026-04-19
**Last active agent:** @dasharch (Claude Sonnet 4.6)
**Branch:** dev

---

## What Was Done This Session

### Completed
- `app/assets/__init__.py` created (package registration).
- `app/assets/normalize_manifest_fields.py` moved from `assets/scripts/`; importable `normalize_file()` API; rich dict format fix applied.
- `wrangle_studio.py` — `_parse_fields_safe` fixed for rich `{col: {type, label}}` dict format.
- `server.py` — added `_build_sibling_map()`, `_load_fields_file()`, `_component_ctx_map`, role-aware field loading in `_handle_manifest_import`, `_handle_normalize_fields` effect.
- **ADR-040** written in `.antigravity/knowledge/architecture_decisions.md` — full design for Bidirectional Lineage Rail.
- **tasks.md** updated — Phase 18 fully decomposed into sub-phases 18-A through 18-F.
- App verified running on port 8081.

### Key design consensus with user (read ADR-040 in full)
- Interface (Fields) tab → replaced by Lineage Rail + 3-column panel (Upstream / Active / Downstream).
- Reverse navigation: start from plot, trace backwards to find where a missing field needs to be added.
- Per-plot wrangling: new optional `pre_plot_wrangling:` key in plot block.
- Assembly upstream: multi-ingredient accordion (no fake unified input schema).

---

## Next Step — Exact Entry Point

**File:** `app/src/server.py`
**Function:** `_build_sibling_map()`
**Task:** Extend to capture two more fields per block:
1. `ingredients` list from assembly blocks → `[{"dataset_id": "FastP"}, ...]` → store as `"ingredients": ["FastP", "metadata_schema", ...]` in the context entry.
2. `target_dataset` from plot spec blocks (inside `analysis_groups` → `plots` → `spec` → `target_dataset`) — **note:** plot specs are !include files so `target_dataset` is inside the resolved file, not the master YAML. May need to read each plot spec file separately.

**Then:** Update `_handle_manifest_import` for:
- `schema_type == "assembly_manifests"` + `role == "wrangling"` → left panel shows ingredients list rendered as info, not a field table.
- `role == "plot_spec"` → left panel shows parent assembly's `final_contract` fields (resolve via `target_dataset` from plot spec file content).

**Reference files:**
- `config/manifests/pipelines/1_test_data_ST22_dummy.yaml` — best test manifest (has multiple assemblies, plots with `target_dataset`, branching).
- `config/manifests/pipelines/1_test_data_ST22_dummy/plots/FastP_reads_horizontal_barplot.yaml` — example plot spec with `target_dataset: "QC_Reads_Anchor"`.
- `.antigravity/tasks/tasks.md` — Phase 18-A remaining tasks listed explicitly.

---

## Active Reactive Values in server.py (for context)
- `_includes_map`: `{rel_path: abs_path_str}` — all !include files in active manifest.
- `_component_ctx_map`: `{rel_path: {role, schema_id, schema_type, siblings: {input_fields, output_fields, wrangling}}}` — built by `_build_sibling_map`.
- `wrangle_studio.active_fields`: `{"input": fields_dict_or_list, "output": fields_dict_or_list}` — drives the Interface (Fields) tab.

## Conflict Resolution
If instructions in chat conflict with this file: HALT and request `@sync`.
