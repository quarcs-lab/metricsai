"""
ch07_Statistical_Inference_for_Bivariate_Regression.py - January 2026 for Python

Python Program
Copyright (C) 2021 by A. Colin Cameron (original R/Stata code)
Python translation: 2026

Used for "Analysis of Economics Data: An Introduction to Econometrics"
by A. Colin Cameron (2021)

Chapter 7: STATISTICAL INFERENCE FOR BIVARIATE REGRESSION

To run you need files:
  AED_HOUSE.DTA
  AED_REALGDPPC.DTA
in the data/ directory

Sections covered:
  7.1 EXAMPLE: HOUSE PRICE AND SIZE
  7.2 THE T STATISTIC
  7.3 CONFIDENCE INTERVALS
  7.4 TESTS OF STATISTICAL SIGNIFICANCE
  7.5 TWO-SIDED HYPOTHESIS TESTS
  7.6 ONE-SIDED DIRECTIONAL HYPOTHESIS TESTS
  7.7 ROBUST STANDARD ERRORS

Translated from R and Stata code
"""

# ========== SETUP ==========

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from statsmodels.formula.api import ols
from scipy import stats
from statsmodels.stats.sandwich_covariance import cov_hc1
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
print("CHAPTER 7: STATISTICAL INFERENCE FOR BIVARIATE REGRESSION")
print("=" * 70)

# ========== 7.1 EXAMPLE: HOUSE PRICE AND SIZE ==========

print("\n" + "=" * 70)
print("7.1 EXAMPLE: HOUSE PRICE AND SIZE")
print("=" * 70)

# Read in the house data
data_house = pd.read_stata(GITHUB_DATA_URL + 'AED_HOUSE.DTA')

print("\nData summary:")
data_summary = data_house.describe()
print(data_summary)
print("\nFirst few observations:")
print(data_house.head())
data_summary.to_csv(os.path.join(TABLES_DIR, 'ch07_house_descriptive_stats.csv'))
print(f"Table saved to: {os.path.join(TABLES_DIR, 'ch07_house_descriptive_stats.csv')}")

# Table 7.1 - Basic regression
print("\n" + "-" * 70)
print("Table 7.1: Regression of House Price on Size")
print("-" * 70)

model_basic = ols('price ~ size', data=data_house).fit()
print(model_basic.summary())
# Save regression summary
with open(os.path.join(TABLES_DIR, 'ch07_regression_summary.txt'), 'w') as f:
    f.write(model_basic.summary().as_text())
# Save coefficients
coef_table = pd.DataFrame({
    'coefficient': model_basic.params,
    'std_err': model_basic.bse,
    't_value': model_basic.tvalues,
    'p_value': model_basic.pvalues
})
coef_table.to_csv(os.path.join(TABLES_DIR, 'ch07_regression_coefficients.csv'))
print(f"Coefficients saved to: {os.path.join(TABLES_DIR, 'ch07_regression_coefficients.csv')}")

# ========== 7.2 THE T STATISTIC ==========

print("\n" + "=" * 70)
print("7.2 THE T STATISTIC")
print("=" * 70)

print("\nRegression coefficients and t-statistics:")
print(model_basic.summary2().tables[1])

# Extract key statistics
coef_size = model_basic.params['size']
se_size = model_basic.bse['size']
t_stat_size = model_basic.tvalues['size']
p_value_size = model_basic.pvalues['size']

print(f"\nDetailed statistics for 'size' coefficient:")
print(f"  Coefficient: {coef_size:.4f}")
print(f"  Standard Error: {se_size:.4f}")
print(f"  t-statistic: {t_stat_size:.4f}")
print(f"  p-value: {p_value_size:.6f}")

# ========== 7.3 CONFIDENCE INTERVALS ==========

print("\n" + "=" * 70)
print("7.3 CONFIDENCE INTERVALS")
print("=" * 70)

# 95% confidence intervals
conf_int = model_basic.conf_int(alpha=0.05)
print("\n95% Confidence Intervals:")
print(conf_int)

# Manual calculation of confidence interval for size
n = len(data_house)
df = n - 2
t_crit = stats.t.ppf(0.975, df)

ci_lower = coef_size - t_crit * se_size
ci_upper = coef_size + t_crit * se_size

print(f"\nManual calculation for 'size' coefficient:")
print(f"  Sample size: {n}")
print(f"  Degrees of freedom: {df}")
print(f"  Critical t-value (α=0.05): {t_crit:.4f}")
print(f"  95% CI: [{ci_lower:.4f}, {ci_upper:.4f}]")

# Example with artificial data
print("\n" + "-" * 70)
print("Example with artificial data")
print("-" * 70)

x = np.array([1, 2, 3, 4, 5])
y = np.array([1, 2, 2, 2, 3])
df_artificial = pd.DataFrame({'x': x, 'y': y})

model_artificial = ols('y ~ x', data=df_artificial).fit()
print(model_artificial.summary())

coef_x = model_artificial.params['x']
se_x = model_artificial.bse['x']
n_art = len(x)
df_art = n_art - 2
t_crit_art = stats.t.ppf(0.975, df_art)

ci_lower_art = coef_x - t_crit_art * se_x
ci_upper_art = coef_x + t_crit_art * se_x

print(f"\nManual CI for artificial data:")
print(f"  Coefficient: {coef_x:.4f}")
print(f"  Standard Error: {se_x:.4f}")
print(f"  95% CI: [{ci_lower_art:.4f}, {ci_upper_art:.4f}]")

# ========== 7.4 TESTS OF STATISTICAL SIGNIFICANCE ==========

print("\n" + "=" * 70)
print("7.4 TESTS OF STATISTICAL SIGNIFICANCE")
print("=" * 70)

print("\nNull hypothesis: β₁ = 0 (size has no effect on price)")
print(f"t-statistic: {t_stat_size:.4f}")
print(f"p-value: {p_value_size:.6f}")

if p_value_size < 0.05:
    print("Result: Reject H₀ at 5% significance level")
    print("Conclusion: Size has a statistically significant effect on price")
else:
    print("Result: Fail to reject H₀ at 5% significance level")

# ========== 7.5 TWO-SIDED HYPOTHESIS TESTS ==========

print("\n" + "=" * 70)
print("7.5 TWO-SIDED HYPOTHESIS TESTS")
print("=" * 70)

# Test H₀: β₁ = 90 vs H₁: β₁ ≠ 90
null_value = 90
t_stat_90 = (coef_size - null_value) / se_size
p_value_90 = 2 * (1 - stats.t.cdf(abs(t_stat_90), df))
t_crit_90 = stats.t.ppf(0.975, df)

print(f"\nTest: H₀: β₁ = {null_value} vs H₁: β₁ ≠ {null_value}")
print(f"  t-statistic: {t_stat_90:.4f}")
print(f"  p-value: {p_value_90:.6f}")
print(f"  Critical value (α=0.05): ±{t_crit_90:.4f}")

if abs(t_stat_90) > t_crit_90:
    print(f"Result: Reject H₀ (|t| = {abs(t_stat_90):.4f} > {t_crit_90:.4f})")
else:
    print(f"Result: Fail to reject H₀ (|t| = {abs(t_stat_90):.4f} < {t_crit_90:.4f})")

# Using statsmodels hypothesis test
print("\n" + "-" * 70)
print("Hypothesis test using statsmodels:")
print("-" * 70)

# Alternative approach using t_test
hypothesis = f'size = {null_value}'
t_test_result = model_basic.t_test(hypothesis)
print(t_test_result)

# ========== 7.6 ONE-SIDED DIRECTIONAL HYPOTHESIS TESTS ==========

print("\n" + "=" * 70)
print("7.6 ONE-SIDED DIRECTIONAL HYPOTHESIS TESTS")
print("=" * 70)

# Upper one-tailed test: H₀: β₁ ≤ 90 vs H₁: β₁ > 90
p_value_upper = 1 - stats.t.cdf(t_stat_90, df)
t_crit_upper = stats.t.ppf(0.95, df)

print(f"\nUpper one-tailed test: H₀: β₁ ≤ {null_value} vs H₁: β₁ > {null_value}")
print(f"  t-statistic: {t_stat_90:.4f}")
print(f"  p-value (one-tailed): {p_value_upper:.6f}")
print(f"  Critical value (α=0.05): {t_crit_upper:.4f}")

if t_stat_90 > t_crit_upper:
    print("Result: Reject H₀")
else:
    print("Result: Fail to reject H₀")

# Lower one-tailed test: H₀: β₁ ≥ 90 vs H₁: β₁ < 90
p_value_lower = stats.t.cdf(t_stat_90, df)

print(f"\nLower one-tailed test: H₀: β₁ ≥ {null_value} vs H₁: β₁ < {null_value}")
print(f"  t-statistic: {t_stat_90:.4f}")
print(f"  p-value (one-tailed): {p_value_lower:.6f}")
print(f"  Critical value (α=0.05): {-t_crit_upper:.4f}")

if t_stat_90 < -t_crit_upper:
    print("Result: Reject H₀")
else:
    print("Result: Fail to reject H₀")

# ========== 7.7 ROBUST STANDARD ERRORS ==========

print("\n" + "=" * 70)
print("7.7 ROBUST STANDARD ERRORS")
print("=" * 70)

# Get heteroskedasticity-robust standard errors (HC1)
robust_results = model_basic.get_robustcov_results(cov_type='HC1')

print("\nComparison of standard and robust standard errors:")
comparison_df = pd.DataFrame({
    'Coefficient': model_basic.params,
    'Std. Error': model_basic.bse,
    'Robust SE': robust_results.bse,
    't-stat (standard)': model_basic.tvalues,
    't-stat (robust)': robust_results.tvalues,
    'p-value (standard)': model_basic.pvalues,
    'p-value (robust)': robust_results.pvalues
})
print(comparison_df)
comparison_df.to_csv(os.path.join(TABLES_DIR, 'ch07_robust_vs_standard_se.csv'))
print(f"Table saved to: {os.path.join(TABLES_DIR, 'ch07_robust_vs_standard_se.csv')}")

print("\n" + "-" * 70)
print("Regression with robust standard errors:")
print("-" * 70)
print(robust_results.summary())

# Robust confidence intervals
robust_conf_int = robust_results.conf_int(alpha=0.05)
print("\n95% Confidence Intervals (Robust):")
print(robust_conf_int)

# ========== VISUALIZATION ==========

print("\n" + "=" * 70)
print("GENERATING FIGURES")
print("=" * 70)

# Figure 7.1: Scatter plot with regression line
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(data_house['size'], data_house['price'], alpha=0.6, s=50,
           color='black', label='Actual observations')
ax.plot(data_house['size'], model_basic.fittedvalues, color='blue',
        linewidth=2, label='Fitted regression line')
ax.set_xlabel('Size (square feet)', fontsize=12)
ax.set_ylabel('Price ($1000s)', fontsize=12)
ax.set_title('Figure 7.1: House Price vs Size with Regression Line',
             fontsize=14, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)

output_file = os.path.join(IMAGES_DIR, 'ch07_fig1_house_price_size.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\nFigure saved to: {output_file}")
plt.close()

# Figure 7.2: Confidence interval visualization
fig, ax = plt.subplots(figsize=(10, 6))

# Plot point estimate and confidence interval
coef_names = ['Intercept', 'Size']
coefs = model_basic.params.values
ci_low = conf_int.iloc[:, 0].values
ci_high = conf_int.iloc[:, 1].values

y_pos = np.arange(len(coef_names))
ax.errorbar(coefs, y_pos, xerr=[coefs - ci_low, ci_high - coefs],
            fmt='o', markersize=8, capsize=5, capthick=2, linewidth=2)
ax.set_yticks(y_pos)
ax.set_yticklabels(coef_names)
ax.axvline(x=0, color='red', linestyle='--', linewidth=1, alpha=0.5)
ax.set_xlabel('Coefficient Value', fontsize=12)
ax.set_title('Figure 7.2: Coefficient Estimates with 95% Confidence Intervals',
             fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, axis='x')

output_file = os.path.join(IMAGES_DIR, 'ch07_fig2_confidence_intervals.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"Figure saved to: {output_file}")
plt.close()

# Figure 7.3: Residual plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(model_basic.fittedvalues, model_basic.resid, alpha=0.6, s=50, color='black')
ax.axhline(y=0, color='red', linestyle='--', linewidth=2)
ax.set_xlabel('Fitted values', fontsize=12)
ax.set_ylabel('Residuals', fontsize=12)
ax.set_title('Figure 7.3: Residual Plot', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)

output_file = os.path.join(IMAGES_DIR, 'ch07_fig3_residuals.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"Figure saved to: {output_file}")
plt.close()

# ========== SUMMARY ==========

print("\n" + "=" * 70)
print("CHAPTER 7 ANALYSIS COMPLETE")
print("=" * 70)
print("\nKey concepts demonstrated:")
print("  - T-statistics for testing hypotheses about regression coefficients")
print("  - Construction and interpretation of confidence intervals")
print("  - Two-sided hypothesis tests")
print("  - One-sided directional hypothesis tests")
print("  - Heteroskedasticity-robust standard errors")
print("  - Statistical significance and p-values")
print("\nAll figures saved to:", IMAGES_DIR)
