
#manifest #improvement #rules
### 1. What questions showed that manifest rules were not explicit enough?

- **The Column Projection Law**: When you asked "where the gene column was filtered," it revealed that the **`final_contract`**’s role as a _strict whitelist_ (Projection Guard) wasn't explicitly stated. In standard YAML, users often assume that if you don't mention a column, it is simply passed through. In SPARMVET, it is dropped.
- **The "Silent Skip" Confusion**: Your concern about `sequence_type` showed that our "Resilient Ingestion" (ADR-013) is too quiet. While it prevents crashes, it masks intent. We need a rule/update that **warns** when a requested field is missing from the source.
- **The Type Casting Ambiguity**: The `Year` float-vs-int issue showed that we lack a "Biological Typing Standard." We need a rule stating: _"Any field used as a discrete categorical in plots (e.g., Year, Tier) MUST be explicitly cast to Int or String in the Tier 1/2 manifest."_ %%Unsure the plot is still not correct%%

### 2. Rules I followed that were not in the explicit protocol

- **YAML Keyword Nuances**: I had to apply a "Technician's Rule" to quote the `'on'` key in joins because it's a reserved YAML boolean. This isn't in any SPARMVET doc but is required for valid manifests. %%This is taken care of normally in the code %%
- **Directory Mirroring (ADR-041)**: The protocol in `ui_manifest_integration_testing.md` focuses on the _test execution_, but the _structural organization_ (putting fragments in `basename/` folders) is hidden in `rules_manifest_structure.md`. For a new user, this "Mirrored Directory" requirement would be a major roadblock.
- **Library Test Locators**: I had to discover 
    
    ![](vscode-file://vscode-app/usr/share/antigravity/resources/app/extensions/theme-symbols/src/icons/files/python.svg)
    
    debug_wrangler.py and 
    
    ![](vscode-file://vscode-app/usr/share/antigravity/resources/app/extensions/theme-symbols/src/icons/files/python.svg)
    
    debug_assembler.py by scanning the file system. The testing protocol mentions `@verify` but doesn't explicitly say: _"Use wrangler for Tier 1, assembler for Tier 2."_

### 3. Missing instructions to proceed without your feedback

- **Tier Visibility Requirement**: I assumed you only cared about the terminal result (Assembly). I lacked the instruction: _"Every materialization MUST provide a separate download link for Tier 1 (cleaned ingredients) to facilitate scientific audit."_
- **Column Carry-over Policy**: I lacked a directive on whether to keep "Original Identity" columns (like `gene` or `Accession`) in joined assemblies.
- **Renaming Logic Strategy**: I didn't have a clear "Clean Naming" convention (e.g., suffixing wrangled columns with `_clean` vs replacing them in-place).

### Next Steps & Task Update:

I have added a task to our backlog: **"Implement non-breaking Warnings in DataIngestor for missing Manifest Columns."**

I will now update the `Instruction.md` with these insights to ensure the next lineage build is more autonomous. Shall we begin **Lineage 2: Plasmid Dynamics** using this improved understanding?