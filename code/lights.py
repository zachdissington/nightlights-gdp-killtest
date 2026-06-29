"""
Country-year VIIRS sum-of-lights - the independent measurement side of the nightlights test.

Source: Earth Observation Atlas (eoatlas/nightlight, CC BY 4.0) - VIIRS monthly nighttime-lights zonal
stats pre-computed per admin unit from World Bank "Light Every Night". One CSV per country (ADM0) at
  https://eoatlas-nightlight.s3.amazonaws.com/eoatlas-monthly-nightlight-{index:05d}.csv   (index 0..197)
Schema: year,month,shapeName,shapeType,shapeGroup(ISO3),...,sum,...  (sum = monthly sum-of-lights).
We download all country ADM0 series and aggregate monthly -> annual sum, complete years only.

Caveat (load-bearing): these LEN monthly composites are NOT gas-flare-removed -> flaring inflates some
countries. That's exactly why nightlights_test.py runs the flaring-country drop robustness check.

Attribution required by CC BY 4.0: Najjar, A. (2024), Earth Observation Atlas, https://eoatlas.org.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import requests

S3 = "https://eoatlas-nightlight.s3.amazonaws.com/eoatlas-monthly-nightlight-{:05d}.csv"
N_COUNTRIES = 198  # ADM0 indices 0..197 (per data/ACCESS_DATA.md)
CACHE = Path(__file__).resolve().parents[2] / ".data" / "nightlights"


def fetch_lights(cache: bool = True) -> pd.DataFrame:
    """Country-year sum-of-lights. Returns [iso3, year, sol] (complete-year annual sum)."""
    CACHE.mkdir(parents=True, exist_ok=True)
    cache_path = CACHE / "eoatlas_sol_annual.csv"
    if cache and cache_path.exists():
        return pd.read_csv(cache_path)

    frames, missed = [], []
    sess = requests.Session()
    for i in range(N_COUNTRIES):
        try:
            r = sess.get(S3.format(i), timeout=60)
            if r.status_code != 200:
                missed.append(i)
                continue
            from io import StringIO
            df = pd.read_csv(StringIO(r.text))
            frames.append(df[df["shapeType"] == "ADM0"][["year", "month", "shapeGroup", "sum"]])
        except Exception:  # noqa: BLE001
            missed.append(i)
    if missed:
        print(f"  (skipped {len(missed)} indices with no/failed CSV: {missed[:10]}{'...' if len(missed) > 10 else ''})")

    monthly = pd.concat(frames, ignore_index=True).rename(columns={"shapeGroup": "iso3"})
    monthly = monthly.dropna(subset=["sum"])

    # keep only complete years (12 monthly obs) so annual sums are comparable
    counts = monthly.groupby(["iso3", "year"])["month"].nunique().rename("nmonth")
    annual = monthly.groupby(["iso3", "year"])["sum"].sum().rename("sol").reset_index()
    annual = annual.merge(counts, on=["iso3", "year"])
    annual = annual[annual["nmonth"] == 12].drop(columns="nmonth").reset_index(drop=True)

    if cache:
        annual.to_csv(cache_path, index=False)
    return annual


if __name__ == "__main__":
    df = fetch_lights()
    print(f"SoL rows: {len(df)} | countries: {df['iso3'].nunique()} | years: {df['year'].min()}-{df['year'].max()}")
    print(df.head())
