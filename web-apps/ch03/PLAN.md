# Chapter 3: The Sample Mean — Dashboard Plan

## Context

Chapter 3 introduces the sampling distribution of the sample mean through coin-toss experiments (400 samples, n=30) and 1880 U.S. Census age data (100 samples, n=25). The chapter covers properties of the sample mean (unbiasedness, precision), the Central Limit Theorem, estimator properties, and weighted means for nonrepresentative samples. The dashboard makes each concept interactive so students can see the consequences of changing sample sizes, population shapes, and estimation strategies.

## Design decisions

- **Charts:** Plotly.js
- **Data:** AED_COINTOSSMEANS.DTA (400 xbar, n=30) + AED_CENSUSAGEMEANS.DTA (100 means, n=25) — pre-computed JSON, embedded inline
- **Simulation:** Widgets 2–4 use live JavaScript simulation (seeded PRNG for reproducibility + Resimulate button)
- **Theming:** light + dark toggle (localStorage-persisted)
- **Scope:** Key Concepts 3.2–3.8 (5 widgets)

## Widgets

| Widget | Key Concept(s) | Target interaction | Learning objective |
|---|---|---|---|
| 1. Sampling Distribution & SE | 3.2, 3.3, 3.4 | Toggle: coin/census; Normal overlay; SE bands (off/±1/±2) | X̄ is a random variable; its distribution centers on μ with spread σ/√n |
| 2. Sample Size Effect | 3.3, 3.4 | Slider: n (5–500); Resimulate button | Quadruple n to halve SE; diminishing returns to larger samples |
| 3. Central Limit Theorem | 3.5, 3.6 | Dropdown: 5 population shapes; Slider: n (2–100) | CLT works regardless of population shape; sample means → Normal |
| 4. Estimator Properties | 3.7 | Toggle: Mean/Median/Trimmed; Sliders: n, contamination | Mean is most efficient for clean data; Median is robust to outliers |
| 5. Weighted Means | 3.8 | Sliders: group means, pop/sample fractions | Nonrepresentative samples need IPW correction |

## Data

- `data/AED_COINTOSSMEANS.DTA` — 400 rows: xbar, stdev, numobs (all n=30)
- `data/AED_CENSUSAGEMEANS.DTA` — 100 rows: mean, stdev, numobs (all n=25)
- No supplementary datasets.

## Verification

- [x] Build runs clean (61.4 KB)
- [x] Mean of 400 coin means = 0.4994 (matches chapter)
- [x] SD of 400 coin means = 0.0863 (matches chapter)
- [x] Theoretical SE = 0.5/√30 = 0.0913 (matches chapter)
- [x] Mean of 100 census means = 23.78 (matches chapter)
- [x] SD of 100 census means = 3.76 (matches chapter)
- [x] Theoretical SE = 18.61/√25 = 3.72 (matches chapter)
- [x] verify_app.py: all checks passed, 5 widgets, 5 rerender hooks
- [x] JS passes node --check

## Key Concepts deliberately not covered

- **KC 3.1 (Random Variables):** Definitional — no meaningful interaction adds pedagogical value.
- **KC 3.9 (Monte Carlo Simulation):** The simulation engine in Widgets 2–4 demonstrates Monte Carlo methods implicitly.
- **KC 3.10–3.11 (Case Study Key Concepts):** Belong in case-study dashboards.

## Simulation engine

Widgets 2–4 use a seeded PRNG (`mulberry32`) for reproducible random sampling:
- **Widget 2:** 500 Bernoulli(0.5) samples of configurable size n
- **Widget 3:** 500 samples from 5 population shapes (Bernoulli, Uniform, Exponential, Bimodal, Gamma/Census-like)
- **Widget 4:** 500 samples from N(50, 10²) with configurable outlier contamination from N(150, 10²)

Box-Muller transform for normal samples; Marsaglia-Tsang method for gamma samples.
