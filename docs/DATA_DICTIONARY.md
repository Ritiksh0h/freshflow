# FreshFlow — Data Dictionary

## Source tables (Corporación Favorita)
### train.csv  (~125.5M rows, ~4.7GB)
| column | type | notes |
|--------|------|-------|
| id | long | row id |
| date | date | daily |
| store_nbr | int | FK → stores |
| item_nbr | int | FK → items |
| unit_sales | double | can be negative (returns) |
| onpromotion | bool | nullable |

### items.csv
| item_nbr | int | PK |
| family | string | product family |
| class | int | product class |
| **perishable** | int (0/1) | ~24% perishable; drives waste-risk |

### stores.csv
| store_nbr | int | PK | | city | string | → weather join |
| state | string | | type | string | | cluster | int | store grouping |

### transactions.csv
| date | date | | store_nbr | int | | transactions | int | daily txn count |

### oil.csv
| date | date | | dcoilwtico | double | daily oil price (Ecuador econ signal), nullable |

### holidays_events.csv
| date | date | | type | string | | locale | string | | locale_name | string |
| description | string | | transferred | bool | |

## Derived (gold) fields
| field | how |
|-------|-----|
| avg_daily_demand_28 | 28-day rolling mean of unit_sales |
| demand_std_28 | 28-day rolling stddev |
| dow, week_of_year, month | from `date` |
| is_weekend | dow in (Sat, Sun) |
| is_holiday | join to holidays_events |
| is_payday | day == 15 or last day of month |
| is_seasonal_sku | monthly demand CV above threshold |
| safety_stock, reorder_point, days_of_supply | see ARCHITECTURE formulas |
| waste_risk_high | perishable AND days_of_supply > threshold |

## Data-quality flags (silver)
`neg_unit_sales` · `dup_row` (same id / same date+store+item) · `orphan_store` ·
`orphan_item` · `impossible_value`. Counts go in the data-quality report.

## Weather (optional bronze, Open-Meteo archive API)
| date | date | | city | string | | temp_mean_c | double | | precip_mm | double |
