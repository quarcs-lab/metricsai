# =============================================================================
# CHAPTER 11 CHEAT SHEET: Statistical Inference for Multiple Regression
# =============================================================================

# --- Libraries ---
import numpy as np                              # numerical operations
import pandas as pd                             # data loading and manipulation
import matplotlib.pyplot as plt                 # creating plots and visualizations
import pyfixest as pf                           # OLS regression with R-style formulas
# !pip install pyfixest  # if not installed
from scipy import stats                         # t and F distributions for inference
from statsmodels.formula.api import ols as sm_ols  # for ANOVA model comparison
from statsmodels.stats.anova import anova_lm    # ANOVA table for model comparison

# =============================================================================
# STEP 1: Load data directly from a URL
# =============================================================================
# pd.read_stata() reads Stata .dta files; the dataset has 29 houses from Davis, CA
url = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_HOUSE.DTA"
data_house = pd.read_stata(url)

print(f"Dataset: {data_house.shape[0]} observations, {data_house.shape[1]} variables")
print(data_house[['price', 'size', 'bedrooms', 'bathrooms', 'lotsize', 'age']].describe().round(2))

# =============================================================================
# STEP 2: Estimate the full multiple regression model
# =============================================================================
# Formula syntax: 'y ~ x1 + x2 + ...' includes an intercept automatically
# pf.feols() estimates the model in one step (no separate .fit() needed)
fit_full = pf.feols('price ~ size + bedrooms + bathrooms + lotsize + age + monthsold',
                    data=data_house)

n = int(fit_full._N)
k = len(fit_full.coef())
df = n - k  # degrees of freedom for t and F tests

print(f"\nSize effect: ${fit_full.coef()['size']:,.2f} per sq ft (p = {fit_full.pval()['size']:.4f})")
print(f"R-squared: {fit_full._r2:.4f} ({fit_full._r2*100:.1f}% of variation explained)")
print(f"Degrees of freedom: n-k = {n}-{k} = {df}")

# Full regression table (coefficients, std errors, t-stats, p-values, R²)
fit_full.summary()

# =============================================================================
# STEP 3: Confidence intervals — does the CI exclude zero?
# =============================================================================
# 95% CI: b_j ± t_critical × se(b_j)
# If the interval excludes zero, the coefficient is statistically significant at 5%
conf_int = fit_full.confint()
print("\n95% Confidence Intervals:")
print(conf_int.round(2))

# Manual calculation for the size coefficient
coef_size = fit_full.coef()['size']
se_size   = fit_full.se()['size']
t_crit    = stats.t.ppf(0.975, df)  # 0.975 = upper tail for two-sided 95% CI

ci_lower = coef_size - t_crit * se_size
ci_upper = coef_size + t_crit * se_size
print(f"\nSize 95% CI: [${ci_lower:.2f}, ${ci_upper:.2f}]  (excludes zero → significant)")

# =============================================================================
# STEP 4: Hypothesis test on a single coefficient
# =============================================================================
# Test H₀: β_size = 50 vs H₁: β_size ≠ 50
# t = (b_j - hypothesized value) / se(b_j)
null_value = 50
t_stat = (coef_size - null_value) / se_size
p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df))

print(f"\nTest H₀: β_size = {null_value}")
print(f"  t-statistic: {t_stat:.4f}")
print(f"  p-value: {p_value:.4f}")
print(f"  Decision: {'Reject' if p_value < 0.05 else 'Fail to reject'} H₀ at 5% level")

# Test of statistical significance: H₀: β_size = 0
t_stat_zero = coef_size / se_size
print(f"\nTest H₀: β_size = 0")
print(f"  t-statistic: {t_stat_zero:.4f}, p-value: {fit_full.pval()['size']:.6f}")
print(f"  Size IS statistically significant at 5% level")

# =============================================================================
# STEP 5: Joint F-test — are groups of coefficients jointly significant?
# =============================================================================
# Overall F-test: H₀: all slope coefficients = 0
# Use statsmodels for F-test functionality
sm_full = sm_ols('price ~ size + bedrooms + bathrooms + lotsize + age + monthsold',
                 data=data_house).fit()
print(f"\nOverall F-test: F = {sm_full.fvalue:.4f}, p = {sm_full.f_pvalue:.6e}")
print(f"  At least one variable matters → model is jointly significant")

# Subset F-test: are variables other than size jointly significant?
# H₀: β_bedrooms = β_bathrooms = β_lotsize = β_age = β_monthsold = 0
hypotheses = ['bedrooms = 0', 'bathrooms = 0', 'lotsize = 0',
              'age = 0', 'monthsold = 0']
f_test_result = sm_full.f_test(hypotheses)
print(f"\nSubset F-test (drop 5 vars, keep size):")
print(f"  F = {f_test_result.fvalue[0][0]:.4f}, p = {float(f_test_result.pvalue):.4f}")
print(f"  Extra variables are NOT jointly significant → simpler model preferred")

# =============================================================================
# STEP 6: Model comparison — restricted vs unrestricted
# =============================================================================
# Restricted model: only size as predictor
fit_restricted = pf.feols('price ~ size', data=data_house)
sm_restricted = sm_ols('price ~ size', data=data_house).fit()

# ANOVA table confirms the F-test result
anova_results = anova_lm(sm_restricted, sm_full)
print("\nANOVA: Restricted (size only) vs Full model:")
print(anova_results)

# Compare fit statistics
print(f"\n{'Model':<25} {'R²':>8} {'Adj. R²':>9}")
print("-" * 44)
for name, m in [('Size only', fit_restricted), ('Full model', fit_full)]:
    print(f"{name:<25} {m._r2:>8.4f} {m._adj_r2:>9.4f}")

# =============================================================================
# STEP 7: Robust standard errors — valid under heteroskedasticity
# =============================================================================
# HC1 (White's correction) provides valid inference without constant variance
fit_robust = pf.feols('price ~ size + bedrooms + bathrooms + lotsize + age + monthsold',
                      data=data_house, vcov='HC1')

print("\nStandard vs Robust SEs:")
print(f"{'Variable':<14} {'Coef':>10} {'Std SE':>10} {'Robust SE':>10} {'p (robust)':>10}")
print("-" * 56)
for var in fit_full.coef().index:
    print(f"{var:<14} {fit_full.coef()[var]:>10.2f} "
          f"{fit_full.se()[var]:>10.2f} {fit_robust.se()[var]:>10.2f} "
          f"{fit_robust.pval()[var]:>10.4f}")

# =============================================================================
# STEP 8: Coefficient plot — visual summary of significance
# =============================================================================
# Error bars crossing zero = not significant at 5%
params_plot = fit_full.coef()[1:]  # exclude intercept
ci_plot = conf_int.iloc[1:, :]

fig, ax = plt.subplots(figsize=(10, 6))
y_pos = np.arange(len(params_plot))
ax.errorbar(params_plot.values, y_pos,
            xerr=[params_plot.values - ci_plot.iloc[:, 0].values,
                  ci_plot.iloc[:, 1].values - params_plot.values],
            fmt='o', markersize=8, capsize=5, capthick=2, linewidth=2)
ax.axvline(x=0, color='red', linestyle='--', linewidth=1.5, alpha=0.7, label='H₀: β = 0')
ax.set_yticks(y_pos)
ax.set_yticklabels(params_plot.index)
ax.set_xlabel('Coefficient Value')
ax.set_title('Coefficient Estimates with 95% Confidence Intervals')
ax.legend()
ax.grid(True, alpha=0.3, axis='x')
plt.tight_layout()
plt.show()
