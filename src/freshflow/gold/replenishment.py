"""Gold: replenishment + perishable waste-risk signals. Writes final gold Delta.

Run: python -m freshflow.gold.replenishment

Formulas (see docs/ARCHITECTURE.md):
  safety_stock   = z * demand_std_28 * sqrt(lead_time_days)      # z from config
  reorder_point  = avg_daily_demand_28 * lead_time_days + safety_stock
  days_of_supply = on_hand_proxy / avg_daily_demand_28
  waste_risk_high = perishable AND days_of_supply > threshold
Write partitioned by store_nbr:  .write.partitionBy("store_nbr").format("delta")...

TODO(ritik): implement after demand_features.py is done.
"""

from __future__ import annotations


def main() -> None:
    raise NotImplementedError("Build gold/replenishment.py using the config formulas.")


if __name__ == "__main__":
    main()
