# CLAUDE.md – AI Assistant Instructions

**READ THIS FILE FIRST** upon entering this project.

This file contains critical rules and context for working on this project. These rules are non-negotiable.

---

## Critical Rules

### 1. NEVER DELETE DATA
Under no circumstances are you ever to DELETE any data files. Protected formats include:
- **Statistical data:** `.dta`, `.sav`, `.sas7bdat`
- **Spreadsheets:** `.xlsx`, `.xls`, `.csv`, `.tsv`
- **Spatial data:** `.shp`, `.geojson`, `.kml`, `.gpkg`
- **Databases:** `.db`, `.sqlite`, `.sql`
- **Raw data:** `.txt`, `.json`, `.xml`, `.parquet`
- **Add other formats as needed for your project**

### 2. NEVER DELETE PROGRAMS
Under no circumstances are you ever to DELETE any program files. Protected formats include:
- **Scripts:** `.do`, `.R`, `.py`, `.jl`, `.m`
- **Notebooks:** `.ipynb`, `.Rmd`, `.qmd`, `.md`
- **Configuration:** `.yaml`, `.yml`, `.toml`, `.ini`, `.txt`
- **Documentation:** `.md`, `.tex`
- **Add other formats as needed for your project**

### 3. STAY WITHIN THIS DIRECTORY
Under no circumstances are you ever to GO UP OUT OF THIS ONE FOLDER called `metricsai`. All work must remain within this project directory.

### 4. MAINTAIN PROGRESS LOGS
The `./log/` directory contains progress logs that preserve conversation context across sessions.

**Why:** Chat sessions can die unexpectedly. When a new Claude starts, it has no memory of previous work. Logs bridge this gap.

**When to log:**
- After completing significant work
- Before ending a session
- After major decisions
- When context is building up

**What to include:**
- Current state of the project
- Summary of work done (include key results, tables, or figures)
- Key decisions made
- Any issues or blockers
- Next steps planned

**How:** Create timestamped entries (`YYYYMMDD_HHMM.md`) documenting what was done, current state, and next steps.

**On startup:** Always check `./log/` for recent entries to understand what was happening before.

---

## Project Context

- **Project Title:** metricsAI: An Introduction to Econometrics with Python and AI in the Cloud
- **Primary Tools:** Python, Jupyter/Colab notebooks
- **Authors:** Carlos Mendez

---

## Generating PDFs from Notebooks

### Overview

The project uses an automated Playwright-based workflow to generate professional-quality PDFs from Jupyter notebooks. This workflow produces publication-ready PDFs with precise formatting control.

**Use cases:**

- Distributing to students without Python/Colab access
- Printing for offline study with book-style typography
- Creating archival versions with all outputs preserved
- Generating professional reports for distribution

### Automated PDF Generation Workflow

**Why Playwright?**

- **Precise control:** Exact margins, no unwanted headers/footers
- **Consistent output:** Reproducible results across all chapters
- **Better CSS rendering:** Full support for modern CSS features (justified text, full-width images)
- **Font loading:** Proper Google Fonts integration (Inter, JetBrains Mono)
- **Automation:** Process all 18 chapters with one command
- **Production ready:** Professional formatting suitable for textbook distribution

### Quick Reference

**Generate a single chapter:**
```bash
# Step 1: Convert notebook to HTML
cd notebooks_colab && jupyter nbconvert --to html ch05_*.ipynb && cd ..

# Step 2: Inject CSS and generate PDF
python3 scripts/inject_print_css.py notebooks_colab/ch05_*.html notebooks_colab/ch05_*_printable.html
python3 scripts/generate_pdf_playwright.py ch05

# Step 3: View result
open notebooks_colab/ch05_*.pdf
```

**Generate all chapters:**
```bash
# Convert all notebooks to HTML
cd notebooks_colab && for nb in ch*.ipynb; do jupyter nbconvert --to html "$nb"; done && cd ..

# Generate all PDFs with Playwright
python3 scripts/generate_pdf_playwright.py --all

# Verify output
ls -lh notebooks_colab/*.pdf
```

### Current Status (as of 2026-01-29)

- ✅ ch00_Preface.pdf (0.82 MB)
- ✅ ch01_Analysis_of_Economics_Data.pdf (1.00 MB)
- ✅ ch02_Univariate_Data_Summary.pdf (1.65 MB)
- ⏳ ch03-ch17 (ready to generate on demand)

### Professional Formatting Features

**Typography:**

- Justified text alignment (book-style, professional appearance)
- Body text: 11pt Inter font
- Input code: 9pt JetBrains Mono (readable for code cells)
- Output code/tables: 7.5pt JetBrains Mono (prevents regression table overflow)

**Layout:**

- Page format: Letter (8.5" × 11") portrait orientation
- Uniform margins: 0.75 inches on all sides
- No headers/footers: Clean pages with maximum content space
- Full-width visual summaries: Chapter opening images span 7 inches (full page width within margins)

**Visual Design:**

- Brand color hierarchy: ElectricCyan (#008CB7), SynapsePurple (#7A209F), DataPink (#C21E72)
- Visual summary images: Cyan borders with soft drop shadows
- Code blocks: Light blue-gray background with cyan left border
- Tables: Light blue headers with alternating row colors
- Blockquotes: Purple left border with light purple background

**Technical Quality:**

- Clickable hyperlinks preserved (URLs don't print as text)
- Regression tables fit without wrapping (7.5pt font prevents overflow)
- Mathematical equations render correctly (LaTeX)
- All figures and plots preserved at high resolution

### Key System Files

1. **`scripts/generate_pdf_playwright.py`** (248 lines) - Primary PDF generator
   - Uses Playwright's Chromium for reliable PDF rendering
   - Configures exact page settings (format, margins, headers/footers)
   - Handles font loading and waits for complete rendering
   - Supports single chapter (`ch05`) or batch mode (`--all`)

2. **`scripts/inject_print_css.py`** - CSS injection tool
   - Reads HTML files from `jupyter nbconvert`
   - Injects custom print styles from `scripts/notebook_pdf_styles.css`
   - Creates "_printable.html" versions ready for PDF generation

3. **`scripts/notebook_pdf_styles.css`** (426 lines) - Master stylesheet
   - All typography, colors, spacing, and layout rules
   - Justified text via `@media print` rules with `!important` flags
   - Font sizes: 11pt body, 9pt input code, 7.5pt output/tables
   - Full-width visual summaries: `width: 100% !important;` overrides inline HTML
   - Uniform 0.75in margins via `@page` rule

### Prerequisites

**Required software:**

```bash
# Install Playwright (Python package)
pip install playwright

# Install Playwright browsers
playwright install chromium

# Verify installation
python3 -c "from playwright.sync_api import sync_playwright; print('Playwright OK')"
```

**Already installed:**

- Python 3.x
- Jupyter/JupyterLab (for `nbconvert`)

### Critical CSS Settings

**Justified text alignment** (lines 411-425 in `scripts/notebook_pdf_styles.css`):
```css
@media print {
    p { text-align: justify !important; }
    .text_cell_render { text-align: justify !important; }
    blockquote { text-align: justify !important; }
    li { text-align: justify !important; }
}
```

**Full-width visual summaries** (line 208):
```css
img[alt*="Visual Summary"] {
    width: 100% !important;  /* Override inline HTML width attributes */
}
```

**Optimized output font sizes** (lines 100-101, 109-110, 188):
```css
pre {
    font-size: 7.5pt !important;  /* Reduced from 9pt to prevent table overflow */
    line-height: 1.35 !important;
}

.output_text, .output_html {
    font-size: 7.5pt !important;  /* Reduced from 10px for compact tables */
    line-height: 1.3 !important;
}

.dataframe, .simpletable {
    font-size: 7.5pt !important;  /* Regression tables fit without wrapping */
}
```

**Page margins** (line 330 in CSS and lines 62-67 in Python script):
```css
@page {
    size: letter portrait;
    margin: 0.75in;  /* Uniform margins on all sides */
}
```

### Troubleshooting

**Issue: Regression tables still wrap to multiple lines**

- **Cause:** Output font size too large
- **Fix:** Verify `pre`, `.output_text`, and `.simpletable` are set to 7.5pt in CSS

**Issue: Visual summary images not full width**

- **Cause:** Missing CSS override or no `!important` flag
- **Fix:** Verify line 208 in CSS has `width: 100% !important;`

**Issue: Text not justified**

- **Cause:** CSS rules not inside `@media print` section
- **Fix:** Verify lines 411-425 have justified text rules with `!important` flags

**Issue: Headers/footers visible in PDF**

- **Cause:** Outdated `scripts/generate_pdf_playwright.py`
- **Fix:** Verify line 68 has `display_header_footer=False`

**Issue: Playwright not installed**

- **Fix:** Run `pip install playwright && playwright install chromium`

### Complete Documentation

For comprehensive workflow details, see:

**[log/20260129_PDF_GENERATION_WORKFLOW.md](log/20260129_PDF_GENERATION_WORKFLOW.md)**

This 600+ line document includes:

- Step-by-step workflow for single and batch processing
- Complete formatting specifications with line numbers
- Troubleshooting guide with 7 common issues and solutions
- Technical details (page setup, CSS critical sections, file structure)
- Dependencies and verification commands
- Future update instructions

### Workflow Summary

**When you need to regenerate PDFs after editing notebooks:**

1. **Save edited notebooks** in Jupyter/Colab
2. **Convert to HTML:** `cd notebooks_colab && jupyter nbconvert --to html ch##_*.ipynb && cd ..`
3. **Inject CSS and generate PDF:** `python3 scripts/inject_print_css.py notebooks_colab/ch##_*.html notebooks_colab/ch##_*_printable.html && python3 scripts/generate_pdf_playwright.py ch##`
4. **Verify results:** `open notebooks_colab/ch##_*.pdf`

**All formatting features are preserved automatically** - no manual adjustments needed!

---

## Generating the HTML Book (Quarto)

### Overview

The project has two separate web presences:

- **Project website:** `index.html` (standalone HTML at root)
- **Online HTML book:** `book/` directory (Quarto book project)

The website's "Learn More" button links to the book at `book/_book/index.html`.

### Project Structure

```
metricsai/
├── index.html                  # Project website (standalone)
├── book/                       # Quarto book project
│   ├── _quarto.yml             # Book config (chapters, format, theme)
│   ├── index.qmd               # Book welcome page (cover image, PDF link)
│   ├── custom.css              # Colab badge left-alignment
│   ├── notebooks_colab -> ../notebooks_colab  # Symlink to source notebooks
│   ├── images -> ../images     # Symlink to images directory
│   ├── _book/                  # Rendered HTML output (committed for GitHub Pages)
│   └── .quarto/                # Quarto cache (gitignored)
├── notebooks_colab/            # Source notebooks (ch00–ch17)
├── images/                     # Cover images + visual summaries
└── .gitignore                  # Ignores book/.quarto/, notebooks_colab/*_files/
```

**Symlink architecture:** `book/notebooks_colab` and `book/images` are symlinks to the root-level directories. This makes Quarto see all sources as local to the `book/` project, ensuring all rendered output goes into `book/_book/` with correct relative paths to CSS/JS/images. Google Translate is inlined in `_quarto.yml` (not a separate file) to avoid path resolution issues with symlinked notebooks.

### Quick Reference

**Re-render the entire book after editing notebooks:**

```bash
cd book && quarto render
# Output: book/_book/index.html
```

**Render a single chapter (faster iteration):**

```bash
cd book && quarto render notebooks_colab/ch05_Bivariate_Data_Summary.ipynb
```

### Path Conventions

- **Notebook paths in `book/_quarto.yml`:** Use `notebooks_colab/` prefix (via symlink, no `../`)
- **Image paths in `book/index.qmd`:** Use `images/` prefix (via symlink, no `../`)
- **Notebook images (inside .ipynb):** Use absolute GitHub URLs (`https://raw.githubusercontent.com/quarcs-lab/metricsai/main/images/`)

### List Formatting

Pandoc (Quarto's rendering engine) requires a **blank line before any markdown list**. This applies to dash (`- `), asterisk (`* `), numbered (`1. `), and indented lists. Without the blank line, lists render as plain text.

When adding new content to notebooks, always ensure a blank line precedes any list.

### Key Files

| File | Purpose |
|------|---------|
| `book/_quarto.yml` | Quarto config — 18 chapters in 4 parts, theme, format options |
| `book/index.qmd` | Book welcome page — cover image, Leanpub PDF download link |
| `book/custom.css` | CSS — left-aligns Colab badges, hides auto-generated figcaptions |
| `book/google-translate.html` | Google Translate widget (legacy file, now inlined in `_quarto.yml`) |
| `index.html` | Project website — "Learn More" links to `book/_book/index.html` |

### Current Status (as of 2026-02-15)

- All 18 pages render successfully (preface + ch01–ch17)
- 4 parts: Statistical Foundations, Bivariate Regression, Multiple Regression, Advanced Topics
- Google Translate bar on every page (inlined in `_quarto.yml`)
- List formatting fixed across all notebooks (~460 fixes)
- Symlink architecture ensures all output renders into `book/_book/` with correct paths
- Deployed to GitHub Pages: `https://quarcs-lab.github.io/metricsai/book/_book/index.html`
- See `log/20260215_HTML_BOOK_SETUP.md` for initial setup details
