# Yaml dashboard configuration strategy - YAML library 

We have decided to do the configuration files for data manifest as yaml and also to specify plotting defaults.
Connectors, if understand well, will define how to get the data from the API and will also use yaml for configuraiton. So if there are different API there will be different configurations files that explain how to get the data but the functions to get datawill be the same

We need a strategy to increase reusability and decrease repetitions
For example, for some pipelines producting data for different species, the default plotting settings and even the data schema can be either identical or very similar (at least the same categories of columns eg. AMR_genes, where Species A and B have each their own set of AMR_genes) and the plotting defaults can be identical. 

Thus we should be able to write generic configuration files, while keeping the possibility to use specific configuration profiles if needed.

For the **Connectors**, the "Get Data" function is like a generic power outlet, and your YAML configuration is the "Adapter" that tells it whether to plug into a Galaxy History, an IRIDA project, or a local CSV.

 

? Reference the templates and inject species-specific metadata.
- yaml configuration files libraries  #REVIEW how to do that ? What structure to adopt ? 


ove toward a configuration-driven architecture (**Externalized Configuration** combined with the **Strategy Pattern**).

we should implement a **Component Registry**.



If Species A and B have different genes, your YAML should define a **Semantic Grouping**.

*   **Constraint:** Your data must be "Tidy" (Long-format). Instead of 100 columns for 100 genes, use: `Sample | Gene_Name | Result`.
*   **Benefit:** Your plotting function just filters for `Gene_Name` based on the YAML list, keeping the code clean.

#### Connector Logic

*   **The "How":** The Python function `fetch_data(source_type, params)` remains constant.
*   **The "What":** The YAML provides the `params` (e.g., `API_KEY`, `HISTORY_ID`).
*   **Benefit:** If you move from Galaxy to a different API later, you just write one new connector function and update the YAML. The UI code never changes.



### 3\. Lead Dev Mode: The "Walking Skeleton" Implementation

Prototype of this logic. 
- A config loader reads the YAML
  - pass instructions to connector -> API to fetch data
  - pass instructions to ingestion (checks data format) ok ->  transformer/wrangler tidy long format ?   
  - pass plot defaults to factory uses those instructions.
  - sent plots to dashboard

#REVIEW -> so yaml define wich plots will be showned in the dashboard and how correct ? 

# REVIEW -> fetching data eg. if different histories in galaxy are in different runs

**Reference & Injection** pattern. 

Since you are using YAML dictionaries, we can treat your "Generic Plots" as a library of blueprints. 
Your species manifest then simply "calls" those blueprints by name and tells them which specific columns to use.

Instead of one giant file, we split the logic into two types of dictionaries:

1.  **The Library (The "How"):** 
A dictionary of plot archetypes (e.g., "The AMR Heatmap", "The Phylogenetic Tree"). These define the geometry and style but leave the data columns as variables.

2.  **The Manifest (The "Who"):** A dictionary of species. Each species "subscribes" to plots from the library and provides the specific "keys" (column names) for that run.

*   **Decoupled Logic:** If you want to change the color scheme of all AMR plots across 10 species, you change it in **one** place (the library).
*   **Scalability:** If a new species doesn't have a Tree, you just don't include the "Tree" key in its manifest. The Dashboard Engine will only render what is explicitly requested.


```
species:
  listeria_monocytogenes:
    history_id: "hist_xyz_789"
    active_plots:
      - template: "amr_heatmap"
        mapping:
          x_axis: "sample_id"
          y_axis: "gene_family" # Categorical group
          values: "resistance_score"
      - template: "core_genome_tree"
        mapping:
          file_ext: ".nwk"
          metadata_overlay: "lineage"
```
| **Separated Files** | Very clean; one file for "Style," one for "Data." | Requires a "Join" step in your Python code to link the two. |
| **Nested Dictionaries** | Extremely easy to iterate through in a loop for the UI. | If the YAML gets too deep (3+ levels), it becomes hard for humans to read. |

#QUESTION : what are the possibilities : allowing general configuration defaults to be passed to the global manifest while allowing manifest to be specific if necessary. 
#QUESTION : how can we best organize the config directory to create libraries for each respective type of yaml config file ? 