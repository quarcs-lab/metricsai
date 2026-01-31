#!/usr/bin/env python3
"""
Comment out student exercise code with _____ placeholders in Chapter 2 Case Studies.

This prevents NameError when running the notebook, while maintaining pedagogical intent
by showing students what code they should complete.
"""

import json
import re


def comment_out_placeholder_lines(source):
    """
    Comment out lines containing _____ placeholders.
    Add STUDENT EXERCISE markers.

    Args:
        source: List of strings (cell source lines)

    Returns:
        Modified source with placeholders commented out
    """
    modified_source = []
    i = 0

    while i < len(source):
        line = source[i]

        # Check if line contains _____ placeholder
        if '_____' in line:
            # Add STUDENT EXERCISE comment before the line
            indent = len(line) - len(line.lstrip())
            modified_source.append(' ' * indent + '# STUDENT EXERCISE: Fill in the blank below\n')

            # Comment out the line with placeholder
            # Preserve indentation
            commented_line = line.lstrip()
            modified_source.append(' ' * indent + '# ' + commented_line)

            # If line doesn't end with \n, add it
            if not modified_source[-1].endswith('\n'):
                modified_source[-1] += '\n'
        else:
            # Keep line as-is
            modified_source.append(line)

        i += 1

    return modified_source


def fix_notebook(notebook_path):
    """Fix all code cells with _____ placeholders."""
    print(f"Reading notebook: {notebook_path}")

    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    cells_fixed = 0
    lines_commented = 0

    # Iterate through all cells
    for idx, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'code':
            # Check if cell contains _____ placeholders
            source_text = ''.join(cell['source'])

            if '_____' in source_text:
                print(f"\nFixing Cell {idx} (code cell with placeholders)...")

                # Count placeholders
                placeholder_count = source_text.count('_____')
                print(f"  Found {placeholder_count} placeholder(s)")

                # Comment out placeholder lines
                original_source = cell['source']
                modified_source = comment_out_placeholder_lines(original_source)

                # Update cell
                cell['source'] = modified_source
                cells_fixed += 1
                lines_commented += placeholder_count

    # Save the fixed notebook
    print(f"\nSaving fixed notebook...")
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)

    print(f"✓ Fixed {cells_fixed} code cells")
    print(f"✓ Commented out {lines_commented} lines with placeholders")
    print(f"✓ Notebook saved: {notebook_path}")

    return cells_fixed, lines_commented


if __name__ == '__main__':
    notebook_path = 'notebooks_colab/ch02_Univariate_Data_Summary.ipynb'
    cells_fixed, lines_commented = fix_notebook(notebook_path)

    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    print(f"Code cells fixed: {cells_fixed}")
    print(f"Lines commented out: {lines_commented}")
    print(f"\nNext steps:")
    print("1. Regenerate HTML: cd notebooks_colab && jupyter nbconvert --to html ch02_Univariate_Data_Summary.ipynb && cd ..")
    print("2. Inject CSS: python3 inject_print_css.py notebooks_colab/ch02_Univariate_Data_Summary.html notebooks_colab/ch02_Univariate_Data_Summary_printable.html")
    print("3. Generate PDF: python3 generate_pdf_playwright.py ch02")
    print("4. Verify notebook runs without errors")
