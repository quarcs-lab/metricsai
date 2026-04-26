# =============================================================================
# CHAPTER 1 CHEAT SHEET: Analysis of Economics Data
# =============================================================================

# --- Libraries ---
import pandas as pd                       # data loading and manipulation
import matplotlib.pyplot as plt           # creating plots and visualizations
import pyfixest as pf                     # OLS regression with R-style formulas
# !pip install pyfixest  # if not installed

# =============================================================================
# STEP 1: Load data directly from a URL
# =============================================================================
# pd.read_stata() reads Stata .dta files (pandas also supports CSV, Excel, etc.)
url = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_HOUSE.DTA"
data_house = pd.read_stata(url)

print(f"Dataset: {data_house.shape[0]} observations, {data_house.shape[1]} variables")

# =============================================================================
# STEP 2: Descriptive statistics — summarize before modeling
# =============================================================================
# .head() shows the first rows; .describe() gives mean, std, min, quartiles, max
print(data_house[['price', 'size']].describe().round(2))

# =============================================================================
# STEP 3: Scatter plot — always visualize before fitting a regression
# =============================================================================
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(data_house['size'], data_house['price'], s=50, alpha=0.7)
ax.set_xlabel('House Size (square feet)')
ax.set_ylabel('House Sale Price (dollars)')
ax.set_title('House Price vs Size')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# =============================================================================
# STEP 4: OLS regression — fit the model
# =============================================================================
# Formula syntax: 'y ~ x' regresses y on x (intercept included automatically)
fit = pf.feols('price ~ size', data=data_house)

# Extract key results
slope     = fit.coef()['size']         # marginal effect: $/sq ft
intercept = fit.coef()['Intercept']    # predicted price when size = 0
r_squared = fit._r2                    # proportion of variation explained

print(f"Estimated equation: price = {intercept:,.0f} + {slope:.2f} × size")
print(f"Interpretation: each additional sq ft is associated with ${slope:,.2f} higher price")
print(f"R-squared: {r_squared:.4f} ({r_squared*100:.1f}% of variation explained)")

# Full regression table (coefficients, std errors, t-stats, p-values, R²)
fit.summary()

# =============================================================================
# STEP 5: Scatter plot with fitted regression line and R²
# =============================================================================
# fit.predict() contains the predicted y-values from the estimated equation
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(data_house['size'], data_house['price'], s=50, alpha=0.7, label='Actual prices')
ax.plot(data_house['size'], fit.predict(), color='red', linewidth=2, label='Fitted line')
ax.set_xlabel('House Size (square feet)')
ax.set_ylabel('House Sale Price (dollars)')
ax.set_title(f'OLS Regression: price = {intercept:,.0f} + {slope:.2f} × size  (R² = {r_squared:.2%})')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# =============================================================================
# STEP 6: Compare predictors — association is NOT causation
# =============================================================================
# Running separate regressions with different x-variables shows that each tells
# a different story. High R² does not prove causation — omitted variables
# (location, condition, school district) can bias any single-variable slope.
predictors = {
    'size':      'Size (sq ft)',
    'bedrooms':  'Bedrooms',
    'bathrooms': 'Bathrooms',
    'lotsize':   'Lot size',
    'age':       'Age (years)',
}

print(f"{'Predictor':<18} {'Slope':>10} {'R²':>8}")
print("-" * 38)
for var, label in predictors.items():
    m = pf.feols(f'price ~ {var}', data=data_house)
    print(f"{label:<18} {m.coef()[var]:>10.2f} {m._r2:>8.4f}")
