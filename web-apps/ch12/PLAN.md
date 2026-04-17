# Chapter 12: Further Topics in Multiple Regression — Dashboard Plan

## Context

Chapter 12 covers advanced inference topics: robust standard errors (HC1, HAC), prediction vs confidence intervals, Type I/II errors and power, autocorrelation, and bootstrap methods. The dashboard makes these concepts interactive — students toggle SE types, visualize prediction funnels, run bootstrap simulations, and explore power curves.

## Design decisions

- **Charts:** Plotly.js
- **Data:** AED_HOUSE.DTA (29 houses) + AED_REALGDPPC.DTA (241 quarters GDP growth) — pre-computed JSON, embedded inline
- **Simulation:** Bootstrap widget uses live JS resampling (seeded PRNG); Type I/II widget uses Monte Carlo
- **Theming:** light + dark toggle (localStorage-persisted)
- **Scope:** Key Concepts 12.1–12.8 (6 widgets)

## Widgets

| Widget | Key Concept(s) | Target interaction |
|---|---|---|
| 1. Robust SE Selector | 12.1, 12.2 | Toggle Default/HC1/HAC SE type; same coefficients, different SEs |
| 2. Prediction Interval Visualizer | 12.3, 12.4 | Size slider; CI vs PI toggle; funnel visualization |
| 3. Type I/II Error Explorer | 12.8 | True effect slider; power curve; Monte Carlo simulation |
| 4. Autocorrelation Visualizer | 12.2 | GDP growth ACF; lag slider |
| 5. SE Ratio Comparator | 12.1 | Bar chart robust/default SE ratio per variable |
| 6. Bootstrap Simulation | 12.7 | Resample button; histogram of bootstrap slope estimates |

## Data

- `data/AED_HOUSE.DTA` — 29 houses: price, size, bedrooms, bathrooms, lotsize, age
- `data/AED_REALGDPPC.DTA` — 241 quarters: GDP growth time series

## Key Concepts not given standalone widgets

- KC 12.5 (Sample Selection Bias): Requires weighted regression; no interactive intuition from sliders
- KC 12.6 (FGLS): Too technical; better suited to chapter prose
- KC 12.9, 12.10 (Case study KCs): Belong in case-study context

## Verification

- [x] Build runs clean (64.4 KB)
- [x] House data: 29 observations, simple reg b1=73.77, R2=0.6175
- [x] GDP growth: 241 observations, mean=1.99, ACF lag1=0.866
- [x] verify_app.py: all checks passed, 6 widgets, 6 rerender hooks
- [x] JS passes node --check
- [x] No unreplaced placeholders
