## loader.py : 

- reads the config files. The different parts of the configs info content need to be dispatched to the correct layers. 

- This file's only job should be reading those .yaml files in config/. It is the "Bridge" between your rules and your code.

- Gatekeeper: Runtime Validation (the user mistake) and Development Validation (the developer mistake).

1. Runtime Validation (The "User" Guardrail)
When the user says "I am working with E. coli" and fetches data, the Ingestion Layer performs a Structural Check. It compares the columns in the fetched file against the required_columns in ecoli.yaml.

If they don't match: The Ingestion Layer raises a specific SpeciesMismatchError.

The Orchestrator: Catches this and sends a message to the Display Layer (e.g., a Shiny ui.notification_show) saying: "Error: Fetched data does not contain expected E. coli markers."

2. Development Validation (The "Developer" Guardrail)
When you are adding a new species (e.g., S. aureus), you might "mess up" the YAML format. To fix this, we use a Meta-Schema (your config/templates/species_schema.yaml).

Before the app even starts, the Config Loader checks every YAML file in species_manifests/ against the Template.

If you forgot the plots: section in saureus.yaml, the app will refuse to boot and tell you exactly which line is broken.

### God VS BAD 
Bad Flow: Visualization calls Ingestion to get config. (Confusing).

Good Flow: Ingestion calls Misc for config; Visualization also calls Misc for config. (Both depend on a neutral third party).


## What I am not sure how to place yet

Will contain diverse utilities that cannot be categorized and that can be used across the different layers. 

? unsure : For example, a function to load configuration files, or a function to check metadata consistency.