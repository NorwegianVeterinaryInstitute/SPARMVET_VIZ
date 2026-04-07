### ### 🧪 Testing Hierarchy & Execution Logic (step 3 - rewritten)

To ensure homogeneity across the project, testing is divided into **Engines** (isolated runners) and **Orchestrators** (full-suite validation).

#### 1. Component Debuggers (The "Engines")

`libs/{lib}/tests/debug_{component_name}.py`

- **Purpose:** These are the specialized execution scripts for the library's core components.
- **Wrangler Engine (`debug_wrangler.py`):** Dedicated to testing individual atomic decorators (Layer 1). It processes a single triplet (TSV + YAML) and materializes the output.
- **Assembler Engine (`debug_assembler.py`):** Dedicated to testing the multi-source join and assembly logic (Layer 2).
- **Rule:** These engines MUST be the exclusive way to verify new logic during active development.

#### 2. The Integrity Suite (The "Orchestrator")

`libs/{lib}/tests/{lib}_integrity_suite.py`

- **Purpose:** A high-level wrapper that automates the verification of the **ENTIRE** library.
- **Logic Flow:**
  1. **Registry Discovery:** It queries the internal `AVAILABLE_ACTIONS` registry.
  2. **Engine Delegation:** For each action, it automatically identifies if it requires the **Wrangler Engine** or the **Assembler Engine**.
  3. **Batch Execution:** It dispatches the correct engine to run the test and collects the result.
- **Rule:** This suite MUST yield a `{lib}_integrity_report.txt` and is mandatory before any Git commit or major refactor.

----

### 🧪 Testing Hierarchy & Logic (step 1 & 2)

To maintain architectural integrity, the project follows a three-tier testing strategy. Every library MUST implement the following structure to ensure both isolated logic and organic system functionality.

#### 1. Component Debuggers (The Execution Engines)

`libs/{lib}/tests/debug_{component_name}.py`

- **Purpose:** These are the functional "runners" that know how to process a specific logic layer.
- **Transformer Example:** * `debug_wrangler.py`: Executes Layer 1 (Atomic) transformations.
  - `debug_assembler.py`: Executes Layer 2 (Relational) joins and assembly.
- **Rule:** These scripts MUST use `argparse` to accept a `--manifest` and `--data` path, allowing for manual, isolated debugging of any single feature or pipeline.

#### 2. Atomic Test Triplets (The Feature Units)

`libs/{lib}/tests/data/{feature_name}_{triplet_part}`

- **Purpose:** Every registered decorator or action MUST have a 1:1:1 test triplet:
    1. **Data:** `{feature}_test.tsv`
    2. **Manifest:** `{feature}_test.yaml`
    3. **Evidence:** `tmp/{feature}_debug_view.tsv` (or `.png`)
- **Logic:** These provide the "fuel" for the Component Debuggers. To test a single decorator (e.g., `strip_whitespace`), the `debug_wrangler.py` is called using the `strip_whitespace_test.yaml` manifest.

#### 3. Global Library Wrapper (The Integrity Orchestrator)

`libs/{lib}/tests/{lib}_integrity_suite.py`

- **Purpose:** An automated "Full-Scan" runner that ensures the entire library functions organically.
- **Logic Flow:**
    1. **Discovery:** Programmatically queries the library's Registry (e.g., `AVAILABLE_WRANGLING_ACTIONS`) to find all implemented decorators.
    2. **Iteration:** For each action found, it locates the corresponding Test Triplet.
    3. **Execution:** It dispatches the appropriate **Component Debugger** (Wrangler or Assembler) to process that specific test.
    4. **Reporting:** Yields a comprehensive `{lib}_integrity_report.txt` in `tmp/` detailing [PASSED] vs [FAILED] status for every component.
- **Rule:** This suite MUST be executed after any broad refactoring to detect regression errors across the entire library.
