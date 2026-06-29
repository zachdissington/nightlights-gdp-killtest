"""Robustness: cross-sectional spec (year FE, no country FE) - Martinez's main identification."""
import sys
from pathlib import Path

import statsmodels.formula.api as smf

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nightlights_test import build_panel, FLARING

df = build_panel()
for lbl, d in [("cross-sectional (year FE only)", df),
               ("cross-sectional, drop flaring", df[~df.iso3.isin(FLARING)])]:
    m = smf.ols("loggdp ~ logsol + logsol:autocracy + autocracy + C(year)", data=d).fit(
        cov_type="cluster", cov_kwds={"groups": d.iso3})
    g = m.params["logsol:autocracy"]
    p = m.pvalues["logsol:autocracy"]
    print(f"{lbl}: gradient={g:+.3f} p={p:.3g} | dem_elasticity={m.params['logsol']:.3f} "
          f"| autocracy_main={m.params['autocracy']:+.2f} | n={int(m.nobs)}")
