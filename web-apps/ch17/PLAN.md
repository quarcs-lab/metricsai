# Chapter 17: Panel Data, Time Series Data, Causation — Dashboard Plan

## Context

Chapter 17 covers panel data models (pooled OLS, fixed effects), time series concepts (stationarity, autocorrelation, spurious regression), and dynamic models (ADL). This dashboard makes these advanced topics interactive using NBA team revenue data (panel) and U.S. interest rate data (time series).

## Design decisions

- Charts: Plotly.js 2.35.2
- Data: Pre-computed panel and time series regressions, ACF values, ADL multipliers
- Theming: light + dark toggle with localStorage persistence
- Scope: Key Concepts 17.1–17.7

## Widgets

| # | Widget | Key Concept | Dataset | Target interaction |
|---|---|---|---|---|
| 1 | Variance decomposition | KC 17.1 | AED_NBA | Bar chart: between vs within SD for revenue and wins |
| 2 | Cluster SEs | KC 17.2 | AED_NBA | Bar chart: default vs robust vs cluster SE comparison |
| 3 | Pooled vs Fixed Effects | KC 17.3, 17.4 | AED_NBA | Toggle pooled/FE/both scatter + regression line |
| 4 | Time series levels vs changes | KC 17.5 | AED_INTERESTRATES | Toggle levels/changes time plot |
| 5 | Autocorrelation (ACF) | KC 17.6 | AED_INTERESTRATES | Toggle levels/changes/ADL correlogram |
| 6 | Spurious regression | KC 17.5, 17.7 | AED_INTERESTRATES | Toggle levels/changes scatter with R² comparison |
| 7 | ADL model & multipliers | KC 17.7 | AED_INTERESTRATES | Coefficient plot + cumulative multiplier bars |

## Data

- **AED_NBA.DTA**: 286 obs (29 NBA teams × 10 seasons, 2001-2011). Variables: lnrevenue, wins, teamid, team, season.
- **AED_INTERESTRATES.DTA**: 397 obs (monthly, Jan 1982 – Jan 2015). Variables: gs10, gs1, dgs10, dgs1, date.

No supplementary datasets.

## Key Concepts deliberately not covered

| KC | Reason |
|---|---|
| 17.4 (Hausman test) | Partially covered by pooled vs FE widget; formal test is computational |
| 17.8 IV / Causal Inference | Narrative/conceptual — better suited to case study chapter |
| 17.9–17.11 Case study | Case study concepts — not interactive |

## Verified Numbers

| Metric | App | Source |
|---|---|---|
| NBA: 286 obs, 29 teams, 10 seasons | ✓ | Dataset |
| Pooled wins coef = 0.006753 | ✓ | Chapter |
| FE wins coef = 0.004505 | ✓ | Chapter |
| Cluster/default SE ratio = 1.81× | ✓ | Chapter |
| Between SD = 0.2127, within SD = 0.1085 | ✓ | Chapter |
| Levels R² = 0.9093, residual ACF1 = 0.977 | ✓ | Chapter |
| Changes R² = 0.5709, residual ACF1 = 0.255 | ✓ | Chapter |
| HAC/default SE ratio = 3.38× | ✓ | Chapter |
| ADL(2,2) R² = 0.3467, residual ACF1 = 0.024 | ✓ | Chapter |

## Verification

- [x] Build runs clean
- [x] Stats match chapter (all 9 sanity checks pass)
- [x] Verification script passes
- [x] 7 widget sections, 7 rerender hooks
- [x] File size: 62.4 KB (budget: 200 KB)
- [x] No leftover `{{...}}` placeholders
- [x] JSON data island parses
- [x] JS passes `node --check`
