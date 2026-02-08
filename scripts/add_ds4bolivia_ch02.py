#!/usr/bin/env python3
"""Add DS4Bolivia Case Study 2 to CH02 notebook."""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
NB_PATH = PROJECT_ROOT / 'notebooks_colab' / 'ch02_Univariate_Data_Summary.ipynb'


def make_md_cell(source):
    """Create a markdown cell dict."""
    lines = source.split('\n')
    source_list = [line + '\n' if i < len(lines) - 1 else line
                   for i, line in enumerate(lines)]
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source_list
    }


def make_code_cell(source):
    """Create a code cell dict."""
    lines = source.split('\n')
    source_list = [line + '\n' if i < len(lines) - 1 else line
                   for i, line in enumerate(lines)]
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source_list
    }


# ============================================================
# Case Study 2 content cells
# ============================================================

cells_to_add = [

# ---------- Introduction ----------
make_md_cell("""\
### Case Study 2: The Geography of Development: Summarizing Bolivia's Municipal SDG Data

In Chapter 1, we introduced the DS4Bolivia project and explored the relationship between nighttime lights and municipal development in Bolivia. In this case study, we apply Chapter 2's univariate summary tools to characterize the *distribution* of development indicators across Bolivia's 339 municipalities.

**The Data**: The [DS4Bolivia project](https://github.com/quarcs-lab/ds4bolivia) provides a comprehensive dataset covering 339 Bolivian municipalities with over 350 variables, including the Municipal Sustainable Development Index (IMDS), individual SDG indices, nighttime lights per capita (2012-2020), population, and socioeconomic indicators. Here we focus on understanding the *shape* of these distributions—their central tendency, spread, skewness, and multimodality—using the univariate tools from this chapter."""),

# ---------- Load Data ----------
make_md_cell("""\
#### Load the DS4Bolivia Data

Let's load the DS4Bolivia dataset and select the key variables for univariate analysis."""),

make_code_cell("""\
# Load the DS4Bolivia dataset
url_bol = "https://raw.githubusercontent.com/quarcs-lab/ds4bolivia/master/ds4bolivia_v20250523.csv"
bol = pd.read_csv(url_bol)

# Display basic information
print("=" * 70)
print("DS4BOLIVIA DATASET")
print("=" * 70)
print(f"Dataset shape: {bol.shape[0]} municipalities, {bol.shape[1]} variables")
print(f"\\nDepartments: {bol['dep'].nunique()} unique departments")
print(f"Department names: {sorted(bol['dep'].unique())}")

# Select key variables for this case study
key_vars = ['mun', 'dep', 'imds', 'ln_NTLpc2017', 'pop2017',
            'index_sdg1', 'sdg1_1_ubn',
            'ln_NTLpc2012', 'ln_NTLpc2013', 'ln_NTLpc2014',
            'ln_NTLpc2015', 'ln_NTLpc2016', 'ln_NTLpc2017',
            'ln_NTLpc2018', 'ln_NTLpc2019', 'ln_NTLpc2020']
# Remove duplicates while preserving order
key_vars = list(dict.fromkeys(key_vars))
bol_key = bol[key_vars].copy()

print(f"\\nKey variables selected: {len(key_vars)}")
print("\\n" + "=" * 70)
print("FIRST 10 MUNICIPALITIES")
print("=" * 70)
print(bol_key.head(10).to_string())"""),

# ---------- Task 1: Summary Statistics (Guided) ----------
make_md_cell("""\
#### Task 1: Summary Statistics (Guided)

**Objective**: Compute and interpret descriptive statistics for key development indicators.

**Instructions**:
1. Use `.describe()` to generate summary statistics for `imds`, `index_sdg1`, `sdg1_1_ubn`, and `ln_NTLpc2017`
2. Calculate the mean, median, standard deviation, skewness, and kurtosis for each variable
3. Discuss what these statistics reveal about the distribution of municipal development in Bolivia

**Apply what you learned in section 2.1**: Use `describe()`, `.mean()`, `.median()`, `.std()`, `.skew()`, and `.kurtosis()` to characterize these distributions."""),

make_code_cell("""\
# Task 1: Summary Statistics
# ----------------------------------------------------------

# 1. Basic descriptive statistics
analysis_vars = ['imds', 'index_sdg1', 'sdg1_1_ubn', 'ln_NTLpc2017']
print("=" * 70)
print("DESCRIPTIVE STATISTICS: KEY DEVELOPMENT INDICATORS")
print("=" * 70)
print(bol_key[analysis_vars].describe().round(2))

# 2. Additional distributional measures
print("\\n" + "=" * 70)
print("DISTRIBUTIONAL SHAPE MEASURES")
print("=" * 70)
for var in analysis_vars:
    series = bol_key[var].dropna()
    print(f"\\n{var}:")
    print(f"  Mean:     {series.mean():.2f}")
    print(f"  Median:   {series.median():.2f}")
    print(f"  Std Dev:  {series.std():.2f}")
    print(f"  Skewness: {series.skew():.3f}")
    print(f"  Kurtosis: {series.kurtosis():.3f}")

# 3. Discussion: What do these reveal?
print("\\n" + "=" * 70)
print("INTERPRETATION")
print("=" * 70)
print("Compare mean vs median for each variable:")
print("If mean > median → right-skewed (long upper tail)")
print("If mean < median → left-skewed (long lower tail)")
print("High kurtosis (>3) indicates heavy tails (extreme municipalities)")"""),

# ---------- Task 2: Histograms and Density Plots (Guided) ----------
make_md_cell("""\
#### Task 2: Histograms and Density Plots (Guided)

**Objective**: Visualize the distributions of `imds` and `ln_NTLpc2017` using histograms and kernel density estimation (KDE) plots.

**Instructions**:
1. Create histograms for `imds` and `ln_NTLpc2017` (side by side)
2. Overlay KDE curves on the histograms
3. Discuss the shape: Is each distribution unimodal or bimodal? Symmetric or skewed?
4. What might explain any multimodality? (Think about the urban-rural divide)

**Apply what you learned in section 2.2**: Use `plt.hist()` with `density=True` and overlay `.plot.kde()` or `sns.kdeplot()`."""),

make_code_cell("""\
# Task 2: Histograms and Density Plots
# ----------------------------------------------------------

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# IMDS histogram with KDE
axes[0].hist(bol_key['imds'].dropna(), bins=25, density=True,
             color='steelblue', alpha=0.7, edgecolor='white')
bol_key['imds'].dropna().plot.kde(ax=axes[0], color='darkblue', linewidth=2)
axes[0].set_xlabel('Municipal Development Index (IMDS)')
axes[0].set_ylabel('Density')
axes[0].set_title('Distribution of IMDS across 339 Municipalities')
axes[0].axvline(bol_key['imds'].mean(), color='red', linestyle='--',
                label=f"Mean = {bol_key['imds'].mean():.1f}")
axes[0].axvline(bol_key['imds'].median(), color='orange', linestyle='--',
                label=f"Median = {bol_key['imds'].median():.1f}")
axes[0].legend()

# Log NTL histogram with KDE
axes[1].hist(bol_key['ln_NTLpc2017'].dropna(), bins=25, density=True,
             color='purple', alpha=0.7, edgecolor='white')
bol_key['ln_NTLpc2017'].dropna().plot.kde(ax=axes[1], color='darkviolet', linewidth=2)
axes[1].set_xlabel('Log Nighttime Lights per Capita (2017)')
axes[1].set_ylabel('Density')
axes[1].set_title('Distribution of Log NTL per Capita')
axes[1].axvline(bol_key['ln_NTLpc2017'].mean(), color='red', linestyle='--',
                label=f"Mean = {bol_key['ln_NTLpc2017'].mean():.2f}")
axes[1].axvline(bol_key['ln_NTLpc2017'].median(), color='orange', linestyle='--',
                label=f"Median = {bol_key['ln_NTLpc2017'].median():.2f}")
axes[1].legend()

plt.tight_layout()
plt.show()

# Discussion prompts
print("DISCUSSION:")
print("1. Is the IMDS distribution unimodal or multimodal?")
print("2. Is the NTL distribution symmetric or skewed?")
print("3. What might explain any bimodality? (urban vs rural)")"""),

# ---------- Key Concept 2.10 ----------
make_md_cell("""\
> **Key Concept 2.10: Spatial Data Distributions**
>
> Municipal-level data often exhibits **multimodality** reflecting the urban-rural divide. Unlike national statistics that produce single averages, municipality-level distributions can reveal distinct subpopulations—highly developed urban centers and less developed rural areas. Identifying these subgroups is essential for targeted policy interventions."""),

# ---------- Task 3: Box Plots by Department (Semi-guided) ----------
make_md_cell("""\
#### Task 3: Box Plots by Department (Semi-guided)

**Objective**: Create box plots of `imds` grouped by department (`dep`) to compare development across Bolivia's 9 departments.

**Instructions**:
1. Create a box plot of `imds` grouped by `dep` (9 departments)
2. Order departments by median IMDS for clarity
3. Identify which departments have the highest and lowest median development
4. Which departments show the most spread (variability)?

**Apply what you learned in section 2.3-2.4**: Use grouped box plots to compare distributions across categories."""),

make_code_cell("""\
# Task 3: Box Plots by Department
# ----------------------------------------------------------

# Your code here: Create box plots of IMDS by department
#
# Steps:
# 1. Order departments by median IMDS
# 2. Create horizontal box plot
# 3. Add labels and formatting

# Example structure:
# dept_order = bol_key.groupby('dep')['imds'].median().sort_values().index
# fig, ax = plt.subplots(figsize=(10, 7))
# bol_key.boxplot(column='imds', by='dep', ax=ax, vert=False,
#                 positions=range(len(dept_order)))
# ax.set_xlabel('Municipal Development Index (IMDS)')
# ax.set_ylabel('Department')
# ax.set_title('Development Distribution by Department')
# plt.suptitle('')  # Remove automatic title
# plt.tight_layout()
# plt.show()

# Hint: You can also use seaborn for cleaner grouped box plots:
import seaborn as sns
dept_order = bol_key.groupby('dep')['imds'].median().sort_values().index.tolist()

fig, ax = plt.subplots(figsize=(10, 7))
sns.boxplot(data=bol_key, x='imds', y='dep', order=dept_order,
            palette='viridis', ax=ax)
ax.set_xlabel('Municipal Development Index (IMDS)')
ax.set_ylabel('Department')
ax.set_title('Municipal Development Distribution by Department')
plt.tight_layout()
plt.show()

# Summary statistics by department
print("=" * 70)
print("IMDS BY DEPARTMENT: MEDIAN AND IQR")
print("=" * 70)
dept_stats = bol_key.groupby('dep')['imds'].describe()[['50%', '25%', '75%', 'std']].round(1)
dept_stats.columns = ['Median', 'Q1', 'Q3', 'Std Dev']
print(dept_stats.sort_values('Median'))"""),

# ---------- Task 4: Log Transformations (Semi-guided) ----------
make_md_cell("""\
#### Task 4: Log Transformations (Semi-guided)

**Objective**: Compare the distribution of raw population (`pop2017`) with its log transformation to demonstrate how log transformations improve symmetry for skewed data.

**Instructions**:
1. Plot the histogram of raw `pop2017` — observe the extreme right skew
2. Apply `np.log(pop2017)` and plot its histogram
3. Compare summary statistics (skewness, kurtosis) before and after transformation
4. Discuss why log transformations are standard practice for population and income data

**Apply what you learned in section 2.5**: Log transformations convert multiplicative relationships into additive ones and reduce skewness."""),

make_code_cell("""\
# Task 4: Log Transformations
# ----------------------------------------------------------

# Your code here: Compare raw vs log-transformed population
#
# Steps:
# 1. Plot raw pop2017 histogram
# 2. Plot np.log(pop2017) histogram
# 3. Compare skewness and kurtosis

import numpy as np

pop = bol_key['pop2017'].dropna()
log_pop = np.log(pop)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Raw population
axes[0].hist(pop, bins=30, color='coral', alpha=0.7, edgecolor='white')
axes[0].set_xlabel('Population (2017)')
axes[0].set_ylabel('Frequency')
axes[0].set_title('Raw Population Distribution')
axes[0].axvline(pop.mean(), color='red', linestyle='--',
                label=f"Mean = {pop.mean():,.0f}")
axes[0].axvline(pop.median(), color='blue', linestyle='--',
                label=f"Median = {pop.median():,.0f}")
axes[0].legend()

# Log-transformed population
axes[1].hist(log_pop, bins=30, color='teal', alpha=0.7, edgecolor='white')
axes[1].set_xlabel('Log Population (2017)')
axes[1].set_ylabel('Frequency')
axes[1].set_title('Log-Transformed Population Distribution')
axes[1].axvline(log_pop.mean(), color='red', linestyle='--',
                label=f"Mean = {log_pop.mean():.2f}")
axes[1].axvline(log_pop.median(), color='blue', linestyle='--',
                label=f"Median = {log_pop.median():.2f}")
axes[1].legend()

plt.tight_layout()
plt.show()

# Compare distributional measures
print("=" * 70)
print("EFFECT OF LOG TRANSFORMATION ON POPULATION")
print("=" * 70)
print(f"{'Measure':<15} {'Raw pop2017':>15} {'log(pop2017)':>15}")
print("-" * 45)
print(f"{'Skewness':<15} {pop.skew():>15.3f} {log_pop.skew():>15.3f}")
print(f"{'Kurtosis':<15} {pop.kurtosis():>15.3f} {log_pop.kurtosis():>15.3f}")
print(f"{'Mean':<15} {pop.mean():>15,.0f} {log_pop.mean():>15.2f}")
print(f"{'Median':<15} {pop.median():>15,.0f} {log_pop.median():>15.2f}")"""),

# ---------- Key Concept 2.11 ----------
make_md_cell("""\
> **Key Concept 2.11: Development Indicator Interpretation**
>
> SDG composite indices like IMDS (0-100) aggregate multiple dimensions of development into a single score. While convenient for ranking, composite indices can mask important variation in specific dimensions. For example, a municipality may score well on education (SDG 4) but poorly on health (SDG 3). Examining individual SDG variables alongside composite indices provides a more complete picture."""),

# ---------- Task 5: Time Series of NTL (Independent) ----------
make_md_cell("""\
#### Task 5: Time Series of NTL (Independent)

**Objective**: Calculate and plot the mean nighttime lights across municipalities for each year from 2012 to 2020 to examine the evolution of satellite-measured economic activity.

**Instructions**:
1. Calculate the mean of `ln_NTLpc2012` through `ln_NTLpc2020` across all municipalities for each year
2. Plot the resulting time series (year on x-axis, mean log NTL on y-axis)
3. Discuss: Is there a trend? Any notable changes? What might explain the pattern?

**Apply what you learned in section 2.6**: Use time series visualization to identify trends and patterns."""),

make_code_cell("""\
# Task 5: Time Series of NTL
# ----------------------------------------------------------

# Your code here: Calculate mean NTL across municipalities for each year
#
# Steps:
# 1. Select NTL columns for 2012-2020
# 2. Calculate means
# 3. Plot time series

# Example structure:
# ntl_cols = [f'ln_NTLpc{yr}' for yr in range(2012, 2021)]
# years = list(range(2012, 2021))
# mean_ntl = [bol_key[col].mean() for col in ntl_cols]
#
# fig, ax = plt.subplots(figsize=(10, 5))
# ax.plot(years, mean_ntl, marker='o', color='navy', linewidth=2)
# ax.set_xlabel('Year')
# ax.set_ylabel('Mean Log NTL per Capita')
# ax.set_title('Evolution of Nighttime Lights across Bolivian Municipalities')
# ax.grid(True, alpha=0.3)
# plt.tight_layout()
# plt.show()"""),

# ---------- Task 6: Regional Distribution Analysis (Independent) ----------
make_md_cell("""\
#### Task 6: Regional Distribution Analysis (Independent)

**Objective**: Compare the distributions of `imds` across departments using overlapping histograms or violin plots. Write a 200-word summary of regional inequality in Bolivia.

**Instructions**:
1. Create overlapping histograms or violin plots of `imds` for at least 3 departments
2. Compare the distributional shapes: Do some departments have more spread? More bimodality?
3. Write a 200-word summary discussing what these distributions reveal about regional inequality in Bolivia
4. Which departments might need the most targeted development interventions? Why?

**Apply your skills**: This task combines histogram/density visualization with substantive economic interpretation."""),

make_code_cell("""\
# Task 6: Regional Distribution Analysis
# ----------------------------------------------------------

# Your code here: Compare IMDS distributions across departments
#
# Option A: Overlapping histograms (select 3-4 key departments)
# Option B: Violin plots for all 9 departments
# Option C: Ridge plot (multiple KDE curves stacked vertically)

# Example structure (violin plots):
# fig, ax = plt.subplots(figsize=(12, 7))
# dept_order = bol_key.groupby('dep')['imds'].median().sort_values().index.tolist()
# sns.violinplot(data=bol_key, x='imds', y='dep', order=dept_order,
#                palette='coolwarm', ax=ax, inner='quartile')
# ax.set_xlabel('Municipal Development Index (IMDS)')
# ax.set_ylabel('Department')
# ax.set_title('Distribution of Municipal Development by Department')
# plt.tight_layout()
# plt.show()

# After creating your visualization, write a 200-word summary below:
# print("REGIONAL INEQUALITY SUMMARY")
# print("=" * 70)
# print("Write your 200-word analysis here...")"""),

# ---------- What You've Learned ----------
make_md_cell("""\
### What You've Learned from This Case Study

By applying Chapter 2's univariate analysis tools to Bolivia's municipal SDG data, you've characterized the *distribution* of development outcomes across 339 municipalities. Specifically, you've practiced:

- **Descriptive statistics** for development indicators—mean, median, SD, skewness, and kurtosis
- **Visualization of distributions** using histograms, box plots, and kernel density estimation (KDE)
- **Log transformations** for highly skewed data like population
- **Time series summary** of satellite-measured nighttime lights (2012-2020)
- **Regional comparison** of development distributions across Bolivia's 9 departments

These univariate tools reveal the *shape* of Bolivia's development distribution—its central tendency, spread, and the urban-rural divide reflected in multimodal patterns. Understanding these distributional properties is the essential first step before more advanced analysis.

**Connection to future chapters**: In Chapter 4, we'll test whether differences across departments are statistically significant. In Chapter 5, we'll explore *bivariate* relationships between satellite data and development. Later chapters will build progressively more sophisticated models for predicting and explaining municipal development outcomes.

---

**Well done!** You've now explored Bolivia's municipal development data using the full univariate analysis toolkit—from summary statistics to distributional visualization and transformation."""),

]


def main():
    with open(NB_PATH, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    # ----------------------------------------------------------
    # Step 1: Check if existing Case Study heading needs renaming
    # ----------------------------------------------------------
    renamed = False
    for cell in notebook['cells']:
        if cell.get('cell_type') == 'markdown':
            source = ''.join(cell.get('source', []))
            # Match "### Case Study:" without a number (but NOT "### Case Study 1:")
            if '### Case Study:' in source and '### Case Study 1:' not in source:
                # Rename to "### Case Study 1:"
                new_source = source.replace('### Case Study:', '### Case Study 1:')
                lines = new_source.split('\n')
                cell['source'] = [line + '\n' if i < len(lines) - 1 else line
                                  for i, line in enumerate(lines)]
                renamed = True
                print("Renamed '### Case Study:' → '### Case Study 1:'")
                break

    if not renamed:
        print("Existing heading already uses '### Case Study 1:' — no rename needed.")

    # ----------------------------------------------------------
    # Step 2: Find insertion point after "What You've Learned"
    # in the Case Study section
    # ----------------------------------------------------------
    insert_idx = None
    for i, cell in enumerate(notebook['cells']):
        if cell.get('cell_type') == 'markdown':
            source = ''.join(cell.get('source', []))
            if "What You've Learned" in source and "case study" in source.lower():
                # Verify this is in the Case Study section (not Chapter Overview)
                # by checking for keywords related to Case Study 1 content
                if any(kw in source.lower() for kw in ['labor productivity', 'convergence',
                                                        'you\'ve practiced', 'toolkit',
                                                        'case study']):
                    insert_idx = i + 1
                    print(f"Found Case Study 1 closing at cell index {i}")
                    break

    if insert_idx is None:
        # Fallback: insert before the last cell
        insert_idx = len(notebook['cells']) - 1
        print(f"WARNING: Could not find Case Study 1 closing. Inserting at index {insert_idx}")

    # ----------------------------------------------------------
    # Step 3: Insert Case Study 2 cells
    # ----------------------------------------------------------
    print(f"Inserting {len(cells_to_add)} cells at index {insert_idx}")

    original_count = len(notebook['cells'])
    for j, cell in enumerate(cells_to_add):
        notebook['cells'].insert(insert_idx + j, cell)

    # ----------------------------------------------------------
    # Step 4: Write modified notebook
    # ----------------------------------------------------------
    with open(NB_PATH, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)
        f.write('\n')

    print(f"Done! Notebook now has {len(notebook['cells'])} cells (was {original_count})")


if __name__ == '__main__':
    main()
