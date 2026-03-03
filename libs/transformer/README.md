Data Tier 1 (Cleaned Bio Data) and Data Tier 2 (Augmented with Metadata) usually happen in sequence, but they belong to the same Logical Layer (The Transformer/Wrangler).

- Tier 1 (Wrangling): Standardizes the bioinformatics tool output (e.g., Column renaming).
- Tier 2 (Augmenting): Joins that clean data with the user's uploaded metadata (e.g., adding "Collection Date" or "Patient Age").

They live in the same "Transformation" folder (libs/transformer/), but they are different functions. You want to keep them separate so that if the metadata upload fails, you can still show the Tier 1 results.


The Transformer (transformer.py) is designed for "Heavy Transformation" (CPU-intensive joins). The Orchestrator is designed for "Fast Reaction."
- If you call the Transformer every time a user moves a slider, the app will feel laggy.
- If the Orchestrator just filters a table that is already in memory, the "Re-plot" feels instantaneous.