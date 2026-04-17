# Chapter 6: The Least Squares Estimator — Dashboard Plan

## Context

Chapter 6 teaches *why* OLS works and *when* we can trust it: unbiasedness, sampling variability, standard errors, and the Gauss-Markov theorem. The dashboard makes these abstract properties tangible through live JavaScript simulation — students draw samples, run Monte Carlo experiments, and watch sampling distributions form in real time.

## Design decisions

- **Charts:** Plotly.js
- **Data:** AED_GENERATEDDATA.DTA (5 obs, manual example) + Mendez 2020 convergence clubs (108 countries, 2014 cross-section) — pre-computed JSON, embedded inline
- **Simulation:** Widgets 1–5 and 7 use live JavaScript simulation (seeded PRNG for reproducibility + Resimulate buttons)
- **OLS engine:** Custom `olsFit()`, `generateSample()`, `monteCarloOLS()` in vanilla JS
- **Theming:** light + dark toggle (localStorage-persisted)
- **Scope:** Key Concepts 6.1–6.10 (7 widgets)

## Widgets

| Widget | Key Concept(s) | Target interaction | Learning objective |
|---|---|---|---|
| 1. Population vs. Sample Regression | 6.1, 6.2 | Sample size slider; Error/Residual toggle; Resimulate | Population line is fixed; sample line varies; errors ≠ residuals |
| 2. OLS Assumptions Diagnostic | 6.3 | Violation toggle (5 modes); Severity slider; Resimulate | Violating assumptions 1–2 biases slope; 3–4 affect SEs |
| 3. Monte Carlo Unbiasedness | 6.4, 6.8 | Simulations slider; n slider; Slope/Intercept toggle; Resimulate | E[b₂] = β₂ (unbiasedness); distribution ≈ normal (CLT); spaghetti plot shows variability |
| 4. Standard Error Anatomy | 6.5, 6.6 | σᵤ, n, σₓ sliders; Resimulate | se(b₂) = sₑ/√SSx; three factors control precision; df = n−2 |
| 5. Gauss-Markov: OLS vs. Alternatives | 6.7 | Homo/Hetero toggle; Simulations slider; Resimulate | OLS is BLUE under assumptions; loses advantage under heteroskedasticity |
| 6. Real-Data Sampling Variability | 6.8, 6.9 | Subsample size slider; MC draws slider; Display toggle; Resimulate | Real economic data shows same sampling variability as generated data |
| 7. Standard Errors and Sample Size | 6.10 | σᵤ, σₓ sliders; DGP/Convergence toggle; Resimulate | se(b₂) ∝ 1/√n; need 4× data to halve SE |

## Data

- `data/AED_GENERATEDDATA.DTA` — 5 rows: x, y, Eygivenx
- Convergence clubs CSV (fetched at build time, cached as `data/mendez2020_convergence.csv`) — 108 countries, 2014 cross-section: country, GDPpc, kl

## Key Concepts deliberately not covered as standalone widgets

All 10 Key Concepts are covered:
- KC 6.1 + 6.2 paired in Widget 1 (error vs. residual toggle on same scatter)
- KC 6.5 + 6.6 paired in Widget 4 (df feeds into SE formula)
- KC 6.8 appears in both Widget 3 (DGP spaghetti) and Widget 6 (real data)
- KC 6.9 + 6.10 covered in Widgets 6 and 7 respectively

## Simulation engine

All widgets use a seeded PRNG (`mulberry32`) for reproducible random sampling:
- `boxMuller(rng)` for standard normal samples
- `generateSample(rng, n, β₁, β₂, σᵤ, μₓ, σₓ)` for DGP: y = β₁ + β₂x + u
- `olsFit(x, y)` for full OLS statistics (b₁, b₂, sₑ, se(b₂), R², etc.)
- `monteCarloOLS(rng, nSim, n, ...)` for batch simulation
- Widget 5 adds `theilMedianSlope()` and `equalWeightSlope()` for estimator comparison

## Verification

- [x] Build runs clean (71.8 KB)
- [x] Generated data: 5 observations loaded
- [x] Convergence: 108 countries (2014 cross-section)
- [x] Pop regression: b1=2648.99 b2=0.0949 se(b2)=0.0046 R2=0.8006
- [x] verify_app.py: all checks passed, 7 widgets, 7 rerender hooks
- [x] JS passes node --check
- [x] No unreplaced placeholders
