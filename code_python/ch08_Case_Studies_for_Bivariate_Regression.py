# %%
"""
ch08_Case_Studies_for_Bivariate_Regression.py - January 2026 for Python

Chapter 8: CASE STUDIES FOR BIVARIATE REGRESSION

To run you need files:
  AED_HEALTH2009.DTA
  AED_CAPM.DTA
  AED_GDPUNEMPLOY.DTA
in the data/ directory

Sections covered:
  8.1 HEALTH OUTCOMES ACROSS COUNTRIES
  8.2 HEALTH EXPENDITURES ACROSS COUNTRIES
  8.3 CAPM MODEL
  8.4 OUTPUT AND UNEMPLOYMENT IN THE U.S.
"""

# %% =========== SETUP ==========

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from statsmodels.formula.api import ols
from scipy import stats
import random
import os

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
print("CHAPTER 8: CASE STUDIES FOR BIVARIATE REGRESSION")
print("=" * 70)

# %% =========== 8.1 HEALTH OUTCOMES ACROSS COUNTRIES ==========

print("\n" + "=" * 70)
print("8.1 HEALTH OUTCOMES ACROSS COUNTRIES")
print("=" * 70)

# Read in the health data
data_health = pd.read_stata(GITHUB_DATA_URL + 'AED_HEALTH2009.DTA')

# %% Explore data structure

print("\nData summary:")
data_summary = data_health.describe()

# %% Calculate statistics
print(data_summary)
print("\nFirst few observations:")
print(data_health.head())
data_summary.to_csv(os.path.join(TABLES_DIR, 'ch08_health_descriptive_stats.csv'))
print(f"Table saved to: {os.path.join(TABLES_DIR, 'ch08_health_descriptive_stats.csv')}")

# Table 8.1 - Key variables
print("\n" + "-" * 70)
print("Table 8.1: Health Variables Summary")
print("-" * 70)
table81_vars = ['hlthpc', 'lifeexp', 'infmort']
print(data_health[table81_vars].describe())

# %% Calculate statistics

# Life Expectancy Analysis
print("\n" + "-" * 70)
print("Life Expectancy Regression")
print("-" * 70)


# %% Estimate regression model

model_lifeexp = ols('lifeexp ~ hlthpc', data=data_health).fit()

# %% Display regression results

print(model_lifeexp.summary())
# Save coefficients
coef_table = pd.DataFrame({
    'coefficient': model_lifeexp.params,
    'std_err': model_lifeexp.bse,
    't_value': model_lifeexp.tvalues,
    'p_value': model_lifeexp.pvalues
})
coef_table.to_csv(os.path.join(TABLES_DIR, 'ch08_lifeexp_regression_coefficients.csv'))
print(f"Coefficients saved to: {os.path.join(TABLES_DIR, 'ch08_lifeexp_regression_coefficients.csv')}")

# Robust standard errors
model_lifeexp_robust = model_lifeexp.get_robustcov_results(cov_type='HC1')
print("\n" + "-" * 70)
print("Life Expectancy Regression (Robust SE):")
print("-" * 70)

# %% Display regression results

print(model_lifeexp_robust.summary())

# Figure 8.1 Panel A - Life Expectancy
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(data_health['hlthpc'], data_health['lifeexp'], alpha=0.6, s=50,
           color='black', label='Actual')
ax.plot(data_health['hlthpc'], model_lifeexp.fittedvalues, color='blue',
        linewidth=2, label='Fitted')
ax.set_xlabel('Health Spending per capita (in $1000s)', fontsize=12)
ax.set_ylabel('Life Expectancy (in years)', fontsize=12)
# ax.set_title('Figure 8.1 Panel A: Life Expectancy vs Health Spending',
#              fontsize=14, fontweight='bold')  # Removed: redundant with LaTeX caption
ax.legend()
ax.grid(True, alpha=0.3)

output_file = os.path.join(IMAGES_DIR, 'ch08_fig1a_life_expectancy.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\nFigure saved to: {output_file}")
plt.close()

# Infant Mortality Analysis
print("\n" + "-" * 70)
print("Infant Mortality Regression")
print("-" * 70)


# %% Estimate regression model

model_infmort = ols('infmort ~ hlthpc', data=data_health).fit()

# %% Display regression results

print(model_infmort.summary())

# Robust standard errors
model_infmort_robust = model_infmort.get_robustcov_results(cov_type='HC1')
print("\n" + "-" * 70)
print("Infant Mortality Regression (Robust SE):")
print("-" * 70)

# %% Display regression results

print(model_infmort_robust.summary())

# Figure 8.1 Panel B - Infant Mortality
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(data_health['hlthpc'], data_health['infmort'], alpha=0.6, s=50,
           color='black', label='Actual')
ax.plot(data_health['hlthpc'], model_infmort.fittedvalues, color='blue',
        linewidth=2, label='Fitted')
ax.set_xlabel('Health Spending per capita (in $1000s)', fontsize=12)
ax.set_ylabel('Infant Mortality per 100 births', fontsize=12)
# ax.set_title('Figure 8.1 Panel B: Infant Mortality vs Health Spending',
#              fontsize=14, fontweight='bold')  # Removed: redundant with LaTeX caption
ax.legend()
ax.grid(True, alpha=0.3)

output_file = os.path.join(IMAGES_DIR, 'ch08_fig1b_infant_mortality.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"Figure saved to: {output_file}")
plt.close()

# %% Continue analysis

# %% =========== 8.2 HEALTH EXPENDITURES ACROSS COUNTRIES ==========

print("\n" + "=" * 70)
print("8.2 HEALTH EXPENDITURES ACROSS COUNTRIES")
print("=" * 70)

# Table 8.2
print("\n" + "-" * 70)
print("Table 8.2: GDP and Health Spending Summary")
print("-" * 70)
table82_vars = ['gdppc', 'hlthpc']
print(data_health[table82_vars].describe())

# %% Calculate statistics

# Health expenditure regression
print("\n" + "-" * 70)
print("Health Expenditure Regression")
print("-" * 70)


# %% Estimate regression model

model_hlthpc = ols('hlthpc ~ gdppc', data=data_health).fit()

# %% Display regression results

print(model_hlthpc.summary())

# Robust standard errors
model_hlthpc_robust = model_hlthpc.get_robustcov_results(cov_type='HC1')
print("\n" + "-" * 70)
print("Health Expenditure Regression (Robust SE):")
print("-" * 70)

# %% Display regression results

print(model_hlthpc_robust.summary())

# Figure 8.2 Panel A - All countries
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(data_health['gdppc'], data_health['hlthpc'], alpha=0.6, s=50,
           color='black', label='Actual')
ax.plot(data_health['gdppc'], model_hlthpc.fittedvalues, color='blue',
        linewidth=2, label='Fitted')
ax.set_xlabel('GDP per capita (in $1000s)', fontsize=12)
ax.set_ylabel('Health Spending per capita (in $1000s)', fontsize=12)
# ax.set_title('Figure 8.2 Panel A: Health Spending vs GDP (All Countries)  # Removed: redundant with LaTeX caption',
#              fontsize=14, fontweight='bold')  # Removed: redundant with LaTeX caption
ax.legend()
ax.grid(True, alpha=0.3)

output_file = os.path.join(IMAGES_DIR, 'ch08_fig2a_health_gdp_all.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\nFigure saved to: {output_file}")
plt.close()

# Drop USA and Luxembourg
print("\n" + "-" * 70)
print("Regression excluding USA and Luxembourg")
print("-" * 70)

data_health_subset = data_health[(data_health['code'] != 'LUX') &
                                  (data_health['code'] != 'USA')]

print(f"Original sample size: {len(data_health)}")
print(f"Subset sample size: {len(data_health_subset)}")


# %% Estimate regression model

model_hlthpc_subset = ols('hlthpc ~ gdppc', data=data_health_subset).fit()

# %% Display regression results

print(model_hlthpc_subset.summary())

# Figure 8.2 Panel B - Excluding USA and Luxembourg
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(data_health_subset['gdppc'], data_health_subset['hlthpc'], alpha=0.6, s=50,
           color='black', label='Actual')
ax.plot(data_health_subset['gdppc'], model_hlthpc_subset.fittedvalues, color='blue',
        linewidth=2, label='Fitted')
ax.set_xlabel('GDP per capita (in $1000s)', fontsize=12)
ax.set_ylabel('Health Spending per capita (in $1000s)', fontsize=12)
# ax.set_title('Figure 8.2 Panel B: Health Spending vs GDP (Excluding USA & Luxembourg)  # Removed: redundant with LaTeX caption',
#              fontsize=14, fontweight='bold')  # Removed: redundant with LaTeX caption
ax.legend()
ax.grid(True, alpha=0.3)

output_file = os.path.join(IMAGES_DIR, 'ch08_fig2b_health_gdp_subset.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"Figure saved to: {output_file}")
plt.close()

# %% Continue analysis

# %% =========== 8.3 CAPM MODEL ==========

print("\n" + "=" * 70)
print("8.3 CAPM MODEL")
print("=" * 70)

# Read in the CAPM data
data_capm = pd.read_stata(GITHUB_DATA_URL + 'AED_CAPM.DTA')

# %% Explore data structure

print("\nData summary:")
print(data_capm.describe())
print("\nFirst few observations:")
print(data_capm.head())

# Table 8.3
print("\n" + "-" * 70)
print("Table 8.3: CAPM Variables Summary")
print("-" * 70)
table83_vars = ['rm', 'rf', 'rko', 'rtgt', 'rwmt', 'rm_rf',
                'rko_rf', 'rtgt_rf', 'rwmt_rf']
print(data_capm[table83_vars].describe())

# %% Calculate statistics

# Figure 8.3 Panel A - Time series plot (last 20% of data)
# Take the last 20% of observations
cutoff_index = int(len(data_capm) * 0.8)
data_capm_recent = data_capm.iloc[cutoff_index:]

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(data_capm_recent['date'], data_capm_recent['rko_rf'],
        linewidth=1.5, label='Coca Cola excess return', color='blue')
ax.plot(data_capm_recent['date'], data_capm_recent['rm_rf'],
        linewidth=1.5, linestyle='--', label='Market excess return', color='red')
ax.set_xlabel('Month', fontsize=12)
ax.set_ylabel('Excess returns', fontsize=12)
# ax.set_title('Figure 8.3 Panel A: Excess Returns Over Time',
#              fontsize=14, fontweight='bold')  # Removed: redundant with LaTeX caption
ax.legend()
ax.grid(True, alpha=0.3)

output_file = os.path.join(IMAGES_DIR, 'ch08_fig3a_capm_timeseries.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\nFigure saved to: {output_file}")
plt.close()

# CAPM regression
print("\n" + "-" * 70)
print("CAPM Regression: Coca Cola")
print("-" * 70)


# %% Estimate regression model

model_capm = ols('rko_rf ~ rm_rf', data=data_capm).fit()

# %% Display regression results

print(model_capm.summary())

# Robust standard errors
model_capm_robust = model_capm.get_robustcov_results(cov_type='HC1')
print("\n" + "-" * 70)
print("CAPM Regression (Robust SE):")
print("-" * 70)

# %% Display regression results

print(model_capm_robust.summary())

print(f"\nInterpretation:")
print(f"  Beta coefficient: {model_capm.params['rm_rf']:.4f}")
print(f"  This means Coca Cola stock has {'higher' if model_capm.params['rm_rf'] > 1 else 'lower'} systematic risk than the market")

# Figure 8.3 Panel B - Scatter plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(data_capm['rm_rf'], data_capm['rko_rf'], alpha=0.4, s=30,
           color='black', label='Actual')
ax.plot(data_capm['rm_rf'], model_capm.fittedvalues, color='blue',
        linewidth=2, label='Fitted')
ax.set_xlabel('Market excess return', fontsize=12)
ax.set_ylabel('Coca Cola excess return', fontsize=12)
# ax.set_title('Figure 8.3 Panel B: Coca Cola vs Market Excess Returns',
#              fontsize=14, fontweight='bold')  # Removed: redundant with LaTeX caption
ax.legend()
ax.grid(True, alpha=0.3)

output_file = os.path.join(IMAGES_DIR, 'ch08_fig3b_capm_scatter.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"Figure saved to: {output_file}")
plt.close()

# %% Continue analysis

# %% =========== 8.4 OUTPUT AND UNEMPLOYMENT IN THE U.S. ==========

print("\n" + "=" * 70)
print("8.4 OUTPUT AND UNEMPLOYMENT IN THE U.S.")
print("=" * 70)

# Read in the GDP-Unemployment data
data_gdp = pd.read_stata(GITHUB_DATA_URL + 'AED_GDPUNEMPLOY.DTA')

# %% Explore data structure

print("\nData summary:")
print(data_gdp.describe())
print("\nFirst few observations:")
print(data_gdp.head())

# Table 8.4
print("\n" + "-" * 70)
print("Table 8.4: GDP Growth and Unemployment Change Summary")
print("-" * 70)
table84_vars = ['rgdpgrowth', 'uratechange']
print(data_gdp[table84_vars].describe())

# %% Calculate statistics

# Okun's Law regression
print("\n" + "-" * 70)
print("Okun's Law Regression")
print("-" * 70)


# %% Estimate regression model

model_okun = ols('rgdpgrowth ~ uratechange', data=data_gdp).fit()

# %% Display regression results

print(model_okun.summary())

# Robust standard errors
model_okun_robust = model_okun.get_robustcov_results(cov_type='HC1')
print("\n" + "-" * 70)
print("Okun's Law Regression (Robust SE):")
print("-" * 70)

# %% Display regression results

print(model_okun_robust.summary())

print(f"\nInterpretation (Okun's Law):")
print(f"  Coefficient on unemployment change: {model_okun.params['uratechange']:.4f}")
print(f"  A 1 percentage point increase in unemployment is associated with")
print(f"  a {abs(model_okun.params['uratechange']):.2f} percentage point decrease in real GDP growth")

# Figure 8.4 Panel A - Scatter plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(data_gdp['uratechange'], data_gdp['rgdpgrowth'], alpha=0.6, s=50,
           color='black', label='Actual')
ax.plot(data_gdp['uratechange'], model_okun.fittedvalues, color='blue',
        linewidth=2, label='Fitted')
ax.set_xlabel('Change in unemployment rate', fontsize=12)
ax.set_ylabel('Percentage change in real GDP', fontsize=12)
# ax.set_title('Figure 8.4 Panel A: Okun\'s Law - GDP Growth vs Unemployment Change',
#              fontsize=14, fontweight='bold')  # Removed: redundant with LaTeX caption
ax.legend()
ax.grid(True, alpha=0.3)

output_file = os.path.join(IMAGES_DIR, 'ch08_fig4a_okun_scatter.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\nFigure saved to: {output_file}")
plt.close()

# Get predictions for time series plot
predictions = model_okun.fittedvalues

# Figure 8.4 Panel B - Time series plot
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(data_gdp['year'], data_gdp['rgdpgrowth'], linewidth=1.5,
        label='Actual', color='black')
ax.plot(data_gdp['year'], predictions, linewidth=1.5, linestyle='--',
        label='Fitted', color='blue')
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Percentage change in real GDP', fontsize=12)
# ax.set_title('Figure 8.4 Panel B: Real GDP Change Over Time',
#              fontsize=14, fontweight='bold')  # Removed: redundant with LaTeX caption
ax.legend()
ax.grid(True, alpha=0.3)

output_file = os.path.join(IMAGES_DIR, 'ch08_fig4b_okun_timeseries.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"Figure saved to: {output_file}")
plt.close()

# %% Continue analysis

# %% =========== SUMMARY ==========

print("\n" + "=" * 70)
print("CHAPTER 8 ANALYSIS COMPLETE")
print("=" * 70)
print("\nKey case studies demonstrated:")
print("  - Health outcomes and expenditures across countries")
print("  - CAPM model for stock returns")
print("  - Okun's Law relating output and unemployment")
print("  - Use of robust standard errors in all applications")
print("\nAll figures saved to:", IMAGES_DIR)
