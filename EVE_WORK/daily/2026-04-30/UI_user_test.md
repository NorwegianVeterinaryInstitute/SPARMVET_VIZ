


# Functionality check 

## Testing  (Phase 22-J) 

- [ ]  Source data files changed - reassembling data -> would be nice to know when done. Right now does not appear to save/replace the reassembled data, because it appears to do that everytime I change between manifests 
- [ ]  hum, I think there is wrong, it says source data has changed for 2_test_data_ST22_dummy. To my knowledge you changed : manifest not data, that can be confusing to say "source data changed" when its the manifest that changed, so we need to find better message. It produces this message in each change of project in the selector, it does not mark it as done. So I think the data might not be writting correctly ? There is at least a bug 






## HOME (Other testing / improvements)
We will review and decide together and create a task list and update architecture decisions and any documentation before we make changes to the code. 



### Left sidebar 

Data Navigator: 
- Add a data navigator -> available all UI persona (ingestion)
- Project navigator (is actually manifest navigator) - > conditional availability per UI persona: not available for simple pipeline automated persona, available for project-independent and advanced exploration personas (dev) 
- Add manifest ingestion (for advanced person) -> there is one down, maybe it would be more logic with the project navigator  ?
- Ensure that the data can be read using from data location defined in the UI persona (or in connectors). Ensure that configuration file for the simple automated pipeline persona points to 2_test_data_ST22_dummy manifest.
- Ensure ensure that the data provided as test in the manifest is overwritten if the users select a different directory or several data file in the UI. 
- Ensure that configuration file can point to use default test data in manifest (on/of) for testing purpose - then if off - the user must select the data (directory or several files eg from history) it want to if use with the active manifest.

Filters: Ok

System tools: 
I am wondering if we should split it (eg to allow also easier adaptation / on off for the different persona)

1. Export bundle (this export the audit report) 
- selection autit report format (html / pdf / docx) via pandoc 
- selection resolution (DPI) : web presentation / vs publication - Maybe a selector for resolution (DPI) with a little hoover to explain what to choose eg. publication > 600 dpb - 300 dpi is good for web / presentation ? 
- export plot format (svg, png, pdf) selector - default (? png - user know how to work with those)
2. Import / export session 

- select Web / presentation overlap with Export resume bundle - everything should be moved down - at least 10 px

- We had said we need to change the text in "Export Results Bundle". We can change to "name (no spaces, no special characters)". Maybe a little mouse hover on information to explain the naming requirement. 

- We have an import .zip session but not export a .zip session 

### Central panel / Theater 

Plots: 

- Plot rendering seems a bit slow - ? precomputed if no data changes ? seems to materialize slowly ? 

Manifest error :
- manifest 1_test_data_ST22_dummy (we need fix: demo of the app next Monday)
    - Virulence Variants plot : Render error: 'rotation'
    - Assembly quality dotplot - Render error: Aesthetic x references unknown column metric

Data Preview: Visible columns 
- Still width of the box where we can select the columns is not at the width of the panel (which makes it wrap over many lines when there are many columsn) - we should make it wider.

Pipeline audit : maybe make sure need to add and then apply (eg. Instead of -> Audit : send to Audit ? both in the central panel and left side bar ). 

Homogeneize ? Pipeline audit we have small trash/bin to remove the steps of the pipeline audit, could we have a small trash/bin for the filters steps instead of the cross (this just looks nicer)

Filters and audit corresponding: 
- Setting = exact France in filter -> country to "any of" in Pipeline audit - is mapping of audit to filters correct ?

Compare T2/T3 -> button does not hold -> gos back to other plot eg. quality control (so the state does not hold) then I cannot see what is ok


- Changing tabs is ok to see the new plots : Propagation of filters between plots - Does not seem to dispatch to all plots when selected, I think it should trace back to the row data (here it can  be eg. the metadata) but it can be that those same columns are also in different datasets - so here we need a duscussion and decision for the filters to ensure that it is repercuted correction. We need also to create a warning that the user must check that all those filters are applied correctly to the desired datasets (eg. explain might not be able to recognize this filter if used in other dataset)

- [X] Right sidebar shows `My Adjustments — <plot_id>` header (with the *currently active* plot's id) YES but it must be more visible : Boold un yellow background ? and a little space between the applied adustements ` 

- problem fitler of year (egm MLST bar) -> I think its because of the types .... whether we should string or numeric types

- cannot test difference between assembled and analysis ready I think because I do not think that I have a plot that required the data in the long format (I think I do not have the T2 data tier)

- [ ] In T3 mode, build a filter on a **non-key column** — e.g. on a similarity / value column, `value > 90`. [FAILED]
- Tested AMR heatmap : filter identity float -> applied : Rneder error : cannot compare string with numeric type f64 (so we have a problem of types casting / transformation that is either not done correctly in manifest or that should be tackled byt the code )

- [ ] Modal opens. The header reads "Add 1 filter/exclusion(s) — choose scope". The summary line shows your column name.
Unsure what you mean by that, but the adding and working of both filter and columns dropping appear ok except for numeric columns

- [ ] **NO** ⚠️ Primary-key warning banner inside the modal (since the column isn't a join key).
The no appears BUT it should be able to filter within primary keys - BUT not to drop primary key column - there is a difference 
- [x] Pending node appears in right sidebar. The node is a `filter_row` (icon: 🔍 Row Filter, NOT 🚫 Exclusion). -> filtering primary key should be alowed, just not dropping primary key colum, but there still should be a warning ! for both filter and droping


Part 3 
The warnings of what has been applied to how many plots has deseapeared  - before they were in the selector of all plots no ? now they are in the popups info - it can be ok but we then need a means to be able to keep track and review all those allerts , because it diseapear a bit too fast.

Part 4 
- your observation that propagation notifications disappear too fast. 
- The task references EVE_WORK/daily/2026-04-30/UI_user_test.md and notes the overlap with PROP-2 (filter inventory panel) — both could merge into one persistent "audit & alerts" panel in the right sidebar. You need to explain a bit more what you mean by that, the steps needs to be clear on the panel, if there are too many steps it will be messy no ? but yes there is an idea here. maybe we can have a little "allerts" button that we can look at or a little note on hover ? any other suggestions ? something simple and efficient is most welcome here.

- noted some switching between plots data / and when we change to T3 and when we change panel modes eg home to blueprint - I am wondering what we had decided for this behavior. I think at least it should not change when we trigger t3 and deselect it 

- we need to control the manifest and check that we can proprely test the ui - eg do we have a plot where t1 a and t2 different ? so we can check the difference ? 
- compare t2 and t3 really does not work, it push me to another plot 

- gallery import broke : `Import Jinja2` failed. DataFrame.style requires jinja2. Use pip or conda to install the Jinja2 package.
- gallery appers always visible on single persona  - either config wrong or conditional rendering not working / implemented
- Error in viz factory 

Part  5 

Should we also not add some specific persona for testing purposes ? Would that allow us to facilitate testing, and eventually partially automate ? 

First we need to consolidate what we have done today, we need to append to the daily loog


Export 
- Check only export what I want, after reformatting side bar 
- Html report is horrible, it needs to be human readeable
- Zip export export other manifests ... we need to fix (might be because manifest is a copy)
- Collapse plot panel (minimize possibility ? )

Theater 
- Collapse plot panel (minimize possibility ? )

## THEN PUSH GOOD ENOUGH FOR DEMO 

--- 

## EXPORT 



## Theather 

### Right sidebar / pipeline audit 

## Dev Studio 


## Gallery 

## Blueprint Architect 


