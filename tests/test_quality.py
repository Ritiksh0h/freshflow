"""Example pytest for the silver data-quality checks.

Shows the pattern: build a tiny DataFrame, run a flag function, assert the result.
Spark in tests is slow to start but this proves the logic works.
"""

from __future__ import annotations

import os
import sys

import pytest
from pyspark.sql import SparkSession

# Spark workers must run the same Python as the driver (the venv's), not the system one.
os.environ.setdefault("PYSPARK_PYTHON", sys.executable)

from freshflow.silver.quality import (
    flag_extreme_unit_sales,
    flag_negative_sales,
    flag_orphan_item,
    flag_orphan_store,
    quality_report,
)


@pytest.fixture(scope="module")
def spark():
    s = SparkSession.builder.master("local[1]").appName("tests").getOrCreate()
    yield s
    s.stop()


def test_flag_negative_sales(spark: SparkSession) -> None:
    df = spark.createDataFrame([(1, 5.0), (2, -3.0), (3, 0.0)], ["id", "unit_sales"])
    flagged = flag_negative_sales(df)
    report = quality_report(flagged, ["neg_unit_sales"])
    assert report["neg_unit_sales"] == 1


def test_flag_orphan_store(spark: SparkSession) -> None:
    facts = spark.createDataFrame([(1, 1, 5.0), (2, 99, 3.0)], ["id", "store_nbr", "unit_sales"])
    stores = spark.createDataFrame([(1,), (2,)], ["store_nbr"])
    flagged = flag_orphan_store(facts, stores)
    report = quality_report(flagged, ["orphan_store"])
    assert report["orphan_store"] == 1
    assert flagged.count() == facts.count()  # flag-not-drop: no rows lost or fanned out


def test_flag_extreme_unit_sales(spark: SparkSession) -> None:
    # One normal, one big sale, one big RETURN: the negative row proves we bound the
    # magnitude, not the raw value — a raw > check would count only 1 and fail here.
    facts = spark.createDataFrame([(1, 5.0), (2, 700.0), (3, -700.0)], ["id", "unit_sales"])
    flagged = flag_extreme_unit_sales(facts)
    report = quality_report(flagged, ["extreme_unit_sales"])
    assert report["extreme_unit_sales"] == 2
    assert {r["id"] for r in flagged.filter("extreme_unit_sales").collect()} == {2, 3}
    assert flagged.count() == facts.count()  # flag-not-drop: no rows lost or fanned out


def test_flag_orphan_item(spark: SparkSession) -> None:
    # Two valid rows + one orphan: a reversed flag would count 2, so == 1 catches inversion.
    facts = spark.createDataFrame(
        [(1, 100, 5.0), (2, 200, 4.0), (3, 999, 3.0)], ["id", "item_nbr", "unit_sales"]
    )
    items = spark.createDataFrame([(100,), (200,)], ["item_nbr"])
    flagged = flag_orphan_item(facts, items)
    report = quality_report(flagged, ["orphan_item"])
    assert report["orphan_item"] == 1
    assert flagged.count() == facts.count()  # flag-not-drop: no rows lost or fanned out
