"""
ch02_Univariate_Data_Summary.py - January 2026 for Python

Chapter 2: UNIVARIATE DATA SUMMARY

To run you need files:
  AED_EARNINGS.DTA
  AED_REALGDPPC.DTA
  AED_HEALTHCATEGORIES.DTA
  AED_FISHING.DTA
  AED_MONTHLYHOMESALES.DTA
in the data_stata/ directory

Sections covered:
  2.1 SUMMARY STATISTICS FOR NUMERICAL DATA
  2.2 CHARTS FOR NUMERICAL DATA
  2.3 CHARTS FOR NUMERICAL DATA BY CATEGORY
  2.4 SUMMARY AND CHARTS FOR CATEGORICAL DATA
  2.5 DATA TRANSFORMATION
  2.6 DATA TRANSFORMATION FOR TIME SERIES DATA
"""

# ========== SETUP ==========

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import random
import os

# Set random seeds for reproducibility
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
os.environ['PYTHONHASHSEED'] = str(RANDOM_SEED)

# GitHub data URL
GITHUB_DATA_URL = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/"

# Output directories (optional - for saving figures and tables locally)
IMAGES_DIR = 'images'
TABLES_DIR = 'tables'
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(TABLES_DIR, exist_ok=True)

# Set plotting style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# ========== DATA DESCRIPTIONS ==========

# (1) Annual Earnings for 191 women aged 30 years in 2010 Full-time workers
#     191 observations on 4 variables
# (2) U.S. quarterly GDP and related data from 1959Q1 to 2020Q1
#     245 Observations on 11 variables
# (3) U.S. Health Expenditures in 2018
#     11 Observations on 2 variables
# (4) Fishing site data
#     1182 observations on 17 variables
# (5) Monthly existing home sales in the U.S. 1999 - 2015
#     193 observations on several variables

print("=" * 70)
print("CHAPTER 2: UNIVARIATE DATA SUMMARY")
print("=" * 70)

# ========== 2.1 SUMMARY STATISTICS FOR NUMERICAL DATA ==========

print("\n" + "=" * 70)
print("2.1 SUMMARY STATISTICS FOR NUMERICAL DATA")
print("=" * 70)

# Read in the earnings data
data_earnings = pd.read_stata(GITHUB_DATA_URL + 'AED_EARNINGS.DTA')

print("\nData structure:")
print(data_earnings.info())

print("\nData summary:")
data_summary = data_earnings.describe()
print(data_summary)
data_summary.to_csv(os.path.join(TABLES_DIR, 'ch02_earnings_descriptive_stats.csv'))
print(f"Table saved to: {os.path.join(TABLES_DIR, 'ch02_earnings_descriptive_stats.csv')}")

# Table 2.1: Detailed statistics for earnings
print("\n" + "-" * 70)
print("Table 2.1: Detailed Statistics for Earnings")
print("-" * 70)

earnings = data_earnings['earnings']

# Calculate statistics
stats_dict = {
    'Count': len(earnings),
    'Mean': earnings.mean(),
    'Std Dev': earnings.std(),
    'Min': earnings.min(),
    '25th percentile': earnings.quantile(0.25),
    'Median': earnings.median(),
    '75th percentile': earnings.quantile(0.75),
    'Max': earnings.max(),
    'Skewness': stats.skew(earnings),
    'Kurtosis': stats.kurtosis(earnings)
}

for key, value in stats_dict.items():
    if key in ['Count']:
        print(f"{key:20s}: {value:,.0f}")
    else:
        print(f"{key:20s}: ${value:,.2f}")

# Save detailed statistics table
stats_df = pd.DataFrame(stats_dict, index=[0]).T
stats_df.columns = ['Value']
stats_df.to_csv(os.path.join(TABLES_DIR, 'ch02_earnings_detailed_stats.csv'))
print(f"Table saved to: {os.path.join(TABLES_DIR, 'ch02_earnings_detailed_stats.csv')}")

# Figure 2.2: Box plot of earnings
fig, ax = plt.subplots(figsize=(8, 6))
bp = ax.boxplot(earnings, vert=False, patch_artist=True,
                boxprops=dict(facecolor='lightblue', alpha=0.7),
                medianprops=dict(color='red', linewidth=2))
ax.set_xlabel('Annual earnings (in dollars)', fontsize=12)
ax.set_title('Figure 2.2: Box Plot of Annual Earnings', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)

output_file = os.path.join(IMAGES_DIR, 'ch02_fig2_earnings_boxplot.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\nFigure 2.2 saved to: {output_file}")
plt.close()

# ========== 2.2 CHARTS FOR NUMERICAL DATA ==========

print("\n" + "=" * 70)
print("2.2 CHARTS FOR NUMERICAL DATA")
print("=" * 70)

# Table 2.2: Earnings ranges
earnings_range = (earnings // 15000).astype(int)
print("\nTable 2.2: Earnings Range Distribution")
print(earnings_range.value_counts().sort_index())

# Figure 2.4: Histograms with different bin widths
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Panel A: Wider bins (15000)
axes[0].hist(earnings, bins=range(0, int(earnings.max()) + 15000, 15000),
             edgecolor='black', alpha=0.7, color='steelblue')
axes[0].set_xlabel('Annual Earnings (in dollars)', fontsize=11)
axes[0].set_ylabel('Frequency', fontsize=11)
axes[0].set_title('Panel A: Bin width = $15,000', fontsize=12, fontweight='bold')
axes[0].grid(True, alpha=0.3)

# Panel B: Narrower bins (7500)
axes[1].hist(earnings, bins=range(0, int(earnings.max()) + 7500, 7500),
             edgecolor='black', alpha=0.7, color='steelblue')
axes[1].set_xlabel('Annual Earnings (in dollars)', fontsize=11)
axes[1].set_ylabel('Frequency', fontsize=11)
axes[1].set_title('Panel B: Bin width = $7,500', fontsize=12, fontweight='bold')
axes[1].grid(True, alpha=0.3)

plt.suptitle('Figure 2.4: Histograms of Annual Earnings', fontsize=14, fontweight='bold', y=1.02)
output_file = os.path.join(IMAGES_DIR, 'ch02_fig4_earnings_histograms.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\nFigure 2.4 saved to: {output_file}")
plt.close()

# Figure 2.5: Kernel density estimate
fig, ax = plt.subplots(figsize=(10, 6))
earnings.plot.kde(ax=ax, linewidth=2, color='darkblue', bw_method=0.3)
ax.set_xlabel('Annual Earnings (in dollars)', fontsize=12)
ax.set_ylabel('Density', fontsize=12)
ax.set_title('Figure 2.5: Kernel Density Estimate of Earnings', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)

output_file = os.path.join(IMAGES_DIR, 'ch02_fig5_earnings_kde.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\nFigure 2.5 saved to: {output_file}")
plt.close()

# Figure 2.6: Time series plot - Real GDP per capita
data_gdp = pd.read_stata(GITHUB_DATA_URL + 'AED_REALGDPPC.DTA')

print("\n" + "-" * 70)
print("GDP Data Summary:")
gdp_summary = data_gdp.describe()
print(gdp_summary)
gdp_summary.to_csv(os.path.join(TABLES_DIR, 'ch02_gdp_descriptive_stats.csv'))
print(f"Table saved to: {os.path.join(TABLES_DIR, 'ch02_gdp_descriptive_stats.csv')}")

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(data_gdp['daten'], data_gdp['realgdppc'], linewidth=2, color='darkblue')
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Real GDP per capita (in 2012 dollars)', fontsize=12)
ax.set_title('Figure 2.6: U.S. Real GDP per Capita', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)

output_file = os.path.join(IMAGES_DIR, 'ch02_fig6_realgdp_timeseries.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\nFigure 2.6 saved to: {output_file}")
plt.close()

# ========== 2.3 CHARTS FOR NUMERICAL DATA BY CATEGORY ==========

print("\n" + "=" * 70)
print("2.3 CHARTS FOR NUMERICAL DATA BY CATEGORY")
print("=" * 70)

# Read in health categories data
data_health = pd.read_stata(GITHUB_DATA_URL + 'AED_HEALTHCATEGORIES.DTA')

# Table 2.3
print("\nTable 2.3: Health Expenditure Categories")
print(data_health)
data_health.to_csv(os.path.join(TABLES_DIR, 'ch02_health_expenditures.csv'), index=False)
print(f"Table saved to: {os.path.join(TABLES_DIR, 'ch02_health_expenditures.csv')}")

# Figure 2.7: Bar chart of health expenditures
fig, ax = plt.subplots(figsize=(12, 6))
data_health_sorted = data_health.sort_values('expenditures', ascending=False)
bars = ax.bar(range(len(data_health_sorted)), data_health_sorted['expenditures'],
              color='steelblue', edgecolor='black', alpha=0.7)
ax.set_xticks(range(len(data_health_sorted)))
ax.set_xticklabels(data_health_sorted['category'], rotation=45, ha='right', fontsize=10)
ax.set_ylabel('Expenditures (in $ billions)', fontsize=12)
ax.set_title('Figure 2.7: U.S. Health Expenditures by Category (2018)',
             fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, axis='y')

output_file = os.path.join(IMAGES_DIR, 'ch02_fig7_health_expenditures.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\nFigure 2.7 saved to: {output_file}")
plt.close()

# ========== 2.4 SUMMARY AND CHARTS FOR CATEGORICAL DATA ==========

print("\n" + "=" * 70)
print("2.4 SUMMARY AND CHARTS FOR CATEGORICAL DATA")
print("=" * 70)

# Read in fishing data
data_fishing = pd.read_stata(GITHUB_DATA_URL + 'AED_FISHING.DTA')

print("\nFishing data summary:")
print(data_fishing.info())

# Table 2.4: Frequency distribution of fishing mode
print("\n" + "-" * 70)
print("Table 2.4: Frequency Distribution of Fishing Mode")
print("-" * 70)

mode_freq = data_fishing['mode'].value_counts()
mode_relfreq = data_fishing['mode'].value_counts(normalize=True)
mode_table = pd.DataFrame({
    'Frequency': mode_freq,
    'Relative Frequency': mode_relfreq
})
print(mode_table)
mode_table.to_csv(os.path.join(TABLES_DIR, 'ch02_fishing_mode_frequency.csv'))
print(f"Table saved to: {os.path.join(TABLES_DIR, 'ch02_fishing_mode_frequency.csv')}")

# Figure 2.9: Pie chart of fishing modes
fig, ax = plt.subplots(figsize=(8, 8))
colors = plt.cm.Set3(range(len(mode_freq)))
wedges, texts, autotexts = ax.pie(mode_freq.values,
                                    labels=mode_freq.index,
                                    autopct='%1.1f%%',
                                    colors=colors,
                                    startangle=90,
                                    textprops={'fontsize': 11})
ax.set_title('Figure 2.9: Distribution of Fishing Modes',
             fontsize=14, fontweight='bold', pad=20)

output_file = os.path.join(IMAGES_DIR, 'ch02_fig9_fishing_modes_pie.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\nFigure 2.9 saved to: {output_file}")
plt.close()

# ========== 2.5 DATA TRANSFORMATION ==========

print("\n" + "=" * 70)
print("2.5 DATA TRANSFORMATION")
print("=" * 70)

# Create log transformation of earnings
data_earnings['lnearnings'] = np.log(data_earnings['earnings'])

print("\nComparison of earnings and log(earnings):")
print(data_earnings[['earnings', 'lnearnings']].describe())

# Figure 2.10: Histograms comparing earnings and log(earnings)
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Panel A: Original earnings
axes[0].hist(data_earnings['earnings'], bins=30,
             edgecolor='black', alpha=0.7, color='steelblue')
axes[0].set_xlabel('Annual Earnings (in dollars)', fontsize=11)
axes[0].set_ylabel('Frequency', fontsize=11)
axes[0].set_title('Panel A: Earnings', fontsize=12, fontweight='bold')
axes[0].grid(True, alpha=0.3)

# Panel B: Log earnings
axes[1].hist(data_earnings['lnearnings'], bins=30,
             edgecolor='black', alpha=0.7, color='coral')
axes[1].set_xlabel('Log of Annual Earnings', fontsize=11)
axes[1].set_ylabel('Frequency', fontsize=11)
axes[1].set_title('Panel B: Log(Earnings)', fontsize=12, fontweight='bold')
axes[1].grid(True, alpha=0.3)

plt.suptitle('Figure 2.10: Data Transformation - Log Transformation',
             fontsize=14, fontweight='bold', y=1.02)
output_file = os.path.join(IMAGES_DIR, 'ch02_fig10_earnings_log_transformation.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\nFigure 2.10 saved to: {output_file}")
plt.close()

# ========== 2.6 DATA TRANSFORMATIONS FOR TIME SERIES DATA ==========

print("\n" + "=" * 70)
print("2.6 DATA TRANSFORMATIONS FOR TIME SERIES DATA")
print("=" * 70)

# Read in monthly home sales data
data_homesales = pd.read_stata(GITHUB_DATA_URL + 'AED_MONTHLYHOMESALES.DTA')

# Filter data for year >= 2005
data_homesales_filtered = data_homesales[data_homesales['year'] >= 2005]

print("\nHome sales data (2005 onwards):")
print(data_homesales_filtered.describe())

# Figure 2.11: Time series plots with moving average and seasonal adjustment
fig, axes = plt.subplots(2, 1, figsize=(12, 10))

# Panel A: Original and Moving Average
axes[0].plot(data_homesales_filtered['daten'], data_homesales_filtered['exsales'],
            linewidth=2, label='Original', color='darkblue')
axes[0].plot(data_homesales_filtered['daten'], data_homesales_filtered['exsales_ma11'],
            linewidth=2, linestyle='--', label='11-month Moving Average', color='red')
axes[0].set_xlabel('Year', fontsize=11)
axes[0].set_ylabel('Monthly Home Sales', fontsize=11)
axes[0].set_title('Panel A: Original Series and Moving Average',
                  fontsize=12, fontweight='bold')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Panel B: Original and Seasonally Adjusted
axes[1].plot(data_homesales_filtered['daten'], data_homesales_filtered['exsales'],
            linewidth=2, label='Original', color='darkblue')
axes[1].plot(data_homesales_filtered['daten'], data_homesales_filtered['exsales_sa'],
            linewidth=2, linestyle='--', label='Seasonally Adjusted', color='green')
axes[1].set_xlabel('Year', fontsize=11)
axes[1].set_ylabel('Monthly Home Sales', fontsize=11)
axes[1].set_title('Panel B: Original Series and Seasonally Adjusted',
                  fontsize=12, fontweight='bold')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.suptitle('Figure 2.11: Time Series Transformations for Home Sales',
             fontsize=14, fontweight='bold', y=0.995)
output_file = os.path.join(IMAGES_DIR, 'ch02_fig11_homesales_transformations.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\nFigure 2.11 saved to: {output_file}")
plt.close()

# Table 2.5: First and last observations of GDP data
print("\n" + "-" * 70)
print("Table 2.5: First and Last Observations of GDP Data")
print("-" * 70)
print("\nFirst observation:")
print(data_gdp[['gdp', 'realgdp', 'gdppc', 'realgdppc', 'gdpdef', 'popthm', 'year']].head(1))
print("\nLast observation:")
print(data_gdp[['gdp', 'realgdp', 'gdppc', 'realgdppc', 'gdpdef', 'popthm', 'year']].tail(1))

# Figure 2.12: GDP comparisons
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Panel A: GDP and Real GDP
axes[0].plot(data_gdp['daten'], data_gdp['gdp'],
            linewidth=2, label='GDP (nominal)', color='darkblue')
axes[0].plot(data_gdp['daten'], data_gdp['realgdp'],
            linewidth=2, linestyle='--', label='Real GDP (2012 dollars)', color='red')
axes[0].set_xlabel('Year', fontsize=11)
axes[0].set_ylabel('GDP (in $ billions)', fontsize=11)
axes[0].set_title('Panel A: GDP and Real GDP', fontsize=12, fontweight='bold')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Panel B: GDP per capita and Real GDP per capita
axes[1].plot(data_gdp['daten'], data_gdp['gdppc'],
            linewidth=2, label='GDP per capita (nominal)', color='darkblue')
axes[1].plot(data_gdp['daten'], data_gdp['realgdppc'],
            linewidth=2, linestyle='--', label='Real GDP per capita (2012 dollars)', color='red')
axes[1].set_xlabel('Year', fontsize=11)
axes[1].set_ylabel('GDP per capita (in dollars)', fontsize=11)
axes[1].set_title('Panel B: GDP per Capita and Real GDP per Capita',
                  fontsize=12, fontweight='bold')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.suptitle('Figure 2.12: GDP Comparisons - Nominal vs Real',
             fontsize=14, fontweight='bold', y=1.0)
output_file = os.path.join(IMAGES_DIR, 'ch02_fig12_gdp_comparisons.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\nFigure 2.12 saved to: {output_file}")
plt.close()

# ========== SUMMARY ==========

print("\n" + "=" * 70)
print("CHAPTER 2 ANALYSIS COMPLETE")
print("=" * 70)
print("\nAll figures saved to:", IMAGES_DIR)
print("\nKey concepts demonstrated:")
print("  - Summary statistics (mean, median, quartiles, skewness, kurtosis)")
print("  - Visual data exploration (box plots, histograms, density plots)")
print("  - Categorical data analysis (frequency tables, pie charts, bar charts)")
print("  - Data transformations (logarithmic transformation)")
print("  - Time series visualizations (line plots, moving averages, seasonal adjustment)")
