# =============================================================================
# CHAPTER 8 CHEAT SHEET: Case Studies for Bivariate Regression
# =============================================================================

# --- Libraries ---
import pandas as pd                       # data loading and manipulation
import matplotlib.pyplot as plt           # creating plots and visualizations
import pyfixest as pf                     # OLS regression with R-style formulas
# !pip install pyfixest  # if not installed

# =============================================================================
# STEP 1: Load OECD health data from a URL
# =============================================================================
# pd.read_stata() reads Stata .dta files — this dataset covers 34 OECD countries
url_health = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_HEALTH2009.DTA"
data_health = pd.read_stata(url_health)

print(f"Health dataset: {data_health.shape[0]} countries, {data_health.shape[1]} variables")

# =============================================================================
# STEP 2: Descriptive statistics — summarize before modeling
# =============================================================================
# .describe() gives mean, std, min, quartiles, max for each variable
print(data_health[['hlthpc', 'lifeexp', 'infmort', 'gdppc']].describe().round(2))

# =============================================================================
# STEP 3: Health outcomes regression with robust standard errors
# =============================================================================
# Does higher health spending improve life expectancy?
fit_life = pf.feols('lifeexp ~ hlthpc', data=data_health)

slope_life = fit_life.coef()['hlthpc']
r2_life    = fit_life._r2

print(f"Life expectancy: slope = {slope_life:.5f}, R² = {r2_life:.4f}")
print(f"Each extra $1,000 in spending → {slope_life*1000:.2f} more years of life expectancy")

# Robust standard errors adjust for non-constant error variance (heteroskedasticity)
fit_life_robust = pf.feols('lifeexp ~ hlthpc', data=data_health, vcov='HC1')
fit_life_robust.summary()

# =============================================================================
# STEP 4: Health spending vs GDP — income elasticity
# =============================================================================
# How much of health spending is driven by national income?
fit_gdp = pf.feols('hlthpc ~ gdppc', data=data_health)

slope_gdp = fit_gdp.coef()['gdppc']
r2_gdp    = fit_gdp._r2

# Income elasticity at the mean: (slope × mean_x) / mean_y
mean_gdp  = data_health['gdppc'].mean()
mean_hlth = data_health['hlthpc'].mean()
elasticity = (slope_gdp * mean_gdp) / mean_hlth

print(f"Health spending on GDP: slope = {slope_gdp:.4f}, R² = {r2_gdp:.4f}")
print(f"Income elasticity at the mean: {elasticity:.2f} (≈1.0 → normal good)")

# =============================================================================
# STEP 5: Outlier robustness — excluding USA and Luxembourg
# =============================================================================
# Two countries drive much of the model's "misfit" — test robustness by excluding them
data_subset = data_health[(data_health['code'] != 'USA') &
                          (data_health['code'] != 'LUX')]

fit_subset = pf.feols('hlthpc ~ gdppc', data=data_subset)

print(f"\nAll 34 countries:  slope = {slope_gdp:.4f}, R² = {r2_gdp:.4f}")
print(f"Excluding USA/LUX: slope = {fit_subset.coef()['gdppc']:.4f}, R² = {fit_subset._r2:.4f}")
print("Removing 2 of 34 countries transforms R² — always check for influential observations!")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
for ax, df, mdl, title in zip(
        axes,
        [data_health, data_subset],
        [fit_gdp, fit_subset],
        ['All 34 Countries', 'Excluding USA & Luxembourg']):
    ax.scatter(df['gdppc'], df['hlthpc'], s=50, alpha=0.7)
    ax.plot(df['gdppc'], mdl.predict(), color='red', linewidth=2)
    ax.set_xlabel('GDP per capita ($)')
    ax.set_ylabel('Health spending per capita ($)')
    ax.set_title(f'{title}  (R² = {mdl._r2:.2f})')
    ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# =============================================================================
# STEP 6: CAPM — estimating Coca-Cola's beta (systematic risk)
# =============================================================================
# Beta measures how a stock's excess return co-moves with the market excess return
url_capm = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_CAPM.DTA"
data_capm = pd.read_stata(url_capm)

fit_capm = pf.feols('rko_rf ~ rm_rf', data=data_capm)

alpha = fit_capm.coef()['Intercept']     # excess return beyond CAPM prediction
beta  = fit_capm.coef()['rm_rf']         # systematic risk
r2_capm = fit_capm._r2

print(f"Coca-Cola CAPM: alpha = {alpha:.4f}, beta = {beta:.4f}, R² = {r2_capm:.4f}")
print(f"Beta < 1 → defensive stock (moves less than the market)")
print(f"R² = {r2_capm:.2%} explained by market; {1-r2_capm:.2%} is idiosyncratic risk")

# Full regression table
fit_capm.summary()

# =============================================================================
# STEP 7: Okun's Law — GDP growth vs unemployment change
# =============================================================================
# Okun (1962): each +1 point in unemployment → ≈ -2 points in GDP growth
url_gdp = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_GDPUNEMPLOY.DTA"
data_gdp = pd.read_stata(url_gdp)

fit_okun = pf.feols('rgdpgrowth ~ uratechange', data=data_gdp)

slope_okun = fit_okun.coef()['uratechange']
r2_okun    = fit_okun._r2

print(f"Okun's Law: slope = {slope_okun:.2f} (Okun's original: -2.0)")
print(f"R² = {r2_okun:.4f} — unemployment explains {r2_okun*100:.0f}% of GDP growth variation")

# Scatter plot with fitted line
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(data_gdp['uratechange'], data_gdp['rgdpgrowth'], s=50, alpha=0.7)
ax.plot(data_gdp['uratechange'], fit_okun.predict(), color='red', linewidth=2,
        label=f'Fitted: slope = {slope_okun:.2f}')
ax.axhline(y=0, color='gray', linestyle=':', linewidth=1, alpha=0.5)
ax.set_xlabel('Change in unemployment rate (percentage points)')
ax.set_ylabel('Real GDP growth (%)')
ax.set_title(f"Okun's Law: GDP Growth vs Unemployment Change  (R² = {r2_okun:.2f})")
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
