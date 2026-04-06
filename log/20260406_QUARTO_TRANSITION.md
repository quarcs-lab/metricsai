# 2026-04-06: Transition to Quarto-Based Workflow

## Summary

Migrated the book's source of truth from Jupyter notebooks (`.ipynb`) to Quarto documents (`.qmd`). The `.qmd` files in `notebooks_quarto/` are now the canonical source. Jupyter notebooks in `notebooks_colab/` are generated artifacts for Google Colab access.

## What Changed

### New Directory: `notebooks_quarto/`
- 18 `.qmd` files (ch00–ch17), one per chapter
- Created via `quarto convert` from the original `.ipynb` files, then post-processed to clean YAML front matter and remove execution metadata
- YAML front matter: `title` + `execute: enabled: false` (no kernel needed for rendering)

### New Scripts
- `scripts/convert_ipynb_to_qmd.py` — converts `.ipynb` → `.qmd` (used for initial migration)
- `scripts/export_qmd_to_ipynb.py` — converts `.qmd` → `.ipynb` for Colab (ongoing use)

### Updated Book Configuration
- `book/_quarto.yml` — all 18 chapter paths changed from `notebooks_colab/*.ipynb` to `notebooks_quarto/*.qmd`
- `book/notebooks_quarto` symlink created (points to `../notebooks_quarto`)
- `book/notebooks_colab` symlink removed (no longer needed by Quarto)
- Cover image JS updated to handle both `/notebooks_colab/` and `/notebooks_quarto/` paths

### Updated Scripts
- `scripts/compile_book.py` — `extract_chapter_sections()` now reads `.qmd` files (falls back to `.ipynb`)

### Updated Documentation
- `CLAUDE.md` — project structure, key commands, conventions, architecture
- `README.md` — replaced Jupytext section with Quarto workflow, updated PDF commands
- `.claude/rules/quarto-book.md` — render commands, path conventions, project structure
- `.claude/rules/pdf-generation.md` — pipeline diagram, quick reference commands

### Updated Claude Skills
- `chapter-standard/scripts/verify_chapter.py` — rewritten to parse `.qmd` instead of `.ipynb` JSON
- `chapter-standard/scripts/apply_fixes.py` — rewritten for `.qmd` text format
- `proofread/scripts/proofread_chapter.py` — rewritten for `.qmd` text format
- All three `SKILL.md` files updated (chapter-standard, proofread, compile-book)

### Updated `.gitignore`
- Added `notebooks_quarto/*.html` and `notebooks_quarto/*_files/`

## New Workflow

```
Edit: notebooks_quarto/*.qmd        (source of truth)
  |
  ├── cd book && quarto render       → book/_book/ (HTML book)
  ├── export_qmd_to_ipynb.py --all   → notebooks_colab/*.ipynb (for Colab)
  └── quarto render → inject CSS → Playwright → PDF
```

## What Stays the Same

- `notebooks_colab/` directory remains at project root (holds generated `.ipynb` for Colab)
- Colab badge links in `index.html` and `.qmd` files still point to `notebooks_colab/*.ipynb`
- PDF pipeline steps 2-3 unchanged (`inject_print_css.py`, `generate_pdf_playwright.py`)
- `book/custom.css` unchanged
- `book/index.qmd` unchanged

## Verified

- All 18 chapters render from `.qmd` via `quarto render` (book)
- All 18 chapters render individually to HTML
- All 18 `.ipynb` files exported successfully via `export_qmd_to_ipynb.py`
- `verify_chapter.py` runs on `.qmd` files (ch01: 91/100 compliance)
- `proofread_chapter.py` runs on `.qmd` files (ch01: 75/100 score)
- Book deployed to GitHub Pages successfully

## Decisions Made

- `.qmd` files use `execute: enabled: false` to avoid needing a Python kernel during render
- Jupytext `.md` paired files are now obsolete (can be archived later)
- The `convert_ipynb_to_qmd.py` script was for the one-time migration; `export_qmd_to_ipynb.py` is for ongoing use

## Next Steps

- Archive Jupytext `.md` paired files in `notebooks_colab/` (no longer maintained)
- Update remaining utility scripts if needed (`add_resource_buttons.py`, `number_key_concepts.py`)
- Consider enabling `execute: true` with `freeze: auto` for chapters that need output rendering
