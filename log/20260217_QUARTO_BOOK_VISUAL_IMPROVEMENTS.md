# Quarto Book Visual Improvements — 2026-02-17

## Summary

Comprehensive visual improvements to the Quarto HTML book (`book/`), including branded styling, chapter title renaming, Key Concept enhancement, and resource buttons for all 17 chapters.

## Changes Made

### 1. Visual Summary Images — Full Width

Made chapter visual summary images span the full page width with decorative styling.

- **CSS selector:** `img[alt*="Visual Summary"]`
- **Styling:** `width: 100%`, cyan border (#008CB7), 8px border-radius, drop shadow
- **File:** `book/custom.css`

### 2. Heading Colors — Brand Palette

Applied the book's brand color palette to all heading levels:

| Level | Color | Name |
|-------|-------|------|
| H1 | #008CB7 | ElectricCyan + bottom border |
| H2 | #7A209F | SynapsePurple + left border |
| H3 | #C21E72 | DataPink |
| H4 | #0B1021 | DeepNavy |

### 3. Comprehensive Styling Additions

Added to `book/custom.css`:

- **Code blocks:** Light background with cyan left border
- **Inline code:** Gray background, rounded corners
- **Tables:** Light header with cyan bottom border, alternating row colors
- **Blockquotes/Key Concepts:** Purple left border, lavender background
- **List markers:** Cyan (unordered), purple (ordered)
- **Links:** Cyan default, purple hover
- **Output images:** Centered, no borders

Added to `book/_quarto.yml`:

- `code-copy: hover`, `code-overflow: wrap`, `highlight-style: github`
- `smooth-scroll: true`, `anchor-sections: true`
- `link-external-icon: true`, `link-external-newwindow: true`
- `fontsize: 1.05em`, `linestretch: 1.6`
- `mainfont: "Inter"`, `monofont: "JetBrains Mono"`
- Google Fonts `@import` in `custom.css` (Quarto's `mainfont` doesn't load fonts)

### 4. TOC Collapse Fix

Quarto's new rendering options caused chapter-level TOC entries to use Bootstrap's `collapse` class (hidden by default).

- **Fix:** Added `#TOC > ul { display: block !important; }` to `custom.css`
- **Root cause:** Bootstrap 5 `collapse` class sets `display: none` unless JS adds `.show`

### 5. Chapter Title Renaming

Renamed all chapter H1 headings from `# Chapter X: Title` to `# X. Title`:

- **Scope:** 17 notebooks (ch01–ch17)
- **CH00:** Renamed from `# Preface: Econometrics Powered by AI` to `# Preface`
- **Method:** Python script using `json` module to modify cell 0 in each notebook

### 6. Key Concept Styling Enhancement

Enhanced the visual differentiation between Key Concept titles and body text:

- **Title** (`blockquote strong`): SynapsePurple (#7A209F), `font-size: 1.05em`
- **Body text** (`blockquote color`): Dark slate blue (#1a365d) with `!important` to override Bootstrap
- **File:** `book/custom.css` lines 94–108

### 7. Resource Buttons (AI Video, AI Slides, Cameron Slides, Quiz, AI Tutor)

Added 5 clickable resource buttons below the Colab badge in every chapter (ch01–ch17), matching the project website's functionality.

- **Buttons:** AI Video (YouTube), AI Slides (Canva), Cameron Slides, Quiz (EdCafe), AI Tutor (EdCafe)
- **Icons:** Emoji (🎬 ✨ 📊 ✏️ 🤖) — no CDN dependency
- **Styling:** Rounded pill buttons, ElectricCyan text, solid fill on hover
- **Script:** `scripts/add_resource_buttons.py` — contains all 17 chapter URL data
- **CSS:** `.chapter-resources` (flex container) + `.resource-btn` (pill buttons)

### 8. Colab Badge Centering Fix (CH03, CH04)

CH03 and CH04 had a trailing `\n` on the Colab badge markdown line, causing Pandoc to wrap the badge in a centered `<figure>` element. All other chapters had the badge inline (left-aligned).

- **Fix:** Stripped trailing `\n` from the badge line in both notebooks
- **Root cause:** A standalone markdown image paragraph (blank line before and after) triggers Pandoc's implicit figure behavior

## Files Changed

### New Files

- `scripts/add_resource_buttons.py` — Automation script with URL data for all 17 chapters

### Modified Files

- `book/custom.css` — Expanded from ~17 lines to ~163 lines (full styling)
- `book/_quarto.yml` — Added formatting options (code, fonts, navigation, etc.)
- `notebooks_colab/ch00_Preface.ipynb` — Title simplified
- `notebooks_colab/ch01–ch17_*.ipynb` — Titles renamed + resource buttons added
- `notebooks_colab/ch03_The_Sample_Mean.ipynb` — Badge newline fix
- `notebooks_colab/ch04_Statistical_Inference_for_the_Mean.ipynb` — Badge newline fix

### Re-rendered

- All HTML in `book/_book/` (19 pages: welcome + ch00–ch17)

## CSS Architecture (`book/custom.css`)

```
Lines   1–2:   Google Fonts @import (Inter, JetBrains Mono)
Lines   4–7:   TOC collapse fix
Lines   9–24:  Colab badge left-alignment
Lines  26–34:  Visual summary full-width styling
Lines  36–59:  Heading colors (H1–H4 brand palette)
Lines  61–82:  Code blocks and inline code
Lines  84–92:  Tables
Lines  94–108: Blockquotes / Key Concepts (title + body colors)
Lines 110–118: List markers
Lines 120–127: Links
Lines 129–157: Chapter resource buttons
Lines 159–163: Output images
```

## Verification

- All 19 Quarto pages render successfully
- Resource buttons link to correct chapter-specific URLs
- Colab badges left-aligned in all chapters
- Key Concepts show purple titles and dark slate blue body text
- TOC visible in all chapters
