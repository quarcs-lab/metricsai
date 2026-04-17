# Chapter 09: Models with Natural Logarithms — Dashboard Plan

## Context

This app teaches logarithmic transformations in regression through interactive visualization. The static chapter covers four model specifications (lin-lin, log-lin, log-log, lin-log), semi-elasticity, elasticity, exponential growth, and the Rule of 72. The dashboard fills the gap by letting users manipulate parameters and see how transformations change scatter plots, fitted lines, and coefficient interpretations in real time.

## Design decisions

- Charts: Plotly.js
- Data: pre-computed JSON embedded inline (72 KB total)
- Theming: light + dark toggle (persisted via localStorage)
- JS: ES5 only (var, function declarations, no const/let/arrow)
- Scope: Key Concepts 9.1 through 9.9

## Widgets

| Widget | Key Concept | Dataset | Target interaction |
|---|---|---|---|
| Log Approximation Explorer | KC 9.1 | Generated | Slider for % change; compare exact vs log approximation |
| Four Model Specifications | KC 9.2–9.5 | AED_EARNINGS | Toggle lin-lin/log-lin/log-log/lin-log; see scatter + OLS |
| Semi-Elasticity Visualizer | KC 9.3 | Generated | Beta slider; dual plot (log-space linear vs level-space exponential) |
| Elasticity Visualizer | KC 9.4 | Generated | Elasticity slider; dual plot (log-log linear vs level power curve) |
| Exponential Growth & Rule of 72 | KC 9.6, 9.7 | AED_SP500INDEX | S&P 500 levels vs logs; custom growth rate slider |
| Model Comparison Grid | KC 9.5 | AED_EARNINGS | 2x2 grid of all 4 specs; highlight individual models |
| Cross-Country Log Models | KC 9.8, 9.9 | Mendez 2020 convergence | Toggle log-log(kl)/log-lin(h)/linear(kl); country labels |

## Data

- **AED_EARNINGS.DTA**: 171 full-time workers aged 30 (2010), earnings and education
- **AED_SP500INDEX.DTA**: S&P 500 index, annual 1927-2019 (93 years)
- **mendez2020_convergence.csv**: 108 countries, 2014 cross-section (lp, kl, h)

## Key Concepts deliberately not covered

None — all 9 Key Concepts (9.1–9.9) are addressed by at least one widget.

## Verification

- [x] Build runs clean (72.0 KB, within 200 KB budget)
- [x] Stats match chapter (lin-lin b2=5021, log-lin b2=0.1314, log-log b2=1.48, S&P growth=6.5%)
- [x] All controls keyboard operable (sliders + toggle groups)
- [x] Hash state roundtrips (REG object covers all 7 widgets)
- [x] Theme toggle re-renders charts (via __rerender_ hooks)
- [x] verify_app.py passes all checks (7 widgets, 7 rerender hooks, no placeholders, JSON parses, JS passes node --check)

## Future improvements

- Add residual plots for each model specification to show heteroskedasticity patterns
- Overlay earnings data points on the semi-elasticity/elasticity theoretical curves
- Add interactive Rule of 72 calculator with multiple economic examples
