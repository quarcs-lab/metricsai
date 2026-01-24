# Chapter 7: Statistical Inference for Bivariate Regression

## Learning Objectives

By the end of this chapter, you will be able to:

- Understand how the t-statistic for regression coefficients follows a T(n-2) distribution under standard assumptions
- Calculate and interpret standard errors for the OLS slope coefficient se(b₂)
- Construct confidence intervals for the population slope parameter β₂ using the formula b₂ ± t_{n-2,α/2} × se(b₂)
- Conduct tests of statistical significance to determine whether a regressor has any relationship with the dependent variable
- Perform two-sided hypothesis tests on β₂ using both p-value and critical value approaches
- Execute one-sided directional hypothesis tests when testing specific claims about parameter values
- Distinguish between statistical significance (based on t-statistics) and economic significance (based on coefficient magnitudes)
- Understand the four key OLS assumptions and their role in statistical inference
- Calculate and interpret heteroskedasticity-robust standard errors when assumption 3 (homoskedasticity) is violated
- Apply the relationship between confidence intervals and hypothesis tests to evaluate null hypotheses

---

## 7.1 Example: House Price and Size

- Key regression output for statistical inference with $n=29$ :

| Variable | Coefficient | Standard Error | t statistic | p value | $95 \%$ conf. interval |  |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Size | 73.77 | 11.17 | 6.60 | 0.000 | 50.84 | 96.70 |
| Intercept | 115017.30 | 21489.36 | 5.35 | 0.000 | 70924.76 | 159109.8 |

- $\widehat{\text { price }}=b_{1}+b_{2}$ size is an estimate of price $=\beta_{1}+\beta_{2}$ size .
- Coefficient of Size
- $b_{2}=73.77$ is least squares estimate of slope $\beta_{2}$
- Standard error of Size
- the estimated standard deviation of $b_{2}$
- the default standard error of $b_{2}$ equals 11.17.
- (later: alternative heteroskedastic-robust standard errors).


### Example (continued)

- We have with $n=29$ :

| Variable | Coefficient | Standard Error | t statistic | p value | $95 \%$ conf. interval |  |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Size | 73.77 | 11.17 | 6.60 | 0.000 | 50.84 | 96.70 |
| Intercept | 115017.30 | 21489.36 | 5.35 | 0.000 | 70924.76 | 159109.8 |

- Confidence interval for size
- $95 \%$ confidence interval for $\beta_{2}$
- is $b_{2} \pm t_{27, .025} \times \operatorname{se}\left(b_{2}\right)=(50.84,96.70)$.
- t statistic of Size tests whether there is any relationship
- is for test of $H_{0}: \beta_{2}=0$ against $H_{a}: \beta_{2} \neq 0$
- in general $t=($ estimate- hypothesized value $) /$ standard error
- $t_{2}=b_{2} / \operatorname{se}\left(b_{2}\right)=73.77 / 11.17=6.60$.
- p value of Size
- is p -value for a two sided test
- $p_{2}=\operatorname{Pr}\left[\left|T_{27}\right|>|6.60|\right]=0.00$.


## 7.2 The t Statistic

- The statistical inference problem
- Sample: $\hat{y}=b_{1}+b_{2} \times$ where $b_{1}$ and $b_{2}$ are least squares estimates
- Population: $\mathrm{E}[y \mid x]=\beta_{1}+\beta_{2} x$ and $y=\beta_{1}+\beta_{2} x+u$.
- Estimators: $b_{1}$ and $b_{2}$ are estimators of $\beta_{1}$ and $\beta_{2}$.
- Goal
- inference on the slope parameter $\beta_{2}$.
- This is based on a $T(n-2)$ distributed statistic

$$
T=\frac{\text { estimate }- \text { parameter }}{\text { standard error }}=\frac{b_{2}-\beta_{2}}{\operatorname{se}\left(b_{2}\right)} \sim T(n-2) .
$$

### Why use the T(n-2) Distribution?

- Make assumptions 1-4 given in the next slide.
- then $\operatorname{Var}\left[b_{2}\right]=\sigma_{u}^{2} / \sum_{i=1}^{n}\left(x_{i}-\bar{x}\right)^{2}$.
- But we don't know $\sigma_{u}^{2}$
- we replace it with the estimate $s_{e}^{2}=\frac{1}{n-2} \sum_{i=1}^{n}\left(y_{i}-\widehat{y}_{i}\right)^{2}$.
- This leads to noise in $\left\{s e\left(b_{2}\right)\right\}^{2}=s_{e}^{2} / \sum_{i=1}^{n}\left(x_{i}-\bar{x}\right)^{2}$
- so the statistic $T=\left(b_{2}-\beta_{2}\right) / s e\left(b_{2}\right)$ is better approximated by $T(n-2)$ than by $N(0,1)$.
- The $T(n-2)$ distribution
- is the exact distribution if additionally the errors $u_{i}$ are normally distributed
- otherwise it is an approximation, one that computer packages use.


### Model Assumptions

- Data assumption is that there is variation in the sample regressors so that $\sum_{i=1}^{n}\left(x_{i}-\bar{x}\right)^{2}=0$.
- Population assumptions 1-4
- 1. The population model is $y=\beta_{1}+\beta_{2} x+u$.
- 2. The error has mean zero conditional on $\mathbf{x}:\left[u_{i} \mid x_{i}\right]=0$.
- 3. The error has constant variance conditional on $\mathbf{x}$ : $\operatorname{Var}\left[u_{i} \mid x_{i}\right]=\sigma_{u}^{2}$.
- 4. The errors for different observations are statistically independent: $u_{i}$ is independent of $u_{j}$.
- Assumptions 1-2 imply a linear conditional mean and yield unbiased estimators

$$
\mathrm{E}[y \mid x]=\beta_{1}+\beta_{2} x .
$$

- Additional assumptions 3-4 yield the variance of estimators.


## 7.3 Confidence Interval for the Slope Parameter

- Recall: A 95 percent confidence interval is approximately

$$
\text { estimate } \pm 2 \times \text { standard error }
$$

- here a $95 \%$ confidence interval is $b_{2} \pm t_{n-2 ; .025} \times s e\left(b_{2}\right)$.
- A $100(1-\alpha)$ percent confidence interval for $\beta_{2}$ is

$$
b_{2} \pm t_{n-2, \alpha / 2} \times \operatorname{se}\left(b_{2}\right),
$$

where

- $b_{2}$ is the slope estimate
- $\operatorname{se}\left(b_{2}\right)$ is the standard error of $b_{2}$
- $t_{n-2 ; \alpha / 2}$ is the critical value from the T(n-2) distribution.


### What Level of Confidence?

- There is no best choice of confidence level
- most common choice is 95\% (or 90\% or 99\%)
- Interpretation
- the calculated $95 \%$ confidence interval for $\beta_{2}$ will correctly include $\beta_{2} 95 \%$ of the time
- if we had many samples and in each sample formed a $95 \%$ confidence interval, then $95 \%$ of these confidence intervals will include the true unknown $\beta_{2}$.


### Example: House Price and Size

- For regress house price on house size a $95 \%$ confidence interval is

$$
\begin{aligned}
& b_{2} \pm t_{n-2, \alpha / 2} \times \operatorname{se}\left(b_{2}\right) \\
= & 73.77 \pm t_{27, .025} \times 11.17 \\
= & 73.77 \pm 2.052 \times 11.17 \\
= & 73.77 \pm 22.93 \\
= & (50.84,96.70) .
\end{aligned}
$$

- This is directly given in computer output from regression.


## 7.4 Tests of Statistical Significance

- A regressor $x$ has no relationship with $y$ if $\beta_{2}=0$.
- A test of "statistical significance" is a two-sided test of whether $\beta_{2}=0$. So test

$$
H_{0}: \beta_{2}=0 \text { against } \quad H_{a}: \beta_{2} \neq 0 .
$$

- Test statistic is then

$$
t=\frac{b_{2}}{\operatorname{se}\left(b_{2}\right)} \sim T(n-2)
$$

- Reject if $|t|$ is large as then $\left|b_{2}\right|$ is large
- How large?
- Large enough that the value of $|t|$ is a low probability event.
- Use either p value approach or critical value approach
- reject at level 0.05 if $p=\operatorname{Pr}\left\{\left|T_{n-2}\right|>|t|\right]<0.05$
- or equivalently reject at level 0.05 if $|t|>c=t_{n-2 ; .025}$.
- This method generalizes to other formulas for $\operatorname{se}\left(b_{2}\right)$.


### Example: House Price and Size

- For regress house price on house size with $n=29$

$$
t=\frac{b_{2}}{s e\left(b_{2}\right)}=\frac{73.77}{11.17}=6.60
$$

- $p=\operatorname{Pr}\left[\left|T_{n-2}\right|>|t|\right]=\operatorname{Pr}\left[\left|T_{27}\right|>6.60\right]=0.000$
- so reject $H_{0}: \beta_{2}=0$ at significance level 0.05 as $p<0.05$.
- $c=t_{n-2 ; .025}=t_{27, .025}=2.052$
- so reject $H_{0}$ at significance level 0.05 as $|t|=6.60>c$.
- Conclude that house size is statistically significant at level 0.05 .


### Economic Significance versus Statistical Significance

- A regressor is of economic significance if its coefficient is of large enough value for it to matter in practice
- economic significance depends directly on $b_{2}$ and the context
- By contrast, statistical significance depends directly on $t$ which is the ratio $b_{2} / \operatorname{se}\left(b_{2}\right)$.
- With large samples $s e\left(b_{2}\right) \rightarrow 0$ as $n \rightarrow \infty$
- so we may find statistical significance
- even if $b_{2}$ is so small that it is of little economic significance.


### Tests based on the Correlation Coefficient

- An alternative way to measure statistical significance, used in many social sciences, uses the correlation coefficient $\left|r_{x y}\right|$.
- Then reject the null hypothesis of no association if $\left|r_{x y}\right|$ is sufficiently large
- this gives similar results to tests based on $t=b_{2} / s e\left(b_{2}\right)$ if default standard errors are used.
- Weaknesses of tests using the correlation coefficient
- this method cannot relax assumptions 3-4
- this method cannot be used if we wish to add additional regressors
- and it tells little about economic significance.


## 7.5 Two-sided Hypothesis Tests

- A two-sided test on the slope coefficient is a test of

$$
H_{0}: \beta_{2}=\beta_{2}^{*} \quad \text { against } \quad H_{a}: \beta_{2} \neq \beta_{2}^{*} .
$$

- Use $t$-statistic where $\beta_{2}=\beta_{2}^{*}$. So compute

$$
t=\frac{b_{2}-\beta_{2}^{*}}{\operatorname{se}\left(b_{2}\right)} \sim T(n-2) .
$$

- Reject if $|t|$ is large as then $\left|b_{2}-\beta_{2}^{*}\right|$ is large
- How large?
  - Large enough that such a large $|t|$ is a low probability event
- Use either p value approach or critical value approach.


### Example: House Price and Size

- For house price example with $\beta_{2}^{*}=90$

$$
t=\frac{b_{2}-90}{\operatorname{se}\left(b_{2}\right)}=\frac{73.77-90}{11.17}=-1.452 .
$$

- p -value approach
- $p=\operatorname{Pr}\left[\left|T_{27}\right|>|-1.452|=0.158\right.$.
- do not reject $H_{0}$ at level 0.05 as $p=0.158>0.05$.
- Critical value approach at level 0.05 :
- $c=t_{27 ; .025}=2.052$.
- do not reject $H_{0}$ at level 0.05 as $|t|=1.452<c=2.052$.
- In either case we do not reject $H_{0}: \beta_{2}=90$ against $H_{a}: \beta_{2} \neq 90$ at level 0.05.
- conclude that house price does not increase by $\$ 90$ per square foot.
- p-value approach: Compute $p=\operatorname{Pr}\left[\left|T_{n-2}\right|>|t|\right]$.
- critical value approach: compute $c$ so that reject if $|t|>c$.
![](https://cdn.mathpix.com/cropped/07ae1b4d-3d81-4f56-a70c-1c6790682a1f-18.jpg?height=423&width=573&top_left_y=323&top_left_x=61)

Two-sided test: critical value approach
![](https://cdn.mathpix.com/cropped/07ae1b4d-3d81-4f56-a70c-1c6790682a1f-18.jpg?height=391&width=580&top_left_y=357&top_left_x=647)

### Rejection using p-values

- p-value approach (at level $\alpha=0.05$ )
- Assume that $\beta_{2}=\beta_{2}^{*}$, i.e. $H_{0}$ is true.
- Obtain the p -value
  - The probability (or significance level) of observing a $\left|T_{n-2}\right| \geq|t|$, where this probability is calculated under the assumption that $\beta_{2}=\beta_{2}^{*}$
- If $p<0.05$ then reject $H_{0}$
  - Reason: there was less than .05 chance of observing our $t$, given $\beta_{2}=\beta_{2}^{*}$

### Rejection using Critical values

- Critical value approach (at level $\alpha=0.05$ )
- Assume that $\beta_{2}=\beta_{2}^{*}$, i.e. $H_{0}$ is true.
- Find the critical value
  - The value $c$ such that $\operatorname{Pr}\left[\left|T_{n-2}\right| \geq c\right]=0.05$
- If $|t|>c$ then reject $H_{0}$
  - Reason: there was less than .05 chance of observing our $t$, given $\beta_{2}=\beta_{2}^{*}$


### Relationship of Tests to Confidence Interval

- For a two-sided test of $H_{0}: \beta_{2}=\beta_{2}^{*}$
- if the null hypothesis value $\beta_{2}^{*}$ falls inside the $100(1-\alpha)$ percent confidence interval then do not reject $H_{0}$ at significance level $\alpha$.
- otherwise reject $H_{0}$ at significance level $\alpha$.
- House example
- $95 \%$ confidence interval for $\beta_{2}$ is $(50.84,96.70)$
- reject $H_{0}: \beta_{2}=0$ at level 0.05 as the $95 \%$ confidence interval does not include 0 .


## 7.6 One-sided Directional Hypothesis Tests

- One-sided test on the slope coefficient is a test of

Upper one-tailed alternative $H_{0}: \beta_{2} \leq \beta_{2}^{*}$ against $H_{a}: \beta_{2}>\beta_{2}^{*}$
Lower one-tailed alternative $H_{0}: \beta_{2} \geq \beta_{2}^{*}$ against $H_{a}: \beta_{2}<\beta_{2}^{*}$

- The statement being tested is specified to be the alternative hypothesis.
- Use same t-statistic as in two-sided case. So

$$
t=\frac{b_{2}-\beta_{2}^{*}}{\operatorname{se}\left(b_{2}\right)} \sim T(n-2) .
$$

- What will differ is the rejection region
- For $H_{0}: \beta_{2} \leq \beta_{2}^{*}$ against $H_{a}: \beta_{2}>\beta_{2}^{*}$ reject in the right tail

$$
\star p=\operatorname{Pr}\left[T_{n-2}>t\right]
$$

- For $H_{0}: \beta_{2} \geq \beta_{2}^{*}$ against $H_{a}: \beta_{2}<\beta_{2}^{*}$ reject in the left tail

$$
\star p=\operatorname{Pr}\left[T_{n-2}<t\right] .
$$

### Example: House Price and Size

- House price example suppose claim is that house price rises by less than $\$ 90$ per square foot, i.e. $\beta_{2}<90$.
- Test $H_{0}: \beta_{2} \geq 90$ against $H_{a}: \beta_{2}<90$ (lower tailed alternative).

$$
t=\frac{b_{2}-90}{\operatorname{se}\left(b_{2}\right)}=\frac{73.77-90}{11.17}=-1.452
$$

- p -value approach:
- $p=\operatorname{Pr}\left[T_{27}<t\right]=\operatorname{Pr}\left[T_{27}<-1.452\right]$
$=\operatorname{Pr}\left[T_{27}>1.452\right]=$ ttail $(27,1.452)=0.079<0.05$.
$\star$ where we have used the symmetry of the $t$ distribution.
- Critical value approach at level 0.05 :
- $c=-t_{27, .05}=-$ invttail $(27, .05)=-1.70$ and $t \nless-1.70$.
- In either case we do not reject $H_{0}: \beta_{2} \geq 90$ at significance level 0.05.
- At level 0.05 there is not enough evidence to support the claim
- note that the claim would be supported if we tested at level 0.10 .


### Computer generated t -statistic

- Computer gives a $t$-statistic
- this is $t=b_{2} / s e\left(b_{2}\right)$
- suitable for testing $\beta_{2}=0$.
- Computer gives a $p$-value
- this is for a two-sided test of $H_{0}: \beta_{2}=0$ against $H_{a}: \beta_{2} \neq 0$.
- For a one-sided test of statistical significance
- if $b_{2}$ is of the expected sign then halve the printed p -value.
- if $b_{2}$ is not of the expected sign then reject since $p>0.5$
- Example: if expect $\beta_{2}>0$ then upper tailed alternative test
- test $H_{0}: \beta_{2} \leq 0$ against $H_{a}: \beta_{2}>0$ at level . 05
- if $b_{2}>0$ then halve the printed p value and reject $H_{0}$ if this is less than .05
- if $b_{2}<0$ we will not reject $H_{0}$ i.e. conclude $\beta_{2}$ is not greater than zero.


## 7.7 Robust Standard Errors

- Default standard errors (and associated t statistics, p values and confidence intervals) make assumptions 1-4
- called default because this is what computer automatically computes
- Robust standard errors
- Keep assumptions 1-2
- Relax assumptions 3-4 in three common ways depending on data type
- Are commonly-used in practice.
- In each case get an alternative formula for $s e\left(b_{2}\right)$, say $s e_{\text {rob }}\left(b_{2}\right)$
- Then base inference on

$$
t=\frac{b_{2}-\beta_{2}}{s e_{r o b}\left(b_{2}\right)}
$$

### Heteroskedastic Robust Standard Errors

- Relax assumption 3 that all errors have the same variance
- called the assumption of homoskedastic errors.
- Instead allow $\operatorname{Var}\left[u_{i} \mid \mathbf{x}_{i}\right]=\sigma_{i}^{2}$ which varies with $i$
- called heteroskedastic errors.
- This is the standard assumption in modern econometrics.
- Then the heteroskedasticity-robust standard error for $b_{2}$ is

$$
\operatorname{se}_{\text {het }}\left(b_{2}\right)=\frac{\sqrt{\sum_{i=1}^{n} e_{i}^{2}\left(x_{i}-\bar{x}\right)^{2}}}{\sum_{i=1}^{n}\left(x_{i}-\bar{x}\right)^{2}} \neq \frac{s_{e}}{\sqrt{\sum_{i=1}^{n}\left(x_{i}-\bar{x}\right)^{2}}}
$$

- Then $t=\left(b_{2}-\beta_{2}\right) /$ se $_{\text {het }}\left(b_{2}\right)$ is viewed as $T(n-2)$ distributed.


### Example: House Price and Size

- For the house price and size example
- Default standard errors
  - 11.17 and 21,489 for the slope and intercept
- Heteroskedastic-robust standard errors
  - 11.33 and 20,928 for the slope and intercept

- Confidence interval using heteroskedastic-robust standard errors
- $73.77 \pm t_{27, .025} \times 11.333=(50.33,97.02)$ compared t0 $(50.84,96.70)$
- Test $H_{0}: \beta_{2}=0$ against $H_{a}: \beta_{2} \neq 0$

$$
t=\frac{b_{2}}{s e\left(b_{2}\right)}=\frac{73.77-0}{11.33}=6.51 \text { compared to } 6.60
$$

### Simulation Example of Heteroskedastic Errors

- Generate 100 observations as follows
- size varies from 1700 to 3700 plus some random noise
- price $=11500+74^{*}$ size + zero-mean error
- (1) error is homoskedastic $u_{i} \sim N\left(0,23500^{2}\right)$
- (2) error is heteroskedastic $u_{i} \sim \frac{\left(\text { size }_{i}-1700\right)}{1400} \times N\left(0,23500^{2}\right)$
  - This error has variance $\left\{\frac{\left(\text { size }_{i}-1700\right)}{1400}\right\}^{2} \times 23500^{2}$ that differs across $i$


### Simulation Example (continued)

- First panel: homoskedastic errors are evenly distributed around the regression line.
- Second panel: heteroskedastic errors scattering around the regression line varies with the level of the regressor
- in this case increasing with regressor size.

Homoskedastic errors
![](https://cdn.mathpix.com/cropped/07ae1b4d-3d81-4f56-a70c-1c6790682a1f-29.jpg?height=381&width=517&top_left_y=461&top_left_x=103)

Heteroskedastic errors
![](https://cdn.mathpix.com/cropped/07ae1b4d-3d81-4f56-a70c-1c6790682a1f-29.jpg?height=375&width=513&top_left_y=463&top_left_x=670)

### Other Robust Standard Errors

- For time series data where model errors may be correlated over time
- use HAC robust.
- For data in clusters (or groups) where errors are correlated within cluster but are uncorrelated across clusters
- people in villages, students in schools, individuals in families,...
- panel data on many individuals over time
- use cluster robust.
- These robust standard errors are presented in chapter 12.1.
- An essential part of any regression analysis is knowing which particular robust standard error method should be used.


---

## Key Takeaways

**Example and Regression Output (Section 7.1):**
- Regression output provides key information for statistical inference: coefficients, standard errors, t-statistics, p-values, and confidence intervals
- House price example: regressing price on size with n=29 gives b₂ = 73.77, se(b₂) = 11.17
- The coefficient b₂ = 73.77 estimates the population slope β₂ (price increase per square foot)
- Standard error se(b₂) = 11.17 is the estimated standard deviation of b₂, measuring its precision
- The 95% confidence interval (50.84, 96.70) provides a range of plausible values for β₂
- The t-statistic t = 6.60 tests whether size has any relationship with price
- The p-value 0.000 indicates strong evidence against the null hypothesis H₀: β₂ = 0
- Larger standard errors indicate less precision; smaller standard errors indicate more precision

**The t-Statistic and Its Distribution (Section 7.2):**
- Statistical inference uses the t-statistic: T = (b₂ - β₂)/se(b₂) which follows a T(n-2) distribution
- The sample regression ŷ = b₁ + b₂x estimates the population relationship E[y|x] = β₁ + β₂x
- Under assumptions 1-4, the t-statistic follows the T(n-2) distribution (n-2 degrees of freedom for bivariate regression)
- We use T(n-2) instead of N(0,1) because we estimate the error variance σ²ᵤ with s²ₑ
- Replacing unknown σ²ᵤ with estimate s²ₑ introduces additional variability captured by the t distribution
- The T(n-2) distribution has fatter tails than N(0,1), accounting for estimation uncertainty
- T(n-2) is the exact distribution if errors are normally distributed; otherwise it's an approximation
- As sample size increases, T(n-2) converges to N(0,1)

**Four Key OLS Assumptions (Section 7.2):**
- Assumption 1 (Correct model): The population model is y = β₁ + β₂x + u
- Assumption 2 (Mean-zero error): E[uᵢ|xᵢ] = 0 for all i (errors uncorrelated with regressor)
- Assumption 3 (Homoskedasticity): Var[uᵢ|xᵢ] = σ²ᵤ for all i (constant error variance)
- Assumption 4 (Independence): uᵢ is independent of uⱼ for all i ≠ j (no autocorrelation)
- Assumptions 1-2 are crucial: they imply E[y|x] = β₁ + β₂x and yield unbiased estimators
- Assumptions 3-4 affect variance calculations and standard errors but not bias
- Data assumption: there must be variation in regressors, Σ(xᵢ-x̄)² > 0
- These assumptions can be relaxed using robust standard errors (Section 7.7)

**Confidence Intervals for β₂ (Section 7.3):**
- A 100(1-α)% confidence interval for β₂ is: b₂ ± t_{n-2,α/2} × se(b₂)
- Approximate 95% CI: b₂ ± 2 × se(b₂) (since t_{n-2,0.025} ≈ 2 for moderate to large n)
- The critical value t_{n-2,α/2} satisfies Pr[|T_{n-2}| ≤ t_{n-2,α/2}] = 1 - α
- Common confidence levels: 90% (α=0.10), 95% (α=0.05), 99% (α=0.01)
- Interpretation: if we constructed 95% CIs for infinite samples, 95% would contain the true β₂
- We have only one sample, so we're "95% confident" our particular interval contains β₂
- House price example: 95% CI = 73.77 ± 2.052 × 11.17 = (50.84, 96.70)
- Wider intervals provide more confidence; narrow intervals provide more precision
- There's no single "best" confidence level, though 95% is conventional

**Tests of Statistical Significance (Section 7.4):**
- A test of statistical significance tests H₀: β₂ = 0 against H_a: β₂ ≠ 0 (two-sided)
- If β₂ = 0, then x has no linear relationship with y
- Test statistic: t = b₂/se(b₂) ~ T(n-2) under H₀
- Reject H₀ if |t| is large (evidence that b₂ is far from 0)
- P-value approach: reject at level α if p = Pr[|T_{n-2}| > |t|] < α
- Critical value approach: reject at level α if |t| > c where c = t_{n-2,α/2}
- Both approaches give identical conclusions
- House price example: t = 73.77/11.17 = 6.60, p = 0.000 < 0.05 → reject H₀
- Conclude that house size is statistically significant at the 5% level
- Computer output typically reports t-statistics and p-values for H₀: β₂ = 0

**Economic vs. Statistical Significance (Section 7.4):**
- Statistical significance: whether coefficient differs from zero (based on t-statistic)
- Economic significance: whether coefficient is large enough to matter in practice (based on b₂ magnitude and context)
- A coefficient can be statistically significant but economically insignificant (small b₂, large sample)
- With large samples, se(b₂) → 0 as n → ∞, so even tiny coefficients become statistically significant
- Always assess both: statistical significance tells us if an effect exists; economic significance tells us if it matters
- Example: b₂ = 0.0001 might be highly significant (p < 0.001) in large sample but economically meaningless
- Context determines economic significance: $1 price increase per square foot is meaningful for houses

**Tests Using Correlation Coefficient (Section 7.4):**
- Alternative approach: reject H₀ if correlation coefficient |r_{xy}| is sufficiently large
- Gives similar results to t-tests when using default standard errors
- Weaknesses: (1) cannot relax assumptions 3-4, (2) cannot extend to multiple regression, (3) tells little about economic significance
- Regression-based t-tests are more flexible and informative
- Prefer t-tests over correlation-based tests in econometric practice

**Two-Sided Hypothesis Tests (Section 7.5):**
- General two-sided test: H₀: β₂ = β₂* against H_a: β₂ ≠ β₂*
- Test statistic: t = (b₂ - β₂*)/se(b₂) ~ T(n-2) under H₀
- Reject if |t| is large (b₂ is far from hypothesized value β₂*)
- P-value: p = Pr[|T_{n-2}| > |t|]
- Critical value: c = t_{n-2,α/2}
- Reject at level α if p < α or equivalently if |t| > c
- House price example testing β₂ = 90: t = (73.77-90)/11.17 = -1.452, p = 0.158 > 0.05 → do not reject
- Cannot conclude that price increases by $90 per square foot
- Two tails used because alternative includes both β₂ > β₂* and β₂ < β₂*

**Relationship Between Tests and Confidence Intervals (Section 7.5):**
- For two-sided test of H₀: β₂ = β₂* at significance level α:
- If β₂* falls inside the 100(1-α)% confidence interval → do not reject H₀
- If β₂* falls outside the 100(1-α)% confidence interval → reject H₀
- This provides a visual way to test hypotheses using confidence intervals
- House price example: 95% CI is (50.84, 96.70); 0 is not in this interval → reject H₀: β₂ = 0
- The value 90 is in the interval → do not reject H₀: β₂ = 90
- This equivalence holds because both are based on the same t distribution

**One-Sided Hypothesis Tests (Section 7.6):**
- Upper one-tailed test: H₀: β₂ ≤ β₂* against H_a: β₂ > β₂* (claim β₂ is greater than β₂*)
- Lower one-tailed test: H₀: β₂ ≥ β₂* against H_a: β₂ < β₂* (claim β₂ is less than β₂*)
- The claim being tested is specified as the alternative hypothesis (requires strong evidence to support)
- Same t-statistic as two-sided: t = (b₂ - β₂*)/se(b₂)
- Different rejection regions: only one tail used
- Upper tail: reject if t > c where c = t_{n-2,α} and p = Pr[T_{n-2} > t]
- Lower tail: reject if t < -c where c = t_{n-2,α} and p = Pr[T_{n-2} < t]
- Note: critical value is t_{n-2,α} not t_{n-2,α/2} (one tail not two)
- House price example testing H₀: β₂ ≥ 90 vs. H_a: β₂ < 90: t = -1.452, p = Pr[T₂₇ < -1.452] = 0.079 > 0.05 → do not reject
- Not enough evidence to support claim that β₂ < 90 at 5% level (but would reject at 10% level)

**Using Computer Output for One-Sided Tests (Section 7.6):**
- Computer reports t = b₂/se(b₂) and p-value for two-sided test of H₀: β₂ = 0
- For one-sided test of statistical significance:
- If b₂ has expected sign → halve the printed p-value
- If b₂ has unexpected sign → do not reject (p > 0.5)
- Example: expect β₂ > 0, computer gives two-sided p = 0.04
  - If b₂ > 0: one-sided p = 0.04/2 = 0.02 < 0.05 → reject H₀: β₂ ≤ 0
  - If b₂ < 0: do not reject H₀: β₂ ≤ 0 (wrong sign)
- This shortcut only works for tests of H₀: β₂ = 0

**Robust Standard Errors Overview (Section 7.7):**
- Default standard errors assume all four OLS assumptions 1-4
- Robust standard errors keep assumptions 1-2 but relax assumptions 3-4
- Robust SEs are commonly used in modern econometric practice
- They provide alternative formula for se(b₂), denoted se_{rob}(b₂)
- Base inference on t = (b₂ - β₂)/se_{rob}(b₂) using T(n-2) distribution
- Three main types: heteroskedasticity-robust, HAC robust (time series), cluster-robust (grouped data)
- Choice of robust SE method depends on data structure and likely violations of assumptions

**Heteroskedasticity-Robust Standard Errors (Section 7.7):**
- Relax assumption 3: allow error variance to vary across observations
- Homoskedastic errors: Var[uᵢ|xᵢ] = σ²ᵤ (constant) - Assumption 3
- Heteroskedastic errors: Var[uᵢ|xᵢ] = σ²ᵢ (varies with i) - relaxed assumption
- Heteroskedasticity is the standard assumption in modern econometrics
- Heteroskedasticity-robust SE: se_{het}(b₂) = √[Σeᵢ²(xᵢ-x̄)²] / Σ(xᵢ-x̄)²
- This differs from default SE: se(b₂) = sₑ / √[Σ(xᵢ-x̄)²]
- Robust SEs account for different error variances across observations
- Inference proceeds using t = (b₂ - β₂)/se_{het}(b₂) ~ T(n-2)

**Heteroskedasticity Example (Section 7.7):**
- House price example with default vs. robust SEs:
  - Default SE: 11.17 for slope, 21,489 for intercept
  - Heteroskedastic-robust SE: 11.33 for slope, 20,928 for intercept
- 95% CI using robust SEs: 73.77 ± 2.052 × 11.33 = (50.33, 97.02) vs. default (50.84, 96.70)
- t-statistic using robust SEs: t = 73.77/11.33 = 6.51 vs. default t = 6.60
- In this example, robust and default SEs are similar (both lead to same conclusion)
- Simulation example shows heteroskedastic errors have variance increasing with regressor level
- Homoskedastic errors are evenly distributed around regression line
- Heteroskedastic errors show increasing scatter as x increases

**Other Types of Robust Standard Errors (Section 7.7):**
- HAC robust (Heteroskedasticity and Autocorrelation Consistent): for time series data where errors may be correlated over time
- Cluster-robust: for data in groups where errors are correlated within cluster but uncorrelated across clusters
- Examples of clustered data: people in villages, students in schools, individuals in families, panel data (individuals over time)
- Chapter 12.1 provides details on these robust SE methods
- Essential to know which robust SE method is appropriate for your data structure
- Using wrong SE method leads to incorrect inference (wrong confidence intervals and hypothesis test conclusions)

**Software Implementation:**
- Python/R: Standard regression packages provide options for default and heteroskedasticity-robust standard errors
- Confidence level can be adjusted (e.g., 99% instead of default 95%)
- Hypothesis tests can be conducted for any null hypothesis value (e.g., H₀: β₂ = 90)
- Dataset: AED_HOUSE.DTA contains house price and size data with n=29

**General Principles:**
- Always assess both statistical and economic significance
- Confidence intervals provide more information than hypothesis tests alone (show range of plausible values)
- Two-sided tests are standard; one-sided tests should only be used when directionality is theoretically justified
- Modern practice: use robust standard errors by default (especially heteroskedasticity-robust)
- The choice of robust SE method depends on data structure (cross-section, time series, panel, clustered)
- Statistical significance with small samples requires larger |t| values (fatter tails of t distribution)
- As sample size increases, statistical significance becomes easier to achieve (se(b₂) → 0)

---

### Some in-class Exercises

(1) We obtain fitted model $\hat{y}=\underset{(1.5)}{3.0}+\underset{(2.0)}{5.0} \times x, R^{2}=0.32, s_{e}=4.0$, $n=200$. Provide an approximate $95 \%$ confidence interval for the population slope parameter.
(2) Test the claim that the population slope equals 2 at the $5 \%$ significance level.
(3) Which of assumptions 1-4 need changing if model errors are heteroskedastic?

