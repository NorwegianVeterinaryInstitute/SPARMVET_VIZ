# Functionning of the Left side panel


Conditional UI Logic

Left side panel
1. Project Navigator 
1.1 Selecting manifests : 
 - ability will depend on UI persona - developper mode yes - but not necessary for low personalities as manifest will be fixed : associated to a pipeline 
 - Note in manifest : data associated are "default data" - if user choose other data : main data : choice directory or file several files (eg. could be xlsx file - and must be able to say which data it corresponds to- will need to be associated to a project- needs to be ingested ) - how to do ? 

1.2 Selection metadata : might always need to be allowed to add updated metadata (but good if persona dependent also) - eg. allow to upload updated metadata for analysis (but fields must conform to minimal metadata required by the pipeline) 


2. System Tools (content also ui persona dependent)


2.1 Export 
- Export Results Bundle: (Minor) "Your name" must be a name but not necessary username - so could be naming (no spaces, no special char) - defensive : ensure no spaces and other special char 
- Selector Web / Presentation VS Publication -> web presentation overlap with Export results bundle : needs to be adjusted down (with all the rest) 
- Export results bundle : ok 
- We need maybe to add : export active graph -> BUT needs to also export recipe (and other elemens that made sure we have the same graph) - Person dependent also 
- Export : selector (will be based on where the user as access - eg- default Location 4 defined in config/connectors and/or Choose location : local pc)

2.2 Import / Save Session (instead of Restore Last Session) - Save location is defined by the save location of the user (config/connectors) eg. user might not have access to all the paths of the system - can be a subdirectory of where to export  

2.3 Specific data ingestion : only available advanced person / user or upon choice 
- Will need to be able to ingest full manifests (can be dir + or several files) so need a + button 
- Data ingestion : can be data , metadata, extra data 
- we need to have a way to add the manifest and add the corresponding data 

Metadata ingestion might be linke to the project metadata ingestion ? 

We will need to recover the functionality that we missed - to allow splitting xlsx into tsv to allow the data for different sheets to be ingested separately (but maybe that could be in the dev studio  but I thought this was more for developpers - so not for all ui persona) 

Should we add a simple excel to tsv converter in the System tools to allow depositing the tsv files in the directory where user will have access - so user will need to select which directory it wants to work into


Dev Studio : Filters on left side bar are not the point here - We will probably change that in this panel -> we will have to think more about usage - but this means that the Filters are also a conditional UI element - so persona/panel dependent



---

Overview of 

What is dependent of deployement context
What is dependent of persona (activity / user type)
- Functionalities activation by persona configuration : which part does what





 

