# Chapter 7: Statistical Inference for Bivariate Regression

## Learning Objectives

By the end of this chapter, you will be able to:

- Understand how the t-statistic for regression coefficients follows a T with n minus 2 degrees of freedom distribution under standard assumptions
- Calculate and interpret standard errors for the OLS slope coefficient se of b-two
- Construct confidence intervals for the population slope parameter beta-two using the formula b-two plus or minus t-sub-n-minus-2-comma-alpha-over-2, times se of b-two
- Conduct tests of statistical significance to determine whether a regressor has any relationship with the dependent variable
- Perform two-sided hypothesis tests on beta-two using both p-value and critical value approaches
- Execute one-sided directional hypothesis tests when testing specific claims about parameter values
- Distinguish between statistical significance (based on t-statistics) and economic significance (based on coefficient magnitudes)
- Understand the four key OLS assumptions and their role in statistical inference
- Calculate and interpret heteroskedasticity-robust standard errors when assumption 3 (homoskedasticity) is violated
- Apply the relationship between confidence intervals and hypothesis tests to evaluate null hypotheses

---

## 7.1 Example: House Price and Size

- Key regression output for statistical inference with n equals 29:

Looking at the regression table, the Size variable has: Coefficient equals 73.77, Standard Error equals 11.17, t statistic equals 6.60, p value equals 0.000, and 95 percent confidence interval from 50.84 to 96.70. The Intercept has: Coefficient equals 115,017.30, Standard Error equals 21,489.36, t statistic equals 5.35, p value equals 0.000, and 95 percent confidence interval from 70,924.76 to 159,109.8.

- Predicted price equals b-one plus b-two times size is an estimate of price equals beta-one plus beta-two times size.
- Coefficient of Size
- b-two equals 73.77 is least squares estimate of slope beta-two
- Standard error of Size
- the estimated standard deviation of b-two
- the default standard error of b-two equals 11.17.
- (later: alternative heteroskedastic-robust standard errors).


### Example (continued)

- We have with n equals 29:

Looking at the regression table: Size has Coefficient 73.77, Standard Error 11.17, t statistic 6.60, p value 0.000, and 95 percent confidence interval from 50.84 to 96.70. Intercept has Coefficient 115,017.30, Standard Error 21,489.36, t statistic 5.35, p value 0.000, and 95 percent confidence interval from 70,924.76 to 159,109.8.

- Confidence interval for size
- 95 percent confidence interval for beta-two
- is b-two plus or minus t-sub-27-comma-0.025, times se of b-two, which equals the interval 50.84 to 96.70.
- t statistic of Size tests whether there is any relationship
- is for test of H-zero: beta-two equals zero against H-a: beta-two does not equal zero
- in general t equals the quantity estimate minus hypothesized value, divided by standard error
- t-two equals b-two divided by se of b-two equals 73.77 divided by 11.17 equals 6.60.
- p value of Size
- is p-value for a two sided test
- p-two equals the probability that the absolute value of T-sub-27 is greater than the absolute value of 6.60, which equals 0.00.

> **Key Concept**: Regression output provides all information needed for statistical inference. The coefficient b-two equals 73.77 estimates the population slope beta-two. The standard error se of b-two equals 11.17 measures precision. The t-statistic equals 6.60 tests whether size affects price. The p-value 0.000 provides strong evidence that beta-two differs from zero. The 95 percent confidence interval from 50.84 to 96.70 gives a range of plausible values for beta-two.

## 7.2 The t Statistic

- The statistical inference problem
- Sample: y-hat equals b-one plus b-two times x where b-one and b-two are least squares estimates
- Population: the expected value of y given x equals beta-one plus beta-two times x, and y equals beta-one plus beta-two times x, plus u.
- Estimators: b-one and b-two are estimators of beta-one and beta-two.
- Goal
- inference on the slope parameter beta-two.
- This is based on a T with n minus 2 degrees of freedom distributed statistic

T equals the quantity estimate minus parameter, divided by standard error, which equals the quantity b-two minus beta-two, divided by se of b-two, which is distributed as T with n minus 2 degrees of freedom.

> **Key Concept**: Statistical inference for the slope parameter beta-two is based on the t-statistic T equals the quantity b-two minus beta-two, divided by se of b-two. Under standard assumptions, this statistic follows a t distribution with n minus 2 degrees of freedom. This distribution forms the basis for confidence intervals and hypothesis tests about beta-two.

### Why use the T with n minus 2 degrees of freedom Distribution?

- Make assumptions 1-4 given in the next slide.
- then the variance of b-two equals sigma-u-squared divided by the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared.
- But we don't know sigma-u-squared
- we replace it with the estimate s-e-squared equals 1 over n minus 2, times the sum from i equals 1 to n of the quantity y-sub-i minus y-hat-sub-i, all squared.
- This leads to noise in the standard error of b-two squared equals s-e-squared divided by the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared
- so the statistic T equals the quantity b-two minus beta-two, divided by se of b-two, is better approximated by T with n minus 2 degrees of freedom than by normal with mean 0 and variance 1.
- The T with n minus 2 degrees of freedom distribution
- is the exact distribution if additionally the errors u-sub-i are normally distributed
- otherwise it is an approximation, one that computer packages use.

> **Key Concept**: We use the t distribution with n minus 2 degrees of freedom instead of the standard normal distribution because we estimate the unknown error variance sigma-u-squared with s-e-squared. This estimation introduces additional uncertainty. The t distribution accounts for this by having fatter tails than the normal distribution. If errors are normally distributed, T with n minus 2 degrees of freedom is the exact distribution; otherwise it's an approximation that works well in practice.

### Model Assumptions

- Data assumption is that there is variation in the sample regressors so that the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared, does not equal zero.
- Population assumptions 1-4
- 1. The population model is y equals beta-one plus beta-two times x, plus u.
- 2. The error has mean zero conditional on x: the expected value of u-sub-i given x-sub-i equals zero.
- 3. The error has constant variance conditional on x: the variance of u-sub-i given x-sub-i equals sigma-u-squared.
- 4. The errors for different observations are statistically independent: u-sub-i is independent of u-sub-j.
- Assumptions 1-2 imply a linear conditional mean and yield unbiased estimators

The expected value of y given x equals beta-one plus beta-two times x.

- Additional assumptions 3-4 yield the variance of estimators.

> **Key Concept**: Four standard OLS assumptions underlie statistical inference: (1) correct linear model, (2) mean-zero errors, (3) constant error variance (homoskedasticity), and (4) independent errors. Assumptions 1-2 are crucial for unbiasedness, ensuring the expected value of y given x equals beta-one plus beta-two times x. Assumptions 3-4 determine variance formulas for the estimators. The data assumption requires variation in x to compute regression coefficients.

## 7.3 Confidence Interval for the Slope Parameter

- Recall: A 95 percent confidence interval is approximately

estimate plus or minus 2 times standard error

- here a 95 percent confidence interval is b-two plus or minus t-sub-n-minus-2-semicolon-0.025, times se of b-two.
- A 100 times the quantity 1 minus alpha percent confidence interval for beta-two is

b-two plus or minus t-sub-n-minus-2-comma-alpha-over-2, times se of b-two,

where

- b-two is the slope estimate
- se of b-two is the standard error of b-two
- t-sub-n-minus-2-semicolon-alpha-over-2 is the critical value from the T with n minus 2 degrees of freedom distribution.

> **Key Concept**: A 100 times the quantity 1 minus alpha percent confidence interval for the slope parameter beta-two is constructed as b-two plus or minus t-sub-n-minus-2-comma-alpha-over-2, times se of b-two. For a 95 percent confidence interval, alpha equals 0.05, so we use the critical value from the t distribution leaving 0.025 probability in each tail. The approximate rule "estimate plus or minus 2 times standard error" works well because t-sub-n-minus-2-comma-0.025 is close to 2 for moderate sample sizes.

### What Level of Confidence?

- There is no best choice of confidence level
- most common choice is 95 percent (or 90 percent or 99 percent)
- Interpretation
- the calculated 95 percent confidence interval for beta-two will correctly include beta-two 95 percent of the time
- if we had many samples and in each sample formed a 95 percent confidence interval, then 95 percent of these confidence intervals will include the true unknown beta-two.

> **Key Concept**: The interpretation of a 95 percent confidence interval is that if we constructed such intervals from many repeated samples, 95 percent would contain the true parameter beta-two. We have only one sample, so we can't know if our particular interval contains beta-two, but we're "95 percent confident" that it does. There's no single best confidence level, though 95 percent is conventional. Higher confidence levels produce wider intervals.

### Example: House Price and Size

- For regress house price on house size a 95 percent confidence interval is

Starting with b-two plus or minus t-sub-n-minus-2-comma-alpha-over-2, times se of b-two, this equals 73.77 plus or minus t-sub-27-comma-0.025, times 11.17. This equals 73.77 plus or minus 2.052 times 11.17. This equals 73.77 plus or minus 22.93. This gives the interval 50.84 to 96.70.

- This is directly given in computer output from regression.

> **Key Concept**: For the house price example with n equals 29, the 95 percent confidence interval is calculated as 73.77 plus or minus 2.052 times 11.17, yielding the interval 50.84 to 96.70. The critical value t-sub-27-comma-0.025 equals 2.052 from the t distribution with 27 degrees of freedom. We're 95 percent confident that each additional square foot adds between 50.84 and 96.70 dollars to house price. Modern statistical software reports this confidence interval automatically.

## 7.4 Tests of Statistical Significance

- A regressor x has no relationship with y if beta-two equals zero.
- A test of "statistical significance" is a two-sided test of whether beta-two equals zero. So test

H-zero: beta-two equals zero against H-a: beta-two does not equal zero.

- Test statistic is then

t equals b-two divided by se of b-two, which is distributed as T with n minus 2 degrees of freedom

- Reject if the absolute value of t is large as then the absolute value of b-two is large
- How large?
- Large enough that the value of the absolute value of t is a low probability event.
- Use either p value approach or critical value approach
- reject at level 0.05 if p equals the probability that the absolute value of T-sub-n-minus-2 is greater than the absolute value of t, and this probability is less than 0.05
- or equivalently reject at level 0.05 if the absolute value of t is greater than c equals t-sub-n-minus-2-semicolon-0.025.
- This method generalizes to other formulas for se of b-two.

> **Key Concept**: A test of statistical significance tests whether the regressor x has any linear relationship with y by testing H-zero: beta-two equals zero against H-a: beta-two does not equal zero. The test statistic is t equals b-two divided by se of b-two. We reject the null hypothesis if the absolute value of t is large enough to be a low-probability event under H-zero. Two equivalent approaches exist: the p-value approach (reject if p less than alpha) and the critical value approach (reject if the absolute value of t greater than the critical value).

### Example: House Price and Size

- For regress house price on house size with n equals 29

t equals b-two divided by se of b-two equals 73.77 divided by 11.17 equals 6.60

- p equals the probability that the absolute value of T-sub-n-minus-2 is greater than the absolute value of t, which equals the probability that the absolute value of T-sub-27 is greater than 6.60, which equals 0.000
- so reject H-zero: beta-two equals zero at significance level 0.05 as p is less than 0.05.
- c equals t-sub-n-minus-2-semicolon-0.025 equals t-sub-27-comma-0.025 equals 2.052
- so reject H-zero at significance level 0.05 as the absolute value of t equals 6.60 is greater than c.
- Conclude that house size is statistically significant at level 0.05.

> **Key Concept**: For the house price example, the t-statistic equals 6.60, which is extremely large compared to the critical value of 2.052. The p-value is essentially zero (0.000), far below 0.05. Both approaches lead to rejecting H-zero: beta-two equals zero at the 5 percent significance level. We conclude that house size is statistically significant—it has a genuine relationship with house price, not just random noise.

### Economic Significance versus Statistical Significance

- A regressor is of economic significance if its coefficient is of large enough value for it to matter in practice
- economic significance depends directly on b-two and the context
- By contrast, statistical significance depends directly on t which is the ratio b-two divided by se of b-two.
- With large samples se of b-two approaches zero as n approaches infinity
- so we may find statistical significance
- even if b-two is so small that it is of little economic significance.

> **Key Concept**: Statistical significance and economic significance are distinct concepts. Statistical significance asks whether an effect exists (is beta-two different from zero). Economic significance asks whether the effect is large enough to matter in practice. With large samples, se of b-two approaches zero, so even tiny coefficients become statistically significant despite being economically meaningless. Always assess both: a coefficient can be statistically significant but economically trivial, especially in large samples.

### Tests based on the Correlation Coefficient

- An alternative way to measure statistical significance, used in many social sciences, uses the correlation coefficient, the absolute value of r-sub-x-y.
- Then reject the null hypothesis of no association if the absolute value of r-sub-x-y is sufficiently large
- this gives similar results to tests based on t equals b-two divided by se of b-two if default standard errors are used.
- Weaknesses of tests using the correlation coefficient
- this method cannot relax assumptions 3-4
- this method cannot be used if we wish to add additional regressors
- and it tells little about economic significance.

> **Key Concept**: Testing using the correlation coefficient r-sub-x-y is an alternative approach to measure statistical significance, common in some social sciences. However, it has significant weaknesses compared to t-tests: it cannot accommodate robust standard errors (relaxing assumptions 3-4), cannot extend to multiple regression, and provides no information about economic significance. Regression-based t-tests are more flexible and informative, making them the preferred approach in econometrics.

## 7.5 Two-sided Hypothesis Tests

- A two-sided test on the slope coefficient is a test of

H-zero: beta-two equals beta-two-star against H-a: beta-two does not equal beta-two-star.

- Use t-statistic where beta-two equals beta-two-star. So compute

t equals the quantity b-two minus beta-two-star, divided by se of b-two, which is distributed as T with n minus 2 degrees of freedom.

- Reject if the absolute value of t is large as then the absolute value of the quantity b-two minus beta-two-star is large
- How large?
  - Large enough that such a large absolute value of t is a low probability event
- Use either p value approach or critical value approach.

> **Key Concept**: A general two-sided hypothesis test evaluates H-zero: beta-two equals beta-two-star against H-a: beta-two does not equal beta-two-star, where beta-two-star is any hypothesized value. The test statistic is t equals the quantity b-two minus beta-two-star, divided by se of b-two. We reject if the absolute value of t is large, meaning b-two is far from the hypothesized value beta-two-star. The two-tailed nature reflects that the alternative includes both beta-two greater than beta-two-star and beta-two less than beta-two-star.

### Example: House Price and Size

- For house price example with beta-two-star equals 90

t equals the quantity b-two minus 90, divided by se of b-two, equals the quantity 73.77 minus 90, divided by 11.17, equals negative 1.452.

- p-value approach
- p equals the probability that the absolute value of T-sub-27 is greater than the absolute value of negative 1.452, which equals 0.158.
- do not reject H-zero at level 0.05 as p equals 0.158 is greater than 0.05.
- Critical value approach at level 0.05:
- c equals t-sub-27-semicolon-0.025 equals 2.052.
- do not reject H-zero at level 0.05 as the absolute value of t equals 1.452 is less than c equals 2.052.
- In either case we do not reject H-zero: beta-two equals 90 against H-a: beta-two does not equal 90 at level 0.05.
- conclude that house price does not increase by 90 dollars per square foot.
- p-value approach: Compute p equals the probability that the absolute value of T-sub-n-minus-2 is greater than the absolute value of t.
- critical value approach: compute c so that reject if the absolute value of t is greater than c.
![](https://cdn.mathpix.com/cropped/07ae1b4d-3d81-4f56-a70c-1c6790682a1f-18.jpg?height=423&width=573&top_left_y=323&top_left_x=61)

Two-sided test: critical value approach
![](https://cdn.mathpix.com/cropped/07ae1b4d-3d81-4f56-a70c-1c6790682a1f-18.jpg?height=391&width=580&top_left_y=357&top_left_x=647)

> **Key Concept**: Testing whether beta-two equals 90 in the house price example yields t equals negative 1.452 with p-value 0.158. Since p equals 0.158 is greater than 0.05, and the absolute value of t equals 1.452 is less than the critical value 2.052, we do not reject H-zero at the 5 percent level. The data don't provide strong evidence that the true price increase differs from 90 dollars per square foot, even though our point estimate is 73.77 dollars.

### Rejection using p-values

- p-value approach (at level alpha equals 0.05)
- Assume that beta-two equals beta-two-star, i.e. H-zero is true.
- Obtain the p-value
  - The probability (or significance level) of observing an absolute value of T-sub-n-minus-2 greater than or equal to the absolute value of t, where this probability is calculated under the assumption that beta-two equals beta-two-star
- If p is less than 0.05 then reject H-zero
  - Reason: there was less than 0.05 chance of observing our t, given beta-two equals beta-two-star

> **Key Concept**: The p-value approach calculates the probability of observing a test statistic as extreme as or more extreme than what we actually observed, assuming the null hypothesis is true. If this probability (the p-value) is less than our significance level alpha, we reject the null hypothesis. The logic is that if beta-two equals beta-two-star were true, observing such an extreme t-statistic would be unlikely (less than alpha probability), so we conclude beta-two does not equal beta-two-star.

### Rejection using Critical values

- Critical value approach (at level alpha equals 0.05)
- Assume that beta-two equals beta-two-star, i.e. H-zero is true.
- Find the critical value
  - The value c such that the probability that the absolute value of T-sub-n-minus-2 is greater than or equal to c, equals 0.05
- If the absolute value of t is greater than c then reject H-zero
  - Reason: there was less than 0.05 chance of observing our t, given beta-two equals beta-two-star

> **Key Concept**: The critical value approach finds the threshold c such that the probability of the absolute value of T-sub-n-minus-2 exceeding c is alpha when the null hypothesis is true. If our observed absolute value of t exceeds this critical value, we reject the null hypothesis. Both the p-value and critical value approaches are equivalent: they always lead to the same decision about whether to reject the null hypothesis.

### Relationship of Tests to Confidence Interval

- For a two-sided test of H-zero: beta-two equals beta-two-star
- if the null hypothesis value beta-two-star falls inside the 100 times the quantity 1 minus alpha percent confidence interval then do not reject H-zero at significance level alpha.
- otherwise reject H-zero at significance level alpha.
- House example
- 95 percent confidence interval for beta-two is the interval from 50.84 to 96.70
- reject H-zero: beta-two equals zero at level 0.05 as the 95 percent confidence interval does not include zero.

> **Key Concept**: There's an intimate connection between confidence intervals and hypothesis tests. For a two-sided test of H-zero: beta-two equals beta-two-star at significance level alpha, reject the null hypothesis if and only if beta-two-star falls outside the 100 times the quantity 1 minus alpha percent confidence interval. This provides a visual way to test multiple hypotheses: any value inside the confidence interval is a plausible value of beta-two, while values outside are rejected.

## 7.6 One-sided Directional Hypothesis Tests

- One-sided test on the slope coefficient is a test of

Upper one-tailed alternative: H-zero: beta-two less than or equal to beta-two-star against H-a: beta-two greater than beta-two-star
Lower one-tailed alternative: H-zero: beta-two greater than or equal to beta-two-star against H-a: beta-two less than beta-two-star

- The statement being tested is specified to be the alternative hypothesis.
- Use same t-statistic as in two-sided case. So

t equals the quantity b-two minus beta-two-star, divided by se of b-two, which is distributed as T with n minus 2 degrees of freedom.

- What will differ is the rejection region
- For H-zero: beta-two less than or equal to beta-two-star against H-a: beta-two greater than beta-two-star, reject in the right tail

p equals the probability that T-sub-n-minus-2 is greater than t

- For H-zero: beta-two greater than or equal to beta-two-star against H-a: beta-two less than beta-two-star, reject in the left tail

p equals the probability that T-sub-n-minus-2 is less than t.

> **Key Concept**: One-sided tests evaluate directional claims. For an upper one-tailed test (claim that beta-two is greater than beta-two-star), we test H-zero: beta-two less than or equal to beta-two-star against H-a: beta-two greater than beta-two-star, rejecting in the right tail. For a lower one-tailed test (claim that beta-two is less than beta-two-star), we test H-zero: beta-two greater than or equal to beta-two-star against H-a: beta-two less than beta-two-star, rejecting in the left tail. The claim being tested is always specified as the alternative hypothesis, requiring strong evidence to support it.

### Example: House Price and Size

- House price example suppose claim is that house price rises by less than 90 dollars per square foot, i.e. beta-two is less than 90.
- Test H-zero: beta-two greater than or equal to 90 against H-a: beta-two less than 90 (lower tailed alternative).

t equals the quantity b-two minus 90, divided by se of b-two, equals the quantity 73.77 minus 90, divided by 11.17, equals negative 1.452

- p-value approach:
- p equals the probability that T-sub-27 is less than t, which equals the probability that T-sub-27 is less than negative 1.452, which equals the probability that T-sub-27 is greater than 1.452 (using symmetry of the t distribution), which equals ttail of 27 comma 1.452, which equals 0.079, which is less than 0.05.
- where we have used the symmetry of the t distribution.
- Critical value approach at level 0.05:
- c equals negative t-sub-27-comma-0.05 equals negative invttail of 27 comma 0.05, equals negative 1.70, and t is not less than negative 1.70.
- In either case we do not reject H-zero: beta-two greater than or equal to 90 at significance level 0.05.
- At level 0.05 there is not enough evidence to support the claim
- note that the claim would be supported if we tested at level 0.10.

> **Key Concept**: Testing the claim that beta-two is less than 90 (lower-tailed test) yields t equals negative 1.452 with one-sided p-value 0.079. At the 5 percent level, we do not reject H-zero: beta-two greater than or equal to 90, so there's insufficient evidence to support the claim that price increases by less than 90 dollars per square foot. However, at the 10 percent level (p equals 0.079 less than 0.10), we would reject and support the claim. This illustrates how the significance level affects our conclusion.

### Computer generated t-statistic

- Computer gives a t-statistic
- this is t equals b-two divided by se of b-two
- suitable for testing beta-two equals zero.
- Computer gives a p-value
- this is for a two-sided test of H-zero: beta-two equals zero against H-a: beta-two does not equal zero.
- For a one-sided test of statistical significance
- if b-two is of the expected sign then halve the printed p-value.
- if b-two is not of the expected sign then reject since p is greater than 0.5
- Example: if expect beta-two greater than zero then upper tailed alternative test
- test H-zero: beta-two less than or equal to zero against H-a: beta-two greater than zero at level 0.05
- if b-two is greater than zero then halve the printed p value and reject H-zero if this is less than 0.05
- if b-two is less than zero we will not reject H-zero, i.e. conclude beta-two is not greater than zero.

> **Key Concept**: Computer output reports t equals b-two divided by se of b-two and the p-value for a two-sided test of beta-two equals zero. For one-sided tests of statistical significance, use this shortcut: if the coefficient has the expected sign, halve the printed two-sided p-value to get the one-sided p-value. If the coefficient has the wrong sign, do not reject (the one-sided p-value exceeds 0.5). This shortcut only works for tests of beta-two equals zero, not for other null hypotheses.

## 7.7 Robust Standard Errors

- Default standard errors (and associated t statistics, p values and confidence intervals) make assumptions 1-4
- called default because this is what computer automatically computes
- Robust standard errors
- Keep assumptions 1-2
- Relax assumptions 3-4 in three common ways depending on data type
- Are commonly-used in practice.
- In each case get an alternative formula for se of b-two, say se-sub-rob of b-two
- Then base inference on

t equals the quantity b-two minus beta-two, divided by se-sub-rob of b-two

> **Key Concept**: Default standard errors assume all four OLS assumptions hold. Robust standard errors keep the crucial assumptions 1-2 (correct model and mean-zero errors) but relax assumptions 3-4 (homoskedasticity and independence). Modern econometric practice commonly uses robust standard errors, with three main types depending on data structure. Using robust standard errors produces an alternative formula se-sub-rob of b-two, and inference proceeds using t equals the quantity b-two minus beta-two, divided by se-sub-rob of b-two.

### Heteroskedastic Robust Standard Errors

- Relax assumption 3 that all errors have the same variance
- called the assumption of homoskedastic errors.
- Instead allow the variance of u-sub-i given x-sub-i equals sigma-sub-i-squared, which varies with i
- called heteroskedastic errors.
- This is the standard assumption in modern econometrics.
- Then the heteroskedasticity-robust standard error for b-two is

se-sub-het of b-two equals the square root of the sum from i equals 1 to n of e-sub-i-squared times the quantity x-sub-i minus x-bar, all squared, divided by the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared. This does not equal s-e divided by the square root of the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared.

- Then t equals the quantity b-two minus beta-two, divided by se-sub-het of b-two, is viewed as T with n minus 2 degrees of freedom distributed.

> **Key Concept**: Heteroskedasticity means error variance varies across observations: the variance of u-sub-i given x-sub-i equals sigma-sub-i-squared instead of constant sigma-u-squared. Heteroskedasticity-robust standard errors account for this by weighting residuals differently. The robust formula se-sub-het of b-two differs from the default se of b-two by using individual squared residuals e-sub-i-squared times squared deviations rather than pooling them. Modern econometrics treats heteroskedasticity as the default assumption, making robust standard errors standard practice.

### Example: House Price and Size

- For the house price and size example
- Default standard errors
  - 11.17 and 21,489 for the slope and intercept
- Heteroskedastic-robust standard errors
  - 11.33 and 20,928 for the slope and intercept

- Confidence interval using heteroskedastic-robust standard errors
- 73.77 plus or minus t-sub-27-comma-0.025, times 11.333, equals the interval from 50.33 to 97.02, compared to the interval from 50.84 to 96.70
- Test H-zero: beta-two equals zero against H-a: beta-two does not equal zero

t equals b-two divided by se of b-two equals the quantity 73.77 minus zero, divided by 11.33, equals 6.51, compared to 6.60

> **Key Concept**: In the house price example, heteroskedastic-robust standard errors (11.33 for slope, 20,928 for intercept) are similar to default standard errors (11.17 for slope, 21,489 for intercept). The 95 percent confidence interval using robust standard errors is 50.33 to 97.02, slightly wider than the default interval 50.84 to 96.70. The t-statistic using robust standard errors is 6.51 compared to default 6.60. In this case, both approaches lead to the same conclusions, but robust standard errors provide valid inference even if heteroskedasticity is present.

### Simulation Example of Heteroskedastic Errors

- Generate 100 observations as follows
- size varies from 1700 to 3700 plus some random noise
- price equals 11,500 plus 74 times size, plus zero-mean error
- (1) error is homoskedastic: u-sub-i is distributed normal with mean zero and variance 23,500-squared
- (2) error is heteroskedastic: u-sub-i is distributed as the quantity size-sub-i minus 1700, divided by 1400, times normal with mean zero and variance 23,500-squared
  - This error has variance equal to the quantity size-sub-i minus 1700, divided by 1400, all squared, times 23,500-squared, that differs across i

> **Key Concept**: This simulation illustrates heteroskedasticity visually. In the homoskedastic case, errors have constant variance 23,500-squared for all observations. In the heteroskedastic case, error variance increases with house size: larger houses have more variable prices. The formula for heteroskedastic errors scales the variance by the quantity size-sub-i minus 1700, divided by 1400, all squared, making variance proportional to size. This pattern is common in economic data where larger values exhibit greater variability.

### Simulation Example (continued)

- First panel: homoskedastic errors are evenly distributed around the regression line.
- Second panel: heteroskedastic errors scattering around the regression line varies with the level of the regressor
- in this case increasing with regressor size.

Homoskedastic errors
![](https://cdn.mathpix.com/cropped/07ae1b4d-3d81-4f56-a70c-1c6790682a1f-29.jpg?height=381&width=517&top_left_y=461&top_left_x=103)

Heteroskedastic errors
![](https://cdn.mathpix.com/cropped/07ae1b4d-3d81-4f56-a70c-1c6790682a1f-29.jpg?height=375&width=513&top_left_y=463&top_left_x=670)

> **Key Concept**: The visual comparison shows how heteroskedasticity manifests in data. With homoskedastic errors (first panel), observations scatter uniformly around the regression line—the vertical spread is roughly constant across all x values. With heteroskedastic errors (second panel), the scatter increases as size increases—observations with larger x values show greater vertical spread. This "funnel shape" is a telltale sign of heteroskedasticity in scatter plots and justifies using heteroskedasticity-robust standard errors.

### Other Robust Standard Errors

- For time series data where model errors may be correlated over time
- use HAC robust.
- For data in clusters (or groups) where errors are correlated within cluster but are uncorrelated across clusters
- people in villages, students in schools, individuals in families,...
- panel data on many individuals over time
- use cluster robust.
- These robust standard errors are presented in chapter 12.1.
- An essential part of any regression analysis is knowing which particular robust standard error method should be used.

> **Key Concept**: Beyond heteroskedasticity-robust standard errors, two other robust methods address different data structures. HAC robust (Heteroskedasticity and Autocorrelation Consistent) standard errors handle time series data where errors are correlated across time periods. Cluster-robust standard errors handle grouped data where errors are correlated within clusters (like students in schools or individuals in families) but uncorrelated across clusters. Choosing the appropriate robust standard error method is essential for valid inference and depends on your data structure and likely violations of standard assumptions.

---

## Key Takeaways

**Example and Regression Output (Section 7.1):**
- Regression output provides key information for statistical inference: coefficients, standard errors, t-statistics, p-values, and confidence intervals
- House price example: regressing price on size with n equals 29 gives b-two equals 73.77, se of b-two equals 11.17
- The coefficient b-two equals 73.77 estimates the population slope beta-two (price increase per square foot)
- Standard error se of b-two equals 11.17 is the estimated standard deviation of b-two, measuring its precision
- The 95 percent confidence interval from 50.84 to 96.70 provides a range of plausible values for beta-two
- The t-statistic t equals 6.60 tests whether size has any relationship with price
- The p-value 0.000 indicates strong evidence against the null hypothesis H-zero: beta-two equals zero
- Larger standard errors indicate less precision; smaller standard errors indicate more precision

**The t-Statistic and Its Distribution (Section 7.2):**
- Statistical inference uses the t-statistic: T equals the quantity b-two minus beta-two, divided by se of b-two, which follows a T with n minus 2 degrees of freedom distribution
- The sample regression y-hat equals b-one plus b-two times x estimates the population relationship the expected value of y given x equals beta-one plus beta-two times x
- Under assumptions 1-4, the t-statistic follows the T with n minus 2 degrees of freedom distribution (n minus 2 degrees of freedom for bivariate regression)
- We use T with n minus 2 degrees of freedom instead of normal with mean 0 and variance 1 because we estimate the error variance sigma-u-squared with s-e-squared
- Replacing unknown sigma-u-squared with estimate s-e-squared introduces additional variability captured by the t distribution
- The T with n minus 2 degrees of freedom distribution has fatter tails than normal with mean 0 and variance 1, accounting for estimation uncertainty
- T with n minus 2 degrees of freedom is the exact distribution if errors are normally distributed; otherwise it's an approximation
- As sample size increases, T with n minus 2 degrees of freedom converges to normal with mean 0 and variance 1

**Four Key OLS Assumptions (Section 7.2):**
- Assumption 1 (Correct model): The population model is y equals beta-one plus beta-two times x, plus u
- Assumption 2 (Mean-zero error): the expected value of u-sub-i given x-sub-i equals zero for all i (errors uncorrelated with regressor)
- Assumption 3 (Homoskedasticity): the variance of u-sub-i given x-sub-i equals sigma-u-squared for all i (constant error variance)
- Assumption 4 (Independence): u-sub-i is independent of u-sub-j for all i not equal to j (no autocorrelation)
- Assumptions 1-2 are crucial: they imply the expected value of y given x equals beta-one plus beta-two times x and yield unbiased estimators
- Assumptions 3-4 affect variance calculations and standard errors but not bias
- Data assumption: there must be variation in regressors, the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared, must be greater than zero
- These assumptions can be relaxed using robust standard errors (Section 7.7)

**Confidence Intervals for beta-two (Section 7.3):**
- A 100 times the quantity 1 minus alpha percent confidence interval for beta-two is: b-two plus or minus t-sub-n-minus-2-comma-alpha-over-2, times se of b-two
- Approximate 95 percent confidence interval: b-two plus or minus 2 times se of b-two (since t-sub-n-minus-2-comma-0.025 is approximately 2 for moderate to large n)
- The critical value t-sub-n-minus-2-comma-alpha-over-2 satisfies the probability that the absolute value of T-sub-n-minus-2 is less than or equal to t-sub-n-minus-2-comma-alpha-over-2, equals 1 minus alpha
- Common confidence levels: 90 percent (alpha equals 0.10), 95 percent (alpha equals 0.05), 99 percent (alpha equals 0.01)
- Interpretation: if we constructed 95 percent confidence intervals for infinite samples, 95 percent would contain the true beta-two
- We have only one sample, so we're "95 percent confident" our particular interval contains beta-two
- House price example: 95 percent confidence interval equals 73.77 plus or minus 2.052 times 11.17, which equals the interval from 50.84 to 96.70
- Wider intervals provide more confidence; narrow intervals provide more precision
- There's no single "best" confidence level, though 95 percent is conventional

**Tests of Statistical Significance (Section 7.4):**
- A test of statistical significance tests H-zero: beta-two equals zero against H-a: beta-two does not equal zero (two-sided)
- If beta-two equals zero, then x has no linear relationship with y
- Test statistic: t equals b-two divided by se of b-two, which is distributed as T with n minus 2 degrees of freedom under H-zero
- Reject H-zero if the absolute value of t is large (evidence that b-two is far from zero)
- P-value approach: reject at level alpha if p equals the probability that the absolute value of T-sub-n-minus-2 is greater than the absolute value of t, and this is less than alpha
- Critical value approach: reject at level alpha if the absolute value of t is greater than c where c equals t-sub-n-minus-2-comma-alpha-over-2
- Both approaches give identical conclusions
- House price example: t equals 73.77 divided by 11.17 equals 6.60, p equals 0.000 which is less than 0.05, so reject H-zero
- Conclude that house size is statistically significant at the 5 percent level
- Computer output typically reports t-statistics and p-values for H-zero: beta-two equals zero

**Economic versus Statistical Significance (Section 7.4):**
- Statistical significance: whether coefficient differs from zero (based on t-statistic)
- Economic significance: whether coefficient is large enough to matter in practice (based on b-two magnitude and context)
- A coefficient can be statistically significant but economically insignificant (small b-two, large sample)
- With large samples, se of b-two approaches zero as n approaches infinity, so even tiny coefficients become statistically significant
- Always assess both: statistical significance tells us if an effect exists; economic significance tells us if it matters
- Example: b-two equals 0.0001 might be highly significant (p less than 0.001) in large sample but economically meaningless
- Context determines economic significance: one dollar price increase per square foot is meaningful for houses

**Tests Using Correlation Coefficient (Section 7.4):**
- Alternative approach: reject H-zero if correlation coefficient, the absolute value of r-sub-x-y, is sufficiently large
- Gives similar results to t-tests when using default standard errors
- Weaknesses: (1) cannot relax assumptions 3-4, (2) cannot extend to multiple regression, (3) tells little about economic significance
- Regression-based t-tests are more flexible and informative
- Prefer t-tests over correlation-based tests in econometric practice

**Two-Sided Hypothesis Tests (Section 7.5):**
- General two-sided test: H-zero: beta-two equals beta-two-star against H-a: beta-two does not equal beta-two-star
- Test statistic: t equals the quantity b-two minus beta-two-star, divided by se of b-two, which is distributed as T with n minus 2 degrees of freedom under H-zero
- Reject if the absolute value of t is large (b-two is far from hypothesized value beta-two-star)
- P-value: p equals the probability that the absolute value of T-sub-n-minus-2 is greater than the absolute value of t
- Critical value: c equals t-sub-n-minus-2-comma-alpha-over-2
- Reject at level alpha if p is less than alpha or equivalently if the absolute value of t is greater than c
- House price example testing beta-two equals 90: t equals the quantity 73.77 minus 90, divided by 11.17, equals negative 1.452, p equals 0.158 which is greater than 0.05, so do not reject
- Cannot conclude that price increases by 90 dollars per square foot
- Two tails used because alternative includes both beta-two greater than beta-two-star and beta-two less than beta-two-star

**Relationship Between Tests and Confidence Intervals (Section 7.5):**
- For two-sided test of H-zero: beta-two equals beta-two-star at significance level alpha:
- If beta-two-star falls inside the 100 times the quantity 1 minus alpha percent confidence interval, then do not reject H-zero
- If beta-two-star falls outside the 100 times the quantity 1 minus alpha percent confidence interval, then reject H-zero
- This provides a visual way to test hypotheses using confidence intervals
- House price example: 95 percent confidence interval is from 50.84 to 96.70; zero is not in this interval, so reject H-zero: beta-two equals zero
- The value 90 is in the interval, so do not reject H-zero: beta-two equals 90
- This equivalence holds because both are based on the same t distribution

**One-Sided Hypothesis Tests (Section 7.6):**
- Upper one-tailed test: H-zero: beta-two less than or equal to beta-two-star against H-a: beta-two greater than beta-two-star (claim beta-two is greater than beta-two-star)
- Lower one-tailed test: H-zero: beta-two greater than or equal to beta-two-star against H-a: beta-two less than beta-two-star (claim beta-two is less than beta-two-star)
- The claim being tested is specified as the alternative hypothesis (requires strong evidence to support)
- Same t-statistic as two-sided: t equals the quantity b-two minus beta-two-star, divided by se of b-two
- Different rejection regions: only one tail used
- Upper tail: reject if t is greater than c where c equals t-sub-n-minus-2-comma-alpha, and p equals the probability that T-sub-n-minus-2 is greater than t
- Lower tail: reject if t is less than negative c where c equals t-sub-n-minus-2-comma-alpha, and p equals the probability that T-sub-n-minus-2 is less than t
- Note: critical value is t-sub-n-minus-2-comma-alpha not t-sub-n-minus-2-comma-alpha-over-2 (one tail not two)
- House price example testing H-zero: beta-two greater than or equal to 90 versus H-a: beta-two less than 90: t equals negative 1.452, p equals the probability that T-sub-27 is less than negative 1.452, which equals 0.079, which is greater than 0.05, so do not reject
- Not enough evidence to support claim that beta-two is less than 90 at 5 percent level (but would reject at 10 percent level)

**Using Computer Output for One-Sided Tests (Section 7.6):**
- Computer reports t equals b-two divided by se of b-two and p-value for two-sided test of H-zero: beta-two equals zero
- For one-sided test of statistical significance:
- If b-two has expected sign, then halve the printed p-value
- If b-two has unexpected sign, then do not reject (p greater than 0.5)
- Example: expect beta-two greater than zero, computer gives two-sided p equals 0.04
  - If b-two is greater than zero: one-sided p equals 0.04 divided by 2 equals 0.02, which is less than 0.05, so reject H-zero: beta-two less than or equal to zero
  - If b-two is less than zero: do not reject H-zero: beta-two less than or equal to zero (wrong sign)
- This shortcut only works for tests of H-zero: beta-two equals zero

**Robust Standard Errors Overview (Section 7.7):**
- Default standard errors assume all four OLS assumptions 1-4
- Robust standard errors keep assumptions 1-2 but relax assumptions 3-4
- Robust standard errors are commonly used in modern econometric practice
- They provide alternative formula for se of b-two, denoted se-sub-rob of b-two
- Base inference on t equals the quantity b-two minus beta-two, divided by se-sub-rob of b-two, using T with n minus 2 degrees of freedom distribution
- Three main types: heteroskedasticity-robust, HAC robust (time series), cluster-robust (grouped data)
- Choice of robust standard error method depends on data structure and likely violations of assumptions

**Heteroskedasticity-Robust Standard Errors (Section 7.7):**
- Relax assumption 3: allow error variance to vary across observations
- Homoskedastic errors: the variance of u-sub-i given x-sub-i equals sigma-u-squared (constant) - Assumption 3
- Heteroskedastic errors: the variance of u-sub-i given x-sub-i equals sigma-sub-i-squared (varies with i) - relaxed assumption
- Heteroskedasticity is the standard assumption in modern econometrics
- Heteroskedasticity-robust standard error: se-sub-het of b-two equals the square root of the sum of e-sub-i-squared times the quantity x-sub-i minus x-bar, all squared, divided by the sum of the quantity x-sub-i minus x-bar, all squared
- This differs from default standard error: se of b-two equals s-e divided by the square root of the sum of the quantity x-sub-i minus x-bar, all squared
- Robust standard errors account for different error variances across observations
- Inference proceeds using t equals the quantity b-two minus beta-two, divided by se-sub-het of b-two, which is distributed as T with n minus 2 degrees of freedom

**Heteroskedasticity Example (Section 7.7):**
- House price example with default versus robust standard errors:
  - Default standard error: 11.17 for slope, 21,489 for intercept
  - Heteroskedastic-robust standard error: 11.33 for slope, 20,928 for intercept
- 95 percent confidence interval using robust standard errors: 73.77 plus or minus 2.052 times 11.33 equals the interval from 50.33 to 97.02, versus default interval from 50.84 to 96.70
- t-statistic using robust standard errors: t equals 73.77 divided by 11.33 equals 6.51, versus default t equals 6.60
- In this example, robust and default standard errors are similar (both lead to same conclusion)
- Simulation example shows heteroskedastic errors have variance increasing with regressor level
- Homoskedastic errors are evenly distributed around regression line
- Heteroskedastic errors show increasing scatter as x increases

**Other Types of Robust Standard Errors (Section 7.7):**
- HAC robust (Heteroskedasticity and Autocorrelation Consistent): for time series data where errors may be correlated over time
- Cluster-robust: for data in groups where errors are correlated within cluster but uncorrelated across clusters
- Examples of clustered data: people in villages, students in schools, individuals in families, panel data (individuals over time)
- Chapter 12.1 provides details on these robust standard error methods
- Essential to know which robust standard error method is appropriate for your data structure
- Using wrong standard error method leads to incorrect inference (wrong confidence intervals and hypothesis test conclusions)

**Software Implementation:**
- Python or R: Standard regression packages provide options for default and heteroskedasticity-robust standard errors
- Confidence level can be adjusted (e.g., 99 percent instead of default 95 percent)
- Hypothesis tests can be conducted for any null hypothesis value (e.g., H-zero: beta-two equals 90)
- Dataset: AED underscore HOUSE dot DTA contains house price and size data with n equals 29

**General Principles:**
- Always assess both statistical and economic significance
- Confidence intervals provide more information than hypothesis tests alone (show range of plausible values)
- Two-sided tests are standard; one-sided tests should only be used when directionality is theoretically justified
- Modern practice: use robust standard errors by default (especially heteroskedasticity-robust)
- The choice of robust standard error method depends on data structure (cross-section, time series, panel, clustered)
- Statistical significance with small samples requires larger absolute value of t values (fatter tails of t distribution)
- As sample size increases, statistical significance becomes easier to achieve (se of b-two approaches zero)

---

### Some in-class Exercises

(1) We obtain fitted model y-hat equals 3.0 with standard error 1.5 in parentheses below, plus 5.0 with standard error 2.0 in parentheses below, times x. R-squared equals 0.32, s-e equals 4.0, n equals 200. Provide an approximate 95 percent confidence interval for the population slope parameter.
(2) Test the claim that the population slope equals 2 at the 5 percent significance level.
(3) Which of assumptions 1-4 need changing if model errors are heteroskedastic?

