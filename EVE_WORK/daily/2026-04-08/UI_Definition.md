# UI definition - How it should work


## Questions 
Need to account for scallability, reusability and maintainability, and growth of the UI components and features over time.

1. How to define the UI components and how to make it flexible and modular for different use cases ? Configuration with UI compenents, properties, events and layout ? 
2. We might need to review how the data tier is functioning and how we can make it interact with the UI components for the user experience 



## Configurations
1. User - Pipeline 
2. Developer - and Gallery 


## PIPELINE / User UI

1. Configuration file -> YAML

### Functionality and components 
#### Data processing for plotting  

1. Raw data must be attached to the plot : Label "Raw data" = Tier 1 data - Checkbox to show/hide raw data on the plot
2. Tier 2 data : Label "Formatted data" Formatted data that is derived from the raw data -> formatted for plot view (eg aggregation, long format etc) - Checkbox to show/hide tier 2 data on the plot)
3. Tier 3 data : Label "Filtered data" Filtered data - Checkbox to show/hide tier 3 data on the plot)
3. Must either show data tier1, data tier2 or data tier3 -  cannot show all three data tiers at the same time on the plot - Radio button to select which data tier to show on the plot (raw data, formatted data, filtered data), or none of them (checkbox to show/hide all data tiers on the plot)
    - Any filtering data needs to be associated with a filtering log
    - The formating of data for the plot needs to be applied after the filtering - so the filtering and formating of the data tier 2 needs to be applied by default, but we need an option to be able to add the filters before the formating of the plot. 
    - There must be an option to be able to reset and go back to the tier 2 data/plot -> so data tier 2 as parket
    - But then the data tier 3 is recalculated on data tier 1 and then the same steps of formating and ploting from data tier 2 are applied, just that the filters are applied before the formating of the data for the plot.

#REVIEW : here the problem is that we need to keep the plot formating but allow fitering of the raw data eg. to remove outliers.  The problem is eg. that eventual aggregation of the data must occur in the data tier 2, and then must be recalculated for the data tier 3 if there is any filtering to allow data exploration. 

4. All user filtering and data manipulation actions must be logged - and accessible - can remove laters 


#### Layout and design of the UI

1. One tab per plot type. So if several plots types, then several tabs. Each tab has the same layout and components but different configuration for the plot type. Each tab has several panels for the different components and functionalities.


1. Central panel: 
    - Display the plot and associated data 
    - Plot in upper part of the central panel, and data table in the lower part of the central panel. 
    - Data filtering - if possible associated with the data table, so that the user can filter the data directly from the data table and see the changes on the plot. (all columns of the data table should be filterable, and the filters should be associated with the plot so that the user can see the changes on the plot when applying the filters on the data table)

1. Left panel: 
    1. If not possible to have the data filtering associated with the data table in the central panel, then the data filtering can occur in the left panel (all columns must be filterable, several filters can be applied simultaneously eg. year < 2020 and year > 2018.
    1. Choice for export plot format (png, svg, pdf)
    1. Choice for export data format (tsv, csv)
    1. The export button: exports the wrangling recipie (complete: as shown on the plot that is exported - eg data tier 1, + filters applied + plot formatting - needs to be commented of what part is what)

     
1. Right panel : 
    1. The recipie panel to process the data
         - The wrangling steps : showing the wrangling steps default from the data tier 2 (must be there but cant be removed)
    - 


#REVIEW: is it possible to have the panel design and what they show to be defined in the configuration file ? So that we can have different panel designs and layouts for different use cases and plot types ?
