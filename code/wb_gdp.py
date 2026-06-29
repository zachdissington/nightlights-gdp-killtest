"""
World Bank WDI - real GDP per country-year, the "official self-reported record" side of the nightlights test.

Verified live 2026-06-28: api.worldbank.org returns 200 here (no cert issue). Indicator NY.GDP.MKTP.KD =
GDP in constant 2015 US$ (real GDP - the right series to regress against log sum-of-lights).
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import requests

BASE = "https://api.worldbank.org/v2"
CACHE = Path(__file__).resolve().parents[2] / ".data" / "nightlights"


def _get(url: str, params: dict) -> list:
    params = {**params, "format": "json", "per_page": 20000}
    r = requests.get(url, params=params, timeout=60)
    r.raise_for_status()
    body = r.json()
    if not isinstance(body, list) or len(body) < 2 or body[1] is None:
        return []
    return body[1]


def real_countries() -> set[str]:
    """ISO3 codes for actual countries (drop WB regional/income aggregates)."""
    rows = _get(f"{BASE}/country", {})
    return {
        r["id"] for r in rows
        if r.get("region", {}).get("value") not in (None, "Aggregates")
    }


def fetch_gdp(start: int = 2012, end: int = 2024, cache: bool = True) -> pd.DataFrame:
    """Country-year real GDP (constant 2015 US$). Returns columns [iso3, year, gdp]."""
    CACHE.mkdir(parents=True, exist_ok=True)
    cache_path = CACHE / f"wb_gdp_{start}_{end}.csv"
    if cache and cache_path.exists():
        return pd.read_csv(cache_path)

    rows = _get(f"{BASE}/country/all/indicator/NY.GDP.MKTP.KD", {"date": f"{start}:{end}"})
    countries = real_countries()
    recs = [
        {"iso3": r["countryiso3code"], "year": int(r["date"]), "gdp": r["value"]}
        for r in rows
        if r.get("value") is not None and r.get("countryiso3code") in countries
    ]
    df = pd.DataFrame(recs).dropna().sort_values(["iso3", "year"]).reset_index(drop=True)
    if cache:
        df.to_csv(cache_path, index=False)
    return df


if __name__ == "__main__":
    df = fetch_gdp()
    print(f"GDP rows: {len(df)} | countries: {df['iso3'].nunique()} | years: {df['year'].min()}-{df['year'].max()}")
    print(df.head())
