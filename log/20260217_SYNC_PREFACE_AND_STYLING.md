# Preface Sync & Book Styling Updates

**Date:** 2026-02-17

## Summary

This session made the Preface the book's landing page, added visual styling (heading colors, code blocks, cover image in sidebar), and synced preface content through multiple notebook revisions.

## Changes Made

### 1. Removed Welcome Page — Preface as Landing Page

- Replaced `book/index.qmd` Welcome page content with full Preface from `ch00_Preface.ipynb`
- Removed `ch00_Preface.ipynb` from `_quarto.yml` chapters list (19 → 18 pages)
- Converted all 15 markdown cells to `.qmd` format with local image paths

### 2. Book Cover in Right Sidebar

- Added JavaScript injection via `include-after-body` in `_quarto.yml`
- Inserts `book1cover.jpg` above TOC on every page
- Path detection: `../images/` for chapter pages, `images/` for index
- Hidden image reference in `index.qmd` forces Quarto to copy `book1cover.jpg` to `_book/`
- CSS styling: centered, rounded corners, subtle shadow, bottom border separator

### 3. Visual Styling (`custom.css`)

- **Heading colors:** H1 ElectricCyan (#008CB7), H2 SynapsePurple (#7A209F), H3 DataPink (#C21E72), H4 DeepNavy (#0B1021)
- **Code blocks:** Cyan left border with light background
- **Tables:** Cyan header borders, alternating row colors
- **Blockquotes:** Purple left border with light purple background
- **Links:** Cyan default, purple on hover
- **Resource buttons:** Pill-shaped with cyan theme
- **Visual summary images:** Full-width, cyan border, rounded corners, shadow
- **Fonts:** Inter (body), JetBrains Mono (code) via Google Fonts
- **Colab badges:** Left-aligned, hidden figcaptions

### 4. Preface Content Syncs (3 rounds)

Round 1: Removed title/subtitle/author/Colab badge, removed "Introduction" heading, promoted headings to H2, removed "Customize Your Learning!" section.

Round 2: Updated opening text to "Welcome to *Econometrics Powered by AI*!", changed "foundational statistical concepts" → "foundational econometric concepts".

Round 3 (final): Changed formatting to bold with quotes `**Welcome to "Econometrics Powered by AI"!**`, shortened "rigor of traditional econometric theory" → "rigor of econometrics".

### 5. Hidden Elements (CSS)

- `#preface > h1 { display: none; }` — hides "Preface" title on landing page
- Visual summary image: removed alt text to prevent Quarto figcaption generation
- CSS selector changed from `img[alt*="Visual Summary"]` to `img[src*="visual_summary"]`

### 6. Date Update

- `date: "2026-02-17"` with `date-format: "MMMM D, YYYY [(in progress)]"`
- Renders as "February 17, 2026 (in progress)"

## Current Project Status

- **18 pages** render successfully (preface + ch01–ch17)
- **4 parts:** Statistical Foundations, Bivariate Regression, Multiple Regression, Advanced Topics
- **Google Translate** bar on every page (inlined in `_quarto.yml`)
- **Book cover** appears in right sidebar on every page
- **Visual styling** applied across all pages (headings, code, tables, blockquotes)
- Deployed to GitHub Pages: `https://quarcs-lab.github.io/metricsai/book/_book/index.html`

## Files Modified

| File | Changes |
|------|---------|
| `book/_quarto.yml` | Removed ch00, added cover image JS, updated date/date-format, added Google Translate |
| `book/index.qmd` | Replaced Welcome with Preface content, synced 3 times |
| `book/custom.css` | Added heading colors, code/table/blockquote styling, cover image, hidden elements |
| `CLAUDE.md` | Updated page count (18 pages) |
