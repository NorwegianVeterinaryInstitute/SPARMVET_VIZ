@Agent: @dasharch - SYSTEM INITIALIZATION & TASK DECOMPOSITION.

1. PERMANENT CONTEXT (Read immediately):

- ./.agents/rules/workspace_standard.md (Authority map & VENV enforcement)
- ./.antigravity/tasks/tasks.md (Current execution status)
- ./.antigravity/knowledge/project_conventions.md (Path registry & terminology)

1. MANDATORY SEARCH & RETRIEVAL PROTOCOL:
You are equipped with a modular rule system. Do not guess logic. You MUST identify and read the relevant files from the following directories BEFORE executing a task. Attached file describes this logic. (see PATH_INITIATION.md attached)

Halt and wait for other instructions.

"@Agent: @dasharch - SYSTEM ALIGNMENT & ARCHITECTURAL RECONCILIATION.

The session cache is clean. You must rebuild your project 'brain' from the source of truth.

1. MANDATORY DISPATCH (Read Order):
   - Read ./.agents/rules/workspace_standard.md to map governing authority.
   - Read ./.antigravity/knowledge/project_conventions.md to identify the 'Who/Where/How'.
   - Read ./.antigravity/plans/implementation_plan_master.md to identify the current Phase.

2. MANDATORY SEARCH & RETRIEVAL PROTOCOL:
You are equipped with a modular rule system. Do not guess logic. You MUST identify and read the relevant files from the following directories BEFORE executing a task. Attached file describes this logic. (see PATH_INITIATION.md attached)

3. SEARCH & RETRIEVAL (No-Discovery Rule):
   - Use tree.txt and PATH_INITIATION.md to locate all active library and app files.
   - Do not perform exploratory reads. If a file is missing, HALT and report.

4. COMPREHENSIVE AUDIT CATEGORIES and FOUNDATIONAL CHECK:
   - Verify that all core libraries (libs/transformer, libs/viz_factory, etc.) are in 'Editable Mode' (-e) [ADR-011].
   - Confirm that sys.path.append is NOT used, and package-first authority is maintained [ADR-016].
   - FUNCTIONALITY: Identify implemented vs. planned features for Phase 11/12. Specifically check app/src/ui.py and server.py for ADR-029a (Theater Layout) and ADR-036 (ID Sanitation).
   - CONSISTENCY: Compare the 't3_recipe' logic in WrangleStudio against the Tiered Data Lifecycle [ADR-024]. Ensure Tier 1/2 are immutable and Tier 3 is transient.
   - Verify implementation of hash to avoid recalculations of data
   - DISCREPANCIES: Identify 'Ghost Logic' (code without an ADR or Task) and 'Ghost Plans' (Tasks marked [x] but not physically present).
   - DOCUMENTATION INTEGRITY:
      - Check all ./libs/ READMEs for sync with current src/ logic.
      - Verify 'Violet Law' compliance in ./docs/ (.qmd files).
      - Ensure 'Split-Documentation Strategy' (Foundations vs Appendix) is maintained.
   - The UI was quite slow: ADVISE on improvements that could make the UI snappier.

5. A part of your plan should  present a Table with:
   - Component | Status (Implemented/Partial/Planned) | Logic Discrepancy | Doc Sync Status.
   - List of identified Technical Debt items.
   - Confirmation of ./.venv/bin/python interpreter lock.

HALT: Only provide the audit report. Do not modify files. Waiting for @verify to align foundations."
