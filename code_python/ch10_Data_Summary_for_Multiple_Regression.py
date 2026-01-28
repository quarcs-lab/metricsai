"""
ch10_Data_Summary_for_Multiple_Regression.py - January 2026 for Python

Chapter 10: DATA SUMMARY FOR MULTIPLE REGRESSION

To run you need files:
  AED_HOUSE.DTA
in the data/ directory

Sections covered:
  10.1 EXAMPLE: HOUSE PRICE AND CHARACTERISTICS
  10.2 TWO-WAY SCATTERPLOTS
  10.3 CORRELATION
  10.4 REGRESSION LINE
  10.5 ESTIMATED PARTIAL EFFECTS
  10.6 MODEL FIT
  10.7 COMPUTER OUTPUT FOLLOWING MULTIPLE REGRESSION
  10.8 INESTIMABLE MODELS
"""

# ========== SETUP ==========

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from statsmodels.formula.api import ols
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

print("=" * 70)
print("CHAPTER 10: DATA SUMMARY FOR MULTIPLE REGRESSION")
print("=" * 70)

# ========== 10.1 EXAMPLE: HOUSE PRICE AND CHARACTERISTICS ==========

print("\n" + "=" * 70)
print("10.1 EXAMPLE: HOUSE PRICE AND CHARACTERISTICS")
print("=" * 70)

# Read in the house data
data_house = pd.read_stata(GITHUB_DATA_URL + 'AED_HOUSE.DTA')

print("\nData summary:")
data_summary = data_house.describe()
print(data_summary)
data_summary.to_csv(os.path.join(TABLES_DIR, 'ch10_house_descriptive_stats.csv'))
print(f"Table saved to: {os.path.join(TABLES_DIR, 'ch10_house_descriptive_stats.csv')}")

# Table 10.1
print("\n" + "-" * 70)
print("Table 10.1: House Characteristics Summary Statistics")
print("-" * 70)
table101_vars = ['price', 'size', 'bedrooms', 'bathrooms', 'lotsize',
                 'age', 'monthsold']
print(data_house[table101_vars].describe())

# Table 10.2 - Full data listing
print("\n" + "-" * 70)
print("Table 10.2: House Data (first 10 observations)")
print("-" * 70)
print(data_house[table101_vars].head(10))

# Bivariate regression vs multiple regression
print("\n" + "-" * 70)
print("Comparison: Bivariate vs Multiple Regression")
print("-" * 70)

# Bivariate regression
model_one = ols('price ~ bedrooms', data=data_house).fit()
print("\nBivariate regression: price ~ bedrooms")
print(model_one.summary())

# Multiple regression
model_two = ols('price ~ bedrooms + size', data=data_house).fit()
print("\nMultiple regression: price ~ bedrooms + size")
print(model_two.summary())

print(f"\nComparison of bedrooms coefficient:")
print(f"  Bivariate model: {model_one.params['bedrooms']:.4f}")
print(f"  Multiple regression: {model_two.params['bedrooms']:.4f}")
print(f"  Change: {model_two.params['bedrooms'] - model_one.params['bedrooms']:.4f}")

# ========== 10.2 TWO-WAY SCATTERPLOTS ==========

print("\n" + "=" * 70)
print("10.2 TWO-WAY SCATTERPLOTS")
print("=" * 70)

# Figure 10.1 - Scatterplot matrix
print("\nGenerating scatterplot matrix...")

plot_vars = ['price', 'size', 'bedrooms', 'age']
fig = plt.figure(figsize=(12, 12))

# Create pairplot using seaborn
g = sns.pairplot(data_house[plot_vars], diag_kind='kde', plot_kws={'alpha': 0.6, 's': 50})
# g.fig.suptitle('Figure 10.1: Simple Scatterplot Matrix', fontsize=14,
#                fontweight='bold', y=1.00)  # Removed: redundant with LaTeX caption

output_file = os.path.join(IMAGES_DIR, 'ch10_fig1_scatterplot_matrix.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"Figure saved to: {output_file}")
plt.close()

# ========== 10.3 CORRELATION ==========

print("\n" + "=" * 70)
print("10.3 CORRELATION")
print("=" * 70)

# Table 10.3 - Correlation matrix
print("\n" + "-" * 70)
print("Table 10.3: Correlation Matrix")
print("-" * 70)

corr_vars = ['price', 'size', 'bedrooms', 'bathrooms', 'lotsize', 'age', 'monthsold']
corr_matrix = data_house[corr_vars].corr()
print(corr_matrix)
corr_matrix.to_csv(os.path.join(TABLES_DIR, 'ch10_correlation_matrix.csv'))
print(f"Table saved to: {os.path.join(TABLES_DIR, 'ch10_correlation_matrix.csv')}")

# Visualize correlation matrix
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='coolwarm', center=0,
            square=True, linewidths=1, cbar_kws={"shrink": 0.8})
# ax.set_title('Correlation Matrix Heatmap', fontsize=14, fontweight='bold')  # Removed: redundant with LaTeX caption
# 
output_file = os.path.join(IMAGES_DIR, 'ch10_correlation_heatmap.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\nCorrelation heatmap saved to: {output_file}")
plt.close()

# ========== 10.4 REGRESSION LINE ==========

print("\n" + "=" * 70)
print("10.4 REGRESSION LINE")
print("=" * 70)

# Full multiple regression
print("\n" + "-" * 70)
print("Multiple Regression: Full Model")
print("-" * 70)

model_full = ols('price ~ size + bedrooms + bathrooms + lotsize + age + monthsold',
                 data=data_house).fit()
print(model_full.summary())
# Save regression summary
with open(os.path.join(TABLES_DIR, 'ch10_regression_summary.txt'), 'w') as f:
    f.write(model_full.summary().as_text())
# Save coefficients
coef_table = pd.DataFrame({
    'coefficient': model_full.params,
    'std_err': model_full.bse,
    't_value': model_full.tvalues,
    'p_value': model_full.pvalues
})
coef_table.to_csv(os.path.join(TABLES_DIR, 'ch10_regression_coefficients.csv'))
print(f"Coefficients saved to: {os.path.join(TABLES_DIR, 'ch10_regression_coefficients.csv')}")

# Display coefficients with confidence intervals
print("\n" + "-" * 70)
print("Coefficients with 95% Confidence Intervals")
print("-" * 70)
conf_int = model_full.conf_int(alpha=0.05)
coef_table = pd.DataFrame({
    'Coefficient': model_full.params,
    'Std. Error': model_full.bse,
    'CI Lower': conf_int.iloc[:, 0],
    'CI Upper': conf_int.iloc[:, 1],
    't-statistic': model_full.tvalues,
    'p-value': model_full.pvalues
})
print(coef_table)

# ========== 10.5 ESTIMATED PARTIAL EFFECTS ==========

print("\n" + "=" * 70)
print("10.5 ESTIMATED PARTIAL EFFECTS")
print("=" * 70)

print("\nDemonstration: Coefficient from multiple regression equals")
print("coefficient from bivariate regression on residualized regressor")

# Step 1: Regress size on other variables
model_size = ols('size ~ bedrooms + bathrooms + lotsize + age + monthsold',
                 data=data_house).fit()
resid_size = model_size.resid

# Step 2: Regress price on residualized size
data_house['resid_size'] = resid_size
model_biv = ols('price ~ resid_size', data=data_house).fit()

print(f"\nCoefficient on size from full multiple regression: {model_full.params['size']:.6f}")
print(f"Coefficient on resid_size from bivariate regression: {model_biv.params['resid_size']:.6f}")
print(f"Difference: {abs(model_full.params['size'] - model_biv.params['resid_size']):.10f}")
print("\nThese coefficients are identical (within numerical precision)")

# ========== 10.6 MODEL FIT ==========

print("\n" + "=" * 70)
print("10.6 MODEL FIT")
print("=" * 70)

# R-squared and related statistics
print("\n" + "-" * 70)
print("Model Fit Statistics")
print("-" * 70)

n = len(data_house)
k = len(model_full.params)  # includes intercept
df = n - k

print(f"Sample size (n): {n}")
print(f"Number of parameters (k): {k}")
print(f"Degrees of freedom (n-k): {df}")
print(f"\nR-squared: {model_full.rsquared:.6f}")
print(f"Adjusted R-squared: {model_full.rsquared_adj:.6f}")
print(f"Root MSE: {np.sqrt(model_full.mse_resid):.6f}")

# Verify R-squared is squared correlation between y and yhat
predicted = model_full.fittedvalues
corr_y_yhat = np.corrcoef(data_house['price'], predicted)[0, 1]
rsq_check = corr_y_yhat ** 2

print(f"\nVerification:")
print(f"  Correlation(y, ŷ): {corr_y_yhat:.6f}")
print(f"  [Correlation(y, ŷ)]²: {rsq_check:.6f}")
print(f"  R²: {model_full.rsquared:.6f}")
print(f"  Match: {np.isclose(rsq_check, model_full.rsquared)}")

# Manual calculation of adjusted R-squared
r2 = model_full.rsquared
r2_adj_manual = r2 - ((k-1)/df) * (1 - r2)
print(f"\nManual calculation of adjusted R²: {r2_adj_manual:.6f}")
print(f"From model output: {model_full.rsquared_adj:.6f}")

# Calculate AIC and BIC
print("\n" + "-" * 70)
print("Information Criteria")
print("-" * 70)

# Sum of squared residuals
rss = np.sum(model_full.resid ** 2)

# AIC (Python/statsmodels convention)
aic_statsmodels = model_full.aic
print(f"AIC (statsmodels): {aic_statsmodels:.4f}")

# BIC (Python/statsmodels convention)
bic_statsmodels = model_full.bic
print(f"BIC (statsmodels): {bic_statsmodels:.4f}")

# Manual calculation (Stata convention)
aic_stata = n * np.log(rss/n) + n * (1 + np.log(2*np.pi)) + 2*k
bic_stata = n * np.log(rss/n) + n * (1 + np.log(2*np.pi)) + k*np.log(n)
print(f"\nAIC (Stata convention): {aic_stata:.4f}")
print(f"BIC (Stata convention): {bic_stata:.4f}")

# ========== 10.7 COMPUTER OUTPUT FOLLOWING MULTIPLE REGRESSION ==========

print("\n" + "=" * 70)
print("10.7 COMPUTER OUTPUT FOLLOWING MULTIPLE REGRESSION")
print("=" * 70)

# Compare multiple models side by side
print("\n" + "-" * 70)
print("Model Comparison Table")
print("-" * 70)

# Simple model
model_small = ols('price ~ size', data=data_house).fit()

# Create comparison table
comparison_df = pd.DataFrame({
    'Variable': model_full.params.index,
    'Full Model Coef': model_full.params.values,
    'Full Model SE': model_full.bse.values,
    'Full Model t': model_full.tvalues.values,
})

# Add simple model coefficients where applicable
simple_coefs = pd.Series(index=model_full.params.index, dtype=float)
simple_se = pd.Series(index=model_full.params.index, dtype=float)
simple_t = pd.Series(index=model_full.params.index, dtype=float)

simple_coefs['Intercept'] = model_small.params['Intercept']
simple_coefs['size'] = model_small.params['size']
simple_se['Intercept'] = model_small.bse['Intercept']
simple_se['size'] = model_small.bse['size']
simple_t['Intercept'] = model_small.tvalues['Intercept']
simple_t['size'] = model_small.tvalues['size']

comparison_df['Simple Model Coef'] = simple_coefs.values
comparison_df['Simple Model SE'] = simple_se.values
comparison_df['Simple Model t'] = simple_t.values

print(comparison_df)

print(f"\n{'Model':<20} {'R²':<10} {'Adj R²':<10} {'N':<5}")
print("-" * 50)
print(f"{'Full Model':<20} {model_full.rsquared:<10.4f} {model_full.rsquared_adj:<10.4f} {n:<5}")
print(f"{'Simple Model':<20} {model_small.rsquared:<10.4f} {model_small.rsquared_adj:<10.4f} {n:<5}")

# ========== 10.8 INESTIMABLE MODELS ==========

print("\n" + "=" * 70)
print("10.8 INESTIMABLE MODELS")
print("=" * 70)

print("\nExample: Perfect multicollinearity")
print("Creating a redundant variable (size_twice = 2 * size)...")

# Create a perfectly collinear variable
data_house['size_twice'] = 2 * data_house['size']

print("\nAttempting to estimate model with perfect collinearity:")
try:
    model_collinear = ols('price ~ size + size_twice + bedrooms',
                          data=data_house).fit()
    print("Model estimated. Checking for dropped variables...")
    print(model_collinear.summary())
except Exception as e:
    print(f"Error encountered: {type(e).__name__}")
    print(f"Message: {str(e)}")

# Demonstrate with rank-deficient design matrix
print("\n" + "-" * 70)
print("Checking for multicollinearity in the full model")
print("-" * 70)

# Variance Inflation Factors (VIF)
from statsmodels.stats.outliers_influence import variance_inflation_factor

X = data_house[['size', 'bedrooms', 'bathrooms', 'lotsize', 'age', 'monthsold']]
vif_data = pd.DataFrame()
vif_data["Variable"] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]

print("\nVariance Inflation Factors (VIF):")
print(vif_data)
print("\nNote: VIF > 10 often indicates problematic multicollinearity")
vif_data.to_csv(os.path.join(TABLES_DIR, 'ch10_vif_table.csv'), index=False)
print(f"Table saved to: {os.path.join(TABLES_DIR, 'ch10_vif_table.csv')}")

# ========== VISUALIZATION ==========

print("\n" + "=" * 70)
print("GENERATING ADDITIONAL FIGURES")
print("=" * 70)

# Figure: Actual vs Predicted
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(data_house['price'], model_full.fittedvalues, alpha=0.6, s=50, color='black')
ax.plot([data_house['price'].min(), data_house['price'].max()],
        [data_house['price'].min(), data_house['price'].max()],
        'r--', linewidth=2, label='Perfect prediction')
ax.set_xlabel('Actual Price ($1000s)', fontsize=12)
ax.set_ylabel('Predicted Price ($1000s)', fontsize=12)
# ax.set_title('Actual vs Predicted House Prices', fontsize=14, fontweight='bold')  # Removed: redundant with LaTeX caption
ax.legend()
ax.grid(True, alpha=0.3)

output_file = os.path.join(IMAGES_DIR, 'ch10_actual_vs_predicted.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\nFigure saved to: {output_file}")
plt.close()

# Figure: Residual plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(model_full.fittedvalues, model_full.resid, alpha=0.6, s=50, color='black')
ax.axhline(y=0, color='red', linestyle='--', linewidth=2)
ax.set_xlabel('Fitted values', fontsize=12)
ax.set_ylabel('Residuals', fontsize=12)
# ax.set_title('Residual Plot: Multiple Regression', fontsize=14, fontweight='bold')  # Removed: redundant with LaTeX caption
ax.grid(True, alpha=0.3)

output_file = os.path.join(IMAGES_DIR, 'ch10_residual_plot.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"Figure saved to: {output_file}")
plt.close()

# Figure: Coefficient plot with confidence intervals
fig, ax = plt.subplots(figsize=(10, 8))

# Exclude intercept for better visualization
params_no_int = model_full.params[1:]
ci_no_int = conf_int.iloc[1:, :]

y_pos = np.arange(len(params_no_int))
ax.errorbar(params_no_int.values, y_pos,
            xerr=[params_no_int.values - ci_no_int.iloc[:, 0].values,
                  ci_no_int.iloc[:, 1].values - params_no_int.values],
            fmt='o', markersize=8, capsize=5, capthick=2, linewidth=2)
ax.set_yticks(y_pos)
ax.set_yticklabels(params_no_int.index)
ax.axvline(x=0, color='red', linestyle='--', linewidth=1, alpha=0.5)
ax.set_xlabel('Coefficient Value', fontsize=12)
# ax.set_title('Coefficient Estimates with 95% Confidence Intervals',
#              fontsize=14, fontweight='bold')  # Removed: redundant with LaTeX caption
ax.grid(True, alpha=0.3, axis='x')

output_file = os.path.join(IMAGES_DIR, 'ch10_coefficient_plot.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"Figure saved to: {output_file}")
plt.close()

# ========== SUMMARY ==========

print("\n" + "=" * 70)
print("CHAPTER 10 ANALYSIS COMPLETE")
print("=" * 70)
print("\nKey concepts demonstrated:")
print("  - Multiple regression with several regressors")
print("  - Two-way scatterplots and correlation matrices")
print("  - Partial effects and interpretation")
print("  - Model fit statistics (R², adjusted R², AIC, BIC)")
print("  - Comparison of multiple models")
print("  - Detection of multicollinearity using VIF")
print("\nAll figures saved to:", IMAGES_DIR)
