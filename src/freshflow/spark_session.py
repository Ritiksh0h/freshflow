"""Single place to build a Delta-enabled SparkSession."""

from __future__ import annotations

import os
import sys

from delta import configure_spark_with_delta_pip
from pyspark.sql import SparkSession


def get_spark(app_name: str = "freshflow") -> SparkSession:
    """Return a local SparkSession with Delta Lake enabled."""
    # Workers must run the same Python as the driver (the venv's), not the system 3.13.
    os.environ.setdefault("PYSPARK_PYTHON", sys.executable)
    builder = (
        SparkSession.builder.appName(app_name)
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config(
            "spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        )
    )
    return configure_spark_with_delta_pip(builder).getOrCreate()
