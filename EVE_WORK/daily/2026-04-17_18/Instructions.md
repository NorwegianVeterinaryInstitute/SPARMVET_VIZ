Ok, it looks much better already. Good work

Hover we still need to do some adjustments so the UI  visuals get better.
Here is a new rough drawing of how it looks and how it should look 
On the left side is what it looks like and on the right it is how it should look like.

One problem is that the selector in the analysis theater does not adjust well with the width of the theater (which is problematic depending on the width of the browser window). I have a wide screen so its ok if I put the browser viewed on the wide screen, but it will likely overlap the right side bar on a more normal screen size. Also I suggest to anchor the start of the selector position in the theater on the left side, just after the "Analysis Theater text".  


- Can we make the grey background in the UI a bit darker grey (I think its too light). 
- Can we reduce the margins width between left side bar, Analysis Theater, and right side bar ? We can start by reducing the margins in half. 
- Can we reduce the margins on the top (all panels and analysis theater by at least half ? Not only the grey background margin, I believe its more the position of the whole UI that appears a bit too much down in the web-browser) Is it possible to fix ? 
- When we have agreed on suitable colour and margin size, we need to rectify the any document / artifact / instructions where previous requirements were specified or documented (eg, requirements, rules, workflows, implementation decisions/plan, UI css ...) 

For the functionality : I see also during the testing that in AMR and Virulence category that it attemps to show all Plots defined in this category on the same tab. We should only have one plot per tab. So we need a good solution for the category and plot.  If it is a complex refactor we could eventually fix that using eg. "AMR and virulence" category tab showing "amr_heatmap: AMR and virulence",
"virulence_bar:  AMR and virulence" - however I would have prefered to have sub-tabs in each category for each plot if possible. 
When we have decided of what is possible to do, then we will implement those changes in the UI definition and requirements - Before building those changes. 


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
