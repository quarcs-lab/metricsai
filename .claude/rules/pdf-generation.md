---
description: PDF generation workflow using Playwright
globs:
  - scripts/generate_pdf_playwright.py
  - scripts/inject_print_css.py
  - scripts/notebook_pdf_styles.css
  - notebooks_colab/*.html
---

# PDF Generation Workflow

The project uses an automated Playwright-based pipeline to generate professional-quality PDFs from Jupyter notebooks.

## Why Playwright?

- Precise control over margins, no unwanted headers/footers
- Consistent, reproducible output across all chapters
- Full support for modern CSS (justified text, full-width images)
- Proper Google Fonts integration (Inter, JetBrains Mono)
- Single chapter or batch mode with one command

## Pipeline

```
jupyter nbconvert --to html  →  inject_print_css.py  →  generate_pdf_playwright.py
     (notebook.ipynb)           (adds custom CSS)         (renders PDF via Chromium)
```

IMPORTANT: All 3 steps must run in order. Skipping `inject_print_css` produces PDFs with stale styling.

## Quick Reference

**Single chapter:**

```bash
cd notebooks_colab && jupyter nbconvert --to html ch05_*.ipynb && cd ..
python3 scripts/inject_print_css.py notebooks_colab/ch05_*.html notebooks_colab/ch05_*_printable.html
python3 scripts/generate_pdf_playwright.py ch05
```

**All chapters:**

```bash
cd notebooks_colab && for nb in ch*.ipynb; do jupyter nbconvert --to html "$nb"; done && cd ..
python3 scripts/generate_pdf_playwright.py --all
```

## Key System Files

1. **`scripts/generate_pdf_playwright.py`** - Primary PDF generator
   - Uses Playwright Chromium for rendering
   - Letter format (8.5" x 11"), 0.75" margins, no headers/footers
   - Supports `ch05` (single) or `--all` (batch)

2. **`scripts/inject_print_css.py`** - CSS injection tool
   - Injects styles from `scripts/notebook_pdf_styles.css` into HTML
   - Creates `_printable.html` versions ready for PDF generation
   - Uses `Path(__file__).parent` to resolve CSS path (works from any directory)

3. **`scripts/notebook_pdf_styles.css`** - Master stylesheet
   - Justified text via `@media print` rules
   - Font sizes: 11pt body (Inter), 9pt input code (JetBrains Mono), 7.5pt output/tables
   - Full-width visual summaries: `width: 100% !important`
   - 0.75in uniform margins via `@page` rule

## Professional Formatting Features

**Typography:**

- Justified text alignment (book-style)
- Body: 11pt Inter | Input code: 9pt JetBrains Mono | Output/tables: 7.5pt JetBrains Mono

**Layout:**

- Letter portrait, 0.75" margins, no headers/footers
- Full-width visual summaries (7" span within margins)

**Visual Design:**

- Brand colors: ElectricCyan (#008CB7), SynapsePurple (#7A209F), DataPink (#C21E72)
- Code blocks: light blue-gray background with cyan left border
- Tables: light blue headers with alternating row colors

**Technical Quality:**

- Clickable hyperlinks preserved
- Regression tables fit without wrapping (7.5pt)
- LaTeX equations render correctly
- All figures preserved at high resolution

## Critical CSS Settings

**Justified text** (in `notebook_pdf_styles.css`):

```css
@media print {
    p { text-align: justify !important; }
    .text_cell_render { text-align: justify !important; }
    blockquote { text-align: justify !important; }
    li { text-align: justify !important; }
}
```

**Full-width visual summaries:**

```css
img[alt*="Visual Summary"] {
    width: 100% !important;
}
```

**Output font sizes (prevents table overflow):**

```css
pre { font-size: 7.5pt !important; }
.output_text, .output_html { font-size: 7.5pt !important; }
.dataframe, .simpletable { font-size: 7.5pt !important; }
```

## Prerequisites

```bash
pip install playwright
playwright install chromium
python3 -c "from playwright.sync_api import sync_playwright; print('OK')"
```

## Troubleshooting

| Issue | Cause | Fix |
| --- | --- | --- |
| Regression tables wrap | Output font too large | Verify `pre`, `.output_text`, `.simpletable` at 7.5pt |
| Visual summaries not full width | Missing CSS override | Verify `img[alt*="Visual Summary"]` has `width: 100% !important` |
| Text not justified | Rules outside `@media print` | Verify justified rules inside `@media print` with `!important` |
| Headers/footers visible | Outdated generator script | Verify `display_header_footer=False` in generator |
| Playwright not installed | Missing dependency | Run `pip install playwright && playwright install chromium` |

## Compiled Book

Use `scripts/compile_book.py` to merge all chapter PDFs into a single book with:

- Cover page, copyright page, Brief Contents, Detailed Contents
- Key Concepts table of contents
- Clickable TOC hyperlinks and page numbers
- Section-level PDF bookmarks

## Complete Documentation

For the full 600+ line workflow reference: [log/20260129_PDF_GENERATION_WORKFLOW.md](../../log/20260129_PDF_GENERATION_WORKFLOW.md)
