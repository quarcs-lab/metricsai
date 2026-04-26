# =============================================================================
# CHAPTER 17 CHEAT SHEET: Panel Data, Time Series Data, Causation
# =============================================================================

# --- Libraries ---
import pandas as pd                       # data loading and manipulation
import numpy as np                         # numerical operations
import matplotlib.pyplot as plt            # creating plots and visualizations
import pyfixest as pf                      # OLS and FE regression with R-style formulas
# !pip install pyfixest  # if not installed
from statsmodels.tsa.stattools import acf  # autocorrelation function

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
fit_pool = pf.feols('lnrevenue ~ wins', data=data_nba)
fit_cluster = pf.feols('lnrevenue ~ wins', data=data_nba, vcov={'CRV1': 'teamid'})

print(f"\nPooled OLS — wins coefficient: {fit_pool.coef()['wins']:.6f}")
print(f"  Default SE:  {fit_pool.se()['wins']:.6f}")
print(f"  Cluster SE:  {fit_cluster.se()['wins']:.6f}")
print(f"  Ratio:       {fit_cluster.se()['wins'] / fit_pool.se()['wins']:.2f}x larger")

# =============================================================================
# STEP 4: Fixed effects — control for unobserved team characteristics
# =============================================================================
# FE uses only within-team variation (de-meaning), eliminating bias from
# persistent traits like market size, brand value, and arena quality.
fit_fe = pf.feols('lnrevenue ~ wins | teamid', data=data_nba, vcov={'CRV1': 'teamid'})

print(f"\nFixed Effects — wins coefficient: {fit_fe.coef()['wins']:.6f}")
print(f"  Cluster SE:  {fit_fe.se()['wins']:.6f}")
print(f"  R² (within): {fit_fe._r2_within:.4f}")

print(f"\nComparison:")
print(f"  Pooled OLS coef: {fit_pool.coef()['wins']:.6f}")
print(f"  Fixed Effects:   {fit_fe.coef()['wins']:.6f}")
print(f"  FE is smaller → pooled OLS had positive omitted variable bias")

# =============================================================================
# STEP 5: Time series — levels vs first differences
# =============================================================================
# Non-stationary (trending) series produce spurious regressions with misleading R².
# First differencing removes trends and restores valid inference.
url_rates = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_INTERESTRATES.DTA"
data_rates = pd.read_stata(url_rates)

# Regression in levels (potentially spurious)
fit_levels = pf.feols('gs10 ~ gs1', data=data_rates)

# Regression in first differences (removes trends)
fit_changes = pf.feols('dgs10 ~ dgs1', data=data_rates)

print(f"\nLevels regression:  gs1 coef = {fit_levels.coef()['gs1']:.4f}, R² = {fit_levels._r2:.4f}")
print(f"Changes regression: dgs1 coef = {fit_changes.coef()['dgs1']:.4f}, R² = {fit_changes._r2:.4f}")
print(f"R² drops after differencing — lower but honest (no spurious trend inflation)")

# =============================================================================
# STEP 6: Autocorrelation diagnostics — the smoking gun
# =============================================================================
# Slowly decaying ACF in residuals signals non-stationarity and invalid SEs.
# After differencing, autocorrelation should drop dramatically.
acf_levels  = acf(pd.Series(fit_levels._u_hat).dropna(), nlags=5)
acf_changes = acf(pd.Series(fit_changes._u_hat).dropna(), nlags=5)

print(f"\nResidual autocorrelation (lag 1):")
print(f"  Levels regression:  {acf_levels[1]:.4f} (high → non-stationary residuals)")
print(f"  Changes regression: {acf_changes[1]:.4f} (much lower → differencing worked)")

# HAC (Newey-West) SEs correct for autocorrelation without differencing
fit_hac = pf.feols('gs10 ~ gs1', data=data_rates, vcov={'NW': 24})
print(f"\nDefault SE on gs1:   {fit_levels.se()['gs1']:.4f}")
print(f"HAC SE on gs1:       {fit_hac.se()['gs1']:.4f}")
print(f"HAC is {fit_hac.se()['gs1'] / fit_levels.se()['gs1']:.1f}x larger — default SEs are too small")

# =============================================================================
# STEP 7: ADL model — dynamic multipliers
# =============================================================================
# Autoregressive distributed lag models capture how effects build over time.
# Lagged dependent and independent variables model persistence and transmission.
data_rates['dgs10_lag1'] = data_rates['dgs10'].shift(1)
data_rates['dgs10_lag2'] = data_rates['dgs10'].shift(2)
data_rates['dgs1_lag1']  = data_rates['dgs1'].shift(1)
data_rates['dgs1_lag2']  = data_rates['dgs1'].shift(2)

fit_adl = pf.feols('dgs10 ~ dgs10_lag1 + dgs10_lag2 + dgs1 + dgs1_lag1 + dgs1_lag2',
                   data=data_rates)

print(f"\nADL(2,2) Model:")
print(f"  Impact multiplier (dgs1):       {fit_adl.coef()['dgs1']:.4f}")
print(f"  1-month cumulative:             {fit_adl.coef()['dgs1'] + fit_adl.coef()['dgs1_lag1']:.4f}")
print(f"  2-month cumulative:             {fit_adl.coef()['dgs1'] + fit_adl.coef()['dgs1_lag1'] + fit_adl.coef()['dgs1_lag2']:.4f}")
print(f"  R²: {fit_adl._r2:.4f} (much higher than static model)")

# Check residual autocorrelation — should be near zero if well-specified
acf_adl = acf(pd.Series(fit_adl._u_hat).dropna(), nlags=5)
print(f"  Residual ACF(1): {acf_adl[1]:.4f} (near zero → dynamics captured)")
