# Pipeline Ingestion Strategy: Native Nested/Multi-Dataset

## The Architectural Challenge
Bioinformatic pipelines output results in multi-sheet Excel files (e.g., one sheet for ResFinder, one for MLST, one for PlasmidFinder). These sheets have fundamentally different structures and lengths (e.g., one row per sample vs. multiple mutation rows per sample). 

## The Recommendation: Native Nested Multi-Dataset
I agree completely with your assessment. Transforming this into a "Wide Table" requires mathematical aggregations that destroy the granularity of the data. 

To maintain the exact structure of the results and allow for independent, specialized visualizations, the Dashboard Architecture will officially adopt a **Native Nested Multi-Dataset** strategy.

### 1. Data Contract ([data_schema](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/libs/utils/src/loader2.py#46-49)) Updates
The YAML data contract will be updated to define multiple nested schemas, one for each "result type" (sheet):

```yaml
data_schemas:
  resfinder_results:
    is_primary_key: "sample_id"
    fields:
      gene_name: {type: "categorical"}
      identity_pct: {type: "numeric"}
  mlst_results:
    is_primary_key: "sample_id"
    fields:
      Sequence_Type: {type: "categorical"}
```

### 2. The Polars Ingestion / Orchestration Update
Instead of handing the visualization factory one giant `pl.DataFrame`, the Ingestion layer will produce a **Dictionary of DataFrames**:

```python
{
  "resfinder_results": <Polars DataFrame (joined with Metadata)>,
  "mlst_results": <Polars DataFrame (joined with Metadata)>
}
```

**The Join Logic:**
The backend will read the central [metadata](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/libs/utils/src/loader2.py#42-45) table once. It will then loop through every dataset defined in the [data_schemas](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/libs/utils/src/loader2.py#46-49) contract. For each dataset, it will perform a clean Left Join with the metadata on the `sample_id`. This means every individual Result dataset now has all the context (Country, Date, Species) it needs for visualization, without inflating row counts.

### 3. The Visualization Factory Update
Since different datasets require different visual representations, the plots will be explicitly bound to a dataset in the configuration:

```yaml
requested_plots:
  - id: "amr_heatmap"
    target_dataset: "resfinder_results"
    x_axis: "gene_name"
```

## Proposed Changes: The Excel Extractor Script
We will still build the helper script [parse_pipeline_excel.py](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/assets/scripts/parse_pipeline_excel.py), but its job is much simpler now! It doesn't need to join anything.

#### [NEW] [assets/scripts/parse_pipeline_excel.py](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/assets/scripts/parse_pipeline_excel.py)
A utility script that reads a multi-sheet Excel report and exports a structured directory of clean TSVs.

**Features:**
- Takes a `--config` YAML file mapping sheet names to cleaner dataset names, and specifying their specific primary keys (e.g., `Sheet_1: {name: "resfinder_results", pkey: "Sample ID"}`).
- Renames the targeted primary keys to a standard `sample_id` column for all sheets.
- Exports each requested sheet as its own separate `dataset_name.tsv` file into a target directory (e.g., `assets/test_data/pipeline_A/`).
- The dashboard's local file connector can then simply be pointed to this directory!

## User Review Required
> [!IMPORTANT]
> **Architecture Decision:** Does this Nested Multi-Dataset architecture perfectly capture the modularity and simplicity you need for handling diverse pipeline results?
> 
> **Excel Script Logic:** Since we aren't joining the sheets, the Excel script will simply standardize their ID column and save them out as separate distinct TSV files in a folder. Does this sound correct?

---

# Declarative Wrangling: AMR Categorization (Preserving Grain)

## The Architectural Challenge
Pipelines like ResFinder generate a `target_column` (e.g. `CGE_Predicted_Phenotype`) that contains **comma-separated strings** of multiple resistance genes (e.g., `Amoxicillin, Ampicillin`). 
We want to map these to broader `AMR Categories` (e.g., `Beta-lactams`) using an external Reference TSV.

**CRITICAL RULE:** We *cannot* permanently explode the dataframe into a "Long Format" because we must preserve the original raw pipeline data and strictly maintain the dataframe's grain (1 row = 1 sample). Exploding the rows would inflate the sample counts across the dashboard!

## The Recommendation: The "Explode-Join-Collapse" Pattern

Instead of mutating the table, the wrangling logic will execute a temporary sub-query that calculates the summarized categories and securely joins them back as a **NEW** column (`AMR_Categories`), leaving the raw data untouched.

### Step-by-Step Polars Logic

1. **`split_to_list`**: Read the `CGE_Predicted_Phenotype` column and split the strings into a true Polars `List` column (e.g. `["Amoxicillin", "Ampicillin"]`).
2. **[explode](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/libs/transformer/src/registry.py#17-27)**: Temporarily flatten this list so we have 1 row per gene.
3. **`lookup_categories`**: Perform a Left Join against `test_amr_categories_phenotype.tsv` to discover the broad `AMR Category` for every gene.
4. **`collapse_unique`**: Group back together down to the `sample_id` level. Because a sample might have both Amoxicillin and Ampicillin, it will have two "Beta-lactams" rows. We use `.unique()` to deduplicate them, and then `.str.join(", ")` to collapse them back into a neat string column: `"Beta-lactams"`.
5. **`append_column`**: Finally, attach this newly synthesized `AMR_Categories` string column securely onto the original, unmutated dataframe!

### Example Expected YAML Architecture (Fully Modular)

As requested, the [wrangling](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/libs/transformer/src/data_wrangler.py#38-76) block and the data schema fields will be independently modularized using the `!include` syntax. This isolates the data definitions from the Python execution instructions, making it extremely clean to parse and test independently.

**In the Master File ([1_Abromics_general_pipeline.yaml](file:///home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/config/manifests/pipelines/1_Abromics_general_pipeline.yaml)):**
```yaml
data_schemas:
  ResFinder:
    fields: !include '1_Abromics_general_pipeline/ResFinder_fields.yaml'
    wrangling: !include '1_Abromics_general_pipeline/ResFinder_wrangling.yaml'
```

**In the Wrangling Rules Fragment (`1_Abromics_general_pipeline/ResFinder_wrangling.yaml`):**
```yaml
- action: "derive_categories"
  source_column: "CGE_Predicted_Phenotype"
  target_column: "AMR_Categories_Summary"      
  separator: ", "
  reference_file: "config/references/amr_phenotypes/test_amr_categories_phenotype.tsv"
  lookup_left: "CGE_Predicted_Phenotype"
  lookup_right: "Predicted Phenotype"
  extract_column: "AMR Category (Class)"
```

---

# The Reference Catalogue Architecture

## The Challenge
External databases (like AMR phenotype mappings or custom sequence type lists) provide critical **Interpretation Context** to the raw pipeline results. These files evolve over time, and developers need to know exactly what reference datasets are available to use in their `lookup_join` or `derive_categories` wrangling rules without opening every file.

## The Solution: The Formatted Reference Directory
We will manage these files strictly within the `config/references/` directory. 
To serve as a maintainable "catalogue", every distinct reference subject must reside in its own dedicated subdirectory containing the raw `.tsv` files and a required `README.md`.

**Example Catalogue Structure:**
```text
config/references/
├── amr_phenotypes/
│   ├── test_amr_categories_phenotype.tsv
│   ├── who_priority_list_2026.tsv
│   └── README.md                    # Mandatory: Describes the TSVs, their columns, and their update cycles.
├── geographic_regions/
│   ├── norwegian_counties.tsv
│   └── README.md
```

### Why this approach?
1. **Discoverability:** A developer looking for AMR mappings opens `config/references/amr_phenotypes/README.md` and instantly understands the available interpretation contexts and exactly what columns they can extract using the wrangling rules.
2. **"Just-in-Time" Autonomy:** By directly pointing to these governed paths in the `_wrangling.yaml` files (e.g., `reference_file: "config/references/amr_phenotypes/test_amr_categories_phenotype.tsv"`), the data contract remains totally decoupled from the system startup sequence, ensuring maximum performance. 
3. **Traceability:** As these databases evolve (e.g., adding a new AMR class), the changes are strictly tracked in Git alongside the updated `README.md`.
