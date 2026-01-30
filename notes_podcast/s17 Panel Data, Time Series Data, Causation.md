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
- If clustered errors with individual i in cluster g we have
- y-sub-i-g equals beta-one plus beta-two times x-sub-2-i-g plus dot-dot-dot plus beta-k times x-sub-k-i-g plus u-sub-i-g, for g equals 1 through G.
- For OLS use cluster-robust standard errors where cluster on g
- or use the following alternative estimation methods.
- Cluster-specific random effects estimator models the error as
- u-sub-i-g equals alpha-sub-g plus epsilon-sub-i-g, where alpha-sub-g is distributed with mean 0 and variance sigma-sub-alpha squared, and epsilon-sub-i-g is distributed with mean 0 and variance sigma-sub-epsilon squared
- advantage: FGLS in this model could be more efficient than OLS.
- Cluster-specific fixed effects estimator again models the error as
- u-sub-i-g equals alpha-sub-g plus epsilon-sub-i-g, but treat alpha-sub-g as an individual-specific fixed effect
- can eliminate alpha-sub-g and consistently estimate the betas by OLS in model y-sub-i-g minus y-bar-sub-g equals beta-two times the quantity x-sub-2-i-g minus x-bar-sub-2-g, plus dot-dot-dot plus beta-k times the quantity x-sub-k-i-g minus x-bar-sub-k-g, plus the quantity epsilon-sub-i-g minus epsilon-bar-sub-g
- advantage: allows regressors to be correlated with alpha-sub-g, so inconsistency only arises if regressors correlated with the epsilon-sub-i-g component of the error.

> **Key Concept**: When observations are clustered (e.g., students within schools, individuals within villages), errors are typically correlated within clusters. Cluster-robust standard errors account for this correlation and can be substantially larger than default or heteroskedastic-robust standard errors.


## 17.2 Panel Data

**In this section:**
- 17.2.1 Variation decomposition in panel data

- Now have data for individual i in years t equals 1 through T
- y-sub-i-t equals beta-one plus beta-two times x-sub-2-i-t plus dot-dot-dot plus beta-k times x-sub-k-i-t plus u-sub-i-t, for i equals 1 through n
- Use OLS with cluster-robust standard errors where cluster on i
- or use the following alternative estimators.
- Random effects and related models
- estimate by FGLS after specifying a model for the correlation over time for a given individual in the error u-sub-i-t.
- Individual-specific fixed effects for individual i in cluster g
- now specify y-sub-i-t equals alpha-sub-i plus beta-one plus beta-two times x-sub-2-i-t plus dot-dot-dot plus beta-k times x-sub-k-i-t plus u-sub-i-t
- can eliminate alpha-sub-i and consistently estimate the betas by OLS in model y-sub-i-t minus y-bar-sub-i equals beta-two times the quantity x-sub-2-i-t minus x-bar-sub-2-i, plus dot-dot-dot plus beta-k times the quantity x-sub-k-i-t minus x-bar-sub-k-i, plus the quantity epsilon-sub-i-t minus epsilon-bar-sub-t
- advantage: allows regressors to be correlated with alpha-sub-t, so inconsistency only arises if regressors correlated with epsilon-sub-i-t.
- Dynamic models allow lagged y-sub-i-t's as regressors
- more complicated.


### 17.2.1 Variation Decomposition in Panel Data

- With panel data, variables potentially vary over both time and individuals.
- This variation for a variable z-sub-i-t can be decomposed as follows.
- Total variation is the variation of z-sub-i-t around the overall mean z-bar equals one over n times T, times the double sum from i equals 1 to n and t equals 1 to T of z-sub-i-t.
- Within variation is variation over time for a given individual, the variation of z-sub-i-t around the individual mean z-bar-sub-i equals one over T times the sum from t equals 1 to T of z-sub-i-t.
- Between variation is variation across individuals, the variation of the individual mean z-bar-sub-i around the overall mean z-bar.
- The corresponding decomposition for the overall variance is

Within variance: s-sub-W squared equals one over n times T minus 1, times the double sum over i and t of the quantity z-sub-i-t minus z-bar-sub-i, all squared. Between variance: s-sub-B squared equals one over n minus 1, times the sum over i of the quantity z-bar-sub-i minus z-bar, all squared. Overall variance: s-sub-O squared equals one over n times T minus 1, times the double sum over i and t of the quantity z-sub-i-t minus z-bar, all squared.

- OLS (and random effects) use both within and between variation.
- The fixed effects estimator uses only within variation.

> **Key Concept**: Panel data variation can be decomposed into within variation (over time for each individual) and between variation (across individuals). Fixed effects estimators use only within variation, while OLS and random effects use both. This distinction is crucial for understanding what each estimator identifies.


## 17.3 Panel Data Example: NBA Team Revenue

**In this section:**
- 17.3.1 Regression results: pooled OLS, random effects, fixed effects
- 17.3.2 Interpretation of results

- Dataset NBA has data on 29 teams for the 10 seasons 2001-02 to 2010-11
- view as short panel dataset (T fixed and n large).

**Example 17.1**: Panel Data Summary Statistics for NBA Team Revenue

| Variable | Definition | Mean | Standard deviation |  |  |
| :--- | :--- | :--- | :--- | :--- | :--- |
|  |  |  | Overall | Between | Within |
| Revenue | Team revenue in 1999 \$millions | 95.714 | 24.442 | 22.467 | 10.319 |
| Lnrevenue | Natural logarithm of team revenue | 4.532 | 0.236 | 0.213 | 0.108 |
| Wins | Number of wins including playoff | 41.04 | 12.438 | 7.044 | 10.356 |
| Playoff | equals 1 if made playoffs in prev.season | 0.545 | 0.499 | 0.243 | 0.439 |
| Champ | equals 1 if champion in previous season | 0.035 | 0.184 | 0.094 | 0.159 |
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

### 17.3.2 Interpretation of Results

- Pooled OLS, random effects and fixed effects estimators
- use cluster-robust standard errors, not the default
- asterisks: single for 10 percent, double for 5 percent, triple for 1 percent.
- The fixed effects slope estimate of 0.0027 means that one more win per season is associated with a 0.27 percent increase in team revenue, after controlling for city characteristics, some immediate past performance measures, and unobserved team characteristics (alpha-sub-i) that are time invariant.

> **Key Concept**: Fixed effects control for unobserved time-invariant individual characteristics (like team quality, city appeal). The coefficient of 0.0027 means one more win increases team revenue by 0.27% after controlling for observable factors and unobservable team-specific effects.


## 17.4 Instrumental Variables

**In this section:**
- 17.4.1 IV estimator and interpretation

- Problem: in model y equals beta-one plus beta-two times x plus u, we have the expected value of u given x not equal to 0
- then x is endogenous and OLS is inconsistent.
- Solution: assume there exists an instrument z that
- does not belong in the model for y (exclusion restriction)
- is correlated with x.

1. OLS consistent
![](https://cdn.mathpix.com/cropped/02e4f915-8a26-4777-8299-892404f92454-10.jpg?height=99&width=163&top_left_y=582&top_left_x=250)
2. OLS inconsistent
![](https://cdn.mathpix.com/cropped/02e4f915-8a26-4777-8299-892404f92454-10.jpg?height=99&width=163&top_left_y=582&top_left_x=558)
3. IV consistent
![](https://cdn.mathpix.com/cropped/02e4f915-8a26-4777-8299-892404f92454-10.jpg?height=104&width=299&top_left_y=578&top_left_x=895)

- Note: This is only possible if one can find a valid instrument.


### 17.4.1 IV Estimator and Interpretation

- The instrumental variables (IV) estimator of beta-two is

b-sub-IV equals the sum over i of the quantity z-sub-i minus z-bar times the quantity y-sub-i minus y-bar, all divided by the sum over i of the quantity z-sub-i minus z-bar times the quantity x-sub-i minus x-bar

- Intuitively it estimates change in y over change in x as the ratio of change in y over change in z, divided by change in x over change in z
- if one-unit change in z is associated with a one unit increase in x of 2 and increase of y of 3, then b-sub-IV equals 3 divided by 2, which equals 1.5.
- and this can be given a causal interpretation of change in y over change in x equals 1.5.
- Can extend to multiple regression
- exogenous regressors (uncorrelated with u) are instruments for themselves
- if more instruments (z) than endogenous regressors (x) then use two-stage least squares.
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
- goal is to get causal estimate of effect of x on z using observational data.
- Stereotypical problem is returns to training where self-select into training
- y-sub-i equals beta-one plus gamma times d-sub-i plus u-sub-i, where d-sub-i is a binary indicator for training
- people choose to get training and we expect that those with higher (unobserved) expected benefits to training will select training
- then the expected value of u-sub-i given d-sub-i equals 1 is greater than the expected value of u-sub-i given d-sub-i equals 0, so the expected value of u-sub-i given d-sub-i not equal to 0.
- There are many different methods to nonetheless obtain a causal estimate
- each method has its own distinct assumptions and data requirements.


### 17.5.1 Potential Outcomes Framework

- Potential outcomes model or Rubin causal model
- standard framework that is used.
- Consider a binary treatment D
- D-sub-i equals 1 for individual i if treated
- D-sub-i equals 0 if individual i is not treated (a control).
- There are two potential outcomes for Y-sub-i
- Y-sub-1-i if D-sub-i equals 1, and Y-sub-0-i if D-sub-i equals 0.
- Interest lies in estimating the treatment effect gamma-sub-i defined as Y-sub-1-i minus Y-sub-0-i
- we cannot estimate gamma-sub-i as we only observe one of Y-sub-1-i and Y-sub-0-i
- so restrict attention to more aggregated measures.
- The average treatment effect (ATE) in the population is

ATE equals the expected value of gamma-sub-i, which equals the expected value of Y-sub-1-i minus Y-sub-0-i.

- The average treatment effect on the treated (ATET) is

ATET equals the expected value of gamma-sub-i given D-sub-i equals 1, which equals the expected value of the quantity Y-sub-1-i minus Y-sub-0-i, given D-sub-i equals 1.

> **Key Concept**: The potential outcomes framework formalizes causal inference by defining treatment effects as the difference between potential outcomes under treatment and control. Since we only observe one outcome per individual, we focus on average treatment effects (ATE) or average treatment effects on the treated (ATET).

### 17.5.2 Randomized Control Trials and Difference-in-Differences

- A random controlled trial (RCT) is an experiment where randomly assign people to treatment and control.
- then estimate ATE by the difference in means y-bar-sub-1-i minus y-bar-sub-0-i
- done more often in economics but still not a lot.
- A difference-in-difference estimate uses the following
- simplest case two periods of time
- no individuals are treated in the first period
- some are treated in the second period and some are not
- ATET-hat equals average change in y over time for those treated in second period, minus average change in y over time for those not treated in second period.
- example of a natural experiment.

> **Key Concept**: Randomized control trials (RCTs) provide causal estimates by randomly assigning treatment, ensuring treatment is uncorrelated with potential outcomes. Difference-in-differences (DiD) estimates the treatment effect as the change over time for treated individuals minus the change for untreated individuals, controlling for time trends.


### 17.5.3 Regression Adjustment and Control Functions

- Control function approach adds controls
- ATE-hat equals gamma-hat from OLS of y-sub-i equals beta-one plus gamma times d-sub-i plus beta-two times x-sub-2-i plus dot-dot-dot plus beta-k times x-sub-k-i plus u-sub-i
- need to ensure d-sub-i and u-sub-i uncorrelated once the controls are added.
- Richer regression adjustment estimator runs separate regressions
- regress y-sub-i on intercept and x-sub-2-i through x-sub-k-i for d-sub-i equals 1 only, compute one over n times the sum from i equals 1 to n of predicted y-sub-1-i, where predicted y-sub-1-i is resulting prediction for d-sub-i equals 0 and d-sub-i equals 1.
- regress y-sub-i on intercept and x-sub-2-i through x-sub-k-i for d-sub-i equals 0 only, compute one over n times the sum from i equals 1 to n of predicted y-sub-0-i, where predicted y-sub-1-i is resulting prediction for d-sub-i equals 0 and d-sub-i equals 1.
- ATE-hat equals one over N times the sum from i equals 1 to N of predicted y-sub-1-i, minus one over N times the sum from i equals 1 to N of predicted y-sub-0-i.
- Fixed effects estimators
- y-sub-i-t equals beta-one plus gamma times d-sub-i-t plus beta-two times x-sub-2-i-t plus dot-dot-dot plus beta-k times x-sub-k-i-t plus alpha-sub-i plus epsilon-sub-i-t
- need to assume d-sub-i-t and epsilon-sub-i-t uncorrelated once the controls and alpha-sub-i are added.

> **Key Concept**: Regression adjustment adds control variables to make treatment assignment independent of potential outcomes conditional on the controls. Fixed effects models extend this by controlling for unobserved individual-specific effects that are constant over time.


### 17.5.4 Regression Discontinuity Design

- Regression discontinuity design (RDD)

- a threshold variable determines treatment status
- e.g. admission into treatment is based on a score denoted s, with scores above 100, say, leading to treatment when d equals 1.
- A simple RDD estimate compares the average value of y for individuals on either side of the threshold.
- Complication: usually the outcome variable y itself varies with s
- suppose that y equals beta-one plus beta-two times s plus u without treatment
- then a simple RDD estimate of ATET is gamma-hat from OLS of

y-sub-i equals beta-one plus gamma times d-sub-i plus beta-two times s-sub-i plus u-sub-i.

- In practice more flexible models are used
- e.g. different linear or quadratic trends on either side of the threshold
- estimates are focused on observations close to the threshold
- or nonparametric methods are used either side of the threshold.

> **Key Concept**: Regression discontinuity design (RDD) exploits threshold-based treatment assignment. By comparing outcomes just above and below the threshold (where treatment changes discontinuously), RDD provides a local causal estimate for individuals near the threshold.


### 17.5.5 Local Average Treatment Effects (LATE)

- Instrumental variables (IV) estimator from chapter 17.4
- IV estimator in model y-sub-i equals beta-one plus gamma times d-sub-i, where z-sub-i is instrument for x-sub-i.
- This restricts constant treatment effect gamma for all individuals.
- Instead allow different (heterogeneous) treatment effects gamma-sub-i.
- Specialize to a binary treatment D and suppose for simplicity that higher value of Z makes selection into treatment when D equals 1 more likely.
- Distinguish between four types of people:
- (1) Always-takers chose treatment when D equals 1 regardless of the value of Z
- (2) Never-takers never chose treatment when D equals 0 regardless of the value of Z;
- (3) Compliers are induced into treatment so D equals 1 when Z equals 1 and D equals 0 when Z equals 0
- (4) Defiers are induced away from treatment so D equals 0 when Z equals 1 and D equals 1 when Z equals 0.
- Then under the crucial and nontestable assumption that there are no defiers, also called the monotonicity assumption, the IV estimator


### 17.5.6 Inverse Probability Weighting and Matching

- Inverse probability weighting uses weighted averages of the outcome
- binary treatment d-sub-i equals 1 or d-sub-i equals 0.
- we observe d-sub-i times y-sub-i if the individual is treated and the quantity 1 minus d-sub-i times y-sub-i if untreated
- ATE is the weighted average one over N times the sum from i equals 1 to n of w-sub-i times the quantity d-sub-i times y-sub-i minus the quantity 1 minus d-sub-i times y-sub-i
- where the weights w-sub-i equals 1 over p-hat-sub-i if treated, and w-sub-i equals 1 over the quantity 1 minus p-hat-sub-i if untreated
- and p-hat-sub-i equals the predicted probability that d-sub-i equals 1 given the regressors x-sub-2-i through x-sub-k-i, is the propensity score, the predicted probability of treatment.
- key: assume that the weights control for selection into treatment.
- Matching compares treated person to a similar (on x's) untreated
- nearest neighbor matching compare outcome for each treated observation to the average outcome of the k observations whose values of x-two through x-k are closest to those for the treated observation.
- propensity score matching instead compares outcomes with similar probability of treatment.

> **Key Concept**: Inverse probability weighting (IPW) and matching methods estimate treatment effects by comparing treated and untreated individuals with similar characteristics. The propensity score—the probability of treatment given covariates—is key to both approaches.


## 17.6 Nonlinear Regression Models

**In this section:**
- 17.6.1 Probit model
- 17.6.2 Exponential conditional mean model

- Binary outcome y-sub-i equals 0 or 1
- model the probability that y-sub-i equals 1 given regressors using a logit model or probit model
- maximum likelihood estimation by computer is straightforward, interpretation of estimates is more difficult.
- The logit model specifies that

**Example 17.3**: Logit Model Specification

The probability that y equals 1 given x-two through x-k equals the exponential of beta-one plus beta-two times x-two plus dot-dot-dot plus beta-k times x-k, all divided by 1 plus the exponential of beta-one plus beta-two times x-two plus dot-dot-dot plus beta-k times x-k. The probability that y equals 0 given x-two through x-k equals 1 minus the probability that y equals 1 given x-two through x-k.

- For the j-th regressor ME-sub-j equals change in p-hat over change in x-sub-j, which equals p-hat times the quantity 1 minus p-hat times b-sub-j
- where p-hat is the predicted probability
- the absolute value of ME-sub-j is less than or equal to 0.25 times the absolute value of b-sub-j, and sign of b-sub-j gives sign of ME.

> **Key Concept**: For binary outcomes, logit and probit models estimate the probability of the outcome being 1 as a function of regressors. Unlike linear probability models, these ensure predicted probabilities lie between 0 and 1. Marginal effects (not coefficients) give the change in probability for a unit change in a regressor.


### 17.6.1 Probit Model

- The probit model specifies that

**Example 17.4**: Probit Model Specification

The probability that y equals 1 given x-two through x-k equals Phi of the quantity beta-one plus beta-two times x-two plus dot-dot-dot plus beta-k times x-k. The probability that y equals 0 given x-two through x-k equals 1 minus the probability that y equals 1 given x-two through x-k.

where Phi is the cumulative distribution function of the standard normal distribution.

- For the probit model ME-sub-j equals phi of p-hat times b-sub-j
- where phi is the standard normal density function
- the absolute value of ME-sub-j is less than or equal to 0.4 times the absolute value of b-sub-j, and sign of b-sub-j gives sign of ME.


### 17.6.2 Exponential Conditional Mean Model

- Suppose the conditional mean is exponential, so that

**Example 17.5**: Exponential Conditional Mean Model

The expected value of y given x-two through x-k equals the exponential of the quantity beta-one plus beta-two times x-two plus dot-dot-dot plus beta-k times x-k.

- This model is applicable to nonnegative data as the expected value of y given x-two through x-k is greater than 0.
- Estimation is by a method called quasi-maximum likelihood
- rather than by least squares regression
- b-one, b-two through b-k maximize the sum from i equals 1 to n of the quantity y-sub-i times ln of mu-sub-i minus mu-sub-i, where mu-sub-i equals the exponential of the quantity b-one plus b-two times x-sub-2-i plus dot-dot-dot plus b-k times x-sub-k-i.
- Now ME-sub-j equals change in predicted y over change in x-sub-j, which equals predicted y times b-sub-j
- where predicted y is the predicted value of y
- and AME equals y-bar times b-sub-j.
- Coefficients b-sub-j can be directly interpreted as semi-elasticities.

> **Key Concept**: Exponential regression models are appropriate for nonnegative outcomes (like counts or expenditures). The exponential form ensures predictions are positive. Coefficients can be interpreted as semi-elasticities: a one-unit change in x changes y by approximately 100 times beta percent.


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
- Application regresses 10-year rate on 1-year rate.

---

## Key Takeaways

**Panel Data Methods (Sections 17.1-17.3):**
- Use cluster-robust standard errors when observations are grouped (students in schools, workers in firms, individuals in villages)
- Cluster-robust SE account for within-cluster correlation and can be substantially larger than default or heteroskedastic-robust SE
- Panel data methods include pooled OLS, random effects, and fixed effects estimators
- Panel data variation decomposes into within variation (over time for each individual) and between variation (across individuals)
- Fixed effects control for unobserved time-invariant individual characteristics (alpha-sub-i)
- Fixed effects use only within variation; random effects and OLS use both within and between variation
- NBA example: one more win increases team revenue by 0.27 percent (fixed effects estimate with cluster-robust SE)
- Always use cluster-robust (not default) standard errors for clustered or panel data
- Random effects assume regressors are uncorrelated with individual effects; fixed effects allow correlation

**Instrumental Variables (Section 17.4):**
- IV addresses endogeneity when a regressor x is correlated with the error term (the expected value of u given x not equal to 0)
- A valid instrument z must satisfy two conditions: (1) relevance (correlated with x) and (2) exclusion restriction (uncorrelated with u)
- The IV estimator provides consistent causal estimates under these assumptions
- IV formula: b-sub-IV equals the sum of the quantity z-sub-i minus z-bar times the quantity y-sub-i minus y-bar, divided by the sum of the quantity z-sub-i minus z-bar times the quantity x-sub-i minus x-bar
- Intuition: IV estimates change in y over change in x as the ratio of change in y over change in z, divided by change in x over change in z
- Two-stage least squares (2SLS) extends IV to multiple endogenous regressors
- Example: distance to college as an instrument for schooling in wage equations
- With multiple instruments and endogenous regressors, use 2SLS estimation

**Causal Inference Framework (Section 17.5):**
- The potential outcomes framework defines treatment effects as Y-sub-1-i minus Y-sub-0-i (potential outcomes under treatment vs. control)
- Average treatment effect (ATE) equals the expected value of Y-sub-1-i minus Y-sub-0-i for the population
- Average treatment effect on the treated (ATET) equals the expected value of Y-sub-1-i minus Y-sub-0-i given D-sub-i equals 1
- Randomized control trials (RCTs) provide gold-standard causal estimates by randomly assigning treatment
- RCTs ensure treatment is uncorrelated with potential outcomes (the expected value of u given D equals 0)
- Difference-in-differences (DiD) estimates ATET as (change for treated) minus (change for untreated)
- DiD controls for time trends affecting both treatment and control groups
- Regression adjustment adds control variables to make treatment assignment independent of outcomes conditional on controls
- Fixed effects models control for time-invariant unobserved heterogeneity (alpha-sub-i) in addition to observed controls

**Regression Discontinuity and Advanced Methods (Section 17.5 continued):**
- Regression discontinuity design (RDD) exploits threshold-based treatment assignment
- RDD compares outcomes just above and below the threshold where treatment changes discontinuously
- RDD provides local causal estimate for individuals near the threshold
- In practice, RDD uses flexible models (different trends on each side) or nonparametric methods
- Local average treatment effect (LATE) from IV estimates causal effect for compliers
- Compliers are individuals induced into treatment by the instrument (D equals 1 when Z equals 1, D equals 0 when Z equals 0)
- LATE requires monotonicity assumption (no defiers)
- Always-takers and never-takers are unaffected by the instrument

**Matching and Propensity Score Methods (Section 17.5 continued):**
- Inverse probability weighting (IPW) uses weighted averages to estimate ATE
- Weights are w-sub-i equals 1 over p-hat-sub-i if treated, w-sub-i equals 1 over the quantity 1 minus p-hat-sub-i if untreated
- Propensity score p-hat-sub-i equals the probability that D-sub-i equals 1 given X-sub-i is the predicted probability of treatment given covariates
- IPW assumes selection into treatment is controlled by the propensity score weights
- Nearest neighbor matching compares each treated observation to k similar untreated observations
- Propensity score matching compares observations with similar probability of treatment
- All matching methods assume selection on observables (no unobserved confounding)

**Nonlinear Regression Models (Section 17.6):**
- Logit and probit models are appropriate for binary (0/1) outcomes
- Logit: the probability that y equals 1 given x equals exp of beta prime x, divided by 1 plus exp of beta prime x
- Probit: the probability that y equals 1 given x equals Phi of beta prime x, where Phi is the standard normal CDF
- These models ensure predicted probabilities lie between 0 and 1 (unlike linear probability model)
- Marginal effects (not raw coefficients) give the change in probability for a unit change in x
- For logit: ME-sub-j is less than or equal to 0.25 times the absolute value of b-sub-j; for probit: ME-sub-j is less than or equal to 0.4 times the absolute value of b-sub-j
- Exponential regression models are appropriate for nonnegative data: the expected value of y given x equals exp of beta prime x
- Exponential form ensures predictions are positive (useful for counts, expenditures)
- Coefficients in exponential models are semi-elasticities: one-unit change in x changes y by approximately 100 times beta percent
- All nonlinear models are estimated by maximum likelihood, not OLS

**Time Series Methods (Sections 17.7-17.8):**
- Time series data requires special methods due to autocorrelation (correlation over time in errors)
- HAC standard errors account for both heteroskedasticity and autocorrelation
- Stationarity is crucial: mean, variance, and covariances are constant over time
- Nonstationary series can lead to spurious regression (high R-squared but no true relationship)
- Autoregressive (AR) models include lagged dependent variables as regressors: y-sub-t equals alpha plus rho times y-sub-t-minus-1 plus epsilon-sub-t
- Distributed lag models include current and lagged values of regressors
- Autoregressive distributed lag (ARDL) models combine both approaches
- Unit root tests (Dickey-Fuller, ADF) determine whether a series is stationary or nonstationary
- If nonstationary, use first differences or cointegration methods
- Forecasting methods include AR, ARMA (autoregressive moving average), and VAR (vector autoregression)
- Time series econometrics is a specialized field requiring careful treatment of dynamics and nonstationarity

---
