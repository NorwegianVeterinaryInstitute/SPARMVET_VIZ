
## Functionality and what is shown in the different elements 

- [ ] UI functionality and reactivity must be improved - (Showing data and plots)
	- [ ] Pre-calculation of Tier 1 and 2 data
	- [ ] ? png format for plots of Tier 1/2 as they are immutable ?
	- [ ] Association of this to the hash method to ensure that they are recalculated - redone when if manifest is changed / or if new data are treated ? 
	- [ ] Tier 3 -> copy of Tier 1 -> then can evolve (that this improve speed ?)

---- 
 - [ ] Gallery fix 
Developer persona : Do not pre-load any data/manifest. 
In the gallery : the Data, plot, manifest, and explanations. As defined by the local connector, those are to be found in Location 5: gallery (assets/gallery_data)

In the gallery, the user should by no means show other data/plot/manifests/metadata than defined at gallery path (Location 5, defined by the connector). The gallery is aimed to be a source of inspiration and copy-paste examples to help user develop their own manifests and graphs. Not a place of working with their own data/plots. 
In the Location 5. The plots are already in a .png format and can directly been inserted in the card, with their associated data, manifest (recipe_manifest.yaml) and recipe_metadata (for any other information that is shown on the right card). It is encouraged to optimize the reactivity of the gallery, to have very fast transition between scrolling/selecting the examples plots of the gallery. 

--- 


## Layout 

UI reactivity - Takes ages to draw (maybe we did not finish the manifest testing correctly)
- only try to display active 
- ? pre compuitations the plots elements so they can be uploaded rapidely (tier 1 and 2)  - I thought we were doing that

--- 



---
> Promps 


Hi, Here are the next changes. Please analyze the image and tell me what you understood before executing

Please document all the changes made to the UI , (rules, architecture decisions, implementation, design, artifacts, decision ... README, audit and user documentation. Everywhere where necessary)

Please prepare a short note about our current work for the next agent in the next session (batton pass)


---

Hub  should I think renamed to Home (but we can discuss)

- Review the attached image and make a list of tasks of requested changes (note some changes apply in all the views, while some are specific to individual views). You have found the perfect visual spacing it will be reused for many spacing.
- Fix : group headers and metrics boxes persisting in the card content area despite being removed from the dynamic_tabs logic.  (Fix ID collision or stale DOM state that requires a surgical **ID Sanitation** audit). 


---

Can we had hoover on mouse information about the functionalities in the project selection ? (Viz, ...)

Please remind me the functionalities and how each element is supposed to work. We were supposed to have a dev studio to help us create manifests  (wrangling and visualisations), that can be turned on off. We had also other parts that were toogle on/off depending on persona but I do not understand why we have so much detail here in the project selection. 

1. Hub 
2. Wrangle studio 
3. Viz
4. Dev Studio
5. Gallery 



---
Whaou, this is starting to look really good. Now we are going into details. 

in the code for the ui please: 

1. Left panel : rename "Agnostic Filters" to "Filters"  - Reduce the spacing between each "FILTER:<Field>" - by half.
2. The toogle side bar buttons are not very well placed for this narrow view. We need to find better solution for their placing. They overlapp sligthly with the text display and or other toogle bottons. Both on left and right side. 
3. We do not need to display "SPARMVET Analysis Theater" We can win some place with that. 
4. The column selector should be wider ( maybe starting on the right of the wide<-> long on/off button. )
5. The display of the columns should be left justified. Note we need to ensure that the primary key does not appear in the column selector "box".  It is important to ensure that the text of the column and the display in the grid are properly matched - it is a bit bad right now. 
6.  When we have a group tab 📊 Quality Control We do not need to show again the Text "eg. #### Group: Quality Control\n📊 Quality Control " This is redundant- We should remove this
7. I think the little grey box to display "number of plots and number of schemas" can be good in the developper persona but could be removed eg. for the some of the other persona. So this can be optional. It size should be reduced and adjusted with the "buttons box" above. When it is visible, it should show on the left of "the button box" with the graph, table and. .. other button view. When we hoover with the mouse on this latest box, we should have a little help showing that explain what each button does. 
8. The theater window should be able to use the whole size of the browser size on the screen (vertically down - if necessary - right now there is a large padding under). 
9. Because of adjusting of points 3,6 and 7 we should now have more place for the "sub-tabs" in each group so it is possible to display them in a larger portion of the analysis theater window. 
10. Add to tasks list : That we will need later to address the actually functionality (plots not showing - So we will have to retest manifest independently of ui first and plot production). For now we focus on adjusting the nice visual (so no fixing on the functionality)


---

ok, its better but we are not totally there yet. The Analysis theater touches the sidebar now. This is a bit too much. You said 4px gap - can we try increase to 8px or 10 px?
The left navigation panel looks too different to the right panel (The whole UI should be more symetrical) and not alligned in hight with the analysis theater and the right panel. 
The visuals were not adjusted on the left side of the theater.
Also I think we need to decrease the spacing between text and drops in each of the elements of the left navigation bar, trying to reduce the necessity for the user to scroll a long left side bar. We need to find the right balance between less spacing, policy size and scrolling necessity. Maybe also add the functionality 
of minimizing the project navigator and system tools ?


----

Ok, we need to reduce the spacing in the elements of the left side bar, (cut but at least half, )

--- 
Ok, The background color seems much better, it should be applied for all backgrounds. It seems there is a two another darker background around the analysis theater. It also seems to me that there are 2 margins layers. 

The position of the analysis theater, left side bar should be adjusted and aligned to the position of the right side bar, which I think is at the correct level on the web-browser. We can use that are reference. The margins between left side bar and analysis theater should be reduced. 



----

Ok, it looks much better already. Good work

- Can we make the grey background in the UI a bit darker grey (I think its too light). 
- Can we reduce the margins width between left side bar, Analysis Theater, and right side bar ? We can start by reducing the margins in half. 
- Can we reduce the margins on the top (all panels and analysis theater by at least half ? Not only the grey background margin, I believe its more the position of the whole UI that appears a bit too much down in the web-browser) Is it possible to fix ? 
- When we have agreed on suitable colour and margin size, we need to rectify the any document / artifact / instructions where previous requirements were specified or documented (eg, requirements, rules, workflows, implementation decisions/plan, UI css ...) 

For the functionality : I see also during the testing that in AMR and Virulence category that it attemps to show all Plots defined in this category on the same tab. We should only have one plot per tab. So we need a good solution for the category and plot.  If it is a complex refactor we could eventually fix that using eg. "AMR and virulence" category tab showing "amr_heatmap: AMR and virulence",
"virulence_bar:  AMR and virulence" - however I would have prefered to have sub-tabs in each category for each plot if possible. 
When we have decided of what is possible to do, then we will implement those changes in the UI definition and requirements - Before building those changes. Please advise. 


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
