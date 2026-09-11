"""Silver layer: clean, dedupe, and join Favorita bronze tables into one fact.

Run: python -m freshflow.silver.clean

TODO(ritik) — implement, one step at a time, asking Claude to explain each:
  1. Read bronze train, items, stores, oil, holidays_events (spark.read.format("delta")).
  2. Cast types; fill null `onpromotion` with False.
  3. Dedupe train via quality.flag_duplicate_ids then filter dup_row == False.
  4. Broadcast-join the small dims (items, stores) onto train; left-join oil, holidays.
  5. Apply quality flags (quality.py); write quality_report to docs/ or data/.
  6. Write the conformed fact to data/silver as Delta.
"""

from __future__ import annotations


def main() -> None:
    raise NotImplementedError("Build silver/clean.py following the TODO steps.")


if __name__ == "__main__":
    main()
