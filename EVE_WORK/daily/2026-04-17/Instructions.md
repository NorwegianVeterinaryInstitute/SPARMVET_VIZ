HEADLESS-FIRST UI TESTING MANDATE:
UI testing is strictly gated. For every UI component task:

- Step 1: Create a sub-task in tasks.md for a Headless Unit Test.
- Step 2: Implement/Fix the component logic.
- Step 3: Execute a headless test using the relevant library debugger (e.g., debug_ingestor.py, debug_wrangler.py).
- Step 4: Materialize results to tmp/Manifest_test/ and output df.glimpse().
- Step 5: HALT for @verify. Only after sign-off may you proceed to the Visual/Reactive UI check.

Review tasks.md. and review verify state and progress of the tasks.
