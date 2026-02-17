# Mobile TOC Button and Dark Theme Default

**Date:** 2026-02-17

## Summary

Made the Quarto book's mobile TOC accessible and set dark theme as the default.

## Changes

### 1. Dark Theme as Default

- Added `respect-user-color-scheme: false` to `book/_quarto.yml`
- Without this, Quarto follows the reader's OS preference (typically light)
- Now the book always opens in dark mode; the light/dark toggle remains available
- Quarto 1.8.27 supports this option (introduced in Quarto 1.7)

### 2. Mobile TOC: Nav Bar Button

**Problem:** The previous mobile TOC was a 52px floating circle at the bottom-right corner. In dark mode, it was nearly invisible (navy-on-navy with thin cyan border). Quarto has no native mobile TOC support ([open feature request #10187](https://github.com/quarto-dev/quarto-cli/discussions/10187)).

**Solution:** Replaced the floating button with a button in Quarto's secondary navigation bar (the top bar shown on mobile). The new button:

- Sits next to the existing sidebar toggle (hamburger icon) — immediately discoverable
- Uses Quarto's native `quarto-btn-toggle btn` classes — looks native
- Uses `bi-list-nested` Bootstrap icon — clearly indicates TOC
- Hidden on desktop (≥992px) where the right sidebar TOC is already visible
- Opens the same slide-in panel from the right with all page headings

**Files modified:**

- `book/_quarto.yml` — JS in `include-after-body`: replaced floating button creation with nav bar button injection into `.quarto-secondary-nav .container-fluid`
- `book/custom.css` — Replaced `.mobile-toc-btn` floating styles with `.mobile-toc-nav-btn` nav button styles

### 3. Case Study Data Fixes (from earlier in session)

- **CH06 cell 43:** `pd.read_stata("Convergence_clubs_2023.dta")` (404) → `pd.read_csv(url_mendez)` with correct columns `GDPpc`, `kl`
- **CH09 cells 41/46/48:** Column names `rk`→`kl`, `hc`→`h`
- **CH09 cells 44/46:** Converted from code to markdown (exercise blanks `_____` caused execution failures)
- Both notebooks re-executed and Quarto book re-rendered

## Current State

- All 18 chapters render successfully in Quarto book
- Dark theme is default, light toggle available
- Mobile TOC button visible in top nav bar on mobile devices
- Desktop sidebar toggles (floating chevrons) unchanged
