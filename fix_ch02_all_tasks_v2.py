#!/usr/bin/env python3
"""
Comprehensive fix for ALL task instruction cells in Chapter 2 Case Studies.
Manually specifies proper formatting for each task cell.
"""

import json

def get_task1_fixed():
    """Return properly formatted Task 1 cell."""
    return [
        "#### Task 1: Data Exploration (Guided)\n",
        "\n",
        "**Objective:** Load and explore the structure of the global productivity distribution.\n",
        "\n",
        "**Instructions:**\n",
        "\n",
        "1. Examine the productivity variable's basic structure (length, data type, any missing values)\n",
        "2. Get summary statistics (count, mean, std, min, max)\n",
        "3. Display observations for 5 different countries to see variation across countries\n",
        "4. Check: Is there variation across countries? Does it seem large or small?\n",
        "\n",
        "**Chapter 2 connection:** This applies the concepts from Section 2.1 (Summary Statistics).\n",
        "\n",
        "**Starter code guidance:**\n",
        "\n",
        "- Use `productivity.describe()` for summary statistics\n",
        "- Check for missing values with `productivity.isnull().sum()`\n",
        "- Use `.loc[]` or `.xs()` to select specific countries' observations\n",
        "- Calculate min and max productivity values globally"
    ]

def get_task2_fixed():
    """Return properly formatted Task 2 cell."""
    return [
        "#### Task 2: Summary Statistics (Semi-guided)\n",
        "\n",
        "**Objective:** Calculate comprehensive summary statistics for the global productivity distribution.\n",
        "\n",
        "**Instructions:**\n",
        "\n",
        "1. Compute mean, median, standard deviation, quartiles (25th, 50th, 75th percentiles)\n",
        "2. Calculate skewness and kurtosis for the overall productivity distribution\n",
        "3. Identify which countries have the highest and lowest productivity (across all years)\n",
        "4. Compare productivity statistics for two time periods: 1990 and 2014\n",
        "\n",
        "**Chapter 2 connection:** Applies Section 2.1 (Summary Statistics) and distribution shape measures.\n",
        "\n",
        "**Starter code guidance:**\n",
        "\n",
        "- Use `.describe()` for the main statistics\n",
        "- Use `scipy.stats.skew()` and `scipy.stats.kurtosis()` for shape measures\n",
        "- Filter by year: `df1.xs(1990, level='year')['lp']`\n",
        "- Use `.nlargest()` and `.nsmallest()` to find extreme values\n",
        "- Create a comparison table of statistics for different time periods"
    ]

def get_task3_fixed():
    """Return properly formatted Task 3 cell."""
    return [
        "#### Task 3: Visualizing Distributions (Semi-guided)\n",
        "\n",
        "**Objective:** Create multiple visualizations to understand the shape of the productivity distribution.\n",
        "\n",
        "**Instructions:**\n",
        "\n",
        "1. Create a histogram of productivity (try different bin widths)\n",
        "2. Create a box plot to identify outliers and quartiles\n",
        "3. Create a kernel density estimate to see the smooth shape\n",
        "4. Compare the original distribution to the log-transformed distribution\n",
        "\n",
        "**Chapter 2 connection:** Applies Section 2.2 (Charts for Numerical Data).\n",
        "\n",
        "**Starter code guidance:**\n",
        "\n",
        "- Use `plt.hist()` for histogram with different bin widths (try 10, 15, 20 bins)\n",
        "- Use `plt.boxplot()` for box plot visualization\n",
        "- Use `.plot.kde()` for kernel density estimate\n",
        "- Create side-by-side panels to compare original vs log-transformed\n",
        "- Label axes clearly and add titles"
    ]

def get_task4_fixed():
    """Return properly formatted Task 4 cell."""
    return [
        "#### Task 4: Comparing Distributions Across Time (More Independent)\n",
        "\n",
        "**Objective:** Analyze how the productivity distribution has changed from 1990 to 2014.\n",
        "\n",
        "**Instructions:**\n",
        "\n",
        "1. Extract productivity data for 1990 and 2014\n",
        "2. Calculate summary statistics for each year separately\n",
        "3. Create overlapping KDE plots to compare the distributions visually\n",
        "4. Analyze: Has the distribution shifted right (convergence/improvement)? Widened (divergence)? Changed shape?\n",
        "\n",
        "**Chapter 2 connection:** Applies Section 2.2 (comparing distributions across groups).\n",
        "\n",
        "**Starter code guidance:**\n",
        "\n",
        "- Use `df1.xs(year, level='year')` to extract data for specific years\n",
        "- Create summary statistics tables for comparison\n",
        "- Plot two KDE curves on the same axes with different colors\n",
        "- Use the 25th and 75th percentiles to measure spread\n",
        "- Calculate the coefficient of variation (std/mean) to compare relative dispersion"
    ]

def get_task5_fixed():
    """Return properly formatted Task 5 cell."""
    return [
        "#### Task 5: Transformation Analysis (Independent)\n",
        "\n",
        "**Objective:** Apply log transformation to productivity data and analyze the effect.\n",
        "\n",
        "**Instructions:**\n",
        "\n",
        "1. Create log-transformed productivity variable: log_productivity = ln(productivity)\n",
        "2. Compare skewness before and after transformation\n",
        "3. Create side-by-side histograms (original vs log-transformed)\n",
        "4. Calculate z-scores for both variables to standardize them\n",
        "5. Interpret: Why does log transformation help? When would you use it?\n",
        "\n",
        "**Chapter 2 connection:** Applies Section 2.5 (Data Transformation).\n",
        "\n",
        "**Starter code guidance:**\n",
        "\n",
        "- Use `np.log()` to create log transformation\n",
        "- Compare skewness values before/after using `stats.skew()`\n",
        "- Create z-scores with: `(x - x.mean()) / x.std()`\n",
        "- Visualize both original and log distributions in histograms\n",
        "- Discuss why log-normal distributions are common in economics"
    ]

def get_task6_fixed():
    """Return properly formatted Task 6 cell."""
    return [
        "#### Task 6: Regional Patterns (Independent)\n",
        "\n",
        "**Objective:** Compare productivity distributions across geographic regions.\n",
        "\n",
        "**Instructions:**\n",
        "\n",
        "1. Add a region column to your dataframe (you'll need to manually assign regions based on country names)\n",
        "2. Group countries by region (at minimum: Africa, Asia, Europe, Americas)\n",
        "3. Create box plots for each region side-by-side\n",
        "4. Calculate summary statistics by region\n",
        "5. Identify: Which regions have highest/lowest productivity? Most inequality?\n",
        "\n",
        "**Chapter 2 connection:** Applies Sections 2.3-2.4 (Charts for categorical breakdowns).\n",
        "\n",
        "**Starter code guidance:**\n",
        "\n",
        "- Create a dictionary mapping countries to regions\n",
        "- Use `.groupby()` to calculate statistics by region\n",
        "- Create side-by-side box plots for visual comparison\n",
        "- Calculate mean and standard deviation by region\n",
        "- Compare median productivity across regions"
    ]

def fix_notebook(notebook_path):
    """Fix all task cells in the notebook."""
    print(f"Reading notebook: {notebook_path}")

    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    cells_fixed = 0

    # Fix each task cell
    task_fixes = {
        64: ("Task 1", get_task1_fixed()),
        66: ("Task 2", get_task2_fixed()),
        68: ("Task 3", get_task3_fixed()),
        70: ("Task 4", get_task4_fixed()),
        72: ("Task 5", get_task5_fixed()),
        74: ("Task 6", get_task6_fixed())
    }

    for cell_idx, (task_name, fixed_source) in task_fixes.items():
        if len(nb['cells']) > cell_idx and nb['cells'][cell_idx]['cell_type'] == 'markdown':
            print(f"Fixing Cell {cell_idx}: {task_name}...")
            nb['cells'][cell_idx]['source'] = fixed_source
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
