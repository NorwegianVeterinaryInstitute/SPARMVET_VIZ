# Instructions 2026-04-09

## Consistency and integration manual changes

@Agent: @dasharch - CRITICAL ALIGNMENT & SYSTEM RECONCILIATION

**Phase 1: Deep Scan & Inconsistency Audit**
Perform a comprehensive read of the files in the following directories to synchronize your internal state with my recent manual changes:

* `./.agents/rules
* `./.agents/workflows
* `./.antigravity/knowledge
* `./.antigravity/plans
* `./.antigravity/tasks

**Phase 2: Logic Verification & Strategic Advice**
Analyze the current codebase and provide a report on the following pillars:

1. **Data Tier Implementation:**
2. **Filtering Process:**
3. **Path Authority (System Connectors):** Advise on the optimal location for system-level connection paths (e.g., IRIDA, Galaxy, Local PC).
   * **Constraint:** These MUST be decoupled from UI Persona templates (The current instructions are in the persona templates and should be adjusted).
   * **Guidance:** `config/connectors/` . A template can be implemented in the `config/connectors/templates/` and must be implemented in `config/connectors/local/local_connector.yaml` for current testing.

**Phase 3: Task List Consolidation**
Once I approve your audit report, and that you have implemented the changes from Phase 2:

1. **Discovery:** Scan all current task files, the master roadmap and implementation decisions.
2. **Merge & Rewrite:** Consolidate, de-duplicate, and rewrite the `tasks.md` to reflect the refined logic from Phases 1 and 2.

**MANDATORY HALT:** Provide the "Inconsistency Report" and "Path Implementation Advice" in the terminal for my review before modifying any existing files.
