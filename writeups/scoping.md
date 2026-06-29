---
id: EOA-nightlights-gdp
title: Nightlights-implied GDP vs official government GDP (autocracy over-reporting)
status: BUILT + RUN, NO-GO (signal absent on VIIRS era)
cf4_fit: cleanest validation substrate; novelty = live maintained product
verdict: NO-GO, Martinez autocracy gradient does not reproduce on VIIRS (2012-2023)
assessed: 2026-06-28
---

## Build verdict (2026-06-28): NO-GO, the gradient doesn't reproduce on VIIRS
Ran the full Martinez elasticity regression end-to-end on live data (World Bank GDP + eoatlas VIIRS
sum-of-lights + OWID/V-Dem regime; ~170 countries × 2012-2023). The methodology gate (the CONDITIONAL)
resolved against it: clean within-country FE gradient ≈ +0.002 (ns); cross-sectional gradient significant
but **wrong sign** (−0.24, confounded by structural heterogeneity). Neither reproduces Martinez's positive
over-reporting gradient on the VIIRS era. Consistent with the predicted risk (his headline used DMSP
1992-2013; VIIRS era too short). Full detail + caveats: `validation_report.md`. Pipeline in `code/`
(reusable for a DMSP-bridge revisit). **Banked negative.**

---

## Cheap-test verdict (2026-06-28): CONDITIONAL (lean GO on occupancy, gated by methodology)
- **Occupancy OPEN:** no free, maintained, named-government "official-vs-lights-implied GDP discrepancy"
  product exists. EOG/Payne ships raw VIIRS only; World Bank has a static 2010 dataset + papers; Martinez
  2022 (JPE) is a one-time paper; gridded-GDP products (Kummu, Chen-Nordhaus) bake the *official* number in;
  World Economics' quality ratings aren't lights-based. The live named-government product slot is empty.
- **The gate is methodology, not occupancy.** The credible version is Martinez's regime-differential
  **elasticity regression** (autocracies show higher lights→GDP elasticity), NOT a naive radiance/GDP ratio.
  A naive build dies to one critique: gas-flaring inflates petrostates (must subtract VIIRS Nightfire),
  elasticity heterogeneity ≠ manipulation (need V-Dem/Polity regime interaction), VIIRS only starts ~2012
  (Martinez's headline used DMSP 1992–2013), aurora/snow/stray-light at high latitudes.
- **kill_risk:** defensibility/thin novelty, done right it's a refreshable re-run of a published JPE
  regression (low value-add); done wrong (the naive ratio) it's refutable in a sentence. The slot is empty
  partly *because* it's a thin wrapper over existing science.
- **Cheapest next step (weekend, free):** download EOG VNL V2.1 flare-removed annual composites 2013–2024,
  sum-of-lights per country, join World Bank WDI GDP + V-Dem, run the elasticity-gradient panel on the
  VIIRS-era window. **GO if** the autocracy gradient survives post-2012 AND survives dropping top flaring
  countries; **kill if** it vanishes in VIIRS-only data or is flaring-driven.

---

# Nightlights-as-GDP-misreporting, scoping

**Thesis:** a free, annually-refreshed, country-by-country artifact comparing VIIRS night-lights-implied
economic activity against official government GDP, flagging named governments whose self-reported growth
diverges from the independent radiance signal. The candidate with the **cleanest validation substrate** of
any in the scan.

## CF4-recipe fit
1. **Independent measurement (STRONG / cleanest):** VIIRS DNB radiance is independent physics, a
   well-established economic-activity proxy.
2. **Crude self-reported proxy (STRONGEST):** official GDP is a textbook interested-party self-report;
   Martinez (Journal of Political Economy 2022) showed autocracies overstate growth by ~35% using exactly
   this radiance-vs-GDP comparison.
3. **Unoccupied slot:** Payne Institute / EOG ship raw lights but NOT a GDP-discrepancy product; no free,
   annually-refreshed, named-government "official-vs-lights-implied GDP" artifact exists.

## Risks
- **Famous insight = thin novelty moat:** the core result is a celebrated published paper (Martinez), so
  differentiation is "the live, free, maintained, named product nobody bothered to ship," not a new idea.
  Most exposed of the three to "why hasn't someone already done this." (Mitigates by being a maintained
  data product + dashboard, not a paper.)
- **Geopolitical (not legal) exposure:** naming governments as over-reporters; framing = radiance-implied
  vs official, a measured discrepancy, not an accusation of fraud.
- **Methodology dependence:** the radiance↔GDP elasticity must be estimated carefully (Martinez's method
  is public); naive ratios are refutable.

## Scope
A tranche of countries (a set of suspected over-reporters + democratic controls), annual, global-extent
feasible because the data is global and light. Lowest data-engineering lift of the three.

## Cheap test (research)
Reproduce the radiance-vs-official-GDP discrepancy for a small autocracy + control country set (Martinez
method) from public VIIRS + World Bank/IMF GDP, and confirm at source that **no free, maintained,
named-government discrepancy product exists**. **Pass if:** the discrepancy reproduces AND the slot is
empty. **Kill if:** a funded actor already ships a maintained named-government version, or the discrepancy
is too noisy to attribute per-country without heavy econometric machinery.
