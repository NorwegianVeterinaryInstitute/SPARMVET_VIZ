



Reads the raw file.

Checks it against the required_columns defined in the YAML.

Ensures the data types are correct (e.g., "The 'Count' column must be a number, not text").

Flags an error if the file is "corrupted" or doesn't match the species map.

We should still keep a type: field inside the YAML as a "Safety Check." If the folder is species but the file says type: audit, the Ingestion Layer should throw an error before the app tries to draw a phylogenetic tree of lab submission dates!