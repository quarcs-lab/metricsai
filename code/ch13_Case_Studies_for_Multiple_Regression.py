# =============================================================================
# CHAPTER 13 CHEAT SHEET: Case Studies for Multiple Regression
# =============================================================================

# --- Libraries ---
import numpy as np                        # numerical operations and log transforms
import pandas as pd                       # data loading and manipulation
import matplotlib.pyplot as plt           # creating plots and visualizations
from statsmodels.formula.api import ols   # OLS regression with R-style formulas
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
model_cobb = ols('lnq ~ lnk + lnl', data=data_cobb).fit(
    cov_type='HAC', cov_kwds={'maxlags': 3}
)

alpha = model_cobb.params['lnk']   # capital elasticity
beta  = model_cobb.params['lnl']   # labor elasticity

print(f"Capital elasticity α = {alpha:.3f}, Labor elasticity β = {beta:.3f}")
print(f"Sum α + β = {alpha + beta:.3f}  (≈1 → constant returns to scale)")
print(f"R² = {model_cobb.rsquared:.4f}")
model_cobb.summary()

# F-test for constant returns to scale: H0: α + β = 1
data_cobb['lnq_l'] = data_cobb['lnq'] - data_cobb['lnl']
data_cobb['lnk_l'] = data_cobb['lnk'] - data_cobb['lnl']
model_r = ols('lnq_l ~ lnk_l', data=data_cobb).fit()
f_stat = ((model_r.ssr - model_cobb.ssr) / 1) / (model_cobb.ssr / model_cobb.df_resid)
p_val  = 1 - stats.f.cdf(f_stat, 1, model_cobb.df_resid)
print(f"CRS test: F = {f_stat:.2f}, p = {p_val:.3f} → {'Fail to reject' if p_val > 0.05 else 'Reject'} CRS")

# =============================================================================
# STEP 2: Phillips Curve — omitted variables bias reverses the sign
# =============================================================================
# Pre-1970 the trade-off works; post-1970 it breaks because expected inflation
# is omitted — a textbook demonstration of OVB
data_phil = pd.read_stata(URL + "AED_PHILLIPS.DTA")

# Pre-1970: classic negative relationship
pre = data_phil[data_phil['year'] < 1970]
m_pre = ols('inflgdp ~ urate', data=pre).fit(cov_type='HAC', cov_kwds={'maxlags': 3})
print(f"\nPre-1970 slope: {m_pre.params['urate']:.3f}  (negative → classic Phillips curve)")

# Post-1970: sign flips due to omitted expected inflation
post = data_phil[data_phil['year'] >= 1970]
m_post = ols('inflgdp ~ urate', data=post).fit(cov_type='HAC', cov_kwds={'maxlags': 5})
print(f"Post-1970 slope: {m_post.params['urate']:.3f}  (positive → breakdown!)")

# Augmented model: adding expected inflation restores the negative sign
post_exp = post.dropna(subset=['inflgdp1yr'])
m_aug = ols('inflgdp ~ urate + inflgdp1yr', data=post_exp).fit(
    cov_type='HAC', cov_kwds={'maxlags': 5}
)
print(f"Augmented slope on urate: {m_aug.params['urate']:.3f}  (negative again!)")
print(f"Expected inflation coef:  {m_aug.params['inflgdp1yr']:.3f}")

# OVB formula: E[b2] = β2 + β3*γ
m_aux = ols('inflgdp1yr ~ urate', data=post_exp).fit()
predicted = m_aug.params['urate'] + m_aug.params['inflgdp1yr'] * m_aux.params['urate']
print(f"OVB predicted bivariate slope: {predicted:.3f}  (actual: {m_post.params['urate']:.3f})")

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
model_rct = ols('spending ~ coins25 + coins50 + coins95 + coinsmixed + coinsindiv',
                data=data_rand_y1).fit(
    cov_type='cluster', cov_kwds={'groups': data_rand_y1['idfamily']}
)
model_rct.summary()

# Joint F-test: do insurance plans matter?
ftest = model_rct.f_test('coins25 = coins50 = coins95 = coinsmixed = coinsindiv = 0')
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
model_did = ols('waz ~ hightreat + post + postXhigh', data=data_did).fit(
    cov_type='cluster', cov_kwds={'groups': data_did['idcommunity']}
)
print(f"DiD coefficient (regression): {model_did.params['postXhigh']:.3f}")
print(f"p-value: {model_did.pvalues['postXhigh']:.4f}")

# =============================================================================
# STEP 5: Regression Discontinuity — incumbency advantage in U.S. Senate
# =============================================================================
# Candidates who barely win vs barely lose are quasi-randomly assigned to
# incumbent status — the jump at margin = 0 is the causal effect
data_rd = pd.read_stata(URL + "AED_INCUMBENCY.DTA")
data_rd = data_rd[data_rd['vote'].notna()].copy()

model_rd = ols('vote ~ win + margin', data=data_rd).fit(cov_type='HC1')
print(f"\nIncumbency advantage: {model_rd.params['win']:.1f} percentage points")
print(f"95% CI: [{model_rd.conf_int().loc['win', 0]:.1f}, {model_rd.conf_int().loc['win', 1]:.1f}]")
print(f"p-value: {model_rd.pvalues['win']:.4f}")

# =============================================================================
# STEP 6: Instrumental Variables — do institutions cause growth?
# =============================================================================
# OLS is biased by reverse causation; settler mortality instruments for
# modern institutions (relevant + exogenous to modern GDP)
data_iv = pd.read_stata(URL + "AED_INSTITUTIONS.DTA")

# OLS (biased)
m_ols = ols('logpgp95 ~ avexpr', data=data_iv).fit(cov_type='HC1')

# First stage: institutions ~ settler mortality
m_1st = ols('avexpr ~ logem4', data=data_iv).fit(cov_type='HC1')
print(f"\nFirst-stage F = {m_1st.fvalue:.1f}  ({'Strong' if m_1st.fvalue > 10 else 'Weak'} instrument)")

# Second stage: GDP ~ predicted institutions
data_iv['avexpr_hat'] = m_1st.fittedvalues
m_2nd = ols('logpgp95 ~ avexpr_hat', data=data_iv).fit(cov_type='HC1')

print(f"OLS coefficient:  {m_ols.params['avexpr']:.3f}  (biased)")
print(f"IV/2SLS coefficient: {m_2nd.params['avexpr_hat']:.3f}  (causal)")
print(f"Causal effect: 1-unit improvement in institutions → "
      f"{np.exp(m_2nd.params['avexpr_hat']):.1f}x increase in GDP")
