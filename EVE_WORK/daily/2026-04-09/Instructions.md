# Instructions 2026-04-09

## Fixing context script

then adding to doc.

---
@dasharch - LOGIC PROMOTION & HYGIENE (ADR-011 / ADR-032).

1. AUDIT TMP/:
Scan all .py scripts currently in tmp/. Identify logic that is NOT redundant and fits into our core libraries:

- Relational/Joining logic -> libs/transformer/
- Ingestion/Path resolution -> libs/ingestion/
- Plotting/Factory components -> libs/viz_factory/
- Manifest/Synthetic utilities -> libs/generator_utils/

1. PROMOTION RULE (ADR-032):
For each identified script:

- MOVE the functional logic to the appropriate library src/ directory.
- CONVERT the script into a Standardized Test Debugger: libs/{lib}/tests/debug_{name}.py.
- ENFORCE CLI MANDATE: Implement argparse and a comprehensive --help docstring (Rule 2, rules_verification_testing.md).

1. VIOLET LAW COMPLIANCE:
Update the Key Components list in the respective libs/{lib}/README.md using the ComponentName (file_name.py) standard.

2. CLEANUP:
Once the logic is promoted and verified via a quick --help execution, you are authorized to delete the original script from tmp/.

FOLLOW VERIFICATION PROTOCOL: Provide a mapping of Moved Logic (Old Path -> New Path) -> HALT for @verify before deletion."

---

@dasharch - ARCHITECTURAL CORRECTION (ADR-003 / ADR-031).

1. REMOVE MOCK DATA:
Strip all hardcoded dataframes or mock dictionaries from app/src/server.py. Logic must be "Thin" (ADR-003).

2. ESTABLISH PATH AUTHORITY:
Read config/connectors/local/local_connector.yaml.

- Set Location 1 (Raw) to assets/test_data.
- Set Location 2 (Manifests) to config/manifests/pipelines/.
- Set Location (3) for user and testing to tmp/UI_TEST - create appropriate subdirectories.

1. DATA INGESTION TASK:
Initialize the DataAssembler (libs/transformer/src/data_assembler.py) using:

- Master Manifest: config/manifests/pipelines/1_Abromics_general_pipeline.yaml.
- Source Data: assets/test_data/1_test_data_ST22_dummy/ and assets/2_VIGAS-P_ST22_dummy (note that data sources are defined in the mainfest config/manifests/pipelines/1_Abromics_general_pipeline.yaml)

1. COMPONENT AUDIT:
Analyze the !included files in the Abromics pipeline directory.
The manifest has currently only one or two active datasets and metadata, but the tier 2 and plot might not be defined yet. This will need to be implemented.

2. EXECUTION:
If manifests are valid, execute Tier 1 materialization:

- Call assembler.assemble() -> sink_parquet("{path_location_3}/session_anchor.parquet").
- The UI must then scan_parquet from this anchor.

FOLLOW VERIFICATION PROTOCOL: List detected data files and manifest status -> HALT for @verify."

---

@dasharch - SYSTEM RESET & INITIALIZATION.

1. READ AUTHORITY FILES:

- ./.agents/rules/workspace_standard.md (Master Index)
- ./.antigravity/knowledge/architecture_decisions.md (ADRs 027-031)
- ./.antigravity/plans/implementation_plan_master.md (Phase 11-C Focus)

1. CONTEXT:
We are entering Phase 11-C: UI Shell & Module Orchestration. The goal is to build the "Thin Shiny Frontend" (ADR-003) using a modular approach.

2. MANDATORY CONSTRAINTS:

- Library Sovereignty: UI must NOT implement wrangling or plotting. Call ./libs/ exclusively.
- Path Authority: System paths MUST be read from config/connectors/local/local_connector.yaml.
- Aesthetic Lock: Sidebars use #f8f9fa. Central Theater is white. No "Deep Violet" in UI.
- Violet Law: Documentation updates must use "ComponentName (file_name.py)".

1. TASK: INITIALIZE BOOTLOADER & SHELL

- Create app/src/bootloader.py: Implement logic to read config/ui/templates/ui_persona_template.yaml to toggle features.
- Update app/src/ui.py: Implement the 3-Zone Shell:
  - Left: Navigation (Sidebar)
  - Center: Central Theater (Main)
  - Right: Audit Stack (Sidebar)
- Update app/src/server.py: Basic imports of libs/transformer and libs/viz_factory.

1. LOGGING:

- Append session audit to ./.antigravity/logs/audit_2026-04-09.md.
- Update docs/workflows/dashboard_app.qmd with the new shell architecture.

FOLLOW VERIFICATION PROTOCOL: MATERIALIZE UI SKELETON -> HALT FOR @verify.

## Consistency and integration manual changes

@Agent: @dasharch - CRITICAL ALIGNMENT & SYSTEM RECONCILIATION

**Phase 1: Deep Scan & Inconsistency Audit**
Perform a comprehensive read of the files in the following directories to synchronize your internal state with my recent manual changes:

- `./.agents/rules
- `./.agents/workflows
- `./.antigravity/knowledge
- `./.antigravity/plans
- `./.antigravity/tasks

**Phase 2: Logic Verification & Strategic Advice**
Analyze the current codebase and provide a report on the following pillars:

1. **Data Tier Implementation:**
2. **Filtering Process:**
3. **Path Authority (System Connectors):** Advise on the optimal location for system-level connection paths (e.g., IRIDA, Galaxy, Local PC).
   - **Constraint:** These MUST be decoupled from UI Persona templates (The current instructions are in the persona templates and should be adjusted).
   - **Guidance:** `config/connectors/` . A template can be implemented in the `config/connectors/templates/` and must be implemented in `config/connectors/local/local_connector.yaml` for current testing.

**Phase 3: Task List Consolidation**
Once I approve your audit report, and that you have implemented the changes from Phase 2:

1. **Discovery:** Scan all current task files, the master roadmap and implementation decisions.
2. **Merge & Rewrite:** Consolidate, de-duplicate, and rewrite the `tasks.md` to reflect the refined logic from Phases 1 and 2.

**MANDATORY HALT:** Provide the "Inconsistency Report" and "Path Implementation Advice" in the terminal for my review before modifying any existing files.
