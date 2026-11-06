"""Every plot of the shipped test manifests must render (issue #13).

Found on 2026-11-05: `amr_heatmap` mapped `fill` to a column that does not exist, and nothing
caught it until someone opened the tab. This test builds the dataset of every plot and renders it,
so a mapping to a missing column fails here.

Run: PYTHONPATH=. ./.venv/bin/python -m pytest app/tests/test_render_every_plot.py -q
"""
from pathlib import Path

import matplotlib
import pytest

matplotlib.use("Agg")

from app.modules.cache_keys import clear_manifest_cache
from app.modules.orchestrator import DataOrchestrator
from utils.config_loader import ConfigManager
from viz_factory.viz_factory import VizFactory

ROOT = Path(__file__).resolve().parents[2]
MANIFESTS_DIR = ROOT / "config" / "manifests" / "pipelines"
# figshare_integration is the large one (about 200000 rows); it builds in under a second.
PROJECTS = ["1_test_data_ST22_dummy", "2_test_data_ST22_dummy", "figshare_integration"]


def _plots():
    for project in PROJECTS:
        raw = ConfigManager(str(MANIFESTS_DIR / f"{project}.yaml")).raw_config
        for group in raw.get("analysis_groups", {}).values():
            for plot_id, entry in group.get("plots", {}).items():
                yield pytest.param(project, plot_id, entry["spec"]["target_dataset"], id=f"{project}-{plot_id}")


@pytest.fixture(scope="module")
def anchors(tmp_path_factory):
    return tmp_path_factory.mktemp("anchors")


@pytest.mark.parametrize("project,plot_id,target", list(_plots()))
def test_plot_renders(anchors, project, plot_id, target):
    clear_manifest_cache()
    raw = ConfigManager(str(MANIFESTS_DIR / f"{project}.yaml")).raw_config
    orchestrator = DataOrchestrator(MANIFESTS_DIR, ROOT / "assets" / "test_data")
    # The data HOME and the export show: the stored Tier 2 (equal to Tier 1 without tier2 steps).
    # Read twice: the first call writes the file, the second reads it back, so a stored file that
    # cannot be read again fails here (found by the export download test, 2026-11-06).
    keys = orchestrator.compute_project_keys(project)
    tier1_path = anchors / f"{project}_{target}.parquet"
    orchestrator.materialize_tier2(project, target, tier1_path, keys=keys).collect()
    lf = orchestrator.materialize_tier2(project, target, tier1_path, keys=keys)
    assert lf.head(1).collect().height == 1, f"{target} has no rows"
    plot = VizFactory().render(lf, raw, plot_id)
    plot.draw()
