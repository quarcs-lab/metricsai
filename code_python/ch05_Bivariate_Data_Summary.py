"""
ch05_Bivariate_Data_Summary.py - January 2026 for Python

Chapter 5: BIVARIATE DATA SUMMARY

To run you need file:
  AED_HOUSE.DTA
in the data_stata/ directory

Sections covered:
  5.1 EXAMPLE: HOUSE PRICE AND SIZE
  5.2 TWO-WAY TABULATION
  5.3 TWO-WAY SCATTER PLOT
  5.4 SAMPLE CORRELATION
  5.5 REGRESSION LINE
  5.6 MEASURES OF MODEL FIT
  5.7 COMPUTER OUTPUT FOLLOWING REGRESSION
  5.8 PREDICTION AND OUTLYING OBSERVATIONS
  5.9 REGRESSION AND CORRELATION
  5.10 CAUSATION
  5.11 NONPARAMETRIC REGRESSION
"""

# ========== SETUP ==========

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.nonparametric.smoothers_lowess import lowess
from scipy import stats
from scipy.ndimage import gaussian_filter1d
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

print("=" * 70)
print("CHAPTER 5: BIVARIATE DATA SUMMARY")
print("=" * 70)

# ========== 5.1 EXAMPLE: HOUSE PRICE AND SIZE ==========

print("\n" + "=" * 70)
print("5.1 EXAMPLE: HOUSE PRICE AND SIZE")
print("=" * 70)

# Read in house data
data_house = pd.read_stata(GITHUB_DATA_URL + 'AED_HOUSE.DTA')

print("\nData summary:")
data_summary = data_house.describe()
print(data_summary)
data_summary.to_csv(os.path.join(TABLES_DIR, 'ch05_house_descriptive_stats.csv'))
print(f"Table saved to: {os.path.join(TABLES_DIR, 'ch05_house_descriptive_stats.csv')}")

print("\nTable 5.1: Complete dataset")
print(data_house)

# Table 5.2: Summary statistics
print("\n" + "-" * 70)
print("Table 5.2: Summary Statistics")
print("-" * 70)

price = data_house['price']
size = data_house['size']

print("\nPrice statistics:")
print(f"  Mean:      ${price.mean():,.2f}")
print(f"  Median:    ${price.median():,.2f}")
print(f"  Min:       ${price.min():,.2f}")
print(f"  Max:       ${price.max():,.2f}")
print(f"  Std Dev:   ${price.std():,.2f}")

print("\nSize statistics:")
print(f"  Mean:      {size.mean():,.0f} sq ft")
print(f"  Median:    {size.median():,.0f} sq ft")
print(f"  Min:       {size.min():,.0f} sq ft")
print(f"  Max:       {size.max():,.0f} sq ft")
print(f"  Std Dev:   {size.std():,.0f} sq ft")

# ========== 5.2 TWO-WAY TABULATION ==========

print("\n" + "=" * 70)
print("5.2 TWO-WAY TABULATION")
print("=" * 70)

# Create categorical variables
price_range = pd.cut(price, bins=[0, 249999, np.inf],
                     labels=['< $250,000', '≥ $250,000'])

size_range = pd.cut(size, bins=[0, 1799, 2399, np.inf],
                    labels=['< 1,800', '1,800-2,399', '≥ 2,400'])

# Table 5.3: Two-way tabulation
print("\nTable 5.3: Two-Way Tabulation")
crosstab = pd.crosstab(price_range, size_range, margins=True)
print(crosstab)
crosstab.to_csv(os.path.join(TABLES_DIR, 'ch05_crosstab.csv'))
print(f"Table saved to: {os.path.join(TABLES_DIR, 'ch05_crosstab.csv')}")

# ========== 5.3 TWO-WAY SCATTER PLOT ==========

print("\n" + "=" * 70)
print("5.3 TWO-WAY SCATTER PLOT")
print("=" * 70)

# Figure 5.1: Scatter plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(size, price, s=80, alpha=0.7, color='black', edgecolor='black')
ax.set_xlabel('House size (in square feet)', fontsize=12)
ax.set_ylabel('House sale price (in dollars)', fontsize=12)
ax.set_title('Figure 5.1: House Price vs Size', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)

output_file = os.path.join(IMAGES_DIR, 'ch05_fig1_scatter_price_vs_size.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\nFigure 5.1 saved to: {output_file}")
plt.close()

# ========== 5.4 SAMPLE CORRELATION ==========

print("\n" + "=" * 70)
print("5.4 SAMPLE CORRELATION")
print("=" * 70)

# Covariance and correlation
cov_matrix = data_house[['price', 'size']].cov()
corr_matrix = data_house[['price', 'size']].corr()

print("\nCovariance matrix:")
print(cov_matrix)

print("\nCorrelation matrix:")
print(corr_matrix)
corr_matrix.to_csv(os.path.join(TABLES_DIR, 'ch05_correlation_matrix.csv'))
print(f"Table saved to: {os.path.join(TABLES_DIR, 'ch05_correlation_matrix.csv')}")

print(f"\nCorrelation coefficient: {corr_matrix.loc['price', 'size']:.4f}")

# Figure 5.2: Different correlation patterns with simulated data
np.random.seed(12345)
n = 30
x = np.random.normal(3, 1, n)
u1 = np.random.normal(0, 0.8, n)
y1 = 3 + x + u1
u2 = np.random.normal(0, 2, n)
y2 = 3 + x + u2
y3 = 5 + u2
y4 = 10 - x - u2

correlations = [
    np.corrcoef(x, y1)[0, 1],
    np.corrcoef(x, y2)[0, 1],
    np.corrcoef(x, y3)[0, 1],
    np.corrcoef(x, y4)[0, 1]
]

fig, axes = plt.subplots(2, 2, figsize=(14, 12))
axes = axes.flatten()

datasets = [(x, y1, 'Panel A'), (x, y2, 'Panel B'),
            (x, y3, 'Panel C'), (x, y4, 'Panel D')]

for idx, (ax, (x_data, y_data, title), corr) in enumerate(zip(axes, datasets, correlations)):
    ax.scatter(x_data, y_data, s=60, alpha=0.7, color='black', edgecolor='black')
    ax.set_xlabel('x', fontsize=11)
    ax.set_ylabel('y', fontsize=11)
    ax.set_title(f'{title}: r = {corr:.2f}', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)

plt.suptitle('Figure 5.2: Different Correlation Patterns',
             fontsize=14, fontweight='bold', y=0.995)
output_file = os.path.join(IMAGES_DIR, 'ch05_fig2_correlation_patterns.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\nFigure 5.2 saved to: {output_file}")
plt.close()

# ========== 5.5 REGRESSION LINE ==========

print("\n" + "=" * 70)
print("5.5 REGRESSION LINE")
print("=" * 70)

# Fit regression model
model = ols('price ~ size', data=data_house).fit()

print("\nOLS Regression Results:")
print(model.summary())
# Save regression summary
with open(os.path.join(TABLES_DIR, 'ch05_regression_summary.txt'), 'w') as f:
    f.write(model.summary().as_text())
# Save coefficients
coef_table = pd.DataFrame({
    'coefficient': model.params,
    'std_err': model.bse,
    't_value': model.tvalues,
    'p_value': model.pvalues
})
coef_table.to_csv(os.path.join(TABLES_DIR, 'ch05_regression_coefficients.csv'))
print(f"Coefficients saved to: {os.path.join(TABLES_DIR, 'ch05_regression_coefficients.csv')}")

# Figure 5.4: Scatter plot with regression line
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(size, price, s=80, alpha=0.7, color='black',
           edgecolor='black', label='Actual')
ax.plot(size, model.fittedvalues, color='blue', linewidth=2, label='Fitted')
ax.set_xlabel('House size (in square feet)', fontsize=12)
ax.set_ylabel('House sale price (in dollars)', fontsize=12)
ax.set_title('Figure 5.4: House Price Regression',
             fontsize=14, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)

output_file = os.path.join(IMAGES_DIR, 'ch05_fig4_regression_line.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\nFigure 5.4 saved to: {output_file}")
plt.close()

# Intercept-only regression
model_intercept = ols('price ~ 1', data=data_house).fit()

print("\n" + "-" * 70)
print("Intercept-only regression:")
print(f"  Coefficient: ${model_intercept.params[0]:,.2f}")
print(f"  Sample mean: ${price.mean():,.2f}")
print("  (These should be equal)")

# ========== 5.6 MEASURES OF MODEL FIT ==========

print("\n" + "=" * 70)
print("5.6 MEASURES OF MODEL FIT")
print("=" * 70)

# Simulated data for demonstration
np.random.seed(123456)
x_sim = np.arange(1, 6)
epsilon = np.random.normal(0, 2, 5)
y_sim = 1 + 2*x_sim + epsilon

df_sim = pd.DataFrame({'x': x_sim, 'y': y_sim})
model_sim = ols('y ~ x', data=df_sim).fit()

print("\nSimulated Data for Model Fit Illustration:")
print(f"{'x':<5} {'ε':<10} {'y':<10} {'ŷ':<10} {'residual':<10}")
print("-" * 50)
for i in range(len(x_sim)):
    print(f"{x_sim[i]:<5} {epsilon[i]:<10.4f} {y_sim[i]:<10.4f} "
          f"{model_sim.fittedvalues[i]:<10.4f} {model_sim.resid[i]:<10.4f}")

print(f"\nModel Statistics:")
print(f"  R-squared:     {model_sim.rsquared:.4f}")
print(f"  Adj R-squared: {model_sim.rsquared_adj:.4f}")
print(f"  Root MSE:      {np.sqrt(model_sim.mse_resid):.4f}")

# Figure 5.5: Visualization of model fit
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Panel A: Actual values vs mean
axes[0].scatter(x_sim, y_sim, s=100, color='black', marker='^', label='Actual y')
axes[0].axhline(y=y_sim.mean(), color='red', linewidth=2, linestyle='--',
                label=f'Mean of y = {y_sim.mean():.2f}')
axes[0].set_xlabel('x', fontsize=12)
axes[0].set_ylabel('y', fontsize=12)
axes[0].set_title('Panel A: Actual Values and Mean', fontsize=12, fontweight='bold')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Panel B: Fitted values vs mean
axes[1].scatter(x_sim, model_sim.fittedvalues, s=100, color='black',
                marker='o', label='Fitted ŷ')
axes[1].axhline(y=y_sim.mean(), color='red', linewidth=2, linestyle='--',
                label=f'Mean of y = {y_sim.mean():.2f}')
axes[1].set_xlabel('x', fontsize=12)
axes[1].set_ylabel('ŷ', fontsize=12)
axes[1].set_title('Panel B: Fitted Values and Mean', fontsize=12, fontweight='bold')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.suptitle('Figure 5.5: Model Fit Illustration',
             fontsize=14, fontweight='bold', y=1.0)
output_file = os.path.join(IMAGES_DIR, 'ch05_fig5_model_fit_illustration.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\nFigure 5.5 saved to: {output_file}")
plt.close()

# ========== 5.8 PREDICTION AND OUTLYING OBSERVATIONS ==========

print("\n" + "=" * 70)
print("5.8 PREDICTION AND OUTLYING OBSERVATIONS")
print("=" * 70)

# Predict for a house of 2000 square feet
new_size = pd.DataFrame({'size': [2000]})
predicted_price = model.predict(new_size)

print(f"\nPrediction for a 2,000 sq ft house:")
print(f"  Predicted price: ${predicted_price.values[0]:,.2f}")

# Manual calculation
beta0 = model.params['Intercept']
beta1 = model.params['size']
manual_prediction = beta0 + beta1 * 2000

print(f"\nManual calculation:")
print(f"  ŷ = {beta0:.2f} + {beta1:.2f} × 2000 = ${manual_prediction:,.2f}")

# ========== 5.9 REGRESSION AND CORRELATION ==========

print("\n" + "=" * 70)
print("5.9 REGRESSION AND CORRELATION")
print("=" * 70)

# Relationship between regression and correlation
r = corr_matrix.loc['price', 'size']
r_squared = r ** 2

print(f"\nCorrelation coefficient (r):  {r:.4f}")
print(f"R-squared from regression:    {model.rsquared:.4f}")
print(f"r²:                           {r_squared:.4f}")
print("  (R² and r² should be equal)")

# ========== 5.10 CAUSATION ==========

print("\n" + "=" * 70)
print("5.10 CAUSATION")
print("=" * 70)

# Reverse regression: size ~ price
reverse_model = ols('size ~ price', data=data_house).fit()

print("\nReverse Regression (size ~ price):")
print(f"  Intercept: {reverse_model.params['Intercept']:.2f}")
print(f"  Slope:     {reverse_model.params['price']:.6f}")
print(f"  R-squared: {reverse_model.rsquared:.4f}")

print("\nOriginal Regression (price ~ size):")
print(f"  Intercept: ${model.params['Intercept']:,.2f}")
print(f"  Slope:     ${model.params['size']:,.2f}")
print(f"  R-squared: {model.rsquared:.4f}")

# ========== 5.11 NONPARAMETRIC REGRESSION ==========

print("\n" + "=" * 70)
print("5.11 NONPARAMETRIC REGRESSION")
print("=" * 70)

# Nonparametric regression using lowess
lowess_result = lowess(price, size, frac=0.6)

# Sort data for smooth plotting
sort_idx = np.argsort(size)
size_sorted = size.iloc[sort_idx]
price_sorted = price.iloc[sort_idx]

# Kernel smoothing (using Gaussian filter as approximation)
from scipy.interpolate import interp1d
sigma = 2  # bandwidth parameter
price_smooth = gaussian_filter1d(price_sorted, sigma)

fig, ax = plt.subplots(figsize=(12, 7))

# Scatter plot
ax.scatter(size, price, s=80, alpha=0.6, color='black',
           edgecolor='black', label='Actual', zorder=1)

# OLS line
ax.plot(size, model.fittedvalues, color='blue', linewidth=2.5,
        label='OLS regression', zorder=2)

# LOWESS
ax.plot(lowess_result[:, 0], lowess_result[:, 1], color='red',
        linewidth=2.5, linestyle='--', label='LOWESS', zorder=3)

# Kernel smoothing
ax.plot(size_sorted, price_smooth, color='green', linewidth=2.5,
        linestyle=':', label='Kernel smoothing', zorder=4)

ax.set_xlabel('House size (in square feet)', fontsize=12)
ax.set_ylabel('House sale price (in dollars)', fontsize=12)
ax.set_title('Figure 5.6: Parametric vs Nonparametric Regression',
             fontsize=14, fontweight='bold')
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)

output_file = os.path.join(IMAGES_DIR, 'ch05_fig6_nonparametric_regression.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\nFigure 5.6 saved to: {output_file}")
plt.close()

# ========== SUMMARY ==========

print("\n" + "=" * 70)
print("CHAPTER 5 ANALYSIS COMPLETE")
print("=" * 70)
print("\nKey concepts demonstrated:")
print("  - Bivariate data visualization (scatter plots)")
print("  - Two-way tabulation for categorical variables")
print("  - Correlation and covariance")
print("  - Simple linear regression (OLS)")
print("  - Measures of model fit (R², residuals)")
print("  - Prediction using regression")
print("  - Relationship between regression and correlation")
print("  - Nonparametric regression (LOWESS, kernel smoothing)")
print("\nAll figures saved to:", IMAGES_DIR)
