# Heading Structure and Content Placement Audit — 2026-02-17

## Summary

Performed two major improvements across all 17 content chapters (CH01-CH17):

1. **Heading structure cleanup** — Demoted 145 non-numbered mid-content `##` headings to `###` so only numbered sections and structural headings appear in the Quarto TOC. Removed section numbers from Case Studies headings in 5 chapters.
2. **Content placement audit** — Audited all 17 chapters for misplaced cells, missing sections, duplicate content, and structural heading issues. Fixed 12 chapters; 5 were clean.

## Heading Structure Changes

### Mid-Content Heading Demotion

Created `scripts/demote_mid_content_headings.py` to classify `##` headings as:

- **Keep at `##`**: Section-numbered (e.g., `## 5.3`) or structural (Chapter Overview, Setup, Key Takeaways, Practice Exercises, Case Studies)
- **Demote to `###`**: All other mid-content descriptive headings

The script also cascades sub-headings within demoted zones (`###` → `####`, `####` → `#####`).

**Result:** 145 heading changes across 11 chapters (CH04, CH06, CH07, CH09-CH12, CH14-CH17).

### Case Studies Heading Unnumbering

Removed section numbers from Case Studies headings in 5 chapters:

- CH01: `## 1.11 Case Studies` → `## Case Studies`
- CH02: `## 2.8 Case Studies` → `## Case Studies`
- CH03: `## 3.9 Case Studies` → `## Case Studies`
- CH06: `## 6.5 Case Studies` → `## Case Studies`
- CH07: `## 7.8 Case Studies` → `## Case Studies`

## Content Placement Audit Results

### CH01-CH04

| Chapter | Issue | Fix |
|---------|-------|-----|
| CH01 | Chapter Overview listed "1.10 Practice Exercises", "1.11 Case Studies" | Removed section numbers |
| CH02 | Chapter Overview listed "2.7 Practice Exercises", "2.8 Case Studies" | Removed section numbers |
| CH03 | Missing section 3.6; numbering jumped 3.5→3.7→3.8 | Renamed 3.8→3.6, reordered to 3.5→3.6→3.7, updated overview |
| CH04 | Missing `## Case Studies` header; Case Study 2 at H4 instead of H3 | Added header; promoted 9 headings in Case Study 2 |

### CH05-CH09

| Chapter | Issue | Fix |
|---------|-------|-----|
| CH05 | "When to Use Nonparametric vs Parametric" cell under 5.10 (Causation) | Moved to section 5.11 (Nonparametric Regression) |
| CH06 | Duplicate "Interpreting Manual SE Calculations" cell; Chapter Overview had numbered back matter in wrong order | Removed duplicate; fixed overview |
| CH07 | 7 cells of hypothesis testing content (KCs 7.3-7.5 + 3 subsections) under section 7.3 (Confidence Intervals) | Moved all to section 7.4 (Tests of Statistical Significance) |
| CH08 | Clean | — |
| CH09 | Clean | — |

### CH10-CH13

| Chapter | Issue | Fix |
|---------|-------|-----|
| CH10 | Clean | — |
| CH11 | 2 F-test cells ("Overall F-test", "Joint Test of Subset") under 11.4 (single parameter tests) | Moved to section 11.5 (joint hypothesis tests) |
| CH12 | Missing section 12.1; misordered cells between 12.6/12.7 | Added "12.1: Example - House Price Prediction"; swapped cells |
| CH13 | Clean | — |

### CH14-CH17

| Chapter | Issue | Fix |
|---------|-------|-----|
| CH14 | 2 cells (worker-type indicator code + Dummy Variable Trap KC) under 14.4 (Structural Change) | Moved to section 14.5 (Sets of Indicator Variables) |
| CH15 | Missing section 15.1; sections 15.6/15.7 at wrong heading level | Added "15.1: Example - Earnings and Education"; promoted 15.6/15.7 to `##` |
| CH16 | Clean | — |
| CH17 | Clean | — |

## Files Changed

- **New:** `scripts/demote_mid_content_headings.py`
- **Modified:** 15 notebooks — CH01-CH07, CH09-CH12, CH14-CH17
- **Re-rendered:** All HTML in `book/_book/`

## Verification

- All 19 Quarto pages render successfully
- Section structure verified per chapter after each fix
- No content lost — all changes are cell moves, heading renames, or structural header additions
