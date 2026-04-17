# Chapter 07: Statistical Inference for Bivariate Regression — Dashboard Plan

## Context

Chapter 7 extends statistical inference to bivariate regression: t-distributions, confidence intervals, hypothesis testing, p-values, economic vs. statistical significance, and robust standard errors. The dashboard makes these abstract concepts tangible through interactive simulations and real data.

## Design decisions

- Charts: Plotly.js (consistent with all other chapter dashboards)
- Data: AED_HOUSE.DTA (29 houses) + Mendez 2020 convergence data pre-computed as JSON
- Theming: light + dark toggle (persisted via localStorage)
- t-distribution math: JS-side tPDF, tCDF (regularized incomplete beta via Numerical Recipes continued fraction), tQuantile (bisection)
- Scope: Key Concepts 7.1-7.6, 7.8

## Widgets

| # | Widget | Key Concept | Dataset | Target interaction |
|---|--------|-------------|---------|-------------------|
| 1 | t-Distribution Explorer | KC 7.1 | Generated | Slider for df, overlay t(df) on N(0,1), shade tails/center |
| 2 | Confidence Interval Simulator | KC 7.2 | Generated (DGP) | Monte Carlo CI coverage, confidence level slider |
| 3 | Hypothesis Testing Framework | KC 7.3, 7.5 | House data | Set null value, choose one/two-sided, show rejection region |
| 4 | p-Value Explorer | KC 7.8 | Generated | Drag t-stat slider, shade p-value area in real time |
| 5 | Economic vs. Statistical Significance | KC 7.4 | Generated (DGP) | Adjust true slope + n to see significance diverge from effect size |
| 6 | Robust Standard Errors | KC 7.6 | Generated (DGP) | Toggle homo/heteroskedastic, compare standard vs robust SEs |
| 7 | House Price Data: Full Inference | KC 7.1-7.6 | AED_HOUSE.DTA | Real data scatter with CI band, hypothesis test, standard vs robust SEs |

## Data

- **AED_HOUSE.DTA**: 29 houses, Central Davis CA 1999. Variables: price, size. Regression: price = 115017.28 + 73.77 * size, se(b2) = 11.17, se_robust(b2) = 11.33, R2 = 0.6175.
- **DGP (generated)**: y = 1 + 2x + u, sigma_u = 2, mu_x = 3, sigma_x = 1 (same as ch06 for continuity).
- **Mendez 2020 convergence clubs**: 108 countries, 2014 cross-section (loaded but used only as embedded JSON reference data).

## Key Concepts deliberately not covered

- **KC 7.7 (Economic Convergence)**: Case-study specific content; better suited to the chapter narrative than an interactive widget.
- **KC 7.9 (Economic Interpretation of Test Results)**: Narrative/interpretive concept, not amenable to interactive visualization.
- **KC 7.10-7.13**: Case study Key Concepts (DS4Bolivia, convergence clubs) — application-specific, not core inference concepts.

## Verification

- [x] Build runs clean (74.6 KB)
- [x] Stats match chapter: b2=73.77, se=11.17, se_robust=11.33, R2=0.6175, t_crit(27)=2.0518
- [x] No {{...}} placeholders remaining
- [x] Valid JSON data island (4 top-level keys)
- [x] JS passes node --check
- [x] 7 widget sections = 7 rerender hooks
- [x] Hash state roundtrips (REG object with all 7 widgets)
- [x] Theme toggle re-renders all charts
- [x] t-distribution math verified: t_crit(0.975,27)=2.0518, tCDF(2.0518,27)=0.975, p(t=-1.452,df=27)=0.158

## Future improvements

- Add prediction intervals widget (KC on prediction vs confidence bands)
- Add Monte Carlo coverage for robust vs standard SEs under heteroskedasticity
- Interactive residual diagnostic plots
