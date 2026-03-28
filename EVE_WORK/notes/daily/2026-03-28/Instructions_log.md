



I do not want to clean up other scripts in assets  - they are helpers, I will clean myself. Then 


## Some cleaning


@Agent: @dasharch - GLOBAL PATH SYNCHRONIZATION.

Due to the consolidation of test runners, we have renamed and moved core debugging scripts. You must now synchronize all internal and external references.

1. Root Search (Excluding EVE_WORK/): 
   - Perform a recursive grep/search across the project root for the following strings:
     - "test_wrangler.py" (To be replaced by "wrangler_debug.py")
     - "assets/scripts/assembler_debug.py" (To be updated to "libs/transformer/tests/assembler_debug.py")
     - "assets/scripts/wrangle_debug.py" (To be updated to "libs/transformer/tests/wrangler_debug.py")

2. Update Targets (Absolute Source of Truth):
   - Mirror these changes in:
     - ./.agents/rules/workspace_standard.md
     - ./.antigravity/knowledge/project_conventions.md
     - ./.antigravity/tasks/tasks.md
     - All relevant files in ./docs/ (Maintaining Documentation Integrity [Section 7]).

3. Knowledge Update: 
   - Update your internal 'databank' and context to reflect that wrangler_debug.py is now the official 'Universal Wrangler Runner' [ADR 005].

4. HALT for @verify: 
   - Provide a list of all files modified and confirm that no legacy paths remain in the .antigravity/ hierarchy.
   
---

@Agent: @dasharch - FINAL TEST CONSOLIDATION (Layer 2).

1. Refactor assembler_debug.py (same logic than for wrangler_debug.py):
   - Implement argparse to support optional overrides for:
     --data (Path to input TSVs/Sources)
     --manifest (Path to the Assembly/Recipe YAML) (REQUIRED)
     --output (Path to the materialized result)
   - Ensure it defaults to the existing mock data if no arguments are provided.

2. Integration Check:
   - Confirm that this script utilizes the DataAssembler and the central registry [ADR 018].
   - Verify it follows the 'Evidence Generation' step of the Verification Protocol (materializing to tmp/ for manual @verify).

3. Logic Audit:
   - Final check: Ensure NO .collect() calls exist in the libs logic; keep them restricted to these test runners or the future data_executor.py.

4. HALT for @verify:
   - Provide the exact CLI command to run a test assembly with custom data.

---

@Agent: @dasharch - PRE-PLOT REFACTORING (Phase 3).

1. Functionality Audit & Comparison:
   - Compare .libs/transformer/tests/test_wrangler.py against .assets/scripts/wrangle_debug.py.
   - Determine if test_wrangler.py is deprecated or if wrangle_debug.py contains superior logic for Layer 1 terminal evaluation.
   - Ensure the survivor maintains the 'Universal Runner' standards (argparse, CLI-First) [ADR 005].

2. Migration & Consolidation:
   - Move .assets/scripts/assembler_debug.py to .libs/transformer/tests/.
   - Consolidate the superior Layer 1 test logic into .libs/transformer/tests/wrangler_debug.py.
   - Delete the redundant scripts from .assets/scripts/ once verified.

3. Lazy Audit:
   - Confirm all @register_action decorators return pl.LazyFrame and NO premature .collect() exists in the transformer core.

4. HALT for @verify:
   - Print the new directory structure of .libs/transformer/tests/ and confirm the CLI arguments for the consolidated twrangler_debug.py.