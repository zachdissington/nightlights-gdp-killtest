"""
Nightlights-GDP cheap test - the Martinez (2022) autocracy elasticity-gradient regression, VIIRS era.

Model (country + year fixed effects, SE clustered by country):
    log(realGDP_it) = b*log(SoL_it) + g*[log(SoL_it) x autocracy_it] + a_i + d_t + e_it
The gradient g = how much STEEPER the GDP-to-lights elasticity is in autocracies. Martinez (DMSP,
1992-2013) found g > 0: autocracies report more GDP per unit of light growth (consistent with
over-statement). This re-runs it on the VIIRS era (2012-2023) and checks it survives dropping the
gas-flaring countries (whose VIIRS lights are flare-inflated).

DECISION: GO iff g > 0 and significant on the full sample AND still positive+significant after dropping
flaring countries. Else CONDITIONAL/NO-GO. Writes ../validation_report.md.
"""
from __future__ import annotations

from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

import lights as L
import regime as R
import wb_gdp as G

# World Bank GGFR top gas-flaring countries (firm top 9 + recurring tier-2); their VNL is flare-inflated.
FLARING = ["RUS", "IRN", "IRQ", "VEN", "MEX", "LBY", "DZA", "NGA", "USA",
           "CHN", "OMN", "SAU", "AGO", "KAZ", "IDN", "EGY", "ARE"]
REPORT = Path(__file__).resolve().parents[1] / "validation_report.md"


def build_panel() -> pd.DataFrame:
    gdp = G.fetch_gdp()
    sol = L.fetch_lights()
    reg = R.fetch_regime()
    df = (gdp.merge(sol, on=["iso3", "year"]).merge(reg, on=["iso3", "year"]))
    df = df[(df["gdp"] > 0) & (df["sol"] > 0)].copy()
    df["loggdp"] = np.log(df["gdp"])
    df["logsol"] = np.log(df["sol"])
    return df


def run(df: pd.DataFrame, label: str) -> dict:
    m = smf.ols("loggdp ~ logsol + logsol:autocracy + C(iso3) + C(year)", data=df).fit(
        cov_type="cluster", cov_kwds={"groups": df["iso3"]}
    )
    g = m.params["logsol:autocracy"]
    p = m.pvalues["logsol:autocracy"]
    b = m.params["logsol"]
    return {"label": label, "n": int(m.nobs), "countries": df["iso3"].nunique(),
            "elasticity_dem": b, "gradient": g, "p": p,
            "sig": "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.1 else "ns"}


def main() -> None:
    df = build_panel()
    full = run(df, "Full sample (2012-2023)")
    noflare = run(df[~df["iso3"].isin(FLARING)], "Drop gas-flaring countries")

    go_full = full["gradient"] > 0 and full["p"] < 0.05
    go_noflare = noflare["gradient"] > 0 and noflare["p"] < 0.10
    verdict = "GO" if (go_full and go_noflare) else (
        "CONDITIONAL (gradient flaring-sensitive)" if go_full else "NO-GO (gradient absent in VIIRS era)")

    for r in (full, noflare):
        print(f"{r['label']}: gradient g={r['gradient']:+.3f} (p={r['p']:.3g} {r['sig']}), "
              f"dem elasticity b={r['elasticity_dem']:.3f}, n={r['n']}, {r['countries']} countries")
    print(f"\nVERDICT: {verdict}")
    _write(full, noflare, verdict)


def _write(full, noflare, verdict) -> None:
    def row(r):
        return (f"| {r['label']} | {r['gradient']:+.3f} ({r['sig']}, p={r['p']:.3g}) | "
                f"{r['elasticity_dem']:.3f} | {r['n']} | {r['countries']} |")
    body = f"""# Nightlights-GDP cheap test - validation report

> Run {date.today().isoformat()}. Product `nightlights-gdp/scoping.md`. Martinez (2022) autocracy
> elasticity-gradient regression on the **VIIRS era (2012-2023)**: log(real GDP) ~ log(sum-of-lights) +
> log(SoL)x autocracy + country FE + year FE, SE clustered by country.
> Data (all live/free): GDP = World Bank WDI NY.GDP.MKTP.KD; lights = Earth Observation Atlas VIIRS
> ADM0 sum-of-lights (CC BY 4.0); regime = OWID/V-Dem Regimes of the World.

The **gradient g** = extra GDP-to-lights elasticity in autocracies. Martinez's thesis (on DMSP 1992-2013):
g > 0 → autocracies report more GDP per unit of light growth (over-statement). This tests whether it
holds on VIIRS and survives dropping flare-inflated countries.

| Sample | Gradient g (log SoL x autocracy) | Dem elasticity b | n | countries |
|---|---|---|---|---|
{row(full)}
{row(noflare)}

## Verdict: **{verdict}**
Decision rule: GO iff g > 0 and significant (full sample, p<0.05) AND still positive+significant after
dropping the World Bank GGFR gas-flaring countries (p<0.10). Flaring drop-set: {", ".join(FLARING)}.

_Honesty: novelty here is productization (a live, refreshable, named-government product), not method - the
Martinez result is published. The slot (a free maintained product) is open; this confirms whether the
signal reproduces cleanly on the VIIRS era a solo would actually ship._
"""
    REPORT.write_text(body, encoding="utf-8")


if __name__ == "__main__":
    main()
