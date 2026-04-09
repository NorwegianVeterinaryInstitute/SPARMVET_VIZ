### 🎨 The "High Theater" Layout Specifications

The layout will be split into two primary functional columns within the **Central Theater**:

|**Feature**|**Left Column: The Reference**|**Right Column: The Active Leaf**|
|---|---|---|
|**Top (Plot)**|**Tier 2 Plot**: Shows the "Gold Standard" view with all inherited branch logic applied.|**Tier 3 Plot**: Reacts instantly to UI filters and outlier selections.|
|**Middle (Toggle)**|**Data Tier Switch**: Toggle between **Tier 1 (Raw)** and **Tier 2 (Summarized)**.|**Inheritance Switch**: Toggle "Apply Tier 2 Formatting" (Long-format logic).|
|**Bottom (Table)**|**Immutable Inspection**: Scrollable, filterable table. Label: _View-only: For inspection and PK discovery._.|**Wrangle Studio Active**: The interactive table where selections directly drive the Tier 3 Plot.|

---

### 🛡️ Implementation Strategy: Protecting the Plot Logic

To ensure that user filters in **Tier 3** do not "break" the plot (e.g., by removing columns required for the Plotnine mapping), we will implement **Predicate Pushdown** that only affects the _rows_ and _non-essential columns_, while locking the aesthetic mappings defined in the manifest.

---

### 🚀 High-Precision Prompt for @dasharch

Copy and paste this into the IDE to execute the refined **Phase 12-A** layout:

Plaintext