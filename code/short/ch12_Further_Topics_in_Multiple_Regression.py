# =============================================================================
# CHAPTER 12 CHEAT SHEET: Further Topics in Multiple Regression
# =============================================================================

# --- Libraries ---
import pandas as pd                       # data loading and manipulation
import numpy as np                        # numerical operations
import matplotlib.pyplot as plt           # creating plots and visualizations
from statsmodels.formula.api import ols   # OLS regression with R-style formulas
import statsmodels.api as sm              # prediction tools (add_constant, get_prediction)
from scipy import stats                   # statistical distributions for CIs and power
from statsmodels.graphics.tsaplots import plot_acf  # autocorrelation plots

# =============================================================================
# STEP 1: Load house price data from a URL
# =============================================================================
# pd.read_stata() reads Stata .dta files directly from the web
url_house = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_HOUSE.DTA"
data_house = pd.read_stata(url_house)

print(f"Dataset: {data_house.shape[0]} observations, {data_house.shape[1]} variables")
print(data_house[['price', 'size', 'bedrooms', 'bathrooms', 'lotsize', 'age']].describe().round(2))

# =============================================================================
# STEP 2: OLS regression with default standard errors
# =============================================================================
# Default SEs assume homoskedasticity (constant error variance)
model_default = ols('price ~ size + bedrooms + bathrooms + lotsize + age + monthsold',
                    data=data_house).fit()

print(f"\nR-squared: {model_default.rsquared:.4f}")
print(f"Size effect (default): ${model_default.params['size']:,.2f} per sq ft")
model_default.summary()

# =============================================================================
# STEP 3: Robust (HC1) standard errors — compare with default
# =============================================================================
# HC1 SEs correct for heteroskedasticity without changing coefficient estimates
# Only the SEs, t-statistics, and confidence intervals change
model_robust = ols('price ~ size + bedrooms + bathrooms + lotsize + age + monthsold',
                   data=data_house).fit(cov_type='HC1')

# SE ratio: how much heteroskedasticity affects each coefficient's uncertainty
print(f"{'Variable':<14} {'Coef':>10} {'Default SE':>12} {'Robust SE':>12} {'Ratio':>8}")
print("-" * 58)
for var in model_default.params.index:
    coef  = model_default.params[var]
    se_d  = model_default.bse[var]
    se_r  = model_robust.bse[var]
    ratio = se_r / se_d                   # ratio > 1 → default was too optimistic
    print(f"{var:<14} {coef:>10.2f} {se_d:>12.2f} {se_r:>12.2f} {ratio:>8.3f}")

# =============================================================================
# STEP 4: Prediction — conditional mean CI vs. individual forecast PI
# =============================================================================
# Predicting E[y|x*] is more precise than predicting an individual y|x*
model_simple = ols('price ~ size', data=data_house).fit()

# Predict for a 2000 sq ft house
new_house = pd.DataFrame({'size': [2000]})
pred = model_simple.get_prediction(new_house)
pred_frame = pred.summary_frame(alpha=0.05)

s_e = np.sqrt(model_simple.mse_resid)    # RMSE — irreducible individual uncertainty

print(f"\nPredicted price (2000 sq ft): ${pred_frame['mean'].values[0]:,.0f}")
print(f"95% CI for E[Y|X=2000]: [${pred_frame['mean_ci_lower'].values[0]:,.0f}, "
      f"${pred_frame['mean_ci_upper'].values[0]:,.0f}]")
print(f"95% PI for individual Y:  [${pred_frame['obs_ci_lower'].values[0]:,.0f}, "
      f"${pred_frame['obs_ci_upper'].values[0]:,.0f}]")
print(f"\nRMSE (s_e): ${s_e:,.0f} — PI can never be narrower than ±1.96 × s_e")

# Visualize: CI (narrow) vs. PI (wide)
sizes_sorted = data_house[['size']].sort_values('size')
pred_all = model_simple.get_prediction(sizes_sorted)
pf = pred_all.summary_frame(alpha=0.05)

fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(data_house['size'], data_house['price'], s=50, alpha=0.6, label='Actual')
ax.plot(sizes_sorted['size'], pf['mean'], color='red', linewidth=2, label='Fitted line')
ax.fill_between(sizes_sorted['size'], pf['mean_ci_lower'], pf['mean_ci_upper'],
                color='red', alpha=0.2, label='95% CI (conditional mean)')
ax.fill_between(sizes_sorted['size'], pf['obs_ci_lower'], pf['obs_ci_upper'],
                color='blue', alpha=0.1, label='95% PI (individual)')
ax.set_xlabel('House Size (sq ft)')
ax.set_ylabel('House Price ($)')
ax.set_title('Confidence Interval vs. Prediction Interval')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# =============================================================================
# STEP 5: HAC (Newey-West) standard errors for time series
# =============================================================================
# Time series errors are often autocorrelated — HAC SEs account for this
url_gdp = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_REALGDPPC.DTA"
data_gdp = pd.read_stata(url_gdp)

mean_growth = data_gdp['growth'].mean()
n_gdp       = len(data_gdp)
lag_length   = int(0.75 * n_gdp**(1/3))  # rule of thumb: m = 0.75 × T^(1/3)

# Compare default SE vs. HAC SE for the mean
se_default = data_gdp['growth'].std() / np.sqrt(n_gdp)
y = data_gdp['growth']
X = np.ones(n_gdp)
from statsmodels.regression.linear_model import OLS
model_hac = OLS(y, X).fit(cov_type='HAC', cov_kwds={'maxlags': lag_length})

print(f"\nGDP Growth: mean = {mean_growth:.4f}")
print(f"Default SE (no autocorrelation): {se_default:.6f}")
print(f"HAC SE (lag = {lag_length}):            {model_hac.bse[0]:.6f}")
print(f"Ratio HAC/Default: {model_hac.bse[0] / se_default:.3f}")

# Correlogram — visualize autocorrelation structure
fig, ax = plt.subplots(figsize=(10, 6))
plot_acf(data_gdp['growth'], lags=10, ax=ax, alpha=0.05)
ax.set_xlabel('Lag')
ax.set_ylabel('Autocorrelation')
ax.set_title('Correlogram of GDP Growth')
plt.tight_layout()
plt.show()

# =============================================================================
# STEP 6: Power curve — Type I vs. Type II error tradeoff
# =============================================================================
# Power = P(reject H₀ | H₀ is false) — depends on true effect size
alpha = 0.05
se_test = 15                              # hypothetical standard error
n_test  = 30
t_crit  = stats.t.ppf(1 - alpha / 2, df=n_test - 1)

# Power as a function of the true coefficient
beta_range = np.linspace(-60, 60, 500)
power = []
for beta_true in beta_range:
    ncp = beta_true / se_test             # non-centrality parameter
    # Two-sided test: reject if |t| > t_crit
    power_val = 1 - (stats.t.cdf(t_crit - ncp, df=n_test - 1)
                      - stats.t.cdf(-t_crit - ncp, df=n_test - 1))
    power.append(power_val)

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(beta_range, power, linewidth=2)
ax.axhline(0.05, color='gray', linestyle='--', alpha=0.5, label='α = 0.05 (Type I)')
ax.axhline(0.80, color='green', linestyle='--', alpha=0.5, label='Power = 0.80 target')
ax.axvline(0, color='gray', linestyle='-', alpha=0.3, label='H₀: β = 0')
ax.set_xlabel('True Coefficient Value (β)')
ax.set_ylabel('Power = P(Reject H₀)')
ax.set_title('Power Curve: Larger Effects Are Easier to Detect')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# =============================================================================
# STEP 7: Bootstrap confidence intervals — no distributional assumptions
# =============================================================================
# Resample data with replacement to estimate the sampling distribution of β
np.random.seed(42)
n_boot = 1000
boot_slopes = []

for _ in range(n_boot):
    boot_sample = data_house.sample(n=len(data_house), replace=True)
    boot_model  = ols('price ~ size', data=boot_sample).fit()
    boot_slopes.append(boot_model.params['size'])

# Percentile method: 95% CI = [2.5th, 97.5th percentile]
ci_lower = np.percentile(boot_slopes, 2.5)
ci_upper = np.percentile(boot_slopes, 97.5)
ols_slope = model_simple.params['size']

print(f"\nOLS slope (size): {ols_slope:.4f}")
print(f"Bootstrap 95% CI: [{ci_lower:.4f}, {ci_upper:.4f}]")
print(f"Analytical 95% CI: [{model_simple.conf_int().loc['size'][0]:.4f}, "
      f"{model_simple.conf_int().loc['size'][1]:.4f}]")

fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(boot_slopes, bins=40, edgecolor='black', alpha=0.7)
ax.axvline(ols_slope, color='red', linewidth=2, label=f'OLS estimate: {ols_slope:.4f}')
ax.axvline(ci_lower, color='green', linewidth=2, linestyle='--', label=f'2.5th pctl: {ci_lower:.4f}')
ax.axvline(ci_upper, color='green', linewidth=2, linestyle='--', label=f'97.5th pctl: {ci_upper:.4f}')
ax.set_xlabel('Bootstrap Slope Estimates')
ax.set_ylabel('Frequency')
ax.set_title('Bootstrap Distribution of Size Coefficient (1000 replications)')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
