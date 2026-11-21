"""Silver layer: clean, dedupe, and join Favorita bronze tables into one fact.

Run: python -m freshflow.silver.clean

TODO(ritik) — implement, one step at a time, asking Claude to explain each:
  1. Read bronze train, items, stores, oil, holidays_events (spark.read.format("delta")).
  2. Cast types; fill null `onpromotion` with False.
  3. [done: dedupe_train] Dedupe train on date+store+item.
  4. Broadcast-join the small dims (items, stores) onto train; left-join oil, holidays.
  5. Apply quality flags (quality.py); write quality_report to docs/ or data/.
  6. Write the conformed fact to data/silver as Delta.
"""

from __future__ import annotations

from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from freshflow.silver.quality import flag_duplicate_ids, quality_report

# One row per store-item-day. A repeat here double-counts a sale, whatever its id.
BUSINESS_KEY = ("date", "store_nbr", "item_nbr")


def dedupe_train(train: DataFrame) -> tuple[DataFrame, int]:
    """Keep one row per BUSINESS_KEY; return (deduped, number of rows dropped).

    The count is taken before filtering so the data-quality report still sees it.
    """
    flagged = flag_duplicate_ids(train, BUSINESS_KEY)
    # ponytail: the count and the later write each run the window shuffle;
    # .cache() `flagged` if that shows up as slow in the Spark UI.
    n_dupes = quality_report(flagged, ["dup_row"])["dup_row"]
    return flagged.filter(~F.col("dup_row")).drop("dup_row"), n_dupes


def main() -> None:
    raise NotImplementedError("Build silver/clean.py following the TODO steps.")


if __name__ == "__main__":
    main()
