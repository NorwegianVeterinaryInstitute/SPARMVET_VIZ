# Pipeline Ingestion Strategy: Native Nested/Multi-Dataset

## The Architectural Challenge
Bioinformatic pipelines output results in multi-sheet Excel files (e.g., one sheet for ResFinder, one for MLST, one for PlasmidFinder). These sheets have fundamentally different structures and lengths (e.g., one row per sample vs. multiple mutation rows per sample). 

## The Recommendation: Native Nested Multi-Dataset
I agree completely with your assessment. Transforming this into a "Wide Table" requires mathematical aggregations that destroy the granularity of the data. 

To maintain the exact structure of the results and allow for independent, specialized visualizations, the Dashboard Architecture will officially adopt a **Native Nested Multi-Dataset** strategy.

### 1. Data Contract (`data_schema`) Updates
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
The backend will read the central `metadata` table once. It will then loop through every dataset defined in the `data_schemas` contract. For each dataset, it will perform a clean Left Join with the metadata on the `sample_id`. This means every individual Result dataset now has all the context (Country, Date, Species) it needs for visualization, without inflating row counts.

### 3. The Visualization Factory Update
Since different datasets require different visual representations, the plots will be explicitly bound to a dataset in the configuration:

```yaml
requested_plots:
  - id: "amr_heatmap"
    target_dataset: "resfinder_results"
    x_axis: "gene_name"
```

## Proposed Changes: The Excel Extractor Script
We will still build the helper script `parse_pipeline_excel.py`, but its job is much simpler now! It doesn't need to join anything.

#### [NEW] `assets/scripts/parse_pipeline_excel.py`
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
