# Book Compilation Technical Guide

## Book Structure

```
metricsAI_complete_book.pdf (803 pages, ~56 MB)
├── Cover page (1 page, unnumbered)
│   └── images/book1cover.jpg with navy blue (#0a1628) background
├── Brief Contents (1 page, unnumbered, clickable hyperlinks)
│   └── Chapters 1-17 grouped by Parts (no Preface)
├── Detailed Contents (4 pages, unnumbered, clickable hyperlinks)
│   └── Preface sections + all chapter sections with page numbers
└── Content (797 pages, numbered 1-797)
    ├── CH00: Preface (15 pages)
    ├── Part I: Foundations
    │   ├── CH01: Analysis of Economics Data (27 pages)
    │   ├── CH02: Univariate Data Summary (53 pages)
    │   ├── CH03: The Sample Mean (41 pages)
    │   └── CH04: Statistical Inference for the Mean (51 pages)
    ├── Part II: Bivariate Regression
    │   ├── CH05: Bivariate Data Summary (56 pages)
    │   ├── CH06: The Least Squares Estimator (38 pages)
    │   ├── CH07: Statistical Inference for Bivariate Regression (66 pages)
    │   └── CH08: Case Studies for Bivariate Regression (41 pages)
    ├── Part III: Multiple Regression
    │   ├── CH09: Models with Natural Logarithms (37 pages)
    │   ├── CH10: Data Summary for Multiple Regression (32 pages)
    │   ├── CH11: Statistical Inference for Multiple Regression (46 pages)
    │   ├── CH12: Further Topics in Multiple Regression (40 pages)
    │   └── CH13: Case Studies for Multiple Regression (63 pages)
    └── Part IV: Advanced Topics
        ├── CH14: Regression with Indicator Variables (39 pages)
        ├── CH15: Regression with Transformed Variables (48 pages)
        ├── CH16: Checking the Model and Data (51 pages)
        └── CH17: Panel Data, Time Series Data, and Causation (53 pages)
```

## PDF Generation Pipeline (Per Chapter)

```
notebook.ipynb
    │
    ▼ jupyter nbconvert --to html
chXX_Title.html
    │
    ▼ inject_print_css.py (injects notebook_pdf_styles.css)
chXX_Title_printable.html
    │
    ▼ generate_pdf_playwright.py (Chromium rendering)
chXX_Title.pdf (1.0-2.0 MB each)
```

### Commands

```bash
# Single chapter
cd notebooks_colab && jupyter nbconvert --to html ch05_*.ipynb && cd ..
python3 inject_print_css.py notebooks_colab/ch05_*.html notebooks_colab/ch05_*_printable.html
python3 generate_pdf_playwright.py ch05

# All chapters
cd notebooks_colab && for nb in ch*.ipynb; do jupyter nbconvert --to html "$nb"; done && cd ..
python3 generate_pdf_playwright.py --all
```

## Book Compilation Script

**Script**: `scripts/compile_book.py`

### 8-Step Process

1. **Cover page**: Playwright renders `images/book1cover.jpg` on navy blue background (`#0a1628`) with `object-fit: contain` for full image display
2. **Count pages + extract sections**: Reads all 18 PDFs, extracts `## X.Y Title` headers from notebooks, maps to PDF pages
3. **Brief Contents**: Playwright renders 1-page HTML with chapters grouped by Parts (brand-styled, placeholder hyperlinks)
4. **Detailed Contents**: Playwright renders 4-page HTML with Preface sections and all chapter sections (placeholder hyperlinks)
5. **Merge PDFs**: pypdf merges cover + Brief + Detailed + 18 chapters
6. **Page numbers**: Playwright renders transparent overlay with centered page numbers; pypdf merges onto content pages
7. **PDF bookmarks**: pypdf adds hierarchical outline (Preface > Parts > Chapters > Sections)
8. **Clickable TOC links**: Extracts placeholder URL annotations from TOC PDFs, converts to internal GoTo links pointing to correct final pages (~324 links)

### Section Extraction

Section titles extracted from notebook JSON (`## ` headers):
- **CH00**: Descriptive headers (e.g., "Introduction", "Why This Book?")
- **CH01-CH17**: Numbered headers in two formats:
  - `## 1.1 What is Regression Analysis?` (space after number)
  - `## 8.1: Health Outcomes Across Countries` (colon after number)
- **Excluded**: Key Takeaways, Practice Exercises, Case Studies, Chapter Overview, Learning Objectives

Mapping: Section titles searched in PDF page text (skipping first 2 pages to avoid Chapter Overview false matches). ~96% match rate (110 of ~115 sections).

### Brand Colors

| Color | Hex | Usage |
|-------|-----|-------|
| ElectricCyan | `#008CB7` | TOC title, page numbers |
| SynapsePurple | `#7A209F` | Part headers, bookmark color |
| Navy | `#0a1628` | Cover background |
| DataPink | `#C21E72` | (reserved) |

### Page Numbering

- Cover: unnumbered
- Brief Contents: unnumbered
- Detailed Contents: unnumbered
- Content pages: numbered 1-797 (centered at bottom, 10pt Inter, #555)
- Front matter count: 1 (cover) + 1 (brief) + 4 (detailed) = 6 pages

## PDF Bookmark Hierarchy

```
Preface
├── Introduction
├── Why This Book? Three Pillars of Learning
├── How to Use This Book
└── Acknowledgments
Part I: Foundations (bold, purple)
├── Chapter 1: Analysis of Economics Data
│   ├── 1.1 What is Regression Analysis?
│   ├── 1.2 Load the Data
│   └── ... (9 sections)
├── Chapter 2: Univariate Data Summary (6 sections)
├── Chapter 3: The Sample Mean (7 sections)
└── Chapter 4: Statistical Inference for the Mean (7 sections)
Part II: Bivariate Regression (bold, purple)
├── Chapter 5-8 with sections
Part III: Multiple Regression (bold, purple)
├── Chapter 9-13 with sections
Part IV: Advanced Topics (bold, purple)
├── Chapter 14-17 with sections
```

Total: 132 bookmark entries (1 Preface + 4 Parts + 17 Chapters + 110 Sections)

## Clickable TOC Hyperlinks

Both Brief Contents and Detailed Contents pages include clickable hyperlinks (~324 total) that jump directly to the target page in the PDF. These are generated automatically during compilation.

### 3-Phase Approach

1. **Placeholder URLs in HTML**: TOC entries are wrapped in `<a class="toc-link" href="https://internal.metricsai/page/{N}">` tags, where `{N}` is the content page number. CSS hides the link styling: `a.toc-link { color: inherit; text-decoration: none; }`

2. **Playwright preserves annotations**: When Playwright renders the HTML to PDF, it preserves `<a>` tags as PDF link annotations with exact coordinate rectangles (rects). These are extracted before the merge step using `extract_toc_links()`.

3. **GoTo link conversion**: After the final PDF is assembled (merge + page numbers + bookmarks), `pypdf.annotations.Link(rect, target_page_index)` creates internal GoTo links. The content page numbers from the placeholder URLs are converted to physical page indices accounting for front matter offset.

### Key Functions

- `generate_brief_toc_html()`: Wraps chapter titles and page numbers in placeholder `<a>` tags
- `generate_detailed_toc_html()`: Wraps Preface sections, chapter titles, section titles, and page numbers in placeholder `<a>` tags
- `extract_toc_links(pdf_path)`: Reads a TOC PDF and extracts `(page_idx, rect, content_page)` tuples from URL annotations matching `internal.metricsai/page/`
- `compile_book()` Step 8: Iterates over extracted links and adds `Link(rect, target_page_index)` annotations to the final PDF writer

### Link Counts

- **Brief Contents**: ~51 links (chapter titles + page numbers)
- **Detailed Contents**: ~273 links (Preface sections + chapter titles + section titles + page numbers)
- **Total**: ~324 clickable links

## Dependencies

| Package | Purpose | Install |
|---------|---------|---------|
| playwright | PDF rendering via Chromium | `pip install playwright && playwright install chromium` |
| pypdf | PDF merging, bookmarks, page overlay, clickable TOC links (`pypdf.annotations.Link`) | `pip install pypdf` |
| jupyter | nbconvert (notebook to HTML) | `pip install jupyter` |

*Last updated: 2026-02-08*
