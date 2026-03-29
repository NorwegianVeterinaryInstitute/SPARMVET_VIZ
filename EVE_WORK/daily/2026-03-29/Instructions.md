

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






