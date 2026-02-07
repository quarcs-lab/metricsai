#!/usr/bin/env python3
"""
Compile all chapter PDFs into a single book PDF.

Creates:
- Cover page from images/book1cover.jpg
- Brief Contents (chapter-level TOC)
- Detailed Contents (section-level TOC with Preface)
- All 18 chapters (CH00-CH17) merged
- Page numbers on every content page
- PDF bookmarks with section-level navigation

Usage:
    python3 scripts/compile_book.py
"""

import asyncio
import json
import os
import re
import tempfile
from pathlib import Path

from playwright.async_api import async_playwright
from pypdf import PdfReader, PdfWriter


# ============================================================
# Configuration
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
NOTEBOOKS_DIR = PROJECT_ROOT / 'notebooks_colab'
COVER_IMAGE = PROJECT_ROOT / 'images' / 'book1cover.jpg'
OUTPUT_PDF = NOTEBOOKS_DIR / 'metricsAI_complete_book.pdf'

CHAPTERS = [
    ('ch00', 'Preface'),
    ('ch01', 'Analysis of Economics Data'),
    ('ch02', 'Univariate Data Summary'),
    ('ch03', 'The Sample Mean'),
    ('ch04', 'Statistical Inference for the Mean'),
    ('ch05', 'Bivariate Data Summary'),
    ('ch06', 'The Least Squares Estimator'),
    ('ch07', 'Statistical Inference for Bivariate Regression'),
    ('ch08', 'Case Studies for Bivariate Regression'),
    ('ch09', 'Models with Natural Logarithms'),
    ('ch10', 'Data Summary for Multiple Regression'),
    ('ch11', 'Statistical Inference for Multiple Regression'),
    ('ch12', 'Further Topics in Multiple Regression'),
    ('ch13', 'Case Studies for Multiple Regression'),
    ('ch14', 'Regression with Indicator Variables'),
    ('ch15', 'Regression with Transformed Variables'),
    ('ch16', 'Checking the Model and Data'),
    ('ch17', 'Panel Data, Time Series Data, and Causation'),
]

# Part groupings for TOC and bookmarks
PARTS = [
    ('Part I: Foundations', ['ch01', 'ch02', 'ch03', 'ch04']),
    ('Part II: Bivariate Regression', ['ch05', 'ch06', 'ch07', 'ch08']),
    ('Part III: Multiple Regression', ['ch09', 'ch10', 'ch11', 'ch12', 'ch13']),
    ('Part IV: Advanced Topics', ['ch14', 'ch15', 'ch16', 'ch17']),
]

# Headers to exclude from section extraction
BACK_MATTER_HEADERS = {
    'Key Takeaways', 'Practice Exercises', 'Case Studies',
    'Chapter Overview', 'Overview', 'Learning Objectives',
}


# ============================================================
# Playwright helpers
# ============================================================

async def html_to_pdf(html_content, pdf_path, margins=None, wait_ms=500):
    """Render HTML string to PDF via Playwright."""
    if margins is None:
        margins = {'top': '0.75in', 'right': '0.75in',
                   'bottom': '0.75in', 'left': '0.75in'}

    with tempfile.NamedTemporaryFile(suffix='.html', delete=False, mode='w') as f:
        f.write(html_content)
        tmp_html = f.name

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(f'file://{tmp_html}')
            await page.wait_for_load_state('networkidle')
            await page.wait_for_timeout(wait_ms)
            await page.pdf(
                path=str(pdf_path),
                format='Letter',
                print_background=True,
                margin=margins,
                display_header_footer=False,
                prefer_css_page_size=False,
            )
            await browser.close()
    finally:
        os.unlink(tmp_html)


# ============================================================
# Step 1: Cover page
# ============================================================

def generate_cover_html():
    """Create HTML for full-bleed cover page with navy blue background."""
    img_path = COVER_IMAGE.resolve()
    return f"""<!DOCTYPE html>
<html>
<head>
<style>
  @page {{ size: letter portrait; margin: 0; }}
  * {{ margin: 0; padding: 0; }}
  body {{ width: 8.5in; height: 11in; overflow: hidden; background: #0a1628; }}
  img {{ width: 8.5in; height: 11in; object-fit: contain; display: block; }}
</style>
</head>
<body>
  <img src="file://{img_path}" />
</body>
</html>"""


# ============================================================
# Step 2: Count pages and extract sections
# ============================================================

def find_chapter_pdf(ch_id):
    """Find the PDF file for a chapter ID."""
    matches = sorted(NOTEBOOKS_DIR.glob(f'{ch_id}_*.pdf'))
    if not matches:
        raise FileNotFoundError(f"No PDF found for {ch_id}")
    return matches[0]


def count_pages():
    """Count pages in each chapter PDF."""
    chapter_data = []
    for ch_id, title in CHAPTERS:
        pdf_path = find_chapter_pdf(ch_id)
        reader = PdfReader(str(pdf_path))
        n_pages = len(reader.pages)
        chapter_data.append({
            'id': ch_id,
            'title': title,
            'pdf_path': pdf_path,
            'pages': n_pages,
        })
    return chapter_data


def extract_chapter_sections(ch_id):
    """Extract content section titles from a chapter notebook.

    For CH00 (Preface): All ## headers except back matter/structural
    For CH01-CH17: Only numbered ## X.Y headers
    """
    nb_matches = sorted(NOTEBOOKS_DIR.glob(f'{ch_id}_*.ipynb'))
    if not nb_matches:
        return []

    with open(nb_matches[0], 'r', encoding='utf-8') as f:
        nb = json.load(f)

    sections = []
    for cell in nb['cells']:
        if cell['cell_type'] != 'markdown':
            continue
        source = ''.join(cell['source'])

        for line in source.split('\n'):
            line = line.strip()
            if not line.startswith('## '):
                continue
            title = line[3:].strip()

            # Strip section numbers for back matter check
            # Handles both "1.1 Title" and "8.1: Title" formats
            base_title = re.sub(r'^\d+\.\d+:?\s*', '', title)
            if base_title in BACK_MATTER_HEADERS:
                continue

            if ch_id == 'ch00':
                sections.append(title)
            else:
                # Only numbered sections (e.g., "1.1 Title" or "8.1: Title")
                if re.match(r'\d+\.\d+[:\s]', title):
                    sections.append(title)

    return sections


def map_sections_to_pdf_pages(sections, pdf_path, ch_id=''):
    """Map section titles to page offsets within a chapter PDF.

    Returns list of (title, page_offset) tuples where page_offset
    is 0-indexed within the chapter PDF.
    """
    reader = PdfReader(str(pdf_path))
    n_pages = len(reader.pages)

    # Extract and normalize text from each page
    page_texts = []
    for i in range(n_pages):
        try:
            text = reader.pages[i].extract_text() or ''
        except Exception:
            text = ''
        # Normalize whitespace for matching
        page_texts.append(' '.join(text.split()))

    # Skip overview pages to avoid false matches from Chapter Overview
    skip = 1 if ch_id == 'ch00' else 2

    section_pages = []
    for title in sections:
        found = None
        clean_title = ' '.join(title.split())

        # Search after overview pages first
        for i in range(skip, n_pages):
            if clean_title in page_texts[i]:
                found = i
                break

        # Fallback: search all pages
        if found is None:
            for i in range(n_pages):
                if clean_title in page_texts[i]:
                    found = i
                    break

        if found is not None:
            section_pages.append((title, found))

    return section_pages


# ============================================================
# Step 3: Brief Contents and Detailed Contents
# ============================================================

def generate_brief_toc_html(chapter_data):
    """Create HTML for Brief Contents (chapter-level only, no Preface)."""
    offset = 1  # page numbering starts at 1 for CH00

    # Build chapter-to-page mapping
    ch_map = {}
    for ch in chapter_data:
        ch_map[ch['id']] = offset
        offset += ch['pages']

    # Build TOC rows grouped by parts
    toc_rows = []
    for part_name, part_chapters in PARTS:
        toc_rows.append(f'<tr class="part-row"><td colspan="3">{part_name}</td></tr>')
        for ch_id in part_chapters:
            ch = next(c for c in chapter_data if c['id'] == ch_id)
            num = ch_id.replace('ch', '').lstrip('0') or '0'
            label = f'Chapter {num}:'
            toc_rows.append(
                f'<tr>'
                f'<td class="ch-label">{label}</td>'
                f'<td class="ch-title">{ch["title"]}</td>'
                f'<td class="ch-page">{ch_map[ch_id]}</td>'
                f'</tr>'
            )

    rows_html = '\n'.join(toc_rows)

    return f"""<!DOCTYPE html>
<html>
<head>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

  @page {{ size: letter portrait; margin: 0.75in; }}

  body {{
    font-family: 'Inter', sans-serif;
    color: #1a1a2e;
    font-size: 11pt;
    line-height: 1.6;
  }}

  h1 {{
    text-align: center;
    font-size: 24pt;
    font-weight: 700;
    color: #008CB7;
    margin-bottom: 0.4in;
    letter-spacing: 1px;
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
  }}

  tr.part-row td {{
    font-weight: 700;
    font-size: 12pt;
    color: #7A209F;
    padding-top: 16px;
    padding-bottom: 6px;
    border-bottom: 2px solid #7A209F;
  }}

  td.ch-label {{
    width: 110px;
    font-weight: 600;
    color: #333;
    padding: 4px 0;
    white-space: nowrap;
  }}

  td.ch-title {{
    padding: 4px 8px;
    color: #1a1a2e;
  }}

  td.ch-page {{
    width: 40px;
    text-align: right;
    font-weight: 600;
    color: #008CB7;
    padding: 4px 0;
  }}
</style>
</head>
<body>
  <h1>Brief Contents</h1>
  <table>
    {rows_html}
  </table>
</body>
</html>"""


def generate_detailed_toc_html(chapter_data, section_data):
    """Create HTML for Detailed Contents (Preface + all chapters with sections)."""
    offset = 1  # page numbering starts at 1 for CH00

    # Build chapter-to-page mapping
    ch_map = {}
    for ch in chapter_data:
        ch_map[ch['id']] = offset
        offset += ch['pages']

    toc_rows = []

    # Preface entry with sections
    ch00 = next((c for c in chapter_data if c['id'] == 'ch00'), None)
    if ch00:
        toc_rows.append(
            f'<tr>'
            f'<td class="ch-label" style="font-weight:700">Preface</td>'
            f'<td class="ch-title"></td>'
            f'<td class="ch-page">{ch_map["ch00"]}</td>'
            f'</tr>'
        )
        if 'ch00' in section_data:
            for sec_title, sec_offset in section_data['ch00']:
                sec_page = ch_map['ch00'] + sec_offset
                toc_rows.append(
                    f'<tr class="section-row">'
                    f'<td></td>'
                    f'<td class="sec-title">{sec_title}</td>'
                    f'<td class="sec-page">{sec_page}</td>'
                    f'</tr>'
                )

    # Parts and chapters with sections
    for part_name, part_chapters in PARTS:
        toc_rows.append(f'<tr class="part-row"><td colspan="3">{part_name}</td></tr>')
        for ch_id in part_chapters:
            ch = next(c for c in chapter_data if c['id'] == ch_id)
            num = ch_id.replace('ch', '').lstrip('0') or '0'
            label = f'Chapter {num}:'
            toc_rows.append(
                f'<tr>'
                f'<td class="ch-label">{label}</td>'
                f'<td class="ch-title">{ch["title"]}</td>'
                f'<td class="ch-page">{ch_map[ch_id]}</td>'
                f'</tr>'
            )
            if ch_id in section_data:
                for sec_title, sec_offset in section_data[ch_id]:
                    sec_page = ch_map[ch_id] + sec_offset
                    toc_rows.append(
                        f'<tr class="section-row">'
                        f'<td></td>'
                        f'<td class="sec-title">{sec_title}</td>'
                        f'<td class="sec-page">{sec_page}</td>'
                        f'</tr>'
                    )

    rows_html = '\n'.join(toc_rows)

    return f"""<!DOCTYPE html>
<html>
<head>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

  @page {{ size: letter portrait; margin: 0.75in; }}

  body {{
    font-family: 'Inter', sans-serif;
    color: #1a1a2e;
    font-size: 10pt;
    line-height: 1.4;
  }}

  h1 {{
    text-align: center;
    font-size: 24pt;
    font-weight: 700;
    color: #008CB7;
    margin-bottom: 0.3in;
    letter-spacing: 1px;
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
  }}

  tr.part-row td {{
    font-weight: 700;
    font-size: 11pt;
    color: #7A209F;
    padding-top: 14px;
    padding-bottom: 4px;
    border-bottom: 2px solid #7A209F;
  }}

  td.ch-label {{
    width: 100px;
    font-weight: 600;
    color: #333;
    padding: 3px 0;
    white-space: nowrap;
  }}

  td.ch-title {{
    padding: 3px 8px;
    color: #1a1a2e;
  }}

  td.ch-page {{
    width: 35px;
    text-align: right;
    font-weight: 600;
    color: #008CB7;
    padding: 3px 0;
  }}

  tr.section-row td {{
    padding: 1px 0;
  }}

  td.sec-title {{
    padding: 1px 8px 1px 24px;
    color: #555;
    font-size: 9pt;
  }}

  td.sec-page {{
    width: 35px;
    text-align: right;
    color: #888;
    font-size: 9pt;
    padding: 1px 0;
  }}
</style>
</head>
<body>
  <h1>Detailed Contents</h1>
  <table>
    {rows_html}
  </table>
</body>
</html>"""


# ============================================================
# Step 4 & 5: Merge and add page numbers
# ============================================================

def generate_page_numbers_html(total_pages, skip_pages=0):
    """Create multi-page HTML where each page has a centered footer number.

    Args:
        total_pages: Total pages in the merged PDF
        skip_pages: Number of front-matter pages to leave unnumbered
    """
    pages = []
    for i in range(total_pages):
        if i < skip_pages:
            pages.append(
                '<div class="page"></div>'
            )
        else:
            page_num = i - skip_pages + 1
            pages.append(
                f'<div class="page">'
                f'<span class="num">{page_num}</span>'
                f'</div>'
            )

    pages_html = '\n'.join(pages)

    return f"""<!DOCTYPE html>
<html>
<head>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

  @page {{ size: letter portrait; margin: 0; }}

  * {{ margin: 0; padding: 0; }}

  body {{
    font-family: 'Inter', sans-serif;
  }}

  .page {{
    width: 8.5in;
    height: 11in;
    position: relative;
    page-break-after: always;
    background: transparent;
  }}

  .page:last-child {{
    page-break-after: auto;
  }}

  .num {{
    position: absolute;
    bottom: 0.4in;
    left: 0;
    right: 0;
    text-align: center;
    font-size: 10pt;
    font-weight: 400;
    color: #555;
  }}
</style>
</head>
<body>
  {pages_html}
</body>
</html>"""


# ============================================================
# Main compilation
# ============================================================

async def compile_book():
    """Main compilation routine."""

    print("=" * 60)
    print("  Compiling metricsAI Complete Book")
    print("=" * 60)

    # ----------------------------------------------------------
    # Step 1: Generate cover page PDF
    # ----------------------------------------------------------
    print("\n[1/7] Generating cover page...")
    cover_html = generate_cover_html()
    cover_pdf = PROJECT_ROOT / 'tmp_cover.pdf'
    await html_to_pdf(
        cover_html, cover_pdf,
        margins={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'},
        wait_ms=1000,
    )
    print(f"  Cover page: {PdfReader(str(cover_pdf)).pages[0].mediabox}")

    # ----------------------------------------------------------
    # Step 2: Count pages and extract sections
    # ----------------------------------------------------------
    print("\n[2/7] Counting chapter pages and extracting sections...")
    chapter_data = count_pages()
    total_chapter_pages = sum(ch['pages'] for ch in chapter_data)
    print(f"  {len(chapter_data)} chapters, {total_chapter_pages} pages")

    section_data = {}  # ch_id -> [(title, page_offset), ...]
    for ch in chapter_data:
        ch_id = ch['id']
        sections = extract_chapter_sections(ch_id)
        if sections:
            mapped = map_sections_to_pdf_pages(sections, ch['pdf_path'], ch_id)
            if mapped:
                section_data[ch_id] = mapped
                print(f"  {ch_id}: {len(mapped)} sections")

    total_sections = sum(len(v) for v in section_data.values())
    print(f"  Total: {total_sections} sections across {len(section_data)} chapters")

    # ----------------------------------------------------------
    # Step 3: Generate Brief Contents and Detailed Contents
    # ----------------------------------------------------------
    print("\n[3/7] Generating Tables of Contents...")

    brief_pdf = PROJECT_ROOT / 'tmp_brief_toc.pdf'
    brief_html = generate_brief_toc_html(chapter_data)
    await html_to_pdf(brief_html, brief_pdf, wait_ms=1000)
    brief_pages = len(PdfReader(str(brief_pdf)).pages)
    print(f"  Brief Contents: {brief_pages} page(s)")

    detailed_pdf = PROJECT_ROOT / 'tmp_detailed_toc.pdf'
    detailed_html = generate_detailed_toc_html(chapter_data, section_data)
    await html_to_pdf(detailed_html, detailed_pdf, wait_ms=1000)
    detailed_pages = len(PdfReader(str(detailed_pdf)).pages)
    print(f"  Detailed Contents: {detailed_pages} page(s)")

    toc_total_pages = brief_pages + detailed_pages

    # ----------------------------------------------------------
    # Step 4: Merge all PDFs
    # ----------------------------------------------------------
    print("\n[4/7] Merging PDFs...")
    writer = PdfWriter()

    # Add cover
    cover_reader = PdfReader(str(cover_pdf))
    for page in cover_reader.pages:
        writer.add_page(page)
    print("  + Cover (1 page)")

    # Add Brief Contents
    brief_reader = PdfReader(str(brief_pdf))
    for page in brief_reader.pages:
        writer.add_page(page)
    print(f"  + Brief Contents ({brief_pages} pages)")

    # Add Detailed Contents
    detailed_reader = PdfReader(str(detailed_pdf))
    for page in detailed_reader.pages:
        writer.add_page(page)
    print(f"  + Detailed Contents ({detailed_pages} pages)")

    # Add chapters
    for ch in chapter_data:
        reader = PdfReader(str(ch['pdf_path']))
        for page in reader.pages:
            writer.add_page(page)
        print(f"  + {ch['id']}: {ch['title']} ({ch['pages']} pages)")

    total_pages = len(writer.pages)
    front_matter = 1 + toc_total_pages  # cover + brief + detailed
    print(f"  Total: {total_pages} pages ({front_matter} front matter + {total_chapter_pages} content)")

    # Write unnumbered merged PDF to temp file
    merged_tmp = PROJECT_ROOT / 'tmp_merged.pdf'
    with open(merged_tmp, 'wb') as f:
        writer.write(f)

    # ----------------------------------------------------------
    # Step 5: Add page numbers
    # ----------------------------------------------------------
    print("\n[5/7] Adding page numbers...")
    numbers_pdf = PROJECT_ROOT / 'tmp_numbers.pdf'
    numbers_html = generate_page_numbers_html(total_pages, skip_pages=front_matter)
    await html_to_pdf(
        numbers_html, numbers_pdf,
        margins={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'},
        wait_ms=2000,
    )

    numbers_reader = PdfReader(str(numbers_pdf))
    print(f"  Number overlay: {len(numbers_reader.pages)} pages")

    # Overlay numbers onto merged PDF
    merged_reader = PdfReader(str(merged_tmp))
    final_writer = PdfWriter()

    for i in range(total_pages):
        page = merged_reader.pages[i]
        if i < len(numbers_reader.pages):
            number_page = numbers_reader.pages[i]
            page.merge_page(number_page)
        final_writer.add_page(page)

    # ----------------------------------------------------------
    # Step 6: Add PDF bookmarks (outline) with sections
    # ----------------------------------------------------------
    print("\n[6/7] Adding PDF bookmarks...")

    # Build chapter offset map (0-indexed physical page in final PDF)
    ch_offsets = {}  # ch_id -> physical page index
    page_idx = front_matter  # skip cover + TOC pages
    for ch in chapter_data:
        ch_offsets[ch['id']] = page_idx
        page_idx += ch['pages']

    # Add Preface bookmark with section sub-bookmarks
    if 'ch00' in ch_offsets:
        preface_ref = final_writer.add_outline_item(
            'Preface', ch_offsets['ch00'], bold=True,
        )
        print("  + Preface")
        if 'ch00' in section_data:
            for sec_title, sec_offset in section_data['ch00']:
                sec_page = ch_offsets['ch00'] + sec_offset
                final_writer.add_outline_item(
                    sec_title, sec_page, parent=preface_ref,
                )
                print(f"    . {sec_title}")

    # Add part and chapter bookmarks with section sub-bookmarks
    for part_name, part_chapters in PARTS:
        first_ch = part_chapters[0]
        part_ref = final_writer.add_outline_item(
            part_name, ch_offsets[first_ch],
            bold=True, color=(0.478, 0.125, 0.624),  # SynapsePurple
        )
        print(f"  + {part_name}")
        for ch_id in part_chapters:
            ch = next(c for c in chapter_data if c['id'] == ch_id)
            num = ch_id.replace('ch', '').lstrip('0')
            title = f'Chapter {num}: {ch["title"]}'
            ch_ref = final_writer.add_outline_item(
                title, ch_offsets[ch_id], parent=part_ref,
            )
            print(f"    - {title}")
            # Add section bookmarks under this chapter
            if ch_id in section_data:
                for sec_title, sec_offset in section_data[ch_id]:
                    sec_page = ch_offsets[ch_id] + sec_offset
                    final_writer.add_outline_item(
                        sec_title, sec_page, parent=ch_ref,
                    )

    # ----------------------------------------------------------
    # Step 7: Write final PDF
    # ----------------------------------------------------------
    print("\n[7/7] Writing final PDF...")
    with open(OUTPUT_PDF, 'wb') as f:
        final_writer.write(f)

    file_size_mb = OUTPUT_PDF.stat().st_size / (1024 * 1024)
    print(f"\n{'=' * 60}")
    print(f"  Book compiled successfully!")
    print(f"  Output: {OUTPUT_PDF}")
    print(f"  Size:   {file_size_mb:.1f} MB")
    print(f"  Pages:  {total_pages}")
    print(f"  Sections in bookmarks: {total_sections}")
    print(f"{'=' * 60}")

    # Clean up temp files
    for tmp in [cover_pdf, brief_pdf, detailed_pdf, merged_tmp, numbers_pdf]:
        if tmp.exists():
            tmp.unlink()

    return OUTPUT_PDF


def main():
    asyncio.run(compile_book())


if __name__ == '__main__':
    main()
