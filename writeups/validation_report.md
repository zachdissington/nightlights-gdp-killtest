# Nightlights-GDP cheap test, validation report

> Run 2026-06-28. Product `nightlights-gdp/scoping.md`. Tests whether the Martinez (2022) autocracy
> elasticity gradient, *autocracies report more GDP per unit of light growth* (over-statement),
> reproduces on the **VIIRS era (2012–2023)**, the window a solo could actually ship a live product on.
> Data, all live/free: GDP = World Bank WDI `NY.GDP.MKTP.KD` (real, constant 2015 US$); lights = Earth
> Observation Atlas VIIRS ADM0 sum-of-lights, CC BY 4.0 (Najjar 2024, eoatlas.org); regime = OWID/V-Dem
> Regimes of the World. Panel: ~170 countries × 2012–2023.

Model: `log(realGDP) = b·log(SoL) + g·[log(SoL)×autocracy] + FE + e`, SE clustered by country. The
**gradient g** is the extra GDP-to-lights elasticity in autocracies; Martinez's thesis needs **g > 0**.

| Spec | Gradient g | Dem elasticity b | Reading |
|---|---|---|---|
| **Within-country FE + year FE** (clean causal) | **+0.002** (ns, p=0.30) | 0.197 | No gradient, signal absent |
| Within-FE, drop gas-flaring countries | +0.002 (ns, p=0.21) | 0.149 | Unchanged |
| Cross-sectional (year FE only) | **−0.237** (p=0.003) | 0.944 | Significant but **WRONG SIGN** |
| Cross-sectional, drop flaring | −0.302 (p=0.0006) | 0.921 | Wrong sign, stronger |

## Verdict: **NO-GO** (the over-reporting signal does not reproduce on VIIRS)
- The **clean within-country identification** (which isolates the manipulation signal from structural
  differences) shows **no gradient**, g≈0, insignificant, robust to dropping flaring countries.
- The **cross-sectional** spec is significant but the **opposite sign** to Martinez's thesis (autocracies
  have a *shallower* slope + a high intercept), and it conflates genuine elasticity heterogeneity
  (autocracies are often resource economies) with manipulation, the exact pitfall the kill-test flagged.
- The democracy elasticity is positive and sensible (lights do predict GDP), so the data/merge are sound;
  it's the *autocracy gradient* specifically that is absent.

**Why this is consistent with the predicted risk:** Martinez's headline used **DMSP (1992–2013)**, a long
panel. The VIIRS era is short (12 yrs) and the within-country signal needs regime *switchers* to identify
, there aren't enough, and the long-run over-reporting accumulation isn't visible. The "live, refreshable,
VIIRS-era named-government product" a solo would ship has **no reproducible signal**.

## Caveats / what would (not) revive it
This is one regime measure (RoW), one lights product (LEN monthly, not the cleaner flare-removed VNL
annual-masked), and a standard panel spec, not a Martinez-byte-exact replication (his lags, weighting,
DMSP–VIIRS bridge). A full replication is a possible academic exercise, but it would be re-running a
published JPE result on a bridged series, which is the thin-novelty problem the occupancy kill-test
already flagged. For the cheap-test decision (does the *shippable* VIIRS-era signal exist), it's NO-GO.

**Banked negative**, a clean, reproducible null, in the spirit of the climate project's SF6/HFC-134a
published negatives. The pipeline (`code/`) is reusable if a DMSP-bridge revisit is ever wanted.
