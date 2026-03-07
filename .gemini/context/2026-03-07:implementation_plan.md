# Goal Description

The goal is to implement a **Declarative Wrangling Rules** system for the Dashboard Configuration. This will allow dataset-specific and metadata-specific transformation steps (e.g., splitting comma-separated strings into a long format, filling nulls, etc.) to be defined directly in the YAML configuration dictionaries rather than being hardcoded. 

This requires updating the architecture documentation and defining the anticipated implementation structure for the Polars-backed Wrangler modules.

## User Review Required

No breaking changes to Python code yet, as this is purely a design and documentation step for the architecture. I will update the documentation to finalize how the data contract `data_schema` and `metadata_schema` dictionaries can include a `wrangling` key.

## Proposed Changes

### Documentation

#### [MODIFY] docs/guide/new_data_contract.qmd
- Add a new section detailing how to add a `wrangling` dictionary to both the `data_schema` and `metadata_schema`.
- Define the standard dictionary structure for wrangling steps, using column names as keys and a list of actions as values.
  - Example: `wrangling: { "AMR_genes": [{action: "split_and_explode", separator: ","}, {action: "fill_nulls", value: "None Detected"}] }`

#### [MODIFY] docs/modules/wrangling.qmd
- Update the Module description to explicitly state that the Data Wrangler and Metadata Validator/Joiner read transformation instructions dynamically from the configuration YAML.

### Planning the Codebase changes (Future Implementation)
- We will need to create standard operations in `transformer/data_wrangler.py` and `transformer/metadata_validator.py` (when we build them) that parse a `wrangling` dictionary and map `action` strings to specific Polars LazyFrame operations (`pl.Expr` expressions) for the specified column keys.

## Verification Plan

### Manual Verification
- The USER will review this Implementation Plan and the changes made to the documentation to ensure the declarative dictionary structure meets their expectations for writing the YAML contracts.
