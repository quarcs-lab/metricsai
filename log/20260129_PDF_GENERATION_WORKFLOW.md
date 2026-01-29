# PDF Generation Workflow Documentation

**Date:** 2026-01-29
**Purpose:** Complete documentation of the PDF generation system for Jupyter notebooks
**Status:** Production-ready workflow established

---

## Table of Contents

1. [Overview](#overview)
2. [System Components](#system-components)
3. [PDF Formatting Features](#pdf-formatting-features)
4. [Complete Workflow](#complete-workflow)
5. [Generating Individual Chapters](#generating-individual-chapters)
6. [Generating All Chapters](#generating-all-chapters)
7. [Troubleshooting](#troubleshooting)
8. [Technical Details](#technical-details)

---

## Overview

This document describes the complete workflow for generating professional PDF files from Jupyter notebooks. The system converts notebooks to HTML, injects custom CSS styling, and generates PDFs using Playwright with precise formatting control.

**Key Benefits:**
- Automated PDF generation from Jupyter notebooks
- Professional typography and layout
- Consistent formatting across all chapters
- Full-width visual summary images
- Properly sized regression tables
- Clickable hyperlinks (no printed URLs)

---

## System Components

### 1. Core Scripts

**`generate_pdf_playwright.py`** (248 lines)
- Primary PDF generation tool using Playwright
- Provides precise control over margins, headers/footers
- Handles font loading and rendering
- Location: Project root directory

**`inject_print_css.py`** (working correctly, unchanged)
- Injects custom CSS into HTML files
- Creates "_printable.html" versions
- Location: Project root directory

**`notebook_pdf_styles.css`** (426 lines)
- Master stylesheet for PDF formatting
- Controls all typography, colors, spacing
- Location: Project root directory

### 2. Supporting Scripts (Optional)

**`generate_pdf.py`** (Chrome headless version)
- Alternative using Chrome instead of Playwright
- Less reliable than Playwright version
- Use only if Playwright unavailable

**`verify_dollar_signs.py`** (143 lines)
- Verification tool for currency escaping
- Run before/after currency fixes
- Location: Project root directory

**`fix_currency_dollars.py`** (130 lines)
- Automated currency dollar sign escaping
- Already applied to all notebooks
- Location: Project root directory

---

## PDF Formatting Features

### Typography

**Font Hierarchy:**
- Body text: 11pt with justified alignment
- Headings: 16pt (h1) down to 10pt (h6)
- Input code: 9pt monospace (JetBrains Mono)
- Output text: 7.5pt monospace (regression tables, print statements)
- Tables: 7.5pt with compact padding

**Font Families:**
- Body: 'Inter', sans-serif (Google Fonts)
- Code: 'JetBrains Mono', monospace (Google Fonts)

**Text Alignment:**
- Body paragraphs: Justified
- List items: Justified
- Blockquotes: Justified
- Headings: Left-aligned
- Code: Left-aligned (monospace)

### Page Layout

**Page Size:** Letter (8.5" × 11")
**Orientation:** Portrait
**Margins:** 0.75 inches on all sides (uniform)
**Headers/Footers:** None (explicitly disabled)

### Visual Elements

**Visual Summary Images:**
- Width: 100% (full width within margins = 7 inches)
- Border: 2px solid cyan (#008CB7)
- Shadow: Soft drop shadow for depth
- Border radius: 8px rounded corners
- Centered with proper vertical spacing

**Code Blocks:**
- Background: Light blue-gray (#f7fafc)
- Border: 3px left border in cyan (#008CB7)
- Padding: Extra left padding for alignment
- Border radius: 4px

**Tables:**
- Header background: Light blue (#e1ebf5)
- Alternating row colors for readability
- Font size: 7.5pt (prevents overflow)
- Cell padding: 2px 5px (compact)

**Blockquotes:**
- Left border: 4px solid purple (#7A209F)
- Background: Light purple (#faf5ff)
- Italic text with justified alignment

### Colors (Brand Identity)

- **ElectricCyan:** #4DF2FE (primary accent)
- **SynapsePurple:** #7A209F (secondary accent)
- **DataPink:** #FE4DD5 (tertiary accent)
- **DeepNavy:** #0B1021 (primary text)

### Special Fixes Applied

1. **Currency Dollar Signs:** All 485 instances across 15 notebooks escaped as `\$` to prevent LaTeX rendering
2. **Reduced Output Font Size:** From 9pt to 7.5pt to prevent regression table overflow
3. **No Printed URLs:** Hyperlinks remain clickable but URLs don't print as text
4. **Full-Width Visual Summaries:** Override inline HTML width attributes via CSS

---

## Complete Workflow

### Prerequisites

**Required Software:**
- Python 3.x
- Jupyter/JupyterLab
- Playwright (Python package)

**Installation:**
```bash
# Install Playwright
pip install playwright

# Install Playwright browsers
playwright install chromium
```

**Verify Setup:**
```bash
# Check Python version
python3 --version

# Check Playwright installation
python3 -c "from playwright.sync_api import sync_playwright; print('Playwright OK')"
```

### Step-by-Step Process

**For Each Chapter:**

1. **Convert Notebook to HTML**
   ```bash
   cd notebooks_colab
   jupyter nbconvert --to html ch##_Chapter_Name.ipynb
   cd ..
   ```

2. **Inject Custom CSS**
   ```bash
   python3 inject_print_css.py \
       notebooks_colab/ch##_Chapter_Name.html \
       notebooks_colab/ch##_Chapter_Name_printable.html
   ```

3. **Generate PDF with Playwright**
   ```bash
   python3 generate_pdf_playwright.py ch##
   ```

4. **Verify PDF**
   ```bash
   open notebooks_colab/ch##_Chapter_Name.pdf
   ```

**Example for Chapter 5:**
```bash
# Step 1: Convert to HTML
cd notebooks_colab
jupyter nbconvert --to html ch05_Bivariate_Data_Summary.ipynb
cd ..

# Step 2: Inject CSS
python3 inject_print_css.py \
    notebooks_colab/ch05_Bivariate_Data_Summary.html \
    notebooks_colab/ch05_Bivariate_Data_Summary_printable.html

# Step 3: Generate PDF
python3 generate_pdf_playwright.py ch05

# Step 4: View PDF
open notebooks_colab/ch05_Bivariate_Data_Summary.pdf
```

---

## Generating Individual Chapters

### Quick Method (Shorthand)

If HTML already exists, use the shorthand:

```bash
python3 inject_print_css.py \
    notebooks_colab/ch##_*.html \
    notebooks_colab/ch##_*_printable.html && \
python3 generate_pdf_playwright.py ch##
```

### Chapters Completed (as of 2026-01-29)

- ✅ ch00_Preface.pdf (0.82 MB)
- ✅ ch01_Analysis_of_Economics_Data.pdf (1.00 MB)
- ✅ ch02_Univariate_Data_Summary.pdf (1.65 MB)
- ⏳ ch03-ch17 (pending)

### After Editing a Notebook

When you finish editing a notebook, regenerate its PDF:

1. **Save the notebook** in Jupyter/Colab
2. **Convert to HTML** (step 1 above)
3. **Inject CSS** (step 2 above)
4. **Generate PDF** (step 3 above)
5. **Verify results** (step 4 above)

**Important:** Always start from step 1 (HTML conversion) to ensure the latest notebook content is included.

---

## Generating All Chapters

### Batch Processing

The `generate_pdf_playwright.py` script supports batch processing with the `--all` flag.

**Full Batch Workflow:**

```bash
# Step 1: Convert all notebooks to HTML
cd notebooks_colab
for notebook in ch*.ipynb; do
    jupyter nbconvert --to html "$notebook"
done
cd ..

# Step 2: Inject CSS into all HTML files
for html in notebooks_colab/ch*.html; do
    if [[ ! "$html" =~ _printable\.html$ ]]; then
        printable="${html%.html}_printable.html"
        python3 inject_print_css.py "$html" "$printable"
    fi
done

# Step 3: Generate all PDFs
python3 generate_pdf_playwright.py --all

# Step 4: Verify output
ls -lh notebooks_colab/*.pdf
```

**Alternative Simple Approach:**

```bash
# Convert all notebooks
cd notebooks_colab && \
for nb in ch*.ipynb; do jupyter nbconvert --to html "$nb"; done && \
cd ..

# Generate all PDFs (includes CSS injection internally)
python3 generate_pdf_playwright.py --all
```

**Expected Output:**
```
Found 18 printable HTML files
======================================================================
Processing: ch00_Preface_printable.html
✓ Created: ch00_Preface.pdf (0.82 MB)
Processing: ch01_Analysis_of_Economics_Data_printable.html
✓ Created: ch01_Analysis_of_Economics_Data.pdf (1.00 MB)
...
======================================================================
Summary: 18 successful, 0 failed
```

---

## Troubleshooting

### Common Issues

#### Issue 1: "FileNotFoundError: HTML file not found"

**Cause:** Notebook hasn't been converted to HTML
**Solution:**
```bash
cd notebooks_colab
jupyter nbconvert --to html ch##_Chapter_Name.ipynb
cd ..
```

#### Issue 2: "Playwright not installed"

**Cause:** Missing Playwright package
**Solution:**
```bash
pip install playwright
playwright install chromium
```

#### Issue 3: "Headers/footers still visible in PDF"

**Cause:** Outdated `generate_pdf_playwright.py`
**Solution:** Verify `display_header_footer=False` at line 68:
```python
display_header_footer=False,   # EXPLICITLY NO HEADERS/FOOTERS
```

#### Issue 4: "Regression tables still wrap to multiple lines"

**Cause:** Outdated `notebook_pdf_styles.css`
**Solution:** Verify output font sizes:
```css
pre {
    font-size: 7.5pt !important;  /* Should be 7.5pt, not 9pt */
}

.output_text, .output_html {
    font-size: 7.5pt !important;  /* Should be 7.5pt, not 10px */
}
```

#### Issue 5: "Visual summary images not full width"

**Cause:** Missing CSS override
**Solution:** Verify line 208 in `notebook_pdf_styles.css`:
```css
img[alt*="Visual Summary"] {
    width: 100% !important;  /* Must have !important flag */
}
```

#### Issue 6: "URLs printing after hyperlinks"

**Cause:** Old CSS with URL printing rule
**Solution:** Ensure the `@media print` section (lines 410-425) does NOT have:
```css
/* This rule should NOT exist: */
a[href^="http"]:after {
    content: " (" attr(href) ")";  /* REMOVE THIS */
}
```

#### Issue 7: "Text alignment not justified"

**Cause:** Missing `!important` flags in `@media print`
**Solution:** Verify lines 411-425 have justified alignment with `!important`:
```css
@media print {
    p {
        text-align: justify !important;
    }
    .text_cell_render {
        text-align: justify !important;
    }
}
```

### Verification Commands

**Check file sizes:**
```bash
ls -lh notebooks_colab/*.pdf
```

**Count generated PDFs:**
```bash
ls notebooks_colab/*.pdf | wc -l
```

**Check CSS injection:**
```bash
grep "notebook_pdf_styles.css" notebooks_colab/ch00_Preface_printable.html
```

**Verify Playwright margins:**
```bash
grep -A 10 "await page.pdf" generate_pdf_playwright.py
```

---

## Technical Details

### PDF Generation Settings (Playwright)

**File:** `generate_pdf_playwright.py` lines 58-70

```python
await page.pdf(
    path=str(pdf_path),
    format='Letter',              # 8.5" x 11"
    print_background=True,         # Include background colors/images
    margin={
        'top': '0.75in',           # Top margin
        'right': '0.75in',         # Right margin
        'bottom': '0.75in',        # Bottom margin
        'left': '0.75in'           # Left margin
    },
    display_header_footer=False,   # EXPLICITLY NO HEADERS/FOOTERS
    prefer_css_page_size=True      # Respect CSS @page rules
)
```

**Key Parameters:**
- `format='Letter'`: Standard US letter size (8.5" × 11")
- `print_background=True`: Ensures colored backgrounds/borders render
- `margin`: Uniform 0.75" margins on all sides
- `display_header_footer=False`: Prevents browser from adding headers/footers
- `prefer_css_page_size=True`: Respects `@page` rules in CSS

### CSS Critical Sections

**File:** `notebook_pdf_styles.css`

**Page Setup (lines 328-330):**
```css
@page {
    size: letter portrait;
    margin: 0.75in;
}
```

**Output Font Sizes (lines 100-101, 109-110, 188):**
```css
pre {
    font-size: 7.5pt !important;
    line-height: 1.35 !important;
}

.output_text, .output_html {
    font-size: 7.5pt !important;
    line-height: 1.3 !important;
}

.dataframe, .simpletable {
    font-size: 7.5pt !important;
}
```

**Visual Summary Override (lines 207-214):**
```css
img[alt*="Visual Summary"] {
    width: 100% !important;  /* Override inline HTML width="65%" */
    border: 2px solid #008CB7;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    margin: 20pt auto;
    display: block;
}
```

**Print Media Justified Text (lines 411-425):**
```css
@media print {
    p {
        text-align: justify !important;
    }
    .text_cell_render {
        text-align: justify !important;
    }
    blockquote {
        text-align: justify !important;
    }
    li {
        text-align: justify !important;
    }
}
```

### File Structure

```
metricsai/
├── generate_pdf_playwright.py    # Primary PDF generator (Playwright)
├── generate_pdf.py                # Alternative (Chrome headless)
├── inject_print_css.py            # CSS injection tool
├── notebook_pdf_styles.css        # Master stylesheet
├── fix_currency_dollars.py        # Currency escaping (already applied)
├── verify_dollar_signs.py         # Verification tool
├── notebooks_colab/
│   ├── ch00_Preface.ipynb         # Source notebook
│   ├── ch00_Preface.html          # Converted HTML
│   ├── ch00_Preface_printable.html # HTML + CSS
│   ├── ch00_Preface.pdf           # Final PDF
│   ├── ch01_*.ipynb, .html, .pdf
│   └── ... (ch02-ch17)
└── log/
    └── 20260129_PDF_GENERATION_WORKFLOW.md  # This file
```

### Dependencies

**Python Packages:**
- `playwright` - For PDF generation
- `jupyter` - For notebook conversion
- Standard library: `asyncio`, `pathlib`, `sys`, `json`, `re`

**System Requirements:**
- Python 3.8+
- Chromium browser (installed via Playwright)
- 500MB+ disk space for browser binaries

---

## Workflow Summary (Quick Reference)

### Single Chapter

```bash
# 1. Convert notebook
cd notebooks_colab && jupyter nbconvert --to html ch##_*.ipynb && cd ..

# 2. Inject CSS + Generate PDF
python3 inject_print_css.py notebooks_colab/ch##_*.html notebooks_colab/ch##_*_printable.html && \
python3 generate_pdf_playwright.py ch##

# 3. View result
open notebooks_colab/ch##_*.pdf
```

### All Chapters

```bash
# 1. Convert all notebooks
cd notebooks_colab && for nb in ch*.ipynb; do jupyter nbconvert --to html "$nb"; done && cd ..

# 2. Generate all PDFs
python3 generate_pdf_playwright.py --all

# 3. Verify
ls -lh notebooks_colab/*.pdf
```

### After Editing

When you finish editing notebooks in the future:

1. Save all edited notebooks
2. Run the batch workflow above
3. Verify PDFs look correct
4. All formatting features will be preserved automatically

---

## Change Log

**2026-01-29:**
- ✅ Established Playwright-based PDF generation
- ✅ Configured 0.75" uniform margins
- ✅ Removed headers/footers
- ✅ Implemented justified text alignment
- ✅ Set visual summary images to full width (100%)
- ✅ Reduced output font size to 7.5pt (prevents table overflow)
- ✅ Removed printed URLs after hyperlinks
- ✅ Applied currency dollar sign escaping (485 instances across 15 notebooks)
- ✅ Generated PDFs for ch00, ch01, ch02
- ✅ Documented complete workflow

**Previous Work (Referenced):**
- Enhanced CSS with brand colors (log/20260129_1524.md)
- Added visual summary images (log/20260129_1219.md)
- Established PDF export workflow (log/20260129_1123.md)
- Fixed currency dollar signs (log/20260129_1543.md)

---

## Future Updates

When you're ready to regenerate PDFs after editing:

1. **Read this document** - Review the workflow
2. **Run batch process** - Convert all notebooks and generate PDFs
3. **Verify results** - Check a few PDFs to ensure formatting is correct
4. **Update this log** - Note any new chapters or changes

**Contact/Questions:**
- All scripts are in the project root directory
- CSS file: `notebook_pdf_styles.css`
- Log directory: `log/`
- Backup notebooks: `notebooks_colab_backup/`

---

## Success Metrics

✅ **Completeness:** All 18 chapters can be converted to PDF
✅ **Formatting:** Professional typography with justified text
✅ **Layout:** Consistent margins, spacing, and page breaks
✅ **Visual Impact:** Full-width chapter summary images
✅ **Readability:** Regression tables fit without wrapping
✅ **Interactivity:** Clickable hyperlinks preserved
✅ **Maintainability:** Single CSS file controls all formatting
✅ **Reproducibility:** Complete documentation for future use

**Status:** Production-ready workflow ✅

---

**End of Documentation**
