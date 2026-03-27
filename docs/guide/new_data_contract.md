# The Abromics Data Contract (ADR-013, ADR-014, ADR-015)

This guide explains the manifest-driven architecture used to ensure predictable data ingestion and transformation across the pipeline.

## 1. Anatomy of a Manifest
Every dataset in the SPARMVET system is governed by a YAML manifest. These can be **standalone** files or **blocks** within a general pipeline manifest (e.g., `./config/manifests/pipelines/1_Abromics_general_pipeline.yaml`).

### The Header
*   **id**: Unique identifier for the pipeline or dataset.
*   **type**: Typically `pipeline` or `dataset`.
*   **info**: Metadata including `display_name`, `version`, and `tags`.

### The Three-Block Structure (Hybrid Schema)
All datasets follow a mandatory three-block logical flow:

1.  **input_fields**: Defines the raw incoming data. Acts as the "Ingestion Schema".
2.  **wrangling**: An ordered list of atomic actions (e.g., `rename_columns`, `regex_extract`) applied to the LazyFrame.
3.  **output_fields**: The **Published Contract**. Defines the final columns and types that will be exposed to the `DataAssembler`.

---

## 2. Manifest Types & Categories
The general manifest organizes datasets into three functional categories:

*   **data_schemas**: The primary datasets coming from the same pipeline (e.g., `MLST_results`).
*   **metadata_schema**: The sample-level metadata (e.g., Country, Year) that ties the datasets together.
*   **additional_datasets_schemas**: References or external datasets (e.g., `VirulenceFinder` from VIGAS-P, or reference gene lists).

Regardless of category, all datasets must implement the three-block structure to ensure architectural homogeneity.

---

## 3. Actions vs. Contracts (The Final Guard)
A common pitfall is assuming that the last action in `wrangling` defines the final schema. In this system:

*   **Wrangling** is the *Process*: It defines HOW we get from A to B.
*   **Output Fields** is the *State*: It defines WHAT is allowed to leave the module.

**The Polars Guard**: The pipeline implements an explicit `.select()` at the very end of processing, using the keys defined in `output_fields`. Even if raw data adds 10 new columns, the `DataAssembler` only sees what is explicitly contracted.

---

## 4. Preventing "Column Drift"
By separating actions from state, we prevent "Column Drift"—a scenario where changes in upstream scripts or raw data formats break downstream joins. The `DataAssembler` relies on the stability of the `output_fields` contract to perform reliable joins across multiple sources.

### ADR-014: Identity Logic
If a dataset requires no processing (e.g., a clean reference TSV):
*   Set `wrangling: []` to bypass the transformation block.
*   Set `output_fields: []` to retain all columns from the input.

---

## 5. Scaling: Adding a New Dataset
To add a new data source to the `1_Abromics_general_pipeline.yaml`:

1.  **Add a `source` block** (ADR-015):
    ```yaml
    source:
      type: "local_tsv"
      path: "./assets/path/to/data.tsv"
    ```
2.  **Define `input_fields`**: Map the raw columns. Use `!include` for cleaner organization.
3.  **Define `wrangling`**: Add the necessary atomic actions.
4.  **Define `output_fields`**: Specify the final columns for the dashboard.
5.  **Verify**: Run the debugger:
    ```bash
    ./.venv/bin/python ./assets/scripts/wrangle_debug.py --manifest ./config/manifests/pipelines/1_Abromics_general_pipeline.yaml
    ```

---

## Code Example (MLST Excerpt)
```yaml
MLST_results: 
  source:
    type: "local_tsv"
    path: "./assets/test_data/1_test_data_ST22_dummy/test_data_MLST_results_20260307_105756.tsv"
  input_fields: !include '1_Abromics_general_pipeline/MLST_input_fields.yaml'
  wrangling: !include '1_Abromics_general_pipeline/MLST_wrangling.yaml'
  output_fields: !include '1_Abromics_general_pipeline/MLST_output_fields.yaml'
```
