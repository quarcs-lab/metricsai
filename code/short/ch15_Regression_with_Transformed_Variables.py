# =============================================================================
# CHAPTER 15 CHEAT SHEET: Regression with Transformed Variables
# =============================================================================

# --- Libraries ---
import numpy as np                        # numerical operations (log, exp, sqrt)
import pandas as pd                       # data loading and manipulation
import matplotlib.pyplot as plt           # creating plots and visualizations
import pyfixest as pf                     # OLS regression with R-style formulas
# !pip install pyfixest  # if not installed
from statsmodels.formula.api import ols as sm_ols  # for Wald test

# =============================================================================
# STEP 1: Load data directly from a URL
# =============================================================================
# 872 full-time workers aged 25-65 with earnings, education, age, and hours
url = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_EARNINGS_COMPLETE.DTA"
data_earnings = pd.read_stata(url)

# Create log and squared variables for transformations
data_earnings['lnage'] = np.log(data_earnings['age'])

print(f"Dataset: {data_earnings.shape[0]} observations, {data_earnings.shape[1]} variables")
print(data_earnings[['earnings', 'lnearnings', 'age', 'education']].describe().round(2))

# =============================================================================
# STEP 2: Log transformations — levels vs log-linear vs log-log
# =============================================================================
# Three specifications of the same relationship reveal different stories
fit_levels = pf.feols('earnings ~ age + education', data=data_earnings, vcov='HC1')
fit_loglin = pf.feols('lnearnings ~ age + education', data=data_earnings, vcov='HC1')
fit_loglog = pf.feols('lnearnings ~ lnage + education', data=data_earnings, vcov='HC1')

print("=== Levels: absolute dollar effects ===")
print(f"  Education: +${fit_levels.coef()['education']:,.0f} per year")

print("\n=== Log-Linear: semi-elasticity (% change per unit) ===")
print(f"  Education: +{100*fit_loglin.coef()['education']:.1f}% per year (Mincer return)")

print("\n=== Log-Log: elasticity (% change per % change) ===")
print(f"  Age elasticity: {fit_loglog.coef()['lnage']:.4f}")

# =============================================================================
# STEP 3: Quadratic model — turning point and varying marginal effects
# =============================================================================
# A quadratic in age captures the inverted-U life-cycle earnings profile
fit_quad = pf.feols('earnings ~ age + agesq + education', data=data_earnings, vcov='HC1')

bage    = fit_quad.coef()['age']
bagesq  = fit_quad.coef()['agesq']
turning_point = -bage / (2 * bagesq)        # age where earnings peak

print(f"Turning point: {turning_point:.1f} years")
for a in [25, 40, 55]:
    me = bage + 2 * bagesq * a              # ME varies with age
    print(f"  ME at age {a}: ${me:,.0f}/year")

# Joint F-test: H0: age and age² are jointly zero
sm_quad = sm_ols('earnings ~ age + agesq + education', data=data_earnings).fit(cov_type='HC1')
f_test = sm_quad.wald_test('(age = 0, agesq = 0)', use_f=True)
print(f"Joint F-test p-value: {f_test.pvalue:.4f}")

# =============================================================================
# STEP 4: Standardized coefficients — compare variable importance
# =============================================================================
# Raw coefficients can't be compared across different units; beta* can
fit_mix = pf.feols('earnings ~ gender + age + agesq + education + dself + dgovt + lnhours',
                   data=data_earnings, vcov='HC1')

sd_y = data_earnings['earnings'].std()
predictors = ['gender', 'age', 'agesq', 'education', 'dself', 'dgovt', 'lnhours']

print(f"\n{'Variable':<12} {'Raw coef':>12} {'Beta*':>8}")
print("-" * 34)
for var in sorted(predictors, key=lambda v: abs(fit_mix.coef()[v] * data_earnings[v].std() / sd_y), reverse=True):
    raw  = fit_mix.coef()[var]
    beta_star = raw * data_earnings[var].std() / sd_y
    print(f"{var:<12} {raw:>12.2f} {beta_star:>8.4f}")

# =============================================================================
# STEP 5: Interaction terms — education returns that vary with age
# =============================================================================
# Does one more year of schooling pay the same at 25 as at 55?
fit_inter = pf.feols('earnings ~ age + education + agebyeduc', data=data_earnings, vcov='HC1')

b_educ  = fit_inter.coef()['education']
b_inter = fit_inter.coef()['agebyeduc']

print(f"\nME of education = {b_educ:,.0f} + {b_inter:.1f} × age")
for a in [25, 40, 55]:
    me = b_educ + b_inter * a               # ME depends on age
    print(f"  At age {a}: ${me:,.0f} per year of education")

# =============================================================================
# STEP 6: Retransformation bias — naive exp() underpredicts
# =============================================================================
# Jensen's inequality: E[exp(u)] > exp(E[u]), so naive predictions are biased
rmse_log = np.sqrt(np.mean(fit_loglin._u_hat**2))
correction = np.exp(rmse_log**2 / 2)        # normal-based smearing factor

naive_pred    = np.exp(fit_loglin.predict())
adjusted_pred = correction * naive_pred

print(f"\nSmearing factor: {correction:.4f}")
print(f"Actual mean:     ${data_earnings['earnings'].mean():,.0f}")
print(f"Naive mean:      ${naive_pred.mean():,.0f}  (underpredicts)")
print(f"Corrected mean:  ${adjusted_pred.mean():,.0f}  (bias removed)")

# =============================================================================
# STEP 7: Comprehensive model — combine all transformation types
# =============================================================================
# A single model mixing logs, quadratics, dummies, and continuous regressors
fit_full = pf.feols('lnearnings ~ gender + age + agesq + education + dself + dgovt + lnhours',
                    data=data_earnings, vcov='HC1')

print(f"\nR²: {fit_full._r2:.4f}")
print(f"Education return: ~{100*fit_full.coef()['education']:.1f}% per year (semi-elasticity)")
print(f"Gender gap: ~{100*fit_full.coef()['gender']:.1f}%")
print(f"Hours elasticity: {fit_full.coef()['lnhours']:.3f} (log-log coefficient)")

# Full regression table
fit_full.summary()
