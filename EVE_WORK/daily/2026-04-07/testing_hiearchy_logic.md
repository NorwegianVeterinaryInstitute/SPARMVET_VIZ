### 🧪 Testing Hierarchy & Logic

To maintain architectural integrity, the project follows a three-tier testing strategy. Every library MUST implement the following structure to ensure both isolated logic and organic system functionality.

#### 1. Component Debuggers (The Execution Engines)

`libs/{lib}/tests/debug_{component_name}.py`

* **Purpose:** These are the functional "runners" that know how to process a specific logic layer.
* **Transformer Example:** * `debug_wrangler.py`: Executes Layer 1 (Atomic) transformations.
  * `debug_assembler.py`: Executes Layer 2 (Relational) joins and assembly.
* **Rule:** These scripts MUST use `argparse` to accept a `--manifest` and `--data` path, allowing for manual, isolated debugging of any single feature or pipeline.

#### 2. Atomic Test Triplets (The Feature Units)

`libs/{lib}/tests/data/{feature_name}_{triplet_part}`

* **Purpose:** Every registered decorator or action MUST have a 1:1:1 test triplet:
    1. **Data:** `{feature}_test.tsv`
    2. **Manifest:** `{feature}_test.yaml`
    3. **Evidence:** `tmp/{feature}_debug_view.tsv` (or `.png`)
* **Logic:** These provide the "fuel" for the Component Debuggers. To test a single decorator (e.g., `strip_whitespace`), the `debug_wrangler.py` is called using the `strip_whitespace_test.yaml` manifest.

#### 3. Global Library Wrapper (The Integrity Orchestrator)

`libs/{lib}/tests/{lib}_integrity_suite.py`

* **Purpose:** An automated "Full-Scan" runner that ensures the entire library functions organically.
* **Logic Flow:**
    1. **Discovery:** Programmatically queries the library's Registry (e.g., `AVAILABLE_WRANGLING_ACTIONS`) to find all implemented decorators.
    2. **Iteration:** For each action found, it locates the corresponding Test Triplet.
    3. **Execution:** It dispatches the appropriate **Component Debugger** (Wrangler or Assembler) to process that specific test.
    4. **Reporting:** Yields a comprehensive `{lib}_integrity_report.txt` in `tmp/` detailing [PASSED] vs [FAILED] status for every component.
* **Rule:** This suite MUST be executed after any broad refactoring to detect regression errors across the entire library.
