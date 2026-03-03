## Orchestrator: app_shell/server_logic.py

### Data filtering -> loop 
In Shiny, filtering is a "Reactive" event.

The UI (Display) provides a slider or dropdown.

The Orchestrator (Logic) detects the change.

The Orchestrator applies the filter to the Data Tier 2 dataframe.

The Orchestrator sends the filtered data to the Visualization Factory.

Why? Because the Visualization Factory should be "dumb." It shouldn't know how to filter; it should just draw whatever data it is handed.

### The Workflow:
Instead of sending data back to the transformer.py file (which should be "pure" and handle the heavy lifting of merging), the Orchestrator handles the "Light Filtering" in memory.

Ingestion: Reads raw files.

Transformer (The Heavy Lifter): Merges Bio-data + Metadata once. This creates the Master Data Tier 2 (the "Full Dataset").

Orchestrator (The Filter): Holds that Master Table in a Reactive Value. When the user moves the "Year" slider, the Orchestrator creates a "Filtered View" (a temporary subset) in memory.

Viz Factory: Receives only that "Filtered View" and redraws the plot.