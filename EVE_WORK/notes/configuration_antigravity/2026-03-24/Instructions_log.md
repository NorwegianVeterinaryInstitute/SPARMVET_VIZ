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


- [ ] Need to merge tasks


--- 

- [ ] Need to merge implementation plans 

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