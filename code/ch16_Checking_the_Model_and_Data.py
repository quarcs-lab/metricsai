# =============================================================================
# CHAPTER 16 CHEAT SHEET: Checking the Model and Data
# =============================================================================

# --- Libraries ---
import numpy as np                                          # numerical operations
import pandas as pd                                         # data loading and manipulation
import matplotlib.pyplot as plt                             # creating plots and visualizations
from statsmodels.formula.api import ols                     # OLS regression with R-style formulas
import statsmodels.api as sm                                # add_constant for VIF calculation
from statsmodels.stats.outliers_influence import (          # diagnostic tools:
    variance_inflation_factor, OLSInfluence)                #   VIF and influence measures
from statsmodels.nonparametric.smoothers_lowess import lowess  # LOWESS smooth for residual plots

# =============================================================================
# STEP 1: Load data
# =============================================================================
# Two datasets: earnings (cross-section) and democracy (cross-country)
url_base = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/"

data_earnings  = pd.read_stata(url_base + "AED_EARNINGS_COMPLETE.DTA")
data_democracy = pd.read_stata(url_base + "AED_DEMOCRACY.DTA")

print(f"Earnings:  {data_earnings.shape[0]} workers, {data_earnings.shape[1]} variables")
print(f"Democracy: {data_democracy.shape[0]} countries, {data_democracy.shape[1]} variables")

# =============================================================================
# STEP 2: Detect multicollinearity with VIF
# =============================================================================
# VIF_j = 1/(1 - R_j^2): measures how much SE inflates due to collinearity
# VIF > 10 = serious problem; VIF > 5 = investigate further

X_vif = data_earnings[['age', 'education', 'agebyeduc']].copy()
X_vif = sm.add_constant(X_vif)

vif_data = pd.DataFrame({
    'Variable': X_vif.columns,
    'VIF': [variance_inflation_factor(X_vif.values, i) for i in range(X_vif.shape[1])]
})
print("\nVariance Inflation Factors (with interaction term):")
print(vif_data.to_string(index=False))

# =============================================================================
# STEP 3: Compare standard vs robust standard errors
# =============================================================================
# Heteroskedasticity makes default SEs too small -> use HC1 (White) robust SEs
model_std    = ols('earnings ~ age + education', data=data_earnings).fit()
model_robust = ols('earnings ~ age + education', data=data_earnings).fit(cov_type='HC1')

se_comparison = pd.DataFrame({
    'Variable':    model_std.params.index,
    'Standard SE': model_std.bse.values.round(2),
    'Robust SE':   model_robust.bse.values.round(2),
    'Ratio':       (model_robust.bse / model_std.bse).values.round(3)
})
print("\nSE Comparison (ratio > 1 signals heteroskedasticity):")
print(se_comparison.to_string(index=False))

# =============================================================================
# STEP 4: Omitted variable bias — democracy and growth
# =============================================================================
# Adding controls reveals how much the bivariate estimate was biased upward
model_bivariate = ols('democracy ~ growth', data=data_democracy).fit(cov_type='HC1')
model_multiple  = ols('democracy ~ growth + constraint + indcent + catholic + muslim + protestant',
                      data=data_democracy).fit(cov_type='HC1')

b_biv  = model_bivariate.params['growth']
b_mult = model_multiple.params['growth']
print(f"\nGrowth coefficient (bivariate):       {b_biv:.4f}")
print(f"Growth coefficient (with controls):   {b_mult:.4f}")
print(f"Reduction: {(1 - b_mult/b_biv)*100:.0f}% — institutional controls absorb the bias")

# =============================================================================
# STEP 5: Diagnostic plots — residual vs fitted
# =============================================================================
# Random scatter around zero = assumptions OK; fan shape = heteroskedasticity
uhat = model_multiple.resid
yhat = model_multiple.fittedvalues

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Panel A: Actual vs Fitted
axes[0].scatter(yhat, data_democracy['democracy'], s=50, alpha=0.6)
axes[0].plot([yhat.min(), yhat.max()], [yhat.min(), yhat.max()],
             'r-', linewidth=2, label='45° line')
axes[0].set_xlabel('Fitted Democracy')
axes[0].set_ylabel('Actual Democracy')
axes[0].set_title('Actual vs Fitted')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Panel B: Residual vs Fitted (with LOWESS smooth)
axes[1].scatter(yhat, uhat, s=50, alpha=0.6)
axes[1].axhline(y=0, color='gray', linewidth=1)
lw = lowess(uhat, yhat, frac=0.3)          # LOWESS reveals hidden patterns
axes[1].plot(lw[:, 0], lw[:, 1], 'r--', linewidth=2, label='LOWESS smooth')
axes[1].set_xlabel('Fitted Democracy')
axes[1].set_ylabel('Residual')
axes[1].set_title('Residual vs Fitted')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# =============================================================================
# STEP 6: Influential observations — DFITS
# =============================================================================
# DFITS_i measures how much prediction i changes when observation i is excluded
# Threshold: |DFITS| > 2*sqrt(k/n)
influence = OLSInfluence(model_multiple)
dfits     = influence.dffits[0]
n = len(data_democracy)
k = len(model_multiple.params)
threshold = 2 * np.sqrt(k / n)

print(f"\nDFITS threshold: {threshold:.4f}")
print(f"Observations exceeding threshold: {np.sum(np.abs(dfits) > threshold)} out of {n}")

fig, ax = plt.subplots(figsize=(10, 6))
colors = ['red' if abs(d) > threshold else 'steelblue' for d in dfits]
ax.scatter(range(n), dfits, c=colors, s=40, alpha=0.7)
ax.axhline(y=threshold,  color='red', linestyle='--', label=f'Threshold ±{threshold:.3f}')
ax.axhline(y=-threshold, color='red', linestyle='--')
ax.axhline(y=0, color='gray', linewidth=0.5)
ax.set_xlabel('Observation Index')
ax.set_ylabel('DFITS')
ax.set_title('Influential Observations (DFITS)')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
