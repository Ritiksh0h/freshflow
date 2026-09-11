"""Bronze layer: land raw Favorita CSVs into Delta, unchanged, with load metadata.

Run: python -m freshflow.bronze.ingest
"""

from __future__ import annotations

from pathlib import Path

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F

from freshflow.config import load_config
from freshflow.spark_session import get_spark

# Favorita files to land as-is. Add/remove as needed.
_TABLES = ("train", "items", "stores", "transactions", "oil", "holidays_events")


def _add_load_metadata(df: DataFrame, source_file: str) -> DataFrame:
    """Attach lineage columns so bronze is auditable and replayable."""
    return df.withColumn("_source_file", F.lit(source_file)).withColumn(
        "_ingested_at", F.current_timestamp()
    )


def ingest_table(spark: SparkSession, name: str, raw_dir: Path, bronze_dir: Path) -> None:
    """Read one raw CSV and write it to a bronze Delta table (overwrite)."""
    src = raw_dir / f"{name}.csv"
    df = spark.read.csv(str(src), header=True, inferSchema=True)
    df = _add_load_metadata(df, src.name)
    df.write.format("delta").mode("overwrite").save(str(bronze_dir / name))
    print(f"bronze/{name}: {df.count():,} rows")


def main() -> None:
    cfg = load_config()
    raw_dir = Path(cfg["paths"]["raw"])
    bronze_dir = Path(cfg["paths"]["bronze"])
    spark = get_spark("freshflow-bronze")
    for name in _TABLES:
        ingest_table(spark, name, raw_dir, bronze_dir)


if __name__ == "__main__":
    main()
