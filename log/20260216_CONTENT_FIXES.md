# Notebook Content Audit and Fixes — 2026-02-16

## Summary

Performed a comprehensive content audit of all 18 notebooks (ch00–ch17) and fixed 4 verified issues affecting list rendering, markdown formatting, and JSON structure. Created an automated fix script for reproducibility.

## Issues Found and Fixed

| # | Issue | Count | Chapters |
|---|-------|-------|----------|
| 1 | Missing blank lines before lists | 426 | 16 chapters (all except CH00, CH05) |
| 2 | Significance asterisks rendered as bold/italic | 6 replacements | CH11 (cells 57, 71) |
| 3 | Empty markdown cells at end of notebooks | 19 cells removed | All 18 notebooks |
| 4 | Char-by-char source arrays in JSON | 12 notebooks normalized | CH06, CH08–CH17 |

### Issue 1: Missing Blank Lines Before Lists (Critical)

Pandoc/Quarto requires a blank line before markdown lists. Without it, lists render as plain text. This was the most critical issue, affecting 426 locations across 16 chapters.

Per-chapter breakdown:

- CH01: 8, CH02: 12, CH03: 10, CH04: 26, CH06: 11, CH07: 18
- CH08: 10, CH09: 11, CH10: 17, CH11: 32, CH12: 49, CH13: 55
- CH14: 13, CH15: 30, CH16: 63, CH17: 61

### Issue 2: Significance Asterisks in CH11

In CH11 cells 57 and 71, `*`, `**`, and `***` were used as statistical significance markers but were being interpreted as italic/bold by markdown. Fixed by wrapping in backticks (e.g., `` `***` for p < 0.01 ``).

### Issue 3: Empty Markdown Cells

Every notebook had 1 empty markdown cell at the end (CH01 had 2). These were trailing spacer cells with no content. All 19 removed.

### Issue 4: Char-by-Char JSON Source Arrays

12 notebooks (CH06, CH08–CH17) had corrupted JSON where cell source text was stored as individual characters instead of line arrays (caused by previous scripts using `json.dump` with single-string source). Fixed automatically by using `nbformat` for read/write, which normalizes the format.

## False Positives Dismissed

The audit initially flagged several issues that turned out to be false positives:

- **"Doubled words"** — All were header-then-paragraph patterns (e.g., `## Prediction` followed by `Prediction is a core application...`)
- **"Missing Colab badges"** — All chapters have them
- **"Missing visual summaries"** — All chapters have them
- **"Missing Key Takeaways/Exercises"** — All chapters have them (CH10: score 100, CH11: score 95)
- **"Concatenated words"** — All were proper nouns or filenames (EdCafe, CobbDouglas.DTA, PanelOLS)

## Fix Script

Created `scripts/fix_notebook_content.py` using `nbformat` (v5.10.4) for safe notebook I/O.

Usage:

```bash
python3 scripts/fix_notebook_content.py --dry-run          # Preview changes
python3 scripts/fix_notebook_content.py                    # Apply changes
python3 scripts/fix_notebook_content.py --dry-run ch16     # Single chapter
python3 scripts/fix_notebook_content.py --verbose          # Detailed output
```

## Verification

1. Dry-run after fix: 0 remaining issues across all 18 notebooks
2. All 18 notebooks pass `nbformat.validate()`
3. Quarto book re-rendered successfully (19/19 pages)

## Files Changed

- **New:** `scripts/fix_notebook_content.py`
- **Modified:** All 18 `notebooks_colab/ch*.ipynb`
- **Re-rendered:** All HTML in `book/_book/`
