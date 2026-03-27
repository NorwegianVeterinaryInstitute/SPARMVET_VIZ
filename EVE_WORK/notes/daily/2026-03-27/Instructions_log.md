# 2026-03-27





- [ ] test one by one the new decorators
- [ ] update documentation (new decorators, architectural decisions)


## Testing 


## New guardrail 
@Agent: @dasharch - PERMANENT WORKSPACE RULE UPDATE.

1. Environment Lock (Rule 5):
- Use ONLY ./.venv/bin/python.

2. Task: Update `./.agents/rules/workspace_standard.md`.
- Section: "ADR-013: The Manifest Data Contract"
    - Rule: All manifests MUST follow the structure: Header (ID/Desc) -> input_fields -> wrangling -> output_fields.
    - Rule: 'output_fields' is a strict Polars .select() contract. It is the final guard against Column Drift.
- Section: "Modular Library Autonomy (The Clear Lines Policy)"
    - Rule: Libraries in ./libs/ are independent, reusable modules. 
    - Rule: Structure MUST be: ./libs/[lib_name]/src/ for logic and ./libs/[lib_name]/tests/ for internal verification.
    - Rule: NO cross-imports between libs (e.g., 'transformer' cannot import 'ingestion').
    - Rule: Orchestration (joining libs) is restricted to the 'app/' layer or top-level 'assets/scripts/'.
- Section: "Python Execution Authority"
    - Rule: Use Editable Mode (pip install -e) for libs. 
    - Rule: Always execute via root ./.venv/bin/python.

3. Cross-Reference Update:
- Update `architecture_decisions.md` to point to these new sections in the workspace rules.

4. Verification:
- Read back the newly added sections to confirm they match the "Clear Lines" philosophy.
- Mirror changes to ./.antigravity/knowledge/.

HALT: Report "Workspace Rules Codified. Boundaries Enforced." @verify

5. Ensure code consistency to the new rules 
- Review the `pyproject.toml` created for `ingestion` and `transformer`. 
- Ensure they do not create "Circular Dependencies." 
- Rule: `libs/transformer` must NOT import from `libs/ingestion`. All cross-library coordination happens in the `app/` layer or via a shared `utils` lib.
- Update `assets/scripts/wrangle_debug.py` to ensure it acts as a "mini-app" that imports both libs correctly without violating their independent structures. 
- Verify that the other scripts use those rules and that __init__.py files are correctly set up to allow imports.

6. Refine Documentation (docs/guide/development_rules.md):
- Add a section: "Modular Boundaries and Reusability."
- Explain that each lib in `./libs/` is a standalone tool.
- Detail the "Clear Lines" policy: Data flows from Ingestor -> App -> Transformer.
- Explain the import strategy: Using `import ingestion` is allowed due to editable installs, but the internal `src/` structure must be respected to maintain local testability.

HALT: Report "Workspace Rules Codified. Boundaries Enforced. Documentation updated." @verify


## Manifest creations for Abromics (Minimum dataset for figures)

@Agent: @dasharch - REFINED WRANGLE DEBUGGER (v2).

1. Environment Lock (Rule 5):
- Use ONLY ./.venv/bin/python.




./.venv/bin/python ./assets/scripts/wrangle_debug.py \
--manifest ./config/manifests/pipelines/1_Abromics_general_pipeline.yaml




---
@Agent: @dasharch - DOCUMENTATION REFINEMENT (The Data Contract).

1. Environment Lock (Rule 5):
- Use ONLY ./.venv/bin/python.
    
2. Task: Create `.assets/scripts/wrangle_debug.py`.
- The script must take 1 argument: `--manifest`.  Deduce the dataset from the 'id' or 'name' field inside the YAML.
- Logic:
    a) Read the general pipeline manifest (./config/manifests/pipelines/1_Abromics_general_pipeline.yaml).
    b) Extract the specific `dataset_id` block.
    c) Use the `ingestion` package to load the LazyFrame via the 'source' block.
    d) Pass the LazyFrame and the wrangling steps to the `DataWrangler`.
    e) Validate vs. `output_fields` (The Contract).
    f) Sink the result to `./tmp/{dataset_id}_debug.tsv` using `df.collect().write_csv(separator='\t')`.


3. Documentation Task: Create/Update `docs/guide/new_data_contract.md`.
- Section 1: The Anatomy of a Manifest.
    - Explain the Header (ID, Description, header Metadata).
    - Explain the data contracts for the different types of datasets (data_schemas, metadata_schema, additional_datasets_schemas). Eg. datasets comming from same pipeline (data_schemas) vs metadata_schema (metadata for the pipeline dataset) vs datasets comming from different pipelines, references datasets, etc (additional_datasets_schemas).
    - Explain the three-block structure that is valid for all dataset types: `input_fields`, `wrangling`, `output_fields`.
    - Use `./config/manifests/pipelines/1_Abromics_general_pipeline.yaml` (active datasets only - uncommented) as the primary code example.
- Section 2: Actions vs. Contracts.
    - Explicitly explain why we separate 'wrangling' (the actions) from 'output_fields' (the final state).
    - Explain that 'output_fields' is the final Polars `.select()` guard.
- Section 3: Preventing Column Drift.
    - Describe how this setup ensures the DataAssembler receives a stable, predictable schema even if raw ingestion changes.
- Section 4: Scaling the Pipeline.
    - Instructions on how to add a new dataset to the general manifest using the same principles.

4. Consistency Check:
- Ensure the documentation matches the actual logic in `libs/ingestion/` and `assets/scripts/wrangle_debug.py`.

5. HALT:
- Mirror the file to ./.antigravity/knowledge/ for session persistence.
- Provide a 3-sentence summary of the new guide. @verify

----

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



