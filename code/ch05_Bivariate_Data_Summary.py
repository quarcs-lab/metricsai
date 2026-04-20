# =============================================================================
# CHAPTER 5 CHEAT SHEET: Bivariate Data Summary
# =============================================================================

# --- Libraries ---
import pandas as pd                                         # data loading and manipulation
import matplotlib.pyplot as plt                              # creating plots and visualizations
from statsmodels.formula.api import ols                      # OLS regression with R-style formulas
from statsmodels.nonparametric.smoothers_lowess import lowess  # LOWESS nonparametric smoothing

# =============================================================================
# STEP 1: Load data directly from a URL
# =============================================================================
# pd.read_stata() reads Stata .dta files — the dataset has 29 house sales
url = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_HOUSE.DTA"
data_house = pd.read_stata(url)

print(f"Dataset: {data_house.shape[0]} observations, {data_house.shape[1]} variables")

# =============================================================================
# STEP 2: Descriptive statistics — summarize each variable before comparing
# =============================================================================
# .describe() gives mean, std, min, quartiles, max for both variables
print(data_house[['price', 'size']].describe().round(2))

# =============================================================================
# STEP 3: Scatter plot — visualize the relationship before quantifying it
# =============================================================================
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(data_house['size'], data_house['price'], s=60, alpha=0.7)
ax.set_xlabel('House Size (square feet)')
ax.set_ylabel('House Sale Price (dollars)')
ax.set_title('House Price vs Size')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# =============================================================================
# STEP 4: Correlation coefficient — one number for direction and strength
# =============================================================================
# .corr() computes the Pearson correlation matrix; r is unit-free and symmetric
corr_matrix = data_house[['price', 'size']].corr()
r = corr_matrix.loc['price', 'size']

print(f"Correlation coefficient: r = {r:.4f}")
print(f"Strength: {'Strong' if abs(r) > 0.7 else 'Moderate' if abs(r) > 0.4 else 'Weak'}")
print(f"r² = {r**2:.4f} ({r**2*100:.1f}% of variation shared)")

# =============================================================================
# STEP 5: OLS regression — fit the best-fitting line
# =============================================================================
# Formula syntax: 'y ~ x' regresses y on x (intercept included automatically)
# IMPORTANT: .fit() estimates the model — without it, nothing is computed!
model = ols('price ~ size', data=data_house).fit()

slope     = model.params['size']        # marginal effect: $/sq ft
intercept = model.params['Intercept']   # predicted price when size = 0
r_squared = model.rsquared              # proportion of variation explained

print(f"Estimated equation: price = {intercept:,.0f} + {slope:.2f} × size")
print(f"Interpretation: each additional sq ft is associated with ${slope:,.2f} higher price")
print(f"R-squared: {r_squared:.4f} ({r_squared*100:.1f}% of variation explained)")

# Full regression table (coefficients, std errors, t-stats, p-values, R²)
model.summary()

# =============================================================================
# STEP 6: Scatter plot with fitted line and R² — visualize model fit
# =============================================================================
# model.fittedvalues contains the predicted y-values from the estimated equation
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(data_house['size'], data_house['price'], s=60, alpha=0.7, label='Actual prices')
ax.plot(data_house['size'], model.fittedvalues, color='red', linewidth=2, label='Fitted line')
ax.set_xlabel('House Size (square feet)')
ax.set_ylabel('House Sale Price (dollars)')
ax.set_title(f'OLS: price = {intercept:,.0f} + {slope:.2f} × size  (R² = {r_squared:.2%})')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# =============================================================================
# STEP 7: Reverse regression — association is NOT causation
# =============================================================================
# If regression = causation, the reverse slope would be 1/slope. It is not.
reverse_model = ols('size ~ price', data=data_house).fit()

print(f"price ~ size  slope: {slope:.4f}")
print(f"size ~ price  slope: {reverse_model.params['price']:.6f}")
print(f"1 / original slope:  {1/slope:.6f}")
print(f"Reciprocals match?   {1/slope:.6f} ≠ {reverse_model.params['price']:.6f}")
print("→ Regression is asymmetric: association, not causation!")

# =============================================================================
# STEP 8: Nonparametric regression — check the linearity assumption
# =============================================================================
# LOWESS fits weighted local regressions; if the curve tracks the OLS line,
# the linear assumption is validated for this dataset
lowess_result = lowess(data_house['price'], data_house['size'], frac=0.6)

fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(data_house['size'], data_house['price'], s=60, alpha=0.6, label='Actual data')
ax.plot(data_house['size'], model.fittedvalues, color='red',
        linewidth=2, label='OLS (parametric)')
ax.plot(lowess_result[:, 0], lowess_result[:, 1], color='green',
        linewidth=2, linestyle='--', label='LOWESS (nonparametric)')
ax.set_xlabel('House Size (square feet)')
ax.set_ylabel('House Sale Price (dollars)')
ax.set_title('Parametric vs Nonparametric Regression')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
