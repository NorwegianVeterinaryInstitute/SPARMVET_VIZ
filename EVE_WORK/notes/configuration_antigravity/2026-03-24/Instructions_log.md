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


## 2. Step by step building and user control 
- implemented workflow rule for one step at the time
- instructions that dasharch must respect the user testing protocol 


--- TESTING TRANSFORMATION DECORATOR PROTOCOL ---



@Agent: @dasharch - Execute Step: Sequential Decorator Audit & Task Initialization.
1. **Protocol & Environment Re-Sync:** 
   - **Protocol Sync:** Strictly follow './agents/workflows/verification_protocol.md' using root `./.venv/` , the updated './agents/rules/dasharch.md' and './agents/rules/workspace_standard.md' to ensure all modular package rules are active.
2. **Phase 0: Task Inventory (The List):** 
   - Before any testing, scan the transformer library and create a complete list of all registered decorators/functions (e.g., drop_duplicates, summarize, etc.).
   - Update `./.antigravity/tasks/tasks.md` with a sub-task for EACH individual decorator.
   - **STOP:** Present this list to me and wait for my 'Inventory Confirmed' signal.
3. **Phase 1: Sequential Testing (One-by-One):**
   - Once confirmed, start ONLY with the first decorator in the list.
   - Open and if necessary update `./libs/transformer/tests/test_wrangler.py` if required so it can be used to test this decorator. Do not remove any other test functionality. 
   - Generate the test data and associated manifest / data contract:   `./libs/transformer/tests/data/[ACTION_NAME]_test.csv` and `./libs/transformer/tests/data/[ACTION_NAME]_manifest.yaml`.
   - **TRIGGER CONTRACT HALT:** : "Test data and manifest ready for decorator : [ACTION NAME]. Please check the files. Plase confirm before pursing." Wait for `@confirm_contract` before pursing.  
4. **Evidence:** 
- (After @confirm_contract) Run `pytest libs/transformer/tests/test_wrangler.py` using the validated test data and manifest for this decorator.
   - Materialize the result to `tmp/USER_debug_view.csv` and print `df.glimpse()`.
   - **HALT:** "Wrangling test complete. Please check the results in Excel Viewer and the terminal glimpse. Waiting for @verify to mark as [DONE]".


--- 

- [ ] Recheck completness and consistency with a thinking model

@Agent: @dasharch - Full Project & Documentation Congruence Audit (The "Zero-Debt" Scan).
1. **The Vision-Reality Audit:** Use a deep-thinking model to cross-reference our 'Planned Logic' against our 'Current Implementation'.
   - **Plans:** `./.antigravity/plans/implementation_plan_master.md`, `./.antigravity/knowledge/architecture_decisions.md`, and `./.antigravity/tasks/tasks.md`.
   - **Implementation:** All files in `./libs/`, `./app/`, `./assets/`, and `./config/`.
   - **Documentation:** All files in `./docs/`.

2. **Global Search for "Legacy Contaminants":** Scan every file in the repository for:
   - **Format Drift:** References to `.csv` or `sep=","` (must be updated to `.tsv` and `sep="\t"`, `.json`  instead of `.yaml`).
   - **CLI Compliance:** Any Python script in `src/` or `tests/` lacking `argparse` support (must support manual execution).
   - **Pathing Errors:** Hardcoded absolute paths (e.g., `/Users/...`) or incorrect relative links in `pyproject.toml` files.

3. **Detection Points for Inconsistency:**
   - **Protocol Mismatch:** Does the Master Plan or docs omit the 'v1.6 Verification Protocol' (TSV + CLI + @verify)?
   - **Dead Tasks:** Are there [TODO] tasks in `tasks.md` that contradict current `blockers.md` or `milestones.md`?
   - **Metadata Sync:** Does the test data in `assets/` match the schemas defined in the `knowledge/` ADRs?

4. **Actionable Report (The Debt List):**
   - List every 'Incongruent File' found.
   - For each item, provide a one-line 'Proposed Reconciliation' (e.g., "Update docs/README.md to reflect TSV standard").
   - **DO NOT APPLY FIXES YET.**

5. **STOP:** Present this Audit Report and wait for my @verify to begin the cleanup or switch to the fast execution model.

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