"""
ch09_Models_with_Natural_Logarithms.py - January 2026 for Python

Chapter 9: MODELS WITH NATURAL LOGARITHMS

To run you need files:
  AED_EARNINGS.DTA
  AED_SP500INDEX.DTA
in the data/ directory

Sections covered:
  9.1 NATURAL LOGARITHM FUNCTION
  9.2 SEMI-ELASTICITIES AND ELASTICITIES
  9.3 LOG-LINEAR, LOG-LOG AND LINEAR-LOG MODELS
  9.4 EXAMPLE: EARNINGS AND EDUCATION
  9.5 FURTHER USES OF THE NATURAL LOGARITHM
  9.6 EXPONENTIAL FUNCTION
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
print("CHAPTER 9: MODELS WITH NATURAL LOGARITHMS")
print("=" * 70)

# ========== 9.1 NATURAL LOGARITHM FUNCTION ==========

print("\n" + "=" * 70)
print("9.1 NATURAL LOGARITHM FUNCTION")
print("=" * 70)

# Table 9.1 - Demonstration of logarithm properties
print("\n" + "-" * 70)
print("Table 9.1: Properties of Natural Logarithm")
print("-" * 70)

x_values = np.array([0.5, 1, 2, 5, 10, 20, 100])
ln_values = np.log(x_values)

log_table = pd.DataFrame({
    'x': x_values,
    'ln(x)': ln_values,
    'exp(ln(x))': np.exp(ln_values)
})
print(log_table)

print("\nKey properties:")
print(f"  ln(1) = {np.log(1):.4f}")
print(f"  ln(e) = {np.log(np.e):.4f}")
print(f"  ln(2*5) = ln(2) + ln(5): {np.log(2*5):.4f} = {np.log(2) + np.log(5):.4f}")
print(f"  ln(10/2) = ln(10) - ln(2): {np.log(10/2):.4f} = {np.log(10) - np.log(2):.4f}")

# ========== 9.2 SEMI-ELASTICITIES AND ELASTICITIES ==========

print("\n" + "=" * 70)
print("9.2 SEMI-ELASTICITIES AND ELASTICITIES")
print("=" * 70)

print("\nModel interpretations:")
print("  Linear model: y = β₀ + β₁x")
print("    Interpretation: Δy = β₁Δx")
print("\n  Log-linear model: ln(y) = β₀ + β₁x")
print("    Interpretation: %Δy ≈ 100β₁Δx (semi-elasticity)")
print("\n  Log-log model: ln(y) = β₀ + β₁ln(x)")
print("    Interpretation: %Δy ≈ β₁%Δx (elasticity)")
print("\n  Linear-log model: y = β₀ + β₁ln(x)")
print("    Interpretation: Δy ≈ β₁(%Δx/100)")

# ========== 9.3 LOG-LINEAR, LOG-LOG AND LINEAR-LOG MODELS ==========

print("\n" + "=" * 70)
print("9.3 LOG-LINEAR, LOG-LOG AND LINEAR-LOG MODELS")
print("=" * 70)

# This section demonstrates the different model specifications
# Detailed examples follow in section 9.4

# ========== 9.4 EXAMPLE: EARNINGS AND EDUCATION ==========

print("\n" + "=" * 70)
print("9.4 EXAMPLE: EARNINGS AND EDUCATION")
print("=" * 70)

# Read in the earnings data
data_earnings = pd.read_stata(GITHUB_DATA_URL + 'AED_EARNINGS.DTA')

print("\nData summary:")
data_summary = data_earnings.describe()
print(data_summary)
print("\nFirst few observations:")
print(data_earnings.head())
data_summary.to_csv(os.path.join(TABLES_DIR, 'ch09_earnings_descriptive_stats.csv'))
print(f"Table saved to: {os.path.join(TABLES_DIR, 'ch09_earnings_descriptive_stats.csv')}")

# Create log variables
data_earnings['lnearn'] = np.log(data_earnings['earnings'])
data_earnings['lneduc'] = np.log(data_earnings['education'])

# Table 9.2
print("\n" + "-" * 70)
print("Table 9.2: Earnings and Education Variables")
print("-" * 70)
table92_vars = ['earnings', 'lnearn', 'education', 'lneduc']
print(data_earnings[table92_vars].describe())

# Table 9.3 - Four different model specifications
print("\n" + "=" * 70)
print("Table 9.3: Four Model Specifications")
print("=" * 70)

# Model 1: Linear model
print("\n" + "-" * 70)
print("Model 1: Linear - earnings = β₀ + β₁(education)")
print("-" * 70)
model_linear = ols('earnings ~ education', data=data_earnings).fit()
print(model_linear.summary())
print(f"\nInterpretation: One additional year of education is associated with")
print(f"${model_linear.params['education']:.2f} increase in annual earnings")

# Model 2: Log-linear model
print("\n" + "-" * 70)
print("Model 2: Log-linear - ln(earnings) = β₀ + β₁(education)")
print("-" * 70)
model_loglin = ols('lnearn ~ education', data=data_earnings).fit()
print(model_loglin.summary())
print(f"\nInterpretation: One additional year of education is associated with")
print(f"{100*model_loglin.params['education']:.2f}% increase in earnings")

# Model 3: Log-log model
print("\n" + "-" * 70)
print("Model 3: Log-log - ln(earnings) = β₀ + β₁ln(education)")
print("-" * 70)
model_loglog = ols('lnearn ~ lneduc', data=data_earnings).fit()
print(model_loglog.summary())
print(f"\nInterpretation: A 1% increase in education is associated with")
print(f"{model_loglog.params['lneduc']:.4f}% increase in earnings (elasticity)")

# Model 4: Linear-log model
print("\n" + "-" * 70)
print("Model 4: Linear-log - earnings = β₀ + β₁ln(education)")
print("-" * 70)
model_linlog = ols('earnings ~ lneduc', data=data_earnings).fit()
print(model_linlog.summary())
print(f"\nInterpretation: A 1% increase in education is associated with")
print(f"${model_linlog.params['lneduc']/100:.2f} increase in annual earnings")

# Comparison table
print("\n" + "-" * 70)
print("Model Comparison Summary")
print("-" * 70)
comparison_df = pd.DataFrame({
    'Model': ['Linear', 'Log-linear', 'Log-log', 'Linear-log'],
    'Specification': ['y ~ x', 'ln(y) ~ x', 'ln(y) ~ ln(x)', 'y ~ ln(x)'],
    'R²': [model_linear.rsquared, model_loglin.rsquared,
           model_loglog.rsquared, model_linlog.rsquared],
    'Slope Coef': [model_linear.params[1], model_loglin.params[1],
                   model_loglog.params[1], model_linlog.params[1]]
})
print(comparison_df.to_string(index=False))
comparison_df.to_csv(os.path.join(TABLES_DIR, 'ch09_model_comparison.csv'), index=False)
print(f"Table saved to: {os.path.join(TABLES_DIR, 'ch09_model_comparison.csv')}")

# Figure 9.1 - Panel A: Linear Model
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(data_earnings['education'], data_earnings['earnings'], alpha=0.5, s=30,
           color='black', label='Actual')
ax.plot(data_earnings['education'], model_linear.fittedvalues, color='blue',
        linewidth=2, label='Fitted')
ax.set_xlabel('Years of completed schooling', fontsize=12)
ax.set_ylabel('Annual earnings (in dollars)', fontsize=12)
ax.set_title('Figure 9.1 Panel A: Linear Model',
             fontsize=14, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)

output_file = os.path.join(IMAGES_DIR, 'ch09_fig1a_linear_model.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\nFigure saved to: {output_file}")
plt.close()

# Figure 9.1 - Panel B: Log-linear Model
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(data_earnings['education'], data_earnings['lnearn'], alpha=0.5, s=30,
           color='black', label='Actual')
ax.plot(data_earnings['education'], model_loglin.fittedvalues, color='blue',
        linewidth=2, label='Fitted')
ax.set_xlabel('Years of completed schooling', fontsize=12)
ax.set_ylabel('Log annual earnings', fontsize=12)
ax.set_title('Figure 9.1 Panel B: Log-linear Model',
             fontsize=14, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)

output_file = os.path.join(IMAGES_DIR, 'ch09_fig1b_loglinear_model.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"Figure saved to: {output_file}")
plt.close()

# Combined figure showing all four models
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Linear model
axes[0, 0].scatter(data_earnings['education'], data_earnings['earnings'],
                   alpha=0.5, s=20, color='black')
axes[0, 0].plot(data_earnings['education'], model_linear.fittedvalues,
                color='blue', linewidth=2)
axes[0, 0].set_xlabel('Education (years)', fontsize=11)
axes[0, 0].set_ylabel('Earnings ($)', fontsize=11)
axes[0, 0].set_title('Linear Model: y = β₀ + β₁x', fontsize=12, fontweight='bold')
axes[0, 0].grid(True, alpha=0.3)

# Log-linear model
axes[0, 1].scatter(data_earnings['education'], data_earnings['lnearn'],
                   alpha=0.5, s=20, color='black')
axes[0, 1].plot(data_earnings['education'], model_loglin.fittedvalues,
                color='blue', linewidth=2)
axes[0, 1].set_xlabel('Education (years)', fontsize=11)
axes[0, 1].set_ylabel('ln(Earnings)', fontsize=11)
axes[0, 1].set_title('Log-linear Model: ln(y) = β₀ + β₁x', fontsize=12, fontweight='bold')
axes[0, 1].grid(True, alpha=0.3)

# Log-log model
axes[1, 0].scatter(data_earnings['lneduc'], data_earnings['lnearn'],
                   alpha=0.5, s=20, color='black')
axes[1, 0].plot(data_earnings['lneduc'], model_loglog.fittedvalues,
                color='blue', linewidth=2)
axes[1, 0].set_xlabel('ln(Education)', fontsize=11)
axes[1, 0].set_ylabel('ln(Earnings)', fontsize=11)
axes[1, 0].set_title('Log-log Model: ln(y) = β₀ + β₁ln(x)', fontsize=12, fontweight='bold')
axes[1, 0].grid(True, alpha=0.3)

# Linear-log model
axes[1, 1].scatter(data_earnings['lneduc'], data_earnings['earnings'],
                   alpha=0.5, s=20, color='black')
axes[1, 1].plot(data_earnings['lneduc'], model_linlog.fittedvalues,
                color='blue', linewidth=2)
axes[1, 1].set_xlabel('ln(Education)', fontsize=11)
axes[1, 1].set_ylabel('Earnings ($)', fontsize=11)
axes[1, 1].set_title('Linear-log Model: y = β₀ + β₁ln(x)', fontsize=12, fontweight='bold')
axes[1, 1].grid(True, alpha=0.3)

plt.suptitle('Four Model Specifications: Earnings and Education',
             fontsize=14, fontweight='bold', y=1.00)
output_file = os.path.join(IMAGES_DIR, 'ch09_four_models_comparison.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"Figure saved to: {output_file}")
plt.close()

# ========== 9.5 FURTHER USES OF THE NATURAL LOGARITHM ==========

print("\n" + "=" * 70)
print("9.5 FURTHER USES OF THE NATURAL LOGARITHM")
print("=" * 70)

# Read in the S&P 500 data
data_sp500 = pd.read_stata(GITHUB_DATA_URL + 'AED_SP500INDEX.DTA')

print("\nS&P 500 Index data summary:")
print(data_sp500.describe())
print("\nFirst few observations:")
print(data_sp500.head())

# Regression in logs to estimate exponential growth
print("\n" + "-" * 70)
print("Exponential Growth Model: ln(sp500) = β₀ + β₁(year)")
print("-" * 70)

model_logs = ols('lnsp500 ~ year', data=data_sp500).fit()
print(model_logs.summary())

print(f"\nInterpretation:")
print(f"  Growth rate: {100*model_logs.params['year']:.4f}% per year")

# Predictions
plnsp500 = model_logs.fittedvalues

# Retransformation bias correction
# Need MSE = ResSS/(n-k)
n = len(data_sp500)
k = 2  # intercept + slope
ResSSQ = np.sum(model_logs.resid**2)
MSE = ResSSQ / (n - k)
rmse = np.sqrt(MSE)

print(f"\nRetransformation bias correction:")
print(f"  RMSE: {rmse:.6f}")
print(f"  MSE: {MSE:.6f}")
print(f"  Correction factor: exp(MSE/2) = {np.exp(MSE/2):.6f}")

# Predictions in levels with bias correction
psp500 = np.exp(plnsp500) * np.exp(MSE/2)

# Figure 9.2 - Panel A: Exponential trend in levels
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(data_sp500['year'], data_sp500['sp500'], linewidth=2,
        label='Actual', color='black')
ax.plot(data_sp500['year'], psp500, linewidth=2, linestyle='--',
        label='Fitted (with bias correction)', color='blue')
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('S&P 500 Index', fontsize=12)
ax.set_title('Figure 9.2 Panel A: Exponential Trend in Levels',
             fontsize=14, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)

output_file = os.path.join(IMAGES_DIR, 'ch09_fig2a_sp500_levels.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\nFigure saved to: {output_file}")
plt.close()

# Figure 9.2 - Panel B: Linear trend in natural logarithms
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(data_sp500['year'], data_sp500['lnsp500'], linewidth=2,
        label='Actual', color='black')
ax.plot(data_sp500['year'], plnsp500, linewidth=2, linestyle='--',
        label='Fitted', color='blue')
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('ln(S&P 500 Index)', fontsize=12)
ax.set_title('Figure 9.2 Panel B: Linear Trend in Natural Logarithms',
             fontsize=14, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)

output_file = os.path.join(IMAGES_DIR, 'ch09_fig2b_sp500_logs.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"Figure saved to: {output_file}")
plt.close()

# ========== 9.6 EXPONENTIAL FUNCTION ==========

print("\n" + "=" * 70)
print("9.6 EXPONENTIAL FUNCTION")
print("=" * 70)

print("\nProperties of the exponential function:")
print(f"  exp(0) = {np.exp(0):.4f}")
print(f"  exp(1) = e = {np.exp(1):.4f}")
print(f"  exp(ln(5)) = {np.exp(np.log(5)):.4f}")
print(f"  exp(2) * exp(3) = exp(5): {np.exp(2)*np.exp(3):.4f} = {np.exp(5):.4f}")

# Demonstration of exponential growth
x_vals = np.linspace(0, 5, 100)
y_vals = np.exp(x_vals)

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(x_vals, y_vals, linewidth=2, color='blue')
ax.set_xlabel('x', fontsize=12)
ax.set_ylabel('exp(x)', fontsize=12)
ax.set_title('The Exponential Function: y = exp(x)',
             fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)

output_file = os.path.join(IMAGES_DIR, 'ch09_exponential_function.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\nFigure saved to: {output_file}")
plt.close()

# ========== SUMMARY ==========

print("\n" + "=" * 70)
print("CHAPTER 9 ANALYSIS COMPLETE")
print("=" * 70)
print("\nKey concepts demonstrated:")
print("  - Natural logarithm properties and transformations")
print("  - Semi-elasticities and elasticities")
print("  - Four model specifications: linear, log-linear, log-log, linear-log")
print("  - Interpretation of coefficients in log models")
print("  - Exponential growth estimation")
print("  - Retransformation bias correction")
print("\nAll figures saved to:", IMAGES_DIR)
