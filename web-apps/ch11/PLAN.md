# Chapter 11: Statistical Inference for Multiple Regression — Dashboard Plan

## Context

Chapter 11 extends single-variable inference to multiple regression: confidence intervals for individual coefficients, t-tests, joint F-tests, the impact of multicollinearity on precision, model comparison via adjusted R², and robust standard errors. The dashboard uses the Davis housing dataset (29 houses, 7 variables) to illustrate how adding correlated variables affects inference.

## Design decisions

- **Charts:** Plotly.js
- **Data:** AED_HOUSE.DTA (29 obs) — 3 nested models with standard and HC1 robust SEs
- **Distribution math:** Full t-distribution and F-distribution (via incomplete beta function)
- **Theming:** light + dark toggle (localStorage-persisted)
- **Scope:** Key Concepts 11.2–11.8 (6 widgets)

## Widgets

| Widget | Key Concept(s) | Target interaction | Learning objective |
|---|---|---|---|
| 1. CI Explorer | 11.3 | Confidence level slider + variable dropdown | CI width trade-off; excluding zero = significance |
| 2. t-Test | 11.4 | H₀ slider for size coefficient | t-distribution with rejection regions; p-value as tail area |
| 3. Multicollinearity | 11.2 | Model 1/2/3 toggle | SE inflation when adding correlated variables |
| 4. Joint F-Test | 11.5, 11.6 | Overall vs subset F-test toggle | Overall model significant but extra vars jointly insignificant |
| 5. Model Comparison | 11.7 | 3-model coefficient table | R² always rises; Adj R² penalizes complexity |
| 6. Robust SEs | 11.8 | Standard vs HC1 toggle | Robustness check; do conclusions change? |

## Verification

- [x] Build runs clean (44.7 KB)
- [x] Model 1: size=$73.77, t=6.60, R²=0.6175 (match chapter)
- [x] Model 3: size=$68.37, se=15.39, R²=0.6506, F=6.83 (match chapter)
- [x] 95% CI for size (Model 3): [$36.44, $100.30] (match chapter)
- [x] Subset F-test: F=0.42 (match chapter)
- [x] verify_app.py: all checks passed, 6 widgets, 6 rerender hooks
