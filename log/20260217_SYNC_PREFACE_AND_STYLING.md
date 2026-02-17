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

### 7. Left Sidebar TOC Colors

- Part titles: SynapsePurple (`#7A209F`) with uppercase, letter-spacing, bottom border
- Chapter titles: ElectricCyan (`#008CB7`)
- Preface link: ElectricCyan (consistent with chapters)
- Active page: cyan left border + light background highlight

### 8. Comprehensive Visual Polish (10 areas)

- **Right TOC:** Card with gradient background, rounded corners, active section highlight
- **Page navigation:** Card-style prev/next buttons with hover effects
- **Title block:** Gradient background with cyan bottom border
- **Code output blocks:** Purple left border with light purple background
- **Sidebar active state:** Cyan left border + light background
- **Part titles:** Uppercase with letter-spacing and subtle bottom border
- **Visual summary hover:** Scale + shadow on mouse hover
- **Search box:** Cyan focus ring
- **Link underlines:** Animated bottom border on hover
- **List spacing:** Consistent vertical rhythm

### 9. Dark/Light Theme Toggle

- Added dual theme: `theme: { dark: darkly, light: cosmo }` in `_quarto.yml`
- Toggle button auto-generated in top-right navbar by Quarto
- User preference persisted via localStorage

### 10. Dark Mode Overrides (`custom.css`)

**Critical discovery:** Quarto 1.3.450 uses `body.quarto-dark` class (NOT `[data-bs-theme="dark"]` attribute). Initial implementation used wrong selector — all dark overrides were dead code. Fixed by replacing all `[data-bs-theme="dark"]` with `.quarto-dark` (35 selectors).

**Dark brand palette** (contrast-audited against `#222` darkly background):

| Element | Light Color | Dark Color | Contrast vs #222 |
|---------|-------------|------------|-------------------|
| H1 | `#008CB7` ElectricCyan | `#22d3ee` Bright Cyan | 9.2:1 |
| H2 | `#7A209F` SynapsePurple | `#c084fc` Bright Purple | 4.9:1 |
| H3 | `#C21E72` DataPink | `#f472b6` Bright Pink | 5.2:1 |
| H4 | `#0B1021` DeepNavy | `#f7fafc` Near-white | 15.3:1 |
| H5/H6 | inherited | `#e2e8f0` Light gray | 12.9:1 |
| Links | `#008CB7` | `#22d3ee` | 9.2:1 |
| Link hover | `#7A209F` | `#c084fc` | 4.9:1 |

**Dark surface colors:**

- Code blocks: `#1a1f2e` (solid dark blue-gray with cyan border)
- Code output: `#1e1a2e` (solid dark with purple tint)
- Tables: `rgba(0,140,183,0.15)` header bg, explicit `#e2e8f0` text
- Blockquotes: `rgba(122,32,159,0.15)` bg with light text
- Right TOC: subtle transparent bg with dim border
- Title block: subtle cyan-tinted bg

**Dark mode set as default** — dark theme listed first in `_quarto.yml`.

### 11. TOC h2 Specificity Fix

`#TOC h2` (ID specificity 1,0,1) was overriding `.quarto-dark h2` (class specificity 0,1,1). Added `.quarto-dark #TOC h2` override with bright purple + cyan border-bottom.

## Current Project Status

- **18 pages** render successfully (preface + ch01–ch17)
- **4 parts:** Statistical Foundations, Bivariate Regression, Multiple Regression, Advanced Topics
- **Dark mode** as default with light mode toggle available
- **Full dark mode styling** with contrast-audited brand colors
- **Google Translate** bar on every page (inlined in `_quarto.yml`)
- **Book cover** appears in right sidebar on every page
- **Visual styling** applied across all pages (headings, code, tables, blockquotes, sidebar, TOC, navigation)
- Deployed to GitHub Pages: `https://quarcs-lab.github.io/metricsai/book/_book/index.html`

## Files Modified

| File | Changes |
|------|---------|
| `book/_quarto.yml` | Removed ch00, added cover image JS, updated date/date-format, Google Translate, dual theme (dark default) |
| `book/index.qmd` | Replaced Welcome with Preface content, synced 3 times |
| `book/custom.css` | Full visual styling: headings, code, tables, blockquotes, sidebar, TOC, navigation, dark mode overrides (35 selectors) |
| `CLAUDE.md` | Updated page count (18 pages) |
