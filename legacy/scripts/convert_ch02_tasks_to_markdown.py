#!/usr/bin/env python3
"""
Convert Chapter 2 Case Studies tasks from code cells to markdown with embedded code examples.

This script:
1. Deletes duplicate cell 69 (Task 3 instruction)
2. Merges instruction + code cells for Tasks 1-6 into combined markdown cells
3. Applies progressive scaffolding (placeholders) based on difficulty level
4. Adds usage instructions for students

Result: 80 cells → 73 cells (7 task markdown cells including usage instructions)
"""

import json
import re


def delete_duplicate_cell_69(nb):
    """Delete cell 69 (duplicate Task 3 instruction)."""
    if len(nb['cells']) > 69:
        print(f"Deleting cell 69 (duplicate Task 3 instruction)...")
        del nb['cells'][69]
        print(f"✓ Cell 69 deleted. New cell count: {len(nb['cells'])}")
    return nb


def create_usage_instructions():
    """Create usage instructions markdown cell to insert before Task 1."""
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### How to Use These Tasks\n",
            "\n",
            "**Instructions:**\n",
            "\n",
            "1. **Read the task objectives and instructions** in each section below\n",
            "2. **Review the example code structure** provided\n",
            "3. **Create a NEW code cell** to write your solution\n",
            "4. **Follow the structure and fill in the blanks** or write complete code\n",
            "5. **Run and test your code**\n",
            "6. **Answer the interpretation questions**\n",
            "\n",
            "**Progressive difficulty:**\n",
            "\n",
            "- **Tasks 1-2:** Guided (fill in specific blanks with `_____`)\n",
            "- **Task 3:** Semi-guided (complete partial code structure)\n",
            "- **Tasks 4-6:** Independent (write full code from outline)\n",
            "\n",
            "**Tip:** Type the code yourself rather than copying—it builds understanding!"
        ]
    }


def create_task1_markdown(instruction_source, code_source):
    """Task 1: GUIDED - Keep existing placeholder structure."""
    # Extract code with preserved placeholders
    code_text = ''.join(code_source)

    # Clean up the code - remove "# STUDENT EXERCISE" lines and uncomment placeholder lines
    code_lines = code_text.split('\n')
    cleaned_lines = []

    i = 0
    while i < len(code_lines):
        line = code_lines[i]

        # Skip "# STUDENT EXERCISE" marker lines
        if '# STUDENT EXERCISE' in line:
            i += 1
            continue

        # Uncomment lines that have placeholders (were commented by previous script)
        if line.strip().startswith('# ') and '_____' in line:
            # Uncomment the line
            cleaned_line = re.sub(r'^(\s*)# ', r'\1', line)
            cleaned_lines.append(cleaned_line)
        else:
            cleaned_lines.append(line)

        i += 1

    code_text = '\n'.join(cleaned_lines)

    # Build combined markdown
    instruction_text = ''.join(instruction_source)

    combined = []
    combined.extend(instruction_source)
    combined.append("\n")
    combined.append("**Example code structure:**\n")
    combined.append("\n")
    combined.append("```python\n")
    combined.append(code_text)
    combined.append("\n```\n")

    return combined


def create_task2_markdown(instruction_source, code_source):
    """Task 2: SEMI-GUIDED - Medium scaffolding with key blanks."""
    code_text = '''# Task 2: Summary Statistics (SEMI-GUIDED)
# Complete the code by implementing each step

# Step 1: Overall summary statistics
overall_stats = {
    'Mean': productivity.mean(),
    'Median': _____,  # Calculate median
    'Std Dev': _____,  # Calculate standard deviation
    'Skewness': stats.skew(_____),
    'Kurtosis': _____,  # Calculate kurtosis
    '25th percentile': productivity.quantile(0.25),
    '75th percentile': productivity.quantile(_____),
    'IQR': productivity.quantile(0.75) - productivity.quantile(0.25)
}

for key, value in overall_stats.items():
    print(f"{key:20s}: {value:.4f}")

# Step 2: Countries with highest/lowest productivity
print("\\n" + "=" * 70)
print("Top 5 Most Productive Countries (average across years)")
print("=" * 70)
country_means = df1.groupby(_____)['lp'].mean().sort_values(_____)
print(country_means.head())

print("\\n" + "=" * 70)
print("Top 5 Least Productive Countries (average across years)")
print("=" * 70)
print(country_means.tail())

# Step 3: Compare 1990 vs 2014
productivity_1990 = df1.xs(1990, level=_____)['lp']
productivity_2014 = df1.xs(_____, level='year')['lp']

# Your code here: Create a comparison DataFrame
# Hint: Use pd.DataFrame() with statistics for both years
# Include: mean, median, std, skewness, min, max'''

    instruction_text = ''.join(instruction_source)

    combined = []
    combined.extend(instruction_source)
    combined.append("\n")
    combined.append("**Example code structure:**\n")
    combined.append("\n")
    combined.append("```python\n")
    combined.append(code_text)
    combined.append("\n```\n")
    combined.append("\n")
    combined.append("**Hints:**\n")
    combined.append("\n")
    combined.append("- Use `.median()`, `.std()` for missing statistics\n")
    combined.append("- `stats.kurtosis()` requires the data series as input\n")
    combined.append("- `.groupby('country')` groups by country name\n")
    combined.append("- `.sort_values(ascending=False)` sorts from high to low\n")
    combined.append("- `.xs(year, level='year')` extracts data for a specific year\n")

    return combined


def create_task3_markdown(instruction_source, code_source):
    """Task 3: SEMI-GUIDED - Medium scaffolding with plot structure."""
    code_text = '''# Task 3: Visualizing Distributions (SEMI-GUIDED)
# Create comprehensive visualizations of the productivity distribution

# Create a 2x2 figure with 4 subplots
fig, axes = plt.subplots(_____, _____, figsize=(14, 10))

# Panel 1: Histogram (original productivity)
axes[0, 0].hist(productivity, bins=_____, edgecolor='black', alpha=0.7, color='steelblue')
axes[0, 0].set_xlabel(_____, fontsize=11)
axes[0, 0].set_ylabel(_____, fontsize=11)
axes[0, 0].set_title('Panel 1: Histogram of Productivity (20 bins)', fontsize=12, fontweight='bold')
axes[0, 0].grid(True, alpha=0.3)

# Panel 2: Box plot (original productivity)
axes[0, 1].boxplot(_____, vert=True, patch_artist=True)
axes[0, 1].set_ylabel('Labor Productivity', fontsize=11)
axes[0, 1].set_title('Panel 2: Box Plot of Productivity', fontsize=12, fontweight='bold')
axes[0, 1].grid(True, alpha=0.3, axis='y')

# Panel 3: KDE (original productivity)
productivity.plot.kde(ax=_____, linewidth=2, color='darkblue')
axes[1, 0].set_xlabel('Labor Productivity', fontsize=11)
axes[1, 0].set_ylabel('Density', fontsize=11)
axes[1, 0].set_title('Panel 3: Kernel Density Estimate', fontsize=12, fontweight='bold')
axes[1, 0].grid(True, alpha=0.3)

# Panel 4: KDE comparison (original vs log-transformed)
# Your code here: Create log-transformed productivity
log_productivity = np.log(productivity)

# Your code here: Plot both KDE curves on the same axes
# Hint: Use .plot.kde() with label='Original' and label='Log-transformed'
# Use different colors and linestyles for clarity

plt.suptitle('Figure: Global Productivity Distribution Visualizations', fontsize=14, fontweight='bold', y=1.00)
plt.tight_layout()
plt.show()'''

    instruction_text = ''.join(instruction_source)

    combined = []
    combined.extend(instruction_source)
    combined.append("\n")
    combined.append("**Example code structure:**\n")
    combined.append("\n")
    combined.append("```python\n")
    combined.append(code_text)
    combined.append("\n```\n")
    combined.append("\n")
    combined.append("**Hints:**\n")
    combined.append("\n")
    combined.append("- `plt.subplots(2, 2)` creates 2 rows and 2 columns\n")
    combined.append("- Try `bins=20` for the histogram\n")
    combined.append("- Set xlabel to 'Labor Productivity'\n")
    combined.append("- For boxplot, pass the productivity series directly\n")
    combined.append("- Use `axes[1, 0]` to reference the bottom-left panel\n")
    combined.append("- For KDE comparison, plot two curves with different colors (e.g., 'darkblue' and 'red')\n")

    return combined


def create_task4_markdown(instruction_source, code_source):
    """Task 4: MORE INDEPENDENT - Light scaffolding with step outline."""
    code_text = '''# Task 4: Comparing Distributions Across Time (MORE INDEPENDENT)
# Analyze how global productivity distribution evolved from 1990 to 2014

# Step 1: Extract data for 1990 and 2014
prod_1990 = df1.xs(_____, level='year')['lp']
prod_2014 = _____  # Extract 2014 data (same pattern as above)

# Step 2: Create comparison visualization
# Your code here: Create figure with 2 subplots (1 row, 2 columns)
# Hint: fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Panel A: Overlapping KDE plots
# Your code here: Plot KDE for both years on the same axes
# - Use prod_1990.plot.kde() and prod_2014.plot.kde()
# - Different colors for each year (e.g., 'darkblue' and 'red')
# - Add labels and legend

# Panel B: Side-by-side box plots
# Your code here: Create box plots for both years
# Hint: axes[1].boxplot([prod_1990, prod_2014], labels=['1990', '2014'])
# Set different colors for each box using patch_artist=True

# Step 3: Calculate comparison statistics
# Your code here: Create a DataFrame comparing statistics for both years
# Include: mean, median, std, coefficient of variation, skewness, min, max, range
# Hint: Use pd.DataFrame() with a dictionary of statistics'''

    instruction_text = ''.join(instruction_source)

    combined = []
    combined.extend(instruction_source)
    combined.append("\n")
    combined.append("**Example code structure:**\n")
    combined.append("\n")
    combined.append("```python\n")
    combined.append(code_text)
    combined.append("\n```\n")
    combined.append("\n")
    combined.append("**Hints:**\n")
    combined.append("\n")
    combined.append("- Coefficient of variation = std / mean (relative dispersion)\n")
    combined.append("- Use `stats.skew()` from scipy.stats for skewness\n")
    combined.append("- For KDE plots, use `label='1990'` and `label='2014'` for legend\n")
    combined.append("- Range = max - min\n")
    combined.append("\n")
    combined.append("**Questions to consider:**\n")
    combined.append("\n")
    combined.append("- Did mean productivity increase from 1990 to 2014?\n")
    combined.append("- Did the spread (std dev) increase or decrease? (Convergence vs divergence)\n")
    combined.append("- Did the coefficient of variation change?\n")
    combined.append("- Did skewness change?\n")

    return combined


def create_task5_markdown(instruction_source, code_source):
    """Task 5: INDEPENDENT - Minimal scaffolding with step outline."""
    code_text = '''# Task 5: Transformation Analysis (INDEPENDENT)
# Apply log transformation to understand how it affects the distribution

# Step 1: Create log transformation
# Your code here: log_productivity = np.log(_____)

# Step 2: Create z-scores (standardized values)
# Your code here: Calculate z-scores for both distributions
# Formula: z = (x - mean) / std
# z_productivity = (productivity - productivity.mean()) / productivity.std()
# z_log_productivity = ?

# Step 3: Create side-by-side histograms
# Your code here: Use plt.subplots(1, 2) for 2 panels
# Panel A: Original productivity histogram (20 bins, blue color)
# Panel B: Log-transformed histogram (20 bins, coral/red color)

# Step 4: Compare skewness
# Your code here: Calculate skewness using stats.skew()
# Calculate percentage reduction: (1 - |skew_log| / |skew_original|) * 100
# Print comparison table showing: mean, median, std, skewness, kurtosis, min, max'''

    instruction_text = ''.join(instruction_source)

    combined = []
    combined.extend(instruction_source)
    combined.append("\n")
    combined.append("**Example code structure:**\n")
    combined.append("\n")
    combined.append("```python\n")
    combined.append(code_text)
    combined.append("\n```\n")
    combined.append("\n")
    combined.append("**Hints:**\n")
    combined.append("\n")
    combined.append("- `np.log()` computes natural logarithm\n")
    combined.append("- Z-scores standardize data to mean=0, std=1\n")
    combined.append("- Use `stats.skew()` and `stats.kurtosis()` for shape measures\n")
    combined.append("- Compare absolute skewness values to quantify reduction\n")
    combined.append("\n")
    combined.append("**Questions to consider:**\n")
    combined.append("\n")
    combined.append("- Is the log-transformed distribution more symmetric?\n")
    combined.append("- When would you use log transformation in economic analysis?\n")
    combined.append("- What happened to skewness and kurtosis after transformation?\n")

    return combined


def create_task6_markdown(instruction_source, code_source):
    """Task 6: INDEPENDENT - Minimal scaffolding with conceptual guidance."""
    code_text = '''# Task 6: Regional Patterns (INDEPENDENT)
# Compare productivity distributions across geographic regions

# Step 1: Create region mapping dictionary
# Your code here: Define region_mapping
# Map each country to its region (Africa, Americas, Asia, Europe, Middle East, Asia-Pacific)
# Example structure:
# region_mapping = {
#     'Australia': 'Asia-Pacific',
#     'Austria': 'Europe',
#     'Brazil': 'Americas',
#     # ... continue for all ~50 countries
# }

# Step 2: Add region column to dataframe
# Your code here: Create a copy of df1 and add region column
# Hint: df_with_region['region'] = df_with_region.index.get_level_values('country').map(region_mapping)
# Remove rows with missing regions: .dropna(subset=['region'])

# Step 3: Calculate regional statistics
# Your code here: Group by region and aggregate statistics
# Hint: df_with_region.groupby('region')['lp'].agg(['count', 'mean', 'median', 'std', 'min', 'max'])
# Sort by mean productivity (descending)

# Step 4: Create box plots by region
# Your code here: Create boxplot visualization comparing regions
# - Extract data for each region: [df[df['region'] == r]['lp'].values for r in regions]
# - Sort regions by mean productivity for better readability
# - Use plt.boxplot() with labels for each region
# - Rotate x-axis labels for readability'''

    instruction_text = ''.join(instruction_source)

    combined = []
    combined.extend(instruction_source)
    combined.append("\n")
    combined.append("**Example code structure:**\n")
    combined.append("\n")
    combined.append("```python\n")
    combined.append(code_text)
    combined.append("\n```\n")
    combined.append("\n")
    combined.append("**Hints:**\n")
    combined.append("\n")
    combined.append("- There are ~50 countries in the dataset - you'll need to map each one\n")
    combined.append("- Regions: Africa (Kenya, Nigeria, etc.), Americas (USA, Brazil, etc.), Asia (China, India, etc.)\n")
    combined.append("- Europe (France, Germany, etc.), Middle East (Israel, Turkey), Asia-Pacific (Australia, Japan, NZ)\n")
    combined.append("- Use `.groupby('region')['lp'].agg([...])` to calculate statistics by region\n")
    combined.append("- Sort regions by mean before plotting for better visualization\n")
    combined.append("\n")
    combined.append("**Questions to consider:**\n")
    combined.append("\n")
    combined.append("- Which region has the highest average productivity?\n")
    combined.append("- Which region has the most internal inequality (widest box)?\n")
    combined.append("- Are there clear regional clusters or is variation continuous?\n")

    return combined


def convert_tasks_to_markdown(notebook_path):
    """Main conversion function."""
    print(f"Reading notebook: {notebook_path}")

    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    print(f"Original cell count: {len(nb['cells'])}")

    # Step 1: Delete duplicate cell 69
    nb = delete_duplicate_cell_69(nb)

    # After deleting cell 69, indices shift down by 1 for cells 70+
    # Original indices → New indices after deletion:
    # 64 (Task 1 inst) → 64
    # 65 (Task 1 code) → 65
    # 66 (Task 2 inst) → 66
    # 67 (Task 2 code) → 67
    # 68 (Task 3 inst) → 68
    # 69 (DELETED)
    # 70 (Task 3 code) → 69
    # 71 (Task 4 inst) → 70
    # 72 (Task 4 code) → 71
    # 73 (Task 5 inst) → 72
    # 74 (Task 5 code) → 73
    # 76 (Task 6 inst) → 75
    # 77 (Task 6 code) → 76

    # Step 2: Create usage instructions and insert before Task 1
    print("\nCreating usage instructions cell...")
    usage_cell = create_usage_instructions()
    nb['cells'].insert(64, usage_cell)  # Insert before Task 1
    print("✓ Usage instructions inserted at cell 64")

    # After inserting usage cell, all subsequent indices shift up by 1:
    # 64 → Usage instructions (NEW)
    # 65 → Task 1 inst
    # 66 → Task 1 code
    # 67 → Task 2 inst
    # 68 → Task 2 code
    # 69 → Task 3 inst
    # 70 → Task 3 code
    # 71 → Task 4 inst
    # 72 → Task 4 code
    # 73 → Task 5 inst
    # 74 → Task 5 code
    # 76 → Task 6 inst
    # 77 → Task 6 code

    # Step 3: Convert tasks to combined markdown (working backwards to preserve indices)
    tasks = [
        (77, 76, 6, "Task 6", create_task6_markdown),
        (74, 73, 5, "Task 5", create_task5_markdown),
        (72, 71, 4, "Task 4", create_task4_markdown),
        (70, 69, 3, "Task 3", create_task3_markdown),
        (68, 67, 2, "Task 2", create_task2_markdown),
        (66, 65, 1, "Task 1", create_task1_markdown),
    ]

    for code_idx, inst_idx, task_num, task_name, merge_func in tasks:
        print(f"\nConverting {task_name}...")
        print(f"  Instruction cell: {inst_idx}")
        print(f"  Code cell: {code_idx}")

        # Get instruction and code
        instruction_source = nb['cells'][inst_idx]['source']
        code_source = nb['cells'][code_idx]['source']

        # Create combined markdown
        combined_source = merge_func(instruction_source, code_source)

        # Replace instruction cell with combined markdown
        nb['cells'][inst_idx]['source'] = combined_source

        # Delete code cell
        del nb['cells'][code_idx]
        print(f"✓ {task_name} converted and merged into cell {inst_idx}")

    # Save modified notebook
    print(f"\nSaving modified notebook...")
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)

    print(f"✓ Notebook saved")
    print(f"✓ Final cell count: {len(nb['cells'])} (was 80, now 73)")

    return len(nb['cells'])


if __name__ == '__main__':
    notebook_path = 'notebooks_colab/ch02_Univariate_Data_Summary.ipynb'
    final_count = convert_tasks_to_markdown(notebook_path)

    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    print(f"✓ Deleted duplicate cell 69 (Task 3 instruction)")
    print(f"✓ Added usage instructions before Task 1")
    print(f"✓ Converted 6 tasks from code cells to markdown with examples")
    print(f"✓ Applied progressive scaffolding (Guided → Independent)")
    print(f"✓ Final cell count: {final_count} (reduced from 80)")
    print(f"\nNext steps:")
    print("1. Regenerate HTML: cd notebooks_colab && jupyter nbconvert --to html ch02_Univariate_Data_Summary.ipynb && cd ..")
    print("2. Inject CSS: python3 inject_print_css.py notebooks_colab/ch02_Univariate_Data_Summary.html notebooks_colab/ch02_Univariate_Data_Summary_printable.html")
    print("3. Generate PDF: python3 generate_pdf_playwright.py ch02")
    print("4. Verify formatting in PDF")
