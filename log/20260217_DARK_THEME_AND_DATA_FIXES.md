# Dark Theme Application and Case Study Data Fixes

**Date:** 2026-02-17

## Summary

Applied a dark theme to all chapter notebooks (CH01-CH17) matching the Quarto book design, and fixed broken case study data loading in CH06 and CH09.

## Dark Theme

### Script: `scripts/apply_dark_theme.py`

New script that automates dark theme application across notebooks. Handles:

- **Setup cell replacement:** `whitegrid` → `dark_background` + custom rcParams
- **Color replacements:** context-aware substitutions for visibility on dark backgrounds
  - `color='black'`/`'navy'`/`'darkblue'` → `#22d3ee` (cyan) for data points
  - `color='blue'` → `#c084fc` (purple) for fitted/regression lines
  - `edgecolor='black'` → `#3a4a6b` (grid color)
  - `facecolor='wheat'` → `#1e2a45` (dark box)
  - `color='darkgreen'` → `#4ade80` (light green)
  - `axhline`/`axvline` with black/blue → white with alpha=0.3
  - `'b-'`/`'b--'` format strings → explicit `color='#c084fc'`

### Color palette

| Element | Color | Hex |
|---------|-------|-----|
| Page background | Dark navy | `#12162c` |
| Axes background | Navy | `#1a2235` |
| Grid lines | Muted blue | `#3a4a6b` |
| Data points (cyan) | Electric cyan | `#22d3ee` |
| Fitted lines (purple) | Soft purple | `#c084fc` |
| Light green | Bright green | `#4ade80` |

### Chapters processed

- CH01-CH02: Dark theme applied manually in earlier session
- CH03-CH17: Dark theme applied via `scripts/apply_dark_theme.py`
- All 17 notebooks re-executed to regenerate figures with dark backgrounds

## Case Study Data Fixes

### CH06: `Convergence_clubs_2023.dta` → CSV

**Problem:** Cell 43 loaded a non-existent `.dta` file from `GITHUB_DATA_URL`, causing a 404 error. Also referenced columns `rgdppc` and `rk` which don't exist.

**Fix:**

- Changed `pd.read_stata(GITHUB_DATA_URL + "Convergence_clubs_2023.dta")` → `pd.read_csv(url_mendez)` using the working Mendez CSV URL
- Column mapping: `rgdppc` → `GDPpc`, `rk` → `kl` (capital per worker = K/L)
- Downstream cells (44-49) are markdown templates — no changes needed

### CH09: Wrong column names + exercise cells as code

**Problem:** Cells 41, 46, 48 referenced non-existent columns `rk` and `hc`. Cells 44 and 46 were code cells with `_____` exercise blanks that caused execution failures.

**Fix — Column names:**

- Cell 41: `['lp', 'rk', 'hc']` → `['lp', 'kl', 'h']`
- Cell 46: `model_hc.params['hc']` → `model_hc.params['h']`
- Cell 48: All `rk` → `kl` and `ln_rk` → `ln_kl` in model formulas

**Fix — Cell types:**

- Cells 44 and 46: Converted from `code` to `markdown` with ```python fences
- These are exercise templates with `_____` blanks — not meant to be executed

### Mendez CSV column reference

The actual CSV at `https://raw.githubusercontent.com/quarcs-lab/mendez2020-convergence-clubs-code-data/master/assets/dat.csv` has columns:

```
id, country, year, Y, K, pop, L, s, alpha_it, GDPpc, lp, h, kl, kp, ky, TFP,
log_GDPpc_raw, log_lp_raw, log_ky_raw, log_h_raw, log_tfp_raw,
log_GDPpc, log_lp, log_ky, log_h, log_tfp, isocode, hi1990, region
```

Key mappings for case studies: `rgdppc` → `GDPpc`, `rk` → `kl`, `hc` → `h`

## Quarto Book

Re-rendered all 18/18 chapters with dark-themed figures. All chapters confirmed showing dark navy backgrounds with the book color palette.

## Files Modified

- `scripts/apply_dark_theme.py` (new)
- `notebooks_colab/ch01_*.ipynb` through `ch17_*.ipynb` (all 17 chapters)
- `book/_quarto.yml`, `book/custom.css`
- `book/_book/` (all rendered HTML and figure PNGs)
