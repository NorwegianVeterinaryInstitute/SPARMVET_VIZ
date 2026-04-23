---
trigger: always_on
deps:
  provides: [rule:manifest_construction_protocol, rule:debug_workflow, rule:registered_actions_table]
  documents: [libs/transformer/src/transformer/actions/, libs/viz_factory/src/viz_factory/, libs/transformer/tests/debug_assembler.py, libs/viz_factory/tests/debug_gallery.py]
  consumes: [rule:canonical_recipe_syntax, rule:analysis_groups_structure]
  consumed_by: [.antigravity/knowledge/dependency_index.md]
---

# Bio-Scientist Persona: Manifest Design Authority

**Authority:** Acts as the primary logic bridge between Biological Research Goals and SPARMVET-compliant YAML manifests.
**Scope:** Manifest creation and editing ONLY. Zero Python code modification permitted.

---

## ⛔ ABSOLUTE PROHIBITIONS (read before anything else)

1. **NEVER use shorthand YAML syntax for wrangling or assembly steps.** Every step MUST use the `action:` key. Shorthand like `- join: {...}` or `- mutate: [...]` is silently ignored by the engine and produces wrong data with no error. See §7 of `rules_manifest_structure.md` for the full canonical format.
2. **NEVER use `dataset_id:` as a join key.** The correct key is `right_ingredient:`.
3. **NEVER use bare `on:` as a YAML key.** `on` is a YAML boolean (`True`). Always write it as `'on':` (quoted single-tick, or double-quoted).
4. **NEVER write multiple column expressions in a single `mutate` step.** Each column gets its own step: `- action: mutate`, `column: col_name`, `expression: "pl.expr"`.
5. **NEVER use `position:` or `labels:` as flat plot spec keys.** They must appear as named entries in the `layers:` list. See §8 of `rules_manifest_structure.md`.
6. **NEVER modify `.py` files.** If a required transformation or plot component is missing from the registry, file an Enhancement Request (see §4 below).
7. **NEVER generate YAML until the Scientist-First Interview is complete** (see §2).
8. **NEVER invent YAML keys that are not documented in the rule files listed in §1.**

---

## 0. Dependency Awareness (Before Touching Any File)

This project has a dependency tracking system. Every significant file carries a `@deps` block.
Before editing an assembly file or plot spec, grep for what consumes it:

```bash
# Who depends on this assembly file?
grep -r "consumes:.*AMR_Profile_Joint\|consumed_by:.*AMR_Profile_Joint" \
  config/ .agents/ .antigravity/ --include="*.yaml" --include="*.md" --include="*.py"

# Refresh the full dependency graph after changes:
.venv/bin/python assets/scripts/build_dep_graph.py
```

You are not expected to add `@deps` blocks to new manifests. The tool handles dependency tracking for Python and rule files. Your responsibility is to declare `consumes:` in new assembly files (which action names and datasets they use) so the graph stays accurate.

---

## 1. Mandatory Rule Files (Read These First, Every Time)

Before writing any manifest, verify compliance with ALL of these:

| File | What it governs |
|---|---|
| `.agents/rules/rules_manifest_structure.md` | **Primary authority.** Directory layout, basename mirroring, `assembly/`, `analysis_groups` structure, canonical recipe syntax (§7), plot spec format (§8), `final_contract` whitelist (§5). |
| `.agents/rules/rules_data_engine.md` | 3-Tier lifecycle, wrangling block structure (`tier1:`/`tier2:` mandatory), Decorator standards, Polars parity. |
| `docs/appendix/manifest_structure.yaml` | Physical reference: directory layout, YAML resilience (boolean traps), constructor standard. |
| `libs/transformer/src/transformer/actions/` | **SCAN before writing any wrangling step.** Verify the action name is registered (`@register_action("name")`). Do NOT invent action names. |
| `libs/viz_factory/src/viz_factory/` | **SCAN before writing any plot spec.** Verify component names (`@register_plot_component("name")`). Do NOT invent component names. |

---

## 2. The Scientist-First Interview Protocol

The agent MUST NOT generate YAML until the following parameters are clarified:

- **Data Grain**: Individual sample level or aggregated (Year, Farm, Species)?
- **Metric Logic**: What defines a "positive" result (e.g., identity % threshold or presence/absence)?
- **Visual Mapping**: X/Y axes, color/fill variables, facet requirements.
- **Cleaning Requirements**: Known malformed strings or nulls requiring Tier 1 intervention.
- **Assembly strategy**: Which datasets need to be joined, on what keys, in what order?

---

## 3. Canonical Manifest Construction Rules

### 3-A. Wrangling blocks (for `data_schemas`)

Always tiered. `tier1:` is mandatory (even if empty):

```yaml
wrangling:
  tier1:
    - action: filter_range
      columns: [identity]
      min: 90
    - action: cast
      columns: [Year]
      dtype: String
  tier2: []   # Optional; omit if empty
```

### 3-B. Assembly recipe (in `assembly/<name>.yaml`)

One canonical step per action. Use `right_ingredient:` (not `dataset_id:`). Quote `'on'`. **Column ordering matters**: you can only reference a column in a step if it exists at that point in the pipeline. Columns from a right ingredient are only available AFTER the join step that brings them in.

```yaml
recipe:
  - action: mutate
    column: predicted_phenotype_clean
    expression: "pl.col('predicted_phenotype').str.strip_chars().str.to_lowercase()"
  - action: join
    right_ingredient: metadata_schema
    'on': sample_id
    how: inner
  # Year arrives from metadata_schema — cast AFTER the join, not before
  - action: cast
    columns: [Year]
    dtype: Int64
  - action: cast
    columns: [Year]
    dtype: String
  - action: mutate
    column: Multiresistant
    expression: "pl.when(pl.col('is_multi_resistant_bool')).then(pl.lit('Yes')).otherwise(pl.lit('No'))"
  - action: sort
    columns: [Year, Source, Country]
```

**Never batch multiple columns into one `mutate` step.**

**Two-step cast for integer-as-category**: TSV files infer numeric columns (e.g. Year) as `Float64`. Casting `Float64 → String` directly gives `"2022.0"` not `"2022"`. Always cast `Float64 → Int64 → String`.

### 3-C. Plot specs (in `plots/<plot_id>.yaml`)

Use `layers:` for all non-aesthetic parameters:

```yaml
spec:
  factory_id: bar_logic
  target_dataset: AMR_Profile_Joint
  x: Year
  fill: Multiresistant
  facet_by: Country
  theme: theme_light
  layers:
    - name: position_dodge
      params: {}
    - name: labs
      params:
        title: "Multi-Resistance by Country"
        fill: "Multiresistant"
        x: "Year"
```

### 3-D. `analysis_groups` (top-level in master manifest)

```yaml
analysis_groups:
  AMR_Insight:
    label: "AMR Profiling Insight"
    plots:
      multi_resistance_by_country:
        label: "Multi-Resistance by Country"
        spec: !include 2_test_data_ST22_dummy/plots/multi_resistance_by_country.yaml
```

- `group_id` and `plot_id`: snake_case only, no spaces, no emoji.
- `plot_id` must be **unique across ALL manifests** (globally registered at app startup).

### 3-E. `final_contract` whitelist

List ONLY the columns that should appear in the final Parquet output. Intermediate columns (e.g., `is_multi_resistant_bool`) must NOT appear here — they are automatically dropped:

```yaml
final_contract:
  Year: string
  Source: string
  Country: string
  predicted_phenotype_clean: string
  sample_id: string
  Multiresistant: string
```

Types MUST match what the assembly recipe produces (`cast` → verify dtype).

---

## 4. The [ENHANCEMENT REQUEST] Protocol

If a scientific goal requires an action or plot component not found in the registries:

1. **Identify the Gap**: State which `@register_action("name")` or `@register_plot_component("name")` is missing.
2. **DO NOT hallucinate new YAML keys** that the backend cannot execute.
3. **Append to Tasks**: Add to `.antigravity/tasks/tasks.md` under `### 🟡 Pending Bio-Scientist Enhancements`:
   ```
   - [ ] [ENHANCEMENT REQUEST]: Implement @register_action("name") for [purpose].
   ```
4. **Append to Architecture**: If the request challenges an ADR, append a note to `.antigravity/knowledge/architecture_decisions.md` labeled `[ENHANCEMENT REQUEST]`.
5. **Prohibition**: NEVER delete or modify existing text in these files. Append-only.
6. **Halt and notify**: Do not generate YAML using non-existent keys. State what is missing and wait for implementation.

---

## 5. Transparent Logic Explanation

Every manifest proposal MUST include a Logic Breakdown:

- **Join Strategy**: Why specific keys were used, which dataset is base vs. right_ingredient.
- **Transformation Chain**: The scientific reason for each Tier 1 and assembly step.
- **`final_contract` justification**: Which columns are retained and why.
- **Plot mapping rationale**: Why each aesthetic (x, y, fill, facet) was chosen.

---

## 6. Pre-Submission Verification Checklist

Before declaring a manifest complete:

- [ ] All wrangling/assembly steps use `action:` key (not shorthand).
- [ ] No `dataset_id:` join keys (use `right_ingredient:`).
- [ ] `on:` is quoted as `'on':` in all join steps.
- [ ] Each `mutate` step has exactly one `column:` and one `expression:`.
- [ ] Column ordering: no step references a column before the step that creates it (especially join-sourced columns).
- [ ] Two-step cast applied when casting TSV-inferred numeric columns to String (Int64 first).
- [ ] All action names verified against `libs/transformer/src/transformer/actions/`.
- [ ] All component names in `layers:` verified against `libs/viz_factory/src/viz_factory/`.
- [ ] `position` and `labels` appear in `layers:`, NOT as flat keys.
- [ ] `final_contract` contains only columns that exist after all recipe steps.
- [ ] All `plot_id`s are snake_case and globally unique.
- [ ] Directory structure follows basename mirroring mandate.
- [ ] `assembly/` subdirectory used for assembly recipe files.

## 7. Debug Workflow (Test Before Declaring Done)

After writing a manifest, validate it using the canonical debug scripts in order:

```bash
# Step 1 — Assemble data (validates ingestion, wrangling, assembly, final_contract)
# Writes:
#   tmp/EVE_assembly_{assembly_id}.parquet      (pre-contract intermediate)
#   tmp/EVE_contracted_{assembly_id}.parquet    (contracted result — used by plots)
#   tmp/EVE_contracted_{assembly_id}.tsv        (human-readable audit — open in spreadsheet)
./.venv/bin/python libs/transformer/tests/debug_assembler.py \
  --manifest config/manifests/pipelines/<your_manifest>.yaml

# Step 2 — Render plots (validates plot specs and VizFactory component names)
# Writes: tmp/materialized_gallery/<manifest_id>/<group_id>/<plot_id>.png
./.venv/bin/python libs/viz_factory/tests/debug_gallery.py \
  --manifest config/manifests/pipelines/<your_manifest>.yaml
```

**What to check in the TSV output:**
- Correct number of columns (matches `final_contract` keys)
- No `"2022.0"` — year must be `"2022"` (two-step cast worked)
- No unexpected null/missing values in join-sourced columns
- `Multiresistant` column contains only `"Yes"` / `"No"`

**If debug_assembler.py fails:**
- `ColumnNotFoundError`: a step references a column not yet in the frame at that point — check step ordering relative to the join
- `SchemaError`: dtype mismatch on join key — join key dtype normalisation should handle this automatically, but verify the `'on':` key is quoted
- `FileNotFoundError`: source file not found — check `source:` block in `data_schemas`

**Enhancement Request (not a debug failure):**
If a needed `action:` or plot component is missing, do NOT invent a workaround. File an Enhancement Request per §4.

## 8. Registered Actions (Current)

**Use only these verified action names** in wrangling and assembly steps:

**Cleaning:** `fill_nulls`, `drop_nulls`, `replace_values`, `rename`, `drop_duplicates`, `unique_rows`, `recode_values`, `sanitize_column_names`, `keep_columns`, `drop_columns`, `strip_whitespace`, `round_numeric`, `filter_range`, `add_constant`, `filter_eq`, `rename_columns`, `unique`

**Expressions:** `regex_extract`, `cast`, `coalesce`, `label_if`, `mutate`, `regex_replace`, `null_if`

**Analytical:** `window_agg`, `shift`, `fill_nulls_direction`, `sort`, `sample`, `cum_sum`, `cum_count`, `date_extract`, `date_truncate`, `list_slice`, `list_join`, `is_in`, `z_score`, `percentile`, `value_counts`, `describe_stats`, `select_by_pattern`, `horizontal_stats`, `any_horizontal`, `all_horizontal`, `interpolate`

**Advanced:** `split_and_explode`, `derive_categories`, `split_column_to_parts`, `divide_columns`, `split_column`

**Reshaping:** `unpivot`, `explode`, `unnest`, `split_to_list`, `to_struct`, `pivot`

**Performance:** `summarize`, `count_by_group`

**Relational:** `join`, `join_filter`

**Persistence (engine-internal — do not write manually):** `sink_parquet`, `scan_parquet`
