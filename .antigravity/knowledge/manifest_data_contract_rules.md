# Manifest Data Contract — Structure, Inheritance & Resolution Rules

**Authority:** ADR-004, ADR-024, ADR-041  
**Last updated:** 2026-04-21 (Session 6)  
**Status:** Active — authoritative reference for Blueprint Architect implementation

---

## 1. Why This Document Exists

The Blueprint Architect must display — for any component a user clicks — what data **enters** that component (Upstream Contract) and what data **leaves** it (Downstream Contract). The rules governing that are non-obvious because:

- Fields can be declared inline OR in separate `!include` files
- `output_fields` is often **omitted** (inheritance applies)
- Assemblies often have no `output_fields` at all (the output IS the union of ingredients)
- Plots never declare output_fields (they are terminal)
- `final_contract` is an alias for `output_fields` on assemblies
- Empty `wrangling: []` means identity (fields pass through unchanged)

Without a clear resolution protocol, the app resolves to empty and the user sees nothing.

---

## 2. Manifest Top-Level Sections

```yaml
id: <manifest_id>
type: species | project

data_schemas:        # Raw source datasets (Tier 0)
  <schema_id>: ...

additional_datasets_schemas:  # Extra reference datasets (also Tier 0)
  <schema_id>: ...

metadata_schema:     # Singleton metadata source (Tier 0, special)
  ...

assembly_manifests:  # Joined datasets (Tier 1)
  <assembly_id>: ...

analysis_groups:     # Grouped plots (Tier 2/3)
  <group_name>:
    plots:
      <plot_id>: ...
```

`ConfigManager` flattens `analysis_groups.*.plots` into a top-level `plots` dict so `VizFactory.render(df, cfg.raw_config, plot_id)` works without knowing the group.

---

## 3. Schema Node Types and Their Roles

| Section | Role token | TubeMap colour | Is terminal? |
|---|---|---|---|
| `data_schemas` | `wrangling` (primary) + `input_fields` + `output_fields` | blue (source) / amber (wrangle) | No |
| `additional_datasets_schemas` | same as data_schemas | grey | No |
| `metadata_schema` | same as data_schemas | orange | No |
| `assembly_manifests` | `assembly` | purple | No |
| `analysis_groups.*.plots` | `plot_spec` | green | Yes — no output |
| `plots.*.pre_plot_wrangling` | `plot_wrangling` | amber | Yes — no output |

---

## 4. The Fields Declaration Options (per schema node)

### 4.1 Inline (monolithic manifest)

All field declarations are embedded directly in the YAML:

```yaml
data_schemas:
  MLST:
    source: { type: local_tsv, path: ... }
    input_fields:
      sample_id: { original_name: sample_id, type: categorical, is_primary_key: true }
      sequence_type: { original_name: Sequence Type, type: categorical }
    wrangling:
      tier1: []     # empty = identity, fields pass through
    output_fields:  # OPTIONAL — see inheritance rules below
      sample_id: {}
      sequence_type: {}
```

### 4.2 File-linked (modular `!include` manifest)

Fields live in separate YAML files, referenced via `!include`:

```yaml
data_schemas:
  VIGAS_VirulenceFinder:
    source: ...
    input_fields: !include 'VIGAS_VirulenceFinder/input_fields/VIGAS_VirulenceFinder_input_fields.yaml'
    wrangling: !include 'VIGAS_VirulenceFinder/wrangling/VIGAS_VirulenceFinder_wrangling.yaml'
    output_fields: !include 'VIGAS_VirulenceFinder/output_fields/VIGAS_VirulenceFinder_output_fields.yaml'
```

The `!include` paths are relative to the master manifest directory. `ConfigManager` resolves them via `yaml.SafeLoader` with a custom `!include` constructor.

### 4.3 Rich Dict format (ADR-041, enforced)

Each field slug maps to a metadata dict:

```yaml
sample_id:
  original_name: Sample_ID   # column name in source file
  type: categorical           # categorical | numeric | string | boolean | date
  label: Sample ID            # human-readable label
  is_primary_key: true        # optional — marks join key
```

**Shorthand (partial):** `sample_id: {}` means "inherit from input_fields or keep as-is, no override".  
**Legacy (deprecated):** `sample_id: categorical` (flat string) — triggers warning badge in Blueprint Architect.

---

## 5. Field Inheritance Rules — The Resolution Protocol

This is the core contract resolution algorithm, implemented as `_resolve_fields_for_schema()` in `server.py`.

### 5.1 For a `data_schema` or `additional_datasets_schema` node

Resolution priority (first non-empty result wins):

```
1. output_fields FILE  (role="output_fields" in ctx_map, file path in inc_map)
2. output_fields INLINE  (siblings["output_fields"] == {"inline": {...}})
3. input_fields FILE  (role="input_fields" in ctx_map)
4. input_fields INLINE  (siblings["input_fields"] == {"inline": {...}})
```

**Semantic meaning of each case:**

| Case | What it means |
|---|---|
| `output_fields` declared | Author explicitly named what columns survive after wrangling |
| `output_fields: {}` or `output_fields: []` | Empty — treat as "not declared", fall through to inheritance |
| `output_fields` absent | Same — fall through |
| `wrangling: []` or `wrangling: {tier1: []}` | Identity transform — output = input |
| Only `input_fields` present | Output is all of input (no wrangling, no narrowing) |

**Key insight:** An empty `output_fields: {}` or `output_fields: []` is NOT the contract — it is a placeholder. The actual contract is resolved by backtracking to `input_fields`.

### 5.2 For an `assembly_manifests` node

Resolution priority:

```
1. final_contract FILE  (role="output_fields" in ctx_map — final_contract is aliased to output_fields)
2. final_contract or output_fields INLINE  (siblings["output_fields"] == {"inline": {...}})
3. Transparent merge — recursively resolve each ingredient's output fields and UNION them
```

**Semantic meaning:**

| Case | What it means |
|---|---|
| `final_contract` declared | Author explicitly named the curated output of the assembly (e.g. selecting only relevant columns from all ingredients) |
| `output_fields` declared | Same as final_contract |
| Neither declared | The assembly output is the UNION of all ingredient output fields. Columns from later ingredients shadow same-named columns from earlier ones. |

**Inheritance chain for a bare assembly:**

```
MLST_with_metadata (assembly, no output_fields)
  ├── MLST (no output_fields)  → inherits MLST.input_fields
  └── metadata_schema          → inherits metadata_schema.output_fields (or input_fields)
  
Result: UNION of {MLST.input_fields} ∪ {metadata_schema.output_fields}
```

### 5.3 For a `plot_spec` or `plot_wrangling` node

- **Upstream Contract** (what enters the plot): resolve the `target_dataset` schema via the protocol above.
- **Downstream Contract**: None. Plots are terminal — they produce a visual, not a data table.
- `target_dataset` is nested inside `spec:` for inline plots:
  ```yaml
  mlst_bar:
    info: ...
    spec:
      factory_id: bar_logic
      target_dataset: MLST_with_metadata   # ← here, under spec
      x: sequence_type
  ```
  **Not** at `mlst_bar.target_dataset`. Resolution code must check both levels.

### 5.4 Inheritance summary table

| Scenario | Upstream shown | Downstream shown |
|---|---|---|
| `input_fields` only, no wrangling, no output_fields | "Raw source — no upstream" | `input_fields` (=output, identity) |
| `input_fields` + `wrangling` + no `output_fields` | `input_fields` | `input_fields` (assumed output = input) |
| `input_fields` + `wrangling` + `output_fields` | `input_fields` | `output_fields` |
| Assembly, no `output_fields` | Ingredient list (accordion) | Union of all ingredient outputs |
| Assembly + `final_contract` | Ingredient list | `final_contract` |
| Plot spec | `target_dataset` output (backtracked) | "Terminal — no output" |

---

## 6. The Two Manifest Styles: Inline vs. Modular

### 6.1 Inline (monolithic)

Everything in one YAML file. Typical for prototypes, small projects, or auto-generated manifests.

```
config/manifests/pipelines/1_test_data_ST22_dummy.yaml   (1200+ lines)
```

- ctx_map stores schema_ids as keys: `ctx_map["MLST"] = {role: "wrangling", siblings: ...}`
- `inc_map` is NOT populated for inline entries (no file paths to store)
- Mode B load path in `_do_load_component`

### 6.2 Modular (`!include`)

Master YAML contains `!include 'subdir/file.yaml'` markers. Components live in their own files.

```
config/manifests/VIGAS-P/
  master.yaml
  VIGAS_VirulenceFinder/
    input_fields/VIGAS_VirulenceFinder_input_fields.yaml
    wrangling/VIGAS_VirulenceFinder_wrangling.yaml
    output_fields/VIGAS_VirulenceFinder_output_fields.yaml
```

- ctx_map stores rel_paths as keys: `ctx_map["VIGAS_VirulenceFinder/output_fields/...yaml"] = {...}`
- `inc_map` maps rel_path → absolute file path
- Mode A load path in `_do_load_component`

### 6.3 Hybrid (modular assembly in inline manifest)

The `1_test_data_ST22_dummy` manifest has some assemblies that reference separate files:

```yaml
Summary_phenotype_length_fragmentation:
  output_fields: !include '1_test_data_ST22_dummy/output_fields/Summary_phenotype_length_fragmentation_output_fields.yaml'
  recipe:
    tier1: !include '1_test_data_ST22_dummy/assembly/Summary_phenotype_length_fragmentation_assembly.yaml'
```

This is fully supported: `_build_sibling_map` registers the rel_path in ctx_map and inc_map for those specific slots.

---

## 7. The ctx_map Structure

Built by `_build_sibling_map(master_path)`. Maps navigable keys → component context:

```python
ctx_map[key] = {
    "role": "input_fields" | "output_fields" | "wrangling" | "assembly"
             | "plot_spec" | "plot_wrangling",
    "schema_id": str,         # The parent schema ID (e.g. "MLST")
    "schema_type": str,       # "data_schemas" | "assembly_manifests" | "plots" | ...
    "siblings": {
        "input_fields": str | {"inline": dict} | None,
        "output_fields": str | {"inline": dict} | None,
        "wrangling": str | {"inline": list} | None,
    },
    "ingredients": list[str],  # For assemblies: ordered schema_id list
    "group_id": str,           # For plots: parent analysis_group name
}
```

**Key registration rules:**
- For file-linked slots: `key = rel_path` (e.g. `"MLST/output_fields/MLST_output_fields.yaml"`)
- For inline schemas (no `!include`): `key = schema_id` (e.g. `"MLST"`)
- Both can coexist in the same manifest (hybrid style)
- Schema_id key is only registered if no rel_path was registered for that schema (avoids duplicates)

---

## 8. Known Edge Cases and Their Fixes

### 8.1 `target_dataset` under `spec:` not at plot top level

```yaml
mlst_bar:         # plot_id
  info: ...
  spec:           # ← spec wrapper (Phase 11-D convention)
    target_dataset: MLST_with_metadata   # ← nested here
    factory_id: bar_logic
```

Fix: always check `pspec.get("target_dataset") or pspec.get("spec", {}).get("target_dataset")`

### 8.2 Assembly with no `output_fields` returns empty

When neither `output_fields` nor `final_contract` is declared, `_resolve_fields_for_schema` must recurse into ingredients and merge their resolved fields. The recursion applies the same priority chain to each ingredient, ultimately hitting `input_fields` if no `output_fields` exists.

### 8.3 Empty `output_fields: []` or `output_fields: {}`

These are syntactically present but semantically absent. The resolution code must NOT return an empty dict/list as the contract. Fall through to the next resolution pass.

### 8.4 `final_contract` vs `output_fields` on assemblies

Both are valid. `_build_sibling_map` normalises them: `effective_out = out or con`. The role registered is always `"output_fields"` regardless of which key was used in YAML.

### 8.5 Inline plot `target_dataset` scan timing in Mode B

In Mode B, the analysis_groups scan must run **unconditionally** (not only when `target is None`), because `mlst_bar` might also be found in `assembly_manifests` (it won't, but the scan must not be gated on `target`).

---

## 9. Data Flow Diagram

```
[Source TSV/CSV]
      │
      ▼
[data_schemas.X]
  input_fields  ──► describes columns as they arrive from the file
  wrangling     ──► transforms (may change column names, types, count)
  output_fields ──► describes columns after wrangling
                    (OPTIONAL: if absent, inherit from input_fields)
      │
      │  (+ other ingredients)
      ▼
[assembly_manifests.Y]
  ingredients: [X, metadata_schema, ...]
  recipe        ──► joins, aggregations across ingredients
  output_fields / final_contract
                ──► OPTIONAL: if absent, union of all ingredient output_fields
      │
      ▼
[analysis_groups.G.plots.P]
  spec.target_dataset: Y    ──► which assembly feeds this plot
  spec.factory_id: bar_logic
  spec.x / spec.fill / ...  ──► column mapping (must exist in target_dataset output)
  pre_plot_wrangling         ──► optional Tier 2 transform before rendering
      │
      ▼
[VizFactory.render(df, manifest, plot_id)]
  reads manifest['plots'][plot_id]  ──► flattened by ConfigManager from analysis_groups
  validates column names against df.columns
  applies geom layers
      │
      ▼
[matplotlib figure]
```

---

## 10. Implementation Checklist for Blueprint Architect

When implementing any feature that reads or displays field contracts:

- [ ] Check BOTH `output_fields` and `final_contract` keys for assemblies
- [ ] Handle both inline (`{"inline": {...}}`) and file-linked (`str` rel_path) siblings
- [ ] Fall through to `input_fields` when `output_fields` is absent or empty
- [ ] For assembly with no output: recurse into ingredients (use `_resolve_fields_for_schema`)
- [ ] For plot `target_dataset`: look under `spec.target_dataset`, not `plot_id.target_dataset`
- [ ] For materialization: use `target_dataset` as `collection_id`, NOT `plot_id`
- [ ] For Mode A (file load): use `inc_map[rel_path]` to get absolute file path
- [ ] For Mode B (inline): read directly from `raw_config` sections
- [ ] Empty `wrangling: []` or `wrangling: {tier1: []}` = identity, do not treat as error
