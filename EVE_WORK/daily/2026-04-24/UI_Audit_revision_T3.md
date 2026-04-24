# Functioning of the UIO audit
Please review The attached document. (2026-07-07/Viz_work/Gemini-Agent_Viz_prep.md) It is an earlier vision of the dashboard, before starting implementation. Much of it is to be considered as legacy, but some elements might be worth to pick up and discuss to improve the current UI. 

So please review, and check what is legacy (new decisions) and not officially decided or could be used. 

Also I would like to be able to define how the data audit trace (For Tier 3) will work, as it is related also to which data will be exported. 

Here are the current thoughts.  For Tier 3, it is used when a user want to adjust plot / data. Used case eg. Fitlering out outliers, filtering out some categories (eg to few samples to be analyzed correctly)
- Dependent on Persona
- Aimed for small adjustments (data / plot layout)

- Need full transparency : what has been changed. And the reason for the change HAS to be added in the audit. Eg this point is error because was problem x in the lab and instrument X failed ..., or detected misslabelling of sample in LAB id is incorrect 

- Need to be able to save new manifest / session when auditing, incl. ghost 
- Export recipie in gallery should allow to export steps to the Tier 3 recipe. Note that in this case we need also to ensure that when changing of the "module" view in the UI between (HOME, Gallery) that it recall the last state of the module, allowing transfer of informaiton between modules. 


