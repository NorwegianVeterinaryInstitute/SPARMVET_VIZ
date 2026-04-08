# UI definition - How it should work


## Questions #REVIEW 
Need to account for scallability, reusability and maintainability, and growth of the UI components and features over time.

1. How to define the UI components and how to make it flexible and modular for different use cases ? Configuration with UI compenents, properties, events and layout ? Is it possible to do the UI design via a configuration file ? (eg. yaml) - so that we can have different UI designs for different use cases and users ?

2. We might need to review how the data tier is functioning and how we can make it interact with the UI components for the user experience 



## Configurations
> Configuration files: Yaml 
stored in : .config/ui

1. User - Pipeline 
2. Developer - and Gallery 
3 ... needs to be adjustable configurations

Common configuration summary 
- Multipanel 
- Sidebars 
- Cards (tabs) : plot and data table - With possibility to maximize data table associated to the plot -> grid layout Top is the Plot and Bottom is a wide data table 

Saving paths must be configurable for the ui must be configurable
- location 1: (specific for each system where the app is implemented - must be configurable) data tier 1 and data tier 2 (eg. if development settings can use eg location 2 also )
- location 2: for data tier 3 or imported data and session saving ...that will create the data tiers 1 and 2 and can include manifests) - can eg. auto populate with subdirectories -> export, session saving (*Local-Storage "Ghost Manifest"** should be automatic in the session saving regular, keep eg last 5 versions or so), imported data, ... 
- location 3: for the galery (data and examples plots) (eg. cloned from github repo) -> this will  contains the manifests and example plots for each type of data/plot available in the gallery. (default save in the project is .gallery) and each will have one subdirectory per type of plot (data + manifest) - this will need to be populated 
> Note will need a system to allow user to request adding to the galery -> eg via github pull request or issue ? make a link for example when the people design new plots ... to allow that 

UI settings can control #REVIEW should this done by mode choice or by selecting the configuration file for the ui?
- mode eg. fixed/locked (pipeline) - no selction option, no modification options - with export options (no need to save session if no modification possible)
- semi-fixed (pipeline with exploration of data) - with export options and save session options 
- mode eg. external data / developper : manifest helper (import, creation, wrangling helper and plot designer eg with galery), create artifical data and submit plot to the gallery ? with export options 

We could of course make some variants 

So will require a **BOOTOLADER FOR THE UI** -> check environment and get its persona


| UI Component | Role in Platform | Expansion Path |
| --- | --- | --- |
| **DataConnector** | Handles File/DB/Galaxy inputs. | Add IRIDA/API connectors later without touching the plots. |
| **WrangleStudio** | The interactive manifest builder. | Add new "Drag-and-Drop" nodes as Transformer grows. |
| **VizViewer** | The multi-tab/max-min plot engine. | Support new Plotnine/D3/Plotly types via the Viz Factory. |
| **AuditEngine** | The "Locked Log" and Export logic. | #REVIEW ... unsure Add "Cloud-Sync" or "Blockchain-Signing" for high-reg audits. |

#REVIEW should we build that as ui modules ? I think so .. Wrangler UI, The Viz UI, The Gallery UI -> so we need a component registry and we need a correct structure ...

Test ui configs -> shiny.test to run headless simulations 


## Data tiers and User experience / usage in the UI
- DATA table : spreadsheet like experience 
    - users can filter directly in a search box at the top of the column 
    - users can highlight specific rows - viz factory update to highlight those values

- Exploration data - interactively and re-definition of the tiered data functionning
    - #REVIEW : cannot be done on aggregated data ! so we need to be able to view the data tier 1 - BUT then the data tier 2 should only contain reformating (aggregation, long format transformation for the plot) - NO DATA FILTERING AT ALL - So data tier 2 is the layer that allows the formatting for FAST plotting. 
    - Data tier 2 associated to each plot. Data tier 2 must be persistent to allow to go back to the plot created from all the data (only formated correctly) 
    - Data tier 1 can be branched into several data tier 2 (allowing reusability to create different plots)
    - To allow data exploration (creation of new plot - eg a restricted selection of samples from the data tier 1)  - we need to have a selection/filter step that can be added / integrated with the data tier 2 (so the way of doing the plot remain the same, unless with less data). So for example the user should see the recipe from going from datatier 1 to the plot (data tier 2 or data tier 3 : dedicated to user exploration) 
    - There should be a save session to allow saving the data tier 3, and all the steps that were added to the data tier 2 (and listing the data tier 1 transformation steps - wrangling, selecting, filtering AND merging with metadata)

Naming labels of data tiers in the UIi: 
1. Data tier 1: "Raw data (Tier 1)"
2. Data tier 2: "Formatted data (Tier 2)"
3. Data tier 3: "Filtered & Formated data (Tier 3)"

Anchors for data tiers : IMPORTANT TO #REVIEW
1. Data tier 1: "Raw data (Tier 1)" -> Anchor : "id_raw_data_tier_1"
2. Data tier 2: "Formatted data (Tier 2)" -> Anchor : "id_formatted_data_tier_2" With a note that the data tier 2 is the formated data tier 1 allowing display on the plot (maybe in an ? button ?)
3. Data tier 3: "Filtered & Formated data (Tier 3)" -> Anchor : "id_filtered_formatted_data_tier_3" (session save) - With a warning that if aggregating can take some time to update #REVIEW unless better solution for that ? 

Locations of saving data tiers:
- must be configurable where the data tiers are saved - so that we can have different locations for different use cases and users (eg. local, server, cloud etc) - and also to allow for scalability and growth of the data tiers over time. This can go into a config file for the integration of the system with the data storage solution. (eg. integration with galaxy, irida, local computer etc)
- For data tier 3: must ensure that the user has access to the save location 

Checkbox to show/hide data tiers on the plot (or not show at all): must either show data tier 1, data tier 2 or data tier 3 - cannot show all three data tiers at the same time if only one plot. 

Functioning of data filtering for data exploration:
- in data tier 3 -> should inherit the wrangling steps from data tier 2. BUT it should be possible to add fiters before (eg. removing outliers) and eventually select (before or after) eg. removing some columns from the view. 
- all steps must be recorded within a recipe panel -> "Transformer-compatible audit Trace" into a manifest (eg. excluded samples X : reason Z)
- if possible  should have possibility to copy the filters applied to another plot that share the same data tier 1
#REVIEW : That would be nice to have possible actions associated -> so if we do the tier3 transformation on the left side panel, would it be possible eg. to have a list of actions to choose from ? 

Reverting to data tier 2: if the user wants to revert to data tier 2, it must be possible, to have a fast revert, so the plot from data tier 2 shows rapidely


Eventually: 
- possibility of grouping plots by type of analysis (eg. QC plots ... vs results plots).  
eg. QC plots groups : distribution check, missing maps, ...
eg. of different groups Global stats, QC analysis groups, several individual types of analyses

- outlier flag -> specific UI button where can clic and point and ex. exclude this sample and / or - select this sample to view the data ? like a preinspection or possibility to drop ? ? click and brush OR coordinate mapping ? eg to select points that are in a certain area and be able to look or exclude those points ? #REVIEW : how to do that ? advantages and inconvenients of each solution ? Eg pop up that ask if want to see or exclude those samples 


## UI DESIGN 

One tab per plot (for all data tiers) : several tabs for several plots. Each tab has the same layout but different plots are done. 


1. Central Panel: Plot + DATA preview (eg. head for large data sets, or full data table if not too much memory required)
- Plot in the upper part of the central panel, and data table in the lower part of the central panel.
- if data not shown would be nice that the plot can be scalled
- Eventuall possibility of showing two plots side by side in the central panel - eg. one plot with the datatier 1(or2) and one plot with the datatier 3 to allow comparison between the raw data and the filtered data. So that would mean a grid where 2 plots on the top and the corresponding data tables on the bottom. Could be with a check box solution to allow this
- If possible: data filtering associated with the data table (so user can see the changes in the data)
    - all columns should be filterable (several filters can be applied simultaneously eg. year < 2020 and year > 2018., or Country = Norway OR France ) - automatically find columns that can be selected and filtered ...
    - all but the primary key columns should be hideable (eg. selection of columns to show or hide) - Solution to do that ? show hide button ? 
> Note: If not possible -> then we need a drop down on the left panel to do the data filtering and selection of columns that can be extended / reduced - and maybe all other functionalites on the left panel will also need this expand reduce functionality to avoid having a very long left panel with all the functionalities.
- number of plots tabs to be deduced by the manifest (dymamic discovery)

2. Left panel :
    1. Navigation panel 
        - groups of plots (eg. QC plots, global stats, ...)
        - plots within each group (eg. plot selector)
    2. Eventually depending on choice - filters / select menu (then will need an shrink/expand button to avoid having a very long left panel with all the functionalities) - depends if we have that on table or not 
    3. Save session / load session button (needs to be able to save fast) -> selector when (go to default user directory session saving)

3. Right panel : 
    1. The recipe panel to process the data (history sidebar) (transformation audit)
        - The wrangling steps : showing the wrangling steps default from the data tier 2 (must be there but can not be removed - maybe in a different color) 
        - The filtering steps : showing the filtering steps added by the user and applied to the data tier 3 (if any)
        - The selecting steps added by the user and applied to the data tier 3 (if any)
        - Each wrangling step added by the user must have comment (eg. reason of the step) and must be removable so that the user can go back to the previous step if needed.
        - reason of step given by the user must be viewable (eg. can be on hover or visible on the side or under)
        - steps modified by the user (eg. filtering or selecting must be removable, one by one)
        - must be an active save / version history of the data tier 3 (AND A DEFINITIVE SAVE - EG SAVE SESSION - so the user can go back to unfinished work)
        - eg possibility to add title and subtitle to the plot ? 
        - audit must always list primary keys that are affected eg. select year < 2020 -> list the primary keys (samples that have been removed)
    2. Plot reset button (going back to tier 2)

4. #REVIEW - Unsure what is best, if central panel or side panel: Global export panel (generate report and export)
- choice of plot to export and which data tier (1/2 or 3) to export with the plot (if any)
    - choice of export plot format (png, svg, pdf) - need appropriate naming
    - choice of export data format (tsv, csv) -> must be transformed from parquet files.
    - export of the total wrangling recipe (complete: as shown on the plot that is exported for each plot exported - eg data tier 1, + filters applied + plot formatting - needs to be commented of what part is what)
    - should be able to select the export location (directory - Naming should include date_time then tier3 plot if any, tier 2 plot AND data manifests for tier3 and tier 2 - All steps included including the wrangling steps from tier 1  -> recipie must be reusable)
    - naming should be consistent and appropriate. The user must only be able to choose part of the name, which should be used in all the files export. ALSO enfore NO SPACE in the name to avoid issues with the export and re-use of the files.
    - Must allow to export the whole config file applied (in zipped form) - for archive
    - single click bundler - to export all. 

    eg: export : 
    - naming attern directory: date_time_<user_defined_name>/ (user choose location and user_defined_name)
    -  date_time format: YYYYMMDD_HHMMSS
    - files exported:
    - plot : date_time_<user_defined_name>_plot_<plot_id>_tier3.png (or svg, pdf) (if any - if not data tier 3 then only tier 2) (note that tier 2 can be = tier 1 if no formatting applied)
    - plot : date_time_<user_defined_name>_plot_<plot_id>_tier2.png (or svg, pdf)

    - data tier 3 : date_time_<user_defined_name>_data_tier3.tsv (or csv) (if any - if not data tier 3 then only tier 2 and tier 1)

    - data tier 2 : date_time_<user_defined_name>_data_tier2.tsv (or csv) AND/OR ter 1
    - data tier 1 : date_time_<user_defined_name>_data_tier1.tsv (or csv)

    - recipe : date_time_<user_defined_name>_recipe_tier2.qmd - with all the steps and comments included
    - recipe : date_time_<user_defined_name>_recipe_tier3.qmd - with all the steps and comments included (if any)

    - config file : date_time_<user_defined_name>_config.yaml  - with all the config files for all the data exported (so can be several files eg. the whole directory and included files -> must be in a zipped format) for archive and re-use of the config file for the same analysis in the future. 
    Naming: date_time_<user_defined_name>_config.yaml (if one file) if many files then date_time_<user_defined_name>_config.zip (with all the config files included)
    -> so config file for data tier 1, 2 and 3 must be included and named appropriately in the export config file.
    - export lock - cannot export only graph - data and recipe must be associated. 
    - overal quarto report that describe the data, and associated plot with which file names --- quarto template with knit -> so the user can have an overview. (knit: html, pdf, docx). Have a structure for each data tier and associated plot and the changes/data processing steps. Eg.use pandoc if necessary for export to docx. Eg if plot modification print original + modified plot side by side with the data changes/recipe.
    - need proper log for the different data tiers and must be clear what is done: tier 1, tier 2/3 and what is the difference between them so it can be used for publication 
    - export standard present: web/presentation vs publication ready (then at least 600 dpi for publication quality. (favor svg by default)
    - some explanations about the choices eg (? button on side of options with explanations) 




### Options : additional panels and features
#REVIEW I think actually that should be its own panel - central - adding functionalitest #REVIEW how should we build that ? 

1. Optional: depending on UI settings (eg. fix pipeline / possibility to add metadata) 
    - import helper for the data : take a excel files with the data or metadata and transform it into tsv files that can be used for the data tier 1. Save in a directory selected by the user.
        - data, metadata and additional data -> needs to allow and help primary keys matching helper pattern and verification
    - then import several individual datasets (eg. a  + add import button) for different datasets or import all in a directory and then eg select type, primary data, metadata, additional data (and select eg primary key) that should allow join of metadata (eg. wuld be nice if we could have a preview of the joining of data with metadata - to ensure that the joins are correct) 
        - eg data from a pipeline, import all the datasets (add one directory with all the dataset)
        - eg. specify the metadata file 
        - eg. add external datasets (eg merging with data obtained from another pipeline)
    - possibility to upload predefined manifest (for data / metadata)
    - possibility to pre-create manifest (manifest helper)
    - helper to apply transform and merging steps and create plots 

1. Optional: Gallery exploration settings
    - A way to look at galery examples (eg. can be toogled)
    - will select example data and plot -> and show in a specific tab the examples (for developper and inspiration for users -> important that the examples of data processing can be exported here and /or copied) 
    - allow to export the manifest and associated data, from all tiers, so can help user to reconstruct the steps similar for their plots 
    - allow showing how the data contract is build 
    - eventually -> helper to add those same settings to one of own dataset (or copy to sandbox to help make it)

1. Optional central panel: possibilty to design own plot with a plot builder
    - branching logic - eg branch from already tier 1 (or tier 2) data OR uploaded data
    - helper to choose the type of plot
    - helper to wrangle the data
    - helper to format the plot (eg. title, axis, colors, ...)
    - helper to add filters and selection to the data (eg. for data tier 3
    - helper to add the aesthetics osv. ---
    - option to submit the plot to the galery - will need data agreement or generate fake data !
    - eg option to copy clone manifest so can be adjusted from a model 