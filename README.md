# Nightlights vs Official GDP Kill-Test

An honest **negative result**. Can free satellite night-lights catch governments overstating their own GDP growth, on the satellite era a solo builder could actually ship a live product on?

This is part of a deliberate practice of **publishing failures, not just wins**. The idea was appealing and the data slot was genuinely empty. The test killed it cleanly, and it's published anyway, with the full regression, the numbers, and the reason it failed, because a fast, reproducible "no" is a real research output.

## TL;DR, the result

| | |
|---|---|
| **Idea** | Autocracies overstate GDP growth; night-lights are an independent measure of activity, so a higher lights-to-GDP elasticity in autocracies = over-reporting (Martinez 2022, *Journal of Political Economy*). |
| **Test** | Reproduce that autocracy elasticity gradient on the **VIIRS era (2012-2023)** with free data, the window a live product would run on. |
| **Verdict** | **NO-GO**, the gradient does not reproduce on VIIRS. |

## The thesis (and why the slot was empty)

The pattern, borrowed from a validated climate project: find a quantity where a free satellite measurement can serve as ground truth, the official record is a crude or self-reported proxy, and no funded institution already ships the cross-referenced result. Official GDP is a textbook interested-party self-report; Martinez showed autocracies overstate growth by ~35% using exactly a radiance-vs-GDP comparison; and no free, annually-refreshed, named-government "official-vs-lights-implied GDP" product exists (raw lights are shipped by EOG/Payne; Martinez is a one-time paper; gridded-GDP products bake the official number back in). The slot is open. The question was whether the signal is real on the *shippable* window.

## What was run

Free data, all public: GDP = World Bank WDI `NY.GDP.MKTP.KD` (real, constant 2015 US$); lights = Earth Observation Atlas VIIRS ADM0 sum-of-lights (CC BY 4.0, Najjar 2024); regime = OWID / V-Dem Regimes of the World. Panel ~170 countries x 2012-2023.

Model: `log(realGDP) = b*log(sum-of-lights) + g*[log(SoL) x autocracy] + country FE + year FE`, SE clustered by country. The gradient **g** is the extra lights-to-GDP elasticity in autocracies; the thesis needs **g > 0**.

| Spec | Gradient g | Reading |
|---|---|---|
| **Within-country FE + year FE** (clean causal) | **+0.002** (ns, p=0.30) | No gradient, signal absent |
| Within-FE, drop gas-flaring countries | +0.002 (ns, p=0.21) | Unchanged |
| Cross-sectional (year FE only) | **-0.237** (p=0.003) | Significant but **wrong sign** |
| Cross-sectional, drop flaring | -0.302 (p=0.0006) | Wrong sign, stronger |

## Why it failed (honestly)

- The **clean within-country identification** (the spec that isolates manipulation from structural differences) shows **no gradient**, robust to dropping flaring petrostates.
- The **cross-sectional** spec is significant but the **opposite sign**, and it conflates genuine elasticity heterogeneity (autocracies are often resource economies) with manipulation, exactly the pitfall the kill-test flagged in advance.
- The democracy elasticity is positive and sensible (lights *do* predict GDP), so the data and merge are sound. It's the autocracy gradient specifically that is absent.
- **Most likely cause:** Martinez's headline used **DMSP (1992-2013)**, a long panel. The VIIRS era is short (12 years) and the within-country signal needs regime *switchers* to identify, there aren't enough, and long-run over-reporting accumulation isn't visible in the window. The live VIIRS-era product has no reproducible signal to ship.

## What's here

- **`code/`**, the pipeline: `wb_gdp.py` (World Bank WDI), `lights.py` (VIIRS sum-of-lights), `regime.py` (V-Dem regime join), `_altspec.py` (alternate specifications), `nightlights_test.py` (the panel regression + verdict). Reusable for a DMSP-bridge revisit.
- **`writeups/`**, the full scoping note and validation report.

## Reproducing

All inputs are free. `pip install -r requirements.txt`, then run the pipeline in `code/` (it fetches World Bank WDI + the Earth Observation Atlas VIIRS export and runs the panel). See `writeups/validation_report.md` for the exact data vintages and specs.

## License & citation

Code under MIT; the writeups under CC-BY-4.0. See `CITATION.cff`. Archived on Zenodo (DOI in `CITATION.cff`). Author: Zach Dissington (ORCID 0009-0007-0196-1371).


## Related artifacts

Part of a series of open, honest research kill-tests, most are negative results, published so others can build on or disprove them rather than duplicate the work:

- [InSAR accountability kill-tests](https://github.com/zachdissington/insar-accountability-killtests): free Sentinel-1 deformation vs official/self-reported records (tailings dams, levees). DOI [10.5281/zenodo.21045290](https://doi.org/10.5281/zenodo.21045290)
- [Nightlights vs official GDP](https://github.com/zachdissington/nightlights-gdp-killtest): does the autocracy over-reporting gradient reproduce on VIIRS? DOI [10.5281/zenodo.21045541](https://doi.org/10.5281/zenodo.21045541)
- [Space-economy solo-wedge assessment](https://github.com/zachdissington/space-economy-killtest): is there a foundable solo wedge in the orbital attribution layer? DOI [10.5281/zenodo.21045736](https://doi.org/10.5281/zenodo.21045736)
- [Climate Solutions Research Kit](https://github.com/zachdissington/climate-solutions-research-kit): spatial-prior method + the validated CF4 smelter prior. DOI [10.5281/zenodo.20617485](https://doi.org/10.5281/zenodo.20617485)

Author: Zach Dissington (ORCID [0009-0007-0196-1371](https://orcid.org/0009-0007-0196-1371)).
