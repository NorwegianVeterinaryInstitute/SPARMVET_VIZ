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