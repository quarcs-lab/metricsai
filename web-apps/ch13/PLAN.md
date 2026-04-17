# Chapter 13: Case Studies for Multiple Regression — Dashboard Plan

## Context

Chapter 13 is an integrated case study chapter where sections 13.1–13.9 ARE the case studies, each demonstrating a different econometric technique. This dashboard makes 6 of the 9 case studies interactive, covering production functions, omitted variables bias, and four causal inference designs (RCT, DiD, RD, IV).

## Design decisions

- Charts: Plotly.js 2.35.2
- Data: 6 datasets pre-computed; raw scatter data for small datasets, pre-computed summaries for large ones
- Theming: light + dark toggle with localStorage persistence
- Scope: Key Concepts 13.2–13.5 and 13.7–13.10

## Widgets

| # | Widget | Key Concept | Dataset | Target interaction |
|---|---|---|---|---|
| 1 | Cobb-Douglas production function | KC 13.2, 13.3 | AED_COBBDOUGLAS (n=24) | Actual vs predicted output; elasticity readouts; CRS test |
| 2 | Phillips curve & OVB | KC 13.4, 13.5 | AED_PHILLIPS (n=66) | Toggle pre/post 1970; OVB formula |
| 3 | RAND Insurance (RCT) | KC 13.7 | AED_HEALTHINSEXP (n=5,639) | Bar chart by plan; F-test |
| 4 | DiD: Health clinic access | KC 13.8 | AED_HEALTHACCESS (n=1,071) | 2×2 table; DiD visual |
| 5 | RD: Incumbency advantage | KC 13.9 | AED_INCUMBENCY (n=1,297) | Toggle binned/raw scatter; threshold jump |
| 6 | IV: Institutions & GDP | KC 13.10 | AED_INSTITUTIONS (n=64) | Toggle OLS/first stage/IV scatter |

## Data

6 datasets, all from AED collection (local .DTA files):
- AED_COBBDOUGLAS.DTA: 24 years US manufacturing (1899–1922)
- AED_PHILLIPS.DTA: 66 years US macro (1949–2014)
- AED_HEALTHINSEXP.DTA: 5,639 person-years (RAND experiment, year 1)
- AED_HEALTHACCESS.DTA: 1,071 South African children
- AED_INCUMBENCY.DTA: 1,297 US Senate elections (1914–2010)
- AED_INSTITUTIONS.DTA: 64 former colonies

No supplementary datasets.

## Key Concepts deliberately not covered

| KC | Reason |
|---|---|
| 13.1 Multiple Regression & Socioeconomic | Similar to ch10 regression builder |
| 13.6 Cluster-Robust SEs | Covered in ch17 cluster widget |
| 13.9 Data Preparation | Non-interactive (file I/O, merging) |

## Verified Numbers

| Metric | App | Match |
|---|---|---|
| Cobb-Douglas: α=0.2331, β=0.8073, sum=1.04, CRS p=0.61 | ✓ |
| Phillips pre-1970: coef=−1.03, post: +0.27 | ✓ |
| RAND F=11.39, p<0.001, n=5,639 | ✓ |
| DiD=0.52 SD, p=0.027, CI=[0.06, 0.98] | ✓ |
| RD win=4.8 pp, CI=[3.1, 6.5], n=1,297 | ✓ |
| IV: OLS=0.52, IV=0.94, 1st stage F=16.3 | ✓ |

## Verification

- [x] Build runs clean
- [x] All sanity checks pass
- [x] Verification script passes
- [x] 6 widget sections, 6 rerender hooks
- [x] File size: 57.9 KB (budget: 200 KB)
- [x] No leftover `{{...}}` placeholders
- [x] JSON data island parses
- [x] JS passes `node --check`
