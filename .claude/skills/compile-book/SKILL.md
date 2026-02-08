---
name: compile-book
description: Compiles all chapter PDFs into a single metricsAI book PDF. Detects modified chapters, regenerates their PDFs, then merges all chapters with cover page, Brief Contents, Detailed Contents, clickable TOC hyperlinks, page numbers, and section-level PDF bookmarks. Use after editing any chapter notebook.
argument-hint: [chapter-numbers...] [--compile-only] [--check] [--all]
context: fork
agent: Explore
---

# Book Compilation Skill

Automates the end-to-end pipeline for compiling the metricsAI textbook: detects modified chapters, regenerates their PDFs, and merges all 18 chapters into a single book PDF with professional formatting.

## Overview

This skill manages the complete book compilation workflow. It detects which chapter notebooks have been modified since their last PDF generation, regenerates only those PDFs, then compiles everything into a single book with cover page, two tables of contents, page numbers, and hierarchical PDF bookmarks.

**Use this skill when:**
- After editing any chapter notebook
- When you want to produce the complete book PDF
- To check which chapters have outdated PDFs
- Before distributing the textbook

**Key Features:**
- Automatic detection of modified chapters (notebook mtime vs PDF mtime)
- 3-step PDF regeneration pipeline (nbconvert, CSS injection, Playwright)
- Book compilation with cover, Brief Contents, Detailed Contents
- Page numbers on all content pages
- Section-level PDF bookmarks (Preface > Parts > Chapters > Sections)
- Clickable TOC hyperlinks (~324 links jump to chapters/sections from both TOC pages)
- 803 pages, ~56 MB output

---

## Quick Start

### Compile After Edits (Default)
```
/compile-book
```

Detects modified chapters, regenerates their PDFs, compiles the full book.

### Regenerate Specific Chapters
```
/compile-book ch05 ch08
```

Force-regenerates PDFs for chapters 5 and 8, then compiles.

### Regenerate All Chapter PDFs
```
/compile-book --all
```

Regenerates all 18 chapter PDFs from scratch, then compiles.

### Compile Only (Skip Regeneration)
```
/compile-book --compile-only
```

Assumes all chapter PDFs are current. Just runs the book compiler.

### Check PDF Freshness
```
/compile-book --check
```

Reports which chapters have outdated PDFs (read-only, no changes).

---

## Compilation Workflow

When you invoke this skill, follow these steps:

### 1. Parse Arguments

Extract chapter numbers and flags from the invocation:
- `ch05` or `5` -> normalized to `ch05`
- `--compile-only` -> skip PDF regeneration
- `--check` -> report-only mode (no compilation)
- `--all` -> regenerate all chapter PDFs
- Multiple chapters: `ch05 ch08 ch12`

### 2. Check PDF Freshness

For each chapter (ch00-ch17), compare modification times:
- **Notebook**: `notebooks_colab/chXX_*.ipynb`
- **PDF**: `notebooks_colab/chXX_*.pdf`

```bash
# Check if notebook is newer than its PDF
# A chapter needs regeneration if:
# 1. No PDF exists, OR
# 2. Notebook mtime > PDF mtime
```

Classify each chapter as:
- **Current**: PDF exists and is newer than notebook
- **Outdated**: Notebook modified after PDF generation
- **Missing**: No PDF file found

### 3. Report Status

Display a status table:

```markdown
## PDF Freshness Report

| Chapter | Status | Notebook Modified | PDF Modified |
|---------|--------|-------------------|--------------|
| ch00    | Current | 2026-02-07 22:30 | 2026-02-07 23:00 |
| ch05    | Outdated | 2026-02-08 10:15 | 2026-02-07 23:00 |
| ch08    | Outdated | 2026-02-08 09:30 | 2026-02-07 23:00 |
| ...     | ...    | ...               | ...          |

**2 chapters need PDF regeneration.**
```

If `--check` flag: stop here (read-only mode).

### 4. Regenerate Chapter PDFs

For each chapter that needs regeneration, run the 3-step pipeline:

```bash
# Step 1: Convert notebook to HTML
cd notebooks_colab && jupyter nbconvert --to html chXX_*.ipynb && cd ..

# Step 2: Inject print CSS
python3 inject_print_css.py notebooks_colab/chXX_*.html notebooks_colab/chXX_*_printable.html

# Step 3: Generate PDF via Playwright
python3 generate_pdf_playwright.py chXX
```

Report each chapter's PDF size after generation.

**Important**: Run chapters sequentially (each uses Playwright which launches a browser).

### 5. Compile Book

Run the book compilation script:

```bash
python3 scripts/compile_book.py
```

This produces `notebooks_colab/metricsAI_complete_book.pdf` with:
- Cover page (navy blue background, `images/book1cover.jpg`)
- Brief Contents (1 page, chapters grouped by Parts, clickable hyperlinks)
- Detailed Contents (3-4 pages, all sections with page numbers, clickable hyperlinks)
- All 18 chapters merged with page numbers
- PDF bookmarks: Preface > Part I-IV > Chapters 1-17 > Sections
- Clickable TOC hyperlinks: ~324 links on both TOC pages jump directly to chapters/sections

### 6. Report Results

Display compilation summary:

```markdown
## Compilation Complete

| Metric | Value |
|--------|-------|
| Total pages | 803 |
| File size | 56.4 MB |
| Chapters | 18 (CH00-CH17) |
| Sections in bookmarks | 110 |
| Clickable TOC links | ~324 |
| Chapters regenerated | 2 |
| Output | notebooks_colab/metricsAI_complete_book.pdf |
```

### 7. Open PDF

```bash
open notebooks_colab/metricsAI_complete_book.pdf
```

---

## Book Structure

### Front Matter (unnumbered)
- **Cover page**: Full-bleed image with navy blue background
- **Brief Contents**: Chapter-level TOC grouped by Parts (no Preface), with clickable hyperlinks
- **Detailed Contents**: Preface sections + all chapter sections with page numbers, with clickable hyperlinks

### Content (numbered from page 1)
- **CH00**: Preface (15 pages)
- **Part I: Foundations** (CH01-CH04, 172 pages)
- **Part II: Bivariate Regression** (CH05-CH08, 201 pages)
- **Part III: Multiple Regression** (CH09-CH13, 218 pages)
- **Part IV: Advanced Topics** (CH14-CH17, 191 pages)

### PDF Bookmarks
Hierarchical navigation sidebar in PDF readers:
- Preface > 4 sections
- Part I > Ch1 (9 sections), Ch2 (6), Ch3 (7), Ch4 (7)
- Part II > Ch5 (11), Ch6 (4), Ch7 (7), Ch8 (3)
- Part III > Ch9 (4), Ch10 (8), Ch11 (7), Ch12 (6), Ch13 (9)
- Part IV > Ch14 (3), Ch15 (4), Ch16 (5), Ch17 (6)

### Clickable TOC Hyperlinks
Both TOC pages include clickable hyperlinks (~324 total) that jump directly to the target chapter or section page:
- **Brief Contents**: Each chapter title and page number is a clickable link
- **Detailed Contents**: Each Preface section, chapter title, section title, and page number is a clickable link
- Links are styled invisibly (no blue underlines) to preserve the professional TOC appearance
- Links are automatically generated during compilation using a 3-phase approach:
  1. Placeholder URLs are embedded in TOC HTML (`https://internal.metricsai/page/{N}`)
  2. Playwright preserves these as PDF link annotations with exact coordinate rectangles
  3. After merging, `extract_toc_links()` reads the rects and `pypdf.annotations.Link` creates internal GoTo links pointing to the correct final page

---

## PDF Generation Pipeline

Each chapter PDF is generated through a 3-step pipeline:

1. **jupyter nbconvert --to html**: Converts `.ipynb` to raw HTML with all outputs
2. **inject_print_css.py**: Injects `notebook_pdf_styles.css` for professional formatting (justified text, brand colors, optimized font sizes)
3. **generate_pdf_playwright.py**: Renders HTML to PDF via Chromium with precise margin and layout control

### Key Formatting
- **Page**: Letter (8.5" x 11"), 0.75" margins
- **Typography**: Inter (body), JetBrains Mono (code)
- **Body text**: 11pt justified
- **Code input**: 9pt monospace
- **Code output/tables**: 7.5pt (prevents regression table overflow)
- **No headers/footers**: Clean pages

---

## Prerequisites

Required software:
- Python 3.x
- Playwright (`pip install playwright && playwright install chromium`)
- pypdf (`pip install pypdf`)
- Jupyter (`pip install jupyter` for nbconvert)

Verify installation:
```bash
python3 -c "from playwright.sync_api import sync_playwright; print('Playwright OK')"
python3 -c "from pypdf import PdfReader; print('pypdf OK')"
jupyter nbconvert --version
```

---

## Troubleshooting

### Chapter PDF Not Regenerating
**Symptom**: `/compile-book` says chapter is current but content is outdated.
**Cause**: Notebook file wasn't saved after editing.
**Fix**: Save the notebook, then re-run. Or force with `/compile-book chXX`.

### Playwright Error
**Symptom**: `Error: Browser not found` or `Playwright not installed`.
**Fix**: `pip install playwright && playwright install chromium`

### Missing Chapter PDF
**Symptom**: `FileNotFoundError: No PDF found for chXX`.
**Fix**: Run `/compile-book chXX` to generate the missing PDF.

### Large File Size
**Symptom**: Book PDF exceeds 60 MB.
**Cause**: High-resolution images or many plot outputs.
**Note**: ~56 MB is expected for 803 pages with charts and plots.

### Section Not Found in Bookmarks
**Symptom**: Some chapter sections missing from PDF bookmarks.
**Cause**: Section title in notebook doesn't match PDF extracted text.
**Note**: ~96% of sections are matched. Minor mismatches are expected.

### TOC Links Not Working
**Symptom**: Clicking a chapter or section title in the TOC does not jump to the page.
**Cause**: The placeholder URL annotations may not have been preserved during PDF generation.
**Fix**: Ensure Playwright is rendering the TOC HTML correctly. Recompile with `/compile-book --compile-only`. Check that `extract_toc_links()` finds annotations in the generated TOC PDFs.

---

## Integration with Other Skills

### Recommended Workflow
```
1. /chapter-standard chXX          # Verify structure (target: 90+)
2. /proofread chXX --fix            # Fix text quality issues
3. /compile-book chXX               # Regenerate PDF and recompile book
```

### After Batch Edits
```
1. /chapter-standard --all          # Check all chapters
2. /proofread --all                 # Check all chapters
3. /compile-book                    # Auto-detect and regenerate modified chapters
```

---

## Key Files

| File | Purpose |
|------|---------|
| `scripts/compile_book.py` | Book compilation script (merges PDFs, generates TOCs, adds bookmarks) |
| `generate_pdf_playwright.py` | Chapter PDF generator (Playwright-based) |
| `inject_print_css.py` | CSS injection for printable HTML |
| `notebook_pdf_styles.css` | Master stylesheet for PDF formatting |
| `images/book1cover.jpg` | Cover image (1407x1916px) |
| `notebooks_colab/metricsAI_complete_book.pdf` | Output: compiled book |
| `notebooks_colab/chXX_*.pdf` | Individual chapter PDFs |

---

*Version: 1.1 | Updated: 2026-02-08 | Author: metricsAI project*
