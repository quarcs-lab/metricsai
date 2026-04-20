# =============================================================================
# CHAPTER 17 CHEAT SHEET: Panel Data, Time Series Data, Causation
# =============================================================================

# --- Libraries ---
import pandas as pd                       # data loading and manipulation
import numpy as np                         # numerical operations
import matplotlib.pyplot as plt            # creating plots and visualizations
import statsmodels.api as sm               # statistical models and tools
from statsmodels.formula.api import ols    # OLS regression with R-style formulas
from statsmodels.tsa.stattools import acf  # autocorrelation function
from linearmodels.panel import PanelOLS    # fixed effects panel estimation

# =============================================================================
# STEP 1: Load panel data (NBA teams across seasons)
# =============================================================================
# Panel data: multiple individuals (teams) observed over multiple time periods
url_nba = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_NBA.DTA"
data_nba = pd.read_stata(url_nba)

print(f"Panel: {data_nba['teamid'].nunique()} teams × {data_nba['season'].nunique()} seasons = {len(data_nba)} obs")

# =============================================================================
# STEP 2: Variance decomposition — between vs within variation
# =============================================================================
# Understanding which variation your estimator uses is the first step in panel analysis
overall_sd = data_nba['lnrevenue'].std()
between_sd = data_nba.groupby('teamid')['lnrevenue'].mean().std()
within_sd  = data_nba.groupby('teamid')['lnrevenue'].apply(lambda x: x - x.mean()).std()

print(f"\nVariance Decomposition of Log Revenue:")
print(f"  Overall SD:  {overall_sd:.4f}")
print(f"  Between SD:  {between_sd:.4f} (across teams)")
print(f"  Within SD:   {within_sd:.4f} (over time)")
print(f"  Between > Within → team characteristics dominate year-to-year swings")

# =============================================================================
# STEP 3: Pooled OLS with cluster-robust SEs
# =============================================================================
# Observations within the same team are correlated over time — default SEs
# dramatically understate uncertainty. Always cluster by individual in panel data.
model_pool = ols('lnrevenue ~ wins', data=data_nba).fit()
model_cluster = ols('lnrevenue ~ wins', data=data_nba).fit(
    cov_type='cluster', cov_kwds={'groups': data_nba['teamid']}
)

print(f"\nPooled OLS — wins coefficient: {model_pool.params['wins']:.6f}")
print(f"  Default SE:  {model_pool.bse['wins']:.6f}")
print(f"  Cluster SE:  {model_cluster.bse['wins']:.6f}")
print(f"  Ratio:       {model_cluster.bse['wins'] / model_pool.bse['wins']:.2f}x larger")

# =============================================================================
# STEP 4: Fixed effects — control for unobserved team characteristics
# =============================================================================
# FE uses only within-team variation (de-meaning), eliminating bias from
# persistent traits like market size, brand value, and arena quality.
data_panel = data_nba.set_index(['teamid', 'season'])
y = data_panel[['lnrevenue']]
X = data_panel[['wins']]

model_fe = PanelOLS(y, X, entity_effects=True).fit(cov_type='clustered', cluster_entity=True)

print(f"\nFixed Effects — wins coefficient: {model_fe.params['wins']:.6f}")
print(f"  Cluster SE:  {model_fe.std_errors['wins']:.6f}")
print(f"  R² (within): {model_fe.rsquared_within:.4f}")

print(f"\nComparison:")
print(f"  Pooled OLS coef: {model_pool.params['wins']:.6f}")
print(f"  Fixed Effects:   {model_fe.params['wins']:.6f}")
print(f"  FE is smaller → pooled OLS had positive omitted variable bias")

# =============================================================================
# STEP 5: Time series — levels vs first differences
# =============================================================================
# Non-stationary (trending) series produce spurious regressions with misleading R².
# First differencing removes trends and restores valid inference.
url_rates = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_INTERESTRATES.DTA"
data_rates = pd.read_stata(url_rates)

# Regression in levels (potentially spurious)
model_levels = ols('gs10 ~ gs1', data=data_rates).fit()

# Regression in first differences (removes trends)
model_changes = ols('dgs10 ~ dgs1', data=data_rates).fit()

print(f"\nLevels regression:  gs1 coef = {model_levels.params['gs1']:.4f}, R² = {model_levels.rsquared:.4f}")
print(f"Changes regression: dgs1 coef = {model_changes.params['dgs1']:.4f}, R² = {model_changes.rsquared:.4f}")
print(f"R² drops after differencing — lower but honest (no spurious trend inflation)")

# =============================================================================
# STEP 6: Autocorrelation diagnostics — the smoking gun
# =============================================================================
# Slowly decaying ACF in residuals signals non-stationarity and invalid SEs.
# After differencing, autocorrelation should drop dramatically.
acf_levels  = acf(model_levels.resid.dropna(), nlags=5)
acf_changes = acf(model_changes.resid.dropna(), nlags=5)

print(f"\nResidual autocorrelation (lag 1):")
print(f"  Levels regression:  {acf_levels[1]:.4f} (high → non-stationary residuals)")
print(f"  Changes regression: {acf_changes[1]:.4f} (much lower → differencing worked)")

# HAC (Newey-West) SEs correct for autocorrelation without differencing
model_hac = ols('gs10 ~ gs1', data=data_rates).fit(cov_type='HAC', cov_kwds={'maxlags': 24})
print(f"\nDefault SE on gs1:   {model_levels.bse['gs1']:.4f}")
print(f"HAC SE on gs1:       {model_hac.bse['gs1']:.4f}")
print(f"HAC is {model_hac.bse['gs1'] / model_levels.bse['gs1']:.1f}x larger — default SEs are too small")

# =============================================================================
# STEP 7: ADL model — dynamic multipliers
# =============================================================================
# Autoregressive distributed lag models capture how effects build over time.
# Lagged dependent and independent variables model persistence and transmission.
data_rates['dgs10_lag1'] = data_rates['dgs10'].shift(1)
data_rates['dgs10_lag2'] = data_rates['dgs10'].shift(2)
data_rates['dgs1_lag1']  = data_rates['dgs1'].shift(1)
data_rates['dgs1_lag2']  = data_rates['dgs1'].shift(2)

model_adl = ols('dgs10 ~ dgs10_lag1 + dgs10_lag2 + dgs1 + dgs1_lag1 + dgs1_lag2',
                data=data_rates).fit()

print(f"\nADL(2,2) Model:")
print(f"  Impact multiplier (dgs1):       {model_adl.params['dgs1']:.4f}")
print(f"  1-month cumulative:             {model_adl.params['dgs1'] + model_adl.params['dgs1_lag1']:.4f}")
print(f"  2-month cumulative:             {model_adl.params['dgs1'] + model_adl.params['dgs1_lag1'] + model_adl.params['dgs1_lag2']:.4f}")
print(f"  R²: {model_adl.rsquared:.4f} (much higher than static model)")

# Check residual autocorrelation — should be near zero if well-specified
acf_adl = acf(model_adl.resid.dropna(), nlags=5)
print(f"  Residual ACF(1): {acf_adl[1]:.4f} (near zero → dynamics captured)")
