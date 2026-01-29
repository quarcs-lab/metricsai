#!/usr/bin/env python3
"""
Generate PDF using Playwright for precise control over margins and headers/footers.

This script provides guaranteed control over:
- Exact margin sizes
- No headers/footers (explicit disable)
- Better CSS rendering
- Font loading

Usage:
    python generate_pdf_playwright.py ch00
    python generate_pdf_playwright.py ch01
    python generate_pdf_playwright.py notebooks_colab/ch05_Bivariate_Data_Summary_printable.html
    python generate_pdf_playwright.py --all
"""

import asyncio
from playwright.async_api import async_playwright
from pathlib import Path
import sys

async def generate_pdf_async(html_path, pdf_path, verbose=False):
    """
    Generate PDF with Playwright for precise control.

    Args:
        html_path: Path to input HTML file
        pdf_path: Path to output PDF file
        verbose: Show detailed progress

    Returns:
        Path to generated PDF
    """
    html_path = Path(html_path).resolve()
    pdf_path = Path(pdf_path).resolve()

    if verbose:
        print(f"  Loading: {html_path}")
        print(f"  Output:  {pdf_path}")

    async with async_playwright() as p:
        # Launch Chromium
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Load HTML file
        await page.goto(f'file://{html_path}')

        # Wait for everything to load (fonts, images, CSS)
        await page.wait_for_load_state('networkidle')
        await page.wait_for_timeout(1000)  # Extra wait for Google Fonts

        if verbose:
            print(f"  Rendering PDF...")

        # Generate PDF with explicit settings
        await page.pdf(
            path=str(pdf_path),
            format='Letter',              # 8.5" x 11"
            print_background=True,         # Include background colors/images
            margin={
                'top': '0.75in',           # Top margin
                'right': '0.75in',         # Right margin (increased to match left)
                'bottom': '0.75in',        # Bottom margin
                'left': '0.75in'           # Left margin (increased to match top/bottom)
            },
            display_header_footer=False,   # EXPLICITLY NO HEADERS/FOOTERS
            prefer_css_page_size=True      # Respect CSS @page rules
        )

        await browser.close()

    return pdf_path

def generate_pdf(html_path, pdf_path, verbose=False):
    """Synchronous wrapper for async function."""
    return asyncio.run(generate_pdf_async(html_path, pdf_path, verbose))

def find_printable_html(chapter_id):
    """
    Find the printable HTML file for a given chapter.

    Args:
        chapter_id: Chapter identifier (e.g., 'ch00', '00', '0')

    Returns:
        Path to HTML file

    Raises:
        FileNotFoundError: If no matching file found
    """
    # Normalize chapter ID to ch## format
    if chapter_id.startswith('ch'):
        ch_id = chapter_id
    else:
        ch_id = f"ch{chapter_id.zfill(2)}"

    # Search for matching file
    notebooks_dir = Path('notebooks_colab')
    pattern = f"{ch_id}*_printable.html"
    matches = list(notebooks_dir.glob(pattern))

    if not matches:
        raise FileNotFoundError(f"No printable HTML found for chapter: {chapter_id}")

    if len(matches) > 1:
        print(f"Warning: Multiple files found for {chapter_id}, using first: {matches[0].name}")

    return matches[0]

def process_all(output_dir=None, verbose=False):
    """
    Process all *_printable.html files in notebooks_colab/.

    Args:
        output_dir: Directory to save PDFs (default: same as HTML)
        verbose: Show detailed progress

    Returns:
        List of (html_path, pdf_path) tuples for successful conversions
    """
    notebooks_dir = Path('notebooks_colab')
    html_files = sorted(notebooks_dir.glob('*_printable.html'))

    if not html_files:
        print("No *_printable.html files found in notebooks_colab/")
        return []

    print(f"Found {len(html_files)} printable HTML files")
    print("="*70)

    results = []
    errors = []

    for html_path in html_files:
        try:
            # Determine output path
            if output_dir:
                output_dir_path = Path(output_dir)
                output_dir_path.mkdir(parents=True, exist_ok=True)
                pdf_name = html_path.stem.replace('_printable', '') + '.pdf'
                pdf_path = output_dir_path / pdf_name
            else:
                pdf_name = html_path.stem.replace('_printable', '') + '.pdf'
                pdf_path = html_path.parent / pdf_name

            print(f"Processing: {html_path.name}")
            generated_pdf = generate_pdf(html_path, pdf_path, verbose)

            file_size_mb = generated_pdf.stat().st_size / (1024 * 1024)
            print(f"✓ Created: {generated_pdf.name} ({file_size_mb:.2f} MB)")

            results.append((html_path, generated_pdf))

        except Exception as e:
            print(f"✗ Failed: {html_path.name} - {e}")
            errors.append((html_path, str(e)))

    print("="*70)
    print(f"Summary: {len(results)} successful, {len(errors)} failed")

    return results

def main():
    """Main entry point."""
    args = sys.argv[1:]

    if not args or '--help' in args or '-h' in args:
        print(__doc__)
        return

    verbose = '--verbose' in args
    if verbose:
        args.remove('--verbose')

    # Handle --all flag
    if '--all' in args:
        args.remove('--all')

        # Check for --output-dir
        output_dir = None
        if '--output-dir' in args:
            idx = args.index('--output-dir')
            if idx + 1 < len(args):
                output_dir = args[idx + 1]
                args.remove('--output-dir')
                args.remove(output_dir)

        process_all(output_dir, verbose)
        return

    # Handle --output-dir for single file
    output_dir = None
    if '--output-dir' in args:
        idx = args.index('--output-dir')
        if idx + 1 < len(args):
            output_dir = args[idx + 1]
            args.remove('--output-dir')
            args.remove(output_dir)

    if not args:
        print("Error: No input file or chapter specified")
        print("Use --help for usage information")
        sys.exit(1)

    input_arg = args[0]

    try:
        # Check if input is a file path
        if Path(input_arg).exists():
            html_path = Path(input_arg)
        else:
            # Try to find chapter HTML
            html_path = find_printable_html(input_arg)

        # Determine output path
        if output_dir:
            output_dir_path = Path(output_dir)
            output_dir_path.mkdir(parents=True, exist_ok=True)
            pdf_name = html_path.stem.replace('_printable', '') + '.pdf'
            pdf_path = output_dir_path / pdf_name
        else:
            pdf_name = html_path.stem.replace('_printable', '') + '.pdf'
            pdf_path = html_path.parent / pdf_name

        print(f"Generating PDF from {html_path.name}...")

        generated_pdf = generate_pdf(html_path, pdf_path, verbose)

        file_size_mb = generated_pdf.stat().st_size / (1024 * 1024)
        print(f"✓ PDF created: {generated_pdf} ({file_size_mb:.2f} MB)")

        # Offer to open
        print(f"\nTo view: open {generated_pdf}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
