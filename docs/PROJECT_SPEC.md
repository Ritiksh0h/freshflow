# FreshFlow — Project Spec

## Goal
Turn raw grocery sales into store-SKU **replenishment** and **perishable waste-risk**
signals, with data-quality checks that also surface administrative-error shrink.

## Why it matters (context, cite in README/interview)
- Retail **shrink** ≈ $112.1B / 1.6% of sales (NRF 2023); ~27% of shrink is process/
  admin error — the slice a pipeline can catch.
- **Food waste**: USDA estimates 30–40% of the food supply; supermarkets alone throw
  out ~43B lbs/yr (~$50B in lost profit).
- **Inventory distortion** (over/understock) ≈ $1.73T globally, 6.5% of sales (IHL 2025).
Use these as order-of-magnitude context, not precision — see report caveats.

## Scope (in)
- Medallion pipeline (bronze/silver/gold) in PySpark + Delta.
- Demand features: rolling 7/28-day averages, volatility, seasonality, seasonal-SKU flag.
- Replenishment: reorder point, safety stock, days-of-supply.
- Perishable waste-risk score.
- Data-quality checks (negative sales, duplicates, orphan keys, impossible values).
- Streamlit dashboard + data-quality report.

## Scope (out / later)
- Real Spark cluster (local mode is fine; discuss scaling verbally).
- Heavy time-series / deep-learning forecasting (a moving-average or XGBoost baseline
  is enough — the story is the pipeline, not the model).
- Weather ingestion is an **optional** milestone (see ARCHITECTURE → weather).

## Success criteria
- `make lint typecheck test` green.
- End-to-end bronze→silver→gold builds on the Favorita data.
- Dashboard shows top waste-risk SKUs and reorder alerts for ≥1 store cluster.
- README: architecture diagram + honest results + "why Spark" note.

## Honest framing for interviews
"I built this to learn Spark and lakehouse patterns properly. Local mode isn't a cluster;
here's what I'd change for production (partitioning strategy, broadcast joins, incremental
loads, orchestration). The data-quality layer is the part I'm proudest of."
