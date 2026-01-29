#!/usr/bin/env python3
"""
Generate PDF from print-ready HTML using Chrome headless.

This script automates PDF generation from HTML files, eliminating the need
for manual browser printing (Cmd+P).

Usage:
    python generate_pdf.py ch00                    # Generate from ch00_Preface_printable.html
    python generate_pdf.py ch01                    # Generate from ch01_*_printable.html
    python generate_pdf.py file.html              # Generate from specific HTML file
    python generate_pdf.py --all                   # Generate all *_printable.html files
    python generate_pdf.py --all --output-dir pdfs # Generate all, save to pdfs/

Options:
    --output-dir DIR    Save PDFs to specified directory (default: same as HTML)
    --all               Process all *_printable.html files in notebooks_colab/
    --verbose           Show detailed progress information
    --help              Show this help message

Examples:
    python generate_pdf.py ch00
    python generate_pdf.py notebooks_colab/ch05_Bivariate_Data_Summary_printable.html
    python generate_pdf.py --all --output-dir notebooks_pdf
"""

import subprocess
import sys
from pathlib import Path
import glob

# Chrome executable path (macOS)
CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

def generate_pdf(html_path, pdf_path=None, verbose=False):
    """
    Generate PDF from HTML using Chrome headless.

    Args:
        html_path: Path to input HTML file
        pdf_path: Path to output PDF file (default: same as HTML with .pdf extension)
        verbose: Show detailed progress

    Returns:
        Path to generated PDF file

    Raises:
        FileNotFoundError: If HTML file doesn't exist
        RuntimeError: If PDF generation fails
    """
    html_path = Path(html_path).resolve()

    if not html_path.exists():
        raise FileNotFoundError(f"HTML file not found: {html_path}")

    # Determine output PDF path
    if pdf_path is None:
        # Replace .html with .pdf, remove _printable if present
        if '_printable' in html_path.stem:
            pdf_name = html_path.stem.replace('_printable', '') + '.pdf'
        else:
            pdf_name = html_path.stem + '.pdf'
        pdf_path = html_path.parent / pdf_name
    else:
        pdf_path = Path(pdf_path).resolve()

    # Ensure output directory exists
    pdf_path.parent.mkdir(parents=True, exist_ok=True)

    if verbose:
        print(f"  Input:  {html_path}")
        print(f"  Output: {pdf_path}")

    # Build Chrome headless command
    cmd = [
        CHROME_PATH,
        "--headless",
        "--disable-gpu",
        f"--print-to-pdf={pdf_path}",
        "--print-to-pdf-no-header",
        "--disable-pdf-tagging",
        "--run-all-compositor-stages-before-draw",
        f"file://{html_path}"
    ]

    # Run Chrome headless
    result = subprocess.run(cmd, capture_output=True, text=True)

    # Check for success
    if result.returncode == 0 and pdf_path.exists():
        return pdf_path
    else:
        error_msg = result.stderr if result.stderr else "Unknown error"
        raise RuntimeError(f"PDF generation failed: {error_msg}")

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
                pdf_path = None

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

def print_help():
    """Print help message."""
    print(__doc__)

def main():
    """Main entry point."""
    args = sys.argv[1:]

    if not args or '--help' in args or '-h' in args:
        print_help()
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
            pdf_path = None

        print(f"Generating PDF from {html_path.name}...")

        generated_pdf = generate_pdf(html_path, pdf_path, verbose)

        file_size_mb = generated_pdf.stat().st_size / (1024 * 1024)
        print(f"✓ PDF created: {generated_pdf} ({file_size_mb:.2f} MB)")

        # Offer to open
        print(f"\nTo view: open {generated_pdf}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except RuntimeError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
