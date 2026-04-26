# =============================================================================
# CHAPTER 14 CHEAT SHEET: Regression with Indicator Variables
# =============================================================================

# --- Libraries ---
import pandas as pd                       # data loading and manipulation
import numpy as np                        # numerical operations
import matplotlib.pyplot as plt           # creating plots and visualizations
import pyfixest as pf                     # OLS regression with R-style formulas
# !pip install pyfixest  # if not installed
from scipy import stats                   # t-tests for group comparisons
from scipy.stats import f_oneway          # one-way ANOVA F-test

# =============================================================================
# STEP 1: Load data directly from a URL
# =============================================================================
# pd.read_stata() reads Stata .dta files — 872 full-time workers aged 25-65
url = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/AED_EARNINGS_COMPLETE.DTA"
data = pd.read_stata(url)

print(f"Dataset: {data.shape[0]} observations, {data.shape[1]} variables")

# =============================================================================
# STEP 2: Descriptive statistics — compare earnings by gender
# =============================================================================
# Indicator variable: gender = 1 (female), gender = 0 (male)
mean_male   = data[data['gender'] == 0]['earnings'].mean()
mean_female = data[data['gender'] == 1]['earnings'].mean()
diff_means  = mean_female - mean_male

print(f"Mean earnings (Male):   ${mean_male:,.2f}")
print(f"Mean earnings (Female): ${mean_female:,.2f}")
print(f"Difference (F - M):     ${diff_means:,.2f}")

# =============================================================================
# STEP 3: Regression on a single indicator — equivalent to difference in means
# =============================================================================
# The intercept = mean for d=0 (males); the gender coefficient = mean difference
# IMPORTANT: vcov='HC1' uses robust standard errors
fit1 = pf.feols('earnings ~ gender', data=data, vcov='HC1')

intercept = fit1.coef()['Intercept']      # mean earnings for males
gap       = fit1.coef()['gender']         # earnings gap (females - males)
r2        = fit1._r2

print(f"\nModel 1: earnings = {intercept:,.0f} + ({gap:,.0f}) × gender")
print(f"Raw gender gap: ${gap:,.0f} (females earn ${abs(gap):,.0f} less)")
print(f"R-squared: {r2:.4f} ({r2*100:.1f}% of variation explained)")

fit1.summary()

# =============================================================================
# STEP 4: Add controls and interaction — how the gap changes
# =============================================================================
# Adding education as a control measures the gap AFTER accounting for education
fit2 = pf.feols('earnings ~ gender + education', data=data, vcov='HC1')

# Adding gender×education interaction allows returns to education to differ by gender
fit3 = pf.feols('earnings ~ gender + education + genderbyeduc', data=data, vcov='HC1')

# Full model with additional controls
fit4 = pf.feols('earnings ~ gender + education + genderbyeduc + age + hours',
                data=data, vcov='HC1')

# Compare how the gender coefficient evolves across models
print(f"{'Model':<12} {'Gender Coef':>14} {'R²':>8}")
print("-" * 36)
for name, m in [('Gender only', fit1), ('+ Education', fit2),
                ('+ Interact', fit3), ('+ Age,Hours', fit4)]:
    g = m.coef()['gender']
    print(f"{name:<12} {g:>14,.0f} {m._r2:>8.4f}")

# =============================================================================
# STEP 5: Scatter plot — visualize separate regression lines by gender
# =============================================================================
# Non-parallel lines indicate different slopes = interaction term is needed
fig, ax = plt.subplots(figsize=(10, 6))

for g, label, color in [(0, 'Male', 'tab:blue'), (1, 'Female', 'tab:red')]:
    subset = data[data['gender'] == g]
    ax.scatter(subset['education'], subset['earnings'], alpha=0.3, s=25,
               label=label, color=color)
    # Fit and plot regression line for each group
    z = np.polyfit(subset['education'], subset['earnings'], 1)
    edu_range = np.linspace(subset['education'].min(), subset['education'].max(), 100)
    ax.plot(edu_range, np.poly1d(z)(edu_range), linewidth=2, color=color,
            label=f'{label} slope: ${z[0]:,.0f}/yr')

ax.set_xlabel('Years of Education')
ax.set_ylabel('Earnings ($)')
ax.set_title('Earnings vs Education by Gender (non-parallel = interaction needed)')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# =============================================================================
# STEP 6: Sets of indicators — worker type and the dummy variable trap
# =============================================================================
# Three mutually exclusive categories: dself, dprivate, dgovt (sum to 1)
# Drop one (dprivate = base) to avoid perfect multicollinearity
fit_worker = pf.feols('earnings ~ dself + dgovt + education + age',
                      data=data, vcov='HC1')

print(f"Base category: Private sector")
print(f"Self-employed vs Private: ${fit_worker.coef()['dself']:,.0f}")
print(f"Government vs Private:   ${fit_worker.coef()['dgovt']:,.0f}")
print(f"R-squared: {fit_worker._r2:.4f}")

fit_worker.summary()

# =============================================================================
# STEP 7: ANOVA — test if earnings differ across worker types
# =============================================================================
# Regression on mutually exclusive indicators = analysis of variance (ANOVA)
group_self = data[data['dself'] == 1]['earnings']
group_priv = data[data['dprivate'] == 1]['earnings']
group_govt = data[data['dgovt'] == 1]['earnings']

f_stat, p_value = f_oneway(group_self, group_priv, group_govt)
print(f"\nANOVA F-statistic: {f_stat:.2f}, p-value: {p_value:.4f}")

# Group means with counts
data['worker_type'] = np.where(data['dself'] == 1, 'Self-employed',
                      np.where(data['dprivate'] == 1, 'Private', 'Government'))
print(data.groupby('worker_type')['earnings'].agg(['mean', 'count']).round(0))
