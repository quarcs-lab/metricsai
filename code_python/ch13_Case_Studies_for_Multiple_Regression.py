#!/usr/bin/env python3
"""
Chapter 13: Case Studies for Multiple Regression
Python script extracted from Jupyter notebook
"""

# ============================================================================
# SETUP
# ============================================================================
# Import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.outliers_influence import variance_inflation_factor
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Random seed
np.random.seed(42)

# Data URL
GITHUB_DATA_URL = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/"

# Plotting
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

print("✓ Setup complete!")


# Ensure output directories exist
import os
IMAGES_DIR = 'images'
TABLES_DIR = 'tables'
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(TABLES_DIR, exist_ok=True)

print("="*70)
print("CHAPTER 13: CASE STUDIES FOR MULTIPLE REGRESSION")
print("="*70)

# ============================================================================
# 13.1 SCHOOL ACADEMIC PERFORMANCE INDEX
# ============================================================================
print("\n" + "="*70)
print("13.1 SCHOOL ACADEMIC PERFORMANCE INDEX")
print("="*70)

# Load API data
data_api = pd.read_stata(GITHUB_DATA_URL + 'AED_API99.DTA')
print(f"Loaded {len(data_api)} California high schools")
print(f"Variables: {list(data_api.columns)}")
data_api.head()

# Summary statistics
print("="*70)
print("SUMMARY STATISTICS")
print("="*70)
vars_api = ['api99', 'edparent', 'meals', 'englearn', 'yearround', 'credteach', 'emerteach']
print(data_api[vars_api].describe())

# Histogram of API scores
plt.figure(figsize=(10, 6))
plt.hist(data_api['api99'], bins=30, color='steelblue', alpha=0.7, edgecolor='black')
plt.axvline(data_api['api99'].mean(), color='red', linestyle='--', linewidth=2,
            label=f'Mean = {data_api["api99"].mean():.1f}')
plt.axvline(800, color='green', linestyle='--', linewidth=2, label='Target = 800')
plt.xlabel('Academic Performance Index (API)')
plt.ylabel('Number of Schools')
# plt.title('Figure 13.1: Distribution of API Scores')  # Removed: redundant with LaTeX caption
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig(os.path.join(IMAGES_DIR, 'ch13_api_distribution.png'), dpi=300, bbox_inches='tight')
plt.close()

# Bivariate regression: API ~ Edparent
model_api_biv = ols('api99 ~ edparent', data=data_api).fit(cov_type='HC1')
print("="*70)
print("BIVARIATE REGRESSION: API ~ EDPARENT")
print("="*70)
print(model_api_biv.summary())

# Scatter plot with regression line
plt.figure(figsize=(10, 6))
plt.scatter(data_api['edparent'], data_api['api99'], alpha=0.5, s=30, color='black')
plt.plot(data_api['edparent'], model_api_biv.fittedvalues, color='blue', linewidth=2,
         label='Fitted line')
plt.xlabel('Average Years of Parent Education')
plt.ylabel('Academic Performance Index (API)')
# plt.title('Figure 13.2: API vs Parent Education')  # Removed: redundant with LaTeX caption
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig(os.path.join(IMAGES_DIR, 'ch13_api_vs_edparent.png'), dpi=300, bbox_inches='tight')
plt.close()

# Correlation matrix
corr_matrix = data_api[vars_api].corr()
print("="*70)
print("CORRELATION MATRIX")
print("="*70)
print(corr_matrix.round(2))

# Heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0,
            square=True, linewidths=1)
# plt.title('Figure 13.3: Correlation Matrix')  # Removed: redundant with LaTeX caption
plt.tight_layout()
plt.savefig(os.path.join(IMAGES_DIR, 'ch13_api_correlation_matrix.png'), dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# 13.2 COBB-DOUGLAS PRODUCTION FUNCTION
# ============================================================================
print("\n" + "="*70)
print("13.2 COBB-DOUGLAS PRODUCTION FUNCTION")
print("="*70)

# Multiple regression
model_api_mult = ols('api99 ~ edparent + meals + englearn + yearround + credteach + emerteach',
                      data=data_api).fit()
print("="*70)
print("MULTIPLE REGRESSION")
print("="*70)
print(model_api_mult.summary())

# Coefficient table
coef_df = pd.DataFrame({
    'Coefficient': model_api_mult.params,
    'Std Error': model_api_mult.bse,
    't-stat': model_api_mult.tvalues,
    'p-value': model_api_mult.pvalues
}).round(3)
print("\n", coef_df)

# Load Cobb-Douglas data
data_cobb = pd.read_stata(GITHUB_DATA_URL + 'AED_COBBDOUGLAS.DTA')
print(f"Loaded {len(data_cobb)} years of US manufacturing data (1899-1922)")
print(f"Variables: {list(data_cobb.columns)}")
data_cobb.head(12)

# Create log transformations
data_cobb['lnq'] = np.log(data_cobb['q'])
data_cobb['lnk'] = np.log(data_cobb['k'])
data_cobb['lnl'] = np.log(data_cobb['l'])

print("Summary statistics (original and log-transformed):")
print(data_cobb[['q', 'k', 'l', 'lnq', 'lnk', 'lnl']].describe())

# Estimate Cobb-Douglas with HAC standard errors
model_cobb = ols('lnq ~ lnk + lnl', data=data_cobb).fit(cov_type='HAC', cov_kwds={'maxlags': 3})
print("="*70)
print("COBB-DOUGLAS REGRESSION: ln(Q) ~ ln(K) + ln(L)")
print("="*70)
print(model_cobb.summary())

beta_k = model_cobb.params['lnk']
beta_l = model_cobb.params['lnl']
print(f"\nSum of coefficients: {beta_k:.3f} + {beta_l:.3f} = {beta_k + beta_l:.3f}")

# Test constant returns to scale
# H0: beta_k + beta_l = 1
sum_betas = beta_k + beta_l
print(f"Testing constant returns to scale:")
print(f"H0: beta_capital + beta_labor = 1")
print(f"Estimated sum: {sum_betas:.3f}")

# Restricted model: ln(Q/L) ~ ln(K/L)
data_cobb['lnq_per_l'] = data_cobb['lnq'] - data_cobb['lnl']
data_cobb['lnk_per_l'] = data_cobb['lnk'] - data_cobb['lnl']
model_restricted = ols('lnq_per_l ~ lnk_per_l', data=data_cobb).fit()

# F-test
rss_unr = model_cobb.ssr
rss_r = model_restricted.ssr
f_stat = ((rss_r - rss_unr) / 1) / (rss_unr / model_cobb.df_resid)
p_value = 1 - stats.f.cdf(f_stat, 1, model_cobb.df_resid)

print(f"F-statistic: {f_stat:.2f}")
print(f"p-value: {p_value:.3f}")
print(f"Conclusion: {'Reject' if p_value < 0.05 else 'Fail to reject'} H0 at 5% level")

# ============================================================================
# 13.3 PHILLIPS CURVE AND OMITTED VARIABLES BIAS
# ============================================================================
print("\n" + "="*70)
print("13.3 PHILLIPS CURVE AND OMITTED VARIABLES BIAS")
print("="*70)

# Predicted output with bias correction
se = np.sqrt(model_cobb.scale)
bias_correction = np.exp(se**2 / 2)
data_cobb['q_pred'] = bias_correction * np.exp(model_cobb.fittedvalues)

# Plot actual vs predicted
plt.figure(figsize=(10, 6))
plt.plot(data_cobb['year'], data_cobb['q'], 'o-', color='black', linewidth=2,
         markersize=6, label='Actual Q')
plt.plot(data_cobb['year'], data_cobb['q_pred'], 's--', color='blue', linewidth=2,
         markersize=5, label='Predicted Q')
plt.xlabel('Year')
plt.ylabel('Output Index')
# plt.title('Figure 13.4: Actual vs Predicted Output (1899-1922)  # Removed: redundant with LaTeX caption')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig(os.path.join(IMAGES_DIR, 'ch13_cobb_douglas_prediction.png'), dpi=300, bbox_inches='tight')
plt.close()

# Load Phillips curve data
data_phillips = pd.read_stata(GITHUB_DATA_URL + 'AED_PHILLIPS.DTA')
print(f"Loaded {len(data_phillips)} years of US data (1949-2014)")
print(f"Variables: {list(data_phillips.columns)}")
data_phillips.head()

# Pre-1970 regression
data_pre1970 = data_phillips[data_phillips['year'] < 1970]
model_pre = ols('inflgdp ~ urate', data=data_pre1970).fit(cov_type='HAC', cov_kwds={'maxlags': 3})
print("="*70)
print("PHILLIPS CURVE PRE-1970 (1949-1969)")
print("="*70)
print(model_pre.summary())

# Plot pre-1970
plt.figure(figsize=(10, 6))
plt.scatter(data_pre1970['urate'], data_pre1970['inflgdp'], alpha=0.7, s=50, color='black')
plt.plot(data_pre1970['urate'], model_pre.fittedvalues, color='blue', linewidth=2,
         label='Fitted line')
plt.xlabel('Unemployment Rate (%)')
plt.ylabel('Inflation Rate (%)')
# plt.title('Figure 13.5: Phillips Curve Pre-1970 (Negative Relationship)  # Removed: redundant with LaTeX caption')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig(os.path.join(IMAGES_DIR, 'ch13_phillips_pre1970.png'), dpi=300, bbox_inches='tight')
plt.close()

# Post-1970 regression
data_post1970 = data_phillips[data_phillips['year'] >= 1970]
model_post = ols('inflgdp ~ urate', data=data_post1970).fit(cov_type='HAC', cov_kwds={'maxlags': 5})
print("="*70)
print("PHILLIPS CURVE POST-1970 (1970-2014)")
print("="*70)
print(model_post.summary())

# Plot post-1970
plt.figure(figsize=(10, 6))
plt.scatter(data_post1970['urate'], data_post1970['inflgdp'], alpha=0.7, s=50, color='black')
plt.plot(data_post1970['urate'], model_post.fittedvalues, color='red', linewidth=2,
         label='Fitted line')
plt.xlabel('Unemployment Rate (%)')
plt.ylabel('Inflation Rate (%)')
# plt.title('Figure 13.6: Phillips Curve Post-1970 (Positive Relationship - Breakdown!)  # Removed: redundant with LaTeX caption')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig(os.path.join(IMAGES_DIR, 'ch13_phillips_post1970.png'), dpi=300, bbox_inches='tight')
plt.close()

# Augmented Phillips curve (adding expected inflation)

data_post1970_exp = data_post1970.dropna(subset=['inflgdp1yr'])

model_augmented = ols('inflgdp ~ urate + inflgdp1yr', data=data_post1970_exp).fit(

    cov_type='HAC', cov_kwds={'maxlags': 5})

print("="*70)

print("AUGMENTED PHILLIPS CURVE POST-1970")

print("="*70)

print(model_augmented.summary())

# ============================================================================
# 13.4 AUTOMOBILE FUEL EFFICIENCY
# ============================================================================
print("\n" + "="*70)
print("13.4 AUTOMOBILE FUEL EFFICIENCY")
print("="*70)

# Demonstrate omitted variables bias



# Bivariate regression of Expinflation on Urate



model_aux = ols('inflgdp1yr ~ urate', data=data_post1970_exp).fit()



gamma = model_aux.params['urate']



beta3 = model_augmented.params['inflgdp1yr']



beta2 = model_augmented.params['urate']







print("="*70)



print("OMITTED VARIABLES BIAS CALCULATION")



print("="*70)



print(f"True model: Inflation = β1 + β2*Urate + β3*Expinflation")



print(f"Omitted model: Inflation = b1 + b2*Urate")



print(f"\nOmitted variables bias formula: E[b2] = β2 + β3*γ")



print(f"where γ = coefficient from Expinflation ~ Urate regression")



print(f"\nγ (from auxiliary regression): {gamma:.3f}")



print(f"β3 (from full model): {beta3:.3f}")



print(f"β2 (from full model): {beta2:.3f}")



print(f"\nPredicted E[b2] = {beta2:.3f} + {beta3:.3f} * {gamma:.3f} = {beta2 + beta3*gamma:.3f}")



print(f"Actual b2 (from bivariate): {model_post.params['urate']:.3f}")



print(f"\n✓ Omitted variables bias explains the sign reversal!")

# Load automobile data
data_auto = pd.read_stata(GITHUB_DATA_URL + 'AED_AUTOSMPG.DTA')
print(f"Loaded {len(data_auto)} vehicle observations (1980-2006)")
print(f"\nKey variables: {['year', 'mfr', 'mpg', 'curbwt', 'hp', 'torque']}")
print(f"\nNote: Dataset has pre-computed log transformations (lmpg, lcurbwt, lhp, ltorque)")
print(data_auto[['year', 'mfr', 'mpg', 'curbwt', 'hp', 'torque']].head())

# Summary statistics
key_vars = ['mpg', 'curbwt', 'hp', 'torque', 'year']
print("="*70)
print("SUMMARY STATISTICS")
print("="*70)
print(data_auto[key_vars].describe())

# Manufacturer distribution
print("\n" + "="*70)
print("TOP 10 MANUFACTURERS BY OBSERVATIONS")
print("="*70)
print(data_auto['mfr'].value_counts().head(10))

# ============================================================================
# 13.5 RAND HEALTH INSURANCE EXPERIMENT (RCT)
# ============================================================================
print("\n" + "="*70)
print("13.5 RAND HEALTH INSURANCE EXPERIMENT (RCT)")
print("="*70)

# Log-log regression with cluster-robust standard errors
# Use pre-computed log variables
model_auto = ols('lmpg ~ lhp + lcurbwt + ltorque + year', data=data_auto).fit(
    cov_type='cluster',
    cov_kwds={'groups': data_auto['mfr']}
)

print("="*70)
print("LOG-LOG REGRESSION: FUEL EFFICIENCY")
print("="*70)
print(model_auto.summary())

# Interpretation
print("\n" + "="*70)
print("ELASTICITY INTERPRETATION")
print("="*70)
print(f"Horsepower elasticity: {model_auto.params['lhp']:.3f}")
print(f"  → 1% increase in HP → {model_auto.params['lhp']:.2f}% change in MPG")
print(f"\nWeight elasticity: {model_auto.params['lcurbwt']:.3f}")
print(f"  → 1% increase in weight → {model_auto.params['lcurbwt']:.2f}% change in MPG")
print(f"\nTorque elasticity: {model_auto.params['ltorque']:.3f}")
print(f"  → 1% increase in torque → {model_auto.params['ltorque']:.2f}% change in MPG")
print(f"\nYear trend: {model_auto.params['year']:.4f}")
print(f"  → Efficiency improves {model_auto.params['year']*100:.2f}% per year")

print("\n" + "="*70)
print("CLUSTER-ROBUST STANDARD ERRORS")
print("="*70)
print(f"Clustered by manufacturer (mfr)")
print(f"Number of clusters: {data_auto['mfr'].nunique()}")
print(f"Average observations per cluster: {len(data_auto)/data_auto['mfr'].nunique():.0f}")
print(f"\nWhy cluster? Vehicles from same manufacturer likely have correlated errors")
print(f"due to common technology, design philosophy, and engineering teams.")

# ============================================================================
# 13.6 HEALTH CARE ACCESS (DIFFERENCE-IN-DIFFERENCES)
# ============================================================================
print("\n" + "="*70)
print("13.6 HEALTH CARE ACCESS (DIFFERENCE-IN-DIFFERENCES)")
print("="*70)

# Load health insurance experiment data
data_health = pd.read_stata(GITHUB_DATA_URL + 'AED_HEALTHINSEXP.DTA')

# Use first year data only (as per textbook)
data_health_y1 = data_health[data_health['year'] == 1]

print(f"Loaded {len(data_health)} total observations")
print(f"Using Year 1 only: {len(data_health_y1)} observations")
print(f"\nInsurance plans: {sorted(data_health_y1['plan'].unique())}")
print(f"\nKey variables:")
print(f"  - plan: Insurance plan assignment (randomized)")
print(f"  - spending: Total medical spending")
print(f"  - Plan indicators: coins0, coins25, coins50, coins95, coinsmixed, coinsindiv")

# Summary statistics by plan
print("\n" + "="*70)
print("MEAN SPENDING BY INSURANCE PLAN")
print("="*70)
spending_by_plan = data_health_y1.groupby('plan')['spending'].agg(['mean', 'std', 'count'])
print(spending_by_plan)

# Regression with plan indicators
model_rct = ols('spending ~ coins25 + coins50 + coins95 + coinsmixed + coinsindiv',
                data=data_health_y1).fit(
    cov_type='cluster',
    cov_kwds={'groups': data_health_y1['idfamily']}
)

print("\n" + "="*70)
print("RCT REGRESSION: SPENDING ON INSURANCE PLANS")
print("="*70)
print("Omitted category: Free Care (coins0)")
print(model_rct.summary())

# F-test for joint significance
print("\n" + "="*70)
print("JOINT F-TEST: DO PLANS MATTER?")
print("="*70)
hypotheses = 'coins25 = coins50 = coins95 = coinsmixed = coinsindiv = 0'
ftest = model_rct.f_test(hypotheses)
print(f"H0: All plan coefficients = 0")
print(f"F-statistic: {ftest.fvalue:.2f}")
print(f"p-value: {ftest.pvalue:.4f}")
print(f"Conclusion: {'Reject H0' if ftest.pvalue < 0.05 else 'Fail to reject H0'} at 5% level")

print("\n" + "="*70)
print("CAUSAL INTERPRETATION")
print("="*70)
print("✓ Randomized Control Trial enables causal inference")
print("✓ Random assignment eliminates selection bias")
print("✓ Free care → highest spending (omitted baseline)")
print("✓ Higher cost-sharing → lower spending")

# ============================================================================
# 13.7 POLITICAL INCUMBENCY (REGRESSION DISCONTINUITY)
# ============================================================================
print("\n" + "="*70)
print("13.7 POLITICAL INCUMBENCY (REGRESSION DISCONTINUITY)")
print("="*70)

# Load health care access data (South Africa)
data_access = pd.read_stata(GITHUB_DATA_URL + 'AED_HEALTHACCESS.DTA')

print(f"Loaded {len(data_access)} observations (South African children 0-4)")
print(f"\nDifference-in-Differences Setup:")
print(f"  - Treatment: High treatment communities (hightreat=1)")
print(f"  - Control: Low treatment communities (hightreat=0)")
print(f"  - Pre period: 1993 (post=0)")
print(f"  - Post period: 1998 (post=1)")
print(f"  - Outcome: waz (weight-for-age z-score)")

# Summary statistics by treatment and time
print("\n" + "="*70)
print("MEAN WEIGHT-FOR-AGE Z-SCORE (WAZ)")
print("="*70)
did_table = data_access.groupby(['hightreat', 'post'])['waz'].agg(['mean', 'count'])
print(did_table)

# Calculate DiD manually
pre_control = data_access[(data_access['hightreat']==0) & (data_access['post']==0)]['waz'].mean()
post_control = data_access[(data_access['hightreat']==0) & (data_access['post']==1)]['waz'].mean()
pre_treat = data_access[(data_access['hightreat']==1) & (data_access['post']==0)]['waz'].mean()
post_treat = data_access[(data_access['hightreat']==1) & (data_access['post']==1)]['waz'].mean()

did_estimate = (post_treat - pre_treat) - (post_control - pre_control)

print(f"\nManual DiD calculation:")
print(f"  Control change: {post_control:.3f} - {pre_control:.3f} = {post_control - pre_control:.3f}")
print(f"  Treated change: {post_treat:.3f} - {pre_treat:.3f} = {post_treat - pre_treat:.3f}")
print(f"  DiD estimate: ({post_treat:.3f} - {pre_treat:.3f}) - ({post_control:.3f} - {pre_control:.3f}) = {did_estimate:.3f}")

# DiD regression
model_did = ols('waz ~ hightreat + post + postXhigh', data=data_access).fit(
    cov_type='cluster',
    cov_kwds={'groups': data_access['idcommunity']}
)

print("\n" + "="*70)
print("DiD REGRESSION")
print("="*70)
print(model_did.summary())

print("\n" + "="*70)
print("INTERPRETATION")
print("="*70)
print(f"DiD coefficient (postXhigh): {model_did.params['postXhigh']:.3f}")
print(f"Matches manual calculation: {did_estimate:.3f} ✓")
print(f"\nCausal interpretation:")
print(f"Clinic access improved child nutrition by {model_did.params['postXhigh']:.2f} standard deviations")
print(f"This is a {'statistically significant' if model_did.pvalues['postXhigh'] < 0.05 else 'not significant'} effect")
print(f"\nCluster-robust SEs by community account for within-community correlation")

# ============================================================================
# 13.8 INSTITUTIONS AND GDP (INSTRUMENTAL VARIABLES)
# ============================================================================
print("\n" + "="*70)
print("13.8 INSTITUTIONS AND GDP (INSTRUMENTAL VARIABLES)")
print("="*70)

# Load incumbency data (U.S. Senate elections)
data_incumb = pd.read_stata(GITHUB_DATA_URL + 'AED_INCUMBENCY.DTA')

print(f"Loaded {len(data_incumb)} Senate elections (1914-2010)")
print(f"\nRegression Discontinuity Setup:")
print(f"  - Running variable: margin (vote margin in election t)")
print(f"  - Threshold: margin = 0 (barely won vs barely lost)")
print(f"  - Outcome: vote (vote share in election t+1)")
print(f"  - win: Indicator for margin > 0")

# Summary statistics
print("\n" + "="*70)
print("SUMMARY STATISTICS")
print("="*70)
print(data_incumb[['vote', 'margin', 'win']].describe())

# Keep only elections with non-missing vote in t+1
data_rd = data_incumb[data_incumb['vote'].notna()].copy()
print(f"\nObservations with outcome data: {len(data_rd)}")

# RD regression (linear)
model_rd = ols('vote ~ win + margin', data=data_rd).fit(cov_type='HC1')

print("\n" + "="*70)
print("REGRESSION DISCONTINUITY ESTIMATION")
print("="*70)
print(model_rd.summary())

print("\n" + "="*70)
print("INCUMBENCY ADVANTAGE")
print("="*70)
print(f"RD estimate (win coefficient): {model_rd.params['win']:.3f}")
print(f"95% CI: [{model_rd.conf_int().loc['win', 0]:.3f}, {model_rd.conf_int().loc['win', 1]:.3f}]")
print(f"\nInterpretation:")
print(f"Barely winning vs barely losing increases vote share in next election by {model_rd.params['win']:.1f}%")
print(f"This is the causal effect of incumbency")
print(f"\nWhy causal? At the threshold (margin≈0), winning is quasi-random")
print(f"Candidates just above/below threshold are similar in all respects except incumbency status")

# Visualization note
print("\n" + "="*70)
print("RD PLOT")
print("="*70)
print("To visualize discontinuity:")
print("  - Bin observations by margin")
print("  - Plot mean vote in next election vs margin")
print("  - Should see jump at margin=0")

# ============================================================================
# 13.9 FROM RAW DATA TO FINAL DATA
# ============================================================================
print("\n" + "="*70)
print("13.9 FROM RAW DATA TO FINAL DATA")
print("="*70)

# Load institutions data (cross-country)
data_inst = pd.read_stata(GITHUB_DATA_URL + 'AED_INSTITUTIONS.DTA')

print(f"Loaded {len(data_inst)} countries")
print(f"\nInstrumental Variables Setup:")
print(f"  - Outcome: logpgp95 (log GDP per capita 1995)")
print(f"  - Endogenous regressor: avexpr (institutions quality)")
print(f"  - Instrument: logem4 (log settler mortality)")
print(f"\nKey idea: Settler mortality affected colonial institutions,")
print(f"which persist to affect GDP today, but mortality doesn't")
print(f"directly affect modern GDP")

# Summary statistics
print("\n" + "="*70)
print("SUMMARY STATISTICS")
print("="*70)
print(data_inst[['logpgp95', 'avexpr', 'logem4']].describe())

# OLS (biased - endogeneity problem)
model_ols = ols('logpgp95 ~ avexpr', data=data_inst).fit(cov_type='HC1')

print("\n" + "="*70)
print("OLS REGRESSION (BIASED)")
print("="*70)
print(model_ols.summary())
print(f"\nOLS coefficient: {model_ols.params['avexpr']:.3f}")
print("⚠️ This is biased due to endogeneity (omitted variables, reverse causation)")

# First stage
model_first = ols('avexpr ~ logem4', data=data_inst).fit(cov_type='HC1')

print("\n" + "="*70)
print("FIRST STAGE: INSTITUTIONS ~ SETTLER MORTALITY")
print("="*70)
print(model_first.summary())
print(f"\nFirst stage F-statistic: {model_first.fvalue:.2f}")
print(f"Rule of thumb: F > 10 for strong instrument")
print(f"Instrument strength: {'Strong ✓' if model_first.fvalue > 10 else 'Weak ⚠️'}")

# 2SLS manually (for pedagogy)
print("\n" + "="*70)
print("TWO-STAGE LEAST SQUARES (2SLS)")
print("="*70)

# Predicted institutions from first stage
data_inst['avexpr_hat'] = model_first.fittedvalues

# Second stage (using predicted values)
model_second = ols('logpgp95 ~ avexpr_hat', data=data_inst).fit(cov_type='HC1')

print("\nSecond stage:")
print(model_second.summary())

print("\n" + "="*70)
print("COMPARISON: OLS vs IV")
print("="*70)
print(f"OLS coefficient: {model_ols.params['avexpr']:.3f}")
print(f"IV/2SLS coefficient: {model_second.params['avexpr_hat']:.3f}")
print(f"\nDifference: {model_second.params['avexpr_hat'] - model_ols.params['avexpr']:.3f}")
print(f"\nIV estimate is larger → OLS has attenuation bias")
print(f"(measurement error and omitted variables bias OLS toward zero)")

print("\n" + "="*70)
print("CAUSAL INTERPRETATION")
print("="*70)
print(f"1-unit improvement in institutions → {model_second.params['avexpr_hat']:.2f} increase in log GDP")
print(f"Exponentiating: {np.exp(model_second.params['avexpr_hat']):.2f}x increase in GDP level")
print(f"\n✓ This is a causal estimate (under IV assumptions)")
print(f"✓ Instrument (settler mortality) is:")
print(f"  - Relevant: Strong first stage (F = {model_first.fvalue:.1f})")
print(f"  - Exogenous: Mortality in 1700s doesn't directly affect modern GDP")

# Demonstrate reading different file formats
print("="*70)
print("DATA READING EXAMPLES")
print("="*70)

# Stata files
print("\n1. Reading Stata files (.dta):")
print("   data = pd.read_stata('file.dta')")

# CSV files
print("\n2. Reading CSV files:")
print("   data = pd.read_csv('file.csv')")

# Excel files
print("\n3. Reading Excel files:")
print("   data = pd.read_excel('file.xlsx')")

# Example: merge operations
print("\n" + "="*70)
print("DATA MERGING EXAMPLE")
print("="*70)

df1 = pd.DataFrame({'id': [1, 2, 3], 'value_a': [10, 20, 30]})
df2 = pd.DataFrame({'id': [1, 2, 4], 'value_b': [100, 200, 400]})

print("\nDataFrame 1:")
print(df1)
print("\nDataFrame 2:")
print(df2)

merged = pd.merge(df1, df2, on='id', how='inner')
print("\nMerged (inner join):")
print(merged)


print("\n" + "="*70)
print("CHAPTER 13 COMPLETE - ALL CASE STUDIES FINISHED")
print("="*70)
