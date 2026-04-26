# =============================================================================
# CHAPTER 9 CHEAT SHEET: Models with Natural Logarithms
# =============================================================================

# --- Libraries ---
import numpy as np                        # logarithms and exponentials
import pandas as pd                       # data loading and manipulation
import matplotlib.pyplot as plt           # creating plots and visualizations
import pyfixest as pf                     # OLS regression with R-style formulas
# !pip install pyfixest  # if not installed

# =============================================================================
# STEP 1: Load the earnings-education dataset
# =============================================================================
# pd.read_stata() reads Stata .dta files directly from a URL
url_earn = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_EARNINGS.DTA"
data_earnings = pd.read_stata(url_earn)

print(f"Dataset: {data_earnings.shape[0]} observations, {data_earnings.shape[1]} variables")

# =============================================================================
# STEP 2: Logarithmic approximation — why economists use logs
# =============================================================================
# Key property: Δln(x) ≈ Δx/x (proportionate change)
# Multiplying by 100 gives the percentage change
x0, x1 = 40, 40.4
exact = (x1 - x0) / x0
approx = np.log(x1) - np.log(x0)
print(f"Change from {x0} to {x1}:")
print(f"  Exact proportionate change: {exact:.6f} ({exact*100:.2f}%)")
print(f"  Log approximation Δln(x):   {approx:.6f} ({approx*100:.2f}%)")

# =============================================================================
# STEP 3: Descriptive statistics and log transformations
# =============================================================================
# Create log-transformed variables for the regression models
data_earnings['lnearn'] = np.log(data_earnings['earnings'])
data_earnings['lneduc'] = np.log(data_earnings['education'])

print(data_earnings[['earnings', 'lnearn', 'education', 'lneduc']].describe().round(2))

# =============================================================================
# STEP 4: Estimate all four model specifications
# =============================================================================
# Each model answers a different economic question about earnings and education

# Model 1: Linear — Δy = β₁Δx (dollar change per year of education)
fit_linear = pf.feols('earnings ~ education', data=data_earnings)

# Model 2: Log-linear — 100β₁ ≈ % change in y per unit x (semi-elasticity)
fit_loglin = pf.feols('lnearn ~ education', data=data_earnings)

# Model 3: Log-log — β₁ ≈ % change in y per % change in x (elasticity)
fit_loglog = pf.feols('lnearn ~ lneduc', data=data_earnings)

# Model 4: Linear-log — β₁/100 ≈ dollar change per % change in x
fit_linlog = pf.feols('earnings ~ lneduc', data=data_earnings)

# Print the most important model: log-linear (semi-elasticity)
semi_elast = fit_loglin.coef()['education']
print(f"Log-linear: each year of education → {100*semi_elast:.1f}% higher earnings")
print(f"Log-log elasticity: {fit_loglog.coef()['lneduc']:.3f}")

# Full regression table for the log-linear model
fit_loglin.summary()

# =============================================================================
# STEP 5: Compare all four models side by side
# =============================================================================
# The comparison shows that model choice affects both R² and interpretation
models = {
    'Linear':     ('earnings ~ education',  fit_linear,  'education', '${:,.0f} per year'),
    'Log-linear': ('ln(y) ~ x',            fit_loglin,  'education', '{:.1f}% per year'),
    'Log-log':    ('ln(y) ~ ln(x)',         fit_loglog,  'lneduc',   '{:.2f}% per 1%'),
    'Linear-log': ('y ~ ln(x)',            fit_linlog,  'lneduc',   '${:,.0f} per 1%'),
}

print(f"{'Model':<12} {'Specification':<16} {'Slope':>10} {'R²':>8}  Interpretation")
print("-" * 75)
for name, (spec, m, var, fmt) in models.items():
    slope = m.coef()[var]
    interp = fmt.format(100*slope if 'per year' in fmt and 'Log' in name else slope/100 if 'per 1%' in fmt and name == 'Linear-log' else slope)
    print(f"{name:<12} {spec:<16} {slope:>10.4f} {m._r2:>8.3f}  {interp}")

# =============================================================================
# STEP 6: Scatter plot with the log-linear fitted line
# =============================================================================
# The log-linear model (semi-elasticity) provides the best fit for earnings data
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(data_earnings['education'], data_earnings['lnearn'], s=50, alpha=0.7)
ax.plot(data_earnings['education'], fit_loglin.predict(),
        color='red', linewidth=2, label='Fitted line')
ax.set_xlabel('Education (years)')
ax.set_ylabel('ln(Earnings)')
ax.set_title(f'Log-Linear Model: semi-elasticity = {semi_elast:.4f}  (R² = {fit_loglin._r2:.3f})')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# =============================================================================
# STEP 7: Exponential growth — S&P 500 and the Rule of 72
# =============================================================================
# Exponential growth in levels becomes linear in logs:
# ln(x_t) ≈ ln(x₀) + r × t, where slope r = annual growth rate
url_sp500 = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_SP500INDEX.DTA"
data_sp500 = pd.read_stata(url_sp500)

fit_sp500 = pf.feols('lnsp500 ~ year', data=data_sp500)
growth_rate = fit_sp500.coef()['year']

print(f"S&P 500 estimated growth rate: {100*growth_rate:.2f}% per year")
print(f"Rule of 72: doubles every {72/(100*growth_rate):.1f} years")
print(f"R-squared: {fit_sp500._r2:.4f}")

# Visualize: exponential in levels vs. linear in logs
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].plot(data_sp500['year'], data_sp500['sp500'], linewidth=2)
axes[0].set_xlabel('Year')
axes[0].set_ylabel('S&P 500 Index')
axes[0].set_title('Exponential Growth in Levels')
axes[0].grid(True, alpha=0.3)

axes[1].plot(data_sp500['year'], data_sp500['lnsp500'], linewidth=2)
axes[1].plot(data_sp500['year'], fit_sp500.predict(),
             color='red', linewidth=2, linestyle='--', label='Fitted (linear)')
axes[1].set_xlabel('Year')
axes[1].set_ylabel('ln(S&P 500 Index)')
axes[1].set_title(f'Linear in Logs: growth = {100*growth_rate:.2f}%/year')
axes[1].legend()
axes[1].grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
