# %%
"""
ch01_Analysis_of_Economics_Data.py - January 2026 for Python

Chapter 1: REGRESSION ANALYSIS

To run you need file:
  AED_HOUSE.DTA
in the data_stata/ directory
"""

# %% ========== SETUP ==========

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.formula.api import ols
import random
import os

# Set random seeds for reproducibility
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
os.environ['PYTHONHASHSEED'] = str(RANDOM_SEED)

# GitHub data URL (reliable mirror of Cameron's textbook data)
GITHUB_DATA_URL = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/"

# Output directories (optional - for saving figures and tables locally)
IMAGES_DIR = 'images'
TABLES_DIR = 'tables'
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(TABLES_DIR, exist_ok=True)

# %% ========== OVERVIEW ==========

# This Python program does analysis for Chapter 1
#  1.3 REGRESSION ANALYSIS

# %% ========== DATA DESCRIPTION ==========

# House sale price for 29 houses in Central Davis in 1999
#     29 observations on 9 variables

# %% ========== 1.3 REGRESSION ANALYSIS ==========

# Read in the Stata data set
# Data is streamed directly from GitHub (reliable mirror)
data_house = pd.read_stata(GITHUB_DATA_URL + 'AED_HOUSE.DTA')

# %% Explore data structure

# Display summary statistics
print("=" * 70)
print("CHAPTER 1: ANALYSIS OF ECONOMICS DATA")
print("=" * 70)
print("\nData Summary:")
data_summary = data_house.describe()

# %% Calculate statistics
print(data_summary)

# Save descriptive statistics table
data_summary.to_csv(os.path.join(TABLES_DIR, 'ch01_descriptive_stats.csv'))
print(f"Table saved to: {os.path.join(TABLES_DIR, 'ch01_descriptive_stats.csv')}")

print("\nData Info:")
print(data_house.info())

# Fit the regression line: price ~ size
# Using statsmodels formula API (similar to R's lm)

# %% Estimate regression model

model = ols('price ~ size', data=data_house).fit()

# Display regression results
print("\n" + "=" * 70)
print("OLS REGRESSION RESULTS: price ~ size")
print("=" * 70)

# %% Display regression results

print(model.summary())

# Save regression summary to text file
with open(os.path.join(TABLES_DIR, 'ch01_regression_summary.txt'), 'w') as f:
    f.write(model.summary().as_text())
print(f"\nRegression summary saved to: {os.path.join(TABLES_DIR, 'ch01_regression_summary.txt')}")

# Save regression coefficients table
coef_table = pd.DataFrame({
    'coefficient': model.params,
    'std_err': model.bse,
    't_value': model.tvalues,
    'p_value': model.pvalues,
    'conf_lower': model.conf_int()[0],
    'conf_upper': model.conf_int()[1]
})
coef_table.to_csv(os.path.join(TABLES_DIR, 'ch01_regression_coefficients.csv'))
print(f"Coefficients table saved to: {os.path.join(TABLES_DIR, 'ch01_regression_coefficients.csv')}")

# %% ========== FIGURE 1.1: SCATTER PLOT WITH FITTED LINE ==========

# Create the scatter plot with fitted regression line
fig, ax = plt.subplots(figsize=(10, 6))

# Scatter plot of actual data
ax.scatter(data_house['size'], data_house['price'],
           color='black', s=50, label='Actual', alpha=0.7)

# Add fitted regression line
ax.plot(data_house['size'], model.fittedvalues,
        color='blue', linewidth=2, label='Fitted')

# Labels
ax.set_xlabel('House size (in square feet)', fontsize=12)
ax.set_ylabel('House sale price (in dollars)', fontsize=12)
# ax.set_title('Figure 1.1: House Price vs Size', fontsize=14, fontweight='bold')  # Removed: redundant with LaTeX caption
ax.legend(loc='upper left')
ax.grid(True, alpha=0.3)

# Save figure
output_file = os.path.join(IMAGES_DIR, 'ch01_fig1_house_price_vs_size.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\nFigure saved to: {output_file}")

# Display the plot
plt.show()

# %% ========== REGRESSION DIAGNOSTICS ==========

print("\n" + "=" * 70)
print("REGRESSION COEFFICIENTS")
print("=" * 70)
print(f"Intercept: ${model.params['Intercept']:,.2f}")
print(f"Slope (size coefficient): ${model.params['size']:,.2f}")
print(f"R-squared: {model.rsquared:.4f}")
print(f"Adj. R-squared: {model.rsquared_adj:.4f}")
print(f"Number of observations: {int(model.nobs)}")

# %% ========== COMPARISON WITH STATA/R OUTPUT ==========

print("\n" + "=" * 70)
print("INTERPRETATION")
print("=" * 70)
print(f"For every additional square foot of house size,")
print(f"the sale price increases by approximately ${model.params['size']:,.2f}")
print(f"\nThe model explains {model.rsquared*100:.2f}% of the variation in house prices.")

print("\n" + "=" * 70)
print("ANALYSIS COMPLETE")
print("=" * 70)
