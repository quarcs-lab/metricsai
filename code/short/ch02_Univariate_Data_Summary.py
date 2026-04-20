# =============================================================================
# CHAPTER 2 CHEAT SHEET: Univariate Data Summary
# =============================================================================

# --- Libraries ---
import numpy as np                        # numerical operations (log, mean)
import pandas as pd                       # data loading and manipulation
import matplotlib.pyplot as plt           # creating plots and visualizations
from scipy import stats                   # skewness, kurtosis, distribution shape

# =============================================================================
# STEP 1: Load data directly from a URL
# =============================================================================
# pd.read_stata() reads Stata .dta files; this dataset has 171 observations
url_earnings = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_EARNINGS.DTA"
data_earnings = pd.read_stata(url_earnings)

earnings = data_earnings['earnings']
print(f"Dataset: {data_earnings.shape[0]} observations, {data_earnings.shape[1]} variables")

# =============================================================================
# STEP 2: Summary statistics — mean vs median reveals skewness
# =============================================================================
# .describe() gives count, mean, std, min, quartiles, max in one call
print(data_earnings[['earnings']].describe().round(2))

# Skewness and kurtosis measure the shape of the distribution
print(f"\nSkewness:        {stats.skew(earnings):.2f}  (> 1 = strongly right-skewed)")
print(f"Excess kurtosis: {stats.kurtosis(earnings):.2f}  (> 0 = heavier tails than normal)")
print(f"Mean - Median:   ${earnings.mean() - earnings.median():,.0f}  (positive gap signals right skew)")

# =============================================================================
# STEP 3: Histogram with KDE overlay — see the distribution shape
# =============================================================================
# Bin width is a choice: narrower = more detail (and noise), wider = smoother
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(earnings, bins=20, edgecolor='black', alpha=0.7, density=True, label='Histogram')
earnings.plot.kde(ax=ax, linewidth=2, color='red', label='KDE')
ax.set_xlabel('Annual Earnings ($)')
ax.set_ylabel('Density')
ax.set_title('Earnings Distribution: Histogram + Kernel Density Estimate')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# =============================================================================
# STEP 4: Box plot — visualize quartiles and outliers
# =============================================================================
# The box spans Q1 to Q3 (IQR); whiskers extend 1.5×IQR; dots are outliers
fig, ax = plt.subplots(figsize=(10, 4))
ax.boxplot(earnings, vert=False, patch_artist=True,
           boxprops=dict(facecolor='lightblue', alpha=0.7),
           medianprops=dict(color='red', linewidth=2))
ax.set_xlabel('Annual Earnings ($)')
ax.set_title('Box Plot of Earnings — Median, Quartiles, and Outliers')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# =============================================================================
# STEP 5: Log transformation — taming right skew
# =============================================================================
# np.log() compresses big values and stretches small ones, making skewed
# distributions more symmetric — a prerequisite for many statistical methods
data_earnings['lnearnings'] = np.log(earnings)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].hist(earnings, bins=20, edgecolor='black', alpha=0.7, color='steelblue')
axes[0].set_title(f'Original  (skewness = {stats.skew(earnings):.2f})')
axes[0].set_xlabel('Earnings ($)')

axes[1].hist(data_earnings['lnearnings'], bins=20, edgecolor='black', alpha=0.7, color='coral')
axes[1].set_title(f'Log-transformed  (skewness = {stats.skew(data_earnings["lnearnings"]):.2f})')
axes[1].set_xlabel('ln(Earnings)')

plt.suptitle('Effect of Log Transformation on Skewness', fontweight='bold')
plt.tight_layout()
plt.show()

# =============================================================================
# STEP 6: Z-scores — how unusual is each observation?
# =============================================================================
# z = (x - mean) / std  puts every value on a common "standard deviations
# from the mean" scale: |z| > 2 is unusual, |z| > 3 is very unusual
z_scores = (earnings - earnings.mean()) / earnings.std()

print(f"Highest earner: ${earnings.max():,.0f}  →  z = {z_scores.max():.2f}")
print(f"Median earner:  ${earnings.median():,.0f}  →  z = {(earnings.median() - earnings.mean()) / earnings.std():.2f}")
print(f"Observations with |z| > 2: {(z_scores.abs() > 2).sum()} out of {len(z_scores)}")

# =============================================================================
# STEP 7: Time series — moving average smooths seasonal noise
# =============================================================================
# Monthly home sales zigzag with the seasons; an 11-month moving average
# cancels one full seasonal cycle, revealing the underlying trend
url_homesales = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_MONTHLYHOMESALES.DTA"
data_hs = pd.read_stata(url_homesales)
data_hs = data_hs[data_hs['year'] >= 2005]

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(data_hs['daten'], data_hs['exsales'], linewidth=1, alpha=0.6, label='Original (monthly)')
ax.plot(data_hs['daten'], data_hs['exsales_ma11'], linewidth=2, color='red',
        linestyle='--', label='11-month Moving Average')
ax.set_xlabel('Year')
ax.set_ylabel('Monthly Home Sales')
ax.set_title('U.S. Home Sales: Raw Series vs. Moving Average (2005–2015)')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
