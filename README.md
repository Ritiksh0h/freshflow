# FreshFlow 🥬 — Perishable Waste & Replenishment Lakehouse

A **PySpark + Delta Lake** medallion pipeline that turns raw grocery sales into
store-SKU **replenishment** and **perishable waste-risk** signals — with data-quality
checks that also surface administrative-error shrink.

> Learning / portfolio project for junior data-engineering roles. Not a production system.

## Problem
Grocery retailers lose billions to **over-ordering** and **perishable spoilage**, and a
real slice of "shrink" is actually **bad data** (negative stock, duplicates, impossible
values). Store managers lack clean, per-store, per-SKU signals telling them how much to
reorder and which perishables are about to be thrown out.

## Solution
A batch pipeline over the medallion architecture:

| Layer | What it does |
|------|--------------|
| **Bronze** | Ingest raw Favorita CSVs as-is into Delta (append-only, with load metadata). |
| **Silver** | Clean, type-cast, deduplicate, join dimensions; run data-quality checks. |
| **Gold** | Demand features (rolling windows, seasonality, seasonal-SKU flag), reorder point, safety stock, days-of-supply, **perishable waste-risk score**. |

## Tech stack
Python 3.11 · PySpark · Delta Lake · Parquet · pytest · ruff · black · mypy · Streamlit ·
Docker. Data: [Corporación Favorita](https://www.kaggle.com/c/favorita-grocery-sales-forecasting).

## Quickstart
```bash
# 1. Environment
make setup                 # or: pip install -e ".[dev]"

# 2. Data (needs a free Kaggle account + accepted competition rules)
kaggle competitions download -c favorita-grocery-sales-forecasting -p data/raw
unzip 'data/raw/*.zip' -d data/raw

# 3. Run the pipeline
make bronze                # raw CSV -> data/bronze (Delta)
make silver                # clean + join + quality -> data/silver
make gold                  # features + replenishment -> data/gold

# 4. Dashboard
make dashboard             # Streamlit

# Quality gates
make lint typecheck test
```

## Repo structure
```
src/freshflow/  bronze/  silver/  gold/  weather/
config/         config.yaml
docs/           PROJECT_SPEC · ARCHITECTURE · DATA_DICTIONARY · BUILD_PLAN
tests/
```

## Status
🚧 In progress — see `docs/BUILD_PLAN.md`.
