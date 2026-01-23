# Chapter 6: The Least Squares Estimator

- The sample leads to a fitted regression line $\widehat{y}=b_{1}+b_{2} x$
- But different samples will lead to different fitted regression lines
- Example: in a random sample individual earnings increase by 7% with an extra year of schooling
  - What can we say about the increase in the entire population?

- We suppose that there is an unknown population line $\beta_{1}+\beta_{2} x$
  - Then the regression slope $b_{2}$ is an estimate of $\beta_{2}$

- **This chapter:**
  - Distribution of the regression estimates $b_{1}$ and $b_{2}$

- **The subsequent chapter:**
  - Confidence intervals and hypothesis tests for the slope parameter $\beta_{2}$

- **Key regression output for statistical inference:**

| Variable | Coefficient | Standard Error | t statistic | p value | $95 \%$ conf. interval |  |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Size | 73.77 | 11.17 | 6.60 | 0.000 | 50.84 | 96.70 |
| Intercept | 115017.30 | 21489.36 | 5.35 | 0.000 | 70924.76 | 159109.8 |

- The standard error of Size is an estimate of the precision of $b_{2}$ as an estimate of $\beta_{2}$
  - We need to explain how this is obtained
  - Different assumptions lead to different standard errors
  - So important to go into details

- The remaining statistics are studied in Chapter 7:
  - The confidence interval for Size is one for $\beta_{2}$
  - The t statistic for Size is a test of $H_{0}: \beta_{2}=0$ against $H_{a}: \beta_{2} \neq 0$
  - i.e., is there any relationship between Size and Price?


## Outline

(1) Population and Sample
(2) Examples of Sampling from a Population
(3) Properties of the Least Squares Estimator
(4) Estimators of Model Parameters

Datasets: GENERATEDDATA, GENERATEDREGRESSIONS, CENSUSREGRESSIONS

### 6.1 Population Model: Conditional Mean of y given x

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


## Population Conditional Mean (continued)

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


## Error Term

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


## Error Term versus Residual - a crucial distinction

- $u$ is not observed - it is the difference between $y$ and the unknown population line $\beta_{1}+\beta_{2} \times$ (the solid line)
- $e$ is observed - it is the difference between $y$ and the known fitted line $b_{2}+b_{2} \times$ (the dashed line)
![](https://cdn.mathpix.com/cropped/1db1a0ef-9c44-414f-9671-ab8a889b52b7-08.jpg?height=449&width=516&top_left_y=397&top_left_x=75)
![](https://cdn.mathpix.com/cropped/1db1a0ef-9c44-414f-9671-ab8a889b52b7-08.jpg?height=445&width=480&top_left_y=399&top_left_x=712)


## Error Term is assumed to have mean zero

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

## Population Conditional Variance of y given x

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

## Summary

- The bottom line:
- Univariate analysis: $y_{1}, \ldots, y_{n}$ is a simple random sample with

$$
Y_{i} \sim\left(\mu, \sigma^{2}\right) .
$$

- Regression analysis: $\left(x_{1}, y_{1}\right), \ldots,\left(x_{n}, y_{n}\right)$ is a simple random sample that allows the mean to vary with $x$, so

$$
y_{i} \mid x_{i} \sim\left(\beta_{1}+\beta_{2} x, \sigma_{u}^{2}\right) .
$$

### 6.2 Examples of Sampling from a Population

- We consider two examples of sampling from a population
- regression generalizations of the two examples in chapter 4.
- 1. Generate by computer 400 samples from an explicit model $y=\beta_{1}+\beta_{2} x+u$.
- 2. Select 400 samples from a finite population - the U.S. 1880 Census for males aged 60-69 years.
- In both cases we run 400 regressions giving 400 estimates $b_{1}$ and $b_{2}$ and find
- the average of the 400 slopes $b_{2}$ is close to $\beta_{2}$
- the distribution of the 400 slopes $b_{2}$ is approximately normal
- similar results hold for the intercept $b_{1}$.


## Single Sample Generated from an Experiment

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

## Many Samples Generated from an Experiment

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


## Three Generated Samples yield three different lines

- Scatterplots and regression lines from three samples of size 30 intercepts and slopes vary across samples.

Sample 1
![](https://cdn.mathpix.com/cropped/1db1a0ef-9c44-414f-9671-ab8a889b52b7-16.jpg?height=282&width=348&top_left_y=424&top_left_x=84)

Sample 2
![](https://cdn.mathpix.com/cropped/1db1a0ef-9c44-414f-9671-ab8a889b52b7-16.jpg?height=282&width=346&top_left_y=424&top_left_x=463)

Sample 3
![](https://cdn.mathpix.com/cropped/1db1a0ef-9c44-414f-9671-ab8a889b52b7-16.jpg?height=287&width=349&top_left_y=423&top_left_x=839)

## 400 Generated Samples of Size 30

- 400 such samples were generated and fitted
- left panel: $\beta_{2}=2$ and average of 400 slopes equals 1.979.
- right panel: $\beta_{1}=1$ and average of 400 intercepts equals 1.039 .
- both histograms are approximately normal.
![](https://cdn.mathpix.com/cropped/1db1a0ef-9c44-414f-9671-ab8a889b52b7-17.jpg?height=402&width=529&top_left_y=407&top_left_x=89)

Generated data: 400 Intercepts
![](https://cdn.mathpix.com/cropped/1db1a0ef-9c44-414f-9671-ab8a889b52b7-17.jpg?height=372&width=529&top_left_y=436&top_left_x=654)

## Many Samples Generated from a Finite Population

- Data from the 1880 Census
- complete enumeration of the U.S. population in 1880.
- Relationship between
- $y=$ labforce $=$ labor force participation
$\star 1$ if in the labor force; 0 if not in the labor force
- and $x=$ age $=60$ to 70 years.
- Population is of size $1,058,475$ (men aged $60-70$ years)
- Population mean of labforce is 0.8945
- so $89.45 \%$ were in the labor force.


## Population Regression Line

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


## 400 Samples of Size 200

- Draw 400 samples of size 200 ; regress labforce on age in each sample
- large sample sizes as regression fit is poor: $R^{2} \simeq 0.01$.
- left panel: $\beta_{2}=-0.0109$ and average of 400 slopes is -0.0115
- right panel: $\beta_{1}=1.593$ and average of 400 intercepts is 1.636
- both histograms are approximately normal.
![](https://cdn.mathpix.com/cropped/1db1a0ef-9c44-414f-9671-ab8a889b52b7-20.jpg?height=405&width=533&top_left_y=416&top_left_x=87)

Census data: 400 Intercepts
![](https://cdn.mathpix.com/cropped/1db1a0ef-9c44-414f-9671-ab8a889b52b7-20.jpg?height=375&width=532&top_left_y=446&top_left_x=653)

### 6.3 Properties of the Least Squares Estimator

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


## Data Assumptions

- Always assume that there is variation in the regressors
- we rule out the case $x_{i}=\bar{x}$ for all $i$
- this ensures $\sum_{i=1}^{n}\left(x_{i}-\bar{x}\right)^{2}>0$.
- Otherwise cannot compute $b_{1}$ and $b_{2}$.
- Also at least 3 observations.


## Population Assumptions

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


## Mean and Variance of the OLS Slope Coefficient

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


## Estimate of the Error Variance

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

## Estimate of the Variance of the OLS Slope Coefficient

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

## Example: Computation of the Standard Error

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


## When is the Slope Coefficient Precisely Estimated?

- The standard error of $b_{2}$ is $s e\left(b_{2}\right)=\sqrt{\frac{s_{e}^{2}}{\sum_{i=1}^{n}\left(x_{i}-\bar{x}\right)^{2}}}$.
- Better precision $=$ smaller standard error occurs if
- 1. Model fits well ( $s_{e}^{2}$ is smaller)
- 2. Many observations (then $\sum_{i=1}^{n}\left(x_{i}-\bar{x}\right)^{2}$ is larger).
- 3. Regressors are widely scattered (then $\sum_{i=1}^{n}\left(x_{i}-\bar{x}\right)^{2}$ is larger).


## Normal Distribution and the Central Limit Theorem

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


## Aside: The OLS Intercept Coefficient

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


## Summary for the OLS Slope Coefficient

A summary given assumptions 1-4 is the following.
(1) $y_{i}$ given $x_{i}$ has conditional mean $\beta_{1}+\beta_{2} x_{i}$ and conditional variance $\sigma_{u}^{2}$.
(2) Slope coefficient $b_{2}$ has mean $\beta_{2}$ and variance $\sigma_{b_{2}}^{2}=\sigma_{u}^{2} / \sum_{i=1}^{n}\left(x_{i}-\bar{x}\right)^{2}$.
(3) Standard error of $b_{2}$ is $s_{b_{2}}$ where $s e\left(b_{2}\right)^{2}=s_{e}^{2} / \sum_{i=1}^{n}\left(x_{i}-\bar{x}\right)^{2}$ and $s_{e}^{2}=\frac{1}{n-1} \sum_{i=1}^{n}\left(x_{i}-\bar{x}\right)^{2}$.
(4) $Z=\left(b_{2}-\beta_{2}\right) / \sigma_{b_{2}}$ has mean 0 and variance 1 .
(5) As sample size $n \rightarrow \infty, Z$ is standard normal distributed by the central limit theorem.

## Least Squares in Practice

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


### 6.4 Estimators of Model Parameters

- Ideal properties of estimators were presented in Chapter 3.6 for estimation of the population mean.
- For centering
- unbiasedness (on average)
- consistency (almost perfect in infinitely large samples).
- For being best
- minimum variance among all possible correctly-centered estimators.
- Bottom line: Under assumptions 1-4 OLS is essentially the best estimator of $\beta_{1}$ and $\beta_{2}$.


## Unbiased Estimator

- Given assumptions 1-2

$$
\mathrm{E}\left[b_{2} \mid x_{1}, \ldots, x_{n}\right]=\beta_{2} .
$$

- $b_{2}$ is unbiased for $\beta_{2}$ (and $b_{1}$ is unbiased for $\beta_{1}$ )
- if we obtain many samples yielding many $b_{2}$ then on average $b_{2}=\beta_{2}$.
- Essentially we need sampling such that $\mathrm{E}\left[y_{i} \mid x_{i}\right]=\beta_{1}+\beta_{2} x_{i}$.


## Consistent Estimator

- A sufficient condition for a consistent estimator is that as $n \rightarrow \infty$
- any bias disappears and the variance goes to zero.
- So $b_{2}$ is consistent for $\beta_{2}$ as:
  - $b_{2}$ is unbiased for $\beta_{2}$ given assumptions 1-2
  - $\operatorname{Var}\left[b_{2}\right] \rightarrow 0$ as $n \rightarrow \infty$ given assumptions 1-4
  - Note: assumptions 3-4 can be relaxed and still get consistency

## Minimum Variance Estimator

- We want as precise an estimator as possible
- OLS is the best linear unbiased estimator (BLUE) of $\beta_{2}$ under assumptions 1-4
  - Lowest variance of all unbiased estimators that are a linear combination of the $y$'s
  - Recall $b_{2}=\sum_{i=1}^{n}\left(x_{i}-\bar{x}\right)\left(y_{i}-\bar{y}\right) / \sum_{i=1}^{n}\left(x_{i}-\bar{x}\right)^{2}=\sum_{i=1}^{n} w_{i} y_{i}$
  - So linear in $y_{i}$
- OLS is the best unbiased estimator (BUE) of $\beta_{2}$ if additionally $u$ is normally distributed
  - So lowest variance of all unbiased estimators
- OLS is the best consistent estimator (BUE) in standard settings under assumptions 1-4,
- it has smallest variance among consistent estimators.


## Key Stata Commands

```
* Generated data
clear
set obs 5
set rng kiss32 // uses old Stata random number generator
generate x = _n // set x to equal the observation number
generate Eygivenx = 1 + 2*x
set seed 123456
generate u = rnormal(0,2)
generate y = Eygivenx + u
list
regress y x
twoway (scatter y x) (lfit y x)
twoway (scatter y x) (lfit ytrue x)
```


## Some in-class Exercises

(1) Suppose we know that $y=8+5 x+u$ where $E[u \mid x]=0$. Give the conditional mean of $y$ given $x$ and the error term for the observation $(x, y)=(5,30)$.
(2) OLS regression of $y$ on $x$ on a large sample leads to slope coefficient equal to 10 with standard error 4. Provide an approximate $95 \%$ confidence interval for $\beta_{2}$ in the model $y=\beta_{1}+\beta_{2} x+u$.
(3) OLS regression of $y$ on $x$ on a large sample leads to slope coefficient equal to 20 with standard error 5 . Test at level 0.05 the claim that the population slope coefficient equals 8 .
(4) You are given the following $\sum_{i=1}^{27}\left(x_{i}-\bar{x}\right)^{2}=20$ and $\sum_{i=1}^{27}\left(y_{i}-\widehat{y}_{i}\right)^{2}=400$. Compute the standard error of the OLS slope coefficient under assumptions 1-4.
(5) Which of assumptions 1-4 ensure that OLS estimates are unbiased?

