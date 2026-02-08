# DS4Bolivia Case Studies + Book Recompilation (2026-02-08)

## Summary

Added a second case study (DS4Bolivia) to 12 chapters, regenerated all 18 chapter PDFs, added a copyright page, and recompiled the complete book.

## DS4Bolivia Case Studies

### Dataset

- **URL**: `https://raw.githubusercontent.com/quarcs-lab/ds4bolivia/master/ds4bolivia_v20250523.csv`
- **Source**: DS4Bolivia project (https://github.com/quarcs-lab/ds4bolivia)
- **Observations**: 339 Bolivian municipalities
- **Key variables**: `imds` (development index), `ln_NTLpc2017` (nighttime lights), `dep` (department), `pop2017`, `A00-A63` (satellite embeddings), SDG indices
- **Overarching theme**: "Can Satellites See Development? Using Remote Sensing to Predict Local Economic Development in Bolivia"

### Chapters Modified (12)

| Chapter | Case Study 2 Title | New Key Concepts |
|---------|-------------------|-----------------|
| CH01 | Can Satellites See Poverty? Predicting Local Development in Bolivia | 1.9, 1.10 |
| CH02 | The Geography of Development: Summarizing Bolivia's Municipal SDG Data | 2.10, 2.11 |
| CH04 | Is Bolivia's Development Equal? Testing Differences Across Departments | 4.12, 4.13 |
| CH05 | Nighttime Lights and Development: A Bivariate Exploration | 5.11, 5.12 |
| CH07 | Is the Light-Development Relationship Significant? | 7.12, 7.13 |
| CH10 | Multiple Satellite Predictors of Development | 10.12, 10.13 |
| CH11 | Which Satellite Features Matter? Joint Tests for Predictive Power | 11.12, 11.13 |
| CH12 | Robust Prediction of Municipal Development | 12.11, 12.12 |
| CH14 | Urban-Rural and Regional Divides in Bolivian Development | 14.9, 14.10 |
| CH15 | Nonlinear Satellite-Development Relationships | 15.11, 15.12 |
| CH16 | Diagnosing the Satellite Prediction Model | 16.11, 16.12 |
| CH17 | Luminosity and Development Over Time: A Panel Approach | 17.10, 17.11 |

### Case Study Structure (per chapter)

- 6 tasks: Tasks 1-2 (Guided), Tasks 3-4 (Semi-guided), Tasks 5-6 (Independent)
- 2 new Key Concepts per case study
- "What You've Learned" summary section
- CH01 provides comprehensive DS4Bolivia introduction; other chapters reference it

### Implementation

- 12 Python scripts created in `scripts/add_ds4bolivia_chXX.py`
- Each script inserts cells into notebook JSON after existing Case Study 1
- Existing case studies renamed from "Case Study:" to "Case Study 1:"

## Copyright Page

Added to `scripts/compile_book.py`:
- `generate_copyright_html()` function renders centered copyright info
- Inserted between cover page and Brief Contents
- Content: Title, copyright notice (Carlos Mendez, 2026), affiliation (Nagoya University), companion website

## PDF Regeneration

All 18 chapter PDFs regenerated via 3-step pipeline:
1. `jupyter nbconvert --to html` (all notebooks)
2. `inject_print_css.py` (inject print styles)
3. `generate_pdf_playwright.py --all` (render PDFs)

### Chapter Page Changes

| Chapter | Old Pages | New Pages | Change |
|---------|-----------|-----------|--------|
| ch00 | 15 | 15 | -- |
| ch01 | 28 | 37 | +9 |
| ch02 | 54 | 62 | +8 |
| ch03 | 41 | 41 | -- |
| ch04 | 51 | 58 | +7 |
| ch05 | 56 | 64 | +8 |
| ch06 | 39 | 39 | -- |
| ch07 | 66 | 72 | +6 |
| ch08 | 41 | 41 | -- |
| ch09 | 37 | 37 | -- |
| ch10 | 32 | 40 | +8 |
| ch11 | 47 | 54 | +7 |
| ch12 | 40 | 48 | +8 |
| ch13 | 63 | 63 | -- |
| ch14 | 39 | 45 | +6 |
| ch15 | 48 | 54 | +6 |
| ch16 | 51 | 59 | +8 |
| ch17 | 53 | 59 | +6 |
| **Total** | **801** | **888** | **+87** |

## Compiled Book Stats

| Metric | Old | New |
|--------|-----|-----|
| Total pages | 811 | 900 |
| Content pages | 801 | 888 |
| Front matter | 10 | 12 |
| Key Concepts | 165 | 189 |
| Key Concepts TOC pages | 4 | 5 |
| File size | 57.3 MB | 62.3 MB |
| Clickable TOC links | ~870 | 753 |
| Sections in bookmarks | 110 | 110 |

### Book Structure (updated)

```
metricsAI_complete_book.pdf (900 pages, 62.3 MB)
├── Cover page (1 page, unnumbered)
├── Copyright page (1 page, unnumbered) [NEW]
├── Brief Contents (1 page, unnumbered, clickable)
├── Detailed Contents (4 pages, unnumbered, clickable)
├── Key Concepts (5 pages, unnumbered, clickable)
└── Content (888 pages, numbered 1-888)
```

## Next Steps

- Commit all changes
- The textbook is publication-ready with dual case studies, copyright page, and updated compilation
