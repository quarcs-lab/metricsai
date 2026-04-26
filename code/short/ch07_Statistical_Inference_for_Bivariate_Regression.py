# =============================================================================
# CHAPTER 7 CHEAT SHEET: Statistical Inference for Bivariate Regression
# =============================================================================

# --- Libraries ---
import pandas as pd                       # data loading and manipulation
import matplotlib.pyplot as plt           # creating plots and visualizations
import pyfixest as pf                     # OLS regression with R-style formulas
# !pip install pyfixest  # if not installed
from scipy import stats                   # t-distribution and critical values

# =============================================================================
# STEP 1: Load data directly from a URL
# =============================================================================
# pd.read_stata() reads Stata .dta files — the house price dataset has 29 houses
url = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_HOUSE.DTA"
data_house = pd.read_stata(url)

print(f"Dataset: {data_house.shape[0]} observations, {data_house.shape[1]} variables")

# =============================================================================
# STEP 2: Estimate the regression and extract key statistics
# =============================================================================
# The t-statistic measures how many standard errors the estimate is from zero
fit = pf.feols('price ~ size', data=data_house)

slope     = fit.coef()['size']         # marginal effect: $/sq ft
intercept = fit.coef()['Intercept']
se_slope  = fit.se()['size']           # standard error of the slope
t_stat    = fit.tstat()['size']        # t = b2 / se(b2)
p_value   = fit.pval()['size']         # two-sided p-value for H0: b2 = 0

print(f"Estimated equation: price = {intercept:,.0f} + {slope:.2f} × size")
print(f"Standard error of slope: {se_slope:.2f}")
print(f"t-statistic: {t_stat:.4f}")
print(f"p-value: {p_value:.6f}")

# Full regression table (coefficients, std errors, t-stats, p-values, R²)
fit.summary()

# =============================================================================
# STEP 3: Confidence interval — a range of plausible values for β₂
# =============================================================================
# CI = b2 ± t_crit × se(b2), using T(n-2) distribution
n  = len(data_house)
df = n - 2                                        # degrees of freedom
t_crit = stats.t.ppf(0.975, df)                   # critical value for 95% CI

ci_lower = slope - t_crit * se_slope
ci_upper = slope + t_crit * se_slope

print(f"Degrees of freedom: {df}")
print(f"Critical t-value (α=0.05, two-sided): {t_crit:.4f}")
print(f"95% CI for slope: [{ci_lower:.2f}, {ci_upper:.2f}]")
print(f"Interpretation: each sq ft adds between ${ci_lower:.0f} and ${ci_upper:.0f} to price")

# =============================================================================
# STEP 4: Hypothesis tests — does size matter? Is the effect $90/sq ft?
# =============================================================================
# Test 1: Statistical significance (H0: β₂ = 0)
print(f"Test H₀: β₂ = 0  →  t = {t_stat:.2f}, p = {p_value:.6f}  →  Reject H₀")

# Test 2: Two-sided test for a specific value (H0: β₂ = 90)
null_value = 90
t_90 = (slope - null_value) / se_slope
p_90 = 2 * (1 - stats.t.cdf(abs(t_90), df))

print(f"Test H₀: β₂ = 90  →  t = {t_90:.4f}, p = {p_90:.4f}  →  Fail to reject H₀")
print(f"  (90 is inside the 95% CI [{ci_lower:.2f}, {ci_upper:.2f}])")

# =============================================================================
# STEP 5: One-sided test — does size increase price by less than $90/sq ft?
# =============================================================================
# H0: β₂ ≥ 90  vs  Ha: β₂ < 90 (lower-tailed test)
p_lower = stats.t.cdf(t_90, df)                   # one-sided p-value (left tail)

print(f"One-sided test H₀: β₂ ≥ 90 vs Hₐ: β₂ < 90")
print(f"  t = {t_90:.4f}, one-sided p = {p_lower:.4f}")
print(f"  Fail to reject at 5% (p = {p_lower:.3f} > 0.05)")
print(f"  Would reject at 10% (p = {p_lower:.3f} < 0.10)")

# =============================================================================
# STEP 6: Robust standard errors — valid with or without heteroskedasticity
# =============================================================================
# HC1 robust SEs protect against non-constant variance in the errors
fit_robust = pf.feols('price ~ size', data=data_house, vcov='HC1')

print(f"{'':20s} {'Standard':>12s} {'Robust (HC1)':>12s}")
print("-" * 46)
print(f"{'SE(size)':<20s} {se_slope:>12.2f} {fit_robust.se()['size']:>12.2f}")
print(f"{'t-statistic':<20s} {t_stat:>12.2f} {fit_robust.tstat()['size']:>12.2f}")
print(f"{'p-value':<20s} {p_value:>12.6f} {fit_robust.pval()['size']:>12.6f}")

pct_change = ((fit_robust.se()['size'] - se_slope) / se_slope) * 100
print(f"\nRobust SE is {pct_change:+.1f}% different from standard SE")

# =============================================================================
# STEP 7: Scatter plot with regression line and inference summary
# =============================================================================
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(data_house['size'], data_house['price'], s=50, alpha=0.7, label='Actual prices')
ax.plot(data_house['size'], fit.predict(), color='red', linewidth=2, label='Fitted line')
ax.set_xlabel('House Size (square feet)')
ax.set_ylabel('House Sale Price (dollars)')
ax.set_title(f'price = {intercept:,.0f} + {slope:.2f} × size    '
             f'95% CI for slope: [{ci_lower:.0f}, {ci_upper:.0f}]')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
