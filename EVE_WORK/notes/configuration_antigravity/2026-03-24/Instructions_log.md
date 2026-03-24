## closing -> as write log, update and put ready new chat for continuing

- See closeout_template.md (only some part to eventually update)


## 3. Building the decorators to wrangle - the first dataset 


--- PREP TESTING PROMPT --- 

- Configure it to load the minimal fake dataset from `./assets/test_data/1_test_data_ST22_dummy/test_data_ResFinder_20260307_105756.tsv` using Polars with the manifest file `./.config/manifests/pipelines/1_Abromics_general_pipeline.yaml`. Solely focus on uncommented parts. and the specific decorator actions testing
- check that it sees all the sub-directories and files associated to this configuration file

--- ADD NEXT TASKS - BLOCKER USER TASKS ---

#EVE BLOCKER USER TASKS : Should implement the following : 
- continue implementation of the pipeline manifest files in `./.config/manifests/pipelines/1_Abromics_general_pipeline/` starting with the wrangling logic for 
   1.`./libs/transformer/src/wrangling/ResFinder_wrangling.yaml` and ask generation of  appropriate decorators
   2. `metadata_schema_wrangling.yaml` and ask generation of  appropriate decorators
- Reminder: Dataset used:  `./assets/test_data/1_test_data_ST22_dummy/test_data_ResFinder_20260307_105756.tsv`





--- TESTING TRANSFORMATION DECORATOR PROTOCOL ---





# 3. Step by step building and user control  - drop_nulls

@Agent: @dasharch - Documentation Update: Decorator Registry & CLI Usage.

1. **Task Completion:** @verify. Mark [drop_nulls] as [DONE] in './.antigravity/tasks/tasks.md'.
2. **Update Documentation:** Augment the 'Decorator Registry' in './docs/modules/wrangling.qmd' appropriate existing guide.
3. **The Universal Testing Command:** Document the standard execution path:
   `.venv/bin/python libs/transformer/tests/test_wrangler.py --data [INPUT_FILE] --manifest [YAML_FILE] --output tmp/USER_debug_view.tsv`
4. **Standard Entry Template:** For each tested decorator (starting with 'drop_nulls'), include:
   - **Description:** A clear functional summary.
   - **Manifest Link:** Provide a relative link to the tested YAML in './libs/transformer/tests/data/'.
   - **Test Data Link:** Provide a relative link to the input TSV/CSV used for the test.
5. **Logic Guardrail (I/O):**
   - **Input:** Flexible (CSV or TSV supported).
   - **Output:** MUST be TSV. Ensure 'test_wrangler.py' uses `include_header=True, separator="\t"` for the final write.
6. **STOP:** Present the documentation entry for 'drop_nulls' and confirm which decorator is next.



--- 

@Agent: @dasharch - Execute Sequential Verification for [drop_nulls].

1. **Step A: The Contract (TSV + YAML):**
   - Generate './libs/transformer/tests/data/drop_nulls_test.tsv' with meaningful bacterial metadata (include nulls in numeric and categorical columns).
   - Generate './libs/transformer/tests/data/drop_nulls_manifest.yaml' defining the drop logic.
   - **HALT:** "Contract for [drop_nulls] is ready. Please verify the TSV and YAML. Waiting for @verify."

2. **Step B: Execution for [drop_nulls]:**
   - Run the universal script: `.venv/bin/python libs/transformer/tests/test_wrangler.py --data ./libs/transformer/tests/data/drop_nulls_test.tsv --manifest ./libs/transformer/tests/data/drop_nulls_manifest.yaml --output tmp/drop_nulls_debug_view.tsv`.

3. **Step C: Evidence & Inspection:**
   - Materialize results to 'tmp/USER_debug_view.tsv' and 'tmp/drop_nulls_debug_view.tsv'.
   - Print `df.glimpse()` to the terminal.
   - **HALT:** "Execution complete. Check USER_debug_view.tsv in Excel Viewer. Waiting for @verify to mark as [DONE]."






# 2. Step by step building and user control  - FILL NULLS



---


@Agent: @dasharch - Documentation Update: Decorator Registry & CLI Usage.

1. **Task Completion:** @verify ok. Mark [fill_nulls] as [DONE] in './.antigravity/tasks/tasks.md'.
2. **Update Documentation:** Augment the 'Decorator Registry' in './docs/modules/wrangling.qmd' appropriate existing guide.
3. **The Universal Testing Command:** Document the standard execution path:
   `.venv/bin/python libs/transformer/tests/test_wrangler.py --data [INPUT_FILE] --manifest [YAML_FILE] --output tmp/USER_debug_view.tsv`
4. **Standard Entry Template:** For each tested decorator (starting with 'fill_nulls'), include:
   - **Description:** A clear functional summary.
   - **Manifest Link:** Provide a relative link to the tested YAML in './libs/transformer/tests/data/'.
   - **Test Data Link:** Provide a relative link to the input TSV/CSV used for the test.
5. **Logic Guardrail (I/O):**
   - **Input:** Flexible (CSV or TSV supported).
   - **Output:** MUST be TSV. Ensure 'test_wrangler.py' uses `include_header=True, separator="\t"` for the final write.
6. **STOP:** Present the documentation entry for 'fill_nulls' and confirm which decorator is next.



--- 

@Agent: @dasharch - Execute Phase 1: Sequential Verification for [fill_nulls].

1. **Context & Rules Sync:**
   - Read './agents/rules/workspace_standard.md' and './agents/workflows/verification_protocol.md'.
   - Confirm active root .venv and TSV/CLI-Argparse standards.

2. **Step A: The Contract (TSV + YAML):**
   - Generate './libs/transformer/tests/data/fill_nulls_test.tsv' with meaningful bacterial metadata (include nulls in numeric and categorical columns).
   - Generate './libs/transformer/tests/data/fill_nulls_manifest.yaml' defining the fill logic.
   - **HALT:** "Contract for [fill_nulls] is ready. Please verify the TSV and YAML. Waiting for @verify."

--- 

@Agent: @dasharch - Universal Runner Implementation and execution for [fill_nulls]

1. **Step A: The Universal Runner (test_wrangler.py):**
   - Refactor './libs/transformer/tests/test_wrangler.py' to be entirely generic.
   - **Logic:** It must load any `--data` (.tsv) and any `--manifest` (.yaml), then use the `DataWrangler.apply_wrangling_rules()` to process the data.
   - **CLI:** Strictly maintain `argparse` for --data, --manifest, and --output.

2. **Step B: Execution for [fill_nulls]:**
   - Run the universal script: `.venv/bin/python libs/transformer/tests/test_wrangler.py --data ./libs/transformer/tests/data/fill_nulls_test.tsv --manifest ./libs/transformer/tests/data/fill_nulls_manifest.yaml --output tmp/fill_nulls_debug_view.tsv`.
3. **Step C: Evidence & Inspection:**
   - Materialize results to 'tmp/USER_debug_view.tsv' and 'tmp/fill_nulls_debug_view.tsv'.
   - Print `df.glimpse()` to the terminal.
   - **HALT:** "Execution complete. Check USER_debug_view.tsv in Excel Viewer. Waiting for @verify to mark as [DONE]."


# Step by step building and user control 
- implemented workflow rule for one step at the time
- instructions that dasharch must respect the user testing protocol 

# 1. Recheck completness and consistency with a thinking model
--- 


- [x] Recheck completness and consistency with a thinking model
> for this used planning and high model 

@Agent: @dasharch - Full Project & Documentation Congruence Audit (The "Zero-Debt" Scan).
1. Read : `./.antigravity/rules/workspace_standard.md` and `./.antigravity/workflows/verification_protocol.md`
2. **The Vision-Reality Audit:** Use a deep-thinking model to cross-reference our 'Planned Logic' against our 'Current Implementation'.
   - **Plans:** `./.antigravity/plans/implementation_plan_master.md`, `./.antigravity/knowledge/architecture_decisions.md`, and `./.antigravity/tasks/tasks.md`.
   - **Implementation:** All files in `./libs/`, `./app/`, `./assets/`, and `./config/`.
   - **Documentation:** All files in `./docs/`.

3. **Global Search for "Legacy Contaminants":** Scan every file in the repository for:
   - **Format Drift:** References to `.csv` or `sep=","` (must be updated to `.tsv` and `sep="\t"`, `.json`  instead of `.yaml`).
   - **CLI Compliance:** Any Python script in `src/` or `tests/` lacking `argparse` support (must support manual execution).
   - **Pathing Errors:** Hardcoded absolute paths (e.g., `/Users/...`) or incorrect relative links in `pyproject.toml` files.

4. **Detection Points for Inconsistency:**
   - **Protocol Mismatch:** Does the Master Plan or docs omit the 'v1.6 Verification Protocol' (TSV + CLI + @verify)?
   - **Dead Tasks:** Are there [TODO] tasks in `tasks.md` that contradict current `blockers.md` or `milestones.md`?
   - **Metadata Sync:** Does the test data in `assets/` match the schemas defined in the `knowledge/` ADRs?

5. **Actionable Report (The Debt List):**
   - List every 'Incongruent File' found.
   - For each item, provide a one-line 'Proposed Reconciliation' (e.g., "Update docs/README.md to reflect TSV standard").
   - **DO NOT APPLY FIXES YET.**

6. **STOP:** Present this Audit Report and wait for my @verify to begin the cleanup or switch to the fast execution model.

---
- [x] Need to merge the paths and force it to use one source of truth


@Agent: @dasharch - Execute Knowledge Audit & Rule Formalization.

1. **Audit Knowledge Directory:** Scan all Markdown files in `./.antigravity/knowledge/`.
2. **Define Usage Rules:** For each file found, determine its unique role in our workflow (e.g., ADRs, long-term memory, technical constraints).
3. **Update Workspace Standard:** 
   - Edit './agents/rules/workspace_standard.md' to include the 'Logic Source of Truth' section.
   - List each path with a short description of its content AND a specific 'Rule of Usage' (e.g., 'Check this file before every new implementation').
4. **Clean & Consolidate:** 
   - If any information is duplicated between files, consolidate it into the most logical human-readable file.
   - Delete any empty or redundant sub-directories in `./.antigravity/knowledge/`.
5. **STOP:** Present the new 'Logic Source of Truth' table from the workspace standard and confirm your commitment to using these files consistently.



@Agent: @dasharch - Permanent Path Authority Lock.

1. **Acknowledge Current Tree:** Note the existing structure in ./.antigravity/. This is now the ONLY authorized pathing schema.
2. **Consolidation Finalization:**
   - Use `./.antigravity/tasks/tasks.md` as the sole source of truth for execution.
   - Use `./.antigravity/plans/implementation_plan_master.md` as the sole roadmap.
   - Delete `./.antigravity/tasks/initialization_task.md` once its contents are merged into the main `tasks.md`.
   - homogenize usage of each required artifact, log and knowledge files
3. **Update Workspace Standard:** Ensure ./.agents/rules/workspace_standard.md reflects these exact paths and forbids the creation of any new top-level folders in ./.antigravity/.




--- 

- [x] Need to merge implementation plans 

@Agent: @dasharch - ARCHITECTURAL CONSOLIDATION REQUIRED.

1. **The Goal:** Merge `implementation_plan_current.md`, `implementation_plan_restoration.md`, and `implementation_plan_v2.md` into ONE file: `./.antigravity/plans/implementation_plan_master.md`.
2. **Priority Logic:**
   - Favor **v2** for high-level architecture.
   - Favor the **restoration** plan for the root .venv and modular lib setup.
   - **MANDATORY:** Include the v1.6 Verification Protocol (TSV-default, CLI-argparse for all tests, and @verify gates).
3. **Conflict Resolution:** If you find contradictory instructions between the three plans, you MUST stop and ask me for clarification. Do not guess.
4. **Cleanup:** Once the 'master' plan is verified by me, delete the 3 old versions to prevent future logic drift.
5. **Instruction Update:** Update 'workspace_standard.md' to reflect that `implementation_plan_master.md` is now the ONLY authoritative roadmap.
6. **STOP:** Present the table of contents and the 'Verification Rules' section of the new Master Plan for my review.
---

- [x] Need to ensure it keep the argparse and allow me to run the tests on the python  -> rule added