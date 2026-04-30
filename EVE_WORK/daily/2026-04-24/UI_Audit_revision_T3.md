
# Revision of T3 audit trace 2
**Adding a new transformation node (non-filter):** This is a real open question — how does the user enter a new wrangling node? Options:

A) Action picker UI** —> would that not be a lot of different actions ? wrangling and plotting ?  including a lot of parameters options ? 
Should we maybe then let the transformation actions be simple (eg. eg put whole data exported so user could eventually add more complex transformation in T3 via the blueprint ? but then that would require to give access to the developper tool ?) Maybe we should keep to simple select columns and filters for T3. And then just maybe the gallery nodes --- still I am ambiguous for adjusting parameters. Or maybe then we should also keep the gallery as source of inspiration and let developper to be requested to implement in pipeline. I am afraid it will be too complex for most users otherwise 

Export trigger pdf/docx separate button
- The "Methods" section of the report renders each Yellow node as plain English (template-based: e.g., "Samples matching `sample_id = S_LAB_042` were excluded. Reason: instrument failure.") - yes, that would be good - and maybe good here because then would work better for simple filter and select

Cant answer the rest before I am sure here what is best

# Revision of T3 audit trace 1

T3 audit : important - all the modifications done in T3 must be traceable, including select and filters. So filter row added must be recorded with justification, block apply untily filled. 

- ordered list yellow nodes - heu, user mind probably needs the recipie from top to bottum but practicallity would be to have most recent at top. We can try that, how difficult would it be to change ? 

- Ghose save yes of the T3 session (I think must be distinct from the ghost save of the T1/T2 - which are only computed once - or when new data or change in manifest -> NB: must verify that his is actually functioning correctly)

- I think the Filters and select Need to be appended to the T3 recipe (most likely will have only those operations anyway - otherwise would use the Blueprint for development)
So for the export filter [for T3] would be the T3 yaml recipes covering the full audit trace (from start to end ! the whole manifest). The render should be a report of all the plots and data -> eg. can save plots, data (T3 data) and link there path into the report. Need to be timestamped (and maybe a way to trace back to original manifest ? hash of the manifest ?) Audit step and reasoning behind must be in the report. Then a html (easier than pdf ?) knitted report. Eventually if can extract the steps in plain text for data transformation (we might have to work with templates for that). Possibility to export html to docx or pdf via pandoc (OR OTHER TOOL python...). What you call the filter is basically the steps added by the users and their reasoning - for me it is the audit part that NEEDs to be recorded and go into the report - to ensure that the user do not loose transformations done and associated reasoning. 

If we need to apply another node (transformation : how do we enter it ? text ? as in manifest ? with arguments ?)

- Does transplanting from Gallery require reasons on the cloned nodes immediately, or can it be deferred until `btn_apply`? deferred until btn_apply but no apply if not filled
- When the user switches Home → Gallery → Home, do the T3 nodes survive YES, and does the gallery know which sub-tab was active to offer context-relevant recipes (YES - well it needs to know which tab shows because then it can clone the recipe in the correct tab)?

Other questions ? 

- Gallery "Export to T3" always goes to the Home T3 sandbox for the **last-active plot sub-tab** YES  - maybe a ghost T3 save when swithing tabls ? could that work to ensure no loss ? 
- Switching Home → Gallery → Home restores: active group tab, active plot sub-tab, tier toggle state, pending/applied filters, T3 recipe nodes - YES

When T1/T2 filter, select do not change the data - they allow preview of the data. 
When T3 filter/select state applied - then it is really modification of T3 data at apply

Define the Home module state object that survives panel switches: sub-tab, tier toggle, filters, T3 recipe - need to keep the state of the T3 (aqua your are editing and you want to go back continuining editing)

# Functioning of the UIO audit
Please review The attached document. (2026-04-07/Viz_work/Gemini-Agent_Viz_prep.md) It is an earlier vision of the dashboard, before starting implementation. Much of it is to be considered as legacy, but some elements might be worth to pick up and discuss to improve the current UI. 

So please review, and check what is legacy (new decisions) and not officially decided or could be used. 

Also I would like to be able to define how the data audit trace (For Tier 3) will work, as it is related also to which data will be exported. 

Here are the current thoughts.  For Tier 3, it is used when a user want to adjust plot / data. Used case eg. Fitlering out outliers, filtering out some categories (eg to few samples to be analyzed correctly)
- Dependent on Persona
- Aimed for small adjustments (data / plot layout)

- Need full transparency : what has been changed. And the reason for the change HAS to be added in the audit. Eg this point is error because was problem x in the lab and instrument X failed ..., or detected misslabelling of sample in LAB id is incorrect 

- Need to be able to save new manifest / session when auditing, incl. ghost 
- Export recipie in gallery should allow to export steps to the Tier 3 recipe. Note that in this case we need also to ensure that when changing of the "module" view in the UI between (HOME, Gallery) that it recall the last state of the module, allowing transfer of informaiton between modules. 


