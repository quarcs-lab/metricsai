# Chapter 6: The Least Squares Estimator

## Learning Objectives

By the end of this chapter, you will be able to:

- Distinguish between the population regression line (beta-one plus beta-two times x) and the sample regression line (b-one plus b-two times x)
- Understand the conditional mean E of y given x equals beta-one plus beta-two times x, and the error term u equals y minus E of y given x
- Differentiate between the unobserved error term u and the observed residual e
- Apply the four key OLS assumptions: correct model, mean-zero errors, homoskedasticity, and independence
- Calculate the variance and standard error of OLS slope coefficient b-two
- Explain why b-two is an unbiased estimator of beta-two under assumptions 1-2
- Compute the standard error of the regression se and use it to estimate precision
- Understand when OLS estimates are more precise (good fit, many observations, scattered regressors)
- Apply the Central Limit Theorem to show b-two is approximately normally distributed for large samples
- Recognize that OLS is the Best Linear Unbiased Estimator, or BLUE, under standard assumptions

---

## 6.1 Population Model: Conditional Mean of y given x

- The sample model is a line b-one plus b-two times x.
- So we assume that the population model is also a line, denoted beta-one plus beta-two times x
- where beta is "beta" and we use Greek letters for (unknown) parameters.
- More formally the conditional mean of y is assumed to be linear in x

The expected value of Y given X equals x, equals beta-one plus beta-two times x.

- The population conditional mean of Y given X equals x
- is the probability-weighted average of all possible values of Y for a given value of x; e.g. earnings conditional on years of schooling
- is denoted E of Y given X equals x
- generalizes E of Y in chapter 3 that is the probability-weighted average of all possible values of Y.


### Population Conditional Mean (continued)

- We assume that the conditional mean is linear in x

The expected value of Y given X equals x, equals beta-one plus beta-two times x.

- Commonly-used simpler notation is

The expected value of y given x equals beta-one plus beta-two times x.

- Note: In general the conditional mean need not be linear.
- Case 1: E of Y given X equals 1 equals 5, E of Y given X equals 2 equals 7, E of Y given X equals 3 equals 9
- This is linear since this implies E of Y given X equals x equals 3 plus 2 times x.
- Case 2: E of Y given X equals 1 equals 5, E of Y given X equals 2 equals 7, E of Y given X equals 3 equals 12
- This is nonlinear as the increase by 2 from X equals 1 to X equals 2 but increases by 5 from X equals 2 to X equals 3.
- In Chapter 9 we consider nonlinear conditional means.


### Error Term

- y does not exactly equal beta-one plus beta-two times x
- instead E of y given x equals beta-one plus beta-two times x.
- The difference between y and E of y given x is called the error term u

To define the error term u, we start with u equals y minus the expected value of y given x, which equals y minus the quantity beta-one plus beta-two times x.

- The error term u is not observed as beta-one and beta-two are unknown.


### Error Term versus Residual - a crucial distinction

- u is not observed - it is the difference between y and the unknown population line beta-one plus beta-two times x (the solid line)
- e is observed - it is the difference between y and the known fitted line b-one plus b-two times x (the dashed line)
![](https://cdn.mathpix.com/cropped/1db1a0ef-9c44-414f-9671-ab8a889b52b7-08.jpg?height=449&width=516&top_left_y=397&top_left_x=75)
![](https://cdn.mathpix.com/cropped/1db1a0ef-9c44-414f-9671-ab8a889b52b7-08.jpg?height=445&width=480&top_left_y=399&top_left_x=712)


### Error Term is assumed to have mean zero

- Since u equals y minus the quantity beta-one plus beta-two times x, we have

y equals beta-one plus beta-two times x, plus u

- The error term is assumed to be zero on average for each x value
- sometimes u-sub-i is greater than zero and so y-sub-i is above the population line
- sometimes u-sub-i is less than zero and so y-sub-i is below the population line
- but the long-run average of u-sub-i (at each value of x) is zero.
- More precisely the error term has conditional mean zero

The expected value of u given x equals zero.

- This ensures that the population line is indeed beta-one plus beta-two times x.

To show this: The expected value of y given x equals the expected value of the quantity beta-one plus beta-two times x, plus u, all given x. This equals beta-one plus beta-two times x, plus the expected value of u given x. Which equals beta-one plus beta-two times x, provided that the expected value of u given x equals zero.

> **Key Concept**: The conditional mean E of y given x equals beta-one plus beta-two times x defines the population regression line as how the average value of y varies with x. The error term u equals y minus this conditional mean captures deviations from the population line. The crucial assumption that the expected value of u given x equals zero ensures that errors average to zero at every x value, making the population line correctly centered. This zero conditional mean assumption is fundamental for unbiased estimation.

### Population Conditional Variance of y given x

- The variability of the error term around the line will determine in part the precision of our estimates
- greater variability is greater noise so less precision.
- We initially assume that the error variance is constant and does not vary with x

The variance of u given x equals sigma-u-squared

- This is called the assumption of homoskedastic errors
- "skedastic" based on the Greek word for scattering
- "homos" is the Greek word for same
- this assumption can be relaxed (and is often relaxed - later).
- The error term provides the only variation in y around the population line so then

The variance of y given x equals the variance of u given x, which equals sigma-u-squared

> **Key Concept**: Homoskedasticity means the error variance is constant across all x values: the variance of u given x equals sigma-u-squared for all x. This assumption of constant variance simplifies inference but can be relaxed in practice. When errors are homoskedastic, the variance of y given x also equals sigma-u-squared, since the error term is the only source of randomness in y conditional on x. Greater error variance means noisier data and less precise estimates.

### Summary

- The bottom line:
- Univariate analysis: y-one, dot-dot-dot, y-n is a simple random sample with

Y-sub-i is distributed with mean mu and variance sigma-squared.

- Regression analysis: the pairs x-one, y-one, through x-n, y-n, is a simple random sample that allows the mean to vary with x, so

y-sub-i given x-sub-i is distributed with mean beta-one plus beta-two times x, and variance sigma-u-squared.

> **Key Concept**: Regression generalizes univariate analysis by allowing the mean to depend on x. In univariate analysis, Y-sub-i has constant mean mu and variance sigma-squared. In regression, y-sub-i given x-sub-i has mean that varies with x (beta-one plus beta-two times x) but constant variance sigma-u-squared under homoskedasticity. This framework shows how regression describes the relationship between variables by modeling the conditional mean.

## 6.2 Examples of Sampling from a Population

- We consider two examples of sampling from a population
- regression generalizations of the two examples in chapter 4.
- 1. Generate by computer 400 samples from an explicit model y equals beta-one plus beta-two times x, plus u.
- 2. Select 400 samples from a finite population - the U.S. 1880 Census for males aged 60-69 years.
- In both cases we run 400 regressions giving 400 estimates b-one and b-two and find
- the average of the 400 slopes b-two is close to beta-two
- the distribution of the 400 slopes b-two is approximately normal
- similar results hold for the intercept b-one.


### Single Sample Generated from an Experiment

- Example with n equals 5 is generate data from

y equals beta-one plus beta-two times x, plus u, which equals 1 plus 2 times x, plus u
u is distributed normal with mean zero and variance sigma-u-squared equals 4
x equals 1, 2, 3, 4, 5.

- note: added the assumption that errors are normally distributed
- Then a random normal generator for u yielded

For five observations, we have: Observation 1 has x equals 1, the expected value of y given x equals 1 plus 2 times 1 equals 3, u equals 1.689889, and y equals 1 plus 2 times x plus u equals 4.689889. Observation 2 has x equals 2, expected value 1 plus 2 times 2 equals 5, u equals negative 0.3187171, and y equals 4.681283. Observation 3 has x equals 3, expected value 1 plus 2 times 3 equals 7, u equals negative 2.506667, and y equals 4.493333. Observation 4 has x equals 4, expected value 1 plus 2 times 4 equals 9, u equals negative 1.63328, and y equals 7.366720. Observation 5 has x equals 5, expected value 1 plus 2 times 5 equals 11, u equals negative 2.390764, and y equals 8.609236.

- Five generated observations
- left panel: population regression line y equals beta-one plus beta-two times x equals 1 plus 2 times x
- right panel: sample regression line y-hat equals b-one plus b-two times x equals 2.81 plus 1.05 times x
- note that b-one does not equal beta-one and b-two does not equal beta-two.

Population line
![](https://cdn.mathpix.com/cropped/1db1a0ef-9c44-414f-9671-ab8a889b52b7-14.jpg?height=395&width=537&top_left_y=426&top_left_x=81)

Regression line
![](https://cdn.mathpix.com/cropped/1db1a0ef-9c44-414f-9671-ab8a889b52b7-14.jpg?height=395&width=545&top_left_y=426&top_left_x=643)

> **Key Concept**: A single sample produces estimates b-one and b-two that typically differ from the true population parameters beta-one and beta-two due to sampling variability. In this example, the population line is y equals 1 plus 2 times x (beta-one equals 1, beta-two equals 2), but the sample of 5 observations yields y-hat equals 2.81 plus 1.05 times x (b-one equals 2.81, b-two equals 1.05). This illustrates that sample estimates are random variables that vary from sample to sample.

### Many Samples Generated from an Experiment

- Samples of size 30 from

y equals beta-one plus beta-two times x, plus u, which equals 1 plus 2 times x, plus u
u is distributed normal with mean zero and variance sigma-u-squared equals 4
x is distributed normal with mean zero and variance 1.

- This is the same model for y as above
- except now regressors are draws from a standard normal distribution
- and n equals 30.
- Next slide gives results from three samples.


### Three Generated Samples yield three different lines

- Scatterplots and regression lines from three samples of size 30 intercepts and slopes vary across samples.

Sample 1
![](https://cdn.mathpix.com/cropped/1db1a0ef-9c44-414f-9671-ab8a889b52b7-16.jpg?height=282&width=348&top_left_y=424&top_left_x=84)

Sample 2
![](https://cdn.mathpix.com/cropped/1db1a0ef-9c44-414f-9671-ab8a889b52b7-16.jpg?height=282&width=346&top_left_y=424&top_left_x=463)

Sample 3
![](https://cdn.mathpix.com/cropped/1db1a0ef-9c44-414f-9671-ab8a889b52b7-16.jpg?height=287&width=349&top_left_y=423&top_left_x=839)

> **Key Concept**: Three different random samples from the same population produce three different regression lines, illustrating sampling variability. Each sample yields different estimates of beta-one and beta-two, but all estimates cluster around the true population values. This demonstrates that the OLS estimators b-one and b-two are random variables whose distributions depend on the sampling process.

### 400 Generated Samples of Size 30

- 400 such samples were generated and fitted
- left panel: beta-two equals 2 and average of 400 slopes equals 1.979.
- right panel: beta-one equals 1 and average of 400 intercepts equals 1.039.
- both histograms are approximately normal.
![](https://cdn.mathpix.com/cropped/1db1a0ef-9c44-414f-9671-ab8a889b52b7-17.jpg?height=402&width=529&top_left_y=407&top_left_x=89)

Generated data: 400 Intercepts
![](https://cdn.mathpix.com/cropped/1db1a0ef-9c44-414f-9671-ab8a889b52b7-17.jpg?height=372&width=529&top_left_y=436&top_left_x=654)

> **Key Concept**: With 400 samples, we see that the average of the 400 slope estimates (1.979) is very close to the true beta-two (2.0), and the average of the 400 intercept estimates (1.039) is very close to the true beta-one (1.0). This demonstrates unbiasedness: on average across many samples, the OLS estimates equal the true parameters. The approximately normal distributions of these estimates illustrate the Central Limit Theorem in action.

### Many Samples Generated from a Finite Population

- Data from the 1880 Census
- complete enumeration of the U.S. population in 1880.
- Relationship between
- y equals labforce equals labor force participation
- 1 if in the labor force; 0 if not in the labor force
- and x equals age equals 60 to 70 years.
- Population is of size 1,058,475 (men aged 60 to 70 years)
- Population mean of labforce is 0.8945
- so 89.45% were in the labor force.


### Population Regression Line

- Population regression line is

labforce equals beta-one plus beta-two times age

- Population regression line based on 1,058,475 observations is

labforce equals 1.593 minus 0.0109 times age

- so beta-one equals 1.593 and beta-two equals negative 0.0109
- with each extra year the probability of being in the labor force falls by 0.0109 or by 1.09 percentage points.

> **Key Concept**: Using the complete 1880 Census population of over one million men aged 60-70, we can calculate the true population regression line: labforce equals 1.593 minus 0.0109 times age. The slope beta-two equals negative 0.0109 means each additional year of age reduces labor force participation probability by 1.09 percentage points. This population line serves as the benchmark against which sample estimates will be compared.

### 400 Samples of Size 200

- Draw 400 samples of size 200; regress labforce on age in each sample
- large sample sizes as regression fit is poor: R-squared is approximately 0.01.
- left panel: beta-two equals negative 0.0109 and average of 400 slopes is negative 0.0115
- right panel: beta-one equals 1.593 and average of 400 intercepts is 1.636
- both histograms are approximately normal.
![](https://cdn.mathpix.com/cropped/1db1a0ef-9c44-414f-9671-ab8a889b52b7-20.jpg?height=405&width=533&top_left_y=416&top_left_x=87)

Census data: 400 Intercepts
![](https://cdn.mathpix.com/cropped/1db1a0ef-9c44-414f-9671-ab8a889b52b7-20.jpg?height=375&width=532&top_left_y=446&top_left_x=653)

> **Key Concept**: Drawing 400 samples of size 200 from the Census population shows unbiasedness and approximate normality in a real-world setting. The average slope estimate (negative 0.0115) is close to the true beta-two (negative 0.0109), and the average intercept (1.636) is close to beta-one (1.593). The approximately normal distributions of these estimates confirm that the Central Limit Theorem applies even when the dependent variable is binary (labor force participation) and the fit is poor (R-squared approximately 0.01).

## 6.3 Properties of the Least Squares Estimator

- Slope estimate is a random variable

b-two equals the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, times the quantity y-sub-i minus y-bar, all divided by the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared

- different samples have different data and hence different b-two values.
- We want to find the expected value of b-two, the variance of b-two, and a distribution for inference.
- If we assume the model is y-sub-i equals beta-one plus beta-two times x-sub-i, plus u-sub-i, then some algebra leads to the re-expression of the formula for b-two as

b-two equals beta-two plus the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, times u-sub-i, all divided by the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared.

- Conditioning on the regressors x-sub-i, the only source of randomness is the errors u-sub-i.
- It follows that the expected value of b-two and the variance of b-two depend crucially on assumptions about the error u-sub-i.

> **Key Concept**: The OLS slope estimator b-two can be re-expressed as b-two equals beta-two plus a weighted sum of the errors. This decomposition shows that b-two equals the true parameter beta-two plus a term involving the errors u-sub-i. When we condition on the regressors x-sub-i, the only source of randomness is the errors. This means the statistical properties of b-two, including its expected value and variance, depend entirely on the properties we assume for the error term.

### Data Assumptions

- Always assume that there is variation in the regressors
- we rule out the case x-sub-i equals x-bar for all i
- this ensures the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared, is strictly greater than zero.
- Otherwise cannot compute b-one and b-two.
- Also at least 3 observations.


### Population Assumptions

- Standard assumptions are that:
- 1. The population model is y-sub-i equals beta-one plus beta-two times x-sub-i, plus u-sub-i for all i.
- 2. The error for the i-th observation has mean zero conditional on x: the expected value of u-sub-i given x-sub-i equals zero for all i.
- 3. The error for the i-th observation has constant variance conditional on x: the variance of u-sub-i given x-sub-i equals sigma-u-squared for all i.
- 4. The errors for different observations are statistically independent: u-sub-i is independent of u-sub-j for all i not equal to j.
- Assumptions 1-2 are the crucial assumptions that ensure

The expected value of y-sub-i given x-sub-i equals beta-one plus beta-two times x-sub-i

- Assumption 3 is called conditionally homoskedastic errors

> **Key Concept**: Four standard OLS assumptions are: (1) correct linear model specification, (2) zero conditional mean errors, (3) homoskedastic errors with constant variance sigma-u-squared, and (4) independent errors across observations. Assumptions 1-2 are essential for unbiasedness, ensuring the conditional mean is correctly specified as beta-one plus beta-two times x. Assumptions 3-4 affect the variance formulas and can be relaxed, but 1-2 are fundamental for consistent and unbiased estimation.

### Mean and Variance of the OLS Slope Coefficient

- Given assumptions 1-2 (y equals beta-one plus beta-two times x, plus u, and the expected value of u given x equals zero)

The expected value of b-two equals beta-two.

- Given assumptions 1-4 (add the variance of u given x equals sigma-u-squared and independent errors)

sigma-b-two-squared equals the variance of b-two equals sigma-u-squared divided by the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared

- These results are proved in Appendix C.1
- in the simpler case of a model without intercept.

> **Key Concept**: Under assumptions 1-2, the OLS slope estimator b-two is unbiased, meaning the expected value of b-two equals beta-two. Under assumptions 1-4, the variance of b-two equals sigma-u-squared divided by the sum of squared deviations of x from its mean. This variance decreases with smaller error variance, larger sample size, and greater spread in the x values. These properties form the foundation for statistical inference about the slope parameter.

### Estimate of the Error Variance

- sigma-b-two-squared equals the variance of b-two depends in part on sigma-u-squared which is unknown.
- So estimation of the variance of b-two requires an estimate of sigma-u-squared.
- Estimate variance of the error sigma-u-squared by the sample variance of the residuals

s-e-squared equals 1 over n minus 2, times the sum from i equals 1 to n of the quantity y-sub-i minus y-hat-sub-i, all squared

- We use 1 over n minus 2 as this guarantees s-e-squared is unbiased for sigma-u-squared.
- the "intuition" is that y-hat equals b-one plus b-two times x is based on two estimated coefficients leaving n minus 2 degrees of freedom.
- The standard error of the regression or the root mean squared error takes the square root to give an estimate of sigma-u

s-e equals the square root of 1 over n minus 2, times the sum from i equals 1 to n of the quantity y-sub-i minus y-hat-sub-i, all squared

> **Key Concept**: Since the error variance sigma-u-squared is unknown, we estimate it using s-e-squared, the sample variance of the residuals. We divide by n minus 2 degrees of freedom (not n) because we've estimated two parameters (beta-one and beta-two), leaving n minus 2 independent pieces of information. The divisor n minus 2 ensures s-e-squared is an unbiased estimator of sigma-u-squared. Taking the square root gives s-e, the standard error of the regression, which estimates sigma-u.

### Estimate of the Variance of the OLS Slope Coefficient

- Under assumptions 1-4

The variance of b-two equals sigma-b-two-squared equals sigma-u-squared divided by the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared

- Replace sigma-u-squared with estimate s-e-squared equals 1 over n minus 2, times the sum from i equals 1 to n of the quantity y-sub-i minus y-hat-sub-i, all squared.
- The estimated variance of b-two is then

s-e-squared divided by the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared.

- Taking the square root, the standard error of b-two is

The standard error of b-two equals the square root of s-e-squared divided by the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared, which equals s-e divided by the square root of the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared

> **Key Concept**: The standard error of b-two is our estimate of the standard deviation of the sampling distribution of b-two. It's calculated by replacing the unknown error variance sigma-u-squared with its estimate s-e-squared in the variance formula. The standard error equals s-e divided by the square root of the sum of squared x deviations. This standard error measures the precision of our slope estimate and is fundamental for constructing confidence intervals and hypothesis tests.

### Example: Computation of the Standard Error

- Artificial data on a sample of size five
- (y, x) equals (1,1), (2,2), (2,3), (2,4) and (3,5).
- From chapter 5: y-hat equals 0.8 plus 0.4 times x.
- so y-hat-sub-1 equals 1.2, y-hat-sub-2 equals 1.6, y-hat-sub-3 equals 2.0, y-hat-sub-4 equals 2.4, y-hat-sub-5 equals 2.8.
- Standard error of the regression s-e equals the square root of 0.1333333 equals 0.365148 since

To calculate s-e-squared, we have s-e-squared equals 1 over n minus 2, times the sum from i equals 1 to n of the quantity y-sub-i minus y-hat-sub-i, all squared. This equals 1 over 3, times the quantity, 1 minus 1.2 all squared, plus 2 minus 1.6 all squared, plus 2 minus 2 all squared, plus 2 minus 2.4 all squared, plus 3 minus 2.8 all squared. This equals 0.13333

- The sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared, equals 10, calculated earlier in computing b-two. So

The standard error of b-two, all squared, equals s-e-squared divided by the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared, which equals 0.133333 divided by 10, which equals 0.0133333.

- Standard error of the slope b-two is the standard error of b-two equals the square root of 0.013333 equals 0.115.

> **Key Concept**: This numerical example demonstrates the calculation of the standard error step by step. With n equals 5 observations, the fitted line y-hat equals 0.8 plus 0.4 times x produces residuals that sum to s-e-squared equals 0.1333 (using n minus 2 equals 3 degrees of freedom). Combined with the sum of squared x deviations of 10, this yields a standard error of b-two of 0.115. This measures the precision of our slope estimate in this small sample.

### When is the Slope Coefficient Precisely Estimated?

- The standard error of b-two is the standard error of b-two equals the square root of s-e-squared divided by the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared.
- Better precision equals smaller standard error occurs if
- 1. Model fits well (s-e-squared is smaller)
- 2. Many observations (then the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared, is larger).
- 3. Regressors are widely scattered (then the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared, is larger).

> **Key Concept**: The precision of the OLS slope estimate, measured by its standard error, improves under three conditions: (1) better model fit with smaller residual variance s-e-squared, (2) larger sample size which increases the sum of squared x deviations, and (3) more widely scattered x values which also increases this sum. These insights guide data collection: when possible, gather more observations and ensure substantial variation in the explanatory variable to achieve more precise estimates.

### Normal Distribution and the Central Limit Theorem

- Under assumptions 1-4

b-two is distributed with mean beta-two and variance sigma-b-two-squared

- The standardized variable

Z equals the quantity b-two minus beta-two, divided by sigma-b-two. This is distributed with mean 0 and variance 1 by construction, and is distributed approximately normal with mean 0 and variance 1 as n approaches infinity if a central limit theorem holds.

- In practice, sigma-b-two is unknown as error standard deviation sigma-u is unknown - this will lead to use of the t distribution in chapter 7.

> **Key Concept**: The Central Limit Theorem tells us that the standardized OLS slope estimator Z equals the quantity b-two minus beta-two divided by sigma-b-two, approaches a standard normal distribution as sample size increases. This holds regardless of the distribution of the error term u, as long as certain regularity conditions are met. Since sigma-b-two is unknown in practice, we replace it with the standard error, leading to the t distribution covered in Chapter 7. This result is the foundation for large-sample inference in regression analysis.

### Aside: The OLS Intercept Coefficient

- Under assumptions 1-2

The expected value of b-one equals beta-one.

- Given assumptions 1-4

sigma-b-one-squared equals the variance of b-one equals sigma-u-squared times the sum from i equals 1 to n of x-sub-i-squared, all divided by n times the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared.

- The standard error of b-one is

The standard error of b-one equals the square root of s-e-squared times the sum from i equals 1 to n of x-sub-i-squared, all divided by n times the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared.

- And Z equals the quantity b-one minus beta-one, divided by sigma-b-one, is distributed approximately normal with mean 0 and variance 1 as n approaches infinity.

> **Key Concept**: The intercept estimator b-one has similar properties to the slope estimator: it's unbiased under assumptions 1-2, has a variance formula under assumptions 1-4, and is asymptotically normal by the Central Limit Theorem. The variance of b-one depends on the sum of squared x values rather than squared deviations from the mean. When x values are centered near zero, the intercept is estimated more precisely. The standard error of b-one is calculated analogously to that of b-two and is used for inference about the intercept.

### Summary for the OLS Slope Coefficient

A summary given assumptions 1-4 is the following.
(1) y-sub-i given x-sub-i has conditional mean beta-one plus beta-two times x-sub-i and conditional variance sigma-u-squared.
(2) Slope coefficient b-two has mean beta-two and variance sigma-b-two-squared equals sigma-u-squared divided by the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared.
(3) Standard error of b-two is se of b-two where se of b-two squared equals s-e-squared divided by the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared, and s-e-squared equals 1 over n minus 1 times the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared.
(4) Z equals the quantity b-two minus beta-two, divided by sigma-b-two, has mean 0 and variance 1.
(5) As sample size n approaches infinity, Z is standard normal distributed by the central limit theorem.

> **Key Concept**: This summary encapsulates the key theoretical results for OLS estimation. Under standard assumptions: (1) the conditional distribution of y given x has linear mean and constant variance, (2) b-two is unbiased with known variance formula, (3) we can estimate this variance using the standard error, (4) standardizing b-two produces a statistic with mean 0 and variance 1, and (5) this statistic is approximately normally distributed in large samples. These five results form the complete foundation for regression inference.

### Least Squares in Practice

- Assumptions 1-2 are essential for least squares to be unbiased and consistent.
- in particular assumption 2 rules out any correlation between x and u
- e.g. rules out high x being associated with high u
- we maintain these assumptions
- chapter 16 discusses failures
- chapter 17 has some possible solutions.
- Assumptions 3-4 can be relaxed
  - A crucial practical part of regression is choosing the correct variation of assumptions 3 and 4
  - This is necessary to get correct standard errors
  - And hence correct confidence intervals and hypothesis tests

- Chapters 7.7 and 12.1 provide methods

> **Key Concept**: In practice, assumptions 1-2 (correct model and zero conditional mean) are maintained as essential for unbiased estimation. Assumption 2 especially rules out correlation between x and u, which would cause bias. Chapters 16-17 discuss what happens when these fail and potential solutions. Assumptions 3-4 (homoskedasticity and independence) can and often should be relaxed. A crucial practical task is choosing appropriate modifications to these assumptions to obtain correct standard errors, which ensures valid confidence intervals and hypothesis tests. Methods for this are covered in Chapters 7.7 and 12.1.

## 6.4 Estimators of Model Parameters

- Ideal properties of estimators were presented in Chapter 3.6 for estimation of the population mean.
- For centering
- unbiasedness (on average)
- consistency (almost perfect in infinitely large samples).
- For being best
- minimum variance among all possible correctly-centered estimators.
- Bottom line: Under assumptions 1-4 OLS is essentially the best estimator of beta-one and beta-two.


### Unbiased Estimator

- Given assumptions 1-2

The expected value of b-two, conditional on x-one through x-n, equals beta-two.

- b-two is unbiased for beta-two (and b-one is unbiased for beta-one)
- if we obtain many samples yielding many b-two then on average b-two equals beta-two.
- Essentially we need sampling such that the expected value of y-sub-i given x-sub-i equals beta-one plus beta-two times x-sub-i.

> **Key Concept**: Unbiasedness means that on average across repeated samples, the OLS estimator b-two equals the true parameter beta-two. This is a finite-sample property that holds under assumptions 1-2 regardless of sample size. If we could draw many samples and calculate b-two for each, the average of these estimates would equal beta-two. This property ensures our estimator is correctly centered and provides the foundation for consistent estimation.

### Consistent Estimator

- A sufficient condition for a consistent estimator is that as n approaches infinity
- any bias disappears and the variance goes to zero.
- So b-two is consistent for beta-two as:
  - b-two is unbiased for beta-two given assumptions 1-2
  - The variance of b-two approaches zero as n approaches infinity given assumptions 1-4
  - Note: assumptions 3-4 can be relaxed and still get consistency

> **Key Concept**: Consistency is an asymptotic property meaning that as sample size grows, b-two converges in probability to the true beta-two. A sufficient condition is unbiasedness plus variance approaching zero. The OLS estimator b-two is consistent because it's unbiased under assumptions 1-2, and its variance approaches zero as n increases under assumptions 1-4. Importantly, assumptions 3-4 can be relaxed while maintaining consistency—only assumptions 1-2 are essential for this property.

### Minimum Variance Estimator

- We want as precise an estimator as possible
- OLS is the best linear unbiased estimator, or BLUE, of beta-two under assumptions 1-4
  - Lowest variance of all unbiased estimators that are a linear combination of the y values
  - Recall b-two equals the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, times the quantity y-sub-i minus y-bar, all divided by the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared, which equals the sum from i equals 1 to n of w-sub-i times y-sub-i
  - So linear in y-sub-i
- OLS is the best unbiased estimator, or BUE, of beta-two if additionally u is normally distributed
  - So lowest variance of all unbiased estimators
- OLS is the best consistent estimator, or BUE, in standard settings under assumptions 1-4,
- it has smallest variance among consistent estimators.

> **Key Concept**: The Gauss-Markov Theorem establishes that OLS is the Best Linear Unbiased Estimator, or BLUE, under assumptions 1-4. This means OLS has minimum variance among all linear unbiased estimators—no other linear unbiased estimator can be more precise. If we additionally assume normality of errors, OLS is the best unbiased estimator period (not just among linear ones). OLS is also the best consistent estimator in standard settings, having the smallest asymptotic variance. These optimality properties justify using OLS as the default regression estimator.

### Some in-class Exercises

(1) Suppose we know that y equals 8 plus 5 times x, plus u where the expected value of u given x equals zero. Give the conditional mean of y given x and the error term for the observation (x, y) equals (5, 30).
(2) OLS regression of y on x on a large sample leads to slope coefficient equal to 10 with standard error 4. Provide an approximate 95% confidence interval for beta-two in the model y equals beta-one plus beta-two times x, plus u.
(3) OLS regression of y on x on a large sample leads to slope coefficient equal to 20 with standard error 5. Test at level 0.05 the claim that the population slope coefficient equals 8.
(4) You are given the following: the sum from i equals 1 to 27 of the quantity x-sub-i minus x-bar, all squared, equals 20, and the sum from i equals 1 to 27 of the quantity y-sub-i minus y-hat-sub-i, all squared, equals 400. Compute the standard error of the OLS slope coefficient under assumptions 1-4.
(5) Which of assumptions 1-4 ensure that OLS estimates are unbiased?

---

## Key Takeaways

**Population Model and Conditional Mean (Section 6.1):**
- The population regression model assumes the expected value of y given x equals beta-one plus beta-two times x, a linear conditional mean
- Beta-one and beta-two are unknown population parameters; b-one and b-two are sample estimates
- The conditional mean, the expected value of Y given X equals x, is the probability-weighted average of all y values for a given x
- This generalizes univariate analysis where the expected value of Y is constant to regression where the expected value of y given x varies with x
- Not all conditional means are linear—linearity is an assumption we impose
- The error term u equals y minus the expected value of y given x, which equals y minus the quantity beta-one plus beta-two times x, captures deviations from the population line
- Error term u is unobserved because beta-one and beta-two are unknown
- Crucial distinction: error u (unobserved, relative to population line) versus residual e (observed, relative to fitted line)
- Assumption: the expected value of u given x equals zero, meaning errors average to zero at each x value
- This assumption ensures the population line is indeed the expected value of y given x equals beta-one plus beta-two times x

**Error Variance and Homoskedasticity (Section 6.1 continued):**
- The variance of u given x equals sigma-u-squared measures variability of errors around the population line
- Greater error variance means greater noise, reducing precision of estimates
- Homoskedasticity assumption: the variance of u given x equals sigma-u-squared is constant (doesn't vary with x)
- "Homoskedastic" comes from Greek: homos (same) plus skedastic (scattering)
- Since u is the only source of randomness in y given x, we have the variance of y given x equals the variance of u given x equals sigma-u-squared
- This assumption can be (and often is) relaxed in practice
- Univariate: Y-sub-i is distributed with mean mu and variance sigma-squared with constant mean mu
- Regression: y-sub-i given x-sub-i is distributed with mean beta-one plus beta-two times x and variance sigma-u-squared, with mean varying with x but constant variance

**Sampling Experiments (Section 6.2):**
- Two types of sampling experiments demonstrate OLS properties
- Generated data: Create 400 samples from known model y equals 1 plus 2 times x, plus u with u distributed normal with mean zero and variance 4
- Finite population: Draw 400 samples from 1880 Census (1.06 million males aged 60-70)
- Key findings from both experiments: (1) Average of 400 slopes b-two is close to true beta-two (unbiasedness)
- (2) Distribution of 400 slopes is approximately normal (Central Limit Theorem)
- (3) Similar results hold for intercept b-one
- Single sample: b-one does not equal beta-one and b-two does not equal beta-two due to sampling variability
- Multiple samples: Estimates vary across samples, but center on true parameters
- Census example: beta-two equals negative 0.0109 (each year reduces labor force participation by 1.09 percentage points)
- 400 samples gave average slope negative 0.0115, close to true negative 0.0109

**OLS as a Random Variable (Section 6.3):**
- The OLS slope b-two equals the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, times the quantity y-sub-i minus y-bar, all divided by the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared, varies across samples (it's a random variable)
- Under model y-sub-i equals beta-one plus beta-two times x-sub-i, plus u-sub-i, algebra shows b-two equals beta-two plus the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, times u-sub-i, all divided by the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared
- Conditional on regressors x-sub-i, the only source of randomness is errors u-sub-i
- Properties of b-two depend crucially on assumptions about u-sub-i
- Data requirement: Must have variation in regressors (the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared, must be greater than zero), otherwise cannot compute b-one and b-two
- Need at least 3 observations for bivariate regression

**Four Core OLS Assumptions (Section 6.3 continued):**
- Assumption 1 (Correct model): y-sub-i equals beta-one plus beta-two times x-sub-i, plus u-sub-i for all i
- Assumption 2 (Mean-zero error): the expected value of u-sub-i given x-sub-i equals zero for all i (no correlation between x and u)
- Assumption 3 (Homoskedasticity): the variance of u-sub-i given x-sub-i equals sigma-u-squared for all i (constant error variance)
- Assumption 4 (Independence): u-sub-i independent of u-sub-j for all i not equal to j (no autocorrelation)
- Assumptions 1-2 are crucial for unbiasedness: ensure the expected value of y-sub-i given x-sub-i equals beta-one plus beta-two times x-sub-i
- Assumptions 3-4 affect variance and standard errors, not bias
- Assumptions can be relaxed: 3-4 often relaxed in practice (use robust standard errors)
- Assumptions 1-2 essential; violations cause bias and inconsistency (Chapter 16)

**Mean and Variance of OLS Slope (Section 6.3 continued):**
- Given assumptions 1-2: the expected value of b-two equals beta-two (unbiasedness)
- Given assumptions 1-4: the variance of b-two equals sigma-u-squared divided by the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared
- Standard deviation of b-two: sigma-b-two equals sigma-u divided by the square root of the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared
- Variance of b-two decreases with: (1) smaller sigma-u-squared (better model fit), (2) larger sum of squared x deviations (more observations or more scattered x)
- Proofs provided in Appendix C.1 for simpler case without intercept

**Estimating Error Variance (Section 6.3 continued):**
- Sigma-u-squared is unknown, so estimate it using residuals
- Standard error of regression: s-e-squared equals 1 over n minus 2, times the sum from i equals 1 to n of the quantity y-sub-i minus y-hat-sub-i, all squared, estimates sigma-u-squared
- Use (n minus 2) denominator (not n) because we estimated 2 coefficients, leaving (n minus 2) degrees of freedom
- This divisor ensures s-e-squared is unbiased for sigma-u-squared
- Root mean squared error: s-e equals the square root of s-e-squared estimates sigma-u
- Example: With n equals 5, y-hat equals 0.8 plus 0.4 times x, we compute s-e equals 0.365

**Standard Error of OLS Slope (Section 6.3 continued):**
- Estimated variance of b-two: s-e-squared divided by the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared (replace unknown sigma-u-squared with estimate s-e-squared)
- Standard error of b-two: the standard error of b-two equals s-e divided by the square root of the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared
- The standard error of b-two measures precision of b-two as estimate of beta-two
- Example calculation: With the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared, equals 10 and s-e-squared equals 0.133, we get the standard error of b-two equals 0.115

**Factors Affecting Precision (Section 6.3 continued):**
- Better precision (smaller standard error of b-two) occurs when:
- 1. Model fits well (s-e-squared is smaller) - less noise around regression line
- 2. Many observations (the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared, is larger) - more data reduces sampling variability
- 3. Regressors widely scattered (the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared, is larger) - more variation in x provides more information
- Precision improves with square root of n, so need 4 times observations to halve standard error
- Trade-off: Can't control regressor scatter in observational data, but can increase sample size

**Central Limit Theorem for OLS (Section 6.3 continued):**
- Under assumptions 1-4: b-two is distributed with mean beta-two and variance sigma-b-two-squared, where sigma-b-two-squared equals sigma-u-squared divided by the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared
- Standardized variable: Z equals the quantity b-two minus beta-two, divided by sigma-b-two, has mean 0 and variance 1 by construction
- Central Limit Theorem: As n approaches infinity, Z is distributed approximately normal with mean 0 and variance 1 (approximately normal for large samples)
- This implies b-two is distributed approximately normal with mean beta-two and variance sigma-b-two-squared for large n
- In practice, sigma-b-two is unknown (depends on unknown sigma-u)
- Replace sigma-b-two with the standard error of b-two leads to t distribution (Chapter 7)
- Normality justifies using normal-based inference for large samples

**Intercept Properties (Section 6.3 continued):**
- Under assumptions 1-2: the expected value of b-one equals beta-one (unbiased)
- Under assumptions 1-4: the variance of b-one equals sigma-u-squared times the sum from i equals 1 to n of x-sub-i-squared, all divided by n times the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared
- Standard error of b-one: the standard error of b-one equals the square root of s-e-squared times the sum from i equals 1 to n of x-sub-i-squared, all divided by n times the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared
- Intercept variance depends on the sum of squared x values
- If x values centered at zero, intercept more precisely estimated
- Central Limit Theorem applies: the quantity b-one minus beta-one, divided by sigma-b-one, is distributed approximately normal with mean 0 and variance 1 as n approaches infinity

**Summary of OLS Properties (Section 6.3 continued):**
- (1) Conditional distribution: y-sub-i given x-sub-i has mean beta-one plus beta-two times x-sub-i and variance sigma-u-squared
- (2) Slope mean and variance: the expected value of b-two equals beta-two and the variance of b-two equals sigma-u-squared divided by the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared
- (3) Standard error: the standard error of b-two squared equals s-e-squared divided by the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared, where s-e-squared equals the sum of squared residuals divided by n minus 2
- (4) Standardized statistic: Z equals the quantity b-two minus beta-two, divided by sigma-b-two, has mean 0, variance 1
- (5) Normality: Z is distributed approximately normal with mean 0 and variance 1 as n approaches infinity by Central Limit Theorem
- These results form the foundation for confidence intervals and hypothesis tests (Chapter 7)

**Practical Considerations (Section 6.3 continued):**
- Assumptions 1-2 are essential for OLS to be unbiased and consistent
- Assumption 2 rules out correlation between x and u (no omitted variables problem)
- Maintain assumptions 1-2 in standard applications
- Chapter 16 discusses violations; Chapter 17 presents solutions
- Assumptions 3-4 can be relaxed (common in practice)
- Crucial task: Choose correct specification for assumptions 3-4 to get correct standard errors
- Incorrect standard errors invalidate confidence intervals and hypothesis tests
- Chapters 7.7 and 12.1 provide methods for robust standard errors

**Unbiased Estimator (Section 6.4):**
- Under assumptions 1-2: the expected value of b-two conditional on x-one through x-n equals beta-two (unbiased)
- If we obtain many samples, on average b-two equals beta-two
- Requires sampling such that the expected value of y-sub-i given x-sub-i equals beta-one plus beta-two times x-sub-i
- Unbiasedness is a finite-sample property (holds for any sample size)
- Both b-one and b-two are unbiased under assumptions 1-2

**Consistent Estimator (Section 6.4 continued):**
- Sufficient condition for consistency: as n approaches infinity, bias approaches zero and variance approaches zero
- b-two is consistent for beta-two because:
  - (1) b-two is unbiased (given assumptions 1-2)
  - (2) The variance of b-two equals sigma-u-squared divided by the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared, approaches zero as n approaches infinity (given assumptions 1-4)
- Consistency is an asymptotic property (behavior as sample size grows)
- Note: Can relax assumptions 3-4 and still get consistency (only need 1-2)
- Consistency means b-two converges in probability to beta-two

**Efficiency and BLUE (Section 6.4 continued):**
- Best Linear Unbiased Estimator, or BLUE: OLS has minimum variance among all linear unbiased estimators under assumptions 1-4
- "Linear" means estimator is linear combination of y values: b-two equals the sum from i equals 1 to n of w-sub-i times y-sub-i
- Gauss-Markov Theorem: OLS is BLUE under assumptions 1-4
- If additionally u is normally distributed: OLS is Best Unbiased Estimator, or BUE
  - Lowest variance among ALL unbiased estimators (not just linear ones)
- OLS is also best consistent estimator in standard settings
- Bottom line: Under assumptions 1-4, OLS is essentially the best estimator of beta-one and beta-two

**Why OLS is Optimal:**
- OLS minimizes sum of squared residuals: minimize the sum from i equals 1 to n of the quantity y-sub-i minus b-one minus b-two times x-sub-i, all squared
- This criterion leads to estimator that is unbiased, consistent, and efficient
- Alternative estimators (LAD, robust regression) may be better under specific violations
- But OLS is optimal baseline under standard assumptions
- Computational advantages: OLS has closed-form solution, easy to implement
- Well-understood statistical properties make inference straightforward

**Software Implementation:**
- Python: Use statsmodels.OLS or scipy.stats.linregress for OLS regression
- Generated data example uses random seed for reproducibility
- Visualization: scatter plots with fitted regression line show data and model
- Can compare population line versus fitted line when population model known

---