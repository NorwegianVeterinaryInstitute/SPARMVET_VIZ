#!/usr/bin/env python3
from app.src.bootloader import Bootloader
import time
import os
import sys
from pathlib import Path

# ADR-016: Use Package-First Authority
# Setup path BEFORE any app imports
project_root = Path(__file__).resolve().parent.parent.parent
# if str(project_root) not in sys.path:
# STRICT BAN: sys.path.append / sys.path.insert are explicitly forbidden. Rely on pip install -e.


def benchmark_persona_switch(iterations=20):
    personas = [
        "pipeline-static",
        "pipeline-exploration-simple",
        "pipeline-exploration-advanced",
        "project-independent",
        "developer"
    ]

    print(f"🚀 Starting UI Performance Benchmark ({iterations} iterations)...")

    # 1. Baseline: Repeated Initialization
    start_time = time.perf_counter()
    for _ in range(iterations):
        for p in personas:
            bl = Bootloader(persona=p)
            _ = bl.is_enabled("comparison_mode_enabled")
    end_time = time.perf_counter()
    baseline_avg = (end_time - start_time) / (iterations * len(personas))

    # 2. Optimized: set_persona (New behavior with Caching)
    bl = Bootloader()
    # Pre-warm cache
    for p in personas:
        bl.set_persona(p)

    start_time = time.perf_counter()
    for _ in range(iterations):
        for p in personas:
            bl.set_persona(p)
            _ = bl.is_enabled("comparison_mode_enabled")
    end_time = time.perf_counter()
    optimized_avg = (end_time - start_time) / (iterations * len(personas))

    reduction = (1 - (optimized_avg / baseline_avg)) * \
        100 if baseline_avg > 0 else 0

    print(f"📊 Baseline Avg:  {baseline_avg*1000:.4f} ms")
    print(f"📊 Optimized Avg: {optimized_avg*1000:.4f} ms")
    print(f"📈 Latency Reduction: {reduction:.2f}%")

    return baseline_avg, optimized_avg, reduction


if __name__ == "__main__":
    b, o, r = benchmark_persona_switch(50)

    report_path = project_root / "tmp/ui_perf_audit.txt"
    os.makedirs(report_path.parent, exist_ok=True)
    with open(report_path, "w") as f:
        f.write("UI Performance Benchmark Report\n")
        f.write(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Baseline Avg:  {b*1000:.4f} ms\n")
        f.write(f"Optimized Avg: {o*1000:.4f} ms\n")
        f.write(f"Reduction:     {r:.2f}%\n")

    print(f"✅ Benchmark report saved to {report_path}")
