# Chapter 4: Statistical Inference for the Mean — Dashboard Plan

## Context

Chapter 4 introduces the complete statistical inference toolkit: standard errors, the t-distribution, confidence intervals, two-sided and one-sided hypothesis tests, and inference for proportions. The dashboard makes each step interactive so students can see how changing hypothesized values, sample sizes, and confidence levels affects test outcomes in real time.

## Design decisions

- **Charts:** Plotly.js
- **Data:** AED_EARNINGS.DTA (n=171), AED_GASPRICE.DTA (n=32), AED_EARNINGSMALE.DTA (n=191), AED_REALGDPPC.DTA (n=241) — pre-computed JSON, embedded inline
- **t-distribution math:** Full implementation of incomplete beta function, t-CDF, t-PDF, t-quantile in JavaScript for accurate p-values and critical values
- **Theming:** light + dark toggle (localStorage-persisted)
- **Scope:** Key Concepts 4.1–4.5, 4.8, 4.9 (7 widgets)

## Widgets

| Widget | Key Concept(s) | Dataset | Target interaction | Learning objective |
|---|---|---|---|---|
| 1. SE & Sample Size | 4.1 | Earnings | n-slider (10–500); SE curve with 4×n marker | SE = s/√n; quadruple n to halve SE; diminishing returns |
| 2. t-Distribution Explorer | 4.2 | Synthetic | df toggle (4/10/30/100); Normal overlay | Fatter tails at low df; convergence to Normal |
| 3. Confidence Interval | 4.3 | Earnings/Gas | Confidence level slider (80–99%); Dataset toggle | Precision-confidence trade-off; wider CI = more confidence |
| 4. Two-Sided Test | 4.4 | Earnings | H₀ slider ($30k–$55k) | t-stat, p-value, rejection regions; boundary = CI endpoint |
| 5. One-Sided Test | 4.8 | Earnings | H₀ slider + direction toggle | One-sided p = half of two-sided; more power in predicted direction |
| 6. Gas Price Test | 4.4, 4.5 | Gas Prices | H₀ slider ($3.40–$4.10) | Statistical vs practical significance; small SE → high power |
| 7. Proportions | 4.9 | Synthetic | p̂, n, p₀ sliders | SE = √(p̂(1−p̂)/n); same inference framework for binary data |

## Data

- `data/AED_EARNINGS.DTA` — 171 female earnings (30-year-old full-time workers)
- `data/AED_GASPRICE.DTA` — 32 gas station prices (Yolo County, CA)
- `data/AED_EARNINGSMALE.DTA` — 191 male earnings (embedded but not directly used in widgets; available for extensions)
- `data/AED_REALGDPPC.DTA` — 241 GDP growth rates (embedded but not directly used in widgets; available for extensions)
- No supplementary datasets.

## Verification

- [x] Build runs clean (57.1 KB)
- [x] Earnings: mean = $41,412.69, SD = $25,527.05, SE = $1,952.10 (all match chapter)
- [x] Gas: mean = $3.6697, SD = $0.1510, SE = $0.0267 (all match chapter)
- [x] t-stat for H₀: μ=$40,000: 0.7237, p-value: 0.4703 (match chapter)
- [x] Gas t-stat for H₀: μ=$3.81: −5.2577, p-value: <0.0001 (match chapter)
- [x] verify_app.py: all checks passed, 7 widgets, 7 rerender hooks
- [x] JS passes node --check

## Key Concepts deliberately not covered

- **KC 4.6 ("Fail to Reject" ≠ "Accept"):** Interpretive concept; reinforced through callout text in Widget 4 rather than a separate interactive widget.
- **KC 4.7 (Context & Consistency):** Narrative concept about applying the testing framework across domains. No single interaction adds pedagogical value.
- **KC 4.10–4.13 (Economic significance, development):** Case-study tier concepts; deferred to case-study dashboards.

## JavaScript math library

Implemented in the template for accurate inference computations:
- `lnGamma()` — Lanczos approximation
- `betaCF()` — Continued fraction for incomplete beta
- `betaInc()` — Regularized incomplete beta function
- `tCDF()`, `tPDF()`, `tQuantile()` — Full t-distribution (via incomplete beta)
- `normalPDF()`, `normalCDF()` — Standard normal (Abramowitz & Stegun approximation)
