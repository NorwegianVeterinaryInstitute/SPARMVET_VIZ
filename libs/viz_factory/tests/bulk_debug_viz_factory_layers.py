#!/usr/bin/env python3
"""
bulk_debug_viz_factory_layers.py
---------------------------------
Bulk Viz Factory Test Runner (Artist Pillar Debug Tool).

Usage:
    # Run all registered components across all layers:
    ./.venv/bin/python libs/viz_factory/tests/bulk_debug_viz_factory_layers.py

    # Run only the 'scales' layer:
    ./.venv/bin/python libs/viz_factory/tests/bulk_debug_viz_factory_layers.py --layer scales

    # Specify a custom output directory:
    ./.venv/bin/python libs/viz_factory/tests/bulk_debug_viz_factory_layers.py --output /tmp/viz_out

For single-component tests, use the sibling test_runner.py:
    ./.venv/bin/python libs/viz_factory/tests/test_runner.py libs/viz_factory/tests/test_data/geom_point_test.yaml
"""
from viz_factory import VizFactory
import polars as pl
import os
import sys
import argparse
import yaml
import re
import traceback

import matplotlib
matplotlib.use('Agg')

# Ensure the package is importable from the project root
sys.path.insert(0, os.path.abspath('libs'))

TEST_DATA_DIR = 'libs/viz_factory/tests/test_data'


def get_all_manifests(layer_filter: str = None):
    """Return sorted list of (component_name, manifest_path) for all test manifests."""
    results = []
    for fname in sorted(os.listdir(TEST_DATA_DIR)):
        if not fname.endswith('_test.yaml'):
            continue
        comp_name = fname.replace('_test.yaml', '')
        # Infer layer from prefix
        layer = comp_name.split('_')[0] + 's'
        if layer == 'stats':
            layer = 'stats'  # normalize (stat_ -> stats)
        if layer == 'geoms':
            layer = 'geoms'
        if layer_filter and layer != layer_filter:
            continue
        results.append((comp_name, layer, os.path.join(TEST_DATA_DIR, fname)))
    return results


def run_component(comp_name, layer, manifest_path, output_dir):
    """Run a single component test. Returns (status, message)."""
    try:
        with open(manifest_path, 'r') as f:
            manifest = yaml.safe_load(f)

        data_rel = manifest.get('data_path')
        if not data_rel:
            return ('FAIL', 'No data_path in manifest')

        data_path = os.path.abspath(os.path.join(
            os.path.dirname(manifest_path), data_rel))
        if not os.path.exists(data_path):
            return ('FAIL', f'Data file missing: {data_path}')

        df = pl.scan_csv(data_path, separator='\t', try_parse_dates=True)

        plots = manifest.get('plots', {})
        if not plots:
            return ('FAIL', 'No plots in manifest')
        plot_id = list(plots.keys())[0]

        factory = VizFactory()
        p = factory.render(df, manifest, plot_id)

        out_dir = os.path.join(output_dir, layer)
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, f'{comp_name}.png')
        p.save(out_path, width=8, height=6, dpi=100)

        return ('PASS', out_path)
    except Exception as e:
        return ('FAIL', str(e))


def print_table(results):
    """Print a formatted PASS/FAIL table to console."""
    # Header
    col1, col2, col3 = 40, 8, 50
    separator = '+' + '-' * (col1 + 2) + '+' + '-' * \
        (col2 + 2) + '+' + '-' * (col3 + 2) + '+'
    print(separator)
    print(f"| {'Component':<{col1}} | {'Status':<{col2}} | {'Detail':<{col3}} |")
    print(separator)
    passes = 0
    fails = 0
    for comp_name, layer, status, detail in results:
        mark = '✅' if status == 'PASS' else '❌'
        # Truncate detail if too long
        detail_str = (detail[:col3 - 3] +
                      '...') if len(detail) > col3 else detail
        print(
            f"| {comp_name:<{col1}} | {mark} {status:<{col2-2}} | {detail_str:<{col3}} |")
        if status == 'PASS':
            passes += 1
        else:
            fails += 1
    print(separator)
    print(
        f"\n  Results: {passes} PASS  |  {fails} FAIL  |  {passes + fails} total\n")


def main():
    parser = argparse.ArgumentParser(
        description='Bulk Viz Factory Layer Test Runner',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        '--layer', type=str, default=None,
        help='Optional: filter to a single layer prefix (e.g. scales, themes, geoms, coords, positions, guides, stats, facets, elements)'
    )
    parser.add_argument(
        '--output', type=str, default='tmp',
        help='Output directory for rendered PNGs (default: tmp/)'
    )
    args = parser.parse_args()

    manifests = get_all_manifests(args.layer)
    if not manifests:
        print(f"No manifests found for layer filter: '{args.layer}'")
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"  Viz Factory Bulk Test Runner")
    if args.layer:
        print(f"  Layer filter: {args.layer}")
    print(f"  Output dir:   {args.output}/")
    print(f"  Manifests:    {len(manifests)} found")
    print(f"{'='*60}\n")

    results = []
    for comp_name, layer, manifest_path in manifests:
        status, detail = run_component(
            comp_name, layer, manifest_path, args.output)
        results.append((comp_name, layer, status, detail))
        # Live feedback
        mark = '✅' if status == 'PASS' else '❌'
        print(f"  {mark} {comp_name}")

    print()
    print_table(results)


if __name__ == '__main__':
    main()
