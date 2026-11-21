"""Silver data-quality checks. Each function adds one boolean flag column.

Flags double as an administrative-error shrink signal (negative stock, dupes, etc.).
"""

from __future__ import annotations

from pyspark.sql import DataFrame, Window
from pyspark.sql import functions as F


def flag_negative_sales(df: DataFrame) -> DataFrame:
    """Flag rows where unit_sales < 0 (returns / correction entries)."""
    return df.withColumn("neg_unit_sales", F.col("unit_sales") < 0)


def flag_duplicate_ids(df: DataFrame, keys: tuple[str, ...] = ("id",)) -> DataFrame:
    """Flag duplicate rows by `keys` (keeps all, marks the extras as dup_row).

    Ordering by every non-key column makes the survivor deterministic across reruns:
    copies that differ always sort the same way; fully identical copies don't matter.
    """
    order_cols = [c for c in df.columns if c not in keys]
    w = Window.partitionBy(*keys).orderBy(*order_cols)
    return df.withColumn("dup_row", F.row_number().over(w) > 1)


def _flag_orphan(df: DataFrame, dim: DataFrame, key: str, flag: str) -> DataFrame:
    """Flag rows whose key has no match in the dim (left-join sentinel, keeps all rows)."""
    dim_keys = dim.select(key).distinct().withColumn("_exists", F.lit(True))
    return (
        df.join(F.broadcast(dim_keys), on=key, how="left")
        .withColumn(flag, F.col("_exists").isNull())
        .drop("_exists")
    )


def flag_orphan_store(df: DataFrame, stores: DataFrame) -> DataFrame:
    """Flag rows whose store_nbr is missing from the stores dimension."""
    return _flag_orphan(df, stores, "store_nbr", "orphan_store")


def flag_orphan_item(df: DataFrame, items: DataFrame) -> DataFrame:
    """Flag rows whose item_nbr is missing from the items dimension."""
    return _flag_orphan(df, items, "item_nbr", "orphan_item")


def flag_extreme_unit_sales(df: DataFrame, max_abs: float = 616.0) -> DataFrame:
    """Flag |unit_sales| > max_abs: review cutoff from sample p99.99 (~616), not impossibility."""
    return df.withColumn("extreme_unit_sales", F.abs(F.col("unit_sales")) > max_abs)


def quality_report(df: DataFrame, flag_cols: list[str]) -> dict[str, int]:
    """Return a {flag: count_true} summary for the data-quality report."""
    agg = df.agg(*[F.sum(F.col(c).cast("int")).alias(c) for c in flag_cols]).collect()[0]
    return {c: int(agg[c] or 0) for c in flag_cols}
