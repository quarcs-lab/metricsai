#!/usr/bin/env python3
"""
add_ch02_case_studies.py

Script to add a Case Studies section to Chapter 2 notebook (ch02_Univariate_Data_Summary.ipynb).

This script:
1. Loads the Chapter 2 notebook JSON
2. Inserts 21 new cells after cell 58 containing:
   - Section header (2.8 Case Studies)
   - Case study introduction
   - Key Concept boxes
   - 6 Tasks (guided -> independent) with code starters
   - Learning summary
3. Updates the Chapter Overview (cell 2) to include "2.8 Case Studies"
4. Writes the modified notebook back to disk

Usage:
    python3 add_ch02_case_studies.py

Author: Carlos Mendez
Date: 2026-01-31
"""

import json
from pathlib import Path
from typing import Dict, List, Any


def create_markdown_cell(content: str) -> Dict[str, Any]:
    """Create a markdown cell with given content."""
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": content.split('\n'),
        "id": ""  # IDs will be updated by Jupyter
    }


def create_code_cell(content: str) -> Dict[str, Any]:
    """Create a code cell with given content."""
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": content.split('\n'),
        "id": ""  # IDs will be updated by Jupyter
    }


def add_case_studies_cells() -> List[Dict[str, Any]]:
    """
    Generate all 21 case study cells.

    Returns:
        List of cell dictionaries to be inserted
    """
    cells = []

    # Cell 1: Section header H2
    cells.append(create_markdown_cell("## 2.8 Case Studies"))

    # Cell 2: Case study introduction (H3 + research context)
    intro_text = """### Case Study 1: Global Labor Productivity Distribution

**Research Question:** How is labor productivity distributed across countries? Are there distinct groups or is it continuous?

In Chapter 1, you examined *relationships between variables*—specifically, how productivity relates to capital stock through regression analysis. Now we shift perspective to analyze a *single variable*—labor productivity—but focus on its **distribution across countries** rather than its associations.

This case study builds on Chapter 1's dataset (Convergence Clubs) but asks fundamentally different questions: What does the distribution of productivity look like across the 61 countries in our sample? Is it symmetric or skewed? Have productivity gaps widened or narrowed over time? These distributional questions are central to development economics and understanding global inequality.

By completing this case study, you'll apply all the univariate analysis tools from Chapter 2 to a real dataset with genuine economic relevance—exploring whether productivity converges globally or if divergence persists."""
    cells.append(create_markdown_cell(intro_text))

    # Cell 3: Key Concept box 1
    key_concept_1 = """> **Key Concept**: Cross-country distributions of economic variables (productivity, GDP per capita, income) are typically right-skewed with long upper tails, reflecting substantial inequality between rich and poor countries. Summary statistics like the median are often more representative than the mean for these distributions, and exploring the shape of the distribution reveals whether gaps between countries are widening or narrowing."""
    cells.append(create_markdown_cell(key_concept_1))

    # Cell 4: Data loading section (H3)
    load_header = """### Load the Productivity Data

We'll use the same Convergence Clubs dataset from Chapter 1, but focus exclusively on the labor productivity variable (`lp`) across countries and years. This gives us 1,220 observations (61 countries × 20 years) of international productivity."""
    cells.append(create_markdown_cell(load_header))

    # Cell 5: Data loading code
    load_code = """# Load convergence clubs data (same as Chapter 1)
df1 = pd.read_csv(
    "https://raw.githubusercontent.com/quarcs-lab/mendez2020-convergence-clubs-code-data/master/assets/dat.csv",
    index_col=["country", "year"]
).sort_index()

# For Chapter 2, focus on labor productivity variable
productivity = df1['lp']

print("=" * 70)
print("LABOR PRODUCTIVITY DISTRIBUTION ANALYSIS")
print("=" * 70)
print(f"Total observations: {len(productivity)}")
print(f"Countries: {len(df1.index.get_level_values('country').unique())}")
print(f"Time period: {df1.index.get_level_values('year').min()} to {df1.index.get_level_values('year').max()}")
print(f"\\nFirst 10 observations (sample):")
print(df1[['lp']].head(10))"""
    cells.append(create_code_cell(load_code))

    # Cell 6: Task 1 header (H4)
    task1_header = """#### Task 1: Data Exploration (Guided)

**Objective:** Load and explore the structure of the global productivity distribution.

**Instructions:**
1. Examine the productivity variable's basic structure (length, data type, any missing values)
2. Get summary statistics (count, mean, std, min, max)
3. Display observations for 5 different countries to see variation across countries
4. Check: Is there variation across countries? Does it seem large or small?

**Chapter 2 connection:** This applies the concepts from Section 2.1 (Summary Statistics).

**Starter code guidance:**
- Use `productivity.describe()` for summary statistics
- Check for missing values with `productivity.isnull().sum()`
- Use `.loc[]` or `.xs()` to select specific countries' observations
- Calculate min and max productivity values globally"""
    cells.append(create_markdown_cell(task1_header))

    # Cell 7: Task 1 code
    task1_code = """# Task 1: Data Exploration (GUIDED)
# Complete the code below by filling in the blanks (_____)

# Step 1: Check data structure
print("Data Structure:")
print(f"Total observations: {_____}")
print(f"Data type: {productivity.dtype}")
print(f"Missing values: {_____}")

# Step 2: Summary statistics
print("\\n" + "=" * 70)
print("Summary Statistics for Global Productivity")
print("=" * 70)
print(productivity.describe())

# Step 3: Variation across countries - look at a few countries
print("\\n" + "=" * 70)
print("Productivity across 5 sample countries:")
print("=" * 70)
sample_countries = ['Australia', 'Brazil', 'China', 'France', 'Nigeria']
for country in sample_countries:
    country_data = df1.loc[country, 'lp']
    print(f"\\n{country}:")
    print(f"  Mean productivity: {_____:.3f}")
    print(f"  Min: {_____:.3f}, Max: {_____:.3f}")
    print(f"  Range: {_____:.3f}")

# Step 4: Global variation
print("\\n" + "=" * 70)
print("Global Variation:")
print("=" * 70)
min_prod = productivity.min()
max_prod = productivity.max()
ratio = max_prod / min_prod
print(f"Minimum global productivity: {min_prod:.3f}")
print(f"Maximum global productivity: {max_prod:.3f}")
print(f"Ratio (max/min): {ratio:.1f}x")
print(f"\\nInterpretation: The most productive country is {ratio:.0f}× more productive than the least productive country!")"""
    cells.append(create_code_cell(task1_code))

    # Cell 8: Task 2 header (H4)
    task2_header = """#### Task 2: Summary Statistics (Semi-guided)

**Objective:** Calculate comprehensive summary statistics for the global productivity distribution.

**Instructions:**
1. Compute mean, median, standard deviation, quartiles (25th, 50th, 75th percentiles)
2. Calculate skewness and kurtosis for the overall productivity distribution
3. Identify which countries have the highest and lowest productivity (across all years)
4. Compare productivity statistics for two time periods: 1990 and 2014

**Chapter 2 connection:** Applies Section 2.1 (Summary Statistics) and distribution shape measures.

**Starter code guidance:**
- Use `.describe()` for the main statistics
- Use `scipy.stats.skew()` and `scipy.stats.kurtosis()` for shape measures
- Filter by year: `df1.xs(1990, level='year')['lp']`
- Use `.nlargest()` and `.nsmallest()` to find extreme values
- Create a comparison table of statistics for different time periods"""
    cells.append(create_markdown_cell(task2_header))

    # Cell 9: Task 2 code
    task2_code = """# Task 2: Summary Statistics (SEMI-GUIDED)
# Complete the code by implementing each step

# Step 1: Overall summary statistics
print("=" * 70)
print("OVERALL PRODUCTIVITY STATISTICS (All countries, all years)")
print("=" * 70)
overall_stats = {
    'Mean': productivity.mean(),
    'Median': productivity.median(),
    'Std Dev': productivity.std(),
    'Skewness': stats.skew(productivity),
    'Kurtosis': stats.kurtosis(productivity),
    '25th percentile': productivity.quantile(0.25),
    '75th percentile': productivity.quantile(0.75),
    'IQR': productivity.quantile(0.75) - productivity.quantile(0.25)
}

for key, value in overall_stats.items():
    print(f"{key:20s}: {value:.4f}")

# Step 2: Countries with highest and lowest productivity (averaging across years)
print("\\n" + "=" * 70)
print("Top 5 Most Productive Countries (average across years)")
print("=" * 70)
country_means = df1.groupby('country')['lp'].mean().sort_values(ascending=False)
print(country_means.head())

print("\\n" + "=" * 70)
print("Top 5 Least Productive Countries (average across years)")
print("=" * 70)
print(country_means.tail())

# Step 3: Compare 1990 vs 2014
print("\\n" + "=" * 70)
print("COMPARING PRODUCTIVITY DISTRIBUTIONS: 1990 vs 2014")
print("=" * 70)

productivity_1990 = df1.xs(1990, level='year')['lp']
productivity_2014 = df1.xs(2014, level='year')['lp']

comparison_stats = {
    'Year': ['1990', '2014'],
    'Mean': [productivity_1990.mean(), productivity_2014.mean()],
    'Median': [productivity_1990.median(), productivity_2014.median()],
    'Std Dev': [productivity_1990.std(), productivity_2014.std()],
    'Skewness': [stats.skew(productivity_1990), stats.skew(productivity_2014)],
    'Min': [productivity_1990.min(), productivity_2014.min()],
    'Max': [productivity_1990.max(), productivity_2014.max()]
}

comparison_df = pd.DataFrame(comparison_stats).set_index('Year')
print(comparison_df.round(4))

print("\\nInterpretation questions:")
print("- Did average productivity increase from 1990 to 2014?")
print("- Did the spread (std dev) increase or decrease? What does this suggest about convergence?")
print("- Did skewness change? What might this mean for inequality?")"""
    cells.append(create_code_cell(task2_code))

    # Cell 10: Key Concept box 2
    key_concept_2 = """> **Key Concept**: Many economic variables follow approximately log-normal distributions, meaning their logarithms are normally distributed. Log transformation is particularly useful for productivity and income data because it reduces skewness and makes distributions more symmetric for statistical analysis. When data are log-normally distributed, differences in log-scale have a percentage interpretation—useful for growth and development economics."""
    cells.append(create_markdown_cell(key_concept_2))

    # Cell 11: Task 3 header (H4)
    task3_header = """#### Task 3: Visualizing Distributions (Semi-guided)

**Objective:** Create multiple visualizations to understand the shape of the productivity distribution.

**Instructions:**
1. Create a histogram of productivity (try different bin widths)
2. Create a box plot to identify outliers and quartiles
3. Create a kernel density estimate to see the smooth shape
4. Compare the original distribution to the log-transformed distribution

**Chapter 2 connection:** Applies Section 2.2 (Charts for Numerical Data).

**Starter code guidance:**
- Use `plt.hist()` for histogram with different bin widths (try 10, 15, 20 bins)
- Use `plt.boxplot()` for box plot visualization
- Use `.plot.kde()` for kernel density estimate
- Create side-by-side panels to compare original vs log-transformed
- Label axes clearly and add titles"""
    cells.append(create_markdown_cell(task3_header))

    # Cell 12: Task 3 code
    task3_code = """# Task 3: Visualizing Distributions (SEMI-GUIDED)
# Create comprehensive visualizations of the productivity distribution

# Create a 2x2 figure with 4 subplots
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Panel 1: Histogram (original productivity)
axes[0, 0].hist(productivity, bins=20, edgecolor='black', alpha=0.7, color='steelblue')
axes[0, 0].set_xlabel('Labor Productivity', fontsize=11)
axes[0, 0].set_ylabel('Frequency', fontsize=11)
axes[0, 0].set_title('Panel 1: Histogram of Productivity (20 bins)', fontsize=12, fontweight='bold')
axes[0, 0].grid(True, alpha=0.3)

# Panel 2: Box plot (original productivity)
axes[0, 1].boxplot(productivity, vert=True, patch_artist=True)
axes[0, 1].set_ylabel('Labor Productivity', fontsize=11)
axes[0, 1].set_title('Panel 2: Box Plot of Productivity', fontsize=12, fontweight='bold')
axes[0, 1].grid(True, alpha=0.3, axis='y')

# Panel 3: KDE (original productivity)
productivity.plot.kde(ax=axes[1, 0], linewidth=2, color='darkblue')
axes[1, 0].set_xlabel('Labor Productivity', fontsize=11)
axes[1, 0].set_ylabel('Density', fontsize=11)
axes[1, 0].set_title('Panel 3: Kernel Density Estimate', fontsize=12, fontweight='bold')
axes[1, 0].grid(True, alpha=0.3)

# Panel 4: KDE comparison (original vs log-transformed)
log_productivity = np.log(productivity)
productivity.plot.kde(ax=axes[1, 1], linewidth=2, label='Original', color='darkblue')
log_productivity.plot.kde(ax=axes[1, 1], linewidth=2, label='Log-transformed', color='red', linestyle='--')
axes[1, 1].set_xlabel('Labor Productivity', fontsize=11)
axes[1, 1].set_ylabel('Density', fontsize=11)
axes[1, 1].set_title('Panel 4: KDE Comparison', fontsize=12, fontweight='bold')
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

plt.suptitle('Figure: Global Productivity Distribution Visualizations', fontsize=14, fontweight='bold', y=1.00)
plt.tight_layout()
plt.show()

# Describe what you observe
print("\\nObservations:")
print("1. Histogram shape: Right-skewed or symmetric?")
print("2. Box plot: Where is the median? Are there outliers?")
print("3. KDE: Single peak or multiple modes?")
print("4. Log transformation: Does it make the distribution more symmetric?")"""
    cells.append(create_code_cell(task3_code))

    # Cell 13: Task 4 header (H4)
    task4_header = """#### Task 4: Comparing Distributions Across Time (More Independent)

**Objective:** Analyze how the productivity distribution has changed from 1990 to 2014.

**Instructions:**
1. Extract productivity data for 1990 and 2014
2. Calculate summary statistics for each year separately
3. Create overlapping KDE plots to compare the distributions visually
4. Analyze: Has the distribution shifted right (convergence/improvement)? Widened (divergence)? Changed shape?

**Chapter 2 connection:** Applies Section 2.2 (comparing distributions across groups).

**Starter code guidance:**
- Use `df1.xs(year, level='year')` to extract data for specific years
- Create summary statistics tables for comparison
- Plot two KDE curves on the same axes with different colors
- Use the 25th and 75th percentiles to measure spread
- Calculate the coefficient of variation (std/mean) to compare relative dispersion"""
    cells.append(create_markdown_cell(task4_header))

    # Cell 14: Task 4 code
    task4_code = """# Task 4: Comparing Distributions Across Time (MORE INDEPENDENT)
# Analyze how global productivity distribution evolved from 1990 to 2014

# Extract data for 1990 and 2014
prod_1990 = df1.xs(1990, level='year')['lp']
prod_2014 = df1.xs(2014, level='year')['lp']

# Create comparison visualization
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Panel A: Overlapping KDE plots
prod_1990.plot.kde(ax=axes[0], linewidth=2.5, label='1990', color='darkblue')
prod_2014.plot.kde(ax=axes[0], linewidth=2.5, label='2014', color='red')
axes[0].set_xlabel('Labor Productivity', fontsize=11)
axes[0].set_ylabel('Density', fontsize=11)
axes[0].set_title('Panel A: Productivity Distribution Evolution', fontsize=12, fontweight='bold')
axes[0].legend(fontsize=11)
axes[0].grid(True, alpha=0.3)

# Panel B: Side-by-side box plots
bp = axes[1].boxplot([prod_1990, prod_2014], labels=['1990', '2014'],
                      patch_artist=True, widths=0.6)
for patch, color in zip(bp['boxes'], ['lightblue', 'lightcoral']):
    patch.set_facecolor(color)
axes[1].set_ylabel('Labor Productivity', fontsize=11)
axes[1].set_title('Panel B: Box Plot Comparison', fontsize=12, fontweight='bold')
axes[1].grid(True, alpha=0.3, axis='y')

plt.suptitle('Productivity Distribution Comparison: 1990 vs 2014', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.show()

# Detailed comparison statistics
print("=" * 70)
print("DISTRIBUTION COMPARISON: 1990 vs 2014")
print("=" * 70)

stats_comparison = pd.DataFrame({
    '1990': [
        prod_1990.mean(),
        prod_1990.median(),
        prod_1990.std(),
        prod_1990.std() / prod_1990.mean(),  # Coefficient of variation
        stats.skew(prod_1990),
        prod_1990.min(),
        prod_1990.max(),
        prod_1990.max() - prod_1990.min()
    ],
    '2014': [
        prod_2014.mean(),
        prod_2014.median(),
        prod_2014.std(),
        prod_2014.std() / prod_2014.mean(),
        stats.skew(prod_2014),
        prod_2014.min(),
        prod_2014.max(),
        prod_2014.max() - prod_2014.min()
    ]
}, index=['Mean', 'Median', 'Std Dev', 'Coeff. of Variation', 'Skewness', 'Min', 'Max', 'Range'])

print(stats_comparison.round(4))

print("\\nKey questions to answer:")
print("- Did mean productivity increase? (Shift in central tendency)")
print("- Did spread (std dev) increase or decrease? (Convergence vs divergence)")
print("- Did the coefficient of variation change? (Relative inequality)")
print("- Did skewness change? (Change in inequality direction)")"""
    cells.append(create_code_cell(task4_code))

    # Cell 15: Task 5 header (H4)
    task5_header = """#### Task 5: Transformation Analysis (Independent)

**Objective:** Apply log transformation to productivity data and analyze the effect.

**Instructions:**
1. Create log-transformed productivity variable: log_productivity = ln(productivity)
2. Compare skewness before and after transformation
3. Create side-by-side histograms (original vs log-transformed)
4. Calculate z-scores for both variables to standardize them
5. Interpret: Why does log transformation help? When would you use it?

**Chapter 2 connection:** Applies Section 2.5 (Data Transformation).

**Starter code guidance:**
- Use `np.log()` to create log transformation
- Compare skewness values before/after using `stats.skew()`
- Create z-scores with: `(x - x.mean()) / x.std()`
- Visualize both original and log distributions in histograms
- Discuss why log-normal distributions are common in economics"""
    cells.append(create_markdown_cell(task5_header))

    # Cell 16: Task 5 code
    task5_code = """# Task 5: Transformation Analysis (INDEPENDENT)
# Apply log transformation to understand how it affects the distribution

# Create log-transformed productivity
log_productivity = np.log(productivity)

# Create z-scores (standardized values)
z_productivity = (productivity - productivity.mean()) / productivity.std()
z_log_productivity = (log_productivity - log_productivity.mean()) / log_productivity.std()

# Compare transformations in a figure
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Panel A: Original productivity histogram
axes[0].hist(productivity, bins=20, edgecolor='black', alpha=0.7, color='steelblue')
axes[0].set_xlabel('Labor Productivity (original scale)', fontsize=11)
axes[0].set_ylabel('Frequency', fontsize=11)
axes[0].set_title('Panel A: Original Productivity Distribution', fontsize=12, fontweight='bold')
axes[0].grid(True, alpha=0.3)

# Panel B: Log-transformed productivity histogram
axes[1].hist(log_productivity, bins=20, edgecolor='black', alpha=0.7, color='coral')
axes[1].set_xlabel('Log(Labor Productivity)', fontsize=11)
axes[1].set_ylabel('Frequency', fontsize=11)
axes[1].set_title('Panel B: Log-Transformed Distribution', fontsize=12, fontweight='bold')
axes[1].grid(True, alpha=0.3)

plt.suptitle('Transformation Analysis: Effect of Log Transformation', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.show()

# Detailed comparison
print("=" * 70)
print("TRANSFORMATION EFFECTS")
print("=" * 70)

transformation_table = pd.DataFrame({
    'Metric': ['Mean', 'Median', 'Std Dev', 'Skewness', 'Kurtosis', 'Min', 'Max'],
    'Original': [
        productivity.mean(),
        productivity.median(),
        productivity.std(),
        stats.skew(productivity),
        stats.kurtosis(productivity),
        productivity.min(),
        productivity.max()
    ],
    'Log-Transformed': [
        log_productivity.mean(),
        log_productivity.median(),
        log_productivity.std(),
        stats.skew(log_productivity),
        stats.kurtosis(log_productivity),
        log_productivity.min(),
        log_productivity.max()
    ]
})

print(transformation_table.to_string(index=False))

print("\\n" + "=" * 70)
print("SKEWNESS REDUCTION")
print("=" * 70)
print(f"Original skewness: {stats.skew(productivity):.4f}")
print(f"Log-transformed skewness: {stats.skew(log_productivity):.4f}")
print(f"Reduction: {abs(stats.skew(productivity)) - abs(stats.skew(log_productivity)):.4f}")
print(f"Percentage reduction: {(1 - abs(stats.skew(log_productivity))/abs(stats.skew(productivity)))*100:.1f}%")

print("\\nInterpretation:")
print("- Is the log-transformed distribution more symmetric?")
print("- When would you use the log transformation in analysis?")
print("- What about the z-scores—how do they compare?")"""
    cells.append(create_code_cell(task5_code))

    # Cell 17: Key Concept box 3
    key_concept_3 = """> **Key Concept**: Distributional convergence (σ-convergence) asks whether the spread (variance) of productivity across countries is narrowing over time. This differs from β-convergence (poor countries growing faster than rich ones). If cross-country distributions are becoming more compressed (lower variance), it suggests countries are converging toward similar productivity levels—important for understanding whether global inequality is increasing or decreasing."""
    cells.append(create_markdown_cell(key_concept_3))

    # Cell 18: Task 6 header (H4)
    task6_header = """#### Task 6: Regional Patterns (Independent)

**Objective:** Compare productivity distributions across geographic regions.

**Instructions:**
1. Add a region column to your dataframe (you'll need to manually assign regions based on country names)
2. Group countries by region (at minimum: Africa, Asia, Europe, Americas)
3. Create box plots for each region side-by-side
4. Calculate summary statistics by region
5. Identify: Which regions have highest/lowest productivity? Most inequality?

**Chapter 2 connection:** Applies Sections 2.3-2.4 (Charts for categorical breakdowns).

**Starter code guidance:**
- Create a dictionary mapping countries to regions
- Use `.groupby()` to calculate statistics by region
- Create side-by-side box plots for visual comparison
- Calculate mean and standard deviation by region
- Compare median productivity across regions"""
    cells.append(create_markdown_cell(task6_header))

    # Cell 19: Task 6 code
    task6_code = """# Task 6: Regional Patterns (INDEPENDENT)
# Compare productivity distributions across geographic regions

# Create region mapping (assign countries to regions)
region_mapping = {
    'Australia': 'Asia-Pacific',
    'Austria': 'Europe',
    'Belgium': 'Europe',
    'Brazil': 'Americas',
    'Canada': 'Americas',
    'Chile': 'Americas',
    'China': 'Asia',
    'Colombia': 'Americas',
    'Costa Rica': 'Americas',
    'Denmark': 'Europe',
    'Egypt': 'Africa',
    'Finland': 'Europe',
    'France': 'Europe',
    'Germany': 'Europe',
    'Greece': 'Europe',
    'Hong Kong': 'Asia',
    'India': 'Asia',
    'Indonesia': 'Asia',
    'Ireland': 'Europe',
    'Israel': 'Middle East',
    'Italy': 'Europe',
    'Jamaica': 'Americas',
    'Japan': 'Asia-Pacific',
    'Kenya': 'Africa',
    'South Korea': 'Asia',
    'Malaysia': 'Asia',
    'Mexico': 'Americas',
    'Netherlands': 'Europe',
    'New Zealand': 'Asia-Pacific',
    'Nigeria': 'Africa',
    'Norway': 'Europe',
    'Pakistan': 'Asia',
    'Peru': 'Americas',
    'Philippines': 'Asia',
    'Poland': 'Europe',
    'Portugal': 'Europe',
    'Singapore': 'Asia',
    'South Africa': 'Africa',
    'Spain': 'Europe',
    'Sri Lanka': 'Asia',
    'Sweden': 'Europe',
    'Switzerland': 'Europe',
    'Taiwan': 'Asia',
    'Thailand': 'Asia',
    'Turkey': 'Middle East',
    'United Kingdom': 'Europe',
    'United States': 'Americas',
    'Venezuela': 'Americas',
    'Vietnam': 'Asia',
}

# Add region to dataframe
df_with_region = df1.copy()
df_with_region['region'] = df_with_region.index.get_level_values('country').map(region_mapping)

# Remove rows with missing region assignments
df_with_region = df_with_region.dropna(subset=['region'])

# Calculate statistics by region
regional_stats = df_with_region.groupby('region')['lp'].agg([
    'count', 'mean', 'median', 'std', 'min', 'max'
]).round(4)

print("=" * 70)
print("REGIONAL PRODUCTIVITY STATISTICS")
print("=" * 70)
print(regional_stats.sort_values('mean', ascending=False))

# Create box plots by region
fig, ax = plt.subplots(figsize=(12, 6))

regions_sorted = df_with_region.groupby('region')['lp'].mean().sort_values(ascending=False).index
data_by_region = [df_with_region[df_with_region['region'] == region]['lp'].values for region in regions_sorted]

bp = ax.boxplot(data_by_region, labels=regions_sorted, patch_artist=True)
for patch in bp['boxes']:
    patch.set_facecolor('lightblue')
ax.set_ylabel('Labor Productivity', fontsize=12)
ax.set_xlabel('Region', fontsize=12)
ax.set_title('Productivity Distribution by Region', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, axis='y')
plt.xticks(rotation=45, ha='right')

plt.tight_layout()
plt.show()

print("\\nKey insights:")
print("- Which region has the highest average productivity?")
print("- Which region has the most internal inequality (widest box)?")
print("- Are there clear regional clusters, or is variation continuous?")"""
    cells.append(create_code_cell(task6_code))

    # Cell 20: Learning summary (H3)
    summary_text = """### What You've Learned from This Case Study

By completing this case study on global labor productivity distribution, you've applied the full toolkit of univariate data analysis to a real international economics question. You've moved beyond calculating statistics and making charts to asking substantive economic questions: Are countries converging or diverging? How has global inequality in productivity evolved? Which regions drive global disparity?

Specifically, you've practiced:
- **Summary statistics** to quantify central tendency and spread
- **Visualizations** (histograms, box plots, KDE) to see distributional shape
- **Comparisons** across time periods to detect changes
- **Transformations** (log) to normalize skewed economic data
- **Categorical breakdowns** (regions) to identify subgroup patterns

These skills extend far beyond productivity. The same analytical approach applies to wealth distribution, income inequality, student test scores, health outcomes, and countless other univariate datasets in economics and social science.

Your next steps (in later chapters) will be to ask *relational* questions: How does productivity relate to capital? Does inequality depend on development level? Can we *predict* a country's productivity from other variables? Those questions require bivariate analysis (Chapter 5) and regression (Chapter 6+)."""
    cells.append(create_markdown_cell(summary_text))

    # Cell 21: Empty cell (spacer)
    cells.append(create_markdown_cell(""))

    return cells


def update_chapter_overview(notebook: Dict[str, Any]) -> None:
    """
    Update cell 2 (Chapter Overview) to add 2.8 Case Studies to the outline.

    Args:
        notebook: The notebook dictionary
    """
    # Cell 2 is the Chapter Overview
    overview_cell = notebook['cells'][2]

    # Find the line with "- 2.7 Practice Exercises" and add "- 2.8 Case Studies" after it
    if overview_cell['cell_type'] == 'markdown':
        # Reconstruct the cell content
        source_text = ''.join(overview_cell['source'])

        # Add the new outline item
        old_outline = """- 2.1 Summary Statistics for Numerical Data
- 2.2 Charts for Numerical Data
- 2.3 Charts for Numerical Data by Category
- 2.4 Charts for Categorical Data
- 2.5 Data Transformation
- 2.6 Data Transformations for Time Series Data
- 2.7 Practice Exercises"""

        new_outline = """- 2.1 Summary Statistics for Numerical Data
- 2.2 Charts for Numerical Data
- 2.3 Charts for Numerical Data by Category
- 2.4 Charts for Categorical Data
- 2.5 Data Transformation
- 2.6 Data Transformations for Time Series Data
- 2.7 Practice Exercises
- 2.8 Case Studies"""

        source_text = source_text.replace(old_outline, new_outline)

        # Update the cell source
        overview_cell['source'] = source_text.split('\n')


def main() -> None:
    """Main function: load notebook, add case studies, and save."""
    # Define paths
    notebook_path = Path('/Users/carlosmendez/Documents/GitHub/metricsai/notebooks_colab/ch02_Univariate_Data_Summary.ipynb')

    # Check that notebook exists
    if not notebook_path.exists():
        print(f"Error: Notebook not found at {notebook_path}")
        return

    print(f"Loading notebook from: {notebook_path}")

    # Load the notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    print(f"Loaded notebook with {len(notebook['cells'])} cells")

    # Verify we have the expected structure
    if len(notebook['cells']) < 59:
        print(f"Error: Expected at least 59 cells, but found {len(notebook['cells'])}")
        return

    # Generate the 21 case study cells
    print("Generating 21 case study cells...")
    case_study_cells = add_case_studies_cells()

    # Insert the cells after position 58 (i.e., at position 59)
    print(f"Inserting {len(case_study_cells)} cells at position 59...")
    for i, cell in enumerate(case_study_cells):
        notebook['cells'].insert(59 + i, cell)

    # Update the Chapter Overview (cell 2)
    print("Updating Chapter Overview to include 2.8 Case Studies...")
    update_chapter_overview(notebook)

    # Save the updated notebook
    print(f"Saving updated notebook (now {len(notebook['cells'])} cells)...")
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)

    print("\n" + "=" * 70)
    print("SUCCESS!")
    print("=" * 70)
    print(f"✓ Added 21 case study cells to Chapter 2")
    print(f"✓ Updated Chapter Overview outline")
    print(f"✓ Notebook now has {len(notebook['cells'])} cells (previously 59)")
    print(f"✓ Saved to: {notebook_path}")
    print("\nNext steps:")
    print("1. Open the notebook in Jupyter/Colab to verify the changes")
    print("2. Execute the case study cells with students")
    print("3. Optionally regenerate the PDF with: python3 generate_pdf_playwright.py ch02")


if __name__ == '__main__':
    main()
