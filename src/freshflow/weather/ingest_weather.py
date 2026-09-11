"""OPTIONAL bronze source: Open-Meteo historical weather per store city (free, no key).

Frame this as a *multi-source ingestion* skill demo: external API -> bronze Delta ->
time-aligned join in silver. Do NOT over-claim it improves the forecast unless measured.

API (archive): https://archive-api.open-meteo.com/v1/archive
  params: latitude, longitude, start_date, end_date, daily=temperature_2m_mean,precipitation_sum

TODO(ritik):
  1. Map store cities -> lat/long (small static dict is fine — ponytail rung 6).
  2. Pull daily weather per city for the sales date range; parse JSON.
  3. Write to data/bronze/weather as Delta; join to silver on (date, city).
"""

from __future__ import annotations


def main() -> None:
    raise NotImplementedError("Optional milestone — see TODO steps.")


if __name__ == "__main__":
    main()
