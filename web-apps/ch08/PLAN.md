# Chapter 08: Case Studies for Bivariate Regression — Dashboard Plan

## Context

Chapter 8 is an integrated case study chapter where sections 8.1–8.4 ARE the case studies. It applies bivariate regression to three domains — health economics (OECD cross-sectional), finance (CAPM monthly returns), and macroeconomics (Okun's Law annual time series). The static chapter presents fixed regression outputs; this dashboard makes the analysis interactive, letting students toggle outcomes, compare stocks, exclude outliers, and predict with sliders.

## Design decisions

- **Charts:** Plotly.js (scatter, time series, histogram)
- **Data:** Three AED .DTA datasets pre-computed into compact JSON (34 OECD countries, 366 monthly returns for 3 stocks, 59 annual US macro observations)
- **OLS:** Pre-computed regressions in build.py for main models; live `olsFit()` in JS for the outlier widget
- **Theming:** light + dark toggle (localStorage-persisted)
- **Scope:** Key Concepts 8.1–8.8 (7 widgets)

## Widgets

| Widget | Key Concept(s) | Dataset | Target interaction |
|---|---|---|---|
| 1. Health Outcomes | 8.1, 8.2 | AED_HEALTH2009 | Toggle life expectancy / infant mortality; show residuals |
| 2. Health Expenditures vs GDP | 8.3 | AED_HEALTH2009 | Toggle all countries / exclude USA & LUX; highlight outliers |
| 3. Outlier Detection & Influence | 8.4 | AED_HEALTH2009 | Slider drops N countries by largest residual; live OLS refit |
| 4. CAPM Stock Betas | 8.5, 8.6 | AED_CAPM | Toggle Coca-Cola / Target / Walmart; show beta=1 reference line |
| 5. CAPM Residual Diagnostics | 8.6 | AED_CAPM | Toggle stock; switch scatter vs histogram view |
| 6. Okun's Law | 8.7 | AED_GDPUNEMPLOY | Prediction slider; toggle Okun's original slope=-2 reference |
| 7. Okun Time Series | 8.8 | AED_GDPUNEMPLOY | Year range sliders; toggle actual+predicted vs residuals; subperiod regression |

## Data

- `data/AED_HEALTH2009.DTA` — 34 OECD countries (2009): hlthpc, lifeexp, infmort, gdppc, code
- `data/AED_CAPM.DTA` — 366 monthly observations (1983–2013): rm_rf, rko_rf, rtgt_rf, rwmt_rf
- `data/AED_GDPUNEMPLOY.DTA` — 59 annual US observations (1961–2019): rgdpgrowth, uratechange, year

## Key Concepts covered

All 8 Key Concepts are addressed:
- KC 8.1 + 8.2 paired in Widget 1 (economic vs. statistical significance + robust SEs via outcome toggle)
- KC 8.3 in Widget 2 (income elasticity of demand)
- KC 8.4 in Widget 3 (outlier detection and influence with interactive exclusion)
- KC 8.5 + 8.6 paired in Widget 4 (systematic risk and beta + R² interpretation)
- KC 8.6 also in Widget 5 (residual diagnostics showing idiosyncratic risk)
- KC 8.7 in Widget 6 (Okun's Law with prediction slider)
- KC 8.8 in Widget 7 (structural breaks via time series view)

## Verification

- [x] Build runs clean (74.3 KB)
- [x] Health: 34 countries loaded
- [x] Lifeexp reg: b1=73.08, b2=0.001112, R²=0.3197
- [x] Infmort reg: b1=6.70, b2=-0.000693, R²=0.1446
- [x] Hlth~GDP all: b2=0.0899, R²=0.6041
- [x] Hlth~GDP subset: b2=0.1267, R²=0.9282
- [x] CAPM KO: alpha=0.0068, beta=0.6063, R²=0.2011
- [x] Okun: b1=3.01, b2=-1.59, R²=0.5920
- [x] verify_app.py: all checks passed, 7 widgets, 7 rerender hooks
- [x] JS passes node --check
- [x] No unreplaced placeholders
- [x] Size 74.3 KB (budget 200 KB)
