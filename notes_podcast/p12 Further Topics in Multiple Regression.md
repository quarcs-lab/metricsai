# Chapter 12: Further Topics in Multiple Regression

## Learning Objectives

By the end of this chapter, you will be able to:
- Understand when to use heteroskedastic-robust, cluster-robust, and HAC-robust standard errors
- Distinguish between prediction of average outcomes and individual outcomes
- Compute prediction intervals for conditional means and forecasts
- Understand the impact of nonrepresentative samples on regression estimates
- Recognize the difference between unbiased and best (most efficient) estimators
- Understand Type I and Type II errors in hypothesis testing
- Appreciate the role of data science and machine learning in modern econometrics
- Understand the Bayesian approach to statistical inference as an alternative to classical methods

---

In [Chapter 11](s11%20Statistical%20Inference%20for%20Multiple%20Regression.md), you learned to conduct hypothesis tests and build confidence intervals—but those methods assumed homoskedastic, independent errors. What if your data violate these assumptions? What if you're working with clustered data (students within schools) or time series (stock prices over time)? And once you've estimated a model, how do you use it to predict house prices or forecast next month's sales? This chapter tackles the practical challenges you'll face in real-world regression analysis: choosing the right standard errors, distinguishing conditional mean prediction from individual forecasts, handling nonrepresentative samples, and understanding modern tools like machine learning and Bayesian methods.

## 12.1 Inference with Robust Standard Errors

**In this section:**
- 12.1.1 Overview of robust standard errors
- 12.1.2 Heteroskedastic-robust standard errors
- 12.1.3 Example: House price with heteroskedastic-robust SE
- 12.1.4 Interpreting heteroskedastic-robust results
- 12.1.5 Cluster-robust standard errors: theory
- 12.1.6 Cluster-robust standard errors: implementation
- 12.1.7 Cluster-robust standard errors in practice
- 12.1.8 HAC-robust standard errors for time series

- Continue with assumptions 1-2 so OLS estimates are still unbiased.
- Relax error assumptions 3-4 as then assumptions are more realistic
- this leads to different standard errors for b-sub-j denoted se-sub-rob of b-sub-j.
- Three common complications give different se-sub-rob of b-sub-j.

**Example 12.1**: Types of Robust Standard Errors for Different Data Structures

| Complication | Robust Standard Error Type | Data Type |
| :--- | :--- | :--- |
| 1. Heteroskedasticity: Error variance varies over i | Heteroskedasticity robust | Cross Section (if errors independent) |
| 2. Clustered: Errors in same cluster are correlated | Cluster robust | Some Cross section Most Short Panel |
| 3. Autocorrelation: Errors correlated over time | Heteroskedasticity and autocorrelation (HAC) robust | Most Time Series Some Long Panel |

### 12.1.1 Overview of Robust Standard Errors

- For implementation, use the appropriate command in a statistical package
- in Python use statsmodels with `cov_type='HC1'` or similar options
- in R use the sandwich package
- chapter 12.1.9 provides details.
- Once the appropriate standard errors se-sub-rob of b-sub-j are obtained the rest follows as usual
- for a single parameter test use t equals the quantity b-sub-j minus beta-sub-j, divided by se-sub-rob of b-sub-j, which is distributed approximately as T-sub-v
- for a confidence interval on beta-sub-j use b-sub-j plus or minus t-sub-v-semicolon-alpha-over-2 times se-sub-rob of b-sub-j.
- The degrees of freedom are usually v equals n minus k
- except for cluster-robust use v equals G minus 1 where G is the number of clusters.
- The key is to know which type of robust standard error to use.

> **Key Concept**: When regression assumptions 3-4 fail, default standard errors are wrong. Use heteroskedastic-robust SE for cross-section data, cluster-robust SE when observations are grouped, and HAC-robust SE for time series data. The OLS estimates remain unbiased, but inference requires correct standard errors.

**Why This Matters**: Using the wrong standard errors can lead to dramatically incorrect conclusions. Suppose you're analyzing student test scores clustered by classroom. Default standard errors assume independence, but students in the same classroom share a teacher, curriculum, and environment—their errors are correlated! Cluster-robust standard errors can be three to five times larger than default SE. A coefficient that appears "highly significant" with default SE (t equals 4.0) might become insignificant with cluster-robust SE (t equals 1.5). Always match your standard errors to your data structure, or you risk publishing false discoveries.

### 12.1.2 Heteroskedastic-Robust Standard Errors

- In many cross-section data applications
- it may be reasonable to assume error independence across observations
- but errors are heteroskedastic (the error variance varies across observations).
- OLS is still unbiased under assumptions 1-2
- but default standard errors are invalid.
- Make the following change to assumptions 1-4
- change 3 to 3-prime that the variance of u-sub-i equals sigma-sub-i squared (which depends on the x's) and n goes to infinity
- The formula for se of b-sub-j changes to, say, se-sub-het of b-sub-j.
- Computer output is qualitatively similar
- b-one through b-k are unchanged
- now get se-sub-het of b-one through se-sub-het of b-k
- leading to different t-statistics and confidence intervals.


### 12.1.3 Example: House Price with Heteroskedastic-Robust SE

**Example 12.2**: House Price Regression with Heteroskedastic-Robust Standard Errors

| Variable | Coefficient | Robust se | t statistic | p value | 95\% conf. int. |  |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Size | 68.37 | 15.36 | 4.44 | 0.000 | 36.52 | 100.22 |
| Lot Size | 23020 | 5329 | 0.43 | 0.670 | -8748 | 13355 |
| Bedrooms | 2685 | 8286 | 0.32 | 0.749 | -14498 | 19868 |
| Bathrooms | 6833 | 19284 | 0.35 | 0.726 | -33159 | 46825 |
| Year Built | -833 | 763 | -1.09 | 0.287 | -2415 | 749 |
| Age | -2089 | 3738 | -0.56 | 0.582 | -9841 | 5664 |
| Intercept | 137791 | 65545 | 2.10 | 0.047 | 1856 | 273723 |
| n | 29 |  |  |  |  |  |
| F(6,22) | 6.41 |  |  |  |  |  |
| p -value for F | 0.0005 |  |  |  |  |  |
| R-squared | 0.651 |  |  |  |  |  |
| St. error | 24936 |  |  |  |  |  |

### 12.1.4 Interpreting Heteroskedastic-Robust Results

- Same intercept and slope coefficient estimates (as still OLS).
- For individual standard errors the biggest change is 30 percent
- again only Size is statistically significant at 5 percent.
- Again regressors are jointly statistically significant at 5 percent
- F equals 6.41 (compared to 6.83 ).
- For test of joint statistical significance of lotsize through monthsold
- F equals 0.46 distributed as F with 5 comma 22 degrees of freedom, compared to F equals 0.42 with default se's
- reject H-sub-0 at level 0.05 as p equals 0.8038 which is greater than 0.05.
- The heteroskedastic-robust standard errors can be larger or smaller than default standard errors
- the two are generally within 30 percent of each other.

> **Key Concept**: Heteroskedastic-robust standard errors typically differ from default SE by less than 30%, but can be larger or smaller. With robust SE, coefficient estimates are unchanged but t-statistics and confidence intervals change. Always use robust SE when heteroskedasticity is suspected.


### 12.1.5 Cluster-Robust Standard Errors: Theory

- In many cross-section data and panel data applications
- errors may be independent across clusters but correlated within cluster
- and additionally errors are heteroskedastic.
- Cross-section data example
- independent errors for individuals in different villages but correlated for individuals in the same village.
- Panel data example
- errors may be independent across individuals but correlated over time for a given individual.
- Then must use cluster-robust standard errors
- these can be several times default or het-robust standard errors!
- with correlation within cluster, adding an observation to a cluster gives less than a completely new independent piece of information
- cluster-robust correct s for this reduced estimator precision!


### 12.1.6 Cluster-Robust Standard Errors: Implementation

- OLS is still unbiased but default standard errors are too small
- Make the following changes to assumptions 1-4
- change 3 to 3-prime: the variance of u-sub-i given the x-sub-i's equals sigma-sub-i squared (so heteroskedastic)
- change 4 to 4-prime: correlated errors for observations in same cluster
  - And need G goes to infinity where G is the number of clusters
- The formula for se of b-sub-j changes to, say, se-sub-clu of b-sub-j
- Inference uses T with G minus 1 degrees of freedom
  - Note the much smaller degrees of freedom
- Implementation requires specifying a variable for the clusters


### 12.1.7 Cluster-Robust Standard Errors in Practice

- Cluster-robust standard errors can be several times the default or heteroskedastic-robust standard errors.
- The difference with default or heteroskedastic-robust se's gets greater
- the more observations there are per cluster
- the more highly correlated the regressors are within cluster
- the more highly correlated the errors are within cluster.
- It is essential to use cluster-robust standard errors if needed.
- It can sometimes be difficult to know how to form the clusters.
- data examples are given in [Chapter 13](s13%20Case%20Studies%20for%20Multiple%20Regression.md) sections 13.4.4, 13.6.4 and [Chapter 17](s17%20Panel%20Data%2C%20Time%20Series%20Data%2C%20Causation.md) section 17.3.1.

> **Key Concept**: Cluster-robust standard errors can be several times larger than default or heteroskedastic-robust SE. With N observations in G clusters, use G-1 (not N-k) degrees of freedom. The difference increases with more observations per cluster and higher within-cluster correlation.


### 12.1.8 HAC-Robust Standard Errors for Time Series

- Time series models often have autocorrelated errors
- an autocorrelated error is one that is correlated with errors in previous periods (e.g. u-sub-t equals 0.8 times u-sub-t-minus-1 ).
- If errors are autocorrelated then default standard errors are invalid
- instead use heteroskedastic- and autocorrelation-robust (HAC) standard errors.
- Make the following changes to assumptions 1-4
- change 2 to 2-prime: error has mean zero conditional on current and past values of the regressors.
- change 3 to 3-prime: the variance of u-sub-t given the x-sub-t's and past x-sub-t's equals sigma-sub-t squared
- change 4 to 4-prime: errors are correlated up to m periods apart and T goes to infinity
- The formula for se of b-sub-j changes to, say, se-sub-HAC of b-sub-j
- The lag length m needs to be specified or be data determined

A rule of thumb is m equals 0.75 times T to the power of one-third, where T equals the number of observations.

- Data examples are given in [Chapter 13](s13%20Case%20Studies%20for%20Multiple%20Regression.md) sections 13.2, 13.3 and [Chapter 17](s17%20Panel%20Data%2C%20Time%20Series%20Data%2C%20Causation.md) section 17.8.
- Heteroskedastic-robust standard errors were first introduced in [Chapter 7](s07%20Statistical%20Inference%20for%20Bivariate%20Regression.md) for bivariate regression.

> **Key Concept**: HAC (heteroskedasticity and autocorrelation consistent) standard errors account for both heteroskedasticity and autocorrelation in time series data. The lag length m must be specified; a rule of thumb is m = 0.75 × T^(1/3).

Now that we know how to conduct valid inference with robust standard errors, let's turn to a different practical question: using regression models to make predictions.

## 12.2 Prediction

**In this section:**
- 12.2.1 Average outcome versus individual outcome
- 12.2.2 Visual example of prediction intervals
- 12.2.3 Predicting the conditional mean
- 12.2.4 Forecasting individual outcomes
- 12.2.5 Why forecasts are imprecise
- 12.2.6 Policy implications of imprecise forecasts
- 12.2.7 Formulas for conditional mean prediction
- 12.2.8 Formulas for individual outcome forecasts
- 12.2.9 Example: Multiple regression prediction (default SE)
- 12.2.10 Example: Multiple regression prediction (robust SE)

- Predicting a value is straightforward.
- Predict for a given value of regressors, say x-two equals x-two-star through x-k equals x-k-star using

Predicted y given x-two-star through x-k-star equals b-one plus b-two times x-two-star plus dot-dot-dot plus b-k times x-k-star.

- Example: regress Price on just Size
- Predict a 2000 square foot 4-bedroom house will sell for \$262,559
- since, using estimates reported in Section 10.4,

Predicted y equals 115,017 plus 73.771 times 2000, which equals 262,559.

- But estimating the standard error of the prediction is subtle
- it depends on whether we are predicting an average outcome or an individual outcome.


### 12.2.1 Average Outcome Versus Individual Outcome

- Key distinction is between predict an average outcome and predict an individual outcome.
- Average outcome or conditional mean

The expected value of y given x-two-star through x-k-star equals beta-one plus beta-two times x-star plus dot-dot-dot plus beta-k times x-k-star

- Individual outcome or the actual value

y given x-two-star through x-k-star equals beta-one plus beta-two times x-star plus dot-dot-dot plus beta-k times x-k-star, plus u-star.

- For both we use the same prediction predicted y equals b-one plus b-two times x-two-star plus dot-dot-dot plus b-k times x-k-star.
- But the precision of the prediction varies with use
- For individual outcome we also need to predict u-star leading to noisier prediction
  - With variance necessarily at least the variance of u-star

- The following slide makes clear this distinction.

> **Key Concept**: Predicting an average outcome (conditional mean E[y|x*]) is more precise than predicting an individual outcome (y|x*). The forecast variance equals the conditional mean variance plus Var[u*], so Var(ŷ_f) ≥ Var(u*) always.


### 12.2.2 Visual Example of Prediction Intervals

- Regress house Price on Size
- predict house price at a range of house sizes
- first panel: 95 percent confidence interval for the conditional mean price.
- second panel: 95 percent confidence interval for actual price is much wider.

**Example 12.3**: Visual Comparison of Conditional Mean and Forecast Intervals

Prediction of Conditional mean
![](https://cdn.mathpix.com/cropped/33ec9fd0-dc14-44a6-a045-853bc82cbb48-15.jpg?height=400&width=538&top_left_y=436&top_left_x=84)

Prediction of Actual value
![](https://cdn.mathpix.com/cropped/33ec9fd0-dc14-44a6-a045-853bc82cbb48-15.jpg?height=400&width=538&top_left_y=436&top_left_x=639)

### 12.2.3 Predicting the Conditional Mean

- The conditional mean of y is

The expected value of y given x-two-star through x-k-star equals beta-one plus beta-two times x-star plus dot-dot-dot plus beta-k times x-k-star.

- Use predicted y-sub-cm equals b-one plus b-two times x-two-star plus dot-dot-dot plus b-k times x-k-star.
- The variance of predicted y-sub-cm depends on the precision of the estimates b-one through b-k.
- Define se of predicted y-sub-cm to be the standard error of predicted y-sub-cm.
- A 100 times one minus alpha percent confidence interval for the conditional mean is

The expected value of y given x-two-star through x-k-star is in the interval predicted y-sub-cm plus or minus t-sub-n-minus-k-comma-alpha-over-2 times se of predicted y-sub-cm.

- The variance of predicted y-sub-cm goes to zero and se of predicted y-sub-cm goes to zero as the estimates b-one through b-k become more precise.


### 12.2.4 Forecasting Individual Outcomes

- The actual value or forecast value of y for x equals x-star is

y given x-star equals beta-one plus beta-two times x-star plus dot-dot-dot plus beta-k times x-k-star, plus u-star.

- Use predicted y-sub-f equals b-one plus b-two times x-two-star plus dot-dot-dot plus b-k times x-k-star, as best estimate of u-star is zero.
- Then the variance of predicted y-sub-f depends additionally on the variance of u-star
- The variance of predicted y-sub-f equals the variance of predicted y-sub-cm plus the variance of u-star
- Define se of predicted y-sub-f to be the standard error of predicted y-sub-f
- then se of predicted y-sub-f equals the square root of the quantity se-squared of predicted y-sub-cm plus s-sub-u-star squared, where s-sub-u-star squared is estimate of the variance of u-star.
- A 100 times one minus alpha percent confidence interval for the forecast is

y given x-two-star through x-k-star is in the interval predicted y-sub-f plus or minus t-sub-n-minus-k-comma-alpha-over-2 times se of predicted y-sub-f

- The variance of predicted y-sub-f is greater than the variance of u-star always, even if b-one through b-k are very precise.

> **Key Concept**: Even with precise coefficient estimates, individual forecasts are imprecise because we cannot predict the error u*. The forecast standard error is at least as large as the standard error of regression (s_e), so 95% forecast intervals are at least ±1.96×s_e wide.

**Why This Matters**: Understanding the distinction between conditional mean prediction and individual forecasts prevents costly mistakes in business and policy. A real estate company might predict the average price of 2,000-square-foot homes very precisely (±$10,000) but struggle to predict any single home's price (±$50,000). This isn't a failure of the model—it's the irreducible uncertainty from unobserved factors (view, condition, negotiation). Policy-makers can confidently predict that raising minimum wage by one dollar increases average earnings, even though we can't predict any individual worker's future income. Confusing these two types of prediction leads to unrealistic expectations and poor decisions.

### 12.2.5 Why Forecasts Are Imprecise

- Recall that in forecasting
- we use predicted y-sub-f equals b-one plus b-two times x-two-star plus dot-dot-dot plus b-k times x-k-star
- to forecast y given x-star equals beta-one plus beta-two times x-star plus dot-dot-dot plus beta-k times x-k-star, plus u-star
- Even if b-one through b-k are very precisely estimated we still have u-star.
- So the variance of predicted y-sub-f is greater than or equal to the variance of u-star, and the standard deviation of predicted y-sub-f is greater than or equal to the standard deviation of u-star.
- The obvious estimate of the standard deviation of u-star is the standard error of the regression s-sub-e.
- So in large samples a 95 percent confidence interval for the forecast is at least as wide as

y given x-two-star through x-k-star is in the interval predicted y-sub-f plus or minus 1.96 times s-sub-e, where s-sub-e squared equals one over n minus k, times the sum from i equals 1 to n of the quantity y-sub-i minus predicted y-sub-i, all squared.

### 12.2.6 Policy Implications of Imprecise Forecasts

- Econometric models of individual behavior can have low R-squared
- so the variance of the model error and s-sub-e are large, so se of predicted y-sub-f is large.
- leading to very noisy forecasts of individual outcomes
- nonetheless the prediction of average outcomes may be quite precise, with low se of predicted y-sub-cm
- and policy-makers often base policy on average outcomes.
- For example, many studies find that on average education has an economically and statistically significant impact on earnings
- even though for an individual the confidence interval for forecast earnings given years of education is very wide.
- Knowing that on average greater education is predicted to lead to higher earnings encourages government to subsidize education
- even though we cannot predict with much certainty that a given person with a high level of education will have high earnings.

> **Key Concept**: Low R² and imprecise individual forecasts don't make regression uninformative. Policy-makers base decisions on average outcomes (which can be precisely estimated), not individual forecasts. Education increases average earnings even though we can't predict any individual's earnings precisely.


### 12.2.7 Formulas for Conditional Mean Prediction

- For bivariate regression under assumptions 1-4 the formula for se of predicted y-sub-cm is

se of predicted y-sub-cm equals s-sub-e times the square root of the quantity one over n plus the quantity x-star minus x-bar, all squared, divided by the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared.

- So the predicted conditional mean is more precise when
- 1. sample y-sub-i are closer to the regression line: then s-sub-e is smaller.
- 2. variation in regressors is greater: then the sum from i equals 1 to n of the quantity x-sub-i minus x-bar squared is larger.
- 3. x-star is closer to the sample mean: then the quantity x-star minus x-bar squared is smaller.
- 4. sample size is larger: then one over n and the quantity x-star minus x-bar squared divided by the sum from i equals 1 to n of the quantity x-sub-i minus x-bar squared are smaller.
- Furthermore: se of predicted y-sub-cm goes to zero as n goes to infinity due to 4.
- When robust standard errors are used specialized software is needed to get confidence intervals.


### 12.2.8 Formulas for Individual Outcome Forecasts

- Again consider regression of y on x under assumptions 1-4.
- Given homoskedastic errors the variance of u-star equals sigma-sub-u squared, so s-sub-u-star squared equals s-sub-e squared
- then se of predicted y-sub-f equals the square root of the quantity se-squared of predicted y-sub-cm plus s-sub-e squared
- For prediction of the actual value the formula for se of predicted y-sub-f is

se of predicted y-sub-f equals s-sub-e times the square root of the quantity 1 plus one over n plus the quantity x-star minus x-bar squared, divided by the sum from i equals 1 to n of the quantity x-sub-i minus x-bar squared.

- Now se of predicted y-sub-f is greater than or equal to s-sub-e, and does not go to zero as n goes to infinity.

> **Key Concept**: For conditional mean prediction, se(ŷ_cm) → 0 as n → ∞. For individual forecasts, se(ŷ_f) ≥ s_e does not go to zero, even in infinite samples. This fundamental difference drives the distinction between predicting averages (precise) and individuals (imprecise).


### 12.2.9 Example: Multiple Regression Prediction (Default SE)

- Predictions for a 2000 square foot house with medium lot size, four bedrooms, two bathrooms, forty-years old and sold in June.
- The predicted value is

Predicted y equals b-one plus 2000 times b-two plus 2 times b-three plus 4 times b-four plus 2 times b-five plus 40 times b-six plus 6 times b-seven, which equals 257,691.

- Predict conditional mean assuming assumptions 1-4 hold
- use statistical software with commands for prediction after OLS
- se of predicted y-sub-cm equals 6488 using default standard errors
- 95 percent confidence interval for the conditional mean house price is 257,691 plus or minus t-sub-22-comma-0.025 times 6488, which equals the interval from \$244,235 to \$271,146.
- Forecast the actual value assuming assumptions 1-4 hold
- s-sub-e equals 24,936, se of predicted y-sub-cm equals 6488, so se of predicted y-sub-f equals the square root of 6488 squared plus 24,936 squared, which equals 25,766.
- 95 percent confidence interval for the actual house price is 257,691 plus or minus t-sub-22-comma-0.025 times 25,766, which equals the interval from \$204,255 to \$311,126.


### 12.2.10 Example: Multiple Regression Prediction (Robust SE)

- Now suppose instead that model errors are heteroskedastic.
- Predict conditional mean
- use statistical software with commands for prediction after OLS
- se of predicted y-sub-cm equals 6631 using heteroskedastic-robust standard errors
- 95 percent confidence interval for the conditional mean house price is 257,691 plus or minus t-sub-22-comma-0.025 times 6631, which equals the interval from \$243,939 to \$271,442.
- Forecast the actual value
- we additionally need an estimate of the variance of u given x-star through x-k-star
- it is simplest to again use s-sub-e squared equals 24,936 squared
- s-sub-e equals 24,936, se of predicted y-sub-cm equals 6631, so se of predicted y-sub-f equals the square root of 6488 squared plus 24,936 squared, which equals 25,803.
- 95 percent confidence interval for the actual house price is 257,691 plus or minus t-sub-22-comma-0.025 times 25,803, which equals the interval from \$204,178 to \$311,203.

**Quick Check**: Before moving on, make sure you understand prediction: (1) Why is predicting the conditional mean E[y|x*] more precise than forecasting an individual outcome y|x*? (2) For the house price example, the conditional mean 95% CI is $244,235 to $271,146 (width $26,911) but the forecast 95% CI is $204,255 to $311,126 (width $106,871)—what accounts for this fourfold difference? (3) Does se(ŷ_cm) go to zero as sample size increases? Does se(ŷ_f)? (4) If a regression has R² = 0.20 and s_e = 50,000, what's the minimum width of a 95% forecast interval? Understanding prediction uncertainty is crucial for realistic expectations and decision-making.

## 12.3 Nonrepresentative Samples

- Many studies use survey data that may be nonrepresentative of the population.
- If there is nonrandom sampling on variables other than the dependent variable y then OLS can estimate population parameters if we include these variables as control variables in the regression
- e.g. include gender and race as controls.
- If there is nonrandom sampling on the dependent variable OLS does not lead to consistent estimates of population parameters
- e.g. if high earners are omitted from survey and we want to model earnings in the population.
- Many surveys include sample weights that adjust for nonrepresentativeness
- then population weighted least squares can be used.

We've focused primarily on unbiased estimation. But unbiasedness isn't the only desirable property—efficiency (having the smallest variance) also matters for precise inference.

## 12.4 Best Estimation

- An estimator b-sub-j is unbiased for beta-sub-j if the expected value of b-sub-j equals beta-sub-j.
- An estimator b-sub-j is consistent if as n goes to infinity any bias in b-sub-j goes to zero and the variance of b-sub-j goes to zero.
- A best estimator has smallest variance among unbiased estimators or among consistent estimators.
- When assumptions 3-4 do not hold OLS is no longer best.
- Feasible generalized least squares (FGLS) is instead the best estimator
- FGLS requires additionally specifying a model for the error variances and covariances and estimating this model
  - This model varies with the model for the errors
- In practice for linear regression models
- most studies just use OLS with appropriate robust standard errors
- this loses some precision but the loss is often not great.

> **Key Concept**: When assumptions 3-4 fail, OLS is no longer best (most efficient). Feasible generalized least squares (FGLS) is best but requires modeling error variances/covariances. In practice, most studies use OLS with robust SE, accepting a small loss in efficiency for greater simplicity.


## 12.5 Best Confidence Intervals

- Best confidence intervals are those with the shortest width at a given level of confidence.
- For standard estimators the 95 percent confidence interval is of form

beta-hat-sub-j plus or minus t-sub-n-minus-k-comma-alpha-over-2 times se of beta-hat-sub-j

- So the shortest interval is that with smallest se of beta-hat-sub-j and hence most efficient estimator.
- In practice even if assumptions 3-4 do not hold
- most studies base confidence intervals on OLS with appropriate robust standard errors
- this increases confidence interval width but the increase is often not great.

> **Key Concept**: Best confidence intervals are those with shortest width at a given confidence level. This requires the most efficient estimator (smallest SE). With robust SE, confidence intervals are wider than with default SE, but remain valid when assumptions fail.


## 12.6 Best Tests: Type I and II errors

**In this section:**
- 12.6.1 Test size and power

- Consider H-sub-0: no disease versus H-sub-a: disease is present.
- Two errors can be made in hypothesis testing.
- A type I error (or false positive)
- H-sub-0 is rejected when H-sub-0 is true
  - So find disease even though no disease is present
- To date we have only considered type 1 error (see Chapter 4.4)
- A type II error (or false negative)
- H-sub-0 is not rejected when H-sub-0 is false
- so find no disease when disease is present.

**Example 12.4**: Type I and Type II Errors in Hypothesis Testing

| Decision | Truth |  |
| :--- | :---: | :---: |
|  | H-sub-0 really true: No disease | H-sub-0 really false: Disease |
| Do not reject H-sub-0: | Correct decision | Type II error |
| Find no disease | Type I error | (false negative) |
| Reject H-sub-0: | (false positive) |  |
| Find disease |  |  |

### 12.6.1 Test Size and Power

- Test size is the probability of a type I error.
- Test size is set at alpha, the significance level of the test.
- Test power is one minus the probability of a type II error
- High power is preferred as then low probability of type II error
- Problem: there is a trade-off
- Probability of type I error decreases implies probability of type II error increases
- e.g. Can set probability of type I error equals zero if never reject H-sub-0.
- Solution: use most powerful test
- this has highest power for given test size
- this is a test based on most precise estimator.
- In practice while test size is set low (e.g. 5 percent)
- the probability of type II error can be high and test power may be low.

> **Key Concept**: Test size equals the probability of Type I error (false positive). Test power equals one minus the probability of Type II error (false negative). The most powerful test for given size uses the most precise estimator. Higher power means lower risk of failing to detect a true effect.

The methods we've covered—OLS, robust standard errors, hypothesis tests—are classical econometric tools. But modern data science offers new approaches that complement traditional regression. Let's explore how machine learning fits into econometric analysis.

## 12.7 Data Science and Big Data: An Overview

**In this section:**
- 12.7.1 Prediction using machine learning
- 12.7.2 Causal inference with machine learning

- Data science or data analytics is the science of discerning patterns in data.
- Machine learning is a branch of artificial intelligence
- algorithmically learn from data (the machine learns)
- rather than specify a model based on expert knowledge of the particular application
- methods include lasso, regression trees, random forests, neural networks, deep learning.
- Big data refers to datasets that are enormously large
- though big data methods may also be applied to smaller datasets.


### 12.7.1 Prediction Using Machine Learning

- Often the goal of big data is prediction
- machine learning methods can predict better than earlier methods such as OLS.
- In some cases the predictions at the individual level are very precise
- e.g. recognizing the numbers and letters on a digital image of a vehicle license plate.
- In other cases the predictions may at the individual level can be imprecise
- but money may still be made if predict well on average
- e.g. a better search engine than competitors
- e.g. a better model for predicting stock prices than competitors
- e.g. a better model for digital ad clicks than competitors.


### 12.7.2 Causal Inference with Machine Learning

- Economists want to estimate models that are only partially specified
- use the machine learner in part of the analysis
- but do valid inference controlling for the machine learning.
- For example, suppose we are interested in estimating the effect of changing x on y after controlling for everything else
- e.g. y equals beta-one plus beta-two times x plus many control variables plus u
- If we included all the control variables, the estimates get very noisy (overfitting).
- Instead use a machine learner to select a subset of the control variables.

> **Key Concept**: Machine learning methods (lasso, random forests, neural networks) can predict better than OLS but don't provide standard errors for inference. Economists combine machine learning for variable selection with OLS for inference, controlling for the machine learning step to get valid standard errors.

**Why This Matters**: Machine learning and econometrics solve different problems. If you want to predict whether a customer will click an ad, use machine learning—it optimizes prediction without needing causal interpretation. But if you want to know whether raising ad spending by one dollar causes more clicks (to decide your budget), you need econometrics with standard errors and hypothesis tests. Many modern applications combine both: use lasso to select which of 10,000 potential control variables to include, then use OLS with robust SE to estimate causal effects. The future of data analysis isn't choosing between machine learning and econometrics—it's using each for what it does best.

## 12.8 Bayesian Methods: An Overview

- An alternative to the "classical" inference approach of this book.
- Base inference on the parameter(s) of interest theta using the posterior distribution which combines the distribution of y given theta with a prior distribution for theta
- the prior can be informative or uninformative.
- One advantage is that a resulting 95 percent Bayesian credible region can be directly interpreted as a being an interval that theta lies in with probability 0.95.
- Rarely used until recently due to intractability.
- Recent Markov chain Monte Carlo methods (MCMC) make Bayesian methods now much easier to implement.
- In very large samples or with uninformative prior get similar results to using "classical" methods.

> **Key Concept**: Bayesian inference combines data with prior beliefs to form a posterior distribution for parameters. A 95% Bayesian credible interval can be directly interpreted as containing the parameter with probability 0.95. With large samples or uninformative priors, Bayesian and classical results converge.


## 12.9 A Brief History of Statistics and Regression

- 1733 Central limit theorem
- 1805 Least squares (without statistical inference)
- 1885 Regression
- 1888 Correlation
- 1894 The term "standard deviation"
- 1895 Histograms
- 1908 The t distribution
- 1924 The F distribution
- 1945 ENIAC (the first electronic general purpose digital computer)
- 1964 Kernel regression (a nonparametric regression method)
- 1980's Robust standard errors
- 1984 Apple Macintosh computer (an early personal computer).

---

## Key Takeaways

**Robust Standard Errors for Different Data Structures:**

- Default standard errors assume homoskedasticity, independence, and (for time series) no autocorrelation
- When these assumptions fail, OLS estimates remain unbiased but inference requires robust SE
- **Heteroskedastic-robust SE**: Use for cross-section data when error variance varies across observations
- Heteroskedastic-robust SE typically differ from default SE by less than 30% (can be larger or smaller)
- **Cluster-robust SE**: Use when observations are grouped (villages, firms, individuals over time)
- Cluster-robust SE can be several times larger than default or heteroskedastic-robust SE
- With N observations in G clusters, use G-1 (not N-k) degrees of freedom for cluster-robust inference
- The difference with default SE increases with more observations per cluster and higher within-cluster correlation
- **HAC-robust SE**: Use for time series data with autocorrelated errors
- HAC (heteroskedasticity and autocorrelation consistent) SE require specifying lag length m
- Rule of thumb for lag length: m = 0.75 × T^(1/3) where T is number of observations
- Always use cluster-robust SE for panel data (cluster on individual ID)

**Prediction: Average Outcomes vs. Individual Forecasts:**

- Predicting an average outcome (conditional mean E[y|x*]) is more precise than predicting an individual outcome (y|x*)
- For conditional mean: Var(ŷ_cm) depends only on estimation uncertainty from coefficient estimates
- For individual forecast: Var(ŷ_f) = Var(ŷ_cm) + Var(u*), so forecasts are always noisier
- Even with very precise coefficient estimates, se(ŷ_f) ≥ s_e does not go to zero
- In large samples, 95% forecast intervals are at least ±1.96×s_e wide
- Conditional mean prediction gets more precise as sample size increases: se(ŷ_cm) → 0 as n → ∞
- Individual forecast precision does not improve beyond reducing estimation uncertainty
- Prediction is most precise when x* is close to sample mean and sample variation in x is large
- Low R² and wide individual forecast intervals don't make regression uninformative
- Policy-makers base decisions on average predictions (which can be precise), not individual forecasts

**Nonrepresentative Samples and Best Estimation:**

- Nonrepresentative samples can bias OLS if sampling depends on the dependent variable y
- Include control variables as regressors if sampling depends on observed characteristics
- Use sample weights with weighted least squares to adjust for known nonrepresentativeness
- An estimator is "best" (most efficient) if it has smallest variance among unbiased or consistent estimators
- When assumptions 3-4 (homoskedasticity, no autocorrelation) fail, OLS is no longer best
- Feasible generalized least squares (FGLS) is best but requires modeling the error variance/covariance structure
- In practice, most studies use OLS with robust SE despite small efficiency loss for simplicity
- Best confidence intervals have shortest width at a given confidence level (requires most efficient estimator)
- With robust SE, confidence intervals are wider than with default SE, but remain valid when assumptions fail

**Hypothesis Testing: Type I and Type II Errors:**

- Type I error (false positive): Reject H₀ when H₀ is true
- Type II error (false negative): Fail to reject H₀ when H₀ is false
- Test size = Pr[Type I error], typically set at α = 0.05
- Test power = 1 - Pr[Type II error]; higher power is better
- Most powerful test for given size uses the most efficient estimator (smallest standard error)
- Trade-off exists: reducing Type I error probability increases Type II error probability
- In practice, test size is controlled (set at 5%), but Type II error probability can be high
- Low power means high risk of failing to detect a true effect when it exists

**Data Science, Machine Learning, and Big Data:**

- Data science focuses on discerning patterns in data using algorithmic methods
- Machine learning (lasso, regression trees, random forests, neural networks, deep learning) can predict better than OLS
- Machine learning emphasizes prediction accuracy, not causal inference or statistical inference
- Some predictions (e.g., license plate recognition) are very precise even at individual level
- Other predictions (stock prices, ad clicks) are imprecise individually but profitable on average
- Big data refers to enormously large datasets, though methods apply to smaller datasets too
- Economists combine machine learning for variable selection with OLS for valid causal inference
- Use machine learner to select subset of control variables, then do inference controlling for the selection step
- Machine learning doesn't automatically solve causal inference problems—causality requires additional assumptions

**Bayesian Methods: An Alternative to Classical Inference:**

- Bayesian inference combines data with prior beliefs to form posterior distributions for parameters
- Prior distribution can be informative (incorporating expert knowledge) or uninformative (letting data dominate)
- A 95% Bayesian credible interval can be directly interpreted as containing the parameter with probability 0.95
- Classical confidence intervals don't have this interpretation (they're based on repeated sampling)
- Markov chain Monte Carlo (MCMC) methods make Bayesian inference computationally feasible
- With large samples or uninformative priors, Bayesian results converge to classical results
- Bayesian methods were rarely used until recently due to computational intractability

**Historical Development of Statistics and Regression:**

- Statistics developed over 300+ years of theoretical and computational advances
- Central limit theorem (1733) provides foundation for inference
- Least squares method (1805) predates modern statistical inference by nearly a century
- Regression (1885) and correlation (1888) formalized by Francis Galton and Karl Pearson
- The term "standard deviation" introduced in 1894
- t distribution (1908) by William Gosset ("Student") enabled small-sample inference
- F distribution (1924) by Ronald Fisher for testing multiple restrictions
- ENIAC (1945) was the first electronic general-purpose digital computer
- Kernel regression (1964) as early nonparametric method
- Robust standard errors (1980s) are relatively recent, enabled by modern computing power
- Apple Macintosh (1984) made personal computing accessible, accelerating statistical software development

---

## Some in-class Exercises

(1) Suppose y-sub-i equals beta-one plus beta-two times x-sub-i plus u-sub-i, and u-sub-i are independent. What standard errors would you use?
(2) Suppose we have y-sub-i-j equals beta-one plus beta-two times x-sub-i-j plus u-sub-i-j, with u-sub-i-j correlated for individuals i in the same village j but uncorrelated for individuals in different villages. What standard errors would you use?
(3) Suppose y-sub-t equals beta-one plus beta-two times x-sub-t plus u-sub-t, and the error u-sub-t is correlated with u-sub-t-minus-1. What standard errors would you use?
(4) We obtain fitted model predicted y equals 3.0 with standard error 0.001, plus 5.0 with standard error 0.002 times x, n equals 200, s-sub-e equals 2.0, with standard errors given in parentheses. Predict y when x equals 10.
(5) For the preceding data give an approximate 95 percent confidence interval for the expected value of y given x equals 10. Hint: how precise are the OLS estimates?
(6) For the preceding data give an approximate 95 percent confidence interval for y given x equals 10.
