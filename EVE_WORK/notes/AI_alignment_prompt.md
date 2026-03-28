
@Agent: @dasharch - CRITICAL RULE RE-SYNC.

1. **Reload Context:** Immediately re-read ./agents/rules/workspace_standard.md and ./.antigravity/knowledge/architecture_decisions.md, and ./.antigravity/knowledge/project_conventions.md.
2. **State Sync:** Update your internal logic to match the latest versions of these files.
3. **Validation:** If my current request contradicts these updated rules, invoke the Logic Conflict Guardrail and ask for clarification before proceeding.



----

@Agent: @dasharch - SYSTEM RESET: Standards & Architecture Alignment.

1. **Rule of Precedence (The Guardrail):**
   - Read 'workspace_standard.md' and all ADRs in '.antigravity/knowledge/'.
   - **CRITICAL:** If any subsequent prompt contradicts these rules (e.g., asking for CSV, non-CLI scripts, or hardcoded logic), you MUST HALT and ask for clarification.

2. **Technical Standards (ADR Lock):**
   - **Data:** Default to TSV (sep="\t") for all bioinformatics metadata.
   - **Execution:** All testing MUST use the Universal Runner 'libs/transformer/tests/test_wrangler.py'. No one-off terminal scripts.
   - **CLI:** All Python tools must use 'argparse' for --data and --manifest.
   - **Vectorization:** All decorators must support 'columns: [list]' for batch processing.

3. **Workflow Sync (v1.6 Protocol):**
   - **Step A:** Generate TSV/YAML Contract -> HALT for @verify.
   - **Step B:** Run Universal Test -> Materialize to tmp/USER_debug_view.csv -> HALT for @verify.

4. **Task Audit:**
   - Review '.antigravity/tasks/tasks.md'.
   - Identify the next [TODO] decorator/action.
   - **STOP:** Confirm you have internalized these rules and state which decorator is next.