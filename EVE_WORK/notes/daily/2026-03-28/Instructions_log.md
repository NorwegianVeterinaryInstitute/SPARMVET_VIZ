



I do not want to clean up other scripts in assets  - they are helpers, I will clean myself. Then 


## Improving helper scripts


@Agent: @dasharch - EMERGENCY PATH REPAIR & PATTERN CRYSTALLIZATION.

You have incorrectly genericized test paths. You must restore the 1:1:1 mapping between decorators, data, and manifests.

1. Path Restoration (Strict Mapping):
   - Iterate through all manifests in ./libs/transformer/tests/data/.
   - For each manifest '{{ACTION_NAME}}_manifest.yaml', ensure the 'source' path points EXACTLY to './libs/transformer/tests/data/{{ACTION_NAME}}_test.tsv'. 
   - Example: 'strip_whitespace_manifest.yaml' MUST point to 'strip_whitespace_test.tsv'.

2. Codify the Naming Law:
   - Update ./.agents/rules/workspace_standard.md (Section 8: Decorator Standards).
   - Add the following rule: 
     "Naming Convention for Atomic Testing: Every registered action MUST have a corresponding test pair using the exact action name:
      - Logic: @register_action('my_action')
      - Manifest: ./libs/transformer/tests/data/my_action_manifest.yaml
      - Data: ./libs/transformer/tests/data/my_action_test.tsv"

3. Automated Suite Alignment:
   - Ensure the 'test_decorator_suite.py' uses this naming convention to dynamically find and execute tests for all registered actions.

4. Documentation Update:
   - Reflect this strict naming convention in ./.antigravity/knowledge/project_conventions.md and the user docs.

5. HALT for @verify:
   - Print a table showing: [Action Name | Manifest Path | Data Path] for all currently implemented decorators to confirm the 1:1:1 mapping is restored.


   ----

- Need to create a wrapper script to automate decorator testing in ./libs/transformer/tests/ using the existing manifests and datasets that are in ./libs/transformer/data. Might need to adjust the manifests to the new standards (path of the data, input_fields and output_fields. Uncertain if the manifest follow the latest adopted standards. but this needs to be verified)

- Then it needs to document this addition (in the appropriate memory bank place and in docs for the user) and mark a rule that everytime a new decorator is added to the testing list of this it needs to be added to the test wrapper script for testing decorators.


@Agent: @dasharch - DECORATOR TEST AUTOMATION & STANDARDIZATION.

1. Manifest Audit (ADR-013/Section 12):
   - Review all YAML manifests in ./libs/transformer/tests/data/.
   - Update them to the mandatory 3-block structure: Header -> input_fields -> wrangling -> output_fields.
   - Ensure 'source' blocks use the correct relative paths for the test TSVs [ADR-015].
   - Verify that output_fields acts as a strict Polars .select() contract [Section 12].

2. Create 'test_decorator_suite.py':
   - Location: ./libs/transformer/tests/
   - Logic: A wrapper script that iterates through all implemented decorators in the registry.
   - Execution: It must call wrangler_debug.py for each decorator using its corresponding test manifest and dataset.
   - Validation: It must catch and report any decorator that fails to return a LazyFrame or violates the output contract.

3. Codify the "Testing Rule":
   - Update ./.agents/rules/workspace_standard.md (Section 8: Decorator Standards).
   - Add: "Mandatory Testing: Every new registered action MUST be added to the test_decorator_suite.py registry to ensure continuous integration of atomic logic."

4. Knowledge Mirroring:
   - Document the suite in ./.antigravity/knowledge/project_conventions.md.
   - Add a technical guide in ./docs/ describing how to add new decorators to the automated test loop.

5. HALT for @verify:
   - Run the suite and print the 'Pass/Fail' summary for all current decorators.

## Some cleaning

---
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