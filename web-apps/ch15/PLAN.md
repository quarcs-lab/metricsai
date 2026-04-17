# Chapter 15: Regression with Transformed Variables — Dashboard Plan

## Context

Chapter 15 covers variable transformations in OLS regression: log transformations (log-linear, log-log), quadratic models with turning points, standardized coefficients for comparing variable importance, interaction terms with varying marginal effects, and retransformation bias correction. The dashboard makes each transformation concept interactive using the AED_EARNINGS_COMPLETE dataset.

## Design decisions

- **Charts:** Plotly.js
- **Data:** AED_EARNINGS_COMPLETE.DTA (872 obs) — raw scatter data + pre-computed OLS results embedded
- **Regressions:** 7 model specifications pre-computed in Python with HC1 robust SEs
- **Theming:** light + dark toggle (localStorage-persisted)
- **Scope:** Key Concepts 15.1–15.7 (6 widgets)

## Widgets

| Widget | Key Concept(s) | Target interaction | Learning objective |
|---|---|---|---|
| 1. Log Transformation Explorer | 15.1, 15.2 | Toggle: Levels vs Log-linear | Same data, different interpretation: $/yr vs %/yr |
| 2. Quadratic & Turning Point | 15.3, 15.4 | Toggle linear/quadratic; age slider for ME | Inverted U-shape; turning point at 49.5 years |
| 3. Standardized Coefficients | 15.5 | Toggle raw/standardized bar chart | Compare variable importance on the same scale |
| 4. Interaction Marginal Effects | 15.6 | Age slider; live ME of education | Returns to education increase with age |
| 5. Retransformation Bias | 15.7 | Toggle naive/corrected predictions | Smearing correction fixes systematic underprediction |
| 6. Residual Distribution | 15.2 | Toggle levels/log residuals | Log transformation reduces skewness |

## Verification

- [x] Build runs clean (76.6 KB)
- [x] Levels: education = $5,737/yr, R² = 0.1032
- [x] Log-linear: education = 0.0995 (9.95%/yr), R² = 0.1758
- [x] Turning point (quadratic): 49.5 years
- [x] Retransformation: naive=$46,861, corrected=$55,503, actual=$56,369, smearing=1.184
- [x] verify_app.py: all checks passed, 6 widgets, 6 rerender hooks

## Key Concepts deliberately not covered

- **KC 15.8 (Mixed regressors):** A comprehensive model table — pedagogically redundant with Widget 1 and the model comparison table in Ch14.
