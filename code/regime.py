"""
Regime classification - needed to test the Martinez autocracy elasticity gradient.

Source: Our World in Data "Political regime" (Regimes of the World, based on V-Dem `v2x_regime`),
direct CSV (no V-Dem form): https://ourworldindata.org/grapher/political-regime.csv
Columns: Entity, Code(ISO3), Year, Political regime (0 closed autocracy, 1 electoral autocracy,
2 electoral democracy, 3 liberal democracy). autocracy = regime <= 1.
"""
from __future__ import annotations

from io import StringIO
from pathlib import Path

import pandas as pd
import requests

URL = "https://ourworldindata.org/grapher/political-regime.csv"
CACHE = Path(__file__).resolve().parents[2] / ".data" / "nightlights"


def fetch_regime(cache: bool = True) -> pd.DataFrame:
    """Returns [iso3, year, regime, autocracy]."""
    CACHE.mkdir(parents=True, exist_ok=True)
    cache_path = CACHE / "owid_regime.csv"
    if cache and cache_path.exists():
        return pd.read_csv(cache_path)

    r = requests.get(URL, timeout=60)
    r.raise_for_status()
    df = pd.read_csv(StringIO(r.text))
    col = [c for c in df.columns if "regime" in c.lower()][0]
    df = df.rename(columns={"Code": "iso3", "Year": "year", col: "regime"})
    df = df[df["iso3"].notna() & (df["iso3"].str.len() == 3)][["iso3", "year", "regime"]].dropna()
    df["regime"] = df["regime"].astype(int)
    df["autocracy"] = (df["regime"] <= 1).astype(int)
    df = df.reset_index(drop=True)
    if cache:
        df.to_csv(cache_path, index=False)
    return df


if __name__ == "__main__":
    df = fetch_regime()
    sub = df[df["year"].between(2012, 2023)]
    print(f"regime rows: {len(df)} | 2012-23 countries: {sub['iso3'].nunique()} | "
          f"autocracies (2023): {df[(df.year==2023)]['autocracy'].sum()}")
    print(df.head())
