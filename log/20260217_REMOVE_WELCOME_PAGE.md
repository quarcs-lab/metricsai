# Remove Welcome Page — Make Preface the Landing Page

**Date:** 2026-02-17
**Session focus:** Remove the separate "Welcome" page from the Quarto book

## Summary

Removed the standalone "Welcome" page (`index.qmd`) and replaced it with the full Preface content from `ch00_Preface.ipynb`. Readers now land directly on the Preface when opening the book.

## Changes Made

### 1. `book/_quarto.yml`

- Removed `notebooks_colab/ch00_Preface.ipynb` from the chapters list
- Page count: 19 → 18 (preface + ch01–ch17)

### 2. `book/index.qmd`

- Replaced 8-line Welcome page (cover image + description + PDF link) with full Preface content
- Converted all 15 markdown cells from ch00_Preface.ipynb to .qmd format
- Title: `# Preface {.unnumbered}`
- Image paths: Converted absolute GitHub URLs → local relative paths (`images/ch00_visual_summary.jpg`)
- Preserved: Colab badge, PDF download link (as blockquote), all Preface sections

### 3. `CLAUDE.md`

- Updated page count: "All 18 pages render successfully (preface + ch01–ch17)"

### 4. Book cover image in right sidebar TOC

- Added JavaScript injection via `include-after-body` in `_quarto.yml`
- Script inserts `book1cover.jpg` above the "Table of contents" in the right sidebar on every page
- Path detection: uses `../images/` for chapter pages, `images/` for index
- Added CSS styling in `custom.css` (`#toc-cover-image`): centered, rounded corners, subtle shadow, bottom border separator
- Hidden image reference in `index.qmd` forces Quarto to copy `book1cover.jpg` to `_book/images/`

### 5. `book/custom.css`

- Added `.hidden` class for Quarto resource inclusion
- Added `#toc-cover-image` styling (centered, rounded, shadow, border separator)

## What Was NOT Changed

- `notebooks_colab/ch00_Preface.ipynb` — preserved, still accessible via Colab badge
- All 17 chapter notebooks (ch01–ch17) — untouched
- Project website `index.html` — still links to `book/_book/index.html`

## Verification

- All 18 pages rendered successfully with `quarto render`
- Sidebar shows "Preface" as first entry (no "Welcome", no duplicate)
- "Next" navigation from Preface goes to Ch01
- Visual summary image renders at 65% width
- Colab badge links to correct notebook
- PDF download link present
- No `ch00_Preface.html` in output (content merged into `index.html`)
- `book1cover.jpg` present in `_book/images/`
- Cover image JS injection present in all chapter HTML files
