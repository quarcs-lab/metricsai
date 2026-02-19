# %%
"""
ch11_Statistical_Inference_for_Multiple_Regression.py - January 2026 for Python

Chapter 11: STATISTICAL INFERENCE FOR MULTIPLE REGRESSION

To run you need files:
  AED_HOUSE.DTA
in the data/ directory

Sections covered:
  11.1 PROPERTIES OF THE LEAST SQUARES ESTIMATOR
  11.2 ESTIMATORS OF MODEL PARAMETERS
  11.3 CONFIDENCE INTERVALS
  11.4 HYPOTHESIS TESTS ON A SINGLE PARAMETER
  11.5 JOINT HYPOTHESIS TESTS
  11.6 F STATISTIC UNDER ASSUMPTIONS 1-4
  11.7 PRESENTATION OF REGRESSION RESULTS
"""

# %% =========== SETUP ==========

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from statsmodels.formula.api import ols
from scipy import stats
from statsmodels.stats.anova import anova_lm
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
print("CHAPTER 11: STATISTICAL INFERENCE FOR MULTIPLE REGRESSION")
print("=" * 70)

# %% =========== DATA PREPARATION ==========

# Read in the house data
data_house = pd.read_stata(GITHUB_DATA_URL + 'AED_HOUSE.DTA')

# %% Explore data structure

print("\nData summary:")
data_summary = data_house.describe()

# %% Calculate statistics
print(data_summary)
data_summary.to_csv(os.path.join(TABLES_DIR, 'ch11_house_descriptive_stats.csv'))
print(f"Table saved to: {os.path.join(TABLES_DIR, 'ch11_house_descriptive_stats.csv')}")

# %% =========== 11.1 PROPERTIES OF THE LEAST SQUARES ESTIMATOR ==========

print("\n" + "=" * 70)
print("11.1 PROPERTIES OF THE LEAST SQUARES ESTIMATOR")
print("=" * 70)

print("\nUnder assumptions 1-4:")
print("  1. Linearity: y = β₀ + β₁x₁ + ... + βₖxₖ + u")
print("  2. Random sampling from population")
print("  3. No perfect collinearity")
print("  4. Zero conditional mean: E[u|X] = 0")
print("\nThe OLS estimator is:")
print("  - Unbiased: E[β̂] = β")
print("  - Consistent: plim(β̂) = β")
print("  - Efficient (BLUE under Gauss-Markov theorem)")

# %% =========== 11.2 ESTIMATORS OF MODEL PARAMETERS ==========

print("\n" + "=" * 70)
print("11.2 ESTIMATORS OF MODEL PARAMETERS")
print("=" * 70)

# Full multiple regression model

# %% Estimate regression model

model_full = ols('price ~ size + bedrooms + bathrooms + lotsize + age + monthsold',

# %% Estimate regression model

                 data=data_house).fit()

print("\n" + "-" * 70)
print("Table 11.2: Multiple Regression Results")
print("-" * 70)

# %% Display regression results

print(model_full.summary())
# Save regression summary
with open(os.path.join(TABLES_DIR, 'ch11_regression_summary.txt'), 'w') as f:
    f.write(model_full.summary().as_text())
# Save coefficients
coef_table = pd.DataFrame({
    'coefficient': model_full.params,
    'std_err': model_full.bse,
    't_value': model_full.tvalues,
    'p_value': model_full.pvalues
})
coef_table.to_csv(os.path.join(TABLES_DIR, 'ch11_regression_coefficients.csv'))
print(f"Coefficients saved to: {os.path.join(TABLES_DIR, 'ch11_regression_coefficients.csv')}")

# Extract key statistics
n = len(data_house)
k = len(model_full.params)
df = n - k

print(f"\nModel diagnostics:")
print(f"  Sample size: {n}")
print(f"  Number of parameters: {k}")
print(f"  Degrees of freedom: {df}")
print(f"  Root MSE (σ̂): {np.sqrt(model_full.mse_resid):.6f}")

# %% =========== 11.3 CONFIDENCE INTERVALS ==========

print("\n" + "=" * 70)
print("11.3 CONFIDENCE INTERVALS")
print("=" * 70)

# 95% confidence intervals
conf_int = model_full.conf_int(alpha=0.05)
print("\n95% Confidence Intervals:")
print(conf_int)

# Detailed confidence interval calculation for 'size'
coef_size = model_full.params['size']
se_size = model_full.bse['size']
t_crit = stats.t.ppf(0.975, df)

ci_lower = coef_size - t_crit * se_size
ci_upper = coef_size + t_crit * se_size

print(f"\nManual calculation for 'size' coefficient:")
print(f"  Coefficient: {coef_size:.6f}")
print(f"  Standard error: {se_size:.6f}")
print(f"  Degrees of freedom: {df}")
print(f"  Critical t-value (α=0.05): {t_crit:.4f}")
print(f"  95% CI: [{ci_lower:.6f}, {ci_upper:.6f}]")

# Create comprehensive coefficient table
print("\n" + "-" * 70)
print("Comprehensive Coefficient Table")
print("-" * 70)
coef_table = pd.DataFrame({
    'Coefficient': model_full.params,
    'Std. Error': model_full.bse,
    't-statistic': model_full.tvalues,
    'p-value': model_full.pvalues,
    'CI Lower': conf_int.iloc[:, 0],
    'CI Upper': conf_int.iloc[:, 1]
})
print(coef_table)

# %% =========== 11.4 HYPOTHESIS TESTS ON A SINGLE PARAMETER ==========

print("\n" + "=" * 70)
print("11.4 HYPOTHESIS TESTS ON A SINGLE PARAMETER")
print("=" * 70)

# Test H₀: β_size = 50 vs H₁: β_size ≠ 50
null_value = 50
t_stat_50 = (coef_size - null_value) / se_size
p_value_50 = 2 * (1 - stats.t.cdf(abs(t_stat_50), df))

print(f"\nTest: H₀: β_size = {null_value} vs H₁: β_size ≠ {null_value}")
print(f"  t-statistic: {t_stat_50:.4f}")
print(f"  p-value: {p_value_50:.6f}")
print(f"  Critical value (α=0.05): ±{t_crit:.4f}")

if abs(t_stat_50) > t_crit:
    print(f"Result: Reject H₀ at 5% significance level")
else:
    print(f"Result: Fail to reject H₀ at 5% significance level")

# Using statsmodels t_test
print("\n" + "-" * 70)
print("Hypothesis test using statsmodels:")
print("-" * 70)
hypothesis = f'size = {null_value}'
t_test_result = model_full.t_test(hypothesis)
print(t_test_result)

# %% =========== 11.5 JOINT HYPOTHESIS TESTS ==========

print("\n" + "=" * 70)
print("11.5 JOINT HYPOTHESIS TESTS")
print("=" * 70)

# Test 1: Joint significance of all slope coefficients
# H₀: β₁ = β₂ = ... = βₖ = 0
print("\n" + "-" * 70)
print("Test 1: Overall F-test (all slopes = 0)")
print("-" * 70)

f_stat = model_full.fvalue
f_pvalue = model_full.f_pvalue
dfn = k - 1  # numerator df (excluding intercept)
dfd = df     # denominator df
f_crit = stats.f.ppf(0.95, dfn, dfd)

print(f"  H₀: All slope coefficients equal zero")
print(f"  F-statistic: {f_stat:.4f}")
print(f"  p-value: {f_pvalue:.6e}")
print(f"  Critical value (α=0.05): {f_crit:.4f}")
print(f"  Numerator df: {dfn}, Denominator df: {dfd}")

if f_stat > f_crit:
    print("Result: Reject H₀ - At least one coefficient is non-zero")
else:
    print("Result: Fail to reject H₀")

# Test 2: Joint test of subset of coefficients
# H₀: β_bedrooms = β_bathrooms = β_lotsize = β_age = β_monthsold = 0
print("\n" + "-" * 70)
print("Test 2: Joint test of multiple coefficients")
print("-" * 70)

hypotheses = ['bedrooms = 0', 'bathrooms = 0', 'lotsize = 0',
              'age = 0', 'monthsold = 0']
f_test_result = model_full.f_test(hypotheses)
print(f_test_result)

print(f"\nInterpretation:")
print(f"  This tests whether bedrooms, bathrooms, lotsize, age, and monthsold")
print(f"  can jointly be excluded from the model (keeping only size)")

# %% =========== 11.6 F STATISTIC UNDER ASSUMPTIONS 1-4 ==========

print("\n" + "=" * 70)
print("11.6 F STATISTIC UNDER ASSUMPTIONS 1-4")
print("=" * 70)

# Manual calculation of F-statistic using sums of squares
print("\n" + "-" * 70)
print("Manual F-statistic calculation")
print("-" * 70)

# Calculate sum of squares
y = data_house['price']
y_mean = y.mean()
y_pred = model_full.fittedvalues
resid = model_full.resid

# Total sum of squares
TSS = np.sum((y - y_mean)**2)
# Explained sum of squares
ESS = np.sum((y_pred - y_mean)**2)
# Residual sum of squares
RSS = np.sum(resid**2)

print(f"Sum of Squares:")
print(f"  Total (TSS): {TSS:.4f}")
print(f"  Explained (ESS): {ESS:.4f}")
print(f"  Residual (RSS): {RSS:.4f}")
print(f"  Check: TSS = ESS + RSS: {np.isclose(TSS, ESS + RSS)}")

# F-statistic
f_stat_manual = (ESS / (k-1)) / (RSS / df)
print(f"\nF-statistic calculation:")
print(f"  F = (ESS/{k-1}) / (RSS/{df})")
print(f"  F = {f_stat_manual:.4f}")
print(f"  From model output: {f_stat:.4f}")
print(f"  Match: {np.isclose(f_stat_manual, f_stat)}")

# Subset F-test using restricted and unrestricted models
print("\n" + "-" * 70)
print("Subset F-test: Restricted vs Unrestricted Model")
print("-" * 70)

# Unrestricted model (already estimated as model_full)
# Restricted model (only size as regressor)

# %% Estimate regression model

model_restricted = ols('price ~ size', data=data_house).fit()

print("\nRestricted model (only size):")

# %% Display regression results

print(model_restricted.summary())

# Calculate F-statistic for subset test
k_unrest = len(model_full.params)
k_rest = len(model_restricted.params)
q = k_unrest - k_rest  # number of restrictions

RSS_unrest = np.sum(model_full.resid**2)
RSS_rest = np.sum(model_restricted.resid**2)
df_unrest = n - k_unrest

F_subset = ((RSS_rest - RSS_unrest) / q) / (RSS_unrest / df_unrest)
p_value_subset = 1 - stats.f.cdf(F_subset, q, df_unrest)
f_crit_subset = stats.f.ppf(0.95, q, df_unrest)

print(f"\nSubset F-test results:")
print(f"  Number of restrictions (q): {q}")
print(f"  RSS (restricted): {RSS_rest:.4f}")
print(f"  RSS (unrestricted): {RSS_unrest:.4f}")
print(f"  F-statistic: {F_subset:.4f}")
print(f"  p-value: {p_value_subset:.6f}")
print(f"  Critical value (α=0.05): {f_crit_subset:.4f}")

if F_subset > f_crit_subset:
    print("Result: Reject H₀ - The additional variables are jointly significant")
else:
    print("Result: Fail to reject H₀")

# Using ANOVA table for comparison
print("\n" + "-" * 70)
print("ANOVA table comparison")
print("-" * 70)
anova_results = anova_lm(model_restricted, model_full)
print(anova_results)

# %% =========== 11.7 PRESENTATION OF REGRESSION RESULTS ==========

print("\n" + "=" * 70)
print("11.7 PRESENTATION OF REGRESSION RESULTS")
print("=" * 70)

# Comparison of multiple models
print("\n" + "-" * 70)
print("Model Comparison: Three Specifications")
print("-" * 70)

# Model 1: Simple regression

# %% Estimate regression model

model1 = ols('price ~ size', data=data_house).fit()

# Model 2: Two regressors

# %% Estimate regression model

model2 = ols('price ~ size + bedrooms', data=data_house).fit()

# Model 3: Full model (already estimated as model_full)
model3 = model_full

# Create comparison table
models = [model1, model2, model3]
model_names = ['Model 1', 'Model 2', 'Model 3']

comparison_data = []
for name, model in zip(model_names, models):
    model_stats = {
        'Model': name,
        'N': int(model.nobs),
        'R²': f"{model.rsquared:.4f}",
        'Adj. R²': f"{model.rsquared_adj:.4f}",
        'RMSE': f"{np.sqrt(model.mse_resid):.4f}",
        'F-stat': f"{model.fvalue:.4f}",
        'p-value': f"{model.f_pvalue:.6f}"
    }
    comparison_data.append(model_stats)

comparison_df = pd.DataFrame(comparison_data)
print(comparison_df.to_string(index=False))

# Detailed coefficient comparison
print("\n" + "-" * 70)
print("Coefficient Comparison Across Models")
print("-" * 70)

# Get all unique parameter names
all_params = set()
for model in models:
    all_params.update(model.params.index)
all_params = sorted(all_params)

# Create coefficient table
coef_comparison = pd.DataFrame(index=all_params)
for i, (name, model) in enumerate(zip(model_names, models), 1):
    coef_col = f'{name} Coef'
    se_col = f'{name} SE'

    coef_comparison[coef_col] = model.params.reindex(all_params)
    coef_comparison[se_col] = model.bse.reindex(all_params)

print(coef_comparison.fillna('-'))

# %% =========== ROBUST STANDARD ERRORS ==========

print("\n" + "=" * 70)
print("ROBUST STANDARD ERRORS (HC1)")
print("=" * 70)

# Get robust results for full model
model_full_robust = model_full.get_robustcov_results(cov_type='HC1')

print("\nComparison of standard vs robust standard errors:")
robust_comparison = pd.DataFrame({
    'Coefficient': model_full.params,
    'Std. Error': model_full.bse,
    'Robust SE': model_full_robust.bse,
    't-stat (std)': model_full.tvalues,
    't-stat (robust)': model_full_robust.tvalues,
    'p-value (std)': model_full.pvalues,
    'p-value (robust)': model_full_robust.pvalues
})
print(robust_comparison)
robust_comparison.to_csv(os.path.join(TABLES_DIR, 'ch11_robust_vs_standard_se.csv'))
print(f"Table saved to: {os.path.join(TABLES_DIR, 'ch11_robust_vs_standard_se.csv')}")

# %% =========== VISUALIZATION ==========

print("\n" + "=" * 70)
print("GENERATING FIGURES")
print("=" * 70)

# Figure 11.1: Confidence intervals for all coefficients
fig, ax = plt.subplots(figsize=(10, 8))

params_no_int = model_full.params[1:]
ci_no_int = conf_int.iloc[1:, :]

y_pos = np.arange(len(params_no_int))
ax.errorbar(params_no_int.values, y_pos,
            xerr=[params_no_int.values - ci_no_int.iloc[:, 0].values,
                  ci_no_int.iloc[:, 1].values - params_no_int.values],
            fmt='o', markersize=8, capsize=5, capthick=2, linewidth=2, color='blue')
ax.set_yticks(y_pos)
ax.set_yticklabels(params_no_int.index)
ax.axvline(x=0, color='red', linestyle='--', linewidth=1.5, alpha=0.7,
           label='H₀: β = 0')
ax.set_xlabel('Coefficient Value', fontsize=12)
# ax.set_title('Figure 11.1: Coefficient Estimates with 95% Confidence Intervals',
#              fontsize=14, fontweight='bold')  # Removed: redundant with LaTeX caption
ax.legend()
ax.grid(True, alpha=0.3, axis='x')

output_file = os.path.join(IMAGES_DIR, 'ch11_fig1_confidence_intervals.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\nFigure saved to: {output_file}")
plt.close()

# %% Continue analysis

# Figure: F-distribution visualization
fig, ax = plt.subplots(figsize=(10, 6))

x_range = np.linspace(0, 10, 1000)
f_pdf = stats.f.pdf(x_range, dfn, dfd)

ax.plot(x_range, f_pdf, 'b-', linewidth=2, label=f'F({dfn}, {dfd}) distribution')
ax.axvline(x=f_stat, color='red', linewidth=2, linestyle='--',
           label=f'Observed F = {f_stat:.2f}')
ax.axvline(x=f_crit, color='green', linewidth=2, linestyle=':',
           label=f'Critical value = {f_crit:.2f}')

# Shade rejection region
x_reject = x_range[x_range >= f_crit]
f_reject = stats.f.pdf(x_reject, dfn, dfd)
ax.fill_between(x_reject, 0, f_reject, alpha=0.3, color='red',
                label='Rejection region (α=0.05)')

ax.set_xlabel('F-statistic', fontsize=12)
ax.set_ylabel('Density', fontsize=12)
# ax.set_title('F-Distribution for Overall Significance Test',
#              fontsize=14, fontweight='bold')  # Removed: redundant with LaTeX caption
ax.legend()
ax.grid(True, alpha=0.3)
ax.set_xlim(0, max(8, f_stat + 1))

output_file = os.path.join(IMAGES_DIR, 'ch11_f_distribution.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"Figure saved to: {output_file}")
plt.close()

# %% Continue analysis

# Figure: Model comparison visualization
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

for i, (model, name) in enumerate(zip(models, model_names)):
    axes[i].scatter(data_house['price'], model.fittedvalues,
                   alpha=0.6, s=50, color='black')
    axes[i].plot([data_house['price'].min(), data_house['price'].max()],
                [data_house['price'].min(), data_house['price'].max()],
                'r--', linewidth=2)
    axes[i].set_xlabel('Actual Price', fontsize=11)
    axes[i].set_ylabel('Predicted Price', fontsize=11)
    # axes[i].set_title(f'{name}\nR² = {model.rsquared:.4f}',
#                      fontsize=11, fontweight='bold')  # Removed: redundant with LaTeX caption
    axes[i].grid(True, alpha=0.3)

# plt.suptitle('Model Comparison: Actual vs Predicted Prices',
#              fontsize=14, fontweight='bold', y=1.00)  # Removed: redundant with LaTeX caption
output_file = os.path.join(IMAGES_DIR, 'ch11_model_comparison.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"Figure saved to: {output_file}")
plt.close()

# %% Continue analysis

# %% =========== SUMMARY ==========

print("\n" + "=" * 70)
print("CHAPTER 11 ANALYSIS COMPLETE")
print("=" * 70)
print("\nKey concepts demonstrated:")
print("  - Properties of OLS estimators in multiple regression")
print("  - Construction of confidence intervals for coefficients")
print("  - Individual hypothesis tests (t-tests)")
print("  - Joint hypothesis tests (F-tests)")
print("  - Overall significance test")
print("  - Subset F-tests for restricted vs unrestricted models")
print("  - Model comparison and presentation of results")
print("  - Heteroskedasticity-robust standard errors")
print("\nAll figures saved to:", IMAGES_DIR)
