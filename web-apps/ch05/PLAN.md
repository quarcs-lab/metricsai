# Chapter 05: Bivariate Data Summary — Dashboard Plan

## Context

Chapter 5 introduces bivariate data analysis: scatterplots, correlation, OLS regression, R², and the association-vs-causation distinction. This dashboard makes the core concepts interactive, letting students explore how different variable pairs produce different correlations and regression lines, visualize what different r values look like, and see why regression is directional (not causal).

## Design decisions

- Charts: Plotly.js 2.35.2
- Data: pre-computed JSON embedded inline (86.5 KB total, ~36 KB data payload)
- Theming: light + dark toggle (persisted via localStorage)
- Scope: Key Concepts 5.1, 5.3, 5.4, 5.5, 5.6, 5.7 + Section 5.11

## Widgets

| # | Widget | Key Concept | Dataset | Target interaction |
|---|---|---|---|---|
| 1 | Bivariate summary stats | KC 5.1 | AED_HOUSE | Variable pair selector; side-by-side stats + covariance |
| 2 | Scatterplot & correlation | KC 5.3, 5.4 | AED_HOUSE | X variable selector; live r readout with strength label |
| 3 | Correlation patterns | KC 5.4 | Synthetic (21×30pts) | Target r slider (-1 to +1); see what r values look like |
| 4 | OLS regression line | KC 5.5, 5.6 | AED_HOUSE | X variable, prediction slider, residuals toggle |
| 5 | R-squared decomposition | KC 5.6 | AED_HOUSE | View toggle (TSS/ESS/RSS); deviation lines on scatter |
| 6 | Regression asymmetry | KC 5.7 | AED_HOUSE | Direction toggle (Y~X / X~Y / both); reciprocal check |
| 7 | Parametric vs nonparametric | Sec 5.11 | AED_HOUSE | OLS/LOWESS/kernel toggles; bandwidth slider |

## Data

- **AED_HOUSE.DTA**: 29 houses, Central Davis CA, 1999. Variables: price, size, bedrooms, bathrooms, lotsize, age.
- **Synthetic correlation data**: 21 datasets (r = -1.0 to +1.0, step 0.1), 30 points each, seed=42.
- **LOWESS fits**: Pre-computed at 15 bandwidth values (frac 0.30 to 1.00, step 0.05).
- **Kernel smoothing**: Pre-computed at 5 bandwidth multipliers (50%, 100%, 150%, 200%, 300% of std(size)).

No supplementary datasets. All data from the chapter's primary dataset.

## Key Concepts deliberately not covered

| KC | Reason |
|---|---|
| 5.2 Two-Way Tabulations | Purely tabular; interactive crosstab has low pedagogical payoff |
| 5.8 Capital-Productivity | Case study narrative — interpretive, not slider-driven |
| 5.9 Interpreting Slope in Context | Case study extension — covered by OLS widget |
| 5.10 Correlation vs. Causation | Narrative — same lesson as asymmetry widget |
| 5.11 NTL as Development Proxy | Case study — conceptual, not interactive |
| 5.12 Prediction vs. Causation | Case study — conceptual, not interactive |

## Verified Numbers

| Metric | App | Chapter | Match |
|---|---|---|---|
| Mean price | $253,910.34 | $253,910.34 | ✓ |
| Mean size | 1,882.76 | 1,882.76 | ✓ |
| r(price,size) | 0.7858 | 0.7858 | ✓ |
| Slope | 73.771 | 73.771 | ✓ |
| Intercept | 115,017.28 | 115,017.28 | ✓ |
| R² | 0.6175 | 0.6175 | ✓ |
| SE | 23,550.66 | 23,550.66 | ✓ |
| Reverse slope | 0.00837 | 0.00837 | ✓ |

## Verification

- [x] Build runs clean (`python3 web-apps/ch05/build.py`)
- [x] Stats match chapter (all 8 sanity checks pass)
- [x] Verification script passes (`verify_app.py`)
- [x] 7 widget sections, 7 rerender hooks
- [x] File size: 86.5 KB (budget: 200 KB)
- [x] No leftover `{{...}}` placeholders
- [x] JSON data island parses
- [x] JS passes `node --check`
