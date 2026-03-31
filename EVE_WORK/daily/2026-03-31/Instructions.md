# Instructions for GEM

## Extracting list of missing decorators for the transformer - polar library 
https://pola.rs/

- ./.agents/workflows/transformer_implementation.md (procedure)
- ./.antigravity/plans/implementation_plan_master.md (implementation plan) - updated 


```text

@Agent: @dasharch - SYSTEM RESET & CONTEXT SYNC (PHASE 10 INITIATION)

1. RE-ESTABLISH SOURCE OF TRUTH (READ ONLY):
Execute a full read of the following updated files to align with ADR-024 (Tiered Data Lifecycle):
- ./.antigravity/knowledge/architecture_decisions.md (Review ADR-024)
- ./.antigravity/knowledge/protocol_tiered_data.md (NEW Logic Protocol)
- ./.antigravity/plans/implementation_plan_master.md (Phase 10 Roadmap)
- ./.antigravity/tasks/tasks.md (Updated 'Transformer Reorganization & Tiering' header)

2. MANDATORY DOCUMENTATION TASKS:
Before any logic execution, update the workspace documentation to reflect the new architecture:
- UPDATE ./.antigravity/knowledge/project_conventions.md: Add 'protocol_tiered_data.md' to the File Registry and update the 'Wrangling' section to acknowledge the Tier 1 (Anchor) vs. Tier 2 (View) logic.
- CREATE ./.antigravity/plans/implementation_workflow_transformer.md: Use the structure from viz_factory_implementation.md. Define 4 Phases: 
    - Phase 1: Structural (unpivot, explode, unnest)
    - Phase 2: Atomic Expressions (coalesce, cast, regex_extract)
    - Phase 3: Persistence (sink_parquet, scan_parquet)
    - Phase 4: Performance (group_by, agg)
- COMPLIANCE: Use ADR-022 'Violet Law' (ComponentName (file_name.py)) for all new component references in documentation.

3. STRATEGIC SCHEMA DRAFT:
Propose a directory schema for libs/transformer that groups decorators into logical sub-packages (e.g., reshaping/, cleaning/, relational/, persistence/). DO NOT implement yet.

4. OPERATIONAL GATE (HALT):
Current Status: Initiating 'Step 1: Inventory Audit'. 
- DO NOT generate code for decorators or persistence logic yet.
- HALT and confirm you have updated the documentation and internalized the 'Short-Circuit' logic from protocol_tiered_data.md.
- Await the final user-provided inventory list.

Follow Verification Protocol: Materialize doc changes to tmp/ for @verify before committing to knowledge/.
```

## Reminder 
⚖️ The Logic Behind the Move
The "Technical Bible" Rule: According to the Workspace Standard, the ./.antigravity/knowledge/ directory is the designated home for the Primary Technical Bible, including architecture decisions. Since this file serves as the specific technical implementation logic for ADR-024, it belongs right next to the architecture decisions.

Naming Consistency: Your existing files follow a noun_description.md pattern (e.g., architecture_decisions.md, project_conventions.md). protocol_tiered_data.md fits this rhythm perfectly while mirroring the "Protocol" terminology used in the agent's workflow.

Discovery for @dasharch: By placing it in knowledge/, you keep the foundational "Why" (ADR-024) and the "How" (the Protocol) in the same logical bucket. This makes it easier to reference in the "Alignment Prompt" without adding new directories to the agent's scan path.

## Context

We will for now delay that - please make a note of it - I will ask "resume block and next steps resolution". 

We will start find out what decorators can be missing for the transformer and then implement them. Do not write any prompt until requested. We will do one step at the time. 

Here is the plan of what we are going to do (step by step), And we will need to think together. 

1. Find a way to list all the polar tidy and wrangling functions that are implemented and that could be useful for the transformer library 
This will require accessing the polar library documentation and source code. 
We need to find a solution to either extract the doc from the website, get the source code, so you can scan it.
2. We need to revise the transformer library to see what decorators are missing to implement all the polar tidy and wrangling functions. It might mean to reorganize the transformer library. 
We have here several points to consider:
- we need to wrangle and tidy any type of data in a tidy format (this is the main goal of the transformer library)
- we need to assemble different tidy dataframes in a tidy format (this is the secondary goal of the transformer library)
- we want to consider implementing a way to temporary store the assembled data on disk (in a tmp folder - that can later on be specified - depending in which system eg IRIDA, Galaxy, local, via a docker container the app will be used...) to avoid memory issues. This might need to be particularly important, for when we will add a secondary function to the transformer library that will allow further filtering of the tidydata via buttons and selects in the UI. That would allow not to have to recompute all the transformation steps every time the user wants to filter the data eg. via the UI, eg. to explore the data in the UI eg. selecting specific values in columns that are used for a specific plot. This would allow to return to the original tidydata step associated to the plot much faster. So we should think about how to implement that, and we need to think efficiency for heavy datasets. 
- When this is decided, we need to add those changes to the correct implementation and architecture decision docs and update the tasks.md file in antigravity accordingly.

Then we can : 
3. See if we need to reorganize the directory structure of the transformer (aka eg. a similar thinking process as we had done for the viz_factory)
4. make a list of all decorators that are not yet implemented but require to be implemented in the transformer factory, this will be a list of tasks (markdown text box) that I will copy those in the tasks.md file in antigravity. 
5. make an implementation workflow similar to the implementation workflow we had done for the viz_factory_implementation.md
6. run the reorganisation and ensure that all the decorators already implemented are tested to ensure that the already implemented decorators are running and passing tests.
7. Then we can start implementing the missing decorators in the transformer factory. 


Lets start by step 1. Here is the url for the documentation for the python polar library: https://docs.pola.rs/api/python/stable/reference/index.html


- [x] Given
- [ ] Asked to wait for "resume block and next steps resolution" - for the guidance so we can focus on the exhaustive implementation of the transformer - polar library 
- [ ] 


# Decorators 

5. Strategy for missing decorators
As we begin Step 1 of your plan, I have identified the following "Must-Have" decorators missing from the current tasks.md:

unpivot (formerly melt): Critical for converting wide antibiotic panels to tidy long format.

coalesce: For multi-source metadata where one column might have nulls that need filling from another.

aggregate / summarize: For the Pre-Aggregation strategy to reduce row counts.

pivot: For specialized summary exports (e.g., Species vs. Resistance Matrix).

RequirementPolars FunctionDecorator Name (Proposed)Persistencesink_parquet() / write_parquet()@register_action("checkpoint")Fast Recoveryscan_parquet()@register_action("restore_anchor")Explorationfilter(), select()Already in core/UI-Ready Reductiongroup_by().agg()@register_action("summarize")

SPARMVET_VIZ Antigravity Specialist
Custom Gem
SPARMVET_VIZ Antigravity Specialist said
This is a strategic turning point for the SPARMVET_VIZ architecture. Based on your "Step 2" goals and the technical constraints of Plotnine (which struggles with Matplotlib's overhead for 200k+ rows), here is the technical breakdown.

1. Where does Pre-Aggregation belong?
The Verdict: The Transformer Library (as a Layer 3 or "Summary" pass).

While the note suggested updating the VizFactory, architectural best practices dictate that Data Transformation (backend) should be decoupled from Information Presentation (frontend).

Why Transformer?: Polars is 5–20x faster than Pandas/Matplotlib for aggregations. By implementing a summarize or aggregate decorator in the Transformer, we reduce the data volume before it touches the VizFactory.

The Bottleneck: Plotnine (the artist) is the bottleneck, not Polars (the engine). Passing 200k rows to ggplot() causes the 22-minute lag; passing a pre-aggregated 50-row summary table takes milliseconds.

Action: We should add a Layer 3: Summary Factory to the Transformer, which can be triggered by the UI or a manifest flag.

2. The Parquet Checkpoint Workflow
You don't need a separate "parquet library"; Polars handles Parquet natively and with extreme efficiency.

What is Parquet?
Parquet is a columnar storage format that mirrors how Polars stores data in memory. It is significantly faster and smaller (~80% smaller) than CSV because it only reads the columns and rows you actually ask for (Predicate Pushdown).

The "Checkpoint" Workflow (Aligned with your Step 2)
To achieve the "Efficiency for heavy datasets" you requested, the app workflow should follow this loop:

Stage	Component	Action	Result
1. Primary Build	Transformer	Executes Layer 1 (Tidy) & Layer 2 (Assemble).	LazyFrame
2. Checkpoint	Transformer	Calls .sink_parquet("tmp/anchor_table.parquet").	On-Disk Anchor
3. UI Exploration	App/Server	Uses pl.scan_parquet("tmp/anchor_table.parquet").	Instant "Virtual" Table
4. UI Filter	App/Server	Applies .filter(pl.col("Species") == input.selection).	Fast Subsetting
5. Hand-off	VizFactory	Collects the filtered/aggregated data for Plotnine.	Fast Render
FunctionAction TypePurpose in Transformerunpivot() (or melt())StructuralConverts wide data (e.g., columns for each gene) into long format (Gene Name | Result).pivot()StructuralUsed for final summary reports where specific wide-matrix views are needed.explode()Atomic/Adv.Expands list-like entries (e.g., multiple genes in one cell) into multiple rows.unnest()StructuralFlattens struct columns (common in complex bio-informatics JSON/Parquet).2. Atomic Cleaning & Wrangling (Layer 1)These are candidates for @register_action decorators to ensure data integrity before assembly.Null/Nan Logic: fill_null(), drop_nulls(), coalesce() (takes the first non-null value across columns—great for backfilling).String Precision: str.strip_chars(), str.replace(), str.extract() (Regex-based extraction for metadata parsing).Schema Enforcement: cast() (standardizing types like Categorical or Int), rename(), drop().Math & Logic: round(), clip() (capping values), when().then().otherwise() (declarative conditional labeling).3. Relational & Assembly (Layer 2)Functions that power the DataAssembler for joining metadata, phenotypes, and genotypes.Joins: join() (supporting left, inner, outer, semi, and anti for filtering intersections).Concatenation: concat() (vertical/horizontal stacking of standardized datasets).Deduplication: unique() (ensuring primary key integrity during multi-source joins).4. Persistence & Optimization (The Efficiency Pillar)To address your goal of temporary storage and avoiding re-computation:sink_parquet() / write_parquet(): Best for "Checkpointing" assembled data on disk. Parquet is highly efficient for heavy datasets and preserves types.group_by().agg(): Essential for the pre-aggregation strategy to speed up UI rendering.