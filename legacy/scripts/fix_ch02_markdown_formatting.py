#!/usr/bin/env python3
"""
Fix markdown formatting issues in Chapter 2 notebook.

Problem: Markdown cells have text concatenated without proper newline characters,
causing text to run together in the PDF output.

Solution: Add proper newline characters (\n) between paragraphs, after headings,
and in bullet lists.
"""

import json
import re

def fix_chapter_overview(source):
    """Fix Cell 2 (Chapter Overview) formatting."""
    # Current source is one concatenated string - split it properly
    text = ''.join(source)

    # Split and rebuild with proper newlines
    fixed_lines = []

    # Add heading with newlines
    fixed_lines.append("## Chapter Overview\n")
    fixed_lines.append("\n")

    # Add intro paragraph
    fixed_lines.append("**Univariate data** consists of observations on a single variable—for example, annual earnings, individual income, or GDP over time. This chapter teaches you how to summarize and visualize such data effectively.\n")
    fixed_lines.append("\n")

    # Add "What you'll learn" section
    fixed_lines.append("**What you'll learn:**\n")
    fixed_lines.append("\n")
    fixed_lines.append("- Calculate summary statistics (mean, median, standard deviation, quartiles, skewness, kurtosis)\n")
    fixed_lines.append("- Create visualizations for numerical data (box plots, histograms, kernel density estimates, line charts)\n")
    fixed_lines.append("- Visualize categorical data (bar charts, pie charts)\n")
    fixed_lines.append("- Apply data transformations (logarithms, standardization)\n")
    fixed_lines.append("- Work with time series transformations (moving averages, seasonal adjustment)\n")
    fixed_lines.append("\n")

    # Add datasets section
    fixed_lines.append("**Datasets used:**\n")
    fixed_lines.append("\n")
    fixed_lines.append("- **AED_EARNINGS.DTA**: Annual earnings for 171 full-time working women aged 30 in 2010\n")
    fixed_lines.append("- **AED_REALGDPPC.DTA**: U.S. quarterly real GDP per capita from 1959 to 2020\n")
    fixed_lines.append("- **AED_HEALTHCATEGORIES.DTA**: U.S. health expenditures by category in 2018\n")
    fixed_lines.append("- **AED_FISHING.DTA**: Fishing site choices for 1,182 fishers\n")
    fixed_lines.append("- **AED_MONTHLYHOMESALES.DTA**: Monthly U.S. home sales from 1999 to 2015\n")
    fixed_lines.append("\n")

    # Add chapter outline
    fixed_lines.append("**Chapter outline:**\n")
    fixed_lines.append("\n")
    fixed_lines.append("- 2.1 Summary Statistics for Numerical Data\n")
    fixed_lines.append("- 2.2 Charts for Numerical Data\n")
    fixed_lines.append("- 2.3 Charts for Numerical Data by Category\n")
    fixed_lines.append("- 2.4 Charts for Categorical Data\n")
    fixed_lines.append("- 2.5 Data Transformation\n")
    fixed_lines.append("- 2.6 Data Transformations for Time Series Data\n")
    fixed_lines.append("- 2.7 Practice Exercises\n")
    fixed_lines.append("- 2.8 Case Studies")

    return fixed_lines

def fix_case_study_intro(source):
    """Fix Case Study introduction cell (Cell 60)."""
    text = ''.join(source)

    fixed_lines = []
    fixed_lines.append("### Case Study 1: Global Labor Productivity Distribution\n")
    fixed_lines.append("\n")
    fixed_lines.append("**Research Question:** How is labor productivity distributed across countries? Are there distinct groups or is it continuous?\n")
    fixed_lines.append("\n")
    fixed_lines.append("In Chapter 1, you examined *relationships between variables*—specifically, how productivity relates to capital stock through regression analysis. Now we shift perspective to analyze a *single variable*—labor productivity—but focus on its **distribution across countries** rather than its associations.\n")
    fixed_lines.append("\n")
    fixed_lines.append("This case study builds on Chapter 1's dataset (Convergence Clubs) but asks fundamentally different questions: What does the distribution of productivity look like across the 61 countries in our sample? Is it symmetric or skewed? Have productivity gaps widened or narrowed over time? These distributional questions are central to development economics and understanding global inequality.\n")
    fixed_lines.append("\n")
    fixed_lines.append("By completing this case study, you'll apply all the univariate analysis tools from Chapter 2 to a real dataset with genuine economic relevance—exploring whether productivity converges globally or if divergence persists.")

    return fixed_lines

def fix_notebook(notebook_path):
    """Main function to fix notebook formatting."""
    print(f"Reading notebook: {notebook_path}")

    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    cells_fixed = 0

    # Fix Cell 2 (Chapter Overview)
    if len(nb['cells']) > 2 and nb['cells'][2]['cell_type'] == 'markdown':
        print("Fixing Cell 2 (Chapter Overview)...")
        nb['cells'][2]['source'] = fix_chapter_overview(nb['cells'][2]['source'])
        cells_fixed += 1

    # Fix Cell 60 (Case Study introduction) - it's cell index 60
    if len(nb['cells']) > 60 and nb['cells'][60]['cell_type'] == 'markdown':
        print("Fixing Cell 60 (Case Study introduction)...")
        nb['cells'][60]['source'] = fix_case_study_intro(nb['cells'][60]['source'])
        cells_fixed += 1

    # Save the fixed notebook
    print(f"\nSaving fixed notebook...")
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)

    print(f"✓ Fixed {cells_fixed} cells")
    print(f"✓ Notebook saved: {notebook_path}")

    return cells_fixed

if __name__ == '__main__':
    notebook_path = 'notebooks_colab/ch02_Univariate_Data_Summary.ipynb'
    cells_fixed = fix_notebook(notebook_path)

    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    print(f"Cells fixed: {cells_fixed}")
    print(f"\nNext steps:")
    print("1. Regenerate HTML: cd notebooks_colab && jupyter nbconvert --to html ch02_Univariate_Data_Summary.ipynb")
    print("2. Inject CSS: python3 inject_print_css.py notebooks_colab/ch02_Univariate_Data_Summary.html notebooks_colab/ch02_Univariate_Data_Summary_printable.html")
    print("3. Generate PDF: python3 generate_pdf_playwright.py ch02")
    print("4. Verify formatting in PDF")
