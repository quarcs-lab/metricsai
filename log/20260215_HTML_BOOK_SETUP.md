# HTML Book Setup and Project Reorganization — 2026-02-15

## Summary

Set up the Quarto HTML book from 18 Jupyter notebooks, fixed rendering issues, added features (Google Translate, PDF link), reorganized the project to separate the website from the book, and audited the entire codebase for problems.

## What Was Done

### 1. Quarto Book Compilation

- Created `book/_quarto.yml` configuring all 18 chapters (ch00–ch17) organized into 4 parts:
  - **Statistical Foundations** (ch01–ch04)
  - **Bivariate Regression** (ch05–ch09)
  - **Multiple Regression** (ch10–ch13)
  - **Advanced Topics** (ch14–ch17)
- Created `book/index.qmd` as the book welcome page with cover image and PDF download link
- Created `book/custom.css` to left-align Colab badges and hide auto-generated figcaptions
- All 19 pages render successfully via `cd book && quarto render`

### 2. List Formatting Fixes (All Notebooks)

- Pandoc (Quarto's engine) requires a blank line before any markdown list
- Applied comprehensive fix to all 18 notebooks (ch00–ch17)
- Handles all list types: dash (`- `), asterisk (`* `), numbered (`1. `), and indented variants
- Total: ~460 fixes across all notebooks

### 3. Google Translate Bar

- Created `book/google-translate.html` with the Google Translate Website Translator widget
- Injected into every page via `include-before-body` in `_quarto.yml`

### 4. PDF Download Link

- Added Leanpub link to `book/index.qmd`: [leanpub.com/econometrics-ai](https://leanpub.com/econometrics-ai)

### 5. Project Reorganization

- **Problem:** Root had both `index.html` (project website) and `index.qmd` (book welcome page) — naming collision
- **Solution:** Moved all Quarto files into `book/` subdirectory
- Updated all notebook paths in `_quarto.yml` with `../` prefix
- Updated `index.html` "Learn More" link to `book/_book/index.html`

### 6. Website "Learn More" Link

- Restored `index.html` from git (had been removed in commit `a9c4621`)
- Changed "Learn More" link in Books section to point to `book/_book/index.html`

### 7. Codebase Audit and Fixes

- **Fixed:** Cover image path in `book/index.qmd` — changed `images/` to `../images/`
- **Fixed:** Added `book/notebooks_colab/` to `.gitignore` (Quarto intermediary files)
- **Verified clean:** All 18 notebook paths, website links, Colab badges, data references, gitignore patterns

## Current Project Structure

```
metricsai/
├── index.html                  # Project website (standalone HTML)
├── favicon.svg                 # Website favicon
├── .gitignore                  # Git ignore rules
├── book/                       # Quarto book project
│   ├── _quarto.yml             # Book config (chapters, format, theme)
│   ├── index.qmd               # Book welcome page
│   ├── custom.css              # Colab badge styling
│   ├── google-translate.html   # Google Translate widget
│   ├── _book/                  # Rendered HTML output (gitignored)
│   ├── .quarto/                # Quarto cache (gitignored)
│   └── notebooks_colab/        # Intermediary render files (gitignored)
├── notebooks_colab/            # Source notebooks (ch00–ch17)
├── images/                     # Book cover + visual summaries
├── data/                       # Data files
├── log/                        # Progress logs
├── notes/                      # Study notes
└── code_python/                # Python scripts (PDF generation, etc.)
```

## Uncommitted Changes

All changes below are uncommitted (relative to last commit `e4d131e`):

| Change | Files |
|--------|-------|
| List formatting fixes | `notebooks_colab/ch01–ch17.ipynb` (17 files) |
| Website "Learn More" link update | `index.html` |
| New Quarto book setup | `book/` directory (new, untracked) |
| Updated gitignore | `.gitignore` (new, untracked) |

## Key Files

| File | Purpose |
|------|---------|
| `book/_quarto.yml` | Quarto config — chapters, parts, format, theme |
| `book/index.qmd` | Book welcome page — cover image, PDF link |
| `book/custom.css` | CSS — Colab badge left-alignment |
| `book/google-translate.html` | Google Translate widget for all pages |
| `index.html` | Project website — links to book via "Learn More" |
| `.gitignore` | Ignores `book/_book/`, `book/.quarto/`, `book/notebooks_colab/`, `*_files/` |

## How to Update the HTML Book After Editing Notebooks

```bash
# Re-render the entire book (from project root)
cd book && quarto render

# Or render a single chapter for faster iteration
cd book && quarto render ../notebooks_colab/ch05_Bivariate_Data_Summary.ipynb

# Output goes to book/_book/index.html
open book/_book/index.html
```

## Symlink Fix (2026-02-15, later session)

### Problem

After deploying to GitHub Pages, two issues appeared:

1. **Cover image missing** — `_book/index.html` referenced `../images/book1cover.jpg` which resolved to `book/images/` (doesn't exist)
2. **Chapter pages unstyled** — Chapter HTML files referenced CSS/JS at `../book/site_libs/` which resolved to `book/book/site_libs/` (doesn't exist)

### Root Cause

Quarto generates broken relative paths when source notebooks are referenced outside the project directory with `../` paths. Chapters rendered to `book/notebooks_colab/` (outside `_book/`) with incorrect asset paths.

### Fix

Created symlinks so Quarto sees sources as local to `book/`:

- `book/notebooks_colab` → `../notebooks_colab` (symlink)
- `book/images` → `../images` (symlink)
- Updated `_quarto.yml` paths from `../notebooks_colab/` to `notebooks_colab/`
- Updated `index.qmd` image path from `../images/` to `images/`
- Inlined Google Translate HTML in `_quarto.yml` (Quarto couldn't resolve the include file path through symlinks)

All 19 pages now render into `book/_book/` with correct paths. Deployed to GitHub Pages successfully.

## Current Status

- All changes committed and pushed to GitHub
- Book deployed at: `https://quarcs-lab.github.io/metricsai/book/_book/index.html`
- Workflow: edit notebooks → `cd book && quarto render` → commit `book/_book/` → push
