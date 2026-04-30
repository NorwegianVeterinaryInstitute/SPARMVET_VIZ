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


### Right sidebar / pipeline audit 

## Dev Studio 


## Gallery 

## Blueprint Architect 


