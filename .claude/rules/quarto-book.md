---
description: Quarto HTML book rendering and configuration
globs:
  - book/**
  - book/_quarto.yml
  - book/index.qmd
  - book/custom.css
---

# Quarto HTML Book

The project publishes all chapters as an interactive online book using Quarto, deployed via GitHub Pages.

**URL:** `https://quarcs-lab.github.io/metricsai/book/_book/index.html`

## Project Structure

```
book/
├── _quarto.yml             # Book config (chapters, format, theme)
├── index.qmd               # Welcome page (cover image, PDF link)
├── custom.css              # Colab badge alignment, hide figcaptions
├── notebooks_colab -> ../notebooks_colab  # Symlink to source
├── images -> ../images     # Symlink to images
├── _book/                  # Rendered HTML (committed for GitHub Pages)
└── .quarto/                # Cache (gitignored)
```

**Symlink architecture:** `book/notebooks_colab` and `book/images` are symlinks to root-level directories. This makes Quarto see all sources as local to `book/`, ensuring correct relative paths in rendered output. Google Translate is inlined in `_quarto.yml` (not a separate file) to avoid path issues with symlinked notebooks.

## Quick Reference

**Render entire book:**

```bash
cd book && quarto render
```

**Render single chapter (faster):**

```bash
cd book && quarto render notebooks_colab/ch05_Bivariate_Data_Summary.ipynb
```

## Path Conventions

- **In `_quarto.yml`:** Use `notebooks_colab/` prefix (via symlink, no `../`)
- **In `index.qmd`:** Use `images/` prefix (via symlink, no `../`)
- **Inside notebooks (.ipynb):** Use absolute GitHub URLs for images (`https://raw.githubusercontent.com/quarcs-lab/metricsai/main/images/`)

## IMPORTANT: List Formatting

Pandoc (Quarto's engine) requires a **blank line before any markdown list**. This applies to `-`, `*`, `1.`, and indented lists. Without the blank line, lists render as plain text. Always ensure a blank line precedes any list when editing notebooks.

## Key Files

| File | Purpose |
| --- | --- |
| `book/_quarto.yml` | 18 chapters in 4 parts, theme, format options |
| `book/index.qmd` | Welcome page with cover image and PDF download link |
| `book/custom.css` | Left-align Colab badges, hide auto-generated figcaptions |
| `index.html` | Project website — "Learn More" links to `book/_book/index.html` |

## Two Web Presences

The project has two separate web presences:

- **Project website:** `index.html` at repository root (standalone HTML)
- **Online book:** `book/_book/index.html` (Quarto-rendered, deployed to GitHub Pages)

The website's "Learn More" button links to the book.
