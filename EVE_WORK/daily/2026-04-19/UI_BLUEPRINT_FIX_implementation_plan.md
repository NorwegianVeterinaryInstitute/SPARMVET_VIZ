# Blueprint Architect — Stabilization & Enhancement Plan (v3 FINAL)

> [!CAUTION]
> **Step-by-step execution mandatory.** Previous sessions broke Gallery by doing broad refactors.
> Each bug fix will be applied and boot-tested independently before moving to the next.

---

## Bug #1 (CRITICAL): `UnboundLocalError` on Boot

**Root cause:** [tier3_leaf()](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/app/src/server.py#101-142) calls `wrangle_studio.apply_logic(lf)` but captures that name at
decorator time, before `wrangle_studio` is instantiated.

**Fix:** Remove `wrangle_studio.apply_logic(lf)` from [tier3_leaf](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/app/src/server.py#101-142). The Architect's preview pipeline
and the main Theater's Tier 3 pipeline are **independent**. [tier3_leaf](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/app/src/server.py#101-142) applies
`snapshot_recipe` only — no cross-dependency.

**Files:** [app/src/server.py](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/app/src/server.py) — surgical 3-line removal.

---

## Bug #2: Schema Viewer Crash

**Root cause:** `pl.DataFrame(fields)` crashes when [input_fields](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/app/modules/wrangle_studio.py#344-353) is a `{col: type}` dict.

**Fix (two-part):**

1. **Defensive parser** `_parse_fields_safe(fields)` handles both formats → `[{"field", "type"}]`.
2. **Advisory banner** shown when dict format detected:
   > "⚠️ Advisory: [input_fields](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/app/modules/wrangle_studio.py#344-353) should be a list of `{name, dtype, description}` objects.
   > Run `normalize_manifest_fields.py` to auto-convert."

**New utility script:** `assets/scripts/normalize_manifest_fields.py`
- CLI: `python normalize_manifest_fields.py --manifest path/to/manifest.yaml [--dry-run]`
- Reads any manifest, finds all [input_fields](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/app/modules/wrangle_studio.py#344-353)/[output_fields](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/app/modules/wrangle_studio.py#354-362) dict entries, converts to list format.
- Prints a diff; writes only if `--write` flag set (dry-run safe by default).

**Files:** [app/modules/wrangle_studio.py](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/app/modules/wrangle_studio.py), `assets/scripts/normalize_manifest_fields.py` [NEW]

---

## Bug #3: TubeMap — Wrong / Missing Plot→Assembly Edges

**Root cause:** [BlueprintMapper](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/libs/utils/src/utils/blueprint_mapper.py#7-108) used silent heuristic fallback (last assembly) for plot edges.

**Fix:** Read plot spec for `target_dataset` / `assembly_id` key explicitly.
- If found → draw correct edge.
- If **not** found → render informational node (NOT error-styled, user-friendly):

```
INFO_pid[["📋 Plot: pid\n(Select manifest to see lineage)"]]
```
Style: `classDef info fill:#e3f2fd,stroke:#1976d2,color:#1a1a1a` (light blue, calm).

> [!NOTE]
> This message will disappear as soon as a manifest with a `target_dataset` key is loaded.
> It is **not** an error — it is a "no data yet" state indicator.

**Files:** [libs/utils/src/utils/blueprint_mapper.py](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/libs/utils/src/utils/blueprint_mapper.py)

---

## Bug #4: Right Sidebar — Full Context Matrix

**Root cause:** Right sidebar is hardcoded as "Pipeline Audit" in [ui.py](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/app/src/ui.py). Per ADR-039, the
right sidebar must be **fully context-sensitive** to the active module.

> [!IMPORTANT]
> The `audit_sidebar` inline content in [ui.py](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/app/src/ui.py) must be replaced with:
> `ui.output_ui("right_sidebar_content_ui")`
> Only this single line changes in [ui.py](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/app/src/ui.py). All routing logic lives in [server.py](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/app/src/server.py).

**Right Sidebar Context Matrix (authoritative):**

| Active Module (`input.sidebar_nav`) | Right Panel Content |
|:---|:---|
| `"Wrangle Studio"` (Blueprint Architect) | **Blueprint Surgeon Panel** — selected node name, step count, schema summary, "Enter Edit" button |
| `"Home"` or `"Viz"` / Analysis Theater | **Pipeline Audit** — Tier 2 (Inherited) + Tier 3 (User) nodes *(unchanged, existing code)* |
| `"Gallery"` | **Gallery Info Panel** — placeholder: "Select a recipe to view details" |
| `"Dev Studio"` | **Dev Inspector** — placeholder: "Developer diagnostic tools" |
| *(future modes)* | Extendable — a dict lookup by [sidebar_nav](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/app/src/server.py#514-540) value |

> [!NOTE]
> Home/Viz/Analysis Theater variable names stay unchanged. This is additive only — existing
> [audit_nodes_tier2](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/app/src/server.py#727-751) / [audit_nodes_tier3](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/app/src/server.py#693-726) renders are reused, not replaced.

**Files:** [app/src/ui.py](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/app/src/ui.py) (1 line change), [app/src/server.py](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/app/src/server.py) (add `right_sidebar_content_ui` render)

---

## Enhancement: Hierarchical YAML Viewer

Replace flat `<pre>` YAML block in tab "4. YAML (Raw Source)" with a collapsible accordion tree.

**Structure:**
- Each **top-level key** ([data_schemas](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/libs/utils/src/utils/config_loader.py#84-87), `assembly_manifests`, `plots`, …) is a collapsible panel.
- Within each panel, sub-keys are second-level accordions.
- Leaf values: styled `<code>` block.
- Each panel for a node known to the TubeMap includes a small **"🎯 Focus"** button that calls
  `window.mermaidClick(node_id)` to highlight the corresponding TubeMap node.

**Files:** [app/modules/wrangle_studio.py](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/app/modules/wrangle_studio.py) — replace [yaml_source_viewer_ui](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/app/modules/wrangle_studio.py#363-370) render.

---

## Proposed Changes (Step-by-step execution order)

| Step | File | Change | Safety Profile |
|:---:|:---|:---|:---|
| 1 | [server.py](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/app/src/server.py) | Remove `wrangle_studio.apply_logic` from [tier3_leaf](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/app/src/server.py#101-142) | ✅ Additive-only (removal of 1 line) |
| 2 | [server.py](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/app/src/server.py) | Add `right_sidebar_content_ui` render function | ✅ New function, no existing code touched |
| 3 | [ui.py](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/app/src/ui.py) | Replace inline audit content with `ui.output_ui(...)` | ⚠️ 1 structural change — boot test after |
| 4 | [wrangle_studio.py](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/app/modules/wrangle_studio.py) | Add `_parse_fields_safe` helper + advisory banner | ✅ Additive |
| 5 | [blueprint_mapper.py](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/libs/utils/src/utils/blueprint_mapper.py) | Fix plot edge logic, remove heuristic fallback | ✅ Scoped to mapper only |
| 6 | [wrangle_studio.py](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/app/modules/wrangle_studio.py) | Replace YAML `<pre>` with accordion tree | ✅ UI only, no data logic |
| 7 | `assets/scripts/` | Add `normalize_manifest_fields.py` | ✅ New file, no existing code touched |

**Boot test after steps 1, 3, and 6.**

---

## Verification Plan

### Headless Boot Test (after each of steps 1, 3, 6)
```bash
export SPARMVET_PERSONA=developer && ./.venv/bin/python -m shiny run app/src/main.py
```
Expected: No traceback. `DEBUG: Initializing Server with Persona: developer` printed.

### Manual @verify Checklist
- [ ] Gallery mode works exactly as before (no regression)
- [ ] Analysis Theater (Home tab): right panel shows Pipeline Audit
- [ ] Gallery tab: right panel shows "Select a recipe" placeholder
- [ ] Wrangle Studio: right panel shows Blueprint Surgeon Panel
- [ ] TubeMap renders; missing-lineage plots show blue info node (not orange error)
- [ ] Schema dict-format: shows table + advisory banner pointing to `normalize_manifest_fields.py`
- [ ] Tab "4. YAML": collapsible accordion sections per top-level key
- [ ] "🎯 Focus" button highlights TubeMap node
