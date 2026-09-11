"""One-off prep: cut data/raw down to one store cluster so the pipeline runs fast locally.

Filters train.csv and transactions.csv to CLUSTER's stores (streamed in chunks — the
full train.csv is ~4.7GB and must never be loaded into memory at once). Dimension
tables are copied unchanged. Output goes to data/raw_sample; config paths.raw points
there. Run: python sample.py
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pandas as pd

CLUSTER = 8
RAW = Path("data/raw")
OUT = Path("data/raw_sample")
COPY_AS_IS = ("stores.csv", "items.csv", "oil.csv", "holidays_events.csv")
FILTER_BY_STORE = ("transactions.csv", "train.csv")


def main() -> None:
    """Write a cluster-only copy of the raw data to data/raw_sample."""
    OUT.mkdir(parents=True, exist_ok=True)
    stores = pd.read_csv(RAW / "stores.csv")
    keep = set(stores.loc[stores["cluster"] == CLUSTER, "store_nbr"])
    print(f"cluster {CLUSTER}: {len(keep)} stores -> {sorted(keep)}")

    for name in COPY_AS_IS:
        shutil.copy(RAW / name, OUT / name)
        print(f"{name}: copied as-is")

    for name in FILTER_BY_STORE:
        first = True
        kept = 0
        for chunk in pd.read_csv(RAW / name, chunksize=1_000_000):
            part = chunk[chunk["store_nbr"].isin(keep)]
            part.to_csv(OUT / name, mode="w" if first else "a", header=first, index=False)
            first = False
            kept += len(part)
        print(f"{name}: kept {kept:,} rows")


if __name__ == "__main__":
    main()
