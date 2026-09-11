"""Gold: demand + seasonality features per (store_nbr, item_nbr) over time.

TODO(ritik) — implement with Spark window functions:
  - Order a Window by date, partition by (store_nbr, item_nbr).
  - avg_daily_demand_7 / _28  = F.avg("unit_sales").over(window.rowsBetween(-N, 0))
  - demand_std_28             = F.stddev("unit_sales").over(...)
  - Seasonality: F.month, F.weekofyear, F.dayofweek; is_weekend; is_holiday (from join);
    is_payday (day == 15 or last day of month).
  - is_seasonal_sku: coefficient of variation of monthly demand above a threshold.
Explain: why window frames vs groupBy, and how partitioning affects the shuffle.
"""

from __future__ import annotations


def add_demand_features():  # noqa: ANN201  (signature TBD by ritik)
    raise NotImplementedError
