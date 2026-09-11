# FreshFlow — Build Plan (~1–2 weeks)

Build one layer at a time. Commit after each. Ask Claude to explain the Spark concepts.

## Day 1–2 · Setup + Bronze
- [ ] `make setup`; confirm `get_spark()` starts with Delta enabled.
- [ ] Download Favorita to `data/raw`.
- [ ] `bronze/ingest.py`: read each CSV → Delta with `_source_file`, `_ingested_at`.
- [ ] Verify: `SELECT count(*)` on each bronze table.

## Day 3–5 · Silver + Data Quality
- [ ] `silver/clean.py`: cast types, handle null `onpromotion`, dedup, join items/stores/
      oil/holidays.
- [ ] `silver/quality.py`: implement the 5 flag functions; write a data-quality report
      (row counts, % nulls, # flagged per rule).
- [ ] Test: `tests/test_quality.py` green.

## Day 6–9 · Gold
- [ ] `gold/demand_features.py`: 7/28-day rolling mean & std (window over store+item
      ordered by date); seasonality features; `is_seasonal_sku`.
- [ ] `gold/replenishment.py`: safety stock, reorder point, days-of-supply, waste-risk;
      `partitionBy("store_nbr")` on write.

## Day 10–12 · Dashboard + report
- [ ] `dashboard.py` (Streamlit): top waste-risk SKUs by store, reorder alerts, DQ summary.

## Day 13–14 · Polish
- [ ] README architecture diagram + screenshots + honest results.
- [ ] Optional: weather ingestion milestone (`weather/ingest_weather.py`) + silver join.
- [ ] `make lint typecheck test` all green; push to GitHub.

## Optional stretch (only if core is done)
- FP-Growth market-basket on Instacart, or XGBoost demand baseline vs moving average.
- Airflow/Prefect DAG wrapper to show orchestration.
