
---
UI visual layout is not correct. I can upload a drawing I made to explain. Which image format do you prefer ? 


--- 
Here is the drawing of the layout. One the left, it is the current layout that appear in the web browser, on the right it is the desired layout. 

Also in the Analysis theater, I did not see any tabs nor categories materialize - so I am unsure how it will look like. 
We can use config/manifests/pipelines/1_test_data_ST22_dummy.yaml to test the complete layout with tabs to see how it will look like with a complex pipeline setup. 




---

HEADLESS-FIRST UI TESTING MANDATE:
UI testing is strictly gated. For every UI component task:

- Step 1: Create a sub-task in tasks.md for a Headless Unit Test.
- Step 2: Implement/Fix the component logic.
- Step 3: Execute a headless test using the relevant library debugger (e.g., debug_ingestor.py, debug_wrangler.py).
- Step 4: Materialize results to tmp/Manifest_test/ and output df.glimpse().
- Step 5: HALT for @verify. Only after sign-off may you proceed to the Visual/Reactive UI check.

Review tasks.md. and review verify state and progress of the tasks.
