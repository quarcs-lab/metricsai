# Chapter 14: Regression with Indicator Variables — Dashboard Plan

## Context

Chapter 14 introduces indicator (dummy) variables in regression: how a single binary variable captures a difference in means, how adding controls changes the estimated gap, how interaction terms allow slopes to differ across groups, and how sets of indicators handle categorical variables. The dashboard makes each concept interactive using the AED_EARNINGS_COMPLETE dataset (872 full-time workers).

## Design decisions

- **Charts:** Plotly.js
- **Data:** AED_EARNINGS_COMPLETE.DTA (872 obs, 45 columns) — raw scatter data + pre-computed OLS results embedded as JSON
- **Regressions:** 5 progressive models + 3 worker-type models pre-computed in Python with HC1 robust SEs
- **Theming:** light + dark toggle (localStorage-persisted)
- **Scope:** Key Concepts 14.1–14.8 (6 widgets)

## Widgets

| Widget | Key Concept(s) | Target interaction | Learning objective |
|---|---|---|---|
| 1. Gender Gap Explorer | 14.1, 14.2 | Dropdown: 4 models (raw gap → full controls) | Watch gender gap change as controls are added |
| 2. Interaction Slope Visualizer | 14.3 | Toggle interaction on/off | Parallel vs non-parallel lines; different returns to education |
| 3. Model Comparison Table | 14.2, 14.4 | Static table with all 5 models | Track coefficient changes and R² across models |
| 4. Dummy Variable Trap | 14.6, 14.7 | Toggle base category (3 options) | R² and predictions identical regardless of base choice |
| 5. Worker Type Bar Chart | 14.5 | Bar chart with 95% CIs | Compare mean earnings across job types |
| 6. Scatter by Gender | 14.3, 14.8 | Toggle: Both/Male/Female | Separate regression lines; gender gap at different education levels |

## Data

- `data/AED_EARNINGS_COMPLETE.DTA` — 872 full-time workers aged 25–65 (2000)
  - 494 males, 378 females
  - 79 self-employed, 663 private, 130 government
- No supplementary datasets.

## Verification

- [x] Build runs clean (54.1 KB)
- [x] Model 1: gender = −$16,396.42, t = −5.0961, R² = 0.0249 (match chapter)
- [x] Male mean = $63,476.32, Female mean = $47,079.89 (match chapter)
- [x] Worker types: Self=$72,306, Private=$54,521, Govt=$56,105
- [x] verify_app.py: all checks passed, 6 widgets, 6 rerender hooks
- [x] JS passes node --check

## Key Concepts deliberately not covered

- **KC 14.9 (Regional Indicators):** Bolivia case study — separate dashboard scope.
- **KC 14.10 (Regional Interactions):** Bolivia case study — separate dashboard scope.

## Pre-computed regression models

| Model | Variables | R² |
|---|---|---|
| 1 | gender | 0.0249 |
| 2 | gender + education | 0.1340 |
| 3 | gender + education + gender×educ | 0.1395 |
| 4 | + age + hours | 0.1979 |
| 5 | + gender×age + gender×hours | 0.2028 |
