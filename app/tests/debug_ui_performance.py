#!/usr/bin/env python3
from app.src.bootloader import Bootloader
import time
import os
import sys
from pathlib import Path

# ADR-016: Use Package-First Authority
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


def benchmark_persona_switch(iterations=100):
    personas = [
        "pipeline-static",
        "pipeline-exploration-simple",
        "pipeline-exploration-advanced",
        "project-independent",
        "developer"
    ]

    print(f"🚀 Starting UI Performance Benchmark ({iterations} iterations)...")

    # Measure Baseline (No Caching yet)
    start_time = time.perf_counter()
    for _ in range(iterations):
        for p in personas:
            bl = Bootloader(persona=p)
            _ = bl.is_enabled("comparison_mode_enabled")
    end_time = time.perf_counter()

    avg_time = (end_time - start_time) / (iterations * len(personas))
    print(f"📊 Baseline Average Switch + Lookup: {avg_time*1000:.4f} ms")

    return avg_time


if __name__ == "__main__":
    avg = benchmark_persona_switch(50)

    report_path = project_root / "tmp/ui_perf_audit.txt"
    os.makedirs(report_path.parent, exist_ok=True)
    with open(report_path, "w") as f:
        f.write("UI Performance Benchmark Report\n")
        f.write(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Baseline Avg Switch + Lookup: {avg*1000:.4f} ms\n")

    print(f"✅ Benchmark report saved to {report_path}")
