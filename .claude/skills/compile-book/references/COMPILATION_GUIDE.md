# Book Compilation Technical Guide

## Book Structure

```
metricsAI_complete_book.pdf (900 pages, 62.3 MB)
├── Cover page (1 page, unnumbered)
│   └── images/book1cover.jpg with navy blue (#0a1628) background
├── Copyright page (1 page, unnumbered)
│   └── Title, copyright, affiliation, companion website (centered)
├── Brief Contents (1 page, unnumbered, clickable hyperlinks)
│   └── Chapters 1-17 grouped by Parts (no Preface)
├── Detailed Contents (4 pages, unnumbered, clickable hyperlinks)
│   └── Preface sections + all chapter sections with page numbers
├── Key Concepts (5 pages, unnumbered, clickable hyperlinks)
│   └── 189 numbered Key Concepts grouped by Parts and Chapters
└── Content (888 pages, numbered 1-888)
    ├── CH00: Preface (15 pages)
    ├── Part I: Foundations
    │   ├── CH01: Analysis of Economics Data (37 pages)
    │   ├── CH02: Univariate Data Summary (62 pages)
    │   ├── CH03: The Sample Mean (41 pages)
    │   └── CH04: Statistical Inference for the Mean (58 pages)
    ├── Part II: Bivariate Regression
    │   ├── CH05: Bivariate Data Summary (64 pages)
    │   ├── CH06: The Least Squares Estimator (39 pages)
    │   ├── CH07: Statistical Inference for Bivariate Regression (72 pages)
    │   └── CH08: Case Studies for Bivariate Regression (41 pages)
    ├── Part III: Multiple Regression
    │   ├── CH09: Models with Natural Logarithms (37 pages)
    │   ├── CH10: Data Summary for Multiple Regression (40 pages)
    │   ├── CH11: Statistical Inference for Multiple Regression (54 pages)
    │   ├── CH12: Further Topics in Multiple Regression (48 pages)
    │   └── CH13: Case Studies for Multiple Regression (63 pages)
    └── Part IV: Advanced Topics
        ├── CH14: Regression with Indicator Variables (45 pages)
        ├── CH15: Regression with Transformed Variables (54 pages)
        ├── CH16: Checking the Model and Data (59 pages)
        └── CH17: Panel Data, Time Series Data, and Causation (59 pages)
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

### 9-Step Process

1. **Cover page + Copyright page**: Playwright renders cover (`images/book1cover.jpg` on navy blue `#0a1628`) and copyright page (centered title, copyright, affiliation, website)
2. **Count pages + extract sections + extract Key Concepts**: Reads all 18 PDFs, extracts `## X.Y Title` headers and `Key Concept X.N: Title` from notebooks, maps to PDF pages
3. **Tables of Contents**: Playwright renders Brief Contents (1 page), Detailed Contents (4 pages), and Key Concepts TOC (5 pages) with placeholder hyperlinks
4. **Merge PDFs**: pypdf merges cover + copyright + Brief + Detailed + Key Concepts + 18 chapters
5. **Page numbers**: Playwright renders transparent overlay with centered page numbers; pypdf merges onto content pages
6. **PDF bookmarks**: pypdf adds hierarchical outline (Preface > Parts > Chapters > Sections)
7. **Clickable TOC links**: Extracts placeholder URL annotations from all three TOC PDFs, converts to internal GoTo links pointing to correct final pages (753 links)
8. **Write final PDF**: Saves compiled book to `notebooks_colab/metricsAI_complete_book.pdf`

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
| ElectricCyan | `#008CB7` | TOC title, page numbers, copyright title |
| SynapsePurple | `#7A209F` | Part headers, bookmark color |
| Navy | `#0a1628` | Cover background |
| DataPink | `#C21E72` | (reserved) |

### Page Numbering

- Cover: unnumbered
- Copyright: unnumbered
- Brief Contents: unnumbered
- Detailed Contents: unnumbered
- Key Concepts: unnumbered
- Content pages: numbered 1-888 (centered at bottom, 10pt Inter, #555)
- Front matter count: 1 (cover) + 1 (copyright) + 1 (brief) + 4 (detailed) + 5 (key concepts) = 12 pages

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
├── Chapter 5-9 with sections
Part III: Multiple Regression (bold, purple)
├── Chapter 10-13 with sections
Part IV: Advanced Topics (bold, purple)
├── Chapter 14-17 with sections
```

Total: 132 bookmark entries (1 Preface + 4 Parts + 17 Chapters + 110 Sections)

## Clickable TOC Hyperlinks

All three TOC sections (Brief Contents, Detailed Contents, Key Concepts) include clickable hyperlinks (753 total) that jump directly to the target page in the PDF. These are generated automatically during compilation.

### 3-Phase Approach

1. **Placeholder URLs in HTML**: TOC entries are wrapped in `<a class="toc-link" href="https://internal.metricsai/page/{N}">` tags, where `{N}` is the content page number. CSS hides the link styling: `a.toc-link { color: inherit; text-decoration: none; }`

2. **Playwright preserves annotations**: When Playwright renders the HTML to PDF, it preserves `<a>` tags as PDF link annotations with exact coordinate rectangles (rects). These are extracted before the merge step using `extract_toc_links()`.

3. **GoTo link conversion**: After the final PDF is assembled (merge + page numbers + bookmarks), `pypdf.annotations.Link(rect, target_page_index)` creates internal GoTo links. The content page numbers from the placeholder URLs are converted to physical page indices accounting for front matter offset (12 pages).

### Key Functions

- `generate_cover_html()`: Full-bleed cover page with navy blue background
- `generate_copyright_html()`: Centered copyright page (title, copyright, affiliation, website)
- `generate_brief_toc_html()`: Wraps chapter titles and page numbers in placeholder `<a>` tags
- `generate_detailed_toc_html()`: Wraps Preface sections, chapter titles, section titles, and page numbers in placeholder `<a>` tags
- `extract_key_concepts(ch_id)`: Extracts numbered Key Concept titles from notebook JSON (`> **Key Concept X.N: Title**`)
- `map_key_concepts_to_pdf_pages(concepts, pdf_path)`: Maps Key Concept titles to PDF page offsets by searching extracted text
- `generate_key_concepts_toc_html()`: Wraps Key Concept numbers, titles, and page numbers in placeholder `<a>` tags, grouped by Parts and Chapters
- `extract_toc_links(pdf_path)`: Reads a TOC PDF and extracts `(page_idx, rect, content_page)` tuples from URL annotations matching `internal.metricsai/page/`
- `compile_book()` Step 7: Iterates over extracted links from all three TOC PDFs and adds `Link(rect, target_page_index)` annotations to the final PDF writer

### Link Counts

- **Brief Contents**: ~51 links (chapter titles + page numbers)
- **Detailed Contents**: ~273 links (Preface sections + chapter titles + section titles + page numbers)
- **Key Concepts**: ~429 links (Key Concept numbers + titles + page numbers)
- **Total**: 753 clickable links

## Dependencies

| Package | Purpose | Install |
|---------|---------|---------|
| playwright | PDF rendering via Chromium | `pip install playwright && playwright install chromium` |
| pypdf | PDF merging, bookmarks, page overlay, clickable TOC links (`pypdf.annotations.Link`) | `pip install pypdf` |
| jupyter | nbconvert (notebook to HTML) | `pip install jupyter` |

*Version: 2.0 | Updated: 2026-02-08 | Author: metricsAI project*
