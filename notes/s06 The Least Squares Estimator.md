# Chapter 6: The Least Squares Estimator

## Learning Objectives

By the end of this chapter, you will be able to:

- Distinguish between the population regression line (β₁ + β₂x) and the sample regression line (b₁ + b₂x)
- Understand the conditional mean E[y|x] = β₁ + β₂x and the error term u = y - E[y|x]
- Differentiate between the unobserved error term u and the observed residual e
- Apply the four key OLS assumptions: correct model, mean-zero errors, homoskedasticity, and independence
- Calculate the variance and standard error of OLS slope coefficient b₂
- Explain why b₂ is an unbiased estimator of β₂ under assumptions 1-2
- Compute the standard error of the regression (se) and use it to estimate precision
- Understand when OLS estimates are more precise (good fit, many observations, scattered regressors)
- Apply the Central Limit Theorem to show b₂ is approximately normally distributed for large samples
- Recognize that OLS is the Best Linear Unbiased Estimator (BLUE) under standard assumptions

---

## 6.1 Population Model: Conditional Mean of y given x

- The sample model is a line $b_{1}+b_{2} x$.
- So we assume that the population model is also a line, denoted $\beta_{1}+\beta_{2} x$
- where $\beta$ is "beta" and we use Greek letters for (unknown) parameters.
- More formally the conditional mean of $y$ is assumed to be linear in $x$

$$
\mathrm{E}[Y \mid X=x]=\beta_{1}+\beta_{2} x
$$

- The population conditional mean of $Y$ given $X=x$
- is the probability-weighted average of all possible values of $Y$ for a given value of $x$; e.g. earnings conditional on years of schooling
- is denoted $\mathrm{E}[Y \mid X=x]$
- generalizes $\mathrm{E}[Y]$ in chapter 3 that is the probability-weighted average of all possible values of $Y$.


### Population Conditional Mean (continued)

- We assume that the conditional mean is linear in $x$

$$
\mathrm{E}[Y \mid X=x]=\beta_{1}+\beta_{2} x
$$

- Commonly-used simpler notation is

$$
\mathrm{E}[y \mid x]=\beta_{1}+\beta_{2} x .
$$

- Note: In general the conditional mean need not be linear.
- Case 1: $\mathrm{E}[Y \mid X=1]=5, \mathrm{E}[Y \mid X=2]=7, \mathrm{E}[Y \mid X=3]=9$
$\star$ linear since this implies $\mathrm{E}[Y \mid X=x]=3+2 x$.
- Case 2: $\mathrm{E}[Y \mid X=1]=5, \mathrm{E}[Y \mid X=2]=7, \mathrm{E}[Y \mid X=3]=12$
$\star$ nonlinear as increase by 2 from $X=1$ to $X=2$ but increases by 5 from $X=2$ to $X=3$.
- In Chapter 9 we consider nonlinear conditional means.


### Error Term

- $y$ does not exactly equal $\beta_{1}+\beta_{2} x$
- instead $\mathrm{E}[y \mid x]=\beta_{1}+\beta_{2} x$.
- The difference between $y$ and $\mathrm{E}[y \mid x]$ is called the error term $u$

$$
\begin{aligned}
u & =y-\mathrm{E}[y \mid x] \\
& =y-\left(\beta_{1}+\beta_{2} x\right) .
\end{aligned}
$$

- The error term $u$ is not observed as $\beta_{1}$ and $\beta_{2}$ are unknown.


### Error Term versus Residual - a crucial distinction

- $u$ is not observed - it is the difference between $y$ and the unknown population line $\beta_{1}+\beta_{2} \times$ (the solid line)
- $e$ is observed - it is the difference between $y$ and the known fitted line $b_{2}+b_{2} \times$ (the dashed line)
![](https://cdn.mathpix.com/cropped/1db1a0ef-9c44-414f-9671-ab8a889b52b7-08.jpg?height=449&width=516&top_left_y=397&top_left_x=75)
![](https://cdn.mathpix.com/cropped/1db1a0ef-9c44-414f-9671-ab8a889b52b7-08.jpg?height=445&width=480&top_left_y=399&top_left_x=712)


### Error Term is assumed to have mean zero

- Since $u=y-\left(\beta_{1}+\beta_{2} x\right)$ we have

$$
y=\beta_{1}+\beta_{2} x+u
$$

- The error term is assumed to be zero on average for each $x$ value
- sometimes $u_{i}>0$ and so $y_{i}$ is above the population line
- sometimes $u_{i}<0$ and so $y_{i}$ is below the population line
- but the long-run average of $u_{i}$ (at each value of $x$ ) is zero.
- More precisely the error term has conditional mean zero

$$
\mathrm{E}[u \mid x]=0 .
$$

- This ensures that the population line is indeed $\beta_{1}+\beta_{2} x$.

$$
\begin{aligned}
\mathrm{E}[y \mid x] & =\mathrm{E}\left[\beta_{1}+\beta_{2} x+u \mid x\right] \\
& =\beta_{1}+\beta_{2} x+\mathrm{E}[u \mid x] \\
& =\beta_{1}+\beta_{2} x \quad \text { if } \mathrm{E}[u \mid x]=0
\end{aligned}
$$

### Population Conditional Variance of y given x

- The variability of the error term around the line will determine in part the precision of our estimates
- greater variability is greater noise so less precision.
- We initially assume that the error variance is constant and does not vary with $x$

$$
\operatorname{Var}[u \mid x]=\sigma_{u}^{2}
$$

- This is called the assumption of homoskedastic errors
- "skedastic" based on the Greek word for scattering
- "homos" is the Greek word for same
- this assumption can be relaxed (and is often relaxed - later).
- The error term provides the only variation in $y$ around the population line so then

$$
\operatorname{Var}[y \mid x]=\operatorname{Var}[u \mid x]=\sigma_{u}^{2}
$$

### Summary

- The bottom line:
- Univariate analysis: $y_{1}, \ldots, y_{n}$ is a simple random sample with

$$
Y_{i} \sim\left(\mu, \sigma^{2}\right) .
$$

- Regression analysis: $\left(x_{1}, y_{1}\right), \ldots,\left(x_{n}, y_{n}\right)$ is a simple random sample that allows the mean to vary with $x$, so

$$
y_{i} \mid x_{i} \sim\left(\beta_{1}+\beta_{2} x, \sigma_{u}^{2}\right) .
$$

## 6.2 Examples of Sampling from a Population

- We consider two examples of sampling from a population
- regression generalizations of the two examples in chapter 4.
- 1. Generate by computer 400 samples from an explicit model $y=\beta_{1}+\beta_{2} x+u$.
- 2. Select 400 samples from a finite population - the U.S. 1880 Census for males aged 60-69 years.
- In both cases we run 400 regressions giving 400 estimates $b_{1}$ and $b_{2}$ and find
- the average of the 400 slopes $b_{2}$ is close to $\beta_{2}$
- the distribution of the 400 slopes $b_{2}$ is approximately normal
- similar results hold for the intercept $b_{1}$.


### Single Sample Generated from an Experiment

- Example with $n=5$ is generate data from

$$
\begin{aligned}
y & =\beta_{1}+\beta_{2} x+u=1+2 x+u \\
u & \sim N\left(0, \sigma_{u}^{2}=4\right) \\
x & =1,2,3,4,5 .
\end{aligned}
$$

- note: added the assumption that errors are normally distributed
- Then a random normal generator for $u$ yielded

| Observation | x | $\mathrm{E}[\mathrm{y} \mid \mathrm{x}]=1+2 \mathrm{x}$ | $u$ | $\mathrm{y}=1+2 \mathrm{x}+u$ |
| :--- | :---: | :---: | :---: | :---: |
| 1 | 1 | $1+2 \times 1=3$ | 1.689889 | 4.689889 |
| 2 | 2 | $1+2 \times 2=5$ | -.3187171 | 4.681283 |
| 3 | 3 | $1+2 \times 3=7$ | -2.506667 | 4.493333 |
| 4 | 4 | $1+2 \times 4=9$ | -1.63328 | 7.366720 |
| 5 | 5 | $1+2 \times 5=11$ | -2.390764 | 8.609236 |

- Five generated observations
- left panel: population regression line $y=\beta_{1}+\beta_{2} x=1+2 x$
- right panel: sample regression line $\widehat{y}=b_{1}+b_{2} x=2.81+1.05 x$
- note that $b_{1} \neq \beta_{1}$ and $b_{2} \neq \beta_{2}$.

Population line
![](https://cdn.mathpix.com/cropped/1db1a0ef-9c44-414f-9671-ab8a889b52b7-14.jpg?height=395&width=537&top_left_y=426&top_left_x=81)

Regression line
![](https://cdn.mathpix.com/cropped/1db1a0ef-9c44-414f-9671-ab8a889b52b7-14.jpg?height=395&width=545&top_left_y=426&top_left_x=643)

### Many Samples Generated from an Experiment

- Samples of size 30 from

$$
\begin{aligned}
y & =\beta_{1}+\beta_{2} x+u=1+2 x+u \\
u & \sim N\left(0, \sigma_{u}^{2}=4\right) \\
x & \sim N(0,1) .
\end{aligned}
$$

- This is the same model for $y$ as above
- except now regressors are draws from a standard normal distribution
- and $n=30$.
- Next slide gives results from three samples.


### Three Generated Samples yield three different lines

- Scatterplots and regression lines from three samples of size 30 intercepts and slopes vary across samples.

Sample 1
![](https://cdn.mathpix.com/cropped/1db1a0ef-9c44-414f-9671-ab8a889b52b7-16.jpg?height=282&width=348&top_left_y=424&top_left_x=84)

Sample 2
![](https://cdn.mathpix.com/cropped/1db1a0ef-9c44-414f-9671-ab8a889b52b7-16.jpg?height=282&width=346&top_left_y=424&top_left_x=463)

Sample 3
![](https://cdn.mathpix.com/cropped/1db1a0ef-9c44-414f-9671-ab8a889b52b7-16.jpg?height=287&width=349&top_left_y=423&top_left_x=839)

### 400 Generated Samples of Size 30

- 400 such samples were generated and fitted
- left panel: $\beta_{2}=2$ and average of 400 slopes equals 1.979.
- right panel: $\beta_{1}=1$ and average of 400 intercepts equals 1.039 .
- both histograms are approximately normal.
![](https://cdn.mathpix.com/cropped/1db1a0ef-9c44-414f-9671-ab8a889b52b7-17.jpg?height=402&width=529&top_left_y=407&top_left_x=89)

Generated data: 400 Intercepts
![](https://cdn.mathpix.com/cropped/1db1a0ef-9c44-414f-9671-ab8a889b52b7-17.jpg?height=372&width=529&top_left_y=436&top_left_x=654)

### Many Samples Generated from a Finite Population

- Data from the 1880 Census
- complete enumeration of the U.S. population in 1880.
- Relationship between
- $y=$ labforce $=$ labor force participation
$\star 1$ if in the labor force; 0 if not in the labor force
- and $x=$ age $=60$ to 70 years.
- Population is of size $1,058,475$ (men aged $60-70$ years)
- Population mean of labforce is 0.8945
- so $89.45 \%$ were in the labor force.


### Population Regression Line

- Population regression line is

$$
\text { labforce }=\beta_{1}+\beta_{2} \times \text { age }
$$

- Population regression line based on $1,058,475$ observations is

$$
\text { labforce }=1.593-0.0109 \times \text { age }
$$

- so $\beta_{1}=1.593$ and $\beta_{2}=-0.0109$
- with each extra year the probability of being in the labor force falls by 0.0109 or by 1.09 percentage points.


### 400 Samples of Size 200

- Draw 400 samples of size 200 ; regress labforce on age in each sample
- large sample sizes as regression fit is poor: $R^{2} \simeq 0.01$.
- left panel: $\beta_{2}=-0.0109$ and average of 400 slopes is -0.0115
- right panel: $\beta_{1}=1.593$ and average of 400 intercepts is 1.636
- both histograms are approximately normal.
![](https://cdn.mathpix.com/cropped/1db1a0ef-9c44-414f-9671-ab8a889b52b7-20.jpg?height=405&width=533&top_left_y=416&top_left_x=87)

Census data: 400 Intercepts
![](https://cdn.mathpix.com/cropped/1db1a0ef-9c44-414f-9671-ab8a889b52b7-20.jpg?height=375&width=532&top_left_y=446&top_left_x=653)

## 6.3 Properties of the Least Squares Estimator

- Slope estimate is a random variable

$$
b_{2}=\frac{\sum_{i=1}^{n}\left(x_{i}-\bar{x}\right)\left(y_{i}-\bar{y}\right)}{\sum_{i=1}^{n}\left(x_{i}-\bar{x}\right)^{2}}
$$

- different samples have different data and hence different $b_{2}^{\prime} s$.
- We want to find $E\left[b_{2}\right], \operatorname{Var}\left[b_{2}\right]$ and a distribution for inference.
- If we assume the model is $y_{i}=\beta_{1}+\beta_{2} x_{i}+u_{i}$ then some algebra leads to the re-expression of the formula for $b_{2}$ as

$$
b_{2}=\beta_{2}+\frac{\sum_{i=1}^{n}\left(x_{i}-\bar{x}\right) u_{i}}{\sum_{i=1}^{n}\left(x_{i}-\bar{x}\right)^{2}} .
$$

- Conditioning on the regressors $x_{i}$, the only source of randomness is the errors $u_{i}$.
- It follows that $E\left[b_{2}\right]$ and $\operatorname{Var}\left[b_{2}\right]$ depend crucially on assumptions about the error $u_{i}$.


### Data Assumptions

- Always assume that there is variation in the regressors
- we rule out the case $x_{i}=\bar{x}$ for all $i$
- this ensures $\sum_{i=1}^{n}\left(x_{i}-\bar{x}\right)^{2}>0$.
- Otherwise cannot compute $b_{1}$ and $b_{2}$.
- Also at least 3 observations.


### Population Assumptions

- Standard assumptions are that:
-1. The population model is $y_{i}=\beta_{1}+\beta_{2} x_{i}+u_{i}$ for all $i$.
- 2. The error for the $i^{\text {th }}$ observation has mean zero conditional on x: $\mathrm{E}\left[u_{i} \mid x_{i}\right]=0$ for all $i$.
- 3. The error for the $i^{\text {th }}$ observation has constant variance conditional on x: $\operatorname{Var}\left[u_{i} \mid x_{i}\right]=\sigma_{u}^{2}$ for all $i$.
- 4. The errors for different observations are statistically independent: $u_{i}$ is independent of $u_{j}$ for all $i \neq j$.
- Assumptions 1-2 are the crucial assumptions that ensure

$$
\mathrm{E}\left[y_{i} \mid x_{i}\right]=\beta_{1}+\beta_{2} x_{i}
$$

- Assumption 3 is called conditionally homoskedastic errors


### Mean and Variance of the OLS Slope Coefficient

- Given assumptions 1-2 $\left(y=\beta_{1}+\beta_{2} x+u\right.$ and $\left.\mathrm{E}[u \mid x]=0\right)$

$$
\mathrm{E}\left[b_{2}\right]=\beta_{2} .
$$

- Given assumptions 1-4 (add $\mathrm{V}[u \mid x]=\sigma_{u}^{2}$ and independent errors)

$$
\sigma_{b_{2}}^{2}=\operatorname{Var}\left[b_{2}\right]=\frac{\sigma_{u}^{2}}{\sum_{i=1}^{n}\left(x_{i}-\bar{x}\right)^{2}}
$$

- These results are proved in Appendix C. 1
- in the simpler case of a model without intercept.


### Estimate of the Error Variance

- $\sigma_{b_{2}}^{2}=\operatorname{Var}\left[b_{2}\right]$ depends in part on $\sigma_{u}^{2}$ which is unknown.
- So estimation of $\operatorname{Var}\left[b_{2}\right]$ requires an estimate of $\sigma_{u}^{2}$.
- Estimate variance of the error $\sigma_{u}^{2}$ by the sample variance of the residuals

$$
s_{e}^{2}=\frac{1}{n-2} \sum_{i=1}^{n}\left(y_{i}-\widehat{y}_{i}\right)^{2}
$$

- We use $1 /(n-2)$ as this guarantees $s_{e}^{2}$ is unbiased for $\sigma_{u}^{2}$.
- the "intuition" is that $\hat{y}=b_{1}+b_{2} x$ is based on two estimated coefficients leaving ( $n-2$ ) degrees of freedom.
- The standard error of the regression or the root mean squared error takes the square root to give an estimate of $\sigma_{u}$

$$
s_{e}=\sqrt{\frac{1}{n-2} \sum_{i=1}^{n}\left(y_{i}-\widehat{y}_{i}\right)^{2}}
$$

### Estimate of the Variance of the OLS Slope Coefficient

- Under assumptions 1-4

$$
\operatorname{Var}\left[b_{2}\right]=\sigma_{b_{2}}^{2}=\frac{\sigma_{u}^{2}}{\sum_{i=1}^{n}\left(x_{i}-\bar{x}\right)^{2}}
$$

- Replace $\sigma_{u}^{2}$ with estimate $s_{e}^{2}=\frac{1}{n-2} \sum_{i=1}^{n}\left(y_{i}-\widehat{y}_{i}\right)^{2}$.
- The estimated variance of $b_{2}$ is then

$$
\frac{s_{e}^{2}}{\sum_{i=1}^{n}\left(x_{i}-\bar{x}\right)^{2}} .
$$

- Taking the square root, the standard error of $b_{2}$ is

$$
\begin{aligned}
s e\left(b_{2}\right) & =\sqrt{\frac{s_{e}^{2}}{\sum_{i=1}^{n}\left(x_{i}-\bar{x}\right)^{2}}} \\
& =\frac{s_{e}}{\sqrt{\sum_{i=1}^{n}\left(x_{i}-\bar{x}\right)^{2}}}
\end{aligned}
$$

### Example: Computation of the Standard Error

- Artificial data on a sample of size five
- $(y, x)$ equals $(1,1),(2,2),(2,3),(2,4)$ and $(3,5)$.
- From chapter 5: $\widehat{y}=0.8+0.4 x$.
- so $\widehat{y}_{1}=1.2, \widehat{y}_{2}=1.6, \widehat{y}_{3}=2.0, \widehat{y}_{4}=2.4, \widehat{y}_{5}=2.8$.
- Standard error of the regression $s_{e}=\sqrt{.1333333}=0.365148$ since

$$
\begin{aligned}
s_{e}^{2} & =\frac{1}{n-2} \sum_{i=1}^{n}\left(y_{i}-\widehat{y}_{i}\right)^{2} \\
& =\frac{1}{3}\left\{(1-1.2)^{2}+(2-1.6)^{2}+(2-2)^{2}+(2-2.4)^{2}+(3-2.8)^{2}\right\} \\
& =0.13333
\end{aligned}
$$

- $\sum_{i=1}^{n}\left(x_{i}-\bar{x}\right)^{2}=10$ calculated earlier in computing $b_{2}$. So

$$
\operatorname{se}\left(b_{2}\right)^{2}=\frac{s_{e}^{2}}{\sum_{i=1}^{n}\left(x_{i}-\bar{x}\right)^{2}}=\frac{0.133333}{10}=0.0133333 .
$$

- Standard error of the slope $b_{2}$ is $\operatorname{se}\left(b_{2}\right)=\sqrt{0.013333}=0.115$.


### When is the Slope Coefficient Precisely Estimated?

- The standard error of $b_{2}$ is $s e\left(b_{2}\right)=\sqrt{\frac{s_{e}^{2}}{\sum_{i=1}^{n}\left(x_{i}-\bar{x}\right)^{2}}}$.
- Better precision $=$ smaller standard error occurs if
- 1. Model fits well ( $s_{e}^{2}$ is smaller)
- 2. Many observations (then $\sum_{i=1}^{n}\left(x_{i}-\bar{x}\right)^{2}$ is larger).
- 3. Regressors are widely scattered (then $\sum_{i=1}^{n}\left(x_{i}-\bar{x}\right)^{2}$ is larger).


### Normal Distribution and the Central Limit Theorem

- Under assumptions 1-4

$$
b_{2} \sim\left(\beta_{2}, \sigma_{b_{2}}^{2}\right)
$$

- The standardized variable

$$
\begin{aligned}
Z & =\frac{b_{2}-\beta_{2}}{\sigma_{b_{2}}} \\
& \sim(0,1) \text { by construction } \\
& \sim N(0,1) \text { as } n \rightarrow \infty \text { if a central limit theorem holds. }
\end{aligned}
$$

- In practice, $\sigma_{b_{2}}$ is unknown as error standard deviation $\sigma_{u}$ is unknown - this will lead to use of the $T$ distribution in chapter 7.


### Aside: The OLS Intercept Coefficient

- Under assumptions 1-2

$$
\mathrm{E}\left[b_{1}\right]=\beta_{1} .
$$

- Given assumptions 1-4

$$
\sigma_{b_{1}}^{2}=\operatorname{Var}\left[b_{1}\right]=\frac{\sigma_{u}^{2} \sum_{i=1}^{n} x_{i}^{2}}{n \sum_{i=1}^{n}\left(x_{i}-\bar{x}\right)^{2}} .
$$

- The standard error of $b_{2}$ is

$$
\operatorname{se}\left(b_{2}\right)=\sqrt{\frac{s_{e}^{2} \sum_{i=1}^{n} x_{i}^{2}}{n \sum_{i=1}^{n}\left(x_{i}-\bar{x}\right)^{2}}} .
$$

- And $Z=\left(b_{2}-\beta_{2}\right) / \sigma_{b_{2}}$ is $N(0,1)$ as $n \rightarrow \infty$.


### Summary for the OLS Slope Coefficient

A summary given assumptions 1-4 is the following.
(1) $y_{i}$ given $x_{i}$ has conditional mean $\beta_{1}+\beta_{2} x_{i}$ and conditional variance $\sigma_{u}^{2}$.
(2) Slope coefficient $b_{2}$ has mean $\beta_{2}$ and variance $\sigma_{b_{2}}^{2}=\sigma_{u}^{2} / \sum_{i=1}^{n}\left(x_{i}-\bar{x}\right)^{2}$.
(3) Standard error of $b_{2}$ is $s_{b_{2}}$ where $s e\left(b_{2}\right)^{2}=s_{e}^{2} / \sum_{i=1}^{n}\left(x_{i}-\bar{x}\right)^{2}$ and $s_{e}^{2}=\frac{1}{n-1} \sum_{i=1}^{n}\left(x_{i}-\bar{x}\right)^{2}$.
(4) $Z=\left(b_{2}-\beta_{2}\right) / \sigma_{b_{2}}$ has mean 0 and variance 1 .
(5) As sample size $n \rightarrow \infty, Z$ is standard normal distributed by the central limit theorem.

### Least Squares in Practice

- Assumptions 1-2 are essential for least squares to be unbiased and consistent.
- in particular assumption 2 rules out any correlation between $x$ and $u$
$\star$ e.g. rules out high $x$ being associated with high $u$
- we maintain these assumptions
- chapter 16 discusses failures
- chapter 17 has some possible solutions.
- Assumptions 3-4 can be relaxed
  - A crucial practical part of regression is choosing the correct variation of assumptions 3 and 4
  - This is necessary to get correct standard errors
  - And hence correct confidence intervals and hypothesis tests

- Chapters 7.7 and 12.1 provide methods


## 6.4 Estimators of Model Parameters

- Ideal properties of estimators were presented in Chapter 3.6 for estimation of the population mean.
- For centering
- unbiasedness (on average)
- consistency (almost perfect in infinitely large samples).
- For being best
- minimum variance among all possible correctly-centered estimators.
- Bottom line: Under assumptions 1-4 OLS is essentially the best estimator of $\beta_{1}$ and $\beta_{2}$.


### Unbiased Estimator

- Given assumptions 1-2

$$
\mathrm{E}\left[b_{2} \mid x_{1}, \ldots, x_{n}\right]=\beta_{2} .
$$

- $b_{2}$ is unbiased for $\beta_{2}$ (and $b_{1}$ is unbiased for $\beta_{1}$ )
- if we obtain many samples yielding many $b_{2}$ then on average $b_{2}=\beta_{2}$.
- Essentially we need sampling such that $\mathrm{E}\left[y_{i} \mid x_{i}\right]=\beta_{1}+\beta_{2} x_{i}$.


### Consistent Estimator

- A sufficient condition for a consistent estimator is that as $n \rightarrow \infty$
- any bias disappears and the variance goes to zero.
- So $b_{2}$ is consistent for $\beta_{2}$ as:
  - $b_{2}$ is unbiased for $\beta_{2}$ given assumptions 1-2
  - $\operatorname{Var}\left[b_{2}\right] \rightarrow 0$ as $n \rightarrow \infty$ given assumptions 1-4
  - Note: assumptions 3-4 can be relaxed and still get consistency

### Minimum Variance Estimator

- We want as precise an estimator as possible
- OLS is the best linear unbiased estimator (BLUE) of $\beta_{2}$ under assumptions 1-4
  - Lowest variance of all unbiased estimators that are a linear combination of the $y$'s
  - Recall $b_{2}=\sum_{i=1}^{n}\left(x_{i}-\bar{x}\right)\left(y_{i}-\bar{y}\right) / \sum_{i=1}^{n}\left(x_{i}-\bar{x}\right)^{2}=\sum_{i=1}^{n} w_{i} y_{i}$
  - So linear in $y_{i}$
- OLS is the best unbiased estimator (BUE) of $\beta_{2}$ if additionally $u$ is normally distributed
  - So lowest variance of all unbiased estimators
- OLS is the best consistent estimator (BUE) in standard settings under assumptions 1-4,
- it has smallest variance among consistent estimators.


### Some in-class Exercises

(1) Suppose we know that $y=8+5 x+u$ where $E[u \mid x]=0$. Give the conditional mean of $y$ given $x$ and the error term for the observation $(x, y)=(5,30)$.
(2) OLS regression of $y$ on $x$ on a large sample leads to slope coefficient equal to 10 with standard error 4. Provide an approximate $95 \%$ confidence interval for $\beta_{2}$ in the model $y=\beta_{1}+\beta_{2} x+u$.
(3) OLS regression of $y$ on $x$ on a large sample leads to slope coefficient equal to 20 with standard error 5 . Test at level 0.05 the claim that the population slope coefficient equals 8 .
(4) You are given the following $\sum_{i=1}^{27}\left(x_{i}-\bar{x}\right)^{2}=20$ and $\sum_{i=1}^{27}\left(y_{i}-\widehat{y}_{i}\right)^{2}=400$. Compute the standard error of the OLS slope coefficient under assumptions 1-4.
(5) Which of assumptions 1-4 ensure that OLS estimates are unbiased?

---

## Key Takeaways

**Population Model and Conditional Mean (Section 6.1):**
- The population regression model assumes E[y|x] = β₁ + β₂x, a linear conditional mean
- β₁ and β₂ are unknown population parameters; b₁ and b₂ are sample estimates
- The conditional mean E[Y|X=x] is the probability-weighted average of all y values for a given x
- This generalizes univariate analysis where E[Y] is constant to regression where E[y|x] varies with x
- Not all conditional means are linear—linearity is an assumption we impose
- The error term u = y - E[y|x] = y - (β₁ + β₂x) captures deviations from the population line
- Error term u is unobserved because β₁ and β₂ are unknown
- Crucial distinction: error u (unobserved, relative to population line) vs. residual e (observed, relative to fitted line)
- Assumption: E[u|x] = 0, meaning errors average to zero at each x value
- This assumption ensures the population line is indeed E[y|x] = β₁ + β₂x

**Error Variance and Homoskedasticity (Section 6.1 continued):**
- The variance Var[u|x] = σ²ᵤ measures variability of errors around the population line
- Greater error variance means greater noise, reducing precision of estimates
- Homoskedasticity assumption: Var[u|x] = σ²ᵤ is constant (doesn't vary with x)
- "Homoskedastic" comes from Greek: homos (same) + skedastic (scattering)
- Since u is the only source of randomness in y given x, we have Var[y|x] = Var[u|x] = σ²ᵤ
- This assumption can be (and often is) relaxed in practice
- Univariate: Yᵢ ~ (μ, σ²) with constant mean μ
- Regression: yᵢ|xᵢ ~ (β₁ + β₂x, σ²ᵤ) with mean varying with x but constant variance

**Sampling Experiments (Section 6.2):**
- Two types of sampling experiments demonstrate OLS properties
- Generated data: Create 400 samples from known model y = 1 + 2x + u with u ~ N(0,4)
- Finite population: Draw 400 samples from 1880 Census (1.06 million males aged 60-70)
- Key findings from both experiments: (1) Average of 400 slopes b₂ is close to true β₂ (unbiasedness)
- (2) Distribution of 400 slopes is approximately normal (CLT)
- (3) Similar results hold for intercept b₁
- Single sample: b₁ ≠ β₁ and b₂ ≠ β₂ due to sampling variability
- Multiple samples: Estimates vary across samples, but center on true parameters
- Census example: β₂ = -0.0109 (each year reduces labor force participation by 1.09 percentage points)
- 400 samples gave average slope -0.0115, close to true -0.0109

**OLS as a Random Variable (Section 6.3):**
- The OLS slope b₂ = Σ(xᵢ-x̄)(yᵢ-ȳ) / Σ(xᵢ-x̄)² varies across samples (it's a random variable)
- Under model yᵢ = β₁ + β₂xᵢ + uᵢ, algebra shows b₂ = β₂ + Σ(xᵢ-x̄)uᵢ / Σ(xᵢ-x̄)²
- Conditional on regressors xᵢ, the only source of randomness is errors uᵢ
- Properties of b₂ depend crucially on assumptions about uᵢ
- Data requirement: Must have variation in regressors (Σ(xᵢ-x̄)² > 0), otherwise cannot compute b₁ and b₂
- Need at least 3 observations for bivariate regression

**Four Core OLS Assumptions (Section 6.3 continued):**
- Assumption 1 (Correct model): yᵢ = β₁ + β₂xᵢ + uᵢ for all i
- Assumption 2 (Mean-zero error): E[uᵢ|xᵢ] = 0 for all i (no correlation between x and u)
- Assumption 3 (Homoskedasticity): Var[uᵢ|xᵢ] = σ²ᵤ for all i (constant error variance)
- Assumption 4 (Independence): uᵢ independent of uⱼ for all i ≠ j (no autocorrelation)
- Assumptions 1-2 are crucial for unbiasedness: ensure E[yᵢ|xᵢ] = β₁ + β₂xᵢ
- Assumptions 3-4 affect variance and standard errors, not bias
- Assumptions can be relaxed: 3-4 often relaxed in practice (use robust standard errors)
- Assumptions 1-2 essential; violations cause bias and inconsistency (Chapter 16)

**Mean and Variance of OLS Slope (Section 6.3 continued):**
- Given assumptions 1-2: E[b₂] = β₂ (unbiasedness)
- Given assumptions 1-4: Var[b₂] = σ²ᵤ / Σ(xᵢ-x̄)²
- Standard deviation of b₂: σ_b₂ = σᵤ / √[Σ(xᵢ-x̄)²]
- Variance of b₂ decreases with: (1) smaller σ²ᵤ (better model fit), (2) larger Σ(xᵢ-x̄)² (more observations or more scattered x)
- Proofs provided in Appendix C.1 for simpler case without intercept

**Estimating Error Variance (Section 6.3 continued):**
- σ²ᵤ is unknown, so estimate it using residuals
- Standard error of regression: s²ₑ = (1/(n-2)) Σ(yᵢ-ŷᵢ)² estimates σ²ᵤ
- Use (n-2) denominator (not n) because we estimated 2 coefficients, leaving (n-2) degrees of freedom
- This divisor ensures s²ₑ is unbiased for σ²ᵤ
- Root mean squared error: sₑ = √[s²ₑ] estimates σᵤ
- Example: With n=5, ŷ = 0.8 + 0.4x, we compute sₑ = 0.365

**Standard Error of OLS Slope (Section 6.3 continued):**
- Estimated variance of b₂: s²ₑ / Σ(xᵢ-x̄)² (replace unknown σ²ᵤ with estimate s²ₑ)
- Standard error of b₂: se(b₂) = sₑ / √[Σ(xᵢ-x̄)²]
- se(b₂) measures precision of b₂ as estimate of β₂
- Example calculation: With Σ(xᵢ-x̄)² = 10 and s²ₑ = 0.133, we get se(b₂) = 0.115

**Factors Affecting Precision (Section 6.3 continued):**
- Better precision (smaller se(b₂)) occurs when:
- 1. Model fits well (s²ₑ is smaller) - less noise around regression line
- 2. Many observations (Σ(xᵢ-x̄)² is larger) - more data reduces sampling variability
- 3. Regressors widely scattered (Σ(xᵢ-x̄)² is larger) - more variation in x provides more information
- Precision improves with √n, so need 4× observations to halve standard error
- Trade-off: Can't control regressor scatter in observational data, but can increase sample size

**Central Limit Theorem for OLS (Section 6.3 continued):**
- Under assumptions 1-4: b₂ ~ (β₂, σ²_b₂) where σ²_b₂ = σ²ᵤ / Σ(xᵢ-x̄)²
- Standardized variable: Z = (b₂ - β₂) / σ_b₂ has mean 0 and variance 1 by construction
- CLT: As n → ∞, Z ~ N(0,1) (approximately normal for large samples)
- This implies b₂ ~ N(β₂, σ²_b₂) for large n
- In practice, σ_b₂ is unknown (depends on unknown σᵤ)
- Replace σ_b₂ with se(b₂) leads to t distribution (Chapter 7)
- Normality justifies using normal-based inference for large samples

**Intercept Properties (Section 6.3 continued):**
- Under assumptions 1-2: E[b₁] = β₁ (unbiased)
- Under assumptions 1-4: Var[b₁] = σ²ᵤ Σx²ᵢ / [n Σ(xᵢ-x̄)²]
- Standard error of b₁: se(b₁) = √[s²ₑ Σx²ᵢ / (n Σ(xᵢ-x̄)²)]
- Intercept variance depends on Σx²ᵢ (sum of squared x values)
- If x values centered at 0, intercept more precisely estimated
- CLT applies: (b₁ - β₁) / σ_b₁ ~ N(0,1) as n → ∞

**Summary of OLS Properties (Section 6.3 continued):**
- (1) Conditional distribution: yᵢ|xᵢ has mean β₁ + β₂xᵢ and variance σ²ᵤ
- (2) Slope mean and variance: E[b₂] = β₂ and Var[b₂] = σ²ᵤ / Σ(xᵢ-x̄)²
- (3) Standard error: se(b₂)² = s²ₑ / Σ(xᵢ-x̄)² where s²ₑ = Σ(yᵢ-ŷᵢ)²/(n-2)
- (4) Standardized statistic: Z = (b₂ - β₂) / σ_b₂ has mean 0, variance 1
- (5) Normality: Z ~ N(0,1) as n → ∞ by CLT
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
- Under assumptions 1-2: E[b₂|x₁,...,xₙ] = β₂ (unbiased)
- If we obtain many samples, on average b₂ equals β₂
- Requires sampling such that E[yᵢ|xᵢ] = β₁ + β₂xᵢ
- Unbiasedness is a finite-sample property (holds for any sample size)
- Both b₁ and b₂ are unbiased under assumptions 1-2

**Consistent Estimator (Section 6.4 continued):**
- Sufficient condition for consistency: as n → ∞, bias → 0 and variance → 0
- b₂ is consistent for β₂ because:
  - (1) b₂ is unbiased (given assumptions 1-2)
  - (2) Var[b₂] = σ²ᵤ / Σ(xᵢ-x̄)² → 0 as n → ∞ (given assumptions 1-4)
- Consistency is an asymptotic property (behavior as sample size grows)
- Note: Can relax assumptions 3-4 and still get consistency (only need 1-2)
- Consistency means b₂ converges in probability to β₂

**Efficiency and BLUE (Section 6.4 continued):**
- Best Linear Unbiased Estimator (BLUE): OLS has minimum variance among all linear unbiased estimators under assumptions 1-4
- "Linear" means estimator is linear combination of y values: b₂ = Σwᵢyᵢ
- Gauss-Markov Theorem: OLS is BLUE under assumptions 1-4
- If additionally u is normally distributed: OLS is Best Unbiased Estimator (BUE)
  - Lowest variance among ALL unbiased estimators (not just linear ones)
- OLS is also best consistent estimator in standard settings
- Bottom line: Under assumptions 1-4, OLS is essentially the best estimator of β₁ and β₂

**Why OLS is Optimal:**
- OLS minimizes sum of squared residuals: min Σ(yᵢ - b₁ - b₂xᵢ)²
- This criterion leads to estimator that is unbiased, consistent, and efficient
- Alternative estimators (LAD, robust regression) may be better under specific violations
- But OLS is optimal baseline under standard assumptions
- Computational advantages: OLS has closed-form solution, easy to implement
- Well-understood statistical properties make inference straightforward

**Software Implementation:**
- Python: Use `statsmodels.OLS` or `scipy.stats.linregress` for OLS regression
- Generated data example uses random seed for reproducibility
- Visualization: scatter plots with fitted regression line show data and model
- Can compare population line vs. fitted line when population model known

---
