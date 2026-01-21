"""
ch12_Further_Topics_in_Multiple_Regression.py - January 2026 for Python

Python Program
Copyright (C) 2021 by A. Colin Cameron (original Stata code)
Python translation: 2026

Used for "Analysis of Economics Data: An Introduction to Econometrics"
by A. Colin Cameron (2021)

Chapter 12: FURTHER TOPICS IN MULTIPLE REGRESSION

To run you need files:
  AED_HOUSE.DTA
  AED_REALGDPPC.DTA
in the data/ directory

Sections covered:
  12.1 INFERENCE WITH ROBUST STANDARD ERRORS
  12.2 PREDICTION
  12.3 NONREPRESENTATIVE SAMPLES (conceptual)
  12.4 BEST ESTIMATION (conceptual)
  12.5 BEST CONFIDENCE INTERVALS (conceptual)
  12.6 BEST TESTS (conceptual)
  12.7 DATA SCIENCE AND BIG DATA: AN OVERVIEW (conceptual)
  12.8 BAYESIAN METHODS: AN OVERVIEW (conceptual)
  12.9 A BRIEF HISTORY OF STATISTICS, REGRESSION AND ECONOMETRICS (conceptual)

Translated from Stata code
"""

# ========== SETUP ==========

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.regression.linear_model import OLS
from scipy import stats
from statsmodels.stats.sandwich_covariance import cov_hac
from statsmodels.graphics.tsaplots import plot_acf
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
print("CHAPTER 12: FURTHER TOPICS IN MULTIPLE REGRESSION")
print("=" * 70)

# ========== 12.1 INFERENCE WITH ROBUST STANDARD ERRORS ==========

print("\n" + "=" * 70)
print("12.1 INFERENCE WITH ROBUST STANDARD ERRORS")
print("=" * 70)

# Load house data
data_house = pd.read_stata(GITHUB_DATA_URL + 'AED_HOUSE.DTA')

print("\nHouse Data Summary:")
house_summary = data_house.describe()
print(house_summary)
house_summary.to_csv(os.path.join(TABLES_DIR, 'ch12_house_descriptive_stats.csv'))
print(f"Table saved to: {os.path.join(TABLES_DIR, 'ch12_house_descriptive_stats.csv')}")

# Table 12.2: Regression with heteroskedastic-robust standard errors (HC1)
print("\n" + "-" * 70)
print("Table 12.2: Multiple Regression with Heteroskedastic-Robust SEs")
print("-" * 70)

model_robust = ols('price ~ size + bedrooms + bathrooms + lotsize + age + monthsold',
                   data=data_house).fit(cov_type='HC1')

print(model_robust.summary())

print("\nNote: HC1 robust standard errors adjust for heteroskedasticity")
print("These are also called White's heteroskedastic-robust standard errors")

# Compare default vs robust standard errors
model_default = ols('price ~ size + bedrooms + bathrooms + lotsize + age + monthsold',
                    data=data_house).fit()

comparison_table = pd.DataFrame({
    'Coefficient': model_default.params,
    'SE (Default)': model_default.bse,
    'SE (HC1)': model_robust.bse,
    'SE Ratio': model_robust.bse / model_default.bse
})

print("\n" + "-" * 70)
print("Comparison of Default vs HC1 Robust Standard Errors")
print("-" * 70)
print(comparison_table)
comparison_table.to_csv(os.path.join(TABLES_DIR, 'ch12_robust_vs_default_se.csv'))
print(f"Table saved to: {os.path.join(TABLES_DIR, 'ch12_robust_vs_default_se.csv')}")

# HAC standard errors for the mean (using GDP growth data)
print("\n" + "-" * 70)
print("HAC Standard Errors for Time Series Data")
print("-" * 70)

# Load GDP data
data_gdp = pd.read_stata(GITHUB_DATA_URL + 'AED_REALGDPPC.DTA')

print("\nGDP Growth Data Summary:")
print(data_gdp['growth'].describe())

# Mean of growth
mean_growth = data_gdp['growth'].mean()
print(f"\nMean growth rate: {mean_growth:.6f}")

# Regress growth on constant (to get mean and standard error)
# Default standard errors
X_const = sm.add_constant(np.ones(len(data_gdp)))
model_mean = OLS(data_gdp['growth'], X_const).fit()

print("\nRegression on constant (default SEs):")
print(f"  Mean: {model_mean.params[0]:.6f}")
print(f"  SE: {model_mean.bse[0]:.6f}")

# Lag 1 autocorrelation manually
data_gdp['growthlag1'] = data_gdp['growth'].shift(1)
corr_lag1 = data_gdp[['growth', 'growthlag1']].corr().iloc[0, 1]
print(f"\nLag 1 autocorrelation: {corr_lag1:.6f}")

# Multiple lag autocorrelations
print("\nAutocorrelations at multiple lags:")
from statsmodels.tsa.stattools import acf
acf_values = acf(data_gdp['growth'], nlags=5, fft=False)
for i in range(6):
    print(f"  Lag {i}: {acf_values[i]:.6f}")

# Correlogram
print("\nCorrelogram (see Figure 12.1a)")
fig, ax = plt.subplots(figsize=(10, 6))
plot_acf(data_gdp['growth'], lags=10, ax=ax, alpha=0.05)
ax.set_xlabel('Lag')
ax.set_ylabel('Autocorrelation')
ax.set_title('Correlogram of GDP Growth')
plt.tight_layout()
plt.savefig(os.path.join(IMAGES_DIR, 'ch12_correlogram_growth.png'), dpi=300, bbox_inches='tight')
print(f"Saved: {os.path.join(IMAGES_DIR, 'ch12_correlogram_growth.png')}")
plt.close()

# HAC standard errors with different lags (Newey-West)
print("\nNewey-West HAC Standard Errors:")

# Lag 0 (no autocorrelation correction - same as default)
model_hac0 = OLS(data_gdp['growth'], X_const).fit(cov_type='HAC', cov_kwds={'maxlags': 0})
print(f"\nLag 0 (no HAC correction):")
print(f"  Mean: {model_hac0.params[0]:.6f}")
print(f"  SE: {model_hac0.bse[0]:.6f}")

# Lag 5
model_hac5 = OLS(data_gdp['growth'], X_const).fit(cov_type='HAC', cov_kwds={'maxlags': 5})
print(f"\nLag 5 (HAC with maxlags=5):")
print(f"  Mean: {model_hac5.params[0]:.6f}")
print(f"  SE: {model_hac5.bse[0]:.6f}")

print("\nNote: HAC (Newey-West) standard errors account for both")
print("heteroskedasticity and autocorrelation in time series data")

# ========== 12.2 PREDICTION ==========

print("\n" + "=" * 70)
print("12.2 PREDICTION")
print("=" * 70)

# Simple regression: price on size
model_simple = ols('price ~ size', data=data_house).fit()

print("\nSimple regression: price = β₀ + β₁*size + u")
print(model_simple.summary())

# Figure 12.1: Confidence intervals for conditional mean vs actual value
print("\n" + "-" * 70)
print("Figure 12.1: Prediction Intervals")
print("-" * 70)

# Prepare prediction data
size_range = np.linspace(data_house['size'].min(), data_house['size'].max(), 100)
pred_df = pd.DataFrame({'size': size_range})

# Predictions with confidence intervals
predictions = model_simple.get_prediction(sm.add_constant(pred_df))
pred_mean = predictions.predicted_mean
pred_ci = predictions.conf_int(alpha=0.05)  # Confidence interval for conditional mean
pred_pi = predictions.conf_int(obs=True, alpha=0.05)  # Prediction interval for actual value

# Create two-panel figure
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Panel 1: Confidence Interval for Conditional Mean
axes[0].scatter(data_house['size'], data_house['price'], alpha=0.6, label='Observed data')
axes[0].plot(size_range, pred_mean, 'r-', linewidth=2, label='Fitted line')
axes[0].fill_between(size_range, pred_ci[:, 0], pred_ci[:, 1],
                     alpha=0.3, color='red', label='95% CI for E[Y|X]')
axes[0].set_xlabel('Size (sq ft)')
axes[0].set_ylabel('Price ($1000)')
axes[0].set_title('Confidence Interval for Conditional Mean')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Panel 2: Prediction Interval for Actual Value
axes[1].scatter(data_house['size'], data_house['price'], alpha=0.6, label='Observed data')
axes[1].plot(size_range, pred_mean, 'r-', linewidth=2, label='Fitted line')
axes[1].fill_between(size_range, pred_pi[:, 0], pred_pi[:, 1],
                     alpha=0.3, color='blue', label='95% PI for Y')
axes[1].set_xlabel('Size (sq ft)')
axes[1].set_ylabel('Price ($1000)')
axes[1].set_title('Prediction Interval for Actual Value')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(IMAGES_DIR, 'ch12_fig1_prediction_intervals.png'), dpi=300, bbox_inches='tight')
print(f"Saved: {os.path.join(IMAGES_DIR, 'ch12_fig1_prediction_intervals.png')}")
plt.close()

# Predict conditional mean for house size = 2000
print("\n" + "-" * 70)
print("Prediction at size = 2000 sq ft")
print("-" * 70)

# Manual calculation
b0 = model_simple.params['Intercept']
b1 = model_simple.params['size']
pred_2000 = b0 + b1 * 2000

print(f"\nManual calculation:")
print(f"  β₀ = {b0:.6f}")
print(f"  β₁ = {b1:.6f}")
print(f"  Predicted price at size=2000: {pred_2000:.2f}")

# Using statsmodels prediction
new_data = pd.DataFrame({'size': [2000]})
prediction = model_simple.get_prediction(sm.add_constant(new_data))

print(f"\nUsing statsmodels prediction:")
print(f"  Predicted price: {prediction.predicted_mean[0]:.2f}")
print(f"  SE for conditional mean: {prediction.se_mean[0]:.6f}")

# Confidence interval for conditional mean
ci_mean = prediction.conf_int(alpha=0.05)
print(f"  95% CI for E[Y|X=2000]: [{ci_mean[0, 0]:.2f}, {ci_mean[0, 1]:.2f}]")

# Prediction interval for actual value
pi_actual = prediction.conf_int(obs=True, alpha=0.05)
print(f"  95% PI for Y at X=2000: [{pi_actual[0, 0]:.2f}, {pi_actual[0, 1]:.2f}]")

# Manual calculation of standard errors
print("\n" + "-" * 70)
print("Manual Calculation of Standard Errors")
print("-" * 70)

n = len(data_house)
xbar = data_house['size'].mean()
sumxminusxbarsq = ((data_house['size'] - xbar) ** 2).sum()
s_e = np.sqrt(model_simple.mse_resid)

y_cm = b0 + b1 * 2000
y_f = b0 + b1 * 2000

# Standard error for conditional mean
s_y_cm = s_e * np.sqrt(1/n + (2000 - xbar)**2 / sumxminusxbarsq)

# Standard error for actual value
s_y_f = s_e * np.sqrt(1 + 1/n + (2000 - xbar)**2 / sumxminusxbarsq)

# Critical t-value
tcrit = stats.t.ppf(0.975, n - 2)

print(f"\nStatistics:")
print(f"  n = {n}")
print(f"  Mean of size = {xbar:.2f}")
print(f"  Sum(x - x̄)² = {sumxminusxbarsq:.2f}")
print(f"  Root MSE (σ̂) = {s_e:.6f}")
print(f"  Critical t-value (df={n-2}, α=0.05): {tcrit:.4f}")

print(f"\nConditional mean at size = 2000:")
print(f"  ŷ = {y_cm:.2f}")
print(f"  SE for conditional mean = {s_y_cm:.6f}")
print(f"  Margin of error = {tcrit * s_y_cm:.2f}")
print(f"  95% CI: [{y_cm - tcrit*s_y_cm:.2f}, {y_cm + tcrit*s_y_cm:.2f}]")

print(f"\nActual value at size = 2000:")
print(f"  ŷ = {y_f:.2f}")
print(f"  SE for actual value = {s_y_f:.6f}")
print(f"  Margin of error = {tcrit * s_y_f:.2f}")
print(f"  95% PI: [{y_f - tcrit*s_y_f:.2f}, {y_f + tcrit*s_y_f:.2f}]")

# Predict for multiple regression
print("\n" + "-" * 70)
print("Prediction for Multiple Regression")
print("-" * 70)

model_multi = ols('price ~ size + bedrooms + bathrooms + lotsize + age + monthsold',
                  data=data_house).fit()

# Predict for specific values
new_house = pd.DataFrame({
    'size': [2000],
    'bedrooms': [4],
    'bathrooms': [2],
    'lotsize': [2],
    'age': [40],
    'monthsold': [6]
})

pred_multi = model_multi.get_prediction(sm.add_constant(new_house))

print("\nPrediction for:")
print("  size=2000, bedrooms=4, bathrooms=2, lotsize=2, age=40, monthsold=6")
print(f"\nPredicted price: {pred_multi.predicted_mean[0]:.2f}")
print(f"SE for conditional mean: {pred_multi.se_mean[0]:.6f}")

# Confidence interval for conditional mean
ci_mean_multi = pred_multi.conf_int(alpha=0.05)
print(f"95% CI for E[Y|X]: [{ci_mean_multi[0, 0]:.2f}, {ci_mean_multi[0, 1]:.2f}]")

# Prediction interval for actual value
s_e_multi = np.sqrt(model_multi.mse_resid)
s_y_cm_multi = pred_multi.se_mean[0]
s_y_f_multi = np.sqrt(s_e_multi**2 + s_y_cm_multi**2)

n_multi = len(data_house)
k_multi = len(model_multi.params)
tcrit_multi = stats.t.ppf(0.975, n_multi - k_multi)

pi_lower = pred_multi.predicted_mean[0] - tcrit_multi * s_y_f_multi
pi_upper = pred_multi.predicted_mean[0] + tcrit_multi * s_y_f_multi

print(f"SE for actual value: {s_y_f_multi:.6f}")
print(f"95% PI for Y: [{pi_lower:.2f}, {pi_upper:.2f}]")

# Repeat with robust standard errors
print("\n" + "-" * 70)
print("Prediction with Heteroskedastic-Robust SEs")
print("-" * 70)

model_multi_robust = ols('price ~ size + bedrooms + bathrooms + lotsize + age + monthsold',
                         data=data_house).fit(cov_type='HC1')

pred_multi_robust = model_multi_robust.get_prediction(sm.add_constant(new_house))

print(f"\nPredicted price: {pred_multi_robust.predicted_mean[0]:.2f}")
print(f"Robust SE for conditional mean: {pred_multi_robust.se_mean[0]:.6f}")

# Robust confidence interval for conditional mean
ci_mean_robust = pred_multi_robust.conf_int(alpha=0.05)
print(f"Robust 95% CI for E[Y|X]: [{ci_mean_robust[0, 0]:.2f}, {ci_mean_robust[0, 1]:.2f}]")

# Robust prediction interval for actual value
s_y_cm_robust = pred_multi_robust.se_mean[0]
s_y_f_robust = np.sqrt(s_e_multi**2 + s_y_cm_robust**2)
print(f"Robust SE for actual value: {s_y_f_robust:.6f}")

# ========== 12.3-12.7 CONCEPTUAL SECTIONS ==========

print("\n" + "=" * 70)
print("12.3 NONREPRESENTATIVE SAMPLES")
print("=" * 70)
print("\nConceptual section - no computation required")
print("Key points:")
print("  - Sample selection can lead to biased estimates")
print("  - Important to have representative samples")
print("  - Selection bias can be addressed with appropriate methods")

print("\n" + "=" * 70)
print("12.4 BEST ESTIMATION")
print("=" * 70)
print("\nConceptual section - no computation required")
print("Key points:")
print("  - OLS is BLUE under Gauss-Markov assumptions")
print("  - GLS can be more efficient with heteroskedasticity")
print("  - Maximum likelihood estimation for parametric models")

print("\n" + "=" * 70)
print("12.5 BEST CONFIDENCE INTERVALS")
print("=" * 70)
print("\nConceptual section - no computation required")
print("Key points:")
print("  - Asymptotic confidence intervals")
print("  - Bootstrap confidence intervals")
print("  - Bayesian credible intervals")

print("\n" + "=" * 70)
print("12.6 BEST TESTS")
print("=" * 70)
print("\nConceptual section - no computation required")
print("Key points:")
print("  - Wald, LR, and LM tests")
print("  - Power of tests")
print("  - Multiple testing adjustments")

print("\n" + "=" * 70)
print("12.7 DATA SCIENCE AND BIG DATA: AN OVERVIEW")
print("=" * 70)
print("\nConceptual section - no computation required")
print("Key points:")
print("  - Machine learning vs econometrics")
print("  - Prediction vs causal inference")
print("  - Cross-validation and regularization")

# ========== 12.8 BAYESIAN METHODS: AN OVERVIEW ==========

print("\n" + "=" * 70)
print("12.8 BAYESIAN METHODS: AN OVERVIEW")
print("=" * 70)
print("\nNote: Full Bayesian estimation requires specialized packages like PyMC3 or Stan")
print("The Stata code uses Bayesian regression with different priors")
print("\nKey concepts:")
print("  - Prior distribution × Likelihood → Posterior distribution")
print("  - Uninformative priors: let data dominate")
print("  - Informative priors: incorporate prior knowledge")
print("  - Choice of prior can affect results, especially with small samples")

# Simple demonstration of the scale sensitivity
data_house['pricenew'] = data_house['price'] / 1000

model_original = ols('price ~ size', data=data_house).fit()
model_scaled = ols('pricenew ~ size', data=data_house).fit()

print("\nEffect of scaling dependent variable:")
print(f"\nOriginal scale (price in $1000):")
print(f"  Intercept: {model_original.params['Intercept']:.6f}")
print(f"  Slope: {model_original.params['size']:.6f}")

print(f"\nRescaled (price in $1,000,000):")
print(f"  Intercept: {model_scaled.params['Intercept']:.6f}")
print(f"  Slope: {model_scaled.params['size']:.6f}")

print("\nNote: In Bayesian analysis with improper priors, scale matters!")
print("With proper priors or large samples, Bayesian and frequentist results converge")

# ========== 12.9 HISTORY ==========

print("\n" + "=" * 70)
print("12.9 A BRIEF HISTORY OF STATISTICS, REGRESSION AND ECONOMETRICS")
print("=" * 70)
print("\nConceptual section - no computation required")
print("Key milestones:")
print("  - 1800s: Least squares (Gauss, Legendre)")
print("  - Early 1900s: Correlation and regression (Galton, Pearson)")
print("  - 1920s-1940s: Statistical inference (Fisher, Neyman, Pearson)")
print("  - 1940s-1960s: Econometrics foundations (Haavelmo, Cowles Commission)")
print("  - 1970s-1980s: Robust methods, time series")
print("  - 1990s-present: Panel data, causal inference, machine learning")

# ========== SUMMARY ==========

print("\n" + "=" * 70)
print("CHAPTER 12 SUMMARY")
print("=" * 70)
print("\nKey topics covered:")
print("  1. Heteroskedastic-robust standard errors (HC1)")
print("  2. HAC (Newey-West) standard errors for time series")
print("  3. Prediction intervals vs confidence intervals")
print("  4. Manual calculation of prediction standard errors")
print("  5. Prediction in multiple regression")
print("  6. Conceptual overview of advanced topics")
print("\nAll figures saved to:", IMAGES_DIR)

print("\n" + "=" * 70)
print("END OF CHAPTER 12")
print("=" * 70)
