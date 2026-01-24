"""
ch17_Panel_Data_Time_Series_Data_Causation.py - January 2026 for Python

Chapter 17: PANEL DATA, TIME SERIES DATA, CAUSATION

To run you need files:
  AED_NBA.DTA
  AED_EARNINGS_COMPLETE.DTA
  AED_INTERESTRATES.DTA
in the data/ directory

Sections covered:
  17.1 CROSS-SECTION DATA (conceptual)
  17.2 PANEL DATA (conceptual)
  17.3 PANEL DATA EXAMPLE: NBA TEAM REVENUE
  17.4 CAUSALITY: AN OVERVIEW (conceptual)
  17.5 NONLINEAR REGRESSION MODELS
  17.6 TIME SERIES DATA (conceptual)
  17.7 TIME SERIES EXAMPLE: U.S. TREASURY SECURITY INTEREST RATES
"""

# ========== SETUP ==========

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from statsmodels.formula.api import ols, logit
from statsmodels.regression.linear_model import OLS
from scipy import stats
from statsmodels.stats.diagnostic import acorr_breusch_godfrey
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.stattools import acf
import random
import os

# For panel data - linearmodels
try:
    from linearmodels.panel import PanelOLS, RandomEffects
    LINEARMODELS_AVAILABLE = True
except ImportError:
    print("Warning: linearmodels not available. Install with: pip install linearmodels")
    LINEARMODELS_AVAILABLE = False

# Set random seeds for reproducibility
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
os.environ['PYTHONHASHSEED'] = str(RANDOM_SEED)

# GitHub data URL
GITHUB_DATA_URL = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/"

# Output directories (optional - for saving figures and tables locally)
IMAGES_DIR = 'images'
TABLES_DIR = 'tables'
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(TABLES_DIR, exist_ok=True)

# Set plotting style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

print("=" * 70)
print("CHAPTER 17: PANEL DATA, TIME SERIES DATA, CAUSATION")
print("=" * 70)

# ========== 17.1 CROSS-SECTION DATA ==========

print("\n" + "=" * 70)
print("17.1 CROSS-SECTION DATA")
print("=" * 70)
print("\nConceptual section - no computation required")
print("Key points:")
print("  - Cross-sectional data: observations at a single point in time")
print("  - Independence assumption: observations are independent")
print("  - Standard OLS inference applies")

# ========== 17.2 PANEL DATA ==========

print("\n" + "=" * 70)
print("17.2 PANEL DATA")
print("=" * 70)
print("\nConceptual section - no computation required")
print("Key points:")
print("  - Panel data: multiple observations per individual over time")
print("  - Three dimensions: individual (i), time (t), variables")
print("  - Methods: Pooled OLS, Fixed Effects (FE), Random Effects (RE)")
print("  - FE: Controls for time-invariant unobserved heterogeneity")
print("  - RE: Assumes individual effects uncorrelated with regressors")

# ========== 17.3 PANEL DATA EXAMPLE: NBA TEAM REVENUE ==========

print("\n" + "=" * 70)
print("17.3 PANEL DATA EXAMPLE: NBA TEAM REVENUE")
print("=" * 70)

# Load NBA data
data_nba = pd.read_stata(GITHUB_DATA_URL + 'AED_NBA.DTA')

print("\nNBA Data Summary:")
nba_summary = data_nba.describe()
print(nba_summary)
nba_summary.to_csv(os.path.join(TABLES_DIR, 'ch17_nba_descriptive_stats.csv'))
print(f"Table saved to: {os.path.join(TABLES_DIR, 'ch17_nba_descriptive_stats.csv')}")

# Table 17.1: Panel data structure
print("\n" + "-" * 70)
print("Table 17.1: Panel Data Structure")
print("-" * 70)

variables = ['revenue', 'lnrevenue', 'wins', 'season', 'playoff',
             'champ', 'allstars', 'lncitypop', 'teamid']

print("\nVariable descriptions:")
for var in variables:
    print(f"  {var}: {data_nba[var].dtype}")

summary_stats = data_nba[variables].describe()
print("\n", summary_stats)

# Panel structure information
n_teams = data_nba['teamid'].nunique()
n_seasons = data_nba['season'].nunique()
n_obs = len(data_nba)

print(f"\nPanel structure:")
print(f"  Number of teams: {n_teams}")
print(f"  Number of seasons: {n_seasons}")
print(f"  Total observations: {n_obs}")
print(f"  Balanced panel: {n_obs == n_teams * n_seasons}")

# Within and between variation
print("\n" + "-" * 70)
print("Within and Between Variation")
print("-" * 70)

# Calculate team means
team_means = data_nba.groupby('teamid')['lnrevenue'].mean()
data_nba['meanlnrev'] = data_nba['teamid'].map(team_means)

# Create observation number within each team
data_nba['obsnum'] = data_nba.groupby('teamid').cumcount() + 1

# Between standard deviation (from team means)
between_sd = team_means.std()
print(f"\nBetween SD (from team means): {between_sd:.6f}")

# Within variation (deviations from team means)
data_nba['mdifflnrev'] = data_nba['lnrevenue'] - data_nba['meanlnrev']
within_sd = data_nba['mdifflnrev'].std()
print(f"Within SD (deviations from team means): {within_sd:.6f}")

# Overall standard deviation
overall_sd = data_nba['lnrevenue'].std()
print(f"Overall SD: {overall_sd:.6f}")

# Verify decomposition
print(f"\nNote: Overall² ≈ Between² + Within²")
print(f"  {overall_sd**2:.6f} ≈ {between_sd**2:.6f} + {within_sd**2:.6f}")

# Figure 17.1: Scatter plot with fitted line
print("\n" + "-" * 70)
print("Figure 17.1: Revenue vs Wins")
print("-" * 70)

fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(data_nba['wins'], data_nba['lnrevenue'], alpha=0.5, s=30)

# Add OLS fit line
z = np.polyfit(data_nba['wins'], data_nba['lnrevenue'], 1)
p = np.poly1d(z)
wins_range = np.linspace(data_nba['wins'].min(), data_nba['wins'].max(), 100)
ax.plot(wins_range, p(wins_range), 'r-', linewidth=2, label='OLS fit')

ax.set_xlabel('Wins')
ax.set_ylabel('Log Revenue')
ax.set_title('NBA Team Revenue vs Wins')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(IMAGES_DIR, 'ch17_fig1_nba_revenue_wins.png'), dpi=300, bbox_inches='tight')
print(f"Saved: {os.path.join(IMAGES_DIR, 'ch17_fig1_nba_revenue_wins.png')}")
plt.close()

# OLS regression (pooled)
model_ols_simple = ols('lnrevenue ~ wins', data=data_nba).fit()
print("\nPooled OLS: lnrevenue ~ wins")
print(model_ols_simple.summary())
# Save coefficients
coef_table = pd.DataFrame({
    'coefficient': model_ols_simple.params,
    'std_err': model_ols_simple.bse,
    't_value': model_ols_simple.tvalues,
    'p_value': model_ols_simple.pvalues
})
coef_table.to_csv(os.path.join(TABLES_DIR, 'ch17_pooled_ols_coefficients.csv'))
print(f"Coefficients saved to: {os.path.join(TABLES_DIR, 'ch17_pooled_ols_coefficients.csv')}")

# Correlation matrix
print("\n" + "-" * 70)
print("Correlation Matrix")
print("-" * 70)
corr_vars = ['revenue', 'lnrevenue', 'wins', 'season', 'playoff', 'champ', 'allstars', 'lncitypop']
corr_matrix = data_nba[corr_vars].corr()
print(corr_matrix)
corr_matrix.to_csv(os.path.join(TABLES_DIR, 'ch17_correlation_matrix.csv'))
print(f"Table saved to: {os.path.join(TABLES_DIR, 'ch17_correlation_matrix.csv')}")

# Pooled OLS estimation with different standard errors
print("\n" + "-" * 70)
print("Table 17.2: Pooled OLS with Different Standard Errors")
print("-" * 70)

# Model: lnrevenue ~ wins + season

# Default standard errors
model_ols_default = ols('lnrevenue ~ wins + season', data=data_nba).fit()
print("\nPooled OLS (default SEs):")
print(model_ols_default.summary())

# Heteroskedastic-robust standard errors
model_ols_robust = ols('lnrevenue ~ wins + season', data=data_nba).fit(cov_type='HC1')
print("\nPooled OLS (heteroskedastic-robust SEs):")
print(model_ols_robust.summary())

# Cluster-robust standard errors (clustered by team)
model_ols_cluster = ols('lnrevenue ~ wins + season', data=data_nba).fit(
    cov_type='cluster', cov_kwds={'groups': data_nba['teamid']})
print("\nPooled OLS (cluster-robust SEs):")
print(model_ols_cluster.summary())

# Comparison table
print("\n" + "-" * 70)
print("Comparison of Standard Errors")
print("-" * 70)

se_comparison = pd.DataFrame({
    'Default SE': model_ols_default.bse,
    'Robust SE': model_ols_robust.bse,
    'Cluster SE': model_ols_cluster.bse
})
print(se_comparison)

# Panel data estimation with linearmodels (if available)
if LINEARMODELS_AVAILABLE:
    print("\n" + "-" * 70)
    print("Table 17.3: Pooled, Random Effects, and Fixed Effects")
    print("-" * 70)

    # Prepare data for linearmodels
    data_nba_panel = data_nba.set_index(['teamid', 'season'])

    # Define regressors
    xvars = ['wins', 'season', 'playoff', 'champ', 'allstars', 'lncitypop']

    # Pooled OLS with heteroskedastic-robust SEs (using linearmodels for consistency)
    # Need to reset index to access 'season' as a column
    data_nba_temp = data_nba_panel.reset_index()
    exog_pooled = sm.add_constant(data_nba_temp[xvars])
    exog_pooled.index = data_nba_panel.index
    model_pool_lm = PanelOLS(data_nba_panel['lnrevenue'], exog_pooled).fit(cov_type='robust')
    print("\nPooled OLS (robust SEs):")
    print(model_pool_lm)

    # Pooled OLS with cluster-robust SEs
    model_pool_cluster = PanelOLS(data_nba_panel['lnrevenue'], exog_pooled).fit(cov_type='clustered')
    print("\nPooled OLS (cluster-robust SEs):")
    print(model_pool_cluster)

    # Random Effects with default SEs
    model_re_default = RandomEffects(data_nba_panel['lnrevenue'], exog_pooled).fit()
    print("\nRandom Effects (default SEs):")
    print(model_re_default)

    # Random Effects with robust SEs
    model_re_robust = RandomEffects(data_nba_panel['lnrevenue'], exog_pooled).fit(cov_type='robust')
    print("\nRandom Effects (robust SEs):")
    print(model_re_robust)

    # Fixed Effects with default SEs
    model_fe_default = PanelOLS(data_nba_panel['lnrevenue'], exog_pooled, entity_effects=True).fit()
    print("\nFixed Effects (default SEs):")
    print(model_fe_default)

    # Fixed Effects with cluster-robust SEs
    model_fe_cluster = PanelOLS(data_nba_panel['lnrevenue'], exog_pooled, entity_effects=True).fit(cov_type='clustered')
    print("\nFixed Effects (cluster-robust SEs):")
    print(model_fe_cluster)

    # Summary comparison
    print("\n" + "-" * 70)
    print("Model Comparison Summary")
    print("-" * 70)

    models_summary = pd.DataFrame({
        'Pooled (Robust)': [model_pool_lm.params['wins'], model_pool_lm.std_errors['wins'],
                            model_pool_lm.rsquared, model_pool_lm.nobs],
        'Pooled (Cluster)': [model_pool_cluster.params['wins'], model_pool_cluster.std_errors['wins'],
                             model_pool_cluster.rsquared, model_pool_cluster.nobs],
        'RE (Default)': [model_re_default.params['wins'], model_re_default.std_errors['wins'],
                         model_re_default.rsquared_overall, model_re_default.nobs],
        'RE (Robust)': [model_re_robust.params['wins'], model_re_robust.std_errors['wins'],
                        model_re_robust.rsquared_overall, model_re_robust.nobs],
        'FE (Default)': [model_fe_default.params['wins'], model_fe_default.std_errors['wins'],
                         model_fe_default.rsquared_overall, model_fe_default.nobs],
        'FE (Cluster)': [model_fe_cluster.params['wins'], model_fe_cluster.std_errors['wins'],
                         model_fe_cluster.rsquared_overall, model_fe_cluster.nobs]
    }, index=['Wins Coef', 'Wins SE', 'R²', 'N'])

    print(models_summary.to_string())

    print("\n" + "-" * 70)
    print("Interpretation of Results")
    print("-" * 70)
    print("\nKey findings:")
    print("  - Pooled OLS: Treats all observations as independent")
    print("  - Random Effects: Accounts for team-specific effects (assumed uncorrelated with X)")
    print("  - Fixed Effects: Controls for time-invariant team characteristics")
    print("  - Cluster SEs: Account for within-team correlation")
    print("  - FE coefficient on 'wins' shows within-team effect")

else:
    print("\nNote: Install linearmodels for panel data estimation:")
    print("  pip install linearmodels")

    # Alternative: Use statsmodels with entity dummies for FE
    print("\n" + "-" * 70)
    print("Alternative: Fixed Effects using Entity Dummies")
    print("-" * 70)

    # Create dummy variables for teams (excluding one as reference)
    team_dummies = pd.get_dummies(data_nba['teamid'], prefix='team', drop_first=True)
    data_nba_fe = pd.concat([data_nba, team_dummies], axis=1)

    # Fixed effects model (LSDV)
    formula_fe = 'lnrevenue ~ wins + season + playoff + champ + allstars + lncitypop + ' + \
                 ' + '.join(team_dummies.columns)
    model_fe_lsdv = ols(formula_fe, data=data_nba_fe).fit(cov_type='cluster',
                                                           cov_kwds={'groups': data_nba_fe['teamid']})

    print("\nFixed Effects (LSDV with cluster SEs):")
    # Print only main coefficients
    main_vars = ['Intercept', 'wins', 'season', 'playoff', 'champ', 'allstars', 'lncitypop']
    print(model_fe_lsdv.summary())

# ========== 17.4 CAUSALITY: AN OVERVIEW ==========

print("\n" + "=" * 70)
print("17.4 CAUSALITY: AN OVERVIEW")
print("=" * 70)
print("\nConceptual section - no computation required")
print("Key points:")
print("  - Correlation ≠ Causation")
print("  - Causal inference requires:")
print("    * Randomized experiments, OR")
print("    * Credible identification strategy (IV, DID, RD, etc.)")
print("  - Regression controls for observed confounders only")
print("  - Omitted variable bias: E[u|X] ≠ 0")
print("\nSee Chapter 13 for detailed applications of causal inference methods")

# ========== 17.5 NONLINEAR REGRESSION MODELS ==========

print("\n" + "=" * 70)
print("17.5 NONLINEAR REGRESSION MODELS")
print("=" * 70)

# Logit example
data_earnings = pd.read_stata(GITHUB_DATA_URL + 'AED_EARNINGS_COMPLETE.DTA')

# Create binary indicator
data_earnings['dbigearn'] = (data_earnings['earnings'] > 60000).astype(int)

print("\nBinary dependent variable: High earnings (> $60,000)")
print(f"Proportion with high earnings: {data_earnings['dbigearn'].mean():.4f}")

# Logit model
print("\n" + "-" * 70)
print("Logit Model")
print("-" * 70)

model_logit = logit('dbigearn ~ age + education', data=data_earnings).fit(cov_type='HC1')
print(model_logit.summary())

# Marginal effects
marginal_effects = model_logit.get_margeff()
print("\nMarginal Effects (at means):")
print(marginal_effects.summary())

# Linear Probability Model for comparison
print("\n" + "-" * 70)
print("Linear Probability Model (for comparison)")
print("-" * 70)

model_lpm = ols('dbigearn ~ age + education', data=data_earnings).fit(cov_type='HC1')
print(model_lpm.summary())

print("\n" + "-" * 70)
print("Comparison: Logit Marginal Effects vs LPM")
print("-" * 70)

comparison_logit_lpm = pd.DataFrame({
    'Logit (Marginal Effect)': marginal_effects.margeff,
    'LPM (Coefficient)': model_lpm.params[1:],  # Exclude intercept
    'Difference': marginal_effects.margeff - model_lpm.params[1:].values
})
print(comparison_logit_lpm)

print("\nNote: Logit marginal effects and LPM coefficients are often similar")
print("Logit ensures predicted probabilities are between 0 and 1")

# ========== 17.6 TIME SERIES DATA ==========

print("\n" + "=" * 70)
print("17.6 TIME SERIES DATA")
print("=" * 70)
print("\nConceptual section - no computation required")
print("Key points:")
print("  - Time series data: observations ordered over time")
print("  - Autocorrelation: correlation with past values")
print("  - Stationarity: statistical properties constant over time")
print("  - Spurious regression: correlation without causal relationship")
print("  - Methods: HAC standard errors, ARIMA, VAR, cointegration")

# ========== 17.7 TIME SERIES EXAMPLE: U.S. TREASURY SECURITY INTEREST RATES ==========

print("\n" + "=" * 70)
print("17.7 TIME SERIES EXAMPLE: U.S. TREASURY SECURITY INTEREST RATES")
print("=" * 70)

# Load interest rates data
data_rates = pd.read_stata(GITHUB_DATA_URL + 'AED_INTERESTRATES.DTA')

print("\nInterest Rates Data:")
print(data_rates.describe())

# Display first few observations
print("\nFirst observations:")
print(data_rates.head(10))

# Table 17.5: Summary statistics
print("\n" + "-" * 70)
print("Table 17.5: Summary Statistics")
print("-" * 70)

summary_rates = data_rates[['gs10', 'gs1', 'dgs10', 'dgs1']].describe()
print(summary_rates)

print("\nVariable definitions:")
print("  gs10: 10-year Treasury rate (level)")
print("  gs1: 1-year Treasury rate (level)")
print("  dgs10: Change in 10-year rate")
print("  dgs1: Change in 1-year rate")

# Regression in levels with time trend
print("\n" + "-" * 70)
print("Regression in Levels with Time Trend")
print("-" * 70)

# Create time variable
data_rates['time'] = np.arange(len(data_rates))

model_levels = ols('gs10 ~ gs1 + time', data=data_rates).fit()
print(model_levels.summary())

# Check residual autocorrelation
data_rates['uhatgs10'] = model_levels.resid

# Correlogram
print("\nCorrelogram of residuals:")
acf_resid = acf(data_rates['uhatgs10'].dropna(), nlags=10)
for i in range(11):
    print(f"  Lag {i}: {acf_resid[i]:.6f}")

# Plot correlogram
fig, ax = plt.subplots(figsize=(10, 6))
plot_acf(data_rates['uhatgs10'].dropna(), lags=24, ax=ax, alpha=0.05)
ax.set_title('Correlogram: Residuals from Levels Regression')
plt.tight_layout()
plt.savefig(os.path.join(IMAGES_DIR, 'ch17_correlogram_levels_resid.png'), dpi=300, bbox_inches='tight')
print(f"Saved: {os.path.join(IMAGES_DIR, 'ch17_correlogram_levels_resid.png')}")
plt.close()

# HAC standard errors (Newey-West)
model_levels_hac = ols('gs10 ~ gs1 + time', data=data_rates).fit(cov_type='HAC', cov_kwds={'maxlags': 24})
print("\nRegression in Levels with HAC Standard Errors (24 lags):")
print(model_levels_hac.summary())

# Figure 17.4: Time series plots
print("\n" + "-" * 70)
print("Figure 17.4: Time Series of Interest Rates")
print("-" * 70)

fig, axes = plt.subplots(2, 1, figsize=(12, 8))

# Panel 1: Levels
axes[0].plot(data_rates.index, data_rates['gs10'], label='10-year rate', linewidth=1.5)
axes[0].plot(data_rates.index, data_rates['gs1'], label='1-year rate', linewidth=1.5)
axes[0].set_xlabel('Observation')
axes[0].set_ylabel('Interest Rate (%)')
axes[0].set_title('Interest Rates (Levels)')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Panel 2: Scatter plot
axes[1].scatter(data_rates['gs1'], data_rates['gs10'], alpha=0.5, s=20)
z = np.polyfit(data_rates['gs1'].dropna(), data_rates['gs10'].dropna(), 1)
p = np.poly1d(z)
gs1_range = np.linspace(data_rates['gs1'].min(), data_rates['gs1'].max(), 100)
axes[1].plot(gs1_range, p(gs1_range), 'r-', linewidth=2, label='OLS fit')
axes[1].set_xlabel('1-year rate (%)')
axes[1].set_ylabel('10-year rate (%)')
axes[1].set_title('10-year vs 1-year Rate')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(IMAGES_DIR, 'ch17_fig4_interest_rates_levels.png'), dpi=300, bbox_inches='tight')
print(f"Saved: {os.path.join(IMAGES_DIR, 'ch17_fig4_interest_rates_levels.png')}")
plt.close()

# Table 17.6: Autocorrelations
print("\n" + "-" * 70)
print("Table 17.6: Autocorrelations")
print("-" * 70)

# Rows 1-2: Levels
print("\nLevels:")
acf_gs10 = acf(data_rates['gs10'].dropna(), nlags=5)
acf_gs1 = acf(data_rates['gs1'].dropna(), nlags=5)

print("  gs10:")
for i in range(6):
    print(f"    Lag {i}: {acf_gs10[i]:.6f}")

print("  gs1:")
for i in range(6):
    print(f"    Lag {i}: {acf_gs1[i]:.6f}")

# Rows 3-4: Detrended (residuals from time trend)
print("\nDetrended (residuals from time trend):")
model_gs10_trend = ols('gs10 ~ time', data=data_rates).fit()
model_gs1_trend = ols('gs1 ~ time', data=data_rates).fit()

uhat_gs10_trend = model_gs10_trend.resid
uhat_gs1_trend = model_gs1_trend.resid

acf_gs10_trend = acf(uhat_gs10_trend.dropna(), nlags=5)
acf_gs1_trend = acf(uhat_gs1_trend.dropna(), nlags=5)

print("  gs10 (detrended):")
for i in range(6):
    print(f"    Lag {i}: {acf_gs10_trend[i]:.6f}")

print("  gs1 (detrended):")
for i in range(6):
    print(f"    Lag {i}: {acf_gs1_trend[i]:.6f}")

# Rows 5-6: AR(1) residuals
print("\nAR(1) model residuals:")
model_gs10_ar1 = ols('gs10 ~ gs10.shift(1)', data=data_rates).fit()
model_gs1_ar1 = ols('gs1 ~ gs1.shift(1)', data=data_rates).fit()

uhat_gs10_ar1 = model_gs10_ar1.resid
uhat_gs1_ar1 = model_gs1_ar1.resid

acf_gs10_ar1 = acf(uhat_gs10_ar1.dropna(), nlags=5)
acf_gs1_ar1 = acf(uhat_gs1_ar1.dropna(), nlags=5)

print("  gs10 (AR(1) residuals):")
for i in range(6):
    print(f"    Lag {i}: {acf_gs10_ar1[i]:.6f}")

print("  gs1 (AR(1) residuals):")
for i in range(6):
    print(f"    Lag {i}: {acf_gs1_ar1[i]:.6f}")

# Breusch-Godfrey test for serial correlation
bg_test_gs10 = acorr_breusch_godfrey(model_gs10_ar1, nlags=12)
print(f"\nBreusch-Godfrey test (gs10, 12 lags):")
print(f"  LM statistic: {bg_test_gs10[0]:.4f}")
print(f"  p-value: {bg_test_gs10[1]:.6f}")

# Rows 7-8: Changes (first differences)
print("\nChanges (first differences):")
acf_dgs10 = acf(data_rates['dgs10'].dropna(), nlags=5)
acf_dgs1 = acf(data_rates['dgs1'].dropna(), nlags=5)

print("  dgs10:")
for i in range(6):
    print(f"    Lag {i}: {acf_dgs10[i]:.6f}")

print("  dgs1:")
for i in range(6):
    print(f"    Lag {i}: {acf_dgs1[i]:.6f}")

# Regression in changes
print("\n" + "-" * 70)
print("Regression in Changes")
print("-" * 70)

model_changes = ols('dgs10 ~ dgs1', data=data_rates).fit()
print(model_changes.summary())

# Check residual autocorrelation
uhat_dgs10 = model_changes.resid
acf_dgs10_resid = acf(uhat_dgs10.dropna(), nlags=10)

print("\nCorrelogram of residuals from changes regression:")
for i in range(11):
    print(f"  Lag {i}: {acf_dgs10_resid[i]:.6f}")

# DL(2) model in changes with HAC SEs
print("\n" + "-" * 70)
print("Distributed Lag Model DL(2) in Changes")
print("-" * 70)

# Create lagged variables
data_rates['dgs1_lag1'] = data_rates['dgs1'].shift(1)
data_rates['dgs1_lag2'] = data_rates['dgs1'].shift(2)

model_dl2 = ols('dgs10 ~ dgs1 + dgs1_lag1 + dgs1_lag2', data=data_rates).fit(
    cov_type='HAC', cov_kwds={'maxlags': 3})
print(model_dl2.summary())

# Also show with default SEs for R² and RMSE
model_dl2_default = ols('dgs10 ~ dgs1 + dgs1_lag1 + dgs1_lag2', data=data_rates).fit()
print(f"\nR²: {model_dl2_default.rsquared:.6f}")
print(f"RMSE: {np.sqrt(model_dl2_default.mse_resid):.6f}")

# AR(2) model in changes
print("\n" + "-" * 70)
print("AR(2) Model in Changes")
print("-" * 70)

data_rates['dgs10_lag1'] = data_rates['dgs10'].shift(1)
data_rates['dgs10_lag2'] = data_rates['dgs10'].shift(2)

model_ar2 = ols('dgs10 ~ dgs10_lag1 + dgs10_lag2', data=data_rates).fit()
print(model_ar2.summary())

# Check residuals
uhat_ar2 = model_ar2.resid
acf_ar2_resid = acf(uhat_ar2.dropna(), nlags=12)

print("\nCorrelogram of AR(2) residuals:")
for i in range(min(13, len(acf_ar2_resid))):
    print(f"  Lag {i}: {acf_ar2_resid[i]:.6f}")

# Breusch-Godfrey test
bg_test_ar2 = acorr_breusch_godfrey(model_ar2, nlags=12)
print(f"\nBreusch-Godfrey test (12 lags):")
print(f"  LM statistic: {bg_test_ar2[0]:.4f}")
print(f"  p-value: {bg_test_ar2[1]:.6f}")

# With robust SEs
model_ar2_robust = ols('dgs10 ~ dgs10_lag1 + dgs10_lag2', data=data_rates).fit(cov_type='HC1')
print("\nAR(2) with robust SEs:")
print(model_ar2_robust.summary())

# ADL(2,2) model in changes
print("\n" + "-" * 70)
print("ADL(2,2) Model in Changes")
print("-" * 70)

model_adl22 = ols('dgs10 ~ dgs10_lag1 + dgs10_lag2 + dgs1 + dgs1_lag1 + dgs1_lag2',
                  data=data_rates).fit(cov_type='HC1')
print(model_adl22.summary())

# Check residuals
uhat_adl22 = model_adl22.resid
acf_adl22_resid = acf(uhat_adl22.dropna(), nlags=10)

print("\nCorrelogram of ADL(2,2) residuals:")
for i in range(min(11, len(acf_adl22_resid))):
    print(f"  Lag {i}: {acf_adl22_resid[i]:.6f}")

# Figure 17.5: Changes
print("\n" + "-" * 70)
print("Figure 17.5: Changes in Interest Rates")
print("-" * 70)

fig, axes = plt.subplots(2, 1, figsize=(12, 8))

# Panel 1: Time series of changes
axes[0].plot(data_rates.index, data_rates['dgs10'], label='Δ 10-year rate', linewidth=1)
axes[0].plot(data_rates.index, data_rates['dgs1'], label='Δ 1-year rate', linewidth=1)
axes[0].axhline(y=0, color='k', linestyle='--', linewidth=0.5)
axes[0].set_xlabel('Observation')
axes[0].set_ylabel('Change in Rate (pct points)')
axes[0].set_title('Changes in Interest Rates')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Panel 2: Scatter plot of changes
axes[1].scatter(data_rates['dgs1'], data_rates['dgs10'], alpha=0.5, s=20)
# Add regression line
valid_idx = data_rates[['dgs1', 'dgs10']].dropna().index
z = np.polyfit(data_rates.loc[valid_idx, 'dgs1'], data_rates.loc[valid_idx, 'dgs10'], 1)
p = np.poly1d(z)
dgs1_range = np.linspace(data_rates['dgs1'].min(), data_rates['dgs1'].max(), 100)
axes[1].plot(dgs1_range, p(dgs1_range), 'r-', linewidth=2, label='OLS fit')
axes[1].axhline(y=0, color='k', linestyle='--', linewidth=0.5)
axes[1].axvline(x=0, color='k', linestyle='--', linewidth=0.5)
axes[1].set_xlabel('Δ 1-year rate')
axes[1].set_ylabel('Δ 10-year rate')
axes[1].set_title('Change in 10-year vs 1-year Rate')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(IMAGES_DIR, 'ch17_fig5_interest_rates_changes.png'), dpi=300, bbox_inches='tight')
print(f"Saved: {os.path.join(IMAGES_DIR, 'ch17_fig5_interest_rates_changes.png')}")
plt.close()

# Spurious regression detection
print("\n" + "-" * 70)
print("Spurious Regression Detection")
print("-" * 70)

# Including lags in levels
data_rates['gs10_lag1'] = data_rates['gs10'].shift(1)
data_rates['gs1_lag1'] = data_rates['gs1'].shift(1)

model_levels_lags = ols('gs10 ~ gs1 + gs10_lag1 + gs1_lag1', data=data_rates).fit()
print("\nLevels with lags:")
print(model_levels_lags.summary())

# With HAC standard errors
model_levels_lags_hac = ols('gs10 ~ gs1 + gs10_lag1 + gs1_lag1', data=data_rates).fit(
    cov_type='HAC', cov_kwds={'maxlags': 24})
print("\nLevels with lags (HAC SEs):")
print(model_levels_lags_hac.summary())

# Check residuals
uhat_levels_lags = model_levels_lags.resid
acf_levels_lags = acf(uhat_levels_lags.dropna(), nlags=10)

print("\nCorrelogram of residuals:")
for i in range(min(11, len(acf_levels_lags))):
    print(f"  Lag {i}: {acf_levels_lags[i]:.6f}")

# Impulse response function for ADL(2,2) model
print("\n" + "-" * 70)
print("Impulse Response Function for ADL(2,2) Model")
print("-" * 70)

# Create forward variables
for h in range(5):
    data_rates[f'dgs10_fwd{h}'] = data_rates['dgs10'].shift(-h)

# Estimate impulse responses
impulse_results = []

for h in range(5):
    if h == 0:
        # Contemporaneous
        model_impulse = ols('dgs10 ~ dgs10_lag1 + dgs10_lag2 + dgs1 + dgs1_lag1 + dgs1_lag2',
                           data=data_rates).fit(cov_type='HAC', cov_kwds={'maxlags': 4})
    else:
        # h periods ahead
        model_impulse = ols(f'dgs10_fwd{h} ~ dgs10_lag1 + dgs10_lag2 + dgs1 + dgs1_lag1 + dgs1_lag2',
                           data=data_rates).fit(cov_type='HAC', cov_kwds={'maxlags': h})

    impulse_coef = model_impulse.params['dgs1']
    impulse_se = model_impulse.bse['dgs1']
    impulse_t = model_impulse.tvalues['dgs1']

    impulse_results.append({
        'Horizon': h,
        'Impulse': impulse_coef,
        'SE': impulse_se,
        't-stat': impulse_t
    })

    print(f"\nHorizon {h}:")
    print(f"  Impulse response: {impulse_coef:.6f}")
    print(f"  Standard error: {impulse_se:.6f}")
    print(f"  t-statistic: {impulse_t:.4f}")

impulse_df = pd.DataFrame(impulse_results)

print("\n" + "-" * 70)
print("Summary: Impulse Response Function")
print("-" * 70)
print(impulse_df.to_string(index=False))

# Plot impulse response
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(impulse_df['Horizon'], impulse_df['Impulse'], 'o-', linewidth=2, markersize=8, label='Impulse')
ax.fill_between(impulse_df['Horizon'],
                impulse_df['Impulse'] - 1.96 * impulse_df['SE'],
                impulse_df['Impulse'] + 1.96 * impulse_df['SE'],
                alpha=0.3, label='95% CI')
ax.axhline(y=0, color='k', linestyle='--', linewidth=0.5)
ax.set_xlabel('Horizon (periods ahead)')
ax.set_ylabel('Response of Δ 10-year rate')
ax.set_title('Impulse Response: Effect of 1 pct point increase in Δ 1-year rate')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(IMAGES_DIR, 'ch17_impulse_response.png'), dpi=300, bbox_inches='tight')
print(f"\nSaved: {os.path.join(IMAGES_DIR, 'ch17_impulse_response.png')}")
plt.close()

# ========== SUMMARY ==========

print("\n" + "=" * 70)
print("CHAPTER 17 SUMMARY")
print("=" * 70)
print("\nKey topics covered:")
print("  1. Panel data structure and estimation methods")
print("     - Pooled OLS, Random Effects, Fixed Effects")
print("     - Different standard error adjustments (robust, cluster)")
print("  2. Within and between variation in panel data")
print("  3. Nonlinear models: Logit vs Linear Probability Model")
print("  4. Time series data and autocorrelation")
print("  5. Spurious regression and differencing")
print("  6. Autoregressive (AR) and distributed lag (DL) models")
print("  7. ADL models and impulse response functions")
print("  8. HAC (Newey-West) standard errors for time series")
print("\nKey findings:")
print("  - NBA: Wins significantly increase team revenue (panel data)")
print("  - Interest rates: Strong autocorrelation requires special treatment")
print("  - First differencing removes trends and reduces spurious correlation")
print("\nAll figures saved to:", IMAGES_DIR)

print("\n" + "=" * 70)
print("END OF CHAPTER 17")
print("=" * 70)
