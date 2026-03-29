
## Starting implementation 

> Implemented that as a workflow and now its almost automatic one by one, perfect ! 
#TODO:  REMEMBER THIS FOR FUTURE


@verify continue to follow ./agents/worfklows/viz_factory_implementation.md and implement next component




@Agent: @dasharch - DOCUMENT, MARK DONE, AND PROGRESS TO NEXT GEOM.

1. **Documentation (Artist Law / Violet Law)**:
   - Update './libs/viz_factory/README.md' and the specific documentation : ./.docs/workflows/visualisation_factory.qmd. 
   - Add 'geom_point' (src/geoms/core.py).
   - Include a 'Usage' example using the exact YAML structure from 'geom_point_test.yaml' (import the yaml file in the qmd file - rule: no code duplication).

2. **Task Management**:
   - Open './.antigravity/tasks/tasks.md'.
   - Mark '- [x] geom_point' as completed.
   - Identify the next incomplete Geom on the list (e.g., geom_line or geom_bar).

3. **Next Implementation (Evidence Loop)**:
   - Search './EVE_WORK/reference/plotnine_api_context.md' for the signature of the NEXT geom.
   - Implement/Register it in the appropriate 'src/geoms/' file.
   - Create the Test Triplet in './libs/viz_factory/tests/test_data/':
     1. '{next_geom}_test.tsv'
     2. '{next_geom}_test.yaml' (pointing to its .tsv)
     3. Run 'test_runner.py' to produce 'tmp/USER_debug_{next_geom}.png'.

HALT for @verify: Show the updated tasks.md and the new PNG artifact.

--- 

@Agent: @dasharch - DIRECTORY RECHECK, PURGE & VIZ FACTORY INITIALIZATION.

DIRECTORY RECHECK & SURGICAL CLEANUP
1. **Audit**: Scan './libs/viz_factory/tests/' and './libs/viz_factory/src/'.
2. **Keep**: Any existing directory structures that align with: geoms/, scales/, themes/, facets/, coords/, positions/, guides/.
3. **Purge**: Delete any files that do not fit the new 'Data-Manifest Coupling' standard (e.g., old standalone python test scripts like 'debug_viz.py' or 'test_plotnine.py' that aren't part of the new 'test_runner.py' logic).
4. **Result**: The 'tests/' folder should only contain 'test_data/' and the new 'test_runner.py' once completed. 



---


cd tmp/
../.venv/bin/python ../libs/viz_factory/tests/test_runner.py ../libs/viz_factory/tests/test_data/geom_point_test.yaml


@Agent: @dasharch - SYSTEM UPDATE & VIZ FACTORY ARCHITECTURE (Data-Manifest Coupling).

PART 1: SYSTEM UPDATE (Hard Requirement)
1. Open './.antigravity/docs/rules_behavior.md'.
2. Append the following 'Artist Law' section exactly:

### 📜 Artist Law: The Evidence-Driven Visual Contract
- **No Implementation without Evidence**: A component is not 'implemented' until it passes a standalone test.
- **Data-Manifest Coupling**: Every component test MUST consist of a triplet in './libs/viz_factory/tests/test_data/':
    1. `{component_name}_test.tsv`: The raw data (Tab-Separated).
    2. `{component_name}_test.yaml`: The manifest (must include a 'data_path' key pointing to its sibling .tsv).
    3. `USER_debug_{component_name}.png`: The resulting artifact in 'tmp/'.
- **Unified Test Runner**: Implementation must include a general test script in './libs/viz_factory/tests/test_runner.py' that can execute any component test by taking ONLY a manifest path as input. (Reference the Transformer library logic for file-based automation).
- **Component Reference**: Use 'Violet Law': 'ClassName (filename.py)' for all documentation.

3. Commit this change before proceeding.

PART2: Verify the implementation of geom_point and ensure the implementation logic and rules are followed

# Refining instructions 

Please improve this prompt so I we can start the implementation of the viz factory.

We will start to implement each geom one by one (follwoing the order in the 
./.antigravity/tasks/tasks.md file). 
Process : implementation 
Invidual tests for each geom (data, manifest everything must be created in the same go) must go in ./.libs/viz_factory/tests/test_data/

We follow the same logic as the transformer lib wrangler implementation. We allow recognizing the geom by {geom_name}_test.py and {geom_name}_test.yaml ... 

Expectations of results if possible. If require eg a minimum eg theme mapping osv for the geoms, it would be nice to be able to use the same for all the tests .

output should be verifyied byt the user -> tmp/user_debug_plot.png for example 

If there is need of debug, the documentation for all layers is in ./EVE_WORK/reference/plotnine_api_context.md 
which can be searched to find the code for the different layers components.



SPARMVET_VIZ Antigravity Specialist
Custom Gem
SPARMVET_VIZ Antigravity Specialist said
This strategy establishes the foundation for the Artist Pillar by aligning the Viz Factory (viz_factory.py) architecture with the complete "Grammar of Graphics" layers found in the Plotnine source code.


3. Implementation Protocol (The Prompting Loop)
For every geom in the list, I will generate a specialized prompt for @dasharch that follows this contract:

Contract: Define the mapping and params dictionary schema for the manifest.

Implementation: Register the component in libs/viz_factory/src/geoms/.

Validation Data: Generate a minimal synthetic Polars LazyFrame suited for that geom.

Verification: Materialize a plot to tmp/ for human review.


---

@Agent: @dasharch - SYSTEM UPDATE & VIZ FACTORY INITIALIZATION.

PART 1: SYSTEM UPDATE (Hard Requirement)
1. Open './.antigravity/docs/rules_behavior.md'.
2. Append the following section exactly:

### 📜 Artist Law: The Evidence-Driven Visual Contract
- **No Implementation without Evidence**: A component (geom, scale, theme, etc.) is not 'implemented' until it passes a standalone test using a local '.py' data generator and a '.yaml' manifest.
- **Verification Artifacts**: For the visualistation factory: Every test must output a high-resolution PNG to './tmp/' named 'USER_debug_{component_name}.png'.
- **Component Reference**: Documentation must strictly follow the 'Violet Law': 'ClassName (filename.py)' when describing layers.
- **Standardization**: All individual tests must use a shared 'test_base_theme.yaml' to ensure aesthetic consistency, allowing focus on functional logic.

3. Commit this change to the ruleset before proceeding.



--- 
@Agent: @dasharch - INITIALIZE VIZ FACTORY & IMPLEMENT FIRST GEOM (Following Artist Law).

**MANDATORY RULE (Artist Law)**: No component is complete without an Evidence Loop. Each implementation MUST include a test data script (.py), a test manifest (.yaml), and a materialized PNG in 'tmp/'.

1. **Verify Library Base Setup**:
   - Ensure './libs/viz_factory/src/' has subdirectories: geoms/, scales/, themes/, facets/, coords/, positions/, guides/.
   - Verify implementation of 'registry.py' with the '@register_plot_component' decorator.
   - Verify implementation of 'VizFactory (viz_factory.py)' core logic:
     * Accept (dataframe, manifest_dict, plot_id).
     * Materialize Polars LazyFrame to Pandas [ADR-010].
     * Initialize 'ggplot' with 'mapping' and pipe 'layers' from the registry.

2. **Standard Test Environment**:
   - Create './libs/viz_factory/tests/test_data/'.
   - Create a 'Standard Theme Mapping' (e.g., theme_minimal) to be reused across all geom tests to ensure consistency.

3. **Geom Implementation (Target: geom_point)**:
   - Search './EVE_WORK/reference/plotnine_api_context.md' for 'geom_point' signatures and parameters.
   - Implement and register 'geom_point' in './libs/viz_factory/src/geoms/core.py'.
   - Ensure naming is strictly functional (e.g., 'geom_point').

4. **The Evidence Loop (Validation)**:
   - Create './libs/viz_factory/tests/test_data/geom_point_test.py' (Polars generator).
   - Create './libs/viz_factory/tests/test_data/geom_point_test.yaml' (Manifest using geom_point + base_theme).
   - Generate the plot and save to 'tmp/USER_debug_geom_point.png'.

5. **Verification**:
   - Save the resulting plot to 'tmp/USER_{{geom_name}}_test_plot.png'.
   - LOG: Display the applied manifest and the successful registration of the component.

HALT for @verify: 
   - Show the 'tmp/USER_{{geom_name}}_test_plot.png' and wait for validation before proceeding to the next geom in tasks.md.


## Sanitize with factory, prepare implementation plan


@Agent: @dasharch - INITIALIZE VIZ FACTORY (Artist Pillar).

1. Library Setup:
   - Verify/Initialize ./libs/viz_factory/src/ and ./libs/viz_factory/tests/.
   - Ensure pyproject.toml exists and is installed in 'Editable Mode' (-e) [ADR-011].
   - verify existing files in the viz_factory directory and make sure they are aligned with the new modular rule files (and inspect their functions).

2. Core Implementation - VizFactory (viz_factory.py):
   - Implement the '@register_plot_component' decorator in 'registry.py'.
   - Logic: The factory MUST accept (dataframe, manifest_dict, plot_id).
   - Manifest Standard: Use 'Dictionary-for-Names' (plot_id) and 'List-for-Layers'.
   - Mapping: Implement the 'data-agnostic mapping' block (aes) as defined in the vision.

3. Module Organization (Subdirectories):
   - Create and initialize: ./geoms/, ./scales/, ./themes/, and ./facets/.
   - Violet Law: Ensure each directory has a __init__.py that auto-registers components.
   - Initial Components: Register 'geom_boxplot' (geoms/core.py) and 'theme_violet' (themes/violet.py).

4. Data Hand-off (ADR-010):
   - Ensure the factory performs the '.collect().to_pandas()' conversion ONLY at the final moment of Plotnine initialization [rules_runtime.md].

5. Verification Script - debug_viz.py:
   - Create './libs/viz_factory/tests/debug_viz.py' following the 'debug_' convention.
   - Evidence Loop: Materialize a test plot to 'tmp/USER_debug_plot.png' and HALT.

6. README & Standards:
   - Update './libs/viz_factory/README.md' using the 'Violet Component' standard.
   - Document the 'Filtered vs. Anchor' logic for state management.

HALT for @verify:
   - Provide the Inventory of registered plot components and the first materialized 'tmp/' plot.

## Workspace standard rules refactor 

so now we need it to make a pass at : 


./.antigravity/knowledge/architecture_decisions.md
./.antigravity/knowledge/project_conventions.md
./.agents/workflows/verification_protocol.md"
To ensure that they do not contain rules that should be integrated into the new modular rule files.

Moreover, the agent yesterday started to create new directories. I moved that into ./.antigravity/backups 
We need to make sure that the all information is either captured in the new modular rule files or in the corresponding files that the normal aligned agent should be using in the following directories: ./.antigravity/knowledge, ./.antigravity/plans and ./.antigravity/tasks 


@Agent: @dasharch - POST-REORGANIZATION AUDIT & CLEANUP.

The modular rule files are created, but we must now verify 'Logic Density' and remove redundancy.

1.  **Re-Check Modular Rules**: Compare 'rules_runtime.md', 'rules_wrangling.md', 'rules_behavior.md', and 'rules_aesthetic.md' against:
    - ./.antigravity/knowledge/architecture_decisions.md (Check ADR-013/014 integration)
    - ./.antigravity/knowledge/project_conventions.md (Check Type Selection Guide)
    - ./.agents/workflows/verification_protocol.md (Check @verify Evidence Loop)

2.  **Audit Backups**: Read everything in './.antigravity/backups'. 
    - Is there any logic or task state there NOT present in the active ./.antigravity/ or ./.agents/ directories? 
    - If YES: Move it to the correct authorized file now.
    - If NO: Prepare the directory for deletion.

3.  **Redundancy Purge**: Once logic is verified in the Rules, suggest which sections of the original Knowledge/Workflow files should be deleted or simplified to prevent 'Double-Rule Drift'.

4.  **Violet Law Enforcement**: Confirm all newly written rules use 'Component (filename.py)'.

HALT and provide a 'Gap Report'—list what was missing and where you moved it.

--- 

> the workspace standard is too large - so we need to refactor it to be more modular.

@Agent: @dasharch - PRE-MIGRATION INVENTORY - CONTEXT INJECTION & REFACTOR.


1. Read the user backup of the latest workspace_standard in './EVE_WORK/daily/2026-03-28/workspace_standard_backup.md'. 
We need to refactor the workspace rules and standards to be more modular.

2. To prevent architectural drift during the modularization of our rules, you must create a temporary file: './.agents/rules/migration_inventory.md'.

3. **Map Every Component**: Document the transition of Sections 1-17 of 'workspace_standard.md' and the 'ANTIGRAVITY_GEM_context.md' system state into the following 4 sub-files in the .agents/rules/ directory:
    - rules_runtime.md
    - rules_wrangling.md
    - rules_behavior.md
    - rules_aesthetic.md

2.  **Incorporate External Context**: Ensure the 'Data Type Selection Guide' (from project_conventions.md) and the 'Evidence Loop' (from verification_protocol.md) are mapped as mandatory inclusions.

3.  **Halt for Approval**: Once this file is written, present it as a table and HALT. Do not begin the actual refactoring or file creation until I provide the @verify command.

4.  **Violet Standard**: All file/class references in the inventory MUST follow 'ClassName (filename.py)'.

















---- 

2. Create './.agents/rules/rules_runtime.md' and include these SYSTEM TRUTHS:
   - IDE Version: Antigravity v1.19.6 (STABLE/PINNED).
   - OS: Fedora 43 KDE (Velocifero Compute).
   - Update Policy: 'update.mode: none' (DNF pinned).
   - VENV: All execution MUST use './.venv/bin/python'. No path hacking (sys.path).

3. Create './.agents/rules/rules_wrangling.md':
   - Include Section 8 (Decorators), Section 9 (Transformation), and Section 12 (ADR-013 Manifest Contract).
   - Pull the 'Data Type Selection' and '1:1:1 Naming Law' from `./.antigravity/knowledge/project_conventions.md` into `rules_wrangling.md`.

4. Create './.agents/rules/rules_behavior.md':
   - Include the @verify Protocol: Generate Test Data/Manifest -> Execute CLI -> Materialize to tmp/ -> df.glimpse() -> HALT.
   - Include the 'Halt & Verify' Protocol for rule changes.
   - Pull the 'Evidence Loop' from `./.agents/workflows/verification_protocol.md` into `rules_behavior.md`.


5. Create './.agents/rules/rules_aesthetic.md` (Violet Law, Documentation, Quarto/Mermaid). 



6. **Clean Up**: 
    - Once the new ./.agents/rules/ directory is verified, update the main workspace_standard.md to be a 'Master Index' that mandates reading these sub-files.
    - Reference all components using the Violet Law: ComponentName (file_name.py).
    - Strip the old monolithic sections.
    - Ensure no component are missing - only reorganized.
    - Transform it into a 'Master Authority Index' that explicitly points to these sub-rulebooks.
    - Apply the Violet Law: ClassName (filename.py) to all descriptions.

HALT and confirm when the local rule directory is the new 'Source of Truth'.






