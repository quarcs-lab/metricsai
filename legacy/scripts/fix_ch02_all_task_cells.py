#!/usr/bin/env python3
"""
Comprehensive fix for ALL task instruction cells in Chapter 2 Case Studies.

This script fixes markdown formatting for ALL task cells (Task 1-6) by adding
proper newline characters between sections.
"""

import json

def fix_task_cell(source_text):
    """Generic function to fix any task instruction cell."""
    lines = []

    # Split the text into sections
    if "**Objective:**" in source_text:
        # Extract components
        parts = source_text.split("**Objective:**")
        header = parts[0].strip()

        rest = parts[1]

        # Add header
        lines.append(f"{header}\n")
        lines.append("\n")

        # Split on instructions
        if "**Instructions:**" in rest:
            obj_parts = rest.split("**Instructions:**")
            objective = obj_parts[0].strip()

            lines.append(f"**Objective:** {objective}\n")
            lines.append("\n")
            lines.append("**Instructions:**\n")
            lines.append("\n")

            # Get rest
            rest_text = obj_parts[1]

            # Find Chapter 2 connection
            if "**Chapter 2 connection:**" in rest_text:
                instr_parts = rest_text.split("**Chapter 2 connection:**")
                instructions = instr_parts[0].strip()

                # Split instructions into numbered items
                import re
                inst_items = re.split(r'(\d+\.)', instructions)
                for i, item in enumerate(inst_items):
                    if item.strip():
                        if re.match(r'\d+\.', item):
                            lines.append(f"{item} ")
                        else:
                            lines.append(f"{item.strip()}\n")

                lines.append("\n")

                # Add Chapter 2 connection
                ch2_parts = instr_parts[1].split("**Starter code guidance:**") if "**Starter code guidance:**" in instr_parts[1] else [instr_parts[1], ""]
                lines.append(f"**Chapter 2 connection:** {ch2_parts[0].strip()}\n")
                lines.append("\n")

                # Add starter code guidance if present
                if len(ch2_parts) > 1 and ch2_parts[1].strip():
                    lines.append("**Starter code guidance:**\n")
                    lines.append("\n")

                    # Split guidance into bullet points
                    guidance_items = re.split(r'(-\s)', ch2_parts[1])
                    for j, item in enumerate(guidance_items):
                        if item.strip():
                            if item.strip() == '-':
                                lines.append("- ")
                            else:
                                lines.append(f"{item.strip()}\n")

    return lines

def fix_notebook(notebook_path):
    """Fix all task cells in the notebook."""
    print(f"Reading notebook: {notebook_path}")

    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    cells_fixed = 0

    # Task cell indices (markdown cells only)
    task_cells = {
        64: "Task 1: Data Exploration (Guided)",
        66: "Task 2: Summary Statistics (Semi-guided)",
        68: "Task 3: Visualizing Distributions (Semi-guided)",
        70: "Task 4: Comparing Distributions Across Time (More Independent)",
        72: "Task 5: Transformation Analysis (Independent)",
        74: "Task 6: Regional Patterns (Independent)"
    }

    for cell_idx, task_name in task_cells.items():
        if len(nb['cells']) > cell_idx and nb['cells'][cell_idx]['cell_type'] == 'markdown':
            print(f"Fixing Cell {cell_idx}: {task_name}...")
            source_text = ''.join(nb['cells'][cell_idx]['source'])
            nb['cells'][cell_idx]['source'] = fix_task_cell(source_text)
            cells_fixed += 1

    # Save the fixed notebook
    print(f"\nSaving fixed notebook...")
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)

    print(f"✓ Fixed {cells_fixed} task cells")
    print(f"✓ Notebook saved: {notebook_path}")

    return cells_fixed

if __name__ == '__main__':
    notebook_path = 'notebooks_colab/ch02_Univariate_Data_Summary.ipynb'
    cells_fixed = fix_notebook(notebook_path)

    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    print(f"Task cells fixed: {cells_fixed}")
    print(f"\nNext steps:")
    print("1. Regenerate HTML: cd notebooks_colab && jupyter nbconvert --to html ch02_Univariate_Data_Summary.ipynb")
    print("2. Inject CSS: python3 inject_print_css.py notebooks_colab/ch02_Univariate_Data_Summary.html notebooks_colab/ch02_Univariate_Data_Summary_printable.html")
    print("3. Generate PDF: python3 generate_pdf_playwright.py ch02")
    print("4. Verify formatting in PDF")
