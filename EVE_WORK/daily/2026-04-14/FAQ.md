# NOTES 7
how does it know which table to use for the filtering ?

It knows which table to use through **Position-Based Initialization**.

Here is how the SPARMVET 

**![](vscode-file://vscode-app/usr/share/antigravity/resources/app/extensions/theme-symbols/src/icons/files/python.svg)**

**DataAssembler** thinks when it reads your manifest:

### 1. The "Backbone" Rule

The engine looks at your `ingredients` list in the main manifest:

yaml

ingredients:

  - dataset_id: "Summary"        # <--- POSITION 0

  - dataset_id: "Summary_quality" # <--- POSITION 1

By architecture, it **always uses the very first ingredient as the "Backbone"** of the assembly.

### 2. Sequential Execution

When it starts processing your 

![](vscode-file://vscode-app/usr/share/antigravity/resources/app/extensions/theme-symbols/src/icons/files/python.svg)

recipe for the assembly:

- **Step 1: `filter_eq`**: Since this is the first step and you haven't mentioned any other table yet, the engine automatically applies the filter to the Backbone (**`Summary`**).
- **Step 2: `join`**: When it sees `right_ingredient: "Summary_quality"`, it takes the current state of the Backbone (which is now filtered `Summary`) and joins it with the quality table.

### 🧩 Why this is powerful:

You can control what the "Base" of your assembly is simply by changing the order of your `ingredients` list.

- **If `Summary` is first**: The pipeline builds outward from the long-format discovery data.
- **If `Summary_quality` was first**: The pipeline would start with the wide-format statistics and then join the phenotypes onto it.

IMPORTANT

**Summary ID Tip**: In SPARMVET, the Backbone is always the **first entry** in your list. Any action in your recipe that isn't a "Join" will always be applied to that evolving Backbone.

# NOTES 6

how can I make a split of my tier 1 to create 2 datasets that can be joined afterwards ?

Analyzed

In the SPARMVET architecture, a dataset follows a **linear** path through its wrangling steps. To "split" a dataset and rejoin it later, you should use the **"Mirror Strategy"**:

### The Mirror Strategy ( branching via definitions)

Instead of trying to split inside a single YAML file, you define the source dataset **twice** in your master manifest under different IDs.

#### 1. Define two "Mirrors" in 

```yaml
data_schemas:
# Branch A: Focus on Genotypes
Summary_Genotypes:
source: !include 'sources/Summary_source.yaml'
wrangling:
tier1:
- action: "split_and_explode"
column: "genotype"
# Branch B: Focus on Plasmids
Summary_Plasmids:
source: !include 'sources/Summary_source.yaml'
wrangling:
tier1:
- action: "split_and_explode"
column: "plasmid"
```

#### 2. Join them in the `assembly_manifests`

Now that you have two independent "streams" (ingredients), you join them back together at the assembly stage:

```yaml
assembly_manifests:
  Summary_Consolidated:
    recipe:
      - action: "join"
        left_ingredient: "Summary_Genotypes"
        right_ingredient: "Summary_Plasmids"
        on: "sample_id"
```
### Why this is better than a "split" decorator:

1. **Memory Safety**: Each branch is processed independently and lazily.
2. **Avoids Cartesian Products**: If you explode both columns in the same linear file, you get a "Row Explosion" (e.g., 2 genotypes $\times$ 2 plasmids = 4 rows). By splitting them into mirrors and joining on `sample_id`, you keep the genotypes and plasmids as independent "long" datasets within the same consolidated table.
3. **Tiered Logic**: You can have a shared `Summary_base_wrangling.yaml` that you `!include` at the start of both mirrors (to handle the common 
    
    ![](vscode-file://vscode-app/usr/share/antigravity/resources/app/extensions/theme-symbols/src/icons/files/python.svg)
    
    drop_columns part) and then add the specific explodes after.

TIP

**Showcase Selection**: This is the "Professional" way to handle multi-valued columns in SPARMVET. It demonstrates how to leverage the relational power of the **DataAssembler** instead of relying on massive row-expansion in the **DataWrangler**.
# NOTES 5

but when I transfrom to long format, would that not be better to drop the columns that I will anyway drop afterwards, that would keep the table more lightweight no ? instead of duplicating all their values ?

Yes! You are absolutely **right**. This is a very insightful performance observation.

In data engineering, this is called **"Pruning Before Expansion."**

### Why you are correct:

When you perform an 

![](vscode-file://vscode-app/usr/share/antigravity/resources/app/extensions/theme-symbols/src/icons/files/python.svg)

explode (Long Format), every other column in the table is **duplicated** for every new row.

- **If you have 50 extra columns** and you explode a row into 10 parts, you just created **500 cells** of redundant data.
- **If you drop them first**, the explosion only duplicates the "bones" of the data (the primary keys and necessary metadata).

### 🚀 Optimized Workflow for your Manifest:

You should structure your 

![](vscode-file://vscode-app/usr/share/antigravity/resources/app/extensions/theme-symbols/src/icons/files/python.svg)

tier1 wrangling in this order:

1. **Selection/Pruning**: Drop everything you don't need for the final output or intermediate calculation.
2. **Long-Format Transformation**: Perform your 
    
    ![](vscode-file://vscode-app/usr/share/antigravity/resources/app/extensions/theme-symbols/src/icons/files/python.svg)
    
    split_to_list and 
    
    ![](vscode-file://vscode-app/usr/share/antigravity/resources/app/extensions/theme-symbols/src/icons/files/python.svg)
    
    explode.
3. **Final Processing**: Calculation of ratios, etc.

**Example for your Showcase**:

yaml

tier1:

  # 1. Prune early to save memory during the explode

  - action: "drop_columns"

    columns: ["taxon", "quality_module_feedback"] 

  # 2. Explode (now much faster and lighter)

  - action: "split_to_list"

    columns: ["genotype", "plasmid"]

    separator: ", "

  - action: "explode"

    columns: ["genotype", "plasmid"]

TIP

**Performance Architecture**: This is exactly why we have **Tier 1 (The Trunk)**. By pruning and standardizing early, we ensure that the "Branch" (Tier 2/3) operations aren't carrying around "ghost data" that will never be used by the visualizations.

# NOTES 4 

If you drop a column during **Wrangling**, you must **NOT** include it in your `output_fields`.

Here is the "Chain of Command" for columns:

1. **Wrangling (
    
    ![](vscode-file://vscode-app/usr/share/antigravity/resources/app/extensions/theme-symbols/src/icons/files/python.svg)
    
    drop_columns)**: This physically removes the column from the data stream. If you do this, the column effectively "ceases to exist" for all subsequent steps.
2. **Output Fields (`select`)**: This is a mandatory contract. If you list a column here that you already dropped in Step 1, the engine will throw a `TransformationError` because it cannot find the column you are asking for.

### 💡 The "Clean-Contract" Strategy

Technically, you don't even need to use the 

![](vscode-file://vscode-app/usr/share/antigravity/resources/app/extensions/theme-symbols/src/icons/files/python.svg)

drop_columns action if you are using a defined `output_fields` block.

- **Best Practice**: Use 
    
    ![](vscode-file://vscode-app/usr/share/antigravity/resources/app/extensions/theme-symbols/src/icons/files/python.svg)
    
    drop_columns only for **intermediate/temporary columns** that you created during wrangling (like your `hsp_len` and `total_len`) to keep the data stream lightweight.
- **The Contract Rule**: Your `output_fields` should only contain the final, published columns you want the user to see. Anything else is automatically pruned by the system at the very end.

---

### ⚠️ Note on your 

![](vscode-file://vscode-app/usr/share/antigravity/resources/app/extensions/theme-symbols/src/icons/files/yaml.svg)

Summary_wrangling.yaml

I noticed a small syntax error in your latest edit at line 21 (a lone dash `-`). Also, your 

![](vscode-file://vscode-app/usr/share/antigravity/resources/app/extensions/theme-symbols/src/icons/files/python.svg)

split_and_explode actions on `genotype`, `phenotype`, etc., will significantly increase the row count. If you perform multiple explodes sequentially:

- **Row Explosion**: If sample `A` has 2 genotypes and 2 plasmids, and you explode them separately, you will end up with **4 rows** for that sample ($2 \times 2$).
- **Recommendation**: If these columns are meant to be synchronized (e.g., the first genotype belongs with the first plasmid), you should use the 
    
    ![](vscode-file://vscode-app/usr/share/antigravity/resources/app/extensions/theme-symbols/src/icons/files/python.svg)
    
    split_to_list + 
    
    ![](vscode-file://vscode-app/usr/share/antigravity/resources/app/extensions/theme-symbols/src/icons/files/python.svg)
    
    explode (multi-column) method we discussed earlier to keep the row count sane.
    

# NOTES 3
You do **not** need to redefine the data type in the `output_fields` if it was already correctly set in the `input_fields`. The Polars engine preserves the data type throughout all transformations until the final export.

Here is the technical breakdown:

### 1. The Persistence Rule

If you set `type: categorical` in the **input**, the column enters the pipeline as a Categorical type. Unless a `wrangling` step explicitly changes it (e.g., a mathematical calculation turning it into a float), it will remain Categorical.

### 2. When to Redefine in Output

You should only redefine the type in `output_fields` if:

- **A wrangling step changed it**: For example, you calculated a ratio that is now a high-precision `Float64`, but you want the output narrowed to `i64` or `categorical`.
- **You want to be "Safe" (Showcase)**: As we discussed, redefining it makes the file a standalone source of truth for the final contract, even if the user hasn't seen the `input_fields` file.

### 3. Efficiency Tip

In your 
```
# Standard selection (uses type from input_fields)
sample_id: {}
# Explicit selection with re-casting (overwrites or confirms type)
genome_length:
type: numeric
```

WARNING

**A Note on `original_name`**: The `original_name` key is **only used during ingestion** to find the header in the raw file. Including it in `output_fields` is ignored by the engine and can be confusing, as the column has already been renamed to its logical slug (e.g., `ST`) by the time it reaches the output stage.

**Recommendation**: For your "Showcase" manifest, keep the `type` and `label` to make it clear what the final product looks like, but you can safely remove `original_name` from the `output_fields` block to keep things clean.
# NOTES 2

### 1. Does the Label "Follow" to Output Fields?

No, the label does not automatically "flow" from `input_fields` to `output_fields` in the YAML structure itself. However, it is **intended to be redundant** for a reason:

- **`input_fields`**: This is your **Metadata Registry**. It defines the "What" and "Who" of each column in the raw data.
- **`output_fields`**: This is your **Contract Gatekeeper**. It defines the "Which" (filtering) and the "How" (final data types for Polars).

### 2. How the UI knows to use it

In the current SPARMVET architecture:

- **Current State**: As we saw in 
    
    ![](vscode-file://vscode-app/usr/share/antigravity/resources/app/extensions/theme-symbols/src/icons/files/python.svg)
    
    server.py, the UI currently uses the standardized **Column Slug** (e.g., `taxon`) for filter titles and headers.
- **Intended Architecture**: The UI is designed to perform a **Lookup Strategy**. When the dashboard renders a filter for `taxon`, it is supposed to query the 
    
    ![](vscode-file://vscode-app/usr/share/antigravity/resources/app/extensions/theme-symbols/src/icons/files/python.svg)
    
    active_cfg to find a matching entry in any of the project's `input_fields` to extract the `label`.

### 3. Redundancy at the Output Level

In your recent change to 

![](vscode-file://vscode-app/usr/share/antigravity/resources/app/extensions/theme-symbols/src/icons/files/yaml.svg)

Summary_output_fields.yaml, you duplicated the `label`. While this is technically redundant (the UI can find it in the input schema), it is **excellent for "Showcase" manifests** because:

1. It keeps the "Final Contract" self-documenting.
2. It ensures that if multiple datasets are joined into an assembly, the specific label you want for the _final_ column is explicitly stated in the contract.

TIP

**Showcase Tip**: For your template, keeping the `label` in `output_fields` is the "Safest" path. It ensures that the human-readable name is explicitly bound to the final published version of that data, regardless of how many joins or transformations it went through.

**Recommendation**: I would keep the labels in both places for the "Showcase" version. It makes the manifest easier to read for a human without having to bounce between different YAML includes.

# NOTES 1

### 2. Implemented Ingestion Controls

> **Question**: "What are the current implemented options to control import?"

The `input_fields` block currently supports these authoritative keys:

- **`original_name`**: Maps the physical TSV/CSV header to your internal logical slug (e.g., `"Detected main taxon"` → `taxon`).
- **`type`**: Triggers automatic Polars casting (`numeric`, `categorical`, `string`/`utf8`, `date`).
- **`label`**: The human-readable string used by the UI components (Persona-masking).
- **`is_primary_key`**: A critical flag used by the `DataAssembler` to identify join anchors for Tier 1 and Tier 2 composition.

### 3. Variable Persistence & Reuse

> **Question**: "Would be nice to be able to keep the values of this in a variable we can reuse later on" (regarding `MLST_scheme`)

The current engine does not support manifest-defined variables for data values yet. However, you can achieve **schema reuse** via YAML inheritance:

- Since you are using `!include`, you can create a standalone `common_fields.yaml` for shared definitions (like `MLST` or `sample_id`) and include the same fragment across different pipeline manifests.
- For persistent metadata (like a "MLST Global Scheme"), we typically handle this in the **Tier 2 Assembly** layer where values are joined from reference datasets (like your `APEC_STEC_virulence_genes`).

### 🛠️ Review of your 
Summary_input_fields.yaml Changes:

1. **Categorical IDs**: Great work changing `sample_id` to `categorical`. This will prevent the join mismatches I observed during the earlier validation run.
2. **Comments Integrity**: I will strictly respect your comments moving forward; they serve as an excellent "Blueprint Gallery" for other developers.
3. **Wrangling vs. Ingestion**: Note that columns like `genotype` marked as `type: string` will require no ingestion logic but will allow you to perform regex or split operations in the `wrangling` block later.

IMPORTANT

**Warning on `output_fields`**: If you define `output_fields: [ ]` (empty list), the system defaults to "Identity Mode" and retains **everything** from the raw file. To drop columns, you must define `output_fields` as a key-value dictionary.

# FAQ 
## Ingestion - Manifest input_fields / output_fields

> **Question**: "Can I omit input_field from the manifest, will this field be removed from the dataset ? eg. if I do not want to ingest the column? (because otherwise I will have to drop it?)

**Short Answer**: Yes, but omitting it from `input_fields` only prevents **standardization** (renaming/casting). To actually **remove** it from the data stream, you must omit it from the `output_fields` contract.

- **Ingestion (Current State)**: The `DataIngestor` performs a "Lazy Scan" of the whole file. If a column is missing from `input_fields`, it remains in the `LazyFrame` with its raw name and inferred type.
- **The Filter Gate**: Per **ADR-013**, the terminal step of every wrangling layer is a `.select()` based on the keys defined in `output_fields`.
- **Recommendation**: To "ingest and forget" a column, you can leave it out of `input_fields` entirely, but you **MUST** ensure it is not present in your corresponding 
    

## Ingestion - Can I omit type and label if my intent is to drop the column from the output?

Yes, you can absolutely omit `type` and `label`. Here is how the engine handles those omissions:

- **`type`**: If omitted, it defaults to **`categorical`**.
- **`label`**: This is purely a UI/Documentation aesthetic. If omitted, the engine simply ignores it and refers to the column by its logical key (e.g., `taxon`).


<u>The "Intent to Drop" Strategy<\u> 

If your goal is to drop the column from the final output, you have three levels of "omission" available:

1. **Omit `type` and `label`**: The column is still ingested and renamed from `"Detected main taxon"` to `taxon`. It will use default categorical casting. You still have to manually exclude it from your   Summary_output_fields.yaml to drop it.
2. **Omit the entire `taxon` entry from `input_fields`**: The column is ingested with its raw name (`"Detected main taxon"`) and an inferred Polars type. You simply don't include that raw name in your `output_fields`, and it disappears at the end of the layer.
3. **Renaming for Wrangling (Most Common)**: Most developers keep the entry in `input_fields` (even without `type/label`) just to give it a clean `original_name` mapping. This makes it easier to refer to the column in a `wrangling` step (e.g., to use it in a filter) before finally dropping it in the `output_fields`.

TIP

**Showcase/Template Recommendation**: For a "Showcase" manifest, it is best practice to keep the entry and define the `type`. It signals to other users that the column exists in the raw data but is being intentionally standardized before being handled by the pipeline.
