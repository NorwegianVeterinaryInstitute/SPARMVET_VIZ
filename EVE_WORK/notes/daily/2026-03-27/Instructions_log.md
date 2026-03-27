# 2026-03-27





- [ ] test one by one the new decorators
- [ ] update documentation (new decorators, architectural decisions)

## Testing 


## Manifest creations for Abromics (Minimum dataset for figures)

- The user has created a general manifest, it contains manifest for several datasets 
- we need a solution to add the path of the dataset in the manifest so it can easily be used by the system for testing (note later on this path might be a variable as the data will be fetched from api or for adatabase - so we need a flexible solution that will allow determine how the data is loaded)
- the general manifest is in ./config/manifests/pipelines/1_Abromics_general_pipeline.yaml - comments mask datasets that are not yet implemented (keep those as is). We need to test if all the different datasets can be loaded and processed correctly. 
- The datasets are currently in ./assets/test_data/1_test_data_ST22_dummy/ directory, ./assets/test_data/2_VIGAS-P_ST22_dummy and ./assets/ref_data/Virulence_genes_APEC


@Agent: @dasharch - MULTI-SOURCE ALIGNMENT (Phase 4 Preparation).

1. Environment Lock (Rule 5): 
- Use ONLY ./.venv/bin/python.

2. General Manifest Update:
- Open `./config/manifests/pipelines/1_Abromics_general_pipeline.yaml`.
- For each active (uncommented) dataset, implement a `source` block:
    ```yaml
    source:
      type: "local_tsv" # Flexible for future 'api' or 'db' types
      path: "./assets/test_data/1_test_data_ST22_dummy/filename.tsv"
    ```
- Use the following directory mappings for the active datasets:
    - Group 1: ./assets/test_data/1_test_data_ST22_dummy/
    - Group 2: ./assets/test_data/2_VIGAS-P_ST22_dummy/
    - Group 3 (Ref): ./assets/ref_data/Virulence_genes_APEC/

3. Ingestion Logic Adaptation:
- Modify `libs/ingestion/src/ingestor.py` (or relevant loader) to:
    a) Read the `source` block from the manifest.
    b) If `type == "local_tsv"`, resolve the path relative to the project root.
    c) Ensure it remains compatible with Polars `scan_csv`.

4. Batch Validation Test:
- Use the Universal Runner or a new loop script to verify that all active datasets in the general manifest can be reached and read into a LazyFrame.
- Report a "Connectivity Table" (Dataset ID | Path | Status).

5. HALT:
- Do NOT uncomment hidden datasets.
- Save changes to the local workspace mirror. @verify


--- Tesing creation of input_fields manifest ---


----

For dataset `./assets/test_data/1_test_data_ST22_dummy/test_data_MLST_results_20260307_105756.tsv` 
- Need creation input_fields manifest (not the global one, so maybe we should have the way to have a script that only create the input fields manifest - could be an option from /home/evezeyl/Documents/Insync/gdrive/OBSWORK/20_GITS/SPARMVET_VIZ/assets/scripts/SF_create_manifest.py script)
-  Need creation output_fields : keep columns : sample_id, Sequence Type
- Need maybe a solution to store a value from Scheme column (unique value - so it can eg be used as information for a plot later on or a method information later on . Here it would be eg . used Scheme: ecoli_achtman_4) - Usure if it could be easy (if not we can keep that for later on - We can write that as a defer solution to find)


- create input_fields manifest for ./assets/test_data/1_test_data_ST22_dummy/test_metadata_20260307_105756.tsv

We will have to create the input_fields manifest in ./config/manifests/pipelines/1_Abromics_general_pipeline directory

The user will create the wrangling and output_fields manifests


@Agent: @dasharch - MANIFEST GENERATION (MLST & Metadata).

1. Environment Lock (Rule 5):
- Execute using ONLY ./.venv/bin/python.

2. Script Enhancement:
- Read `assets/scripts/SF_create_manifest.py`.
- Add a `--mode` argument with options: `full` (default) or `input_only`.
- In `input_only` mode, the script should ONLY generate the `input_fields` block based on Polars schema inference and leave `wrangling` and `output_fields` as empty lists `[]`.

3. Task - MLST Manifest:
- Generate input-only manifest for: `./assets/test_data/1_test_data_ST22_dummy/test_data_MLST_results_20260307_105756.tsv`
- Save to: `./config/manifests/pipelines/1_Abromics_general_pipeline/MLST_results_manifest.yaml`

4. Task - Metadata Manifest:
- Generate input-only manifest for: `./assets/test_data/1_test_data_ST22_dummy/test_metadata_20260307_105756.tsv`
- Save to: `./config/manifests/pipelines/1_Abromics_general_pipeline/test_metadata_manifest.yaml`

5. Metadata Extraction (Conceptual):
- Identify the unique value in the 'Scheme' column of the MLST data.
- Do NOT implement a solution yet. Log this requirement in ./.antigravity/knowledge/blockers.md as: "ST22-001: Implement Metadata Constant Extraction for global plot labels."

6. HALT:
- Confirm both YAML files exist in the target directory.
- Print the first 5 lines of each to verify ADR-013 structure. @verify



## Initiation

@Agent: @dasharch - SYSTEM INITIALIZATION 
1. Mandatory Context Injection (Read First):
- ./.agents/rules/workspace_standard.md (The Law)
- ./.antigravity/knowledge/architecture_decisions.md (The History)
-  ./.agents/workflows/verification_protocol.md (procedure)

2. Environment Lock ( NON-NEGOTIABLE):
- You MUST use the root `./.venv/bin/python`. 
- Verify now: Run `which python` and `python -c "import sys; print(sys.prefix)"`. 
- If it is NOT the project .venv, STOP and report the error.

3. Execution Protocol (Rule 11 & ADR-013):
- Manifests now use: input_fields -> wrangling -> output_fields.
- Do NOT execute tasks autonomously. The user will prompt for specific tasks
- Every task must end with a HALT and a request for @verify.

Confirm your environment is locked to ./.venv and you are ready for Phase 3 manual verification support. @verify

--- 
@Agent: Assume persona @dasharch.
Welcome back. Before generating any code or executing steps, you MUST fulfill the following contextual handoff requirements:
**Read `./EVE_WORK/notes/daily/2026-03-27/Instructions_log.md`** This is the log from yesterday. W we will continue where we left off.

---



