# =============================================================================
# CHAPTER 13 CHEAT SHEET: Case Studies for Multiple Regression
# =============================================================================

# --- Libraries ---
import numpy as np                        # numerical operations and log transforms
import pandas as pd                       # data loading and manipulation
import matplotlib.pyplot as plt           # creating plots and visualizations
import pyfixest as pf                     # OLS regression with R-style formulas
# !pip install pyfixest  # if not installed
from statsmodels.formula.api import ols as sm_ols  # for SSR-based F-tests and cluster SEs
from scipy import stats                   # F-distribution for hypothesis tests

# --- Data source ---
URL = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/"

# =============================================================================
# STEP 1: Cobb-Douglas Production Function — log-linearize and estimate
# =============================================================================
# Taking logs converts Q = A*K^alpha*L^beta into a linear model estimable by OLS
data_cobb = pd.read_stata(URL + "AED_COBBDOUGLAS.DTA")
data_cobb['lnq'] = np.log(data_cobb['q'])
data_cobb['lnk'] = np.log(data_cobb['k'])
data_cobb['lnl'] = np.log(data_cobb['l'])

# OLS with HAC standard errors (time series: autocorrelation + heteroskedasticity)
fit_cobb = pf.feols('lnq ~ lnk + lnl', data=data_cobb, vcov={'NW': 3})

alpha = fit_cobb.coef()['lnk']    # capital elasticity
beta  = fit_cobb.coef()['lnl']    # labor elasticity

print(f"Capital elasticity α = {alpha:.3f}, Labor elasticity β = {beta:.3f}")
print(f"Sum α + β = {alpha + beta:.3f}  (≈1 → constant returns to scale)")
print(f"R² = {fit_cobb._r2:.4f}")
fit_cobb.summary()

# F-test for constant returns to scale: H0: α + β = 1
data_cobb['lnq_l'] = data_cobb['lnq'] - data_cobb['lnl']
data_cobb['lnk_l'] = data_cobb['lnk'] - data_cobb['lnl']
# Use statsmodels for SSR-based F-test
sm_cobb = sm_ols('lnq ~ lnk + lnl', data=data_cobb).fit()
sm_r = sm_ols('lnq_l ~ lnk_l', data=data_cobb).fit()
f_stat = ((sm_r.ssr - sm_cobb.ssr) / 1) / (sm_cobb.ssr / sm_cobb.df_resid)
p_val  = 1 - stats.f.cdf(f_stat, 1, sm_cobb.df_resid)
print(f"CRS test: F = {f_stat:.2f}, p = {p_val:.3f} → {'Fail to reject' if p_val > 0.05 else 'Reject'} CRS")

# =============================================================================
# STEP 2: Phillips Curve — omitted variables bias reverses the sign
# =============================================================================
# Pre-1970 the trade-off works; post-1970 it breaks because expected inflation
# is omitted — a textbook demonstration of OVB
data_phil = pd.read_stata(URL + "AED_PHILLIPS.DTA")

# Pre-1970: classic negative relationship
pre = data_phil[data_phil['year'] < 1970]
fit_pre = pf.feols('inflgdp ~ urate', data=pre, vcov={'NW': 3})
print(f"\nPre-1970 slope: {fit_pre.coef()['urate']:.3f}  (negative → classic Phillips curve)")

# Post-1970: sign flips due to omitted expected inflation
post = data_phil[data_phil['year'] >= 1970]
fit_post = pf.feols('inflgdp ~ urate', data=post, vcov={'NW': 5})
print(f"Post-1970 slope: {fit_post.coef()['urate']:.3f}  (positive → breakdown!)")

# Augmented model: adding expected inflation restores the negative sign
post_exp = post.dropna(subset=['inflgdp1yr'])
fit_aug = pf.feols('inflgdp ~ urate + inflgdp1yr', data=post_exp, vcov={'NW': 5})
print(f"Augmented slope on urate: {fit_aug.coef()['urate']:.3f}  (negative again!)")
print(f"Expected inflation coef:  {fit_aug.coef()['inflgdp1yr']:.3f}")

# OVB formula: E[b2] = β2 + β3*γ
fit_aux = pf.feols('inflgdp1yr ~ urate', data=post_exp)
predicted = fit_aug.coef()['urate'] + fit_aug.coef()['inflgdp1yr'] * fit_aux.coef()['urate']
print(f"OVB predicted bivariate slope: {predicted:.3f}  (actual: {fit_post.coef()['urate']:.3f})")

# =============================================================================
# STEP 3: RAND Health Insurance Experiment — RCT as the gold standard
# =============================================================================
# Random assignment to insurance plans eliminates selection bias
data_rand = pd.read_stata(URL + "AED_HEALTHINSEXP.DTA")
data_rand_y1 = data_rand[data_rand['year'] == 1]

# Mean spending by plan
print(f"\n{'Plan':<12} {'Mean $':>10} {'N':>8}")
for plan, grp in data_rand_y1.groupby('plan')['spending']:
    print(f"{plan:<12} {grp.mean():>10,.0f} {len(grp):>8,}")

# Regression with cluster-robust SEs by family
fit_rct = pf.feols('spending ~ coins25 + coins50 + coins95 + coinsmixed + coinsindiv',
                   data=data_rand_y1, vcov={'CRV1': 'idfamily'})
fit_rct.summary()

# Joint F-test: do insurance plans matter?
sm_rct = sm_ols('spending ~ coins25 + coins50 + coins95 + coinsmixed + coinsindiv',
                data=data_rand_y1).fit(
    cov_type='cluster', cov_kwds={'groups': data_rand_y1['idfamily']}
)
ftest = sm_rct.f_test('coins25 = coins50 = coins95 = coinsmixed = coinsindiv = 0')
print(f"Joint F-test: F = {ftest.fvalue:.2f}, p = {ftest.pvalue:.4f}")

# =============================================================================
# STEP 4: Difference-in-Differences — health clinic access in South Africa
# =============================================================================
# DiD removes both time-invariant confounders and common time trends
data_did = pd.read_stata(URL + "AED_HEALTHACCESS.DTA")

# Manual DiD calculation
pre_c  = data_did[(data_did['hightreat']==0) & (data_did['post']==0)]['waz'].mean()
post_c = data_did[(data_did['hightreat']==0) & (data_did['post']==1)]['waz'].mean()
pre_t  = data_did[(data_did['hightreat']==1) & (data_did['post']==0)]['waz'].mean()
post_t = data_did[(data_did['hightreat']==1) & (data_did['post']==1)]['waz'].mean()
did    = (post_t - pre_t) - (post_c - pre_c)
print(f"\nDiD estimate (manual): {did:.3f} SD improvement in child nutrition")

# DiD regression with cluster-robust SEs by community
fit_did = pf.feols('waz ~ hightreat + post + postXhigh', data=data_did,
                   vcov={'CRV1': 'idcommunity'})
print(f"DiD coefficient (regression): {fit_did.coef()['postXhigh']:.3f}")
print(f"p-value: {fit_did.pval()['postXhigh']:.4f}")

# =============================================================================
# STEP 5: Regression Discontinuity — incumbency advantage in U.S. Senate
# =============================================================================
# Candidates who barely win vs barely lose are quasi-randomly assigned to
# incumbent status — the jump at margin = 0 is the causal effect
data_rd = pd.read_stata(URL + "AED_INCUMBENCY.DTA")
data_rd = data_rd[data_rd['vote'].notna()].copy()

fit_rd = pf.feols('vote ~ win + margin', data=data_rd, vcov='HC1')
print(f"\nIncumbency advantage: {fit_rd.coef()['win']:.1f} percentage points")
print(f"95% CI: [{fit_rd.confint().loc['win'].iloc[0]:.1f}, {fit_rd.confint().loc['win'].iloc[1]:.1f}]")
print(f"p-value: {fit_rd.pval()['win']:.4f}")

# =============================================================================
# STEP 6: Instrumental Variables — do institutions cause growth?
# =============================================================================
# OLS is biased by reverse causation; settler mortality instruments for
# modern institutions (relevant + exogenous to modern GDP)
data_iv = pd.read_stata(URL + "AED_INSTITUTIONS.DTA")

# OLS (biased)
fit_ols_iv = pf.feols('logpgp95 ~ avexpr', data=data_iv, vcov='HC1')

# First stage: institutions ~ settler mortality
fit_1st = pf.feols('avexpr ~ logem4', data=data_iv, vcov='HC1')
sm_1st = sm_ols('avexpr ~ logem4', data=data_iv).fit(cov_type='HC1')
print(f"\nFirst-stage F = {sm_1st.fvalue:.1f}  ({'Strong' if sm_1st.fvalue > 10 else 'Weak'} instrument)")

# Second stage: GDP ~ predicted institutions
data_iv['avexpr_hat'] = fit_1st.predict()
fit_2nd = pf.feols('logpgp95 ~ avexpr_hat', data=data_iv, vcov='HC1')

print(f"OLS coefficient:  {fit_ols_iv.coef()['avexpr']:.3f}  (biased)")
print(f"IV/2SLS coefficient: {fit_2nd.coef()['avexpr_hat']:.3f}  (causal)")
print(f"Causal effect: 1-unit improvement in institutions → "
      f"{np.exp(fit_2nd.coef()['avexpr_hat']):.1f}x increase in GDP")
