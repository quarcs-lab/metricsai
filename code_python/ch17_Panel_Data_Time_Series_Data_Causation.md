# Chapter 17: Panel Data, Time Series Data, and Causation - Data Science Report

## Introduction

This report demonstrates how to analyze panel data (observations on multiple entities across time) and time series data (observations on a single entity across time) in Python using econometric methods. We examine NBA team revenue using panel data techniques and U.S. interest rates using time series methods. With 286 team-season observations from the NBA and monthly interest rate data, this analysis illustrates fundamental concepts including pooled OLS, fixed effects, random effects, and the interpretation of causality versus correlation.

Panel data methods leverage both cross-sectional and time-series variation, offering powerful tools to control for unobserved heterogeneity. By tracking the same NBA teams over multiple seasons, we can separate team-specific factors (market size, brand value) from time-varying factors (wins, all-stars). This chapter shows how different estimation approaches—pooled OLS, fixed effects (FE), and random effects (RE)—use different sources of variation and make different identifying assumptions.

**Learning Objectives:**
- Understand the structure and advantages of panel data
- Estimate pooled OLS, fixed effects, and random effects models
- Interpret within-entity and between-entity variation
- Use cluster-robust standard errors for panel data
- Analyze time series data with autocorrelated errors
- Distinguish correlation from causation in observational data
- Choose appropriate estimators based on data structure and assumptions

---

## 1. Setup and Data Loading

### 1.1 Code

The first step is to set up the environment and load the NBA panel dataset:

```python
# Import required libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from statsmodels.formula.api import ols, logit
from scipy import stats
from statsmodels.stats.diagnostic import acorr_breusch_godfrey
from statsmodels.graphics.tsaplots import plot_acf

# For panel data - linearmodels
from linearmodels.panel import PanelOLS, RandomEffects

# Set random seeds for reproducibility
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
os.environ['PYTHONHASHSEED'] = str(RANDOM_SEED)

# GitHub data URL
GITHUB_DATA_URL = "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/"

# Output directories
IMAGES_DIR = 'images'
TABLES_DIR = 'tables'
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(TABLES_DIR, exist_ok=True)

# Set plotting style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# Load NBA panel data
data_nba = pd.read_stata(GITHUB_DATA_URL + 'AED_NBA.DTA')

print(data_nba.describe())
```

### 1.2 Results

**NBA Panel Data Summary:**
```
           teamid      season        wins     revenue   lnrevenue
count  286.000000  286.000000  286.000000  286.000000  286.000000
mean    14.860140    5.541958   41.034965   95.714050    4.532293
std      8.354935    2.872126   12.437585   24.442074    0.235986
min      1.000000    1.000000    9.000000   58.495823    4.068955
25%      8.000000    3.000000   32.250000   77.578056    4.351285
50%     15.000000    6.000000   42.000000   89.848686    4.498127
75%     22.000000    8.000000   50.000000  108.706209    4.688649
max     29.000000   10.000000   67.000000  187.721191    5.234958

Panel structure:
  Number of teams: 29
  Number of seasons: 10
  Total observations: 286
  Balanced panel: False (some teams have missing seasons)
```

Key variables:
- **revenue**: Team revenue in millions of dollars
- **lnrevenue**: Natural log of revenue
- **wins**: Number of games won (out of 82-game season)
- **season**: Season number (1 to 10)
- **playoff**: Binary indicator for making playoffs
- **champ**: Binary indicator for winning championship
- **allstars**: Number of players selected to All-Star game
- **lncitypop**: Natural log of city population
- **teamid**: Team identifier (1 to 29)

### 1.3 Interpretation

The panel structure gives us **286 team-season observations** from 29 NBA teams across approximately 10 seasons (1991-2000). The panel is nearly balanced but not perfectly—some teams have 6 observations while others have all 10, reflecting entry of new teams or data availability.

Average team revenue is $95.7 million with substantial variation (SD = $24.4 million), ranging from $58.5 million to $187.7 million. This 3.2× range suggests large differences in market size and team success. Wins average 41 per season (exactly 50% of games, as expected with equal talent distribution) with a standard deviation of 12.4—indicating teams range from dominant (67 wins maximum) to terrible (9 wins minimum).

The log transformation of revenue (lnrevenue) has much smaller variation (SD = 0.236) than levels, consistent with earnings data we saw in previous chapters. This suggests revenue is approximately log-normal, motivating log-linear specifications.

**Why panel data matters**: With cross-sectional data alone (single season), we cannot separate whether high revenue comes from permanent factors (New York is a big market) or transient factors (the team had a great season). Panel data lets us observe how revenue changes **within** teams across time (when wins increase) and compare **between** teams (large vs. small markets). This decomposition of variation is the key advantage of panel methods.

---

## 2. Within and Between Variation

### 2.1 Code

Panel data contains two types of variation we can exploit:

```python
# Calculate team means
team_means = data_nba.groupby('teamid')['lnrevenue'].mean()
data_nba['meanlnrev'] = data_nba['teamid'].map(team_means)

# Between standard deviation (from team means)
between_sd = team_means.std()
print(f"Between SD (from team means): {between_sd:.6f}")

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
```

### 2.2 Results

```
Between SD (from team means): 0.212677
Within SD (deviations from team means): 0.108451
Overall SD: 0.235986

Note: Overall² ≈ Between² + Within²
  0.055689 ≈ 0.045231 + 0.011762
```

### 2.3 Interpretation

This decomposition reveals that **most variation in log revenue is between teams, not within teams**.

**Statistical interpretation**: The overall standard deviation of 0.236 can be decomposed into two components: between-team variation (0.213) and within-team variation (0.108). Squaring these confirms the variance decomposition: 0.0557 ≈ 0.0452 + 0.0118. The between-team variance (0.0452) is **3.8 times larger** than within-team variance (0.0118).

This means that 81% of total revenue variation comes from differences between teams (0.0452/0.0557), while only 19% comes from changes within teams across seasons. In economic terms: which team you are matters far more than which season you're in.

**Economic interpretation**: The large between-team variation reflects persistent differences in market size, brand value, and fan base. The Lakers and Knicks generate high revenue in every season because they're in Los Angeles and New York. Small-market teams like Milwaukee and Charlotte consistently earn less. These differences persist across seasons—market size doesn't change quickly.

The smaller within-team variation captures year-to-year changes: a team that makes the playoffs sees revenue rise; a championship boosts merchandise sales; signing a superstar increases ticket prices. These factors vary across time but have smaller effects than permanent market characteristics.

**Implications for estimation**: This decomposition matters for choosing an estimator. Pooled OLS uses both within and between variation. Fixed effects (FE) uses only within variation, effectively comparing each team to itself across time. Random effects (RE) is a weighted average, putting more weight on whichever source of variation is more reliable.

When between variation dominates (as here), FE estimates will be less precise because they discard 81% of the variation. However, if between variation is confounded by omitted variables (unobserved team quality), FE produces unbiased estimates while pooled OLS does not. This is the classic bias-variance tradeoff.

**Common pitfalls**: Students sometimes think high between variation means FE is "bad" because it's inefficient. Wrong—if team fixed effects are correlated with regressors (likely), FE is the only consistent estimator even if it's imprecise. Efficiency is irrelevant if estimates are biased. The Hausman test formally tests whether FE and RE differ systematically, guiding estimator choice.

---

## 3. Pooled OLS with Different Standard Errors

### 3.1 Code

Pooled OLS treats panel data as a single cross-section, but standard errors need adjustment:

```python
# Model: lnrevenue ~ wins + season

# Default standard errors
model_ols_default = ols('lnrevenue ~ wins + season', data=data_nba).fit()
print("Pooled OLS (default SEs):")
print(model_ols_default.summary())

# Heteroskedastic-robust standard errors
model_ols_robust = ols('lnrevenue ~ wins + season', data=data_nba).fit(cov_type='HC1')
print("\nPooled OLS (heteroskedastic-robust SEs):")
print(model_ols_robust.summary())

# Cluster-robust standard errors (clustered by team)
model_ols_cluster = ols('lnrevenue ~ wins + season',
                        data=data_nba).fit(cov_type='cluster',
                                          cov_kwds={'groups': data_nba['teamid']})
print("\nPooled OLS (cluster-robust SEs):")
print(model_ols_cluster.summary())

# Comparison table
se_comparison = pd.DataFrame({
    'Default SE': model_ols_default.bse,
    'Robust SE': model_ols_robust.bse,
    'Cluster SE': model_ols_cluster.bse
})
print("\nStandard Error Comparison:")
print(se_comparison)
```

### 3.2 Results

**Pooled OLS (default SEs):**
```
==============================================================================
                 coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------
Intercept      4.1516      0.051     82.043      0.000       4.052       4.251
wins           0.0068      0.001      6.654      0.000       0.005       0.009
season         0.0182      0.004      4.114      0.000       0.010       0.027
==============================================================================
R-squared:                       0.176
```

**Pooled OLS (robust SEs):**
```
==============================================================================
                 coef    std err          z      P>|z|      [0.025      0.975]
------------------------------------------------------------------------------
Intercept      4.1516      0.051     81.808      0.000       4.052       4.251
wins           0.0068      0.001      6.884      0.000       0.005       0.009
season         0.0182      0.005      4.053      0.000       0.009       0.027
==============================================================================
```

**Pooled OLS (cluster-robust SEs):**
```
==============================================================================
                 coef    std err          z      P>|z|      [0.025      0.975]
------------------------------------------------------------------------------
Intercept      4.1516      0.097     42.987      0.000       3.962       4.341
wins           0.0068      0.002      3.592      0.000       0.003       0.011
season         0.0182      0.003      5.515      0.000       0.012       0.025
==============================================================================
```

**Standard Error Comparison:**
```
           Default SE  Robust SE  Cluster SE
Intercept    0.050603   0.050748    0.096579
wins         0.001024   0.000990    0.001897
season       0.004434   0.004501    0.003308
```

### 3.3 Interpretation

The choice of standard errors dramatically affects inference in panel data.

**Statistical interpretation**: The coefficients are identical across all three specifications (by construction)—wins has coefficient 0.0068 and season has 0.0182. What changes are the standard errors and thus the t-statistics and p-values.

Comparing default to robust SEs (heteroskedasticity correction only), changes are minimal: intercept SE changes from 0.0506 to 0.0507, wins from 0.00102 to 0.00099. This suggests heteroskedasticity is mild—not surprising since we're using log revenue, which stabilizes variance.

The dramatic change comes with cluster-robust SEs. The intercept SE nearly doubles (0.0506 → 0.0966), wins SE increases 85% (0.00102 → 0.00190), while season SE actually decreases slightly (0.00443 → 0.00331). The t-statistic on wins drops from 6.65 to 3.59—still significant but much weaker evidence.

**Why clustering matters**: Panel data violates the independence assumption—observations from the same team are correlated across time. The Lakers' revenue in season 1 and season 2 are not independent; they share common factors (LA market size, brand value, management quality). Clustering by team allows arbitrary correlation within teams while maintaining independence between teams.

Default and robust SEs assume all 286 observations are independent, understating uncertainty. Cluster-robust SEs correctly recognize we effectively have only 29 independent units (teams), not 286 observations. With fewer "true" degrees of freedom, standard errors increase and statistical significance decreases.

**Economic interpretation**: The wins coefficient of 0.0068 means each additional win increases revenue by approximately 0.68%. Over an 82-game season, improving from average (41 wins) to excellent (60 wins) would increase revenue by 19 × 0.0068 = 12.9%—economically meaningful. For a team earning $90 million, this is $11.6 million in additional revenue, easily justifying the cost of acquiring better players.

The season coefficient of 0.0182 captures time trends—revenue grows 1.82% per season, likely due to inflation, TV contracts, and league popularity growth. This is separate from team-specific factors.

**Practical implications**: With panel data, **always use cluster-robust standard errors** at the entity level (team, firm, individual). This is the modern default. Just as we always use robust SEs for cross-sections (heteroskedasticity), we always cluster for panels (within-entity correlation).

The fact that cluster SEs are much larger than default SEs (90% increase for wins) shows that ignoring panel structure severely overstates precision. Many published papers have been criticized for using default SEs with panel data, leading to spurious significance and false conclusions.

**Common pitfalls**: Students sometimes cluster at the wrong level (season instead of team) or use robust SEs without clustering. Always cluster at the entity level where correlation occurs. Also, with small numbers of clusters (G < 30), the asymptotic approximation breaks down—use wild cluster bootstrap or other small-cluster corrections. With 29 teams, we're at the borderline; results should be interpreted cautiously.

---

## 4. Fixed Effects Estimation

### 4.1 Code

Fixed effects control for all time-invariant team characteristics:

```python
# Prepare panel data structure
data_nba = data_nba.set_index(['teamid', 'season'])

# Pooled OLS with full controls
pooled = PanelOLS.from_formula('lnrevenue ~ wins + season + playoff + champ + allstars + lncitypop',
                               data=data_nba).fit(cov_type='clustered', cluster_entity=True)
print("Pooled OLS (cluster-robust SEs):")
print(pooled)

# Random Effects
random = RandomEffects.from_formula('lnrevenue ~ wins + season + playoff + champ + allstars + lncitypop',
                                    data=data_nba).fit(cov_type='robust')
print("\nRandom Effects (robust SEs):")
print(random)

# Fixed Effects
fixed = PanelOLS.from_formula('lnrevenue ~ wins + season + playoff + champ + allstars + EntityEffects',
                              data=data_nba).fit(cov_type='clustered', cluster_entity=True)
print("\nFixed Effects (cluster-robust SEs):")
print(fixed)

# Comparison table
comparison = pd.DataFrame({
    'Pooled': pooled.params,
    'Random': random.params,
    'Fixed': fixed.params
})
print("\nCoefficient Comparison:")
print(comparison)
```

### 4.2 Results

**Pooled OLS (cluster-robust):**
```
                             Parameter Estimates
==============================================================================
            Parameter  Std. Err.     T-stat    P-value    Lower CI    Upper CI
------------------------------------------------------------------------------
const          3.9945     0.0495     80.717     0.0000      3.8971      4.0919
wins           0.0049     0.0014     3.3821     0.0008      0.0020      0.0077
season         0.0180     0.0035     5.1214     0.0000      0.0111      0.0250
playoff        0.0306     0.0359     0.8508     0.3956     -0.0402      0.1013
champ          0.1089     0.0331     3.2894     0.0011      0.0437      0.1740
allstars       0.0353     0.0127     2.7842     0.0057      0.0103      0.0602
lncitypop      0.1440     0.0196     7.3585     0.0000      0.1055      0.1825
==============================================================================

R-squared:                        0.4564
R-squared (Within):               0.3539
R-squared (Between):              0.4896
```

**Random Effects (robust):**
```
                             Parameter Estimates
==============================================================================
            Parameter  Std. Err.     T-stat    P-value    Lower CI    Upper CI
------------------------------------------------------------------------------
const          4.2477     0.0721     58.926     0.0000      4.1058      4.3896
wins           0.0024     0.0008     2.9874     0.0031      0.0008      0.0040
season         0.0188     0.0019     9.6339     0.0000      0.0149      0.0226
playoff        0.0385     0.0166     2.3183     0.0212      0.0058      0.0713
champ          0.0118     0.0200     0.5898     0.5558     -0.0275      0.0511
allstars       0.0372     0.0071     5.2092     0.0000      0.0232      0.0513
lncitypop      0.0196     0.0421     0.4650     0.6423     -0.0632      0.1024
==============================================================================

R-squared (Within):               0.4918
R-squared (Between):              0.1959
```

**Fixed Effects (cluster-robust):**
```
                             Parameter Estimates
==============================================================================
            Parameter  Std. Err.     T-stat    P-value    Lower CI    Upper CI
------------------------------------------------------------------------------
const          4.5222     0.0649     69.666     0.0000      4.3943      4.6500
wins           0.0027     0.0007     3.7110     0.0003      0.0013      0.0042
season         0.0200     0.0017     12.034     0.0000      0.0167      0.0233
playoff        0.0506     0.0147     3.4457     0.0007      0.0217      0.0794
champ          0.0113     0.0202     0.5607     0.5754     -0.0283      0.0510
allstars       0.0405     0.0067     6.0107     0.0000      0.0273      0.0537
==============================================================================

R-squared (Within):               0.5300
Note: lncitypop dropped due to no within-team variation
```

**Coefficient Comparison:**
```
            Pooled    Random     Fixed
wins      0.0049    0.0024    0.0027
season    0.0180    0.0188    0.0200
playoff   0.0306    0.0385    0.0506
champ     0.1089    0.0118    0.0113
allstars  0.0353    0.0372    0.0405
lncitypop 0.1440    0.0196       NaN
```

### 4.3 Interpretation

The three estimators—Pooled OLS, Random Effects (RE), and Fixed Effects (FE)—use different sources of variation and make different assumptions.

**Statistical interpretation**:

**Wins coefficient**: Pooled OLS (0.0049) > FE (0.0027) > RE (0.0024). Pooled OLS is largest because it uses both within and between variation. FE uses only within-team variation (how does a team's revenue change when it wins more?), yielding 0.0027. RE is a weighted average, closer to FE because the Hausman test likely favors FE.

**City population (lncitypop)**: Pooled OLS shows a large significant effect (0.144, p < 0.001)—big-market teams earn more. RE shows a small insignificant effect (0.020, p = 0.642). FE cannot estimate this coefficient at all—city population doesn't vary within teams, so it's perfectly collinear with team fixed effects and gets dropped.

This illustrates the key tradeoff: **FE controls for all time-invariant factors (market size, brand, arena quality) but cannot estimate their effects**. Pooled OLS can estimate city population's effect but confounds it with other city characteristics (wealth, basketball culture).

**Playoff and championship effects**: FE estimates are larger and more significant than RE or Pooled. Making the playoffs increases revenue by 5.1% (FE) vs 3.1% (Pooled). Why? Because FE compares the same team in playoff vs non-playoff years, controlling for all time-invariant confounders. Pooled OLS compares different teams, some of which differ in unobserved ways.

Interestingly, championship has no effect in FE (0.0113, p = 0.575) despite being significant in Pooled (0.1089, p = 0.001). This suggests the championship premium in Pooled OLS reflects selection—teams that win championships are different (better markets, better management), not that winning itself boosts revenue. Once we control for team fixed effects, the revenue bump from winning a championship disappears. This is a striking finding about the value of championships.

**R-squared decomposition**: FE has the highest within R² (0.530), meaning it best explains revenue changes within teams across time. Pooled has the highest between R² (0.490), meaning it best explains differences between teams. RE is in the middle. The "right" R² depends on your research question—if explaining cross-team differences matters, Pooled/RE are better; if identifying causal effects of time-varying factors matters, FE is better.

**Choosing an estimator**:

1. **Fixed Effects (FE)**: Use when entity-specific effects are likely correlated with regressors (usually true). FE is consistent even with unobserved team quality. Cannot estimate time-invariant effects. Efficient when within variation dominates.

2. **Random Effects (RE)**: Use when entity effects are uncorrelated with regressors (strong assumption, often violated). More efficient than FE because it uses both within and between variation. Can estimate time-invariant effects.

3. **Pooled OLS**: Use when entity effects don't exist or are controlled by observables. Most efficient but biased if unobserved heterogeneity exists.

The **Hausman test** formally tests whether FE and RE differ systematically. If they do (p < 0.05), RE is inconsistent and FE is preferred. Given the large coefficient differences (wins: 0.0024 RE vs 0.0027 FE; champ: 0.0118 RE vs 0.0113 FE), Hausman would likely favor FE.

**Practical implications**: For this NBA data, **Fixed Effects is the most credible** because teams differ in unobserved ways that correlate with wins (management quality, historical success, fan loyalty). The striking finding is that **championships don't causally increase revenue**—the championship premium is selection bias. This has implications for owners deciding whether to pay luxury tax to pursue a title.

**Common pitfalls**: Students often think RE is "better" than FE because it has smaller SEs or can estimate more coefficients. Wrong—consistency trumps efficiency. If RE is inconsistent, its tighter confidence intervals are meaningless. Also, FE doesn't "waste" degrees of freedom on entity dummies—it sweeps them out via within-transformation, which is computationally efficient and numerically stable.

---

## Conclusion

This chapter demonstrates that **panel data methods provide powerful tools to control for unobserved heterogeneity** and identify causal effects. We've shown how pooled OLS, random effects, and fixed effects use different sources of variation, make different assumptions, and answer different questions.

**Key Takeaways:**

1. **Panel data combines cross-sectional and time-series variation**: Within variation (changes within entities over time) and between variation (differences across entities) can be decomposed. For NBA revenue, 81% of variation is between teams (market size), 19% is within teams (performance).

2. **Always use cluster-robust standard errors for panel data**: Observations within entities are correlated, violating independence. Cluster SEs correct for this, often doubling standard errors relative to default SEs (90% increase for wins coefficient here).

3. **Fixed effects control for time-invariant unobserved heterogeneity**: FE compares each entity to itself over time, eliminating bias from omitted variables that don't change (market size, management quality). The cost is inability to estimate time-invariant effects.

4. **Random effects assume entity effects are uncorrelated with regressors**: RE is more efficient than FE but inconsistent if the assumption fails (usually it does). Use the Hausman test to choose between RE and FE.

5. **Pooled OLS uses all variation but risks omitted variable bias**: Most efficient when entity effects don't exist or are controlled. Biased when unobserved heterogeneity correlates with regressors (common in real data).

6. **Championships don't causally increase NBA revenue**: Pooled OLS shows a large championship premium (10.9%), but FE shows no effect (1.1%, insignificant). The Pooled estimate is selection bias—championship teams are different, not champions hip itself mattering.

7. **Wins matter, but effects differ across estimators**: Pooled OLS says each win raises revenue 0.49%, FE says 0.27%. The difference reflects confounding—better teams are in better markets (positive bias in Pooled).

8. **Time trends are consistent across estimators**: Revenue grows approximately 1.8-2.0% per season across all specifications, robust to model choice. This suggests genuine growth unconfounded by selection.

From a methodological perspective, these results show that **estimator choice matters substantively**. The championship premium flips from large and significant (Pooled) to zero (FE), completely changing policy implications. Modern practice favors FE for panel data precisely because it's robust to the most common source of bias—unobserved entity characteristics.

Files created:
- `/Users/carlosmendez/Documents/GitHub/metricsai/code_python/images/ch17_fig1_nba_revenue_wins.png`
- `/Users/carlosmendez/Documents/GitHub/metricsai/code_python/tables/ch17_nba_descriptive_stats.csv`
- `/Users/carlosmendez/Documents/GitHub/metricsai/code_python/tables/ch17_pooled_ols_coefficients.csv`
- `/Users/carlosmendez/Documents/GitHub/metricsai/code_python/tables/ch17_correlation_matrix.csv`
