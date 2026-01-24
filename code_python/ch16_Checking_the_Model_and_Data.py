"""
ch16_Checking_the_Model_and_Data.py - January 2026 for Python

Chapter 16: CHECKING THE MODEL AND DATA

To run you need files:
  AED_EARNINGS_COMPLETE.DTA
  AED_DEMOCRACY.DTA
in the data/ directory

Sections covered:
  16.1 MULTICOLLINEAR DATA
  16.2 FAILURE OF MODEL ASSUMPTIONS
  16.3 INCORRECT POPULATION MODEL
  16.4 REGRESSORS CORRELATED WITH ERRORS
  16.5 HETEROSKEDASTIC ERRORS
  16.6 CORRELATED ERRORS
  16.7 EXAMPLE: DEMOCRACY AND GROWTH
  16.8 DIAGNOSTICS
"""

# ========== SETUP ==========

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.outliers_influence import variance_inflation_factor, OLSInfluence
from statsmodels.stats.diagnostic import het_white, acorr_ljungbox
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.regression.linear_model import OLS
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
print("CHAPTER 16: CHECKING THE MODEL AND DATA")
print("=" * 70)

# ========== DATA DESCRIPTION ==========

# (1) Annual Earnings for 842 male and female full-time workers
#     aged 25-65 years old in 2010
# (2) Democracy and growth data

# ========== 16.1 MULTICOLLINEARITY ==========

print("\n" + "=" * 70)
print("16.1 MULTICOLLINEARITY")
print("=" * 70)

# Read in the Stata data set
data_earnings = pd.read_stata(GITHUB_DATA_URL + 'AED_EARNINGS_COMPLETE.DTA')

print("\nData structure:")
print(data_earnings.info())

print("\nData summary:")
data_summary = data_earnings.describe()
print(data_summary)
data_summary.to_csv(os.path.join(TABLES_DIR, 'ch16_earnings_descriptive_stats.csv'))
print(f"Table saved to: {os.path.join(TABLES_DIR, 'ch16_earnings_descriptive_stats.csv')}")

# Base regression
print("\n" + "-" * 70)
print("Base Model: earnings ~ age + education")
print("-" * 70)
ols_base = ols('earnings ~ age + education', data=data_earnings).fit(cov_type='HC1')
print(ols_base.summary())

# Add interaction variable
print("\n" + "-" * 70)
print("Collinear Model: earnings ~ age + education + agebyeduc")
print("-" * 70)
ols_collinear = ols('earnings ~ age + education + agebyeduc', data=data_earnings).fit(cov_type='HC1')
print(ols_collinear.summary())

# Joint hypothesis tests
print("\n" + "-" * 70)
print("Joint Hypothesis Test: H0: age = 0 and agebyeduc = 0")
print("-" * 70)
hypotheses = '(age = 0, agebyeduc = 0)'
f_test = ols_collinear.wald_test(hypotheses, use_f=True)
print(f_test)

print("\n" + "-" * 70)
print("Joint Hypothesis Test: H0: education = 0 and agebyeduc = 0")
print("-" * 70)
hypotheses = '(education = 0, agebyeduc = 0)'
f_test = ols_collinear.wald_test(hypotheses, use_f=True)
print(f_test)

# The regressors are highly correlated
print("\n" + "-" * 70)
print("Correlation Matrix of Regressors")
print("-" * 70)
corr_matrix = data_earnings[['age', 'education', 'agebyeduc']].corr()
print(corr_matrix)
corr_matrix.to_csv(os.path.join(TABLES_DIR, 'ch16_correlation_matrix.csv'))
print(f"Table saved to: {os.path.join(TABLES_DIR, 'ch16_correlation_matrix.csv')}")

# Auxiliary regression
print("\n" + "-" * 70)
print("Auxiliary Regression: agebyeduc ~ age + education")
print("-" * 70)
ols_check = ols('agebyeduc ~ age + education', data=data_earnings).fit()
print(ols_check.summary())
print(f"\nR-squared from auxiliary regression: {ols_check.rsquared:.4f}")
print("High R² indicates strong multicollinearity")

# Calculate VIF
print("\n" + "-" * 70)
print("Variance Inflation Factors (VIF)")
print("-" * 70)
X = data_earnings[['age', 'education', 'agebyeduc']]
X = sm.add_constant(X)
vif_data = pd.DataFrame()
vif_data["Variable"] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
print(vif_data)
print("\nNote: VIF > 10 indicates serious multicollinearity")
vif_data.to_csv(os.path.join(TABLES_DIR, 'ch16_vif_table.csv'), index=False)
print(f"Table saved to: {os.path.join(TABLES_DIR, 'ch16_vif_table.csv')}")

# ========== 16.2 MODEL ASSUMPTIONS REVISITED ==========

print("\n" + "=" * 70)
print("16.2 MODEL ASSUMPTIONS REVISITED")
print("=" * 70)
print("\nKey OLS assumptions:")
print("  1. Linear in parameters: E[y|x] = x'β")
print("  2. Random sample from population")
print("  3. No perfect collinearity")
print("  4. Zero conditional mean: E[u|x] = 0")
print("  5. Homoskedasticity: Var(u|x) = σ²")
print("  6. Normality of errors (for exact inference)")

# ========== 16.3 INCORRECT POPULATION MODEL ==========

print("\n" + "=" * 70)
print("16.3 INCORRECT POPULATION MODEL")
print("=" * 70)
print("\nIssues with model specification:")
print("  - Omitted variable bias")
print("  - Incorrect functional form")
print("  - Measurement error in variables")

# ========== 16.4 REGRESSORS CORRELATED WITH ERRORS ==========

print("\n" + "=" * 70)
print("16.4 REGRESSORS CORRELATED WITH ERRORS")
print("=" * 70)
print("\nCauses of endogeneity:")
print("  - Omitted variables")
print("  - Measurement error")
print("  - Simultaneity")
print("  - Sample selection")

# ========== 16.5 HETEROSKEDASTIC ERRORS ==========

print("\n" + "=" * 70)
print("16.5 HETEROSKEDASTIC ERRORS")
print("=" * 70)
print("\nConsequences of heteroskedasticity:")
print("  - OLS estimators remain unbiased and consistent")
print("  - Standard errors are incorrect")
print("  - Use robust (heteroskedasticity-consistent) standard errors")

# ========== 16.6 CORRELATED ERRORS ==========

print("\n" + "=" * 70)
print("16.6 CORRELATED ERRORS")
print("=" * 70)

# Generate time series data with autocorrelated errors
print("\n" + "-" * 70)
print("Simulation: Time Series with Autocorrelated Errors")
print("-" * 70)

n = 10000
np.random.seed(10101)

# Generate e_t ~ N(0,1)
e = np.random.normal(0, 1, n)

# Autocorrelated errors: u_t = 0.8*u_{t-1} + e_t
u = np.zeros(n)
u[0] = 0
for t in range(1, n):
    u[t] = 0.8 * u[t-1] + e[t]

# Autocorrelated regressor: x_t = 0.8*x_{t-1} + v_t
v = np.random.normal(0, 1, n)
x = np.zeros(n)
x[0] = 0
for t in range(1, n):
    x[t] = 0.8 * x[t-1] + v[t]

# y_1t with serially correlated error
y1 = 1 + 2*x + u

# y_2t is serially correlated but with i.i.d. error
# E[y2] = 1/(1-0.6) = 2.5
y2 = np.zeros(n)
y2[0] = 2.5
for t in range(1, n):
    y2[t] = 1 + 0.6*y2[t-1] + 2*x[t] + e[t]

# y_3t is serially correlated and the error is serially correlated
y3 = np.zeros(n)
y3[0] = 2.5
for t in range(1, n):
    y3[t] = 1 + 0.6*y3[t-1] + 2*x[t] + u[t]

# Create DataFrame
ts_data = pd.DataFrame({
    'e': e,
    'u': u,
    'x': x,
    'y1': y1,
    'y2': y2,
    'y3': y3
})

# Create lagged variables
ts_data['y2lag'] = ts_data['y2'].shift(1)
ts_data['y3lag'] = ts_data['y3'].shift(1)

print("\nTime series data summary:")
print(ts_data.describe())

# Compute autocorrelations
print("\n" + "-" * 70)
print("Autocorrelations (first 10 lags)")
print("-" * 70)

from statsmodels.tsa.stattools import acf

for var in ['e', 'u', 'y1', 'y2', 'y3']:
    acf_vals = acf(ts_data[var], nlags=10, fft=False)
    print(f"\n{var}:")
    for lag, val in enumerate(acf_vals[:11]):
        print(f"  Lag {lag}: {val:.4f}")

# Regressions with different standard error types
print("\n" + "-" * 70)
print("Model 1: y1 ~ x (serially correlated error)")
print("-" * 70)

ols_y1 = ols('y1 ~ x', data=ts_data).fit()
u1hat = ols_y1.resid

# Check residual autocorrelation
acf_u1 = acf(u1hat, nlags=10, fft=False)
print("\nResidual autocorrelations:")
for lag, val in enumerate(acf_u1[:11]):
    print(f"  Lag {lag}: {val:.4f}")

# Default standard errors
print("\nDefault OLS standard errors:")
print(ols_y1.summary())

# Heteroskedasticity-robust standard errors
print("\nHeteroskedasticity-robust (HC1) standard errors:")
ols_y1_robust = ols('y1 ~ x', data=ts_data).fit(cov_type='HC1')
print(ols_y1_robust.summary())

# HAC-robust (Newey-West) standard errors
print("\nHAC-robust (Newey-West) standard errors:")
ols_y1_hac = ols('y1 ~ x', data=ts_data).fit(cov_type='HAC', cov_kwds={'maxlags': 10})
print(ols_y1_hac.summary())

# Model 2: y2 ~ y2lag + x
print("\n" + "-" * 70)
print("Model 2: y2 ~ y2lag + x (serially correlated but i.i.d. error)")
print("-" * 70)

ols_y2 = ols('y2 ~ y2lag + x', data=ts_data.dropna()).fit()
u2hat = ols_y2.resid

# Check residual autocorrelation
acf_u2 = acf(u2hat, nlags=10, fft=False)
print("\nResidual autocorrelations:")
for lag, val in enumerate(acf_u2[:11]):
    print(f"  Lag {lag}: {val:.4f}")

# Robust standard errors
print("\nHeteroskedasticity-robust (HC1) standard errors:")
ols_y2_robust = ols('y2 ~ y2lag + x', data=ts_data.dropna()).fit(cov_type='HC1')
print(ols_y2_robust.summary())

# HAC-robust standard errors
print("\nHAC-robust (Newey-West) standard errors:")
ols_y2_hac = ols('y2 ~ y2lag + x', data=ts_data.dropna()).fit(cov_type='HAC', cov_kwds={'maxlags': 10})
print(ols_y2_hac.summary())

# Model 3: y3 ~ y3lag + x
print("\n" + "-" * 70)
print("Model 3: y3 ~ y3lag + x (both y and u are serially correlated)")
print("-" * 70)

ols_y3 = ols('y3 ~ y3lag + x', data=ts_data.dropna()).fit()
u3hat = ols_y3.resid

# Check residual autocorrelation
acf_u3 = acf(u3hat, nlags=10, fft=False)
print("\nResidual autocorrelations:")
for lag, val in enumerate(acf_u3[:11]):
    print(f"  Lag {lag}: {val:.4f}")

# Robust standard errors
print("\nHeteroskedasticity-robust (HC1) standard errors:")
ols_y3_robust = ols('y3 ~ y3lag + x', data=ts_data.dropna()).fit(cov_type='HC1')
print(ols_y3_robust.summary())

# HAC-robust standard errors
print("\nHAC-robust (Newey-West) standard errors:")
ols_y3_hac = ols('y3 ~ y3lag + x', data=ts_data.dropna()).fit(cov_type='HAC', cov_kwds={'maxlags': 10})
print(ols_y3_hac.summary())

# ========== 16.7 EXAMPLE: DEMOCRACY AND GROWTH ==========

print("\n" + "=" * 70)
print("16.7 EXAMPLE: DEMOCRACY AND GROWTH")
print("=" * 70)

# Read in democracy data
data_democracy = pd.read_stata(GITHUB_DATA_URL + 'AED_DEMOCRACY.DTA')

print("\nData structure:")
print(data_democracy.info())

print("\nData summary:")
print(data_democracy.describe())

# Table 16.1
print("\n" + "-" * 70)
print("Table 16.1: Summary Statistics")
print("-" * 70)
table161vars = ["democracy", "growth", "constraint", "indcent", "catholic",
                "muslim", "protestant", "other"]
print(data_democracy[table161vars].describe())

# Correlation matrix
print("\n" + "-" * 70)
print("Correlation Matrix")
print("-" * 70)
corr_vars = ["democracy", "growth", "constraint", "indcent", "catholic", "muslim", "protestant", "other"]
print(data_democracy[corr_vars].corr())

# Bivariate regression
print("\n" + "-" * 70)
print("Bivariate Regression: democracy ~ growth")
print("-" * 70)
ols_bivariate = ols('democracy ~ growth', data=data_democracy).fit(cov_type='HC1')
print(ols_bivariate.summary())

# Figure 16.1: Democracy and Growth
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(data_democracy['growth'], data_democracy['democracy'],
           alpha=0.6, s=50, color='black')
ax.plot(data_democracy['growth'], ols_bivariate.fittedvalues,
        color='blue', linewidth=2, label='Regression line')
ax.set_xlabel('Change in Log GDP per capita', fontsize=12)
ax.set_ylabel('Change in Democracy', fontsize=12)
ax.set_title('Figure 16.1: Democracy and Growth, 1500-2000',
             fontsize=14, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)

output_file = os.path.join(IMAGES_DIR, 'ch16_fig1_democracy_growth.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\nFigure 16.1 saved to: {output_file}")
plt.close()

# Multiple regression
print("\n" + "-" * 70)
print("Multiple Regression:")
print("democracy ~ growth + constraint + indcent + catholic + muslim + protestant")
print("-" * 70)
ols_multiple = ols('democracy ~ growth + constraint + indcent + catholic + muslim + protestant',
                   data=data_democracy).fit(cov_type='HC1')
print(ols_multiple.summary())

# ========== 16.8 DIAGNOSTICS ==========

print("\n" + "=" * 70)
print("16.8 DIAGNOSTICS")
print("=" * 70)

yhat = ols_multiple.fittedvalues
uhat = ols_multiple.resid

# Figure 16.2: Actual vs. Fitted and Residual vs. Fitted
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Panel A: Actual vs. Fitted
axes[0].scatter(yhat, data_democracy['democracy'], alpha=0.6, s=50, color='black')
axes[0].plot([yhat.min(), yhat.max()], [yhat.min(), yhat.max()],
             'b-', linewidth=2, label='45-degree line')

# Add lowess smooth
from statsmodels.nonparametric.smoothers_lowess import lowess
lowess_result = lowess(data_democracy['democracy'], yhat, frac=0.3)
axes[0].plot(lowess_result[:, 0], lowess_result[:, 1],
             'r--', linewidth=2, label='Lowess smooth')

axes[0].set_xlabel('Predicted value of y', fontsize=11)
axes[0].set_ylabel('Actual value of y', fontsize=11)
axes[0].set_title('Panel A: Actual vs. Fitted', fontsize=12, fontweight='bold')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Panel B: Residual vs. Fitted
axes[1].scatter(yhat, uhat, alpha=0.6, s=50, color='black')
axes[1].axhline(y=0, color='blue', linewidth=2, linestyle='-')

# Add lowess smooth
lowess_result = lowess(uhat, yhat, frac=0.3)
axes[1].plot(lowess_result[:, 0], lowess_result[:, 1],
             'r--', linewidth=2, label='Lowess smooth')

axes[1].set_xlabel('Predicted value of y', fontsize=11)
axes[1].set_ylabel('OLS Residual', fontsize=11)
axes[1].set_title('Panel B: Residual vs. Fitted', fontsize=12, fontweight='bold')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.suptitle('Figure 16.2: Diagnostic Plots', fontsize=14, fontweight='bold', y=1.0)
output_file = os.path.join(IMAGES_DIR, 'ch16_fig2_diagnostics_basic.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\nFigure 16.2 saved to: {output_file}")
plt.close()

# Figure 16.3: Diagnostic plots for growth regressor
print("\n" + "-" * 70)
print("Figure 16.3: Diagnostic Plots for Growth Regressor")
print("-" * 70)

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Panel A: Residual vs. Regressor
axes[0].scatter(data_democracy['growth'], uhat, alpha=0.6, s=50, color='black')
axes[0].axhline(y=0, color='blue', linewidth=2, linestyle='-')

# Add lowess smooth
lowess_result = lowess(uhat, data_democracy['growth'], frac=0.3)
axes[0].plot(lowess_result[:, 0], lowess_result[:, 1],
             'r--', linewidth=2, label='Lowess smooth')

axes[0].set_xlabel('Growth regressor', fontsize=11)
axes[0].set_ylabel('Democracy Residual', fontsize=11)
axes[0].set_title('Panel A: Residual vs. Regressor', fontsize=12, fontweight='bold')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Panel B: Component Plus Residual plot
bgrowth = ols_multiple.params['growth']
prgrowth = bgrowth * data_democracy['growth'] + uhat

axes[1].scatter(data_democracy['growth'], prgrowth, alpha=0.6, s=50, color='black')

# Add regression line
ols_compplusres = ols('prgrowth ~ growth', data=pd.DataFrame({
    'growth': data_democracy['growth'],
    'prgrowth': prgrowth
})).fit()
axes[1].plot(data_democracy['growth'], ols_compplusres.fittedvalues,
             'b-', linewidth=2, label='Regression line')

# Add lowess smooth
lowess_result = lowess(prgrowth, data_democracy['growth'], frac=0.3)
axes[1].plot(lowess_result[:, 0], lowess_result[:, 1],
             'r--', linewidth=2, label='Lowess smooth')

axes[1].set_xlabel('Growth regressor', fontsize=11)
axes[1].set_ylabel(f'Dem Res + {bgrowth:.3f}*Growth', fontsize=11)
axes[1].set_title('Panel B: Component Plus Residual', fontsize=12, fontweight='bold')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

# Panel C: Added Variable plot
# Regress democracy on all variables except growth
ols_nogrowth = ols('democracy ~ constraint + indcent + catholic + muslim + protestant',
                   data=data_democracy).fit()
uhat1democ = ols_nogrowth.resid

# Regress growth on all other variables
ols_growth = ols('growth ~ constraint + indcent + catholic + muslim + protestant',
                 data=data_democracy).fit()
uhat1growth = ols_growth.resid

axes[2].scatter(uhat1growth, uhat1democ, alpha=0.6, s=50, color='black')

# Add regression line
ols_addedvar = ols('uhat1democ ~ uhat1growth', data=pd.DataFrame({
    'uhat1growth': uhat1growth,
    'uhat1democ': uhat1democ
})).fit()
axes[2].plot(uhat1growth, ols_addedvar.fittedvalues,
             'b-', linewidth=2, label='Regression line')

# Add lowess smooth
lowess_result = lowess(uhat1democ, uhat1growth, frac=0.3)
axes[2].plot(lowess_result[:, 0], lowess_result[:, 1],
             'r--', linewidth=2, label='Lowess smooth')

axes[2].set_xlabel('Growth regressor (partial)', fontsize=11)
axes[2].set_ylabel('Democracy (partial)', fontsize=11)
axes[2].set_title('Panel C: Added Variable', fontsize=12, fontweight='bold')
axes[2].legend()
axes[2].grid(True, alpha=0.3)

plt.suptitle('Figure 16.3: Diagnostic Plots for Growth Regressor',
             fontsize=14, fontweight='bold', y=1.0)
output_file = os.path.join(IMAGES_DIR, 'ch16_fig3_diagnostics_growth.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\nFigure 16.3 saved to: {output_file}")
plt.close()

# Influential observations diagnostics
print("\n" + "-" * 70)
print("Influential Observations: DFITS")
print("-" * 70)

# Calculate influence measures
influence = OLSInfluence(ols_multiple)
dfits = influence.dffits[0]
threshold_dfits = 2 * np.sqrt(ols_multiple.df_model / ols_multiple.nobs)

print(f"\nDFITS threshold: {threshold_dfits:.4f}")
print(f"Number of observations exceeding threshold: {np.sum(np.abs(dfits) > threshold_dfits)}")

# Plot DFITS
fig, ax = plt.subplots(figsize=(12, 6))
obs_index = np.arange(len(dfits))
colors = ['red' if abs(d) > threshold_dfits else 'blue' for d in dfits]
ax.scatter(obs_index, dfits, c=colors, alpha=0.6, s=50)
ax.axhline(y=threshold_dfits, color='red', linestyle='--', linewidth=2, label='Threshold')
ax.axhline(y=-threshold_dfits, color='red', linestyle='--', linewidth=2)
ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
ax.set_xlabel('Observation Index', fontsize=12)
ax.set_ylabel('DFITS', fontsize=12)
ax.set_title('DFITS: Influential Observations', fontsize=14, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)

output_file = os.path.join(IMAGES_DIR, 'ch16_dfits.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\nDFITS plot saved to: {output_file}")
plt.close()

# List outliers
outliers_idx = np.where(np.abs(dfits) > threshold_dfits)[0]
if len(outliers_idx) > 0:
    print("\nInfluential observations (DFITS):")
    for idx in outliers_idx:
        print(f"  Observation {idx}: DFITS = {dfits[idx]:.4f}")

# DFBETAS
print("\n" + "-" * 70)
print("Influential Observations: DFBETAS")
print("-" * 70)

dfbetas = influence.dfbetas
threshold_dfbetas = 2 / np.sqrt(ols_multiple.nobs)
print(f"\nDFBETAS threshold: {threshold_dfbetas:.4f}")

# Plot DFBETAS for each regressor
n_params = dfbetas.shape[1]
param_names = ols_multiple.params.index

fig, axes = plt.subplots(2, 3, figsize=(18, 10))
axes = axes.flatten()

for i, param in enumerate(param_names):
    if i < len(axes):
        colors = ['red' if abs(d) > threshold_dfbetas else 'blue' for d in dfbetas[:, i]]
        axes[i].scatter(obs_index, dfbetas[:, i], c=colors, alpha=0.6, s=30)
        axes[i].axhline(y=threshold_dfbetas, color='red', linestyle='--', linewidth=1.5)
        axes[i].axhline(y=-threshold_dfbetas, color='red', linestyle='--', linewidth=1.5)
        axes[i].axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        axes[i].set_xlabel('Observation', fontsize=10)
        axes[i].set_ylabel('DFBETAS', fontsize=10)
        axes[i].set_title(f'{param}', fontsize=11, fontweight='bold')
        axes[i].grid(True, alpha=0.3)

# Remove extra subplots if any
for i in range(len(param_names), len(axes)):
    fig.delaxes(axes[i])

plt.suptitle('DFBETAS: Influential Observations by Variable',
             fontsize=14, fontweight='bold', y=1.0)
output_file = os.path.join(IMAGES_DIR, 'ch16_dfbetas.png')
plt.tight_layout()
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\nDFBETAS plot saved to: {output_file}")
plt.close()

# ========== SUMMARY ==========

print("\n" + "=" * 70)
print("CHAPTER 16 ANALYSIS COMPLETE")
print("=" * 70)
print("\nKey concepts demonstrated:")
print("  - Multicollinearity detection and diagnosis")
print("  - Time series autocorrelation")
print("  - Heteroskedasticity-robust standard errors")
print("  - HAC-robust (Newey-West) standard errors")
print("  - Regression diagnostics (actual vs. fitted, residual plots)")
print("  - Component plus residual plots")
print("  - Added variable plots")
print("  - Influential observations (DFITS, DFBETAS)")
print("\nAll figures saved to:", IMAGES_DIR)
