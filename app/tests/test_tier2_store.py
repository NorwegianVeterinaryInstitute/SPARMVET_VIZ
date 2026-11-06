"""Tier 2 is stored as a parquet with a chained key (ADR-089 point 6, fork issue evezeyl/SPARMVET_VIZ#10).

Same tiny project as test_cache_chain.py. Rewrite detection: after the first build both parquet
files get an old modification time; a rewrite shows as a different one.

Run: PYTHONPATH=. ./.venv/bin/python -m pytest app/tests/test_tier2_store.py -q
"""
import os

import pytest

from app.modules.cache_keys import clear_manifest_cache, tier2_key
from app.modules.orchestrator import TIER2_KEY_META, tier2_path_for
from app.tests.test_cache_chain import FILTER_A, FILTER_B, OLD_MTIME_NS, World
from utils.hashing import get_parquet_metadata_hash


class Tier2World(World):
    def __init__(self, root):
        super().__init__(root)
        self.t2 = tier2_path_for(self.anchor)

    def read_t2(self):
        """One session reads T2: keys first, then the stored file. Returns the rows."""
        keys = self.orch.compute_project_keys("tiny")
        lf = self.orch.materialize_tier2("tiny", "C", self.anchor, keys=keys)
        return sorted(lf.collect().to_dicts(), key=lambda r: r["sample_id"])

    def pin_both(self):
        for p in (self.anchor, self.t2):
            if p.exists():
                os.utime(p, ns=(OLD_MTIME_NS, OLD_MTIME_NS))

    @staticmethod
    def rewritten(path):
        return os.stat(path).st_mtime_ns != OLD_MTIME_NS


@pytest.fixture(autouse=True)
def _fresh_cache():
    clear_manifest_cache()
    yield
    clear_manifest_cache()


@pytest.fixture
def world(tmp_path):
    """A project whose join has one tier2 step (keep group A), already built once."""
    w = Tier2World(tmp_path)
    w.write_manifest(recipe_tier2=[FILTER_A])
    rows = w.read_t2()
    assert [r["sample_id"] for r in rows] == ["s1", "s2"]
    w.pin_both()
    return w


def test_tier2_is_written_next_to_tier1_with_its_chained_key(world):
    keys = world.orch.compute_project_keys("tiny")
    assert world.t2.name == "C__T2.parquet" and world.t2.parent == world.anchor.parent
    assert get_parquet_metadata_hash(str(world.t2), TIER2_KEY_META) == tier2_key(keys.tier1_key, [FILTER_A])


def test_nothing_changed_reads_the_stored_file(world):
    rows = world.read_t2()
    assert [r["sample_id"] for r in rows] == ["s1", "s2"]
    assert not world.rewritten(world.t2) and not world.rewritten(world.anchor)


def test_tier2_step_change_recomputes_only_tier2(world):
    world.write_manifest(recipe_tier2=[FILTER_B])
    rows = world.read_t2()
    assert [r["sample_id"] for r in rows] == ["s3"]
    assert world.rewritten(world.t2)
    assert not world.rewritten(world.anchor), "a Tier 2 step must not rewrite the Tier 1 file"


def test_tier1_change_recomputes_both(world):
    world.write_data("sample_id\tgroup\ns1\tA\ns2\tA\ns3\tB\ns4\tA\n")
    rows = world.read_t2()
    assert [r["sample_id"] for r in rows] == ["s1", "s2", "s4"]
    assert world.rewritten(world.anchor) and world.rewritten(world.t2)


def test_missing_tier2_file_is_recomputed_from_tier1(world):
    world.t2.unlink()
    rows = world.read_t2()
    assert [r["sample_id"] for r in rows] == ["s1", "s2"]
    assert world.t2.exists() and not world.rewritten(world.anchor)


def test_empty_tier2_writes_no_file_and_equals_tier1(tmp_path):
    w = Tier2World(tmp_path)
    w.write_manifest(recipe_tier2=[])
    assert len(w.read_t2()) == 3
    assert not w.t2.exists()


def test_a_stale_tier2_file_is_removed_when_the_steps_are_dropped(world):
    world.write_manifest(recipe_tier2=[])
    assert len(world.read_t2()) == 3
    assert not world.t2.exists()
