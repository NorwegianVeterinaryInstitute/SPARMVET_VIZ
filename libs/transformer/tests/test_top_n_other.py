"""The top_n_other action: keep the N most frequent values, label the rest (issue #23).

Run: PYTHONPATH=. ./.venv/bin/python -m pytest libs/transformer/tests/test_top_n_other.py -q
"""
import random

import polars as pl
import pytest

from transformer.actions.cleaning.analytical import action_top_n_other
from utils.errors import TransformationError


def run(values, spec, **extra):
    frame = pl.DataFrame({"v": values, **extra}).lazy()
    return action_top_n_other(frame, {"column": "v", **spec}).collect()


def test_keeps_the_n_most_frequent_and_labels_the_rest():
    out = run(["a", "a", "a", "b", "b", "c", "d"], {"n": 2})
    assert out.columns == ["v", "v_top2"]
    assert out["v_top2"].to_list() == ["a", "a", "a", "b", "b", "Other", "Other"]


def test_ties_are_broken_alphabetically():
    # b, c and d each occur twice: the first two alphabetically (b, c) are kept
    out = run(["d", "d", "c", "c", "b", "b", "a"], {"n": 2})
    assert out["v_top2"].to_list() == ["Other", "Other", "c", "c", "b", "b", "Other"]


def test_the_same_data_gives_the_same_result_whatever_the_row_order():
    rng = random.Random(3)
    values = [rng.choice("abcdefgh") for _ in range(500)]
    shuffled = values[:]
    rng.shuffle(shuffled)
    kept = lambda vs: sorted(set(run(vs, {"n": 3})["v_top3"].to_list()) - {"Other"})
    assert kept(values) == kept(shuffled)


def test_rows_keep_their_order_and_nothing_is_lost():
    values = ["x", "y", "x", "z", "y", "x"]
    out = run(values, {"n": 1}, row_id=list(range(6)))
    assert out["row_id"].to_list() == list(range(6))
    assert out["v"].to_list() == values


def test_nulls_stay_null_and_take_no_place_in_the_top():
    out = run(["a", None, None, None, "b", "b"], {"n": 1})
    assert out["v_top1"].to_list() == ["Other", None, None, None, "b", "b"]


def test_a_custom_label_and_overwriting_the_same_column():
    out = run(["a", "a", "b", "c"], {"n": 1, "other_label": "Rest", "new_column": "v"})
    assert out.columns == ["v"]
    assert out["v"].to_list() == ["a", "a", "Rest", "Rest"]


def test_count_distinct_ranks_by_different_samples_not_rows():
    # "a" has 4 rows but 1 sample; "b" and "c" have 2 samples each
    out = run(["a", "a", "a", "a", "b", "b", "c", "c"], {"n": 2, "count_distinct": "s"},
              s=["s1", "s1", "s1", "s1", "s2", "s3", "s4", "s5"])
    assert out["v_top2"].to_list() == ["Other"] * 4 + ["b", "b", "c", "c"]


def test_works_on_a_categorical_column():
    frame = pl.DataFrame({"v": ["a", "a", "b", "c"]}).with_columns(pl.col("v").cast(pl.Categorical)).lazy()
    out = action_top_n_other(frame, {"column": "v", "n": 1}).collect()
    assert out["v_top1"].to_list() == ["a", "a", "Other", "Other"]


@pytest.mark.parametrize("spec", [{"n": 2}, {"column": "v"}, {"column": "v", "n": 0}, {"column": "v", "n": "3"}])
def test_bad_parameters_are_reported(spec):
    with pytest.raises(TransformationError):
        action_top_n_other(pl.DataFrame({"v": ["a"]}).lazy(), spec)
