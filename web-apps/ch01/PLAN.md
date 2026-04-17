# Chapter 1: Analysis of Economics Data — Dashboard Plan

## Context

Chapter 1 introduces regression analysis through a concrete example: predicting house prices from house size in Central Davis, CA (n = 29). The chapter walks through scatter plots, OLS, slope interpretation, R², and the crucial distinction between association and causation. The dashboard makes each of these steps interactive so students can see the consequences of their choices rather than reading about them.

## Design decisions

- **Charts:** Plotly.js
- **Data:** AED_HOUSE.DTA (29 houses, 8 columns) — pre-computed JSON, embedded inline
- **Theming:** light + dark toggle (localStorage-persisted)
- **Scope:** Key Concepts 1.1, 1.3, 1.4, 1.5, 1.6, 1.9 (5 widgets)
- **No supplementary data.** Everything comes from the book's dataset.

## Widgets

| Widget | Key Concept(s) | Target interaction | Learning objective |
|---|---|---|---|
| 1. Summary Statistics | 1.1 | Dropdown: price / size / bedrooms | Understand scale, spread, and shape before running regressions |
| 2. Scatter + Regression Line | 1.3, 1.4 | Toggle: line on/off; toggle: residuals on/off | Visual exploration reveals direction, form, strength; residuals show what the line misses |
| 3. Prediction Explorer | 1.5, 1.9 | Size slider + what-if slope slider | Slope = marginal effect; coefficient uncertainty → prediction uncertainty; extrapolation warning |
| 4. R² Visualizer | 1.5 | 3-way toggle: scatter+line / explained / residual | R² = ESS/TSS; visual decomposition into explained and residual components |
| 5. Multi-predictor Comparison | 1.6 | Dropdown across 5 predictors | Same Y, different X → different fits; association is not causation |

## Data

- `data/AED_HOUSE.DTA` — 29 Central Davis, CA houses (1999). Columns: price, size, bedrooms, bathrooms, lotsize, age, monthsold, list.
- No supplementary datasets.

## Verification

- [x] Build runs clean (48.6 KB)
- [x] Mean price = $253,910.34 (matches chapter)
- [x] OLS price~size: intercept=$115,017.28, slope=$73.77, R²=0.6175 (all match)
- [x] verify_app.py: all checks passed, 5 widgets, 5 rerender hooks
- [x] JS passes node --check

## Key Concepts deliberately not covered

- **KC 1.2 (Observational Data):** Definitional — no meaningful interaction adds pedagogical value. The concept is reinforced in the causation callout of Widget 5.
- **KC 1.7–1.8 (Case Studies: Convergence, Panel Data):** Out of scope for single-chapter dashboard.

## Future improvements

- Bivariate-regression-with-confounding widget (show how slope changes when a control variable is added) — belongs in Ch 7+ apps.
- Residual-vs-predicted diagnostic plot (teaches OLS assumptions).
