# FreshFlow — Architecture

## Medallion data flow
```
              Kaggle CSVs                         Open-Meteo (optional)
                  │                                       │
                  ▼                                       ▼
 ┌───────────────────────────────┐         ┌───────────────────────────┐
 │            BRONZE             │         │      BRONZE (weather)      │
 │  raw Delta tables, as-is,     │         │  daily weather per city,   │
 │  + load metadata (src, ts)    │         │  as-is                     │
 └───────────────┬───────────────┘         └──────────────┬────────────┘
                 │                                         │
                 ▼                                         │
 ┌───────────────────────────────┐                        │
 │            SILVER             │◄───────────────────────┘  (time-aligned join)
 │  typed, deduped, joined dims  │
 │  (items, stores, oil, hols)   │
 │  + DATA-QUALITY checks/flags  │
 └───────────────┬───────────────┘
                 │
                 ▼
 ┌───────────────────────────────┐
 │             GOLD              │
 │  rolling demand (7/28d),      │
 │  seasonality + seasonal flag, │
 │  reorder point, safety stock, │
 │  days-of-supply, WASTE-RISK   │
 │  partitioned by store_nbr     │
 └───────────────┬───────────────┘
                 │
                 ▼
        Streamlit dashboard + data-quality report
```

## Layer responsibilities
- **Bronze** — immutable landing zone. No transforms; replayable. Adds `_source_file`,
  `_ingested_at`.
- **Silver** — one conformed, analytics-ready fact joined to dimensions. This is where
  data-quality checks run and write a report + boolean flags (flags double as an
  admin-error/shrink signal).
- **Gold** — business aggregates and decision signals, partitioned by `store_nbr` for
  query speed.

## Key formulas
- `avg_daily_demand` = rolling mean of `unit_sales` (28-day window).
- `demand_std` = rolling stddev of daily `unit_sales`.
- `safety_stock` = z × demand_std × √(lead_time_days)   (z = 1.645 for 95%).
- `reorder_point` = avg_daily_demand × lead_time_days + safety_stock.
- `days_of_supply` = current_on_hand_proxy / avg_daily_demand.
- `waste_risk_high` = `perishable` AND `days_of_supply` > threshold.

## Spark techniques demonstrated
DataFrame API + Spark SQL · window functions (rolling mean/std, `lag`, `row_number` for
dedup) · multi-table joins (broadcast the small dims) · `partitionBy` on write · schema
enforcement · optional MLlib (FP-Growth) or XGBoost baseline.
