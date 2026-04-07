#!/usr/bin/env python3
import os
import sys
import subprocess
import datetime
from pathlib import Path
from typing import List, Dict

# Ensure project root is in sys.path for fallback
project_root = Path(__file__).resolve().parent.parent.parent.parent
# Add libs/transformer to sys.path to enable 'from transformer...'
sys.path.insert(0, str(project_root / "libs/transformer"))

try:
    from transformer.actions.base import AVAILABLE_WRANGLING_ACTIONS
    # Import subpackages to trigger registration via the auto-load strategy
    import transformer.actions.reshaping
    import transformer.actions.cleaning
    import transformer.actions.relational
    import transformer.actions.performance
    import transformer.actions.persistence
except ImportError as e:
    print(f"❌ ERROR: [Integrity Suite] Failed to load action registry. {e}")
    sys.exit(1)

# Paths
wrangler_runner = project_root / "libs/transformer/tests/debug_wrangler.py"
assembler_runner = project_root / "libs/transformer/tests/assembler_debug.py"
test_data_dir = project_root / "libs/transformer/tests/data"
pipeline_dir = project_root / "config/manifests/pipelines"
# Materialize output report
report_filename = f"{datetime.date.today().isoformat()}_transformer_integrity_report.txt"
output_report = project_root / "tmp" / report_filename


def run_suite():
    report_lines = []

    def log(msg: str):
        print(msg)
        report_lines.append(msg)

    log(f"[{'='*60}]")
    log(f" 🛡️  TRANSFORMER MASTER INTEGRITY SUITE (ADR-024 Audit)")
    log(f" Date: {datetime.datetime.now().isoformat()}")
    log(f"[{'='*60}]\n")

    # 1. CATEGORIZED INVENTORY
    log("📋 ACTION INVENTORY (By Tiered Schema)")
    log(f"{'Category':<20} | {'Action Name':<30}")
    log("-" * 55)

    categories = {
        "Reshaping": ["unpivot", "explode", "unnest", "split_column", "split_to_list", "to_struct", "pivot"],
        "Cleaning (Core)": ["fill_nulls", "drop_nulls", "replace_values", "rename", "drop_duplicates",
                            "unique_rows", "sanitize_column_names", "keep_columns", "drop_columns",
                            "strip_whitespace", "round_numeric", "filter_range"],
        "Cleaning (Expr)": ["regex_extract"],
        "Cleaning (Adv)": ["split_and_explode", "derive_categories"],
        "Relational": ["join", "join_filter"],
        "Performance": ["summarize"],
        "Persistence": []  # Phase 3 Future
    }

    registered = AVAILABLE_WRANGLING_ACTIONS.keys()

    for cat, actions in categories.items():
        found_in_cat = 0
        for action in actions:
            if action in registered:
                log(f"{cat:<20} | {action:<30}")
                found_in_cat += 1
        if found_in_cat == 0:
            log(f"{cat:<20} | [NONE REGISTERED]")
    log("\n")

    # 2. PHASE 1: WRANGLER TRIAD TESTS
    log("🧪 PHASE 1: ATOMIC WRANGLER TESTS (1:1:1 Naming Law)")
    log(f"{'Action Name':<30} | {'Status':<10} | {'Details'}")
    log("-" * 75)

    wrangler_results = []
    for action in sorted(registered):
        # Relational actions are tested in Assembly phase
        if action in ["join", "join_filter"]:
            continue

        manifest_path = test_data_dir / f"{action}_manifest.yaml"
        data_path = test_data_dir / f"{action}_test.tsv"

        if not manifest_path.exists() or not data_path.exists():
            status = "NO TEST"
            log(f"{action:<30} | 🟡 {status:<8} | Missing triplet in tests/data/")
            wrangler_results.append((action, status))
            continue

        # Execute via wrangler_debug.py
        cmd = [sys.executable, str(wrangler_runner),
               "--manifest", str(manifest_path)]
        try:
            # We use a short timeout to prevent hanging
            res = subprocess.run(cmd, capture_output=True,
                                 text=True, timeout=15)
            if res.returncode == 0:
                status = "PASSED"
                log(f"{action:<30} | 🟢 {status:<8} | Logic Verified (ADR-013)")
                wrangler_results.append((action, status))
            else:
                status = "FAILED"
                err_msg = res.stderr.strip().split(
                    '\n')[-1] if res.stderr else "Unknown error"
                log(f"{action:<30} | 🔴 {status:<8} | {err_msg}")
                wrangler_results.append((action, status))
        except subprocess.TimeoutExpired:
            status = "TIMEOUT"
            log(f"{action:<30} | 🟠 {status:<8} | Execution timed out")
            wrangler_results.append((action, status))
        except Exception as e:
            status = "ERROR"
            log(f"{action:<30} | 🛑 {status:<8} | {str(e)}")
            wrangler_results.append((action, status))

    # 3. PHASE 2: ASSEMBLY TESTS
    log("\n🏗️  PHASE 2: RELATIONAL ASSEMBLY TESTS (Layer 2 Recipes)")
    log(f"{'Pipeline Manifest':<50} | {'Status'}")
    log("-" * 75)

    assembly_results = []
    if pipeline_dir.exists():
        pipelines = list(pipeline_dir.glob("*.yaml"))
        for pipe in pipelines:
            # Skip contract-only fragments
            if "_contract" in pipe.name or "_fields" in pipe.name or "_wrangling" in pipe.name:
                continue

            cmd = [sys.executable, str(
                assembler_runner), "--manifest", str(pipe)]
            try:
                res = subprocess.run(
                    cmd, capture_output=True, text=True, timeout=45)
                if res.returncode == 0:
                    log(f"{pipe.name:<50} | 🟢 PASSED")
                    assembly_results.append((pipe.name, "PASSED"))
                else:
                    log(f"{pipe.name:<50} | 🔴 FAILED")
                    assembly_results.append((pipe.name, "FAILED"))
            except Exception as e:
                log(f"{pipe.name:<50} | 🛑 ERROR: {str(e)}")
                assembly_results.append((pipe.name, "ERROR"))
    else:
        log("[WARNING] Pipeline directory not found. Skipping Layer 2 tests.")

    # 4. FINAL INTEGRITY SUMMARY
    passed = len([r for r in wrangler_results if r[1] == "PASSED"])
    failed = len([r for r in wrangler_results if r[1]
                 in ["FAILED", "ERROR", "TIMEOUT"]])
    no_test = len([r for r in wrangler_results if r[1] == "NO TEST"])

    log(f"\n[{'='*60}]")
    log(" 📊 FINAL INTEGRITY SUMMARY")
    log(f" Total Registered Actions: {len(registered)}")
    log(f" Wrangler Passed:          {passed}")
    log(f" Wrangler Failed:          {failed}")
    log(f" Wrangler No Test:        {no_test}")
    log(f" Assembly Pipelines Run:   {len(assembly_results)}")
    log(
        f" Assembly Pipelines Pass:  {len([r for r in assembly_results if r[1] == 'PASSED'])}")
    log(f"[{'='*60}]\n")

    # Save the report
    os.makedirs(os.path.dirname(output_report), exist_ok=True)
    with open(output_report, "w") as f:
        f.write('\n'.join(report_lines))
    print(f"✅ Integrity Report Saved: {output_report}")


if __name__ == "__main__":
    run_suite()
