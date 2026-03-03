## Ingestion Layer

- Reads the raw file.

- Checks it against the required_columns defined in the YAML (Data contract : from the configuration layer, 
both for analysis data AND metadata).

- Ensures the data types are correct (e.g., "The 'Count' column must be a number, not text").

- Flags an error if the file is "corrupted" or doesn't match the species map.

- We should still keep a type: field inside the YAML as a "Safety Check." If the folder is species but the file says type: audit, the Ingestion Layer should throw an error before the app tries to draw a phylogenetic tree of lab submission dates!


Ingestion Layer must verify:
- "Does this metadata file have the required IDs?"
- "Are the columns named what I expect?"


When the Ingestion Layer (um_sanitization.py) runs, it will:
Look at the keys in fields (e.g., collection_date).

Check if that key exists as a column in the user's uploaded CSV.

If it finds it, it applies the type and format rules.
