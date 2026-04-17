# Chapter 10: Data Summary for Multiple Regression — Dashboard Plan

## Context

Chapter 10 introduces multiple regression: partial effects, correlation matrices, model fit statistics (R², adj R², AIC, BIC), the FWL theorem, multicollinearity (VIF), and the parsimony principle. This dashboard makes these concepts interactive, letting students build any of 63 possible models from 6 predictors and see how coefficients, significance, and fit change.

## Design decisions

- Charts: Plotly.js 2.35.2
- Data: All 63 possible OLS models (6 predictors, 2^6−1 combinations) pre-computed in build.py
- Theming: light + dark toggle with localStorage persistence
- Scope: Key Concepts 10.1–10.8

## Widgets

| # | Widget | Key Concept | Dataset | Target interaction |
|---|---|---|---|---|
| 1 | Partial vs total effects | KC 10.1 | AED_HOUSE | Focus + control variable selectors; bar comparison |
| 2 | Correlation matrix heatmap | KC 10.2, 10.3 | AED_HOUSE | Interactive annotated heatmap (7×7) |
| 3 | Multiple regression builder | KC 10.4 | AED_HOUSE | Checkbox toggles for 6 predictors; live coefficient table + CI plot |
| 4 | FWL theorem demo | KC 10.5 | AED_HOUSE | Target + control selectors; residual scatter with FWL line |
| 5 | Model comparison | KC 10.6, 10.7 | AED_HOUSE | Progressive 1→6 variable models; R²/adj R²/AIC/BIC chart |
| 6 | VIF detector | KC 10.8 | AED_HOUSE | Color-coded VIF bars with severity thresholds |
| 7 | Diagnostics | § 10.4 | AED_HOUSE | Model selector; actual vs predicted + residual plots |

## Data

- **AED_HOUSE.DTA**: 29 houses, 8 columns (price, size, bedrooms, bathrooms, lotsize, age, monthsold, list)
- **63 pre-computed OLS models**: All combinations of 6 predictors, each with coefficients, SE, t-stats, p-values, 95% CIs, R², adj R², AIC, BIC, RMSE, fitted values, residuals
- **Correlation matrix**: 7×7 (price + 6 predictors)
- **VIF values**: Full model + drop-one variants

No supplementary datasets.

## Key Concepts deliberately not covered

| KC | Reason |
|---|---|
| 10.9 Functional Form / Cross-Country | Case study — narrative, not interactive |
| 10.10 Multiple Regression in Development | Case study — narrative |
| 10.12 High-Dimensional Satellite Features | Case study — requires external data |
| 10.13 Incremental Predictive Power | Covered by model comparison widget |

## Verified Numbers

| Metric | App | Chapter | Match |
|---|---|---|---|
| Bivariate bedrooms coef | $23,667.30 | $23,667 | ✓ |
| Multiple bedrooms coef (size+bed) | $1,553.46 | $1,553 | ✓ |
| Simple R² (size) | 0.6175 | 0.6175 | ✓ |
| Simple adj R² (size) | 0.6033 | 0.6033 | ✓ |
| Full R² | 0.6506 | 0.6506 | ✓ |
| Full adj R² | 0.5552 | 0.5552 | ✓ |
| Full AIC | 675.48 | 675.48 | ✓ |
| Full BIC | 685.05 | 685.05 | ✓ |
| Full size coef | $68.37/sqft | $68.37 | ✓ |

## Verification

- [x] Build runs clean (`python3 web-apps/ch10/build.py`)
- [x] Stats match chapter (all 10 sanity checks pass)
- [x] Verification script passes (`verify_app.py`)
- [x] 7 widget sections, 7 rerender hooks
- [x] File size: 124.9 KB (budget: 200 KB)
- [x] No leftover `{{...}}` placeholders
- [x] JSON data island parses (6 top-level keys)
- [x] JS passes `node --check`
- [x] 63 models pre-computed
