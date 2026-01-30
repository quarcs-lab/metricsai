# Chapter 11: Statistical Inference for Multiple Regression

## Learning Objectives

By the end of this chapter, you will be able to:

- Extend statistical inference from bivariate regression to multiple regression with k regressors
- Understand how the t-statistic for individual regression coefficients follows a T with n minus k degrees of freedom distribution
- Calculate and interpret standard errors for OLS slope coefficients in multiple regression: se of b-sub-j equals s-e divided by the square root of the sum of x-tilde-sub-j-i-squared
- Construct confidence intervals for population parameters beta-sub-j using the formula b-sub-j plus or minus t-sub-n-minus-k-comma-alpha-over-2, times se of b-sub-j
- Conduct hypothesis tests on individual parameters to determine statistical significance after controlling for other regressors
- Understand and apply F tests for joint hypotheses involving multiple parameter restrictions
- Interpret the F distribution with two degrees of freedom (v-one equals number of restrictions, v-two equals n minus k)
- Perform the test of overall statistical significance using H-zero: beta-two equals dot-dot-dot equals beta-k equals zero and the F statistic
- Test whether subsets of regressors are jointly statistically significant using nested model comparisons
- Present regression results in multiple standard formats (standard errors, t-statistics, p-values, confidence intervals, asterisks)

---

In [Chapter 10](s10%20Data%20Summary%20for%20Multiple%20Regression.md), you discovered that each extra square foot increases house price by 68.37 dollars—but how confident can you be in that number? Is it statistically different from zero? Could the true effect be anywhere from 30 to 100 dollars? And while Size is significant, are all six regressors together providing useful information? This chapter extends the statistical inference tools from [Chapter 7](s07%20Statistical%20Inference%20for%20Bivariate%20Regression.md) to answer these questions in multiple regression. You'll learn about t-statistics with n minus k degrees of freedom, confidence intervals for partial effects, and F-tests for evaluating joint hypotheses about multiple parameters.

### Example for this Chapter with dependent variable price

Looking at the regression results: Size has Coefficient 68.37, Standard Error 15.39, t statistic 4.44, p value 0.000, and 95 percent confidence interval from 36.45 to 101.29. Bedrooms has Coefficient 2,685, Standard Error 9,193, t statistic 0.29, p value 0.773, and 95 percent confidence interval from negative 16,379 to 21,749. Bathrooms has Coefficient 6,833, Standard Error 15,721, t statistic 0.43, p value 0.668, and 95 percent confidence interval from negative 25,771 to 39,437. Lot Size has Coefficient 2,303, Standard Error 7,227, t statistic 0.32, p value 0.753, and 95 percent confidence interval from negative 12,684 to 17,290. Age has Coefficient negative 833, Standard Error 719, t statistic negative 1.16, p value 0.259, and 95 percent confidence interval from negative 2,325 to 659. Month Sold has Coefficient negative 2,089, Standard Error 3,521, t statistic negative 0.59, p value 0.559, and 95 percent confidence interval from negative 9,390 to 5,213. Intercept has Coefficient 137,791, Standard Error 61,464, t statistic 2.24, p value 0.036, and 95 percent confidence interval from 10,321 to 265,261. Sample size n equals 29. F with 6 comma 22 degrees of freedom equals 6.83. p-value for F equals 0.0003. R-squared equals 0.651. Adjusted R-squared equals 0.555. Standard error equals 24,936.

> **Key Concept**: This regression shows multiple regressors estimated simultaneously. Only Size is statistically significant (p less than 0.05). The overall F-test (F equals 6.83, p equals 0.0003) indicates the regressors are jointly significant. Standard errors, t-statistics, p-values, and confidence intervals provide different ways to assess statistical significance.

## 11.1 Properties of the Least Squares Estimator

- Data assumption
- There is variation in the sample regressors so regressors are not perfectly correlated with each other
- generalize bivariate regression cannot estimate b-two if the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared, equals zero.
- If this data assumption does not hold then it is not possible to estimate all k regression coefficients
- see chapter 10.8 and later chapter on multicollinearity.


### Population Model Assumptions

- These are a straightforward extension of those for bivariate regression.
(1) Population model:

y equals beta-one plus beta-two times x-two, plus beta-three times x-three, plus dot-dot-dot, plus beta-k times x-k, plus u

(2) Error has zero mean conditional on all regressors:

The expected value of u-sub-i given x-two-i through x-k-i equals zero, for i equals 1 through n

(3) Error has constant variance conditional on the regressors:

The variance of u-sub-i given x-two-i through x-k-i equals sigma-u-squared, for i equals 1 through n.

(4) Errors for different observations are statistically independent: u-sub-i is independent of u-sub-j, for i not equal to j.

> **Key Concept**: The four population assumptions extend bivariate assumptions to multiple regression. Assumption 1 specifies the correct linear model. Assumption 2 ensures zero conditional mean errors. Assumption 3 requires homoskedastic errors. Assumption 4 requires independent errors across observations. Together, assumptions 1-2 ensure unbiasedness while 3-4 determine variance formulas.

### Population Model Assumptions (continued)

- Key is that Assumptions 1-2 imply the population regression line or the conditional mean of y given x-one through x-k is

The expected value of y given x-two through x-k equals beta-one plus beta-two times x-two, plus beta-three times x-three, plus dot-dot-dot, plus beta-k times x-k

- Assumptions 2-4 imply

u-sub-i is distributed with mean zero and variance sigma-u-squared, and is independent over i.

- Assumptions 1-4 imply

y-sub-i given x-two-i through x-k-i is distributed with mean the quantity beta-one plus beta-two times x-two-i, plus beta-three times x-three-i, plus dot-dot-dot, plus beta-k times x-k-i, and variance sigma-u-squared

and is independent over i.

- Similar to univariate: mu replaced by beta-one plus beta-two times x-two, plus dot-dot-dot, plus beta-k times x-k.
- Similar to bivariate: beta-one plus beta-two times x-two replaced by beta-one plus beta-two times x-two, plus dot-dot-dot, plus beta-k times x-k.

> **Key Concept**: Assumptions 1-4 together imply that y-sub-i conditional on the regressors has mean equal to the linear combination of regressors and constant variance sigma-u-squared. This generalizes univariate analysis (where mean is constant mu) and bivariate regression (where mean depends on one regressor) to multiple regressors.

### Properties of Least Squares Estimates

- Mean of b-sub-j is beta-sub-j under assumptions 1-2.
- Variance of b-sub-j is the variance of b-sub-j equals sigma-b-sub-j-squared equals sigma-u-squared divided by the sum from i equals 1 to n of x-tilde-sub-j-i-squared
- where x-tilde-sub-j-i is the residual from regressing x-sub-j-i on an intercept and all regressors other than x-sub-j-i
- from chapter 10, b-sub-j equals the sum from i equals 1 to n of x-tilde-sub-j-i times y-sub-i, all divided by the sum from i equals 1 to n of x-tilde-sub-j-i-squared.
- Standard error of the regression is s-e where s-e-squared equals 1 over n minus k, times the sum from i equals 1 to n of the quantity y-sub-i minus predicted y-sub-i, all squared
- same as for bivariate except divide by n minus k
- this ensures the expected value of s-e-squared equals sigma-u-squared given assumptions 1-4.
- Estimated variance of b-sub-j is s-e-squared divided by the sum from i equals 1 to n of x-tilde-sub-j-i-squared.
- Standard error of estimator b-sub-j is se of b-sub-j equals s-e divided by the square root of the sum from i equals 1 to n of x-tilde-sub-j-i-squared.

> **Key Concept**: The standard error formula se of b-sub-j equals s-e divided by the square root of the sum of x-tilde-sub-j-i-squared shows that precision depends on model fit (s-e) and variation in regressor j after controlling for other regressors (sum of x-tilde-sub-j-i-squared). The residual x-tilde-sub-j-i represents the part of regressor j orthogonal to all other regressors.

### When is a Slope Coefficient Precisely Estimated?

- Standard error of estimator b-sub-j is se of b-sub-j equals s-e divided by the square root of the sum from i equals 1 to n of x-tilde-sub-j-i-squared.
- So more precise estimate when
- model fit is good so s-e is small
- when there are many observations as then the sum from i equals 1 to n of x-tilde-sub-j-i-squared is big
- when the absolute value of x-tilde-sub-j-i is big
  - Which is the case if there is big dispersion in the j-th regressor after controlling for the other regressors

> **Key Concept**: Coefficient precision improves with three factors: (1) better model fit (smaller s-e), (2) larger sample size (increases sum of x-tilde-squared), and (3) greater variation in regressor j independent of other regressors (larger absolute values of x-tilde-sub-j-i). Multicollinearity reduces precision by making x-tilde values small.

### The t-Statistic

- Confidence intervals and hypothesis tests are based on the t-statistic.
- Given assumptions 1-4:

t-sub-j equals the quantity b-sub-j minus beta-sub-j, divided by se of b-sub-j, which is distributed approximately as T with n minus k degrees of freedom

- now T with n minus k degrees of freedom rather than T with n minus 2 degrees of freedom.
- The result is exact if additionally the errors are normally distributed.
- How large should the sample be?
- Larger than in the bivariate regression case.

> **Key Concept**: The t-statistic for multiple regression follows the T with n minus k degrees of freedom distribution (not T with n minus 2 degrees of freedom from bivariate regression). Fewer degrees of freedom (n minus k rather than n minus 2) means larger critical values and wider confidence intervals, reflecting the additional parameters estimated.

**Why This Matters**: Degrees of freedom directly affect every confidence interval and hypothesis test you conduct. With n equals 29 observations and k equals 7 parameters, you have only 22 degrees of freedom—not 27. This means your t-critical value is 2.074 instead of 2.052, making confidence intervals about 1 percent wider. Add more regressors and degrees of freedom drop further, widening intervals even more. This is why parsimonious models (fewer regressors) are preferred when possible—you preserve degrees of freedom and get more precise inference.

We've established that OLS estimates have the right distribution for inference. But what makes OLS the right estimator to use in the first place? Let's examine the optimality properties that justify using OLS.

## 11.2 Estimators of Model Parameters

- We want OLS estimator b-sub-j for the coefficient j-th regressor x-sub-j to be
- centered on beta-sub-j: unbiased and consistent
- smallest variance (best) among such estimators.
- Centering
- b-sub-j is unbiased for beta-sub-j (the expected value of b-sub-j equals beta-sub-j) given assumptions 1-2
- b-sub-j is consistent for beta-sub-j (b-sub-j approaches beta-sub-j as n approaches infinity) given assumptions 1-2 plus a little more to ensure the variance of b-sub-j approaches zero as n approaches infinity.
- Smallest variance
- b-sub-j is best linear unbiased for beta-sub-j given assumptions 1-4
  - i.e. smallest variance among unbiased estimators that are a weighted average of y-sub-i, the sum over i of a-sub-i times y-sub-i, with weights a-sub-i depending on the regressors
- b-sub-j is best unbiased for beta-sub-j given assumptions 1-4 and normally distributed errors
  - i.e. minimum variance among unbiased estimators

> **Key Concept**: OLS estimators in multiple regression have three key properties: (1) unbiasedness (expected value equals true parameter) under assumptions 1-2, (2) consistency (converges to true parameter) under assumptions 1-2 plus regularity conditions, and (3) Best Linear Unbiased Estimator or BLUE property (minimum variance among linear unbiased estimators) under assumptions 1-4. With normal errors, OLS is best among all unbiased estimators.

Now that we know OLS is the best estimator, let's use it to construct confidence intervals that quantify uncertainty about the true parameter values.

## 11.3 Confidence Intervals

- Usual estimate plus or minus critical t-value times standard error.
- A 100 times the quantity 1 minus alpha percent confidence interval for beta-sub-j is

b-sub-j plus or minus t-sub-n-minus-k-semicolon-alpha-over-2, times se of b-sub-j,

where

- b-sub-j is the slope estimate
- se of b-sub-j is the standard error of b-sub-j
- t-sub-n-minus-k-comma-alpha-over-2 is the critical value
- A 95 percent confidence interval is approximately

b-sub-j plus or minus 2 times se of b-sub-j.

> **Key Concept**: Confidence intervals in multiple regression follow the same structure as bivariate regression: estimate plus or minus critical value times standard error. The critical value comes from the T with n minus k degrees of freedom distribution. For 95 percent confidence, the approximate rule "estimate plus or minus 2 times standard error" works well when n is large.

### Confidence Interval Example

- Regression of house price on house size and five other regressors
- output given at start of slides
- includes a 95 percent confidence interval for beta-sub-SF is the interval from 36.45 to 100.29.
- Manual computation using b-sub-SF equals 68.37 and se of b-sub-SF equals 15.39:

Starting with b-sub-SF plus or minus t-sub-n-minus-k-comma-alpha-over-2, times se of b-sub-SF, this equals 68.37 plus or minus t-sub-22-comma-0.025, times 15.39. This equals 68.37 plus or minus 2.074 times 15.39. This equals 68.37 plus or minus 31.92. This gives the interval from 36.45 to 100.29.

> **Key Concept**: For the house price example with n equals 29 and k equals 7, the 95 percent confidence interval for the Size coefficient is calculated as 68.37 plus or minus 2.074 times 15.39, yielding 36.45 to 100.29. The critical value t-sub-22-comma-0.025 equals 2.074 from the T distribution with 22 degrees of freedom. We're 95 percent confident this interval contains the true population coefficient.

Confidence intervals tell us a range of plausible values. But often we want to test specific claims—like "Does Size have any effect at all?" or "Is the effect exactly 50 dollars per square foot?" Let's see how to conduct these hypothesis tests.

## 11.4 Tests on Individual Parameters

- Two-sided test that beta-sub-j equals beta-sub-j-star

H-zero: beta-sub-j equals beta-sub-j-star against H-a: beta-sub-j does not equal beta-sub-j-star

- Use

t equals the quantity b-sub-j minus beta-sub-j-star, divided by se of b-sub-j, which is distributed as T with n minus k degrees of freedom

- Can also do one-sided tests.

> **Key Concept**: Testing individual parameters in multiple regression uses the same t-statistic structure as bivariate regression: t equals the quantity estimate minus hypothesized value, divided by standard error. The statistic follows a T with n minus k degrees of freedom distribution. Both two-sided and one-sided tests are possible.

### Tests of Statistical Significance

- Test whether there is any relationship between y and x-sub-j (after controlling for the other regressors).
- Does beta-sub-j equal zero? Formally test

H-zero: beta-sub-j equals zero against H-a: beta-sub-j does not equal zero

- Use t-statistic where beta-sub-j equals zero. So simply

t equals b-sub-j divided by se of b-sub-j, which is distributed as T with n minus k degrees of freedom

- Aside: the absolute value of t is greater than 1 if R-bar-squared increases when a regressor is added
- so usual t-test is more demanding than including regressor if adjusted R-squared increases.

> **Key Concept**: The test of statistical significance evaluates whether regressor x-sub-j has any relationship with y after controlling for all other regressors. The null hypothesis H-zero: beta-sub-j equals zero tests whether the coefficient is zero. The test statistic simplifies to t equals b-sub-j divided by se of b-sub-j. A regressor is statistically significant if the absolute value of t exceeds the critical value.

### Example: House Price

- Test of statistical significance of size for house price example
- t equals b-sub-Size divided by se of b-sub-Size, equals 68.37 divided by 15.39, equals 4.44
- So for two-sided test
  - p equals 2 times ttail of 22 comma 4.44, equals 0.0002, which is less than 0.05, so reject H-zero
  - or c equals invttail of 22 comma 0.05, equals 1.717, and the absolute value of t equals 4.44 is greater than c, so reject H-zero
- Conclude that Size is statistically significance at level 0.05
- Test of H-zero: beta-two equals 50 against H-a: beta-two does not equal 50
- t equals the quantity b-sub-Size minus 50, divided by se of b-sub-Size, equals the quantity 68.37 minus 50, divided by 15.39, equals 1.194
- So for two-sided test
  - p equals 2 times ttail of 22 comma 1.194, equals 0.245, which is greater than 0.05, so do not reject H-zero
  - or c equals invttail of 22 comma 0.05, equals 1.717, and the absolute value of t equals 1.194 is less than c, so do not reject H-zero
- Conclude that Size is not statistically different from 50 at level 0.05

> **Key Concept**: For the Size coefficient, t equals 4.44 with p equals 0.0002, strongly rejecting H-zero: beta equals zero. However, testing H-zero: beta equals 50 yields t equals 1.194 with p equals 0.245, failing to reject. This shows Size is statistically significant (nonzero) but we cannot reject that its value is 50. Different null hypotheses can lead to different conclusions.

Individual t-tests are powerful for testing one coefficient at a time. But what if you want to test whether multiple coefficients are simultaneously zero? Or whether several parameters satisfy a set of restrictions together? For these questions, we need a different tool.

## 11.5 Joint Hypothesis Tests

- Suppose we wish to test more than one restriction on the parameters.
- e.g. both beta-two equals zero and beta-three equals zero
- e.g. all slope parameters equal zero
- e.g. beta-two equals negative beta-three and 2 times beta-four plus beta-six equals 9.
- Tests of several restrictions are called tests of joint hypotheses.
- t tests can handle test of only one restriction on the parameters.
- Instead use F tests and the F distribution
- this nests t tests and t distribution as a special case
- for tests of a single restriction F equals t-squared.

> **Key Concept**: Joint hypothesis tests evaluate multiple parameter restrictions simultaneously. Examples include testing whether several coefficients are jointly zero or whether linear combinations of parameters satisfy specific values. t-tests handle only one restriction at a time. F-tests extend to multiple restrictions, with F equals t-squared for single restrictions.

**Why This Matters**: Imagine testing whether education, experience, and gender jointly affect wages. You could run three separate t-tests, but this doesn't answer the key question: "Do these three variables together add explanatory power?" The F-test answers this directly. It's also essential for model selection—if bedrooms, bathrooms, lot size, age, and month sold are jointly insignificant beyond Size, you should use the simpler model with only Size. F-tests let you rigorously compare nested models and avoid overfitting.

### 11.5 Joint Hypothesis Tests: F Distribution

- The F distribution is for a random variable that is greater than zero
- it is right-skewed
- it depends on two parameters v-one and v-two called degrees of freedom
- v-one equals number of restrictions; v-two equals n minus k.
![](https://cdn.mathpix.com/cropped/12658980-b149-4df5-a03e-72200f64dac3-18.jpg?height=498&width=670&top_left_y=355&top_left_x=297)

> **Key Concept**: The F distribution is right-skewed and takes only positive values. It has two degrees of freedom parameters: v-one equals the number of restrictions being tested, and v-two equals n minus k (sample size minus number of parameters). The distribution's shape depends on both degrees of freedom.

### Probabilities and Inverse Probabilities for the F

- General notation is F with v-one comma v-two degrees of freedom.
- The critical values (and p values) for the F distribution vary with the two degrees of freedom
- For F with v-one comma v-two degrees of freedom, the critical value (area in right tail) is
- decreasing in both v-one and v-two
- Some representative values
- 5 percent and one restriction: F with 1 comma 30 degrees of freedom at 0.05 level equals 4.17, and F with 1 comma infinity degrees of freedom at 0.05 level equals 3.84
- 5 percent and ten restrictions: F with 10 comma 30 degrees of freedom at 0.05 level equals 2.16, and F with 10 comma infinity degrees of freedom at 0.05 level equals 1.83.

> **Key Concept**: Critical values for the F distribution decrease as degrees of freedom increase. At the 5 percent level with one restriction, the critical value is 4.17 for finite samples (v-two equals 30) and 3.84 asymptotically (v-two equals infinity). With ten restrictions, critical values are much smaller: 2.16 and 1.83 respectively. More restrictions and larger samples both reduce critical values.

### The F Statistic

- Consider two models that are nested in each other.
- General model: unrestricted model or complete model, is a model with k regressors, so

y equals beta-one plus beta-two times x, plus beta-three times x-three, plus dot-dot-dot, plus beta-k times x-k, plus u

- Restricted model or reduced model places q restrictions on beta-one, beta-two, dot-dot-dot, beta-k.
- e.g. all regressors but the intercept are dropped so q equals k minus 1.
- e.g. a subset of g regressors is included so q equals k minus g.
- e.g. one regressor is dropped so q equals 1.
- In general the formula for the F statistic is complicated
- just use computer output.

> **Key Concept**: F-tests compare nested models. The unrestricted (complete) model has k regressors. The restricted (reduced) model imposes q restrictions on the parameters. Common examples: dropping all slopes (q equals k minus 1), including only g regressors (q equals k minus g), or dropping one regressor (q equals 1). The F-statistic formula is complex—use computer output.

### F Tests

- An F test is a two-sided test of
- H-zero: The q parameter restrictions implied by the restricted model are correct
- against H-a: The q parameter restrictions implied by the restricted model are incorrect.
- Define alpha to be the desired significance level of the test.
- p-value: p equals the probability that F with q comma n minus k degrees of freedom is greater than or equal to F
- H-zero is rejected if p is less than alpha.
- critical value: c is such that c equals F with q comma n minus k degrees of freedom at significance level alpha, equivalently the probability that the absolute value of F with q comma n minus k degrees of freedom is greater than or equal to c, equals alpha
- H-zero is rejected if F is greater than c.

> **Key Concept**: F-tests evaluate whether q parameter restrictions are correct. The null hypothesis is that restrictions hold; the alternative is that they don't. Using p-values, reject H-zero if p is less than alpha. Using critical values, reject if the computed F exceeds the critical value c. Both approaches are equivalent. F-tests are always two-sided tests.

### Example: Test of Overall Statistical Significance

- Special case that is a test

H-zero: beta-two equals zero through beta-k equals zero, against H-a: At least one of beta-two through beta-k does not equal zero.

- Regression programs automatically provide this in regression output.
- For house price example with k equals 7 regressors including intercept
- Test statistic is F with q comma n minus k degrees of freedom equals F with 6 comma 22 degrees of freedom distributed
- F equals 6.83 with p equals 0.0003
- so reject H-zero at level 0.05.
- conclude regressors are jointly statistically significant.
- Test only says that the regressors are jointly statistically significant
- It does not say which regressors are individually statistically significant
  - In this example only Size was individually statistically significant at 5 percent

> **Key Concept**: The test of overall statistical significance tests H-zero: all slope coefficients equal zero (beta-two through beta-k equal zero) against H-a: at least one is nonzero. This is automatically reported in regression output. For the house price example, F equals 6.83 with p equals 0.0003 strongly rejects H-zero, showing regressors are jointly significant even though only Size is individually significant at 5 percent.

### Test of Subsets of Regressors

- Clearly variable Size matters
- suppose we want to test whether the remaining regressors matter.
- The unrestricted model or complete model has all k regressors

y equals beta-one plus beta-two times x-two, plus dot-dot-dot plus beta-g times x-g, plus beta-g-plus-1 times x-g-plus-1, plus dot-dot-dot, plus beta-k times x-k, plus epsilon

- The restricted model or reduced model has only the first g regressors

y equals beta-one plus beta-two times x-two, plus dot-dot-dot plus beta-g times x-g, plus epsilon

- We test whether the last k minus g coefficients are statistically significant.

H-zero: beta-g-plus-1 equals zero through beta-k equals zero, against H-a: At least one of beta-g-plus-1 through beta-k does not equal zero

- A specialized test command yields F equals 0.417 with p equals 0.832, which is greater than 0.05
- we do not reject H-zero: beta-three through beta-seven all equal zero at significance level 0.05
- the additional five regressors are jointly statistically insignificant
- it is best to just include Size as a regressor.

> **Key Concept**: Testing subsets of regressors asks whether the last k minus g coefficients are jointly significant. For house price, testing whether bedrooms, bathrooms, lot size, age, and month sold add value beyond size alone yields F equals 0.417 with p equals 0.832. We fail to reject H-zero, concluding these five regressors are jointly insignificant. The best model includes only Size.

**Quick Check**: Before moving on, test your understanding of joint hypothesis tests: (1) Why can't you use individual t-tests to evaluate whether five regressors are jointly significant? (2) What do the two degrees of freedom (v-one and v-two) represent in an F distribution? (3) For the house price example, the overall F-test rejects (F equals 6.83, p equals 0.0003) but the subset test does not reject (F equals 0.417, p equals 0.832)—how is this possible? (4) If adjusted R-squared increases when adding a regressor, does that mean the regressor is statistically significant at 5 percent? Understanding F-tests is crucial for model selection and avoiding overfitting.

### Further Details

- For test of a single restriction F equals t-squared
- The F test gives the same answer as a two-sided t test
- The p value is the same
- The critical value for F equals that for t squared
  - In particular for large n the F with 1 comma n minus k degrees of freedom critical value is 1.96-squared equals 3.84

- Some packages report chisquared tests rather than F tests
- in large samples with n approaches infinity
- q times F with q comma infinity degrees of freedom is distributed chi-squared with q degrees of freedom (chi-squared with q degrees of freedom).
- to get the F-statistic divide the chi-squared-statistic by q.
- Separate tests of many hypotheses
- with many separate tests there is high probability of erroneously finding a variable statistically significant
- adjusting for multiple testing is beyond the scope of this text.

> **Key Concept**: For a single restriction, F equals t-squared, so F-tests and two-sided t-tests are equivalent. The 5 percent critical value for F with 1 comma infinity degrees of freedom is 1.96-squared equals 3.84. Some packages report chi-squared tests: in large samples, q times F is distributed chi-squared with q degrees of freedom. Multiple testing increases Type I error probability but adjustments are beyond this text's scope.

The F-tests we've seen so far work with any type of standard errors (including robust standard errors). But under the classical assumptions 1-4, the F-statistic has a particularly simple and intuitive form based on residual sums of squares.

## 11.6 F Statistic under Assumptions 1-4

- The proceeding presentation of the F test also applies following regression with robust standard errors.
- Now specialize to default standard errors (assumptions 1-4)
- then analysis simplifies and provides some insights.
- Intuitively, reject restrictions if the restricted model has much poorer fit
- Reject restrictions if RSS-sub-r minus RSS-sub-u is large where
  - RSS-sub-r is residual sum of squares in restricted model
  - RSS-sub-u is residual sum of squares in unrestricted model
- Under assumptions 1-4 the F statistic is a function of RSS-sub-r minus RSS-sub-u

> **Key Concept**: Under assumptions 1-4 (homoskedastic errors), the F-statistic simplifies to a function of residual sums of squares. Intuition: reject restrictions if the restricted model fits much worse than unrestricted model, meaning RSS-sub-r minus RSS-sub-u is large. This RSS-based formula also works with robust standard errors.

### F Statistic under Assumptions 1-4

- Under H-zero and assumptions 1-4 the F-statistic can be shown to be

F equals the quantity RSS-sub-r minus RSS-sub-u, divided by q, all divided by the quantity RSS-sub-u divided by n minus k, which is distributed as F with q comma n minus k degrees of freedom

- This is a two-sided test - there is no one-sided test
- Reject H-zero when F is large, since then restricted model fits much worse
- Reject at level alpha if p equals the probability that F with k minus 1 comma n minus k degrees of freedom is greater than F, and this is less than alpha
- Or reject at level alpha if F is greater than c equals F with k minus 1 comma n minus k degrees of freedom at significance level alpha

> **Key Concept**: The F-statistic formula F equals the quantity RSS-sub-r minus RSS-sub-u, divided by q, all divided by the quantity RSS-sub-u divided by n minus k, shows how F measures the relative worsening of fit when restrictions are imposed. Large F values indicate the restricted model fits much worse, leading to rejection of the restrictions.

### Test Overall Statistical Significance under Assumptions 1-4

- Test H-zero: beta-two equals zero through beta-k equals zero versus H-a: At least one of beta-two through beta-k does not equal zero.
- The restricted model is an intercept-only model with predicted y-sub-i equals y-bar
- so RSS-sub-r equals the sum from i equals 1 to n of the quantity y-sub-i minus y-bar, all squared, which equals TSS.
- Some algebra then shows that in this special case

F equals the quantity R-squared divided by k minus 1, all divided by the quantity 1 minus R-squared, divided by n minus k, which is distributed as F with k minus 1 comma n minus k degrees of freedom,

- where R-squared is the usual R-squared from the regression of y on all regressors.
- Example: House price regressed on all regressors
- R-squared equals 0.6506, n equals 29, k equals 7
- F equals the quantity 0.6506 divided by 6, all divided by the quantity 0.3494 divided by 22, which equals 6.827.
- p equals Ftail of 6 comma 22 comma 6.827, equals 0.000342
- reject H-zero at 5 percent since p is less than 0.05.

> **Key Concept**: For the overall significance test, the restricted model is intercept-only with RSS-sub-r equals total sum of squares. This yields the convenient formula F equals R-squared divided by k minus 1, all divided by 1 minus R-squared divided by n minus k. For house price with R-squared equals 0.6506, this gives F equals 6.827 with p equals 0.000342, strongly rejecting that all slopes are zero.

### Test of Subsets of Regressors under Assumptions 1-4

- Test whether regressors other than house price are statistically significant
- so test H-zero: beta-sub-bed equals zero, beta-sub-bath equals zero, dot-dot-dot, beta-sub-month equals zero.
- Manual computation
- Full model: RSS-sub-u equals 13,679,397,855 (k equals 7 including intercept).
- Restricted model: RSS-sub-r equals 14,975,101,655 (g equals 2: Size plus intercept)
- F equals the quantity 14,975,101,655 minus 13,679,397,855, divided by 5, all divided by the quantity 13,679,397,855 divided by 22, which equals 0.417.
- p equals Ftail of 5 comma 22 comma 0.417, equals 0.832, which is greater than 0.05
- c equals invFtail of 22 comma 0.05 comma 5 comma 22, equals 2.66
- do not reject H-zero at level 0.05.
- The additional five regressors are not jointly statistically significant at 5 percent.

> **Key Concept**: Testing whether five regressors beyond Size are jointly significant uses RSS values from full and restricted models. F equals the quantity RSS difference divided by number of restrictions, all divided by the quantity unrestricted RSS divided by n minus k. With F equals 0.417 and p equals 0.832, we cannot reject that these five coefficients are jointly zero, suggesting the simpler model with only Size is adequate.

### Relationship between F test and adjusted R-Squared

- Under assumptions 1-4
- as regressors are added R-bar-squared increases if and only if F is greater than 1
- if a single regressor is added R-bar-squared increases if and only if the absolute value of t is greater than 1.
- So including a regressor or regressors on the basis of increasing R-bar-squared is a much lower threshold than testing at 5 percent.

> **Key Concept**: Adjusted R-squared increases when adding regressors if and only if F is greater than 1 (for multiple regressors) or the absolute value of t is greater than 1 (for single regressor). Since 5 percent significance typically requires t greater than 2 or F greater than 4, the adjusted R-squared criterion (requiring only F greater than 1) is a much lower threshold than formal significance testing.

You now know how to conduct all the major statistical tests in multiple regression. But how should you present these results to others? Let's examine the standard formats for reporting regression output.

## 11.7 Presentation of Regression Results

- Save space by not reporting all of b, s-b, t and p.
- 1. Report just coefficients and standard errors

Predicted Price equals 111,691 with standard error 21,489 in parentheses, plus 73.77 with standard error 11.17 in parentheses, times Size, plus 1,553 with standard error 7,846 in parentheses, times Bedrooms; R-squared equals 0.618.

- 2. Report just coefficients and t statistics for H-zero: beta-two equals zero

Predicted Price equals 111,691 with t-statistic 5.35 in parentheses, plus 72.41 with t-statistic 6.60 in parentheses, times Size, plus 1,553 with t-statistic 0.20 in parentheses, times Bedrooms; R-squared equals 0.618.

- 3. Report just coefficients and p values for H-zero: beta-two equals zero

Predicted Price equals 111,691 with p-value 0.000 in parentheses, plus 72.41 with p-value 0.000 in parentheses, times Size, plus 1,553 with p-value 0.845 in parentheses, times Bedrooms; R-squared equals 0.618.

- 4. Report just coefficients and 95 percent confidence intervals.
- 5. Report just coefficients and asterisks:
- one if statistically significant at 10 percent
- two if statistically significant at 5 percent
- three if statistically significant at 1 percent.

> **Key Concept**: Regression results can be presented in multiple space-efficient formats: (1) coefficients with standard errors, (2) coefficients with t-statistics, (3) coefficients with p-values, (4) coefficients with confidence intervals, or (5) coefficients with significance asterisks. All formats convey the same information but emphasize different aspects. Format 1 (standard errors) is most common in economics.

## 11.7 Presentation of Regression Results

- Different ways to present results from the same regression
- same coefficients but different quantities in parentheses.

Comparing five presentation formats for the same regression: Results 1 shows standard errors, Results 2 shows t statistics, Results 3 shows p-values, Results 4 shows 95 percent confidence intervals, Results 5 shows asterisks. For Size: coefficient 72.41 with standard error 13.29, or t-statistic 5.44, or p-value 0.000, or 95 percent confidence interval from 45.07 to 99.75, or three asterisks. For Bedrooms: coefficient 1,553 with standard error 7,847, or t-statistic 0.20, or p-value 0.845, or 95 percent confidence interval from negative 14,576 to 17,682, or no asterisks. For Intercept: coefficient 11,691 with standard error 27,589, or t-statistic 4.05, or p-value 0.000, or 95 percent confidence interval from 54,981 to 168,401, or three asterisks. All formats show R-squared 0.618, F with 2 comma 26 degrees of freedom equals 21.93, n equals 29.

> **Key Concept**: The table demonstrates five equivalent ways to present the same regression results. All formats report identical coefficients (Size equals 72.41, Bedrooms equals 1,553) but differ in what appears in parentheses. Key summary statistics (R-squared, F-statistic, sample size) are reported regardless of format. Choose format based on audience and journal conventions.

### Some in-class Exercises

(1) We obtain fitted model predicted y equals 3.0 with standard error 1.5 in parentheses, plus 5.0 with standard error 2.0 in parentheses, times x-two, plus 7.0 with standard error 2.0 in parentheses, times x-three, with n equals 200, with standard errors given in parentheses. Provide an approximate 95 percent confidence interval for the population slope parameter.
(2) For the preceding data is x-two statistically significant at level 0.05?
(3) For the preceding data test the claim that the coefficient of x-three equals 10.0 at significance level 0.05.
(4) Consider the model y equals beta-one plus beta-two times x-two, plus plus beta-three times x-three, plus dot-dot-dot, plus beta-k times x-k, plus u. We wish to test the claim that the only regressors that should be included in the model are x-two and x-three. State H-zero and H-a for this test, and give the degrees of freedom for the resultant F test.

---

## Key Takeaways

**Extension from Bivariate to Multiple Regression:**
- Multiple regression extends bivariate regression (Chapter 7) by including k regressors instead of just one regressor plus intercept
- The key difference is using T with n minus k degrees of freedom distribution instead of T with n minus 2 degrees of freedom distribution for t-statistics and confidence intervals
- Most inference procedures are straightforward extensions: same logic but different degrees of freedom
- New concept introduced: F tests for joint hypotheses involving restrictions on multiple parameters simultaneously
- Individual parameter tests now test significance "after controlling for" or "holding constant" all other regressors in the model
- Example: House price regressed on size, bedrooms, bathrooms, lot size, age, and month sold (k equals 7 including intercept)
- Multiple regression allows us to isolate the effect of one variable while accounting for other factors

**Data Assumptions and Multicollinearity (Section 11.1):**
- Data assumption: There must be variation in the sample regressors and regressors cannot be perfectly correlated with each other
- This generalizes the bivariate requirement that the sum of the quantity x-sub-i minus x-bar, all squared, must be greater than zero to prevent division by zero
- If regressors are perfectly correlated (perfect multicollinearity), it is impossible to estimate all k regression coefficients
- This issue is addressed in Chapter 10.8 and later chapters on multicollinearity
- Imperfect multicollinearity (high but not perfect correlation) is common and affects precision but not unbiasedness

**Four Population Model Assumptions:**
- **Assumption 1 (Correct model):** Population model is y equals beta-one plus beta-two times x-two, plus beta-three times x-three, plus dot-dot-dot, plus beta-k times x-k, plus u
- **Assumption 2 (Mean-zero errors):** The expected value of u-sub-i given x-two-i through x-k-i equals zero for i equals 1 through n (errors have zero mean conditional on all regressors)
- **Assumption 3 (Homoskedasticity):** The variance of u-sub-i given x-two-i through x-k-i equals sigma-u-squared for i equals 1 through n (constant error variance across all regressor values)
- **Assumption 4 (Independence):** u-sub-i is independent of u-sub-j for i not equal to j (errors for different observations are statistically independent)
- Assumptions 1-2 imply the conditional mean the expected value of y given x-two through x-k equals beta-one plus beta-two times x-two, plus dot-dot-dot, plus beta-k times x-k (the population regression line)
- Assumptions 2-4 imply u-sub-i is distributed with mean zero and variance sigma-u-squared, and is independent over i
- Assumptions 1-4 together imply y-sub-i given x-two-i through x-k-i is distributed with mean beta-one plus beta-two times x-two-i, plus dot-dot-dot, plus beta-k times x-k-i, and variance sigma-u-squared, and is independent over i
- These assumptions extend bivariate assumptions by replacing beta-one plus beta-two times x-two with beta-one plus beta-two times x-two, plus dot-dot-dot, plus beta-k times x-k

**Properties of Least Squares Estimates:**
- Mean of b-sub-j equals beta-sub-j under assumptions 1-2 (unbiasedness: the expected value of b-sub-j equals beta-sub-j)
- Variance of b-sub-j is the variance of b-sub-j equals sigma-b-sub-j-squared equals sigma-u-squared divided by the sum of x-tilde-sub-j-i-squared, where x-tilde-sub-j-i is the residual from regressing x-sub-j on all other regressors
- The residual x-tilde-sub-j-i represents the part of x-sub-j-i that is orthogonal to (uncorrelated with) all other regressors
- From Chapter 10: b-sub-j equals the sum of x-tilde-sub-j-i times y-sub-i, all divided by the sum of x-tilde-sub-j-i-squared (OLS coefficient as weighted average of y values)
- Standard error of the regression is s-e where s-e-squared equals 1 over n minus k, times the sum of the quantity y-sub-i minus predicted y-sub-i, all squared (sum of squared residuals divided by n minus k)
- Division by n minus k (instead of n minus 2 in bivariate) ensures the expected value of s-e-squared equals sigma-u-squared given assumptions 1-4 (unbiased estimator)
- Estimated variance of b-sub-j is s-e-squared divided by the sum of x-tilde-sub-j-i-squared (plug in estimated error variance)
- Standard error of estimator b-sub-j is se of b-sub-j equals s-e divided by the square root of the sum of x-tilde-sub-j-i-squared (estimated standard deviation of the sampling distribution)

**Variance and Standard Errors in Multiple Regression:**
- The variance formula the variance of b-sub-j equals sigma-u-squared divided by the sum of x-tilde-sub-j-i-squared involves residuals x-tilde-sub-j-i from an auxiliary regression
- To compute x-tilde-sub-j-i: regress x-sub-j on an intercept and all other regressors, then extract the residuals
- If x-sub-j is highly correlated with other regressors, the sum of x-tilde-sub-j-i-squared will be small, leading to large variance
- This is the source of the multicollinearity problem: high correlation inflates standard errors
- The standard error se of b-sub-j combines two sources of uncertainty: model fit (s-e) and regressor variation (sum of x-tilde-squared)

**Precision Factors for Coefficient Estimates:**
- Standard error formula se of b-sub-j equals s-e divided by the square root of the sum of x-tilde-sub-j-i-squared shows three ways to get more precise estimates:
- **Factor 1 (Good model fit):** Smaller s-e leads to smaller standard error (better fitting model gives more precise estimates)
- **Factor 2 (Many observations):** Larger n leads to larger sum of x-tilde-squared, which leads to smaller standard error (more data improves precision)
- **Factor 3 (Large absolute values of x-tilde-sub-j-i):** More variation in the jth regressor after controlling for other regressors leads to smaller standard error
- Factor 3 means precision is high when there is big dispersion in x-sub-j that is independent of other regressors
- Multicollinearity reduces precision because high correlation among regressors makes the sum of x-tilde-squared small
- These factors apply to each coefficient separately: some coefficients may be precisely estimated while others are not

**The t-Statistic and T with n minus k degrees of freedom Distribution:**
- Confidence intervals and hypothesis tests in multiple regression are based on the t-statistic
- Given assumptions 1-4: t-sub-j equals the quantity b-sub-j minus beta-sub-j, divided by se of b-sub-j, which is distributed approximately as T with n minus k degrees of freedom
- The distribution is now T with n minus k degrees of freedom rather than T with n minus 2 degrees of freedom from bivariate regression (fewer degrees of freedom)
- Degrees of freedom equals n minus k where k includes all regressors (slopes plus intercept)
- The t-statistic result is exact if errors are additionally normally distributed, otherwise approximate for large n
- Sample size should be larger than in bivariate regression case for good approximation (rule of thumb: n greater than 30 plus k)
- Critical values from T with n minus k degrees of freedom are used for confidence intervals and hypothesis tests

**Unbiased, Consistent, and BLUE Properties (Section 11.2):**
- **Unbiasedness:** b-sub-j is unbiased for beta-sub-j (the expected value of b-sub-j equals beta-sub-j) given assumptions 1-2
- **Consistency:** b-sub-j is consistent for beta-sub-j (b-sub-j approaches beta-sub-j as n approaches infinity) given assumptions 1-2 plus conditions ensuring the variance of b-sub-j approaches zero as n approaches infinity
- **Best Linear Unbiased, or BLUE:** b-sub-j has smallest variance among unbiased estimators that are linear in y (sum of a-sub-i times y-sub-i) given assumptions 1-4
- **Best Unbiased:** b-sub-j has minimum variance among all unbiased estimators given assumptions 1-4 and normally distributed errors
- The Gauss-Markov Theorem establishes the BLUE property: OLS is optimal among linear unbiased estimators
- These properties parallel those from bivariate regression (Chapter 6) and extend to the multiple regression context
- The optimality results justify using OLS as the default estimation method

**Confidence Intervals for Multiple Regression (Section 11.3):**
- General formula for 100 times the quantity 1 minus alpha percent confidence interval: b-sub-j plus or minus t-sub-n-minus-k-comma-alpha-over-2, times se of b-sub-j
- Structure is "estimate plus or minus critical value times standard error" (same as bivariate regression)
- Critical value t-sub-n-minus-k-comma-alpha-over-2 is from the T with n minus k degrees of freedom distribution
- For 95 percent confidence interval: approximately b-sub-j plus or minus 2 times se of b-sub-j when n is large
- Example: 95 percent CI for house size coefficient with b-sub-SF equals 68.37, se of b-sub-SF equals 15.39, n equals 29, k equals 7 gives the interval from 36.45 to 100.29
- Manual computation: 68.37 plus or minus t-sub-22-comma-0.025, times 15.39, equals 68.37 plus or minus 2.074 times 15.39, equals 68.37 plus or minus 31.92, equals the interval from 36.45 to 100.29
- Interpretation: We are 95 percent confident the interval from 36.45 to 100.29 contains the true population coefficient
- Confidence level can be adjusted: common choices are 90 percent, 95 percent, 99 percent (higher confidence leads to wider intervals)

**Tests on Individual Parameters (Section 11.4):**
- Two-sided test of H-zero: beta-sub-j equals beta-j-star against H-a: beta-sub-j does not equal beta-j-star uses t equals the quantity b-sub-j minus beta-j-star, divided by se of b-sub-j, which is distributed as T with n minus k degrees of freedom
- The test statistic follows the T with n minus k degrees of freedom distribution under the null hypothesis
- P-value approach: Calculate p equals the probability that the absolute value of T-sub-n-minus-k is greater than or equal to the absolute value of t, and reject H-zero if p is less than alpha
- Critical value approach: Find c equals t-sub-n-minus-k-comma-alpha-over-2, and reject H-zero if the absolute value of t is greater than c
- One-sided tests are also possible: same structure as in bivariate regression but using T with n minus k degrees of freedom distribution
- Example: Testing H-zero: beta-sub-Size equals 50 gives t equals the quantity 68.37 minus 50, divided by 15.39, equals 1.194, with p equals 0.245 which is greater than 0.05, so do not reject H-zero

**Tests of Statistical Significance:**
- Test whether there is any relationship between y and x-sub-j after controlling for other regressors
- Null hypothesis: H-zero: beta-sub-j equals zero against H-a: beta-sub-j does not equal zero (most common test in regression analysis)
- Test statistic simplifies to t equals b-sub-j divided by se of b-sub-j, which is distributed as T with n minus k degrees of freedom when testing beta-sub-j equals zero
- Reject H-zero if p-value is less than alpha or if the absolute value of t is greater than critical value from T with n minus k degrees of freedom distribution
- Example: Size coefficient has t equals 68.37 divided by 15.39 equals 4.44, with p equals 0.0002 which is less than 0.05, so Size is statistically significant
- Statistical significance after controlling for other regressors is different from marginal (bivariate) significance
- A regressor can be statistically significant in bivariate regression but insignificant in multiple regression (or vice versa)
- Aside: the absolute value of t is greater than 1 if and only if adjusted R-squared increases when regressor is added to the model
- So the usual t-test (alpha equals 0.05) is more demanding than the adjusted R-squared criterion for including a regressor

**Joint Hypothesis Tests - Introduction (Section 11.5):**
- Joint hypothesis tests evaluate restrictions on multiple parameters simultaneously
- Examples: H-zero: beta-two equals zero and beta-three equals zero; H-zero: all slope parameters equal zero; H-zero: beta-two equals negative beta-three and 2 times beta-four plus beta-six equals 9
- T-tests can only handle one restriction on the parameters at a time
- Joint tests with q restrictions require F tests and the F distribution
- The F distribution nests the t distribution as a special case: for one restriction, F equals t-squared
- Joint tests answer questions like "Are these regressors jointly significant?" that cannot be answered by individual t-tests

**The F Distribution:**
- The F distribution is for a random variable that takes only positive values (F greater than zero)
- The distribution is right-skewed (not symmetric)
- It depends on two parameters v-one and v-two called degrees of freedom
- For regression tests: v-one equals number of restrictions (q), v-two equals n minus k
- Notation: F with v-one comma v-two degrees of freedom, or F-sub-v-one-comma-v-two
- Critical values decrease as both v-one and v-two increase
- Example critical values: F-sub-1-comma-30-semicolon-0.05 equals 4.17, F-sub-1-comma-infinity-semicolon-0.05 equals 3.84, F-sub-10-comma-30-semicolon-0.05 equals 2.16, F-sub-10-comma-infinity-semicolon-0.05 equals 1.83

**F Tests and Test Procedures:**
- F tests compare two nested models: unrestricted (complete) model with k regressors versus restricted (reduced) model with q restrictions
- Null hypothesis H-zero: The q parameter restrictions are correct
- Alternative hypothesis H-a: The q parameter restrictions are incorrect
- F-statistic measures how much worse the restricted model fits compared to unrestricted model
- P-value: p equals the probability that F-sub-q-comma-n-minus-k is greater than or equal to F, where F is the computed F-statistic
- Reject H-zero if p is less than alpha (restricted model fits significantly worse)
- Critical value approach: Reject H-zero if F is greater than c where c equals F-sub-q-comma-n-minus-k-semicolon-alpha
- F tests are always two-sided (no one-sided F test)
- In general the F-statistic formula is complicated and should be obtained from computer output
- For a single restriction (q equals 1): F equals t-squared and the F test gives same result as two-sided t test

**Test of Overall Statistical Significance:**
- Special case: Test H-zero: beta-two equals zero through beta-k equals zero (all slope coefficients equal zero) against H-a: At least one beta-sub-j does not equal zero
- This tests whether the model has any explanatory power at all
- Regression programs automatically provide this test in standard output
- Test statistic is F with q comma n minus k degrees of freedom equals F with k minus 1 comma n minus k degrees of freedom distributed under H-zero (q equals k minus 1 because intercept is unrestricted)
- Example: House price regression with k equals 7 gives F with 6 comma 22 degrees of freedom equals 6.83, with p equals 0.0003 which is less than 0.05, so reject H-zero
- Conclusion: Regressors are jointly statistically significant (model has explanatory power)
- Joint significance does NOT imply each regressor is individually significant (in example only Size was individually significant)
- Passing the overall F test is minimum requirement for a useful regression model

**Tests of Subsets of Regressors:**
- Test whether a subset of regressors is jointly statistically significant
- Unrestricted model includes all k regressors: y equals beta-one plus beta-two times x-two, plus dot-dot-dot, plus beta-k times x-k, plus epsilon
- Restricted model includes only first g regressors: y equals beta-one plus beta-two times x-two, plus dot-dot-dot, plus beta-g times x-g, plus epsilon
- Null hypothesis: H-zero: beta-g-plus-1 equals zero through beta-k equals zero (last k minus g regressors have zero coefficients)
- Alternative: H-a: At least one of beta-g-plus-1 through beta-k does not equal zero
- Number of restrictions q equals k minus g (number of coefficients set to zero)
- F-statistic has F with k minus g comma n minus k degrees of freedom distribution under H-zero
- Example: Testing whether bedrooms, bathrooms, lotsize, age, monthsold are jointly significant beyond size
- Result: F equals 0.417, with p equals 0.832 which is greater than 0.05, so do not reject H-zero (these five regressors are jointly insignificant)
- Conclusion: Best model includes only Size as regressor (simplest adequate model)

**F Statistic under Assumptions 1-4 (Section 11.6):**
- Under assumptions 1-4 (homoskedastic errors), the F-statistic has a simple form based on residual sums of squares
- General formula: F equals the quantity RSS-sub-r minus RSS-sub-u, divided by q, all divided by the quantity RSS-sub-u divided by n minus k, which is distributed as F with q comma n minus k degrees of freedom
- RSS-sub-r equals residual sum of squares in restricted model equals the sum of the quantity y-sub-i minus predicted y-sub-i-comma-r, all squared
- RSS-sub-u equals residual sum of squares in unrestricted model equals the sum of the quantity y-sub-i minus predicted y-sub-i-comma-u, all squared
- Intuition: Reject restrictions if RSS-sub-r minus RSS-sub-u is large (restricted model fits much worse)
- Reject H-zero when F is large because then restricted model has significantly poorer fit
- This formula also applies after regression with robust standard errors
- The RSS-based formula provides insight into what drives F-statistic values

**Test of Overall Significance under Assumptions 1-4:**
- For test H-zero: beta-two equals zero through beta-k equals zero, the restricted model is intercept-only with predicted y-sub-i equals y-bar
- Therefore RSS-sub-r equals the sum of the quantity y-sub-i minus y-bar, all squared, which equals TSS (total sum of squares)
- Algebra shows F equals the quantity R-squared divided by k minus 1, all divided by the quantity 1 minus R-squared, divided by n minus k, which is distributed as F with k minus 1 comma n minus k degrees of freedom
- This expresses F-statistic in terms of R-squared from the unrestricted regression
- Example: House price with R-squared equals 0.6506, n equals 29, k equals 7 gives F equals the quantity 0.6506 divided by 6, all divided by the quantity 0.3494 divided by 22, which equals 6.827
- P-value: p equals Ftail of 6 comma 22 comma 6.827, equals 0.000342 which is less than 0.05, so reject H-zero
- This convenient formula allows computing F directly from R-squared without calculating RSS values

**Test of Subsets under Assumptions 1-4:**
- For testing subset H-zero: beta-g-plus-1 equals zero through beta-k equals zero, use F equals the quantity RSS-sub-r minus RSS-sub-u, divided by q, all divided by the quantity RSS-sub-u divided by n minus k
- Example: Test whether five regressors beyond Size are jointly significant
- Full model (unrestricted): RSS-sub-u equals 13,679,397,855 with k equals 7
- Restricted model (Size only): RSS-sub-r equals 14,975,101,655 with g equals 2
- F equals the quantity 14,975,101,655 minus 13,679,397,855, divided by 5, all divided by the quantity 13,679,397,855 divided by 22, which equals 0.417
- P-value: p equals Ftail of 5 comma 22 comma 0.417, equals 0.832 which is greater than 0.05, so do not reject H-zero
- Conclusion: The additional five regressors are not jointly statistically significant at 5 percent

**Relationship to R-squared and Adjusted R-squared:**
- Under assumptions 1-4: As regressors are added, adjusted R-squared increases if and only if F is greater than 1
- For a single regressor: Adjusted R-squared increases if and only if the absolute value of t is greater than 1
- So including a regressor based on increasing adjusted R-squared is a much lower threshold than testing at 5 percent level
- The 5 percent significance test typically requires the absolute value of t greater than 2 (approximately), which is more demanding than the absolute value of t greater than 1
- This explains why researchers often include regressors that are not statistically significant but increase adjusted R-squared
- For single restriction: F equals t-squared, so the critical value for F equals that for t squared (e.g., F-sub-1-comma-infinity-semicolon-0.05 equals 1.96-squared equals 3.84)

**Relationship to Chi-Squared Distribution:**
- Some statistical packages report chi-squared tests instead of F tests
- In large samples as n approaches infinity: q times F with q comma infinity degrees of freedom is distributed as chi-squared with q degrees of freedom
- To convert chi-squared statistic to F-statistic: divide by q (i.e., F equals chi-squared divided by q)
- The F and chi-squared tests are asymptotically equivalent but F is preferred for finite samples
- Separate tests of many hypotheses can lead to inflated Type I error (multiple testing problem)
- Adjusting for multiple testing is beyond the scope but important in practice

**Presentation of Regression Results (Section 11.7):**
- Space-efficient presentation reports only two of: coefficient, standard error, t-statistic, p-value, confidence interval
- **Format 1:** Coefficients with standard errors in parentheses (most common in economics)
- **Format 2:** Coefficients with t-statistics in parentheses (tests H-zero: beta-sub-j equals zero)
- **Format 3:** Coefficients with p-values in parentheses (directly shows significance levels)
- **Format 4:** Coefficients with 95 percent confidence intervals (shows precision and significance)
- **Format 5:** Coefficients with asterisks (one asterisk equals 10 percent, two asterisks equals 5 percent, three asterisks equals 1 percent significance)
- Always report n, R-squared, F-statistic, and other model diagnostics regardless of format chosen
- Example table shows all five formats produce same coefficients but different auxiliary information
- Choose format based on audience and journal conventions

**Software Implementation and Commands:**
- Regression output provides: coefficients, standard errors, t-statistics, p-values, confidence intervals, R-squared, adjusted R-squared, F-statistic
- Modern practice: Use heteroskedasticity-robust standard errors by default (extends to multiple regression from [Chapter 7](s07%20Statistical%20Inference%20for%20Bivariate%20Regression.md))
- Most software packages (R, Python) provide similar functionality with slightly different syntax
- For further topics like multicollinearity, interaction terms, and model specification tests, see [Chapter 12](s12%20Further%20Topics%20in%20Multiple%20Regression.md)

---
