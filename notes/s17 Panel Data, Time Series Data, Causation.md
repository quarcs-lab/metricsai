# Chapter 17: Panel Data, Time Series Data, Causation

## Learning Objectives

By the end of this chapter, you will be able to:
- Apply cluster-robust standard errors for cross-section data with grouped observations
- Understand panel data methods including random effects and fixed effects estimators
- Decompose panel data variation into within and between components
- Use instrumental variables (IV) to address endogeneity problems
- Understand the potential outcomes framework for causal inference
- Apply difference-in-differences, regression discontinuity, and matching methods
- Interpret results from logit and probit models for binary outcomes
- Understand exponential regression models for nonnegative data
- Recognize time series issues including autocorrelation and nonstationarity

---

## 17.1 Cross-section Data

- If independent errors use heteroskedastic-robust standard errors.
- If clustered errors with individual $i$ in cluster $g$ we have
- $y_{i g}=\beta_{1}+\beta_{2} x_{2 i g}+\cdots+\beta_{k} x_{k i g}+u_{i g}, g=1, . ., G$.
- For OLS use cluster-robust standard errors where cluster on $g$
- or use the following alternative estimation methods.
- Cluster-specific random effects estimator models the error as
- $u_{i g}=\alpha_{g}+\varepsilon_{i g}$ where $\alpha_{g} \sim\left(0, \sigma_{\alpha}^{2}\right)$ and $\varepsilon_{i g} \sim\left(0, \sigma_{\varepsilon}^{2}\right)$
- advantage: FGLS in this model could be more efficient than OLS.
- Cluster-specific fixed effects estimator again models the error as
- $u_{i g}=\alpha_{g}+u_{i g}$ but treat $\alpha_{g}$ as an individuals-specific fixed effect
- can eliminate $\alpha_{g}$ and consistently estimate $\beta$ 's by OLS in model $y_{i g}-\bar{y}_{g}=\beta_{2}\left(x_{2 i g}-\bar{x}_{2 g}\right)+\cdots+\beta_{k}\left(x_{k i g}-\bar{x}_{k g}\right)+\left(\varepsilon_{i g}-\bar{\varepsilon}_{g}\right)$
- advantage: allows regressors to be correlated with $\alpha_{g}$ so inconsistency only arises if regressors correlated with the $\varepsilon_{i g}$ component of the error.

> **Key Concept**: When observations are clustered (e.g., students within schools, individuals within villages), errors are typically correlated within clusters. Cluster-robust standard errors account for this correlation and can be substantially larger than default or heteroskedastic-robust standard errors.


## 17.2 Panel Data

**In this section:**
- 17.2.1 Variation decomposition in panel data

- Now have data for individual $i$ in years $t=1, \ldots T$
- $y_{i t}=\beta_{1}+\beta_{2} x_{2 i t}+\cdots+\beta_{k} x_{k i t}+u_{i t}, i=1, \ldots, n$
- Use OLS with cluster-robust standard errors where cluster on $i$
- or use the following alternative estimators.
- Random effects and related models
- estimate by FGLS after specifying a model for the correlation over time for a given individual in the error $u_{i t}$.
- Individual-specific fixed effects for individual $i$ in cluster $g$
- now specify $y_{i t}=\alpha_{i}+\beta_{1}+\beta_{2} x_{2 i t}+\cdots+\beta_{k} x_{k i t}+u_{i t}$
- can eliminate $\alpha_{i}$ and consistently estimate $\beta$ 's by OLS in model $y_{i t}-\bar{y}_{i}=\beta_{2}\left(x_{2 i t}-\bar{x}_{2 i}\right)+\cdots+\beta_{k}\left(x_{k i t}-\bar{x}_{k i}\right)+\left(\varepsilon_{i t}-\bar{\varepsilon}_{t}\right)$
- advantage: allows regressors to be correlated with $\alpha_{t}$ so inconsistency only arises if regressors correlated with $\varepsilon_{i t}$.
- Dynamic models allow lagged $y_{i t}$ 's as regressors
- more complicated.


### 17.2.1 Variation Decomposition in Panel Data

- With panel data, variables potentially vary over both time and individuals.
- This variation for a variable $z_{i t}$ can be decomposed as follows.
- Total variation is the variation of $z_{i t}$ around the overall mean $\bar{z}=\frac{1}{n T} \sum_{i=1}^{n} \sum_{t=1}^{T} z_{i t}$.
- Within variation is variation over time for a given individual, the variation of $z_{i t}$ around the individual mean $\bar{z}_{i}=\frac{1}{T} \sum_{t=1}^{T} z_{i t}$.
- Between variation is variation across individuals, the variation of the individual mean $\bar{z}_{i}$ around the overall mean $\bar{z}$.
- The corresponding decomposition for the overall variance is

$$
\begin{array}{ll}
\text { Within variance: } & s_{\mathrm{W}}^{2}=\frac{1}{n T-1} \sum_{i} \sum_{t}\left(z_{i t}-\bar{z}_{i}\right)^{2} \\
\text { Between variance: } & s_{\mathrm{B}}^{2}=\frac{1}{n-1} \sum_{i}\left(\bar{z}_{i}-\bar{z}\right)^{2} \\
\text { Overall variance: } & s_{\mathrm{O}}^{2}=\frac{1}{n T-1} \sum_{i} \sum_{t}\left(z_{i t}-\bar{z}\right)^{2} .
\end{array}
$$

- OLS (and random effects) use both within and between variation.
- The fixed effects estimator uses only within variation.

> **Key Concept**: Panel data variation can be decomposed into within variation (over time for each individual) and between variation (across individuals). Fixed effects estimators use only within variation, while OLS and random effects use both. This distinction is crucial for understanding what each estimator identifies.


## 17.3 Panel Data Example: NBA Team Revenue

**In this section:**
- 17.3.1 Regression results: pooled OLS, random effects, fixed effects
- 17.3.2 Interpretation of results

- Dataset NBA has data on 29 teams for the 10 seasons 2001-02 to 2010-11
- view as short panel dataset ( $T$ fixed and $n$ large).

**Example 17.1**: Panel Data Summary Statistics for NBA Team Revenue

| Variable | Definition | Mean | Standard deviation |  |  |
| :--- | :--- | :--- | :--- | :--- | :--- |
|  |  |  | Overall | Between | Within |
| Revenue | Team revenue in 1999 \$millions | 95.714 | 24.442 | 22.467 | 10.319 |
| Lnrevenue | Natural logarithm of team revenue | 4.532 | 0.236 | 0.213 | 0.108 |
| Wins | Number of wins including playoff | 41.04 | 12.438 | 7.044 | 10.356 |
| Playoff | $=1$ if made playoffs in prev.season | 0.545 | 0.499 | 0.243 | 0.439 |
| Champ | $=1$ if champion in previous season | 0.035 | 0.184 | 0.094 | 0.159 |
| Allstars | Number of players voted Allstars | 0.860 | 0.871 | 0.524 | 0.704 |
| Lncitypop | Log of city population in millions | 1.301 | 0.801 | 0.807 | 0.097 |
| Teamid | Team identifier | 14.86 | 8.355 | 8.517 | 0.000 |
| Season | Season identifier | 5.54 | 2.872 | 0.371 | 2.858 |

### 17.3.1 Regression Results: Pooled OLS, Random Effects, Fixed Effects

- Log-linear model: dependent variable is natural logarithm of team revenue.

**Example 17.2**: Panel Data Regression Results (Pooled OLS, Random Effects, Fixed Effects)

| Variable | Estimator, coefficients and standard errors |  |  |  |  |  |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
|  | Pooled Het-robust | OLS Robust | Random Default | Effects Robust | Fixed Default | Effects Robust |
|  |  |  |  |  |  |  |
| Wins | .0049*** (.0014) | .0049*** (.0015) | .0024*** (.0008) | .0024*** (.0008) | .0027*** (.0007) | .0027*** (.0007) |
| Season | .0180*** (.0035) | 0180*** (.0033) | .0188*** (.0017) | .0188*** (.0033) | .0200*** (.0017) | .0200*** (.0029) |
| Playoff | . 0306 (.0359) | . 0306 (.0447) | .0385** (.0176) | .0385* (.0200) | 0362** (.0167) | .0362* (.0209) |
| Champion | 1089*** (.0331) | 1089*** (.0473) | . 0118 (.0316) | . 0118 (.0163) | 0052 (.0300) | 0052 (.0167) |
| Allstars | 0353*** (.0127) | .0353* (.0178) | 0372*** (.0075) | 0372*** (.0066) | 0356*** (.0071) | .0356*** (.0068) |
| Lncitypop | 1440*** (.0196) | 1440*** (.0598) | . 0196 (.0315) | . 0196 (.0872) | -.2021*** (.0491) | -.2021*** (.0632) |
| Intercept | 3.9945 (.0491) | 3.9945 (.0596) | 4.2477 (.0560) | 4.2477 (.1076) | 4.5222 (.0649) | 4.5222 (.0957) |
| Observations | 286 | 286 | 286 | 286 | 286 | 286 |

[^0]
### 17.3.2 Interpretation of Results

- Pooled OLS, random effects and fixed effects estimators
- use cluster-robust standard errors, not the default
- asterisks: single for $10 \%$, double for $5 \%$, triple for $1 \%$.
- The fixed effects slope estimate of 0.0027 means that one more win per season is associated with a $0.27 \%$ increase in team revenue, after controlling for city characteristics, some immediate past performance measures, and unobserved team characteristics $\left(\alpha_{i} m\right)$ that are time invariant.

> **Key Concept**: Fixed effects control for unobserved time-invariant individual characteristics (like team quality, city appeal). The coefficient of 0.0027 means one more win increases team revenue by 0.27% after controlling for observable factors and unobservable team-specific effects.


## 17.4 Instrumental Variables

**In this section:**
- 17.4.1 IV estimator and interpretation

- Problem: in model $y=\beta_{1}+\beta_{2} x+u$ we have $\mathrm{E}[u \mid x]=0$
- then $x$ is endogenous and OLS is inconsistent.
- Solution: assume there exists an instrument $z$ that
- does not belong in the model for $y$ (exclusion restriction)
- is correlated with $x$.

1. OLS consistent
![](https://cdn.mathpix.com/cropped/02e4f915-8a26-4777-8299-892404f92454-10.jpg?height=99&width=163&top_left_y=582&top_left_x=250)
2. OLS inconsistent
![](https://cdn.mathpix.com/cropped/02e4f915-8a26-4777-8299-892404f92454-10.jpg?height=99&width=163&top_left_y=582&top_left_x=558)
3. IV consistent
![](https://cdn.mathpix.com/cropped/02e4f915-8a26-4777-8299-892404f92454-10.jpg?height=104&width=299&top_left_y=578&top_left_x=895)

- Note: This is only possible if one can find a valid instrument.


### 17.4.1 IV Estimator and Interpretation

- The instrumental variables (IV) estimator of $\beta_{2}$ is

$$
b_{I V}=\frac{\sum_{i}\left(z_{i}-\bar{z}\right)\left(y_{i}-\bar{y}\right)}{\sum_{i}\left(z_{i}-\bar{z}\right)\left(x_{i}-\bar{x}\right)}
$$

- Intuitively it estimates $\frac{\Delta y}{\Delta x}$ as the ratio $\frac{\Delta y}{\Delta z} / \frac{\Delta z}{\Delta x}$
- if one-unit change in $z$ is associated with a one unit increase in $x$ of 2 and increase of $y$ of 3 then $b_{I V}=3 / 2=1.5$.
- and this can be given a causal interpretation of $\frac{\Delta y}{\Delta x}=1.5$.
- Can extend to multiple regression
- exogenous regressors (uncorrelated with $u$ ) are instruments for themselves
- if more instruments ( $z$ ) than endogenous regressors ( $x$ ) then use two-stage least squares.
- Example: in log-wage model treat schooling as endogenous
- use distance to closest college as an instrument.

> **Key Concept**: Instrumental variables (IV) provide consistent estimates when a regressor is endogenous (correlated with the error). A valid instrument must be (1) correlated with the endogenous regressor and (2) uncorrelated with the error (exclusion restriction). The IV estimator can be interpreted as measuring the causal effect of x on y.


## 17.5 Causal Inference: An Overview

**In this section:**
- 17.5.1 Potential outcomes framework
- 17.5.2 Randomized control trials and difference-in-differences
- 17.5.3 Regression adjustment and control functions
- 17.5.4 Regression discontinuity design
- 17.5.5 Local average treatment effects (LATE)
- 17.5.6 Inverse probability weighting and matching

- Causal inference
- goal is to get causal estimate of effect of $x$ on $z$ using observational data.
- Stereotypical problem is returns to training where self-select into training
- $y_{i}=\beta_{1}+\gamma d_{i}+u_{i}$ where $d_{i}$ is a binary indicator for training
- people choose to get training and we expect that those with higher (unobserved) expected benefits to training will select training
- then $\mathrm{E}\left[u_{i} \mid d_{i}=1\right]>\mathrm{E}\left[u_{i} \mid d_{i}=0\right]$ so $\mathrm{E}\left[u_{i} \mid d_{i}\right] \neq 0$.
- There are many different methods to nonetheless obtain a causal estimate
- each method has its own distinct assumptions and data requirements.


### 17.5.1 Potential Outcomes Framework

- Potential outcomes model or Rubin causal model
- standard framework that is used.
- Consider a binary treatment $D$
- $D_{i}=1$ for individual $i$ if treated
- $D_{i}=0$ if individual $i$ is not treated (a control).
- There are two potential outcomes for $Y_{i}$
- $Y_{1 i}$ if $D_{i}=1$ and $Y_{0 i}$ if $D_{i}=0$.
- Interest lies in estimating the treatment affect $\gamma_{i} \equiv Y_{1 i}-Y_{0 i}$
- we cannot estimate $\gamma_{i}$ as we only observe one of $Y_{1 i}$ and $Y_{0 i}$
- so restrict attention to more aggregated measures.
- The average treatment effect (ATE) in the population is

$$
\mathrm{ATE}=E\left[\gamma_{i}\right]=E\left[Y_{1 i}-Y_{0 i}\right] .
$$

- The average treatment effect on the treated (ATET) is

$$
\mathrm{ATET}=E\left[\gamma_{i} \mid D_{i}=1\right]=E\left[\left(Y_{1 i}-Y_{0 i}\right) \mid D_{i}=1\right] .
$$

> **Key Concept**: The potential outcomes framework formalizes causal inference by defining treatment effects as the difference between potential outcomes under treatment and control. Since we only observe one outcome per individual, we focus on average treatment effects (ATE) or average treatment effects on the treated (ATET).

### 17.5.2 Randomized Control Trials and Difference-in-Differences

- A random controlled trial ( RCT ) is an experiment where randomly assign people to treatment and control.
- then estimate ATE by the difference in means $\bar{y}_{1 i}-\bar{y}_{0 i}$
- done more often in economics but still not a lot.
- A difference-in-difference estimate uses the following
- simplest case two periods of time
- no individuals are treated in the first period
- some are treated in the second period and some are not
- $\widehat{\text { ATET }}=$ average change in $y$ over time for those treated in second period minus average change in $y$ over time for those not treated in second period.
- example of a natural experiment.

> **Key Concept**: Randomized control trials (RCTs) provide causal estimates by randomly assigning treatment, ensuring treatment is uncorrelated with potential outcomes. Difference-in-differences (DiD) estimates the treatment effect as the change over time for treated individuals minus the change for untreated individuals, controlling for time trends.


### 17.5.3 Regression Adjustment and Control Functions

- Control function approach adds controls
- $\widehat{\mathrm{ATE}}=\widehat{\gamma}$ from OLS of $y_{i}=\beta_{1}+\gamma d_{i}+\beta_{2} x_{2 i}+\cdots+\beta_{k} x_{k i}+u_{i}$
- need to ensure $d_{i}$ and $u_{i}$ uncorrelated once the controls are added.
- Richer regression adjustment estimator runs separate regressions
- regress $y_{i}$ on intercept and $x_{2 i}, \ldots, x_{k i}$ for $d_{i}=1$ only compute $\frac{1}{n} \sum_{i=1}^{n} \widehat{y}_{1 i}$ where $\widehat{y}_{1 i}$ is resulting prediction for $d_{i}=0$ and $d_{i}=1$.
- regress $y_{i}$ on intercept and $x_{2 i}, \ldots, x_{k i}$ for $d_{i}=0$ only compute $\frac{1}{n} \sum_{i=1}^{n} \widehat{y}_{0 i}$ where $\widehat{y}_{1 i}$ is resulting prediction for $d_{i}=0$ and $d_{i}=1$.
- $\widehat{\mathrm{ATE}}=\frac{1}{N} \sum_{i=1}^{N} \hat{y}_{1 i}-\frac{1}{N} \sum_{i=1}^{N} \hat{y}_{0 i}$.
- Fixed effects estimators
- $y_{i t}=\beta_{1}+\gamma d_{i t}+\beta_{2} x_{2 i t}+\cdots+\beta_{k} x_{k i t}+\alpha_{i}+\varepsilon_{i t}$
- need to assume $d_{i t}$ and $\varepsilon_{i t}$ uncorrelated once the controls and $\alpha_{i}$ are added.

> **Key Concept**: Regression adjustment adds control variables to make treatment assignment independent of potential outcomes conditional on the controls. Fixed effects models extend this by controlling for unobserved individual-specific effects that are constant over time.


### 17.5.4 Regression Discontinuity Design

- Regression discontinuity design (RDD)

- a threshold variable determines treatment status
- e.g. admission into treatment is based on a score denoted $s$, with scores above 100 , say, leading to treatment $(d=1)$.
- A simple RDD estimate compares the average value of $y$ for individuals on either side of the threshold.
- Complication: usually the outcome variable $y$ itself varies with $s$
- suppose that $y=\beta_{1}+\beta_{2} s+u$ without treatment
- then a simple RDD estimate of ATET is $\widehat{\gamma}$ from OLS of

$$
\star y_{i}=\beta_{1}+\gamma d_{i}+\beta_{2} s_{i}+u_{i} .
$$

- In practice more flexible models are used
- e.g. different linear or quadratic trends on either side of the threshold
- estimates are focused on observations close to the threshold
- or nonparametric methods are used either side of the threshold.

> **Key Concept**: Regression discontinuity design (RDD) exploits threshold-based treatment assignment. By comparing outcomes just above and below the threshold (where treatment changes discontinuously), RDD provides a local causal estimate for individuals near the threshold.


### 17.5.5 Local Average Treatment Effects (LATE)

- Instrumental variables (IV) estimator from chapter 17.4
- IV estimator in model $y_{i}=\beta_{1}+\gamma d_{i}$ where $z_{i}$ is instrument for $x_{i}$.
- This restricts constant treatment effect $\gamma$ for all individuals.
- Instead allow different (heterogeneous) treatment effects $\gamma_{i}$.
- Specialize to a binary treatment $D$ and suppose for simplicity that higher value of $Z$ makes selection into treatment ( $D=1$ ) more likely.
- Distinguish between four types of people:
- (1) Always-takers chose treatment $(D=1)$ regardless of the value of $Z$
- (2) Never-takers never chose treatment ( $D=0$ ) regardless of the value of $Z$;
- (3) Compliers are induced into treatment so $D=1$ when $Z=1$ and $D=0$ when $Z=0$
- (4) Defiers are induced away from treatment so $D=0$ when $Z=1$ and $D=1$ when $Z=0$.
- Then under the crucial and nontestable assumption that there are no defiers, also called the monotonicity assumption, the IV estimator


### 17.5.6 Inverse Probability Weighting and Matching

- Inverse probability weighting uses weighted averages of the outcome
- binary treatment $d_{i}=1$ or $d_{i}=0$.
- we observe $d_{i} y_{i}$ if the individual is treated and $\left(1-d_{i}\right) y_{i}$ if untreated
- ATE is the weighted average $\frac{1}{N} \sum_{i=1}^{n} w_{i}\left\{d_{i} y_{i}-\left(1-d_{i}\right) y_{i}\right\}$
$\star$ where the weights $w_{i}=1 / \widehat{p}_{i}$ if treated and $w_{i}=1 /\left(1-\widehat{p}_{i}\right)$ if untreated
$\star$ and $\widehat{p}_{i}=\widehat{\operatorname{Pr}}\left(d_{i}=1 \mid\left(x_{2 i}, \ldots, x_{k i}\right)\right.$ is the propensity score, the predicted probability of treatment.
- key: assume that the weights control for selection into treatment.
- Matching compares treated person to a similar (on $x$ 's) untreated
- nearest neighbor matching compare outcome for each treated observation to the average outcome of the $k$ observations whose values of $x_{2}, \ldots, x_{k}$ are closest to those for the treated observation.
- propensity score matching instead compares outcomes with similar probability of treatment..

> **Key Concept**: Inverse probability weighting (IPW) and matching methods estimate treatment effects by comparing treated and untreated individuals with similar characteristics. The propensity score—the probability of treatment given covariates—is key to both approaches.


## 17.6 Nonlinear Regression Models

**In this section:**
- 17.6.1 Probit model
- 17.6.2 Exponential conditional mean model

- Binary outcome $y_{i}=0$ or 1
- model $\operatorname{Pr}\left[y_{i}=1 \mid\right.$ regressors $]$ using a logit model or probit model
- maximum likelihood estimation by computer is straightforward, interpretation of estimates is more difficult.
- The logit model specifies that

**Example 17.3**: Logit Model Specification

$$
\begin{aligned}
& \operatorname{Pr}\left[y=1 \mid x_{2}, \ldots, x_{k}\right]=\frac{\exp \left(\beta_{1}+\beta_{2} x_{2}+\cdots+\beta_{k} x_{k}\right)}{1+\exp \left(\beta_{1}+\beta_{2} x_{2}+\cdots+\beta_{k} x_{k}\right)} \\
& \operatorname{Pr}\left[y=0 \mid x_{2}, \ldots, x_{k}\right]=1-\operatorname{Pr}\left[y=1 \mid x_{2}, \ldots, x_{k}\right]
\end{aligned}
$$

- For the $j^{t h}$ regressor $\mathrm{ME}_{j}=\frac{\Delta \widehat{p}}{\Delta x_{j}}=\widehat{p}(1-\widehat{p}) b_{j}$
- where $\widehat{p}$ is the predicted probability
- $\mathrm{ME}_{j}\left|\leq 0.25 \times\left|b_{j}\right|\right.$ and sign of $b_{j}$ gives sign of ME.

> **Key Concept**: For binary outcomes, logit and probit models estimate the probability of the outcome being 1 as a function of regressors. Unlike linear probability models, these ensure predicted probabilities lie between 0 and 1. Marginal effects (not coefficients) give the change in probability for a unit change in a regressor.


### 17.6.1 Probit Model

- The probit model specifies that

**Example 17.4**: Probit Model Specification

$$
\begin{aligned}
& \operatorname{Pr}\left[y=1 \mid x_{2}, \ldots, x_{k}\right]=\Phi\left(\beta_{1}+\beta_{2} x_{2}+\cdots+\beta_{k} x_{k}\right) \\
& \operatorname{Pr}\left[y=0 \mid x_{2}, \ldots, x_{k}\right]=1-\operatorname{Pr}\left[y=1 \mid x_{2}, \ldots, x_{k}\right]
\end{aligned}
$$

where $\Phi(\cdot)$ is the cumulative distribution function of the standard normal distribution.

- For the probit model $\mathrm{ME}_{j}=\phi(\widehat{p}) b_{j}$
- where $\phi(\cdot)$ is the standard normal density function
- $\mathrm{ME}_{j}\left|\leq 0.4 \times\left|b_{j}\right|\right.$ and sign of $b_{j}$ gives sign of ME.


### 17.6.2 Exponential Conditional Mean Model

- Suppose the conditional mean is exponential, so that

**Example 17.5**: Exponential Conditional Mean Model

$$
\mathrm{E}\left[y \mid x_{2}, \ldots, x_{k}\right]=\exp \left(\beta_{1}+\beta_{2} x_{2}+\cdots+\beta_{k} x_{k}\right) .
$$

- This model is applicable to nonnegative data as $\mathrm{E}\left[y \mid x_{2}, \ldots, x_{k}\right]>0$.
- Estimation is by a method called quasi-maximum likelihood
- rather than by least squares regression
- $b_{1}, b_{2}, \ldots, b_{k}$ maximize $\sum_{i=1}^{n}\left\{y_{i} \ln \mu_{i}-\mu_{i}\right\}$ where $\mu_{i}=\exp \left(b_{1}+b_{2} x_{2 i}+\cdots+b_{k} x_{k i}\right)$.
- Now $\mathrm{ME}_{j}=\frac{\Delta \hat{y}}{\Delta x_{j}}=\widehat{y} b_{j}$
- where $\widehat{y}$ is the predicted value of $y$
- and $\mathrm{AME}=\bar{y} b_{j}$.
- Coefficients $b_{j}$ can be directly interpreted as semi-elasticities.

> **Key Concept**: Exponential regression models are appropriate for nonnegative outcomes (like counts or expenditures). The exponential form ensures predictions are positive. Coefficients can be interpreted as semi-elasticities: a one-unit change in x changes y by approximately 100×β percent.


## 17.7 Time Series Data

- Topics covered in the text
- HAC Standard errors
- stationary process and data transformation
- sample autocorrelations
- tests for autocorrelation
- autoregressive models
- finite distributed lag models
- autoregressive distributed lag models
- autoregressive error models
- nonstationary time series and unit roots
- spurious regression
- regression with nonstationary data
- forecasting.


## 17.8 Time Series Data: U.S. Treasury Security Interest Rates

- Dataset INTERESTRATES has monthly data from January 1982 to January 2015 on 1-year and 10-year treasury note constant maturity rates.
- Application regresses 10 -year rate on 1 -year rate.

---

## Key Takeaways

**Panel Data Methods (Sections 17.1-17.3):**
- Use cluster-robust standard errors when observations are grouped (students in schools, workers in firms, individuals in villages)
- Cluster-robust SE account for within-cluster correlation and can be substantially larger than default or heteroskedastic-robust SE
- Panel data methods include pooled OLS, random effects, and fixed effects estimators
- Panel data variation decomposes into within variation (over time for each individual) and between variation (across individuals)
- Fixed effects control for unobserved time-invariant individual characteristics (α_i)
- Fixed effects use only within variation; random effects and OLS use both within and between variation
- NBA example: one more win increases team revenue by 0.27% (fixed effects estimate with cluster-robust SE)
- Always use cluster-robust (not default) standard errors for clustered or panel data
- Random effects assume regressors are uncorrelated with individual effects; fixed effects allow correlation

**Instrumental Variables (Section 17.4):**
- IV addresses endogeneity when a regressor x is correlated with the error term (E[u|x] ≠ 0)
- A valid instrument z must satisfy two conditions: (1) relevance (correlated with x) and (2) exclusion restriction (uncorrelated with u)
- The IV estimator provides consistent causal estimates under these assumptions
- IV formula: b_IV = Σ(z_i - z̄)(y_i - ȳ) / Σ(z_i - z̄)(x_i - x̄)
- Intuition: IV estimates Δy/Δx as the ratio (Δy/Δz) / (Δx/Δz)
- Two-stage least squares (2SLS) extends IV to multiple endogenous regressors
- Example: distance to college as an instrument for schooling in wage equations
- With multiple instruments and endogenous regressors, use 2SLS estimation

**Causal Inference Framework (Section 17.5):**
- The potential outcomes framework defines treatment effects as Y_1i - Y_0i (potential outcomes under treatment vs. control)
- Average treatment effect (ATE) = E[Y_1i - Y_0i] for the population
- Average treatment effect on the treated (ATET) = E[Y_1i - Y_0i | D_i = 1]
- Randomized control trials (RCTs) provide gold-standard causal estimates by randomly assigning treatment
- RCTs ensure treatment is uncorrelated with potential outcomes (E[u|D] = 0)
- Difference-in-differences (DiD) estimates ATET as (change for treated) - (change for untreated)
- DiD controls for time trends affecting both treatment and control groups
- Regression adjustment adds control variables to make treatment assignment independent of outcomes conditional on controls
- Fixed effects models control for time-invariant unobserved heterogeneity (α_i) in addition to observed controls

**Regression Discontinuity and Advanced Methods (Section 17.5 continued):**
- Regression discontinuity design (RDD) exploits threshold-based treatment assignment
- RDD compares outcomes just above and below the threshold where treatment changes discontinuously
- RDD provides local causal estimate for individuals near the threshold
- In practice, RDD uses flexible models (different trends on each side) or nonparametric methods
- Local average treatment effect (LATE) from IV estimates causal effect for compliers
- Compliers are individuals induced into treatment by the instrument (D=1 when Z=1, D=0 when Z=0)
- LATE requires monotonicity assumption (no defiers)
- Always-takers and never-takers are unaffected by the instrument

**Matching and Propensity Score Methods (Section 17.5 continued):**
- Inverse probability weighting (IPW) uses weighted averages to estimate ATE
- Weights are w_i = 1/p̂_i if treated, w_i = 1/(1-p̂_i) if untreated
- Propensity score p̂_i = Pr(D_i=1 | X_i) is the predicted probability of treatment given covariates
- IPW assumes selection into treatment is controlled by the propensity score weights
- Nearest neighbor matching compares each treated observation to k similar untreated observations
- Propensity score matching compares observations with similar probability of treatment
- All matching methods assume selection on observables (no unobserved confounding)

**Nonlinear Regression Models (Section 17.6):**
- Logit and probit models are appropriate for binary (0/1) outcomes
- Logit: Pr[y=1|x] = exp(β'x) / (1 + exp(β'x))
- Probit: Pr[y=1|x] = Φ(β'x) where Φ is the standard normal CDF
- These models ensure predicted probabilities lie between 0 and 1 (unlike linear probability model)
- Marginal effects (not raw coefficients) give the change in probability for a unit change in x
- For logit: ME_j ≤ 0.25 × |b_j|; for probit: ME_j ≤ 0.4 × |b_j|
- Exponential regression models are appropriate for nonnegative data: E[y|x] = exp(β'x)
- Exponential form ensures predictions are positive (useful for counts, expenditures)
- Coefficients in exponential models are semi-elasticities: one-unit change in x changes y by approximately 100×β percent
- All nonlinear models are estimated by maximum likelihood, not OLS

**Time Series Methods (Sections 17.7-17.8):**
- Time series data requires special methods due to autocorrelation (correlation over time in errors)
- HAC standard errors account for both heteroskedasticity and autocorrelation
- Stationarity is crucial: mean, variance, and covariances are constant over time
- Nonstationary series can lead to spurious regression (high R² but no true relationship)
- Autoregressive (AR) models include lagged dependent variables as regressors: y_t = α + ρy_{t-1} + ε_t
- Distributed lag models include current and lagged values of regressors
- Autoregressive distributed lag (ARDL) models combine both approaches
- Unit root tests (Dickey-Fuller, ADF) determine whether a series is stationary or nonstationary
- If nonstationary, use first differences or cointegration methods
- Forecasting methods include AR, ARMA (autoregressive moving average), and VAR (vector autoregression)
- Time series econometrics is a specialized field requiring careful treatment of dynamics and nonstationarity

---

[^0]:    (C) A. Colin Cameron Univ. of Calif. Davis

