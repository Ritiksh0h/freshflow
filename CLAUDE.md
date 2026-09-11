# CLAUDE.md — FreshFlow project context

> Paste this file's contents into your **claude.ai Project → Custom Instructions**,
> and keep it at the repo root so **Claude Code** reads it automatically.

## What we're building
**FreshFlow** is a PySpark + Delta Lake **medallion (bronze → silver → gold)** batch
pipeline that turns raw grocery sales into store-SKU **replenishment and perishable
waste-risk** signals. It is a learning/portfolio project targeting junior **data
engineering** roles (SOCAN, Flight Centre).

Problem it solves: grocery retailers lose billions to over-ordering and perishable
spoilage, and part of "shrink" is actually bad data (negative stock, duplicates,
impossible values). FreshFlow computes demand signals, reorder points, safety stock,
and a waste-risk score per store-SKU, and flags data-quality anomalies along the way.

## Tech stack
Python 3.11 · PySpark · Delta Lake (open-source) · Parquet · pytest · ruff · black ·
mypy · Streamlit (dashboard) · Docker. Dataset: **Corporación Favorita** (Kaggle).
Optional second source: **Open-Meteo** historical weather (free, no key).

## Repo layout
- `src/freshflow/bronze|silver|gold/` — one module per medallion layer
- `src/freshflow/weather/` — optional external-source ingestion
- `config/config.yaml` — paths + business params (lead time, service level, windows)
- `docs/` — spec, architecture, data dictionary, build plan (READ THESE FIRST)
- `tests/` — pytest
- `data/` — raw/bronze/silver/gold (git-ignored)

## How I (Ritik) want to work with you in this project
1. **Explain before you generate.** I'm learning PySpark and RAG. For every non-trivial
   piece, tell me *why* (what a shuffle is, why we partition on store_nbr, why this
   window function) before/after the code. I must be able to defend every line in an
   interview.
2. **Build incrementally, one layer at a time.** Bronze first, then silver, then gold.
   Don't dump the whole pipeline at once.
3. **No over-engineering (the ponytail rule).** Before writing code, walk this ladder
   and stop at the first rung that holds:
   1. Does this need to exist? → no: skip it (YAGNI)
   2. Already in this codebase? → reuse it
   3. Does the stdlib / PySpark built-in do it? → use it
   4. Native platform feature? → use it
   5. Installed dependency does it? → use it
   6. One line? → one line
   7. Only then: the minimum that works
   **Lazy about the solution, never about correctness.** Never cut data-quality checks,
   schema enforcement, error handling, or clear naming.
4. **Small, typed, documented functions.** Type hints on everything, short docstrings,
   functions that do one thing. Code must pass `make lint typecheck test`.
5. **Ask me for the real numbers.** Don't invent metrics or fake results in the README.

## Business parameters (see config/config.yaml)
- Lead time: default 7 days · Service level: 95% (z = 1.645) · Rolling windows: 7 & 28 days
- Perishable items come from `items.perishable` (~24% of items).
- Seasonality features (month, week-of-year, day-of-week, is-holiday, is-payday) are in
  the gold layer **from day one**. Payday in Ecuador = 15th and month-end.
- Weather is an **optional** bronze source added as a separate "multi-source ingestion"
  milestone — framed as a data-engineering skill demo (external API + time-aligned join),
  not a forecasting silver bullet.

## Definition of done
`make lint typecheck test` is green · bronze/silver/gold Delta tables build end-to-end ·
data-quality report generates · Streamlit dashboard shows waste-risk + reorder alerts for
at least one store cluster · README has an architecture diagram and honest results.
