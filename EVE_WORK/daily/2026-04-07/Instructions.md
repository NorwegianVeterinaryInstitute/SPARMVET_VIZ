# Instructions and work log

date:: 2026-04-07

## Stage 3

Improvement / clarification

---

- [ ] update the script to provide context for the chat agent.

---

- [ ] viz_factory_implementation : some weird changes were made here, please review the initial state and correct those eg. there is a reference to :
- **Source Material**: Search `EVE_WORK/reference/plotnine_api_context.md` for the component signature and available parameters.

- EVE_WORK is my notes, and this should not be used by the agent unless explicitly asked to do so.

---

- [ ] rules_data_engine.md

- shared by all the plots depending on the data source  (need to ensure the engine is generic enough to be used by all plots)

---

- [ ] dasharch.md
- must read the workspace_standard.md file entry rule and must be redirected to all other rules, workflow and knowlege file .

----

- [ ] please review that this paragraph in rules_verification_testing.md is correct and consistent with the testing_hiearchy_logic.md file.

```
- **Global Library Wrapper:** `libs/{lib}/tests/{lib}_integrity_suite.py`
  - *Purpose:* Programmatically query the registry, ingest all registered manifest-data combinations, execute them, and yield an automated `{lib}_integrity_report.txt`.
  - *Rule:* The global library wrapper script MUST be launched to ensure the entire system functions organically during broad refactorings.
- **Component Debuggers:** `libs/{lib}/tests/debug_{component_name}.py` 
  - *Purpose:* Isolated testing for individual features, decorators, or core modules during active development.
```

 I need to ensure that it is clear eg:  transformer library has 2 componets: the wrangler and the assembler, so we need 2 tests files BUT eg the wrangler need to be able to test all decorators, but one by one. While the  Global Library Wrapper is a wrapper that use the wrangler and assembler tester to test each decorator that is implemented on the whole library so I need to ensure that this logic is clear. Can you rewrite this paragraph instructions in a markdown text box so I can add it in the correct place in the documentation ? p

### 🧪 Testing Hierarchy & Logic

To maintain architectural integrity, the project follows a three-tier testing strategy. Every library MUST implement the following structure to ensure both isolated logic and organic system functionality.

#### 1. Component Debuggers (The Execution Engines)

`libs/{lib}/tests/debug_{component_name}.py`

- **Purpose:** These are the functional "runners" that know how to process a specific logic layer.
- **Transformer Example:** * `debug_wrangler.py`: Executes Layer 1 (Atomic) transformations.
  - `debug_assembler.py`: Executes Layer 2 (Relational) joins and assembly.
- **Rule:** These scripts MUST use `argparse` to accept a `--manifest` and `--data` path, allowing for manual, isolated debugging of any single feature or pipeline.

#### 2. Atomic Test Triplets (The Feature Units)

`libs/{lib}/tests/data/{feature_name}_{triplet_part}`

- **Purpose:** Every registered decorator or action MUST have a 1:1:1 test triplet:
    1. **Data:** `{feature}_test.tsv`
    2. **Manifest:** `{feature}_test.yaml`
    3. **Evidence:** `tmp/{feature}_debug_view.tsv` (or `.png`)
- **Logic:** These provide the "fuel" for the Component Debuggers. To test a single decorator (e.g., `strip_whitespace`), the `debug_wrangler.py` is called using the `strip_whitespace_test.yaml` manifest.

#### 3. Global Library Wrapper (The Integrity Orchestrator)

`libs/{lib}/tests/{lib}_integrity_suite.py`

- **Purpose:** An automated "Full-Scan" runner that ensures the entire library functions organically.
- **Logic Flow:**
    1. **Discovery:** Programmatically queries the library's Registry (e.g., `AVAILABLE_WRANGLING_ACTIONS`) to find all implemented decorators.
    2. **Iteration:** For each action found, it locates the corresponding Test Triplet.
    3. **Execution:** It dispatches the appropriate **Component Debugger** (Wrangler or Assembler) to process that specific test.
    4. **Reporting:** Yields a comprehensive `{lib}_integrity_report.txt` in `tmp/` detailing [PASSED] vs [FAILED] status for every component.
- **Rule:** This suite MUST be executed after any broad refactoring to detect regression errors across the entire library.

## Stage 2

@Agent: Execute "Project Architecture & Rulebook Homogenization" (Refactor Phase 11).

I. OBJECTIVE
Restructure all project rules, workflows, and test naming conventions to align with the "3-Tier Tree Data Lifecycle" and "Homogeneous CLI Standards." You must eliminate architectural drift and redundancy.

II. MANDATORY READS (CURRENT STATE)

- ./.agents/rules/ (all files)
- ./.antigravity/knowledge/architecture_decisions.md
- ./.antigravity/knowledge/project_conventions.md
- ./libs/transformer/tests/
- ./libs/viz_factory/tests/

III. TASK 1: THE 5-FILE RULEBOOK SPLIT
Delete all existing files in ./.agents/rules/ and replace them with these 5 authoritative files (Max 12k chars each):

1. rules_documentation_aesthetics.md:
   - Merge rules_aesthetic.md and rules_documentation_standards.md.
   - Enforce "Violet Law": ComponentName (file_name.py) is strictly for HUMAN-FACING .qmd and READMEs.
   - Prohibit Violet Law in functional code, logic, or docstrings.
   - Include Quarto/Mermaid zoomability and CSS theme standards.

2. rules_data_engine.md:
   - Merge rules_wrangling.md, rules_tiered_data.md, and ADR-024.
   - Implement the "3-Tier Tree Lifecycle":
     - Tier 1 (Trunk): Relational Anchor (All joins/heavy cleaning). Parquet on disk.
     - Tier 2 (Branch): Plot-Specific Anchor (Pre-aggregation/shrunk data for heavy plots). Parquet on disk.
     - Tier 3 (Leaf): Interactive UI View (Transient filters/LazyFrames). In-memory or tmp/.
   - Define "Bifurcation Point": Transformations shared by >3 plots move to Tier 1; plot-specific logic stays in Tier 2.

3. rules_verification_testing.md:
   - Standardize Naming:
     - Full Library: libs/{lib}/tests/{lib}_integrity_suite.py
     - Component Debuggers: libs/{lib}/tests/debug_{component_name}.py
   - CLI Mandate: Every Python script (libs and assets/scripts) MUST use argparse with a --help docstring. No hardcoded paths.
   - Enforce the @verify protocol (1:1:1 Evidence Loop).

4. rules_runtime_environment.md:
   - Enforce ADR-011 (Modular Monorepo) and ADR-016 (Editable Mode).
   - Strict VENV lock and DNF pinning for Antigravity v1.19.6 integrity.

5. rules_asset_scripts.md:
   - Governance for ./assets/scripts/.
   - Data Priority Hierarchy: 1. CLI Override (--data), 2. Manifest 'source' key, 3. Default Skeleton.
   - Differentiate "Suggestive Tools" (Synthetic data) from "Functional Assistants" (Manifest bootstrappers).

IV. TASK 2: WORKFLOW REFACTORING
Update ./.agents/workflows/ (implementation_workflow_transformer.md and visualisation_factory.md) to:

- Use the 3-Tier Tree logic (Trunk -> Branch -> Leaf).
- Reference the new standardized test naming (lib_integrity_suite.py).

V. TASK 3: CODEBASE & INDEX CLEANUP

- Rename all existing integrity suites to follow the {lib}_integrity_suite.py pattern.
- Update ./.agents/rules/workspace_standard.md (The Master Index) to point to the 5 new rulebooks.
- Update ./.agents/rules/dasharch.md: Add "Integrity Guardian" instructions: check integrity_report.txt before writing code; enforce naming laws.

VI. FINAL HALT
Provide a summary of deleted/renamed files and a "One-line State of Truth." Await @verify before committing changes to .antigravity/tasks/tasks.md.

## Stage 1

- [ ] Review all rules for AI context (first pass). In .agents/rules/
  - [x] rules_documentation_standards.md
  - [x] rules_aesthetic.md -
  - [x] rules_behavior.md
  - [x] rules_runtime.md
  - [x] rules_tiered_data.md
  - [x] rules_wrangling.md
  - [x] workspace_standard.md
- [ ] in .agents/workflows/
  - [ ] implementation_workflow_transformer.md
  - [ ] verification_protocol.md
  - [ ] viz_factory_implementation.md
- [ ] in .antigravity/knowledge/
  - [ ] architecture_decisions.md
  - [ ] blockers.md
  - [ ] milestones.md  
  - [ ] project_conventions.md
  - [ ] protocol_tiered_data.md
- [ ] in .antigravity/plans/
  - [ ] implementation_plan_master.md
- [ ] in .antigravity/tasks/
  - [ ] tasks.md

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
