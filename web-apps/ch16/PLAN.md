# Chapter 16: Checking the Model and Data -- Dashboard Plan

## Context

This dashboard complements the static Chapter 16 notebook on regression diagnostics and model validation. It lets students interactively explore multicollinearity (VIF), heteroskedasticity (robust SEs), autocorrelation (AR(1) simulation), diagnostic plots, influential observations (DFITS/DFBETAS), and omitted variable bias -- all concepts that benefit from hands-on manipulation rather than static output.

## Design decisions

- Charts: Plotly.js (v2.35.2)
- Data: pre-computed JSON embedded inline (111.5 KB total)
- Theming: light + dark toggle (persisted via localStorage)
- Scope: Key Concepts 16.1 through 16.8

## Widgets

| Widget | Key Concept | Dataset | Target interaction |
|---|---|---|---|
| VIF Explorer | KC 16.1, 16.2 | AED_EARNINGS_COMPLETE | Toggle base vs collinear model, adjust VIF threshold |
| Robust vs Standard SEs | KC 16.3, 16.4 | AED_EARNINGS_COMPLETE | Toggle SE comparison vs residual scatter, highlight variables |
| Autocorrelation Explorer | KC 16.5 | Simulated AR(1) | Adjust rho (0-0.95), n (50-500), resimulate |
| Diagnostic Plots | KC 16.7 | AED_DEMOCRACY | Toggle bivariate/multiple, actual-vs-fitted/residual-vs-fitted, country labels |
| Influential Observations | KC 16.8 | AED_DEMOCRACY | Toggle DFITS/DFBETAS, label modes (flagged/all/off) |
| Omitted Variable Bias | KC 16.6 | AED_DEMOCRACY | Toggle control sets progressively, scatter vs coefficient bar view |

## Data

- **AED_EARNINGS_COMPLETE.DTA**: 872 full-time workers with earnings, age, education, agebyeduc (2010)
- **AED_DEMOCRACY.DTA**: 131 countries with democracy, growth, and institutional variables (Acemoglu et al. 2008)

## Key Concepts deliberately not covered

- KC 16.3 (OLS Assumption Violations): covered conceptually in the callout text but not as a separate interactive widget since the chapter's treatment is mainly a reference table. The Robust SE and Autocorrelation widgets demonstrate the two major violation types.

## Verification

- [x] Build runs clean (111.5 KB, under 200 KB budget)
- [x] Stats match chapter: VIF collinear age=22.0, educ=17.3, agebyeduc=36.88
- [x] Stats match chapter: SE ratio education = 1.1246
- [x] Stats match chapter: growth coef bivariate=0.1308, multiple=0.0468 (64.2% reduction)
- [x] Stats match chapter: DFITS threshold=0.4623, 5 flagged observations
- [x] verify_app.py passes: no placeholders, valid JSON (3 keys), JS syntax OK, 6 widgets, 6 rerender hooks
- [x] All controls keyboard operable (toggle groups, sliders, resim button)
- [x] Hash state roundtrips (REG object covers all 12 controls)
- [x] Theme toggle re-renders all 6 charts

## Future improvements

- Add LOWESS overlay toggle for diagnostic plots (would require JS LOWESS implementation)
- Add DFBETAS panels for all coefficients (currently only growth)
- Add White test p-value display in Robust SE widget
