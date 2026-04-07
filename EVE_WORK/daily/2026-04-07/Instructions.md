# Instructions and work log

date:: 2026-04-07

## Stage 4 actually
>
> + fixing the stupid simplink and retest !

@Agent: Execute "Structural Repair & Task Ledger Reconciliation" (Phase 11-D).

I. OBJECTIVE
Repair the library directory structures (remove symlinks) and reconcile the Phase 3 Persistence tasks to eliminate duplicates and align with the new Data-Source-Centric tiering doctrine.

II. TASK 1: DIRECTORY REPAIR (LIBS/)
The current 'transformer -> src' and 'viz_factory -> src' structure is incorrect. We require physical, standard packaging.

1. Remove all symbolic links in ./libs/.
2. Ensure every library (transformer, viz_factory, ingestion, connector, utils) follows this exact physical layout:
   + libs/{lib}/pyproject.toml
   + libs/{lib}/README.md
   + libs/{lib}/src/ (Contains all functional package code)
   + libs/{lib}/tests/ (Contains all debug scripts and /data/ folder)
3. Use 'mv' and 'rm' commands to fix this physically. Do NOT use symlinks.

III. TASK 2: TASK LEDGER RECONCILIATION (tasks.md)

1. Read ./.antigravity/tasks/tasks.md.
2. Identify and DELETE all duplicated task blocks.
3. Re-index Phase 3 (Persistence Layer) to reflect the new doctrine:
   + "Implement Tier 1 (Trunk) persistence (sink_parquet) anchored on Common Data Source ID/Path."
   + "Implement Tier 2 (Branch) pre-aggregation shared by Functional Plot Groups."
   + "Verify that 'Short-Circuit' logic correctly identifies existing Parquet anchors to prevent 22-min re-renders."

IV. TASK 3: RE-VERIFICATION OF REFRESHED LIBS

1. Once directories are moved, confirm 'pip install -e ./libs/{lib}' is still valid in the root .venv.
2. Run 'libs/transformer/tests/transformer_integrity_suite.py' once to ensure the directory move didn't break import paths.

V. FINAL HALT
+ Provide a clear summary of the physical directory changes (from/to).
+ Confirm duplication removal in tasks.md.
+ Provide a "One-line State of Truth" regarding the structural integrity.
+ Await @verify.

## Stage 3

@Agent: Execute "Surgical Architectural Finalization" (Phase 11-C).

I. OBJECTIVE
Finalize the homogenization of project rules, persona protocols, and testing logic. You must ensure strict boundary enforcement and optimize data processing for large, multi-source manifests.

II. MANDATORY UPDATES

1. Boundary Lock (.aiignore at Root):
   + Update `rules_runtime_environment.md` and `dasharch.md`.
   + Command: "The agent MUST strictly respect the .aiignore file located at the project root. Do not scan directories like EVE_WORK, archives, or .antigravity/embeddings/ unless the user explicitly grants a 'Border-Crossing Permit' for a specific file."

2. Tiered Data (Data-Source Centric Sharing):
   + Update `rules_data_engine.md`.
   + Redefine the 'Bifurcation Point' for large manifests (e.g., ResFinder, Virulence Finder):
     + Tier 1 (The Trunk): Relational Anchor. Logic applied to a common data source (identified by ID or Path) that is shared by ALL plots dependent on that source.
     + Tier 2 (The Branch): Plot-Specific Anchor. Logic or pre-aggregation shared by a Functional Group of plots (e.g., all Heatmaps using the same filtered subset).
     + Instruction: "To minimize recalculation, always suggest a wrangling sequence that prioritizes shared transformations as early as possible (Tier 1) based on the common data source ID/Path."

3. Persona Entry Protocol (Token & Logic Efficiency):
   + Update `dasharch.md`.
   + Command: "SESSION START: Your absolute first action is to read ./.agents/rules/workspace_standard.md. Based on the task at hand, selectively ingest only the relevant rules and workflows to conserve tokens and prevent knowledge drift. Do not scan the entire workspace by default."

4. Testing Hierarchy (Engines vs. Orchestrators):
   + Replace the 'Testing Protocols' section in `rules_verification_testing.md` with this logic:
     + Component Debuggers (The Engines): `libs/{lib}/tests/debug_{component}.py`. Specialized runners for isolated logic (e.g., `debug_wrangler.py` for Layer 1 decorators).
     + Global Library Wrapper (The Orchestrator): `libs/{lib}/tests/{lib}_integrity_suite.py`. A high-level runner that programmatically discovers actions and dispatches them to the appropriate 'Engine' for verification.
   + Command: "The Orchestrator MUST use the Engines to perform the actual execution; it does not contain the testing logic itself."

III. DOCUMENTATION & SITE SYNC

+ Update `docs/reference/testing.qmd` to reflect the 'Engines vs. Orchestrators' hierarchy exactly.
+ Update `docs/foundations/data_tiering_adr.qmd` with the new data-source-centric sharing rules.
+ Ensure all library READMEs point to the correct `{lib}_integrity_suite.py`.

IV. FINAL HALT

+ Provide a summary of updated files.
+ Provide a "One-line State of Truth" regarding the new boundary and data sharing rules.
+ Await @verify before updating .antigravity/tasks/tasks.md.

-----
Improvement / clarification - modulation

Hi, we need to have a control of some of the updates and agent behaviour that was made-

1. The agent does not respect the boundaries of AI ignore - and scans through the whole project, including directories that are not relevant to the task and that are defined, directories that are marked as to be ignored in the .aiignore file (it can however asks specific permission when relevant or when explicitly asked to do so in the rules files). This is not good from my token usage nor for privacy purposes, and it risks to confuse the agent as I keep archives in the EVE_WORK directory. We need to ensure respect of AI ignore boundaries.

2. We need to inspect if the changes that were made are correct and complete. I attached the new context and rules files (attached the new context files as a single concatenated file, I ommited the python scripts as they are not relevant for now). You need to review if the changes that have been implemented are correct and complete (when asked you can make a review prompt for antigravity so that the agent can implement the minor required updates). I ask you to focus even more thouroughly on those specific points:  

+ A) rules_data_engine.md : move from tier 2 to tier 1 : when its shared by more than 3 plots, maybe it needs to be when shared by all the plots depending on the data source  (need to ensure the data can be used by all branches otherwise the app will fail, but it could suggest eg a logic that allow to maximize sharing eg, steps order feks)
+ B) dasharch.md -> @dasharch must read the workspace_standard.md file entry rule and must be redirected to all other rules, workflow and knowlege file. Also I think the agent should be able to access and read relevant context depending on the task at hand, is this something we need to codify ?
+ C) please review that this paragraph in rules_verification_testing.md is correct and consistent with the testing_hiearchy_logic.md file.

```
- **Global Library Wrapper:** `libs/{lib}/tests/{lib}_integrity_suite.py`
  - *Purpose:* Programmatically query the registry, ingest all registered manifest-data combinations, execute them, and yield an automated `{lib}_integrity_report.txt`.
  - *Rule:* The global library wrapper script MUST be launched to ensure the entire system functions organically during broad refactorings.
- **Component Debuggers:** `libs/{lib}/tests/debug_{component_name}.py` 
  - *Purpose:* Isolated testing for individual features, decorators, or core modules during active development.
```

 I need to ensure that it is clear eg:  transformer library has 2 componets: the wrangler and the assembler, so we need 2 tests files BUT eg the wrangler need to be able to test all decorators, but one by one. While the  Global Library Wrapper is a wrapper that use the wrangler and assembler tester to test each decorator that is implemented on the whole library so I need to ensure that this logic is clear. Can you rewrite this paragraph instructions in a markdown text box so I can add it in the correct place in the documentation ?
 It seems that the reformating has been done according to what I want, but I am unsure if the instructions are clear enough (I might understadn those diferently than the AI)

 -D) Ebsyre that the documentation correctly reflect your paragraph on ### 🧪 Testing Hierarchy & Logic

## Stage 2

@Agent: Execute "Project Architecture & Rulebook Homogenization" (Refactor Phase 11).

I. OBJECTIVE
Restructure all project rules, workflows, and test naming conventions to align with the "3-Tier Tree Data Lifecycle" and "Homogeneous CLI Standards." You must eliminate architectural drift and redundancy.

II. MANDATORY READS (CURRENT STATE)

+ ./.agents/rules/ (all files)
+ ./.antigravity/knowledge/architecture_decisions.md
+ ./.antigravity/knowledge/project_conventions.md
+ ./libs/transformer/tests/
+ ./libs/viz_factory/tests/

III. TASK 1: THE 5-FILE RULEBOOK SPLIT
Delete all existing files in ./.agents/rules/ and replace them with these 5 authoritative files (Max 12k chars each):

1. rules_documentation_aesthetics.md:
   + Merge rules_aesthetic.md and rules_documentation_standards.md.
   + Enforce "Violet Law": ComponentName (file_name.py) is strictly for HUMAN-FACING .qmd and READMEs.
   + Prohibit Violet Law in functional code, logic, or docstrings.
   + Include Quarto/Mermaid zoomability and CSS theme standards.

2. rules_data_engine.md:
   + Merge rules_wrangling.md, rules_tiered_data.md, and ADR-024.
   + Implement the "3-Tier Tree Lifecycle":
     + Tier 1 (Trunk): Relational Anchor (All joins/heavy cleaning). Parquet on disk.
     + Tier 2 (Branch): Plot-Specific Anchor (Pre-aggregation/shrunk data for heavy plots). Parquet on disk.
     + Tier 3 (Leaf): Interactive UI View (Transient filters/LazyFrames). In-memory or tmp/.
   + Define "Bifurcation Point": Transformations shared by >3 plots move to Tier 1; plot-specific logic stays in Tier 2.

3. rules_verification_testing.md:
   + Standardize Naming:
     + Full Library: libs/{lib}/tests/{lib}_integrity_suite.py
     + Component Debuggers: libs/{lib}/tests/debug_{component_name}.py
   + CLI Mandate: Every Python script (libs and assets/scripts) MUST use argparse with a --help docstring. No hardcoded paths.
   + Enforce the @verify protocol (1:1:1 Evidence Loop).

4. rules_runtime_environment.md:
   + Enforce ADR-011 (Modular Monorepo) and ADR-016 (Editable Mode).
   + Strict VENV lock and DNF pinning for Antigravity v1.19.6 integrity.

5. rules_asset_scripts.md:
   + Governance for ./assets/scripts/.
   + Data Priority Hierarchy: 1. CLI Override (--data), 2. Manifest 'source' key, 3. Default Skeleton.
   + Differentiate "Suggestive Tools" (Synthetic data) from "Functional Assistants" (Manifest bootstrappers).

IV. TASK 2: WORKFLOW REFACTORING
Update ./.agents/workflows/ (implementation_workflow_transformer.md and visualisation_factory.md) to:

+ Use the 3-Tier Tree logic (Trunk -> Branch -> Leaf).
+ Reference the new standardized test naming (lib_integrity_suite.py).

V. TASK 3: CODEBASE & INDEX CLEANUP

+ Rename all existing integrity suites to follow the {lib}_integrity_suite.py pattern.
+ Update ./.agents/rules/workspace_standard.md (The Master Index) to point to the 5 new rulebooks.
+ Update ./.agents/rules/dasharch.md: Add "Integrity Guardian" instructions: check integrity_report.txt before writing code; enforce naming laws.

VI. FINAL HALT
Provide a summary of deleted/renamed files and a "One-line State of Truth." Await @verify before committing changes to .antigravity/tasks/tasks.md.

## Stage 1

+ [ ] Review all rules for AI context (first pass). In .agents/rules/
  + [x] rules_documentation_standards.md
  + [x] rules_aesthetic.md -
  + [x] rules_behavior.md
  + [x] rules_runtime.md
  + [x] rules_tiered_data.md
  + [x] rules_wrangling.md
  + [x] workspace_standard.md
+ [ ] in .agents/workflows/
  + [ ] implementation_workflow_transformer.md
  + [ ] verification_protocol.md
  + [ ] viz_factory_implementation.md
+ [ ] in .antigravity/knowledge/
  + [ ] architecture_decisions.md
  + [ ] blockers.md
  + [ ] milestones.md  
  + [ ] project_conventions.md
  + [ ] protocol_tiered_data.md
+ [ ] in .antigravity/plans/
  + [ ] implementation_plan_master.md
+ [ ] in .antigravity/tasks/
  + [ ] tasks.md

AI TO DO :
Hi, I attached your !sync file for the context (one large file that concatenates the main context and some other files we will need to review). Please read this context thoroughly.

We need to inspect the context and rules files and propose a new version of the rules files.

1 Do not remove rules unless agreed with me.
2 When we agree at the end of our conversation, and solely then, you will need to prepare a prompt for the antigravity integrated AI with the detail instructions so it can do the necessary changes we agreed upon, using the gemini 3 Flash model. This means you will need to detail all the steps and provide clear instruction of what needs to be changed. I will indicate that all has been reviewed and agreed via @generate_prompt.
3 **Important: All rules and workflow files are limited to 12,000 characters each, Therefore it is important to adopt a correct structure and split the files in logical parts**.

Here are some points I noted for review, but they are not exhaustive (so you will need to review all the and suggest better organization):

A. rules_aesthetic.md and rules_documentation_standards.md : redundancy shoult it be merged  in one single document ? Eventual inconsistencies must be found and resolved.
B. we need to ensure homogeneity in development rules : for the tests scripts eg. naming -> extract rule from the code structure (eg `tests/{lib}_integrity_suite.py`  might need to be renamed to current debug (see tree), we need also to ensure that it is writen in the rules that we an individual test script eg. per decorator / function and then a global wrapper to test the whole library (there are some parts already in the files). But we need to ensure consistency when continuing development.
C. It is important that a rule is given to ensure that all python scripts use argparse, because it needs to be possible for the user to use via command line. Wrappers scripts must adapt to this, running all individual tests via argparse.
D. rules_behavior.md : violet law ? shoult it only appear in the docs ? or should it refered to when necessary (avoid redundancy when not necessary)
E. tiered data protocol : note that a plot might reuse the same basic wrangling, so tier data might need to be stopped at a certain level, which will allow bifurcating the data transformation for different plots. We will need a solution after for update of the tier data2 from user (but need to be at a later stage)
F. should the rules_tiered_data.md merged or at least be mentionned in rules_wrangling.md ? should the context .antigravity/knowledge/protocol_tiered_data.md be mentionned or partially merged with rules_tiered_data.md ... and rules_wrangling.md ... ?
G. we need to create rules for the development of helper scripts for the user, in order consistency and their usage and purpose must also be documented. Scripts to assist uers are in .assets/scripts and I added those scripts to the context file.
H. At the end,  you will need to review the antigravity agent definition (.agents/rules/dasharch.md), and propose improvements of its definition so it can better assist the user in its tasks.
I. When this is settled , .agents/rules/workspace_standard.md will need to be updated, to ensure that the agent has to review the appropriate context files and rules ... as this is the main entry point for the agent (the file that explain what the agent must read and ingest before starting to work)
