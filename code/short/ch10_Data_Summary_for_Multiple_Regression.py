# =============================================================================
# CHAPTER 10 CHEAT SHEET: Data Summary for Multiple Regression
# =============================================================================

# --- Libraries ---
import numpy as np                                          # numerical operations
import pandas as pd                                         # data loading and manipulation
import matplotlib.pyplot as plt                             # creating plots and visualizations
import seaborn as sns                                       # statistical visualization (heatmaps, pairplots)
import pyfixest as pf                                       # OLS regression with R-style formulas
# !pip install pyfixest  # if not installed
from statsmodels.stats.outliers_influence import variance_inflation_factor  # multicollinearity detection

# =============================================================================
# STEP 1: Load data and explore
# =============================================================================
# pd.read_stata() reads Stata .dta files directly from a URL
url = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_HOUSE.DTA"
data_house = pd.read_stata(url)

print(f"Dataset: {data_house.shape[0]} observations, {data_house.shape[1]} variables")
print(data_house[['price', 'size', 'bedrooms', 'bathrooms', 'lotsize', 'age']].describe().round(2))

# =============================================================================
# STEP 2: Partial effects vs. total effects — why controls matter
# =============================================================================
# Bivariate regression captures TOTAL effect (direct + indirect through size)
fit_bivariate = pf.feols('price ~ bedrooms', data=data_house)

# Multiple regression isolates the PARTIAL effect (holding size constant)
fit_partial = pf.feols('price ~ bedrooms + size', data=data_house)

print(f"Bedrooms coefficient (bivariate):  ${fit_bivariate.coef()['bedrooms']:,.2f}")
print(f"Bedrooms coefficient (multiple):   ${fit_partial.coef()['bedrooms']:,.2f}")
print(f"Change: ${fit_partial.coef()['bedrooms'] - fit_bivariate.coef()['bedrooms']:,.2f}")
# The coefficient drops from ~$23,667 to ~$1,553 once we control for size

# =============================================================================
# STEP 3: Correlation matrix — check pairwise associations before modeling
# =============================================================================
# High correlations between regressors signal potential multicollinearity
corr_vars = ['price', 'size', 'bedrooms', 'bathrooms', 'lotsize', 'age']
corr_matrix = data_house[corr_vars].corr()

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='coolwarm', center=0,
            square=True, linewidths=1)
ax.set_title('Correlation Matrix Heatmap')
plt.tight_layout()
plt.show()

print(f"Price-Size correlation: {corr_matrix.loc['price', 'size']:.3f}")
print(f"Size-Bedrooms correlation: {corr_matrix.loc['size', 'bedrooms']:.3f}")

# =============================================================================
# STEP 4: Full multiple regression — estimate partial effects
# =============================================================================
# Each coefficient measures the change in price for a one-unit change in that
# variable, holding ALL other regressors constant
fit_full = pf.feols('price ~ size + bedrooms + bathrooms + lotsize + age + monthsold',
                    data=data_house)

size_coef = fit_full.coef()['size']
print(f"Size effect: each additional sq ft is associated with ${size_coef:,.2f} higher price")
print(f"R-squared: {fit_full._r2:.4f} ({fit_full._r2*100:.1f}% of variation explained)")
print(f"Adjusted R-squared: {fit_full._adj_r2:.4f}")

# Full regression table (coefficients, std errors, t-stats, p-values)
fit_full.summary()

# =============================================================================
# STEP 5: FWL theorem — how "holding constant" actually works
# =============================================================================
# Step A: Regress size on all other regressors, keep residuals
fit_size_on_others = pf.feols('size ~ bedrooms + bathrooms + lotsize + age + monthsold',
                              data=data_house)
resid_size = fit_size_on_others._u_hat

# Step B: Regress price on those residuals — the slope matches the full model
data_house['resid_size'] = resid_size
fit_fwl = pf.feols('price ~ resid_size', data=data_house)

print(f"Size coef from FULL regression:     {fit_full.coef()['size']:.10f}")
print(f"Coef from FWL residual regression:  {fit_fwl.coef()['resid_size']:.10f}")
# These are identical — the FWL theorem in action

# =============================================================================
# STEP 6: Model comparison — parsimony vs. complexity
# =============================================================================
# Compare simple (size only) vs. full model using fit statistics
fit_simple = pf.feols('price ~ size', data=data_house)

comparison = pd.DataFrame({
    'Model': ['Size only', 'Full (all variables)'],
    'R²':     [fit_simple._r2,     fit_full._r2],
    'Adj R²': [fit_simple._adj_r2, fit_full._adj_r2],
    'AIC':    [fit_simple._aic,    fit_full._aic],
    'BIC':    [fit_simple._bic,    fit_full._bic],
})
print(comparison.to_string(index=False))
# Adj R² DECREASES when adding 5 weak predictors — parsimony wins

# =============================================================================
# STEP 7: VIF — detect multicollinearity
# =============================================================================
# VIF_j = 1 / (1 - R²_j), where R²_j is from regressing x_j on all other x's
# VIF > 5: moderate concern; VIF > 10: severe multicollinearity
X = data_house[['size', 'bedrooms', 'bathrooms', 'lotsize', 'age', 'monthsold']]
vif_data = pd.DataFrame({
    'Variable': X.columns,
    'VIF': [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
})
print(vif_data.to_string(index=False))

# =============================================================================
# STEP 8: Diagnostics — actual vs. predicted and residual plots
# =============================================================================
# Good fit: points hug the 45° line; residuals scatter randomly around zero
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Actual vs. predicted
axes[0].scatter(data_house['price'], fit_full.predict(), alpha=0.7, s=50)
axes[0].plot([data_house['price'].min(), data_house['price'].max()],
             [data_house['price'].min(), data_house['price'].max()],
             'r--', linewidth=2, label='Perfect prediction (45° line)')
axes[0].set_xlabel('Actual Price ($)')
axes[0].set_ylabel('Predicted Price ($)')
axes[0].set_title('Actual vs Predicted')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Residual plot
axes[1].scatter(fit_full.predict(), fit_full._u_hat, alpha=0.7, s=50)
axes[1].axhline(y=0, color='red', linestyle='--', linewidth=2)
axes[1].set_xlabel('Fitted Values ($)')
axes[1].set_ylabel('Residuals ($)')
axes[1].set_title('Residual Plot')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
