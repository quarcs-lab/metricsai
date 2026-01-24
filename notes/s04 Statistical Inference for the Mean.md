# Chapter 4: Statistical Inference for the Mean

## Learning Objectives

By the end of this chapter, you will be able to:

- Understand how to extrapolate from sample mean x̄ to population mean μ using statistical inference
- Construct confidence intervals to identify the range of plausible values for the population mean
- Compute and interpret t-statistics and understand the t distribution
- Conduct two-sided hypothesis tests to evaluate claims about the population mean
- Calculate and interpret p-values for hypothesis tests
- Distinguish between Type I and Type II errors and understand significance levels
- Perform one-sided (directional) hypothesis tests and choose appropriate null and alternative hypotheses
- Generalize confidence interval and hypothesis testing methods to other parameters beyond the mean
- Apply statistical inference methods to proportions data and binary outcomes
- Use statistical software (R, Python, Excel) to implement confidence intervals and hypothesis tests

---

## 4.1 Example: Mean Annual Earnings

- Sample of 171 female full-time workers aged 30 in 2010.
- Descriptive statistics:

| Variable | Obs | Mean | Std. Dev. | Min | Max |
| ---: | ---: | ---: | ---: | ---: | ---: |
| earnings | 171 | 41412.69 | 25527.05 | 1050 | 172000 |

- Key statistics:
- Mean: sample mean $\bar{x}$
- Std. Dev.: standard error $s$ measures the precision of $\bar{x}$ as an estimate of $\mu$.
- The next slides present methods for statistical inference on $\mu$ that are explained in detail in the remainder of the chapter.

**Key Concept: Sample Mean as Estimator**

The sample mean x̄ is an unbiased estimator of the population mean μ: E[x̄] = μ. The standard error se(x̄) = s/√n measures the precision of x̄ as an estimate of μ. With sample size n=171 and standard deviation s=25,527, the standard error is 1,952, indicating moderate precision in our estimate of mean earnings.

### 95\% Confidence Interval for the Mean

- A $95 \%$ confidence interval for a parameter is a range of likely values that the parameter lies in with $95 \%$ confidence.
- $95 \%$ Confidence interval for $\mu$:

Mean estimation
Number of obs $=171$

|  | Mean | Std. Err. | [95\% Conf. Interval] |  |
| :--- | ---: | ---: | :--- | ---: |
| earnings | 41412.69 | 1952.103 | 37559.21 | 45266.17 |

- **Key statistics:**
  - Mean: sample mean $\bar{x}$ is the estimate of $\mu$
  - Std. Err: standard error measures the precision of $\bar{x}$ as an estimate of $\mu$
    - This equals $s / \sqrt{n}=25527.05 / \sqrt{171}=1952.1$

### 95\% Confidence Interval Calculation

- In general a confidence interval is

$$
\text{estimate} \pm \text{critical value} \text{×} \text{standard error}
$$

- Here we consider the population mean $\mu$.
- The estimate is $\bar{x}=41412.69$
- The standard error measures the precision of $\bar{x}$ as an estimate of $\mu$
- $\operatorname{se}(\bar{x})=s / \sqrt{n}=25527.05 / \sqrt{171}=1952.1$.
- The $95 \%$ critical value is approximately 2
- more precisely here $c=1.974$ as $\operatorname{Pr}\left[\left|T_{170}\right| \leq 1.974\right]=0.95$.
- The $95 \%$ confidence interval is then

$$
\bar{x} \pm c \times \operatorname{se}(\bar{x})=41412.69 \pm 1.974 \times 1952.1=(37559,45266) .
$$

### Critical Value for the Confidence Interval

- For $\mu$ use the $T$ distribution with $n-1$ degrees of freedom
- very similar to standard normal distribution except with fatter tails.
- Let $T_{n-1}$ denoted a random variable that is $T(n-1)$ distributed.
- The critical value $c$ for a $95 \%$ conf. interval is that value for which
- the probability that $\left|T_{n-1}\right| \leq c=0.95$
- equivalently the probability that $T_{n-1} \geq c=0.05 / 2=0.025$.

Critical value for 95\% conf. int.
![](https://cdn.mathpix.com/cropped/fc949097-0aa0-4241-b263-6c42fd6c818c-07.jpg?height=414&width=603&top_left_y=477&top_left_x=406)

### Hypothesis test on the Mean

- As illustrative example test whether or not $\mu=40,000$.

One-sample t test

| Variable | Obs | Mean | Std. Err. | Std. Dev. | [95\% Conf. Interval] |  |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| earnings | 171 | 41412.69 | 1952.103 | 25527.05 | 37559.21 | 45266.17 |


| mean = mean(earnings) |  | $\mathrm{t}=0.7237$ |
| :--- | :--- | :--- |
| Ho: mean = 40000 |  | degrees of freedom = 170 |
| Ha: mean < 40000 | Ha: mean != 40000 | Ha: mean > 40000 |
| $\operatorname{Pr}(\mathrm{T}<\mathrm{t})=0.7649$ | $\operatorname{Pr}(\|\mathrm{T}\|>\|\mathrm{t}\|)=0.4703$ | $\operatorname{Pr}(\mathrm{T}>\mathrm{t})=0.2351$ |

- We test $H_{0}: \mu=40000$ against $H_{a}: \mu \neq 40000$.
- The test statistic is $t=0.7237$.
- The $p$-value is 0.4703 (as we test against $H_{a}: \mu \neq 40000$ ).
- Since $p>0.05$ we do not reject $H_{0}: \mu=40000$ at level 0.05 .


### Hypothesis test calculation

- In general a $t$ test statistic is

$$
t=\frac{\text{estimate} - \text{hypothesized value}}{\text{standard error}} .
$$

- Here

$$
t=\frac{\bar{x}-\mu_{0}}{\operatorname{se}(\bar{x})}=\frac{41412.69-40000}{1952.1}=0.7237
$$

- The $p$-value is the probability of observing a value at least as large as this in absolute value.
- Here $p$ equals the probability that $\left|T_{170}\right| \geq 0.7237=0.4703$.
- Since this probability exceeds 0.05 we do not reject $H_{0}$.

**Key Concept: Confidence Intervals and Hypothesis Tests**

A 95% confidence interval provides a range of plausible values for μ: estimate ± critical value × standard error. A hypothesis test uses the t-statistic t = (x̄ - μ₀)/se(x̄) to evaluate whether a hypothesized value μ₀ is consistent with the data. The p-value measures how extreme the observed t-statistic is under H₀. Here, with t=0.724 and p=0.470, we do not reject H₀: μ=40,000 at the 5% level.

## 4.2 t Statistic and t distribution

- Estimate $\mu$ using $\bar{x}$ which is the sample value of draw of the random variable $\bar{X}$
- So far we have $E[\bar{X}]=\mu$ and $\operatorname{Var}[\bar{X}]=\sigma^{2} / n$ for a simple random sample.
- For confidence intervals and hypothesis tests on $\mu$ we need a distribution
- under certain assumptions $\bar{X}$ is normally distributed
- but with variance that depends on the unknown $\sigma^{2}$
- we replace $\sigma^{2}$ by the estimate $s^{2}$
- this leads to use of the $t$-statistic and the $t$ distribution

[^0]
### Normal Distribution and the Central Limit Theorem

- We assume a simple random sample where
- A. $X_{i}$ has common mean $\mu: \mathrm{E}\left[X_{i}\right]=\mu$ for all $i$.
- B. $X_{i}$ has common variance $\sigma^{2}: \operatorname{Var}\left[X_{i}\right]=\sigma^{2}$ for all $i$.
- C. Statistically independence: $X_{i}$ is statistically independent of $X_{j}, i \neq j$.
- Then $\bar{X} \sim\left(\mu, \sigma^{2} / n\right)$, i.e. $\bar{X}$ has mean $\mu$ and variance $\sigma^{2} / n$.
- Under these assumptions the standardized variable $Z=\frac{\bar{X}-\mu}{\sigma / \sqrt{n}} \sim(0,1)$.
- The central limit theorem (a remarkable result) states that if additionally the sample size is large $Z$ is normally distributed

$$
Z=\frac{\bar{X}-\mu}{\sigma / \sqrt{n}} \sim N(0,1) \text{as } n \rightarrow \infty .
$$

### The t-statistic

- Now replace the unknown $\sigma^{2}$ by an estimator $S^{2}=\frac{1}{n-1} \sum_{i=1}^{n}\left(X_{i}-\bar{X}\right)^{2}$.

$$
T=\frac{\bar{X}-\mu}{S / \sqrt{n}}
$$

- The distribution for $T$ is complicated. The standard approximation is $T$ has the $t$ distribution with ( $n-1$ ) degrees of freedom

$$
T \sim T(n-1)
$$

- Comments
- different degrees of freedom correspond to different $t$ distributions
- the term degrees of freedom is used because $\bar{X}=\frac{1}{n} \sum_{i=1}^{n} X_{i}$ implies that only ( $n-1$ ) terms in the sum are free to vary
- $T \sim T(n-1)$ exactly in the very special case that $X_{i} s$ are normally distributed
- otherwise $T$ is not $T(n-1)$ exactly but is the standard approximation.

**Key Concept: The t Distribution**

The t distribution is similar to the standard normal N(0,1) but with fatter tails. The t-statistic T = (X̄ - μ)/(S/√n) follows a t distribution with (n-1) degrees of freedom. As n increases, the t distribution approaches the standard normal distribution. For n > 30, t_{n-1,0.025} ≈ 2, giving the "two-standard-error rule" for approximate 95% confidence intervals.

### The t -statistic (continued)

- In summary, inference on $\mu$ is based on the sample $t$-statistic is

$$
t=\frac{\bar{x}-\mu}{\operatorname{se}(\bar{x})}=\frac{\bar{x}-\mu}{s / \sqrt{n}},
$$

- $\bar{x}$ is the sample mean
- $\operatorname{se}(\bar{x})$ is the standard error of $\bar{x}$
- $s$ is the sample standard deviation.
- The statistic $t$ is viewed as a realization of the $T(n-1)$ distribution.


### The t Distribution

- $t$ distribution has probability density function that is bell-shaped
- $\operatorname{Pr}[a<T<b]$ is the area under the curve between $a$ and $b$
- The $t$ distribution has fatter tails than the standard normal.
- $T_{v}$ denotes a random variable that has the $T(v)$ distribution.
- Different values of $v$ correspond to different $T$ distributions
- $t_{\infty}$ is the same as $N(0,1)$.
![](https://cdn.mathpix.com/cropped/fc949097-0aa0-4241-b263-6c42fd6c818c-14.jpg?height=436&width=546&top_left_y=470&top_left_x=76)
![](https://cdn.mathpix.com/cropped/fc949097-0aa0-4241-b263-6c42fd6c818c-14.jpg?height=439&width=546&top_left_y=470&top_left_x=641)


### Probabilities for the t Distribution

- Probabilities are the area under the $t$ probability density function.
- e.g. $\operatorname{Pr}[a<T<b]$ is the area under the curve from $a$ to $b$
- Computing these probabilities requires a computer.
- The R function $1-\mathrm{pt}(\mathrm{t}, \mathrm{v})$ gives $\operatorname{Pr}\left[T_{v}>t\right]$
- e.g. $\operatorname{Pr}\left[T_{170}>0.724\right]=1-\mathrm{pt}(0.724,170)=0.235$.
- Python: `1 - t.cdf(t, v)` using `scipy.stats` gives $\operatorname{Pr}\left[T_{v}>t\right]$


### Inverse Probabilities for the t Distribution

- For confidence intervals we need to find the inverse probability
- called a critical value.
- Definition: the inverse probability or critical value $c=t_{v, \alpha}$ is that value such that the probability that a $T(v)$ distributed random variable exceeds $t_{v, \alpha}$ equals $\alpha$.

$$
\operatorname{Pr}\left[T_{v}>t_{v, \alpha}\right]=\alpha
$$

- i.e. the area in the right tail beyond $t_{v, \alpha}$ equals $\alpha$.
- Example: $\operatorname{Pr}\left[T_{170}>1.654\right]=0.05$ so $c=t_{170, .05}=1.654$.
- The R function is $\mathrm{qt}(1-\mathrm{a}, \mathrm{v})$ e.g. $\mathrm{qt}(0.95,170)=1.654$.
- Python: `t.ppf(1-a, v)` using `scipy.stats` gives the critical value


### Inverse probabilities (continued)

- Left panel: $\operatorname{Pr}\left[T_{170}>1.654\right]=0.05$, so $t_{170,05}=1.654$.
- Right panel: $\operatorname{Pr}\left[-1.974<T_{170}<1.974\right]=0.05$
using $\operatorname{Pr}\left[T_{170}>1.974\right]=0.025$ and $t_{170, .025}=1.974$.
![](https://cdn.mathpix.com/cropped/fc949097-0aa0-4241-b263-6c42fd6c818c-17.jpg?height=394&width=536&top_left_y=398&top_left_x=85)
![](https://cdn.mathpix.com/cropped/fc949097-0aa0-4241-b263-6c42fd6c818c-17.jpg?height=394&width=536&top_left_y=398&top_left_x=640)


## 4.3 Confidence Intervals

- For simplicity focus on $95 \%$ confidence intervals.
- A 95 percent confidence interval for the population mean is

$$
\bar{x} \pm t_{n-1, .025} \times \operatorname{se}(\bar{x}),
$$

- $\bar{x}$ is the sample mean
- $t_{n-1, .025}$ is exceeded by a $T(n-1)$ random variable with probability 0.025
- $\operatorname{se}(\bar{x})=s / \sqrt{n}$ is the standard error of the sample mean.
- The area in the tails is $0.025+0.025=0.05$
- leaving area 0.95 in the middle
- hence a $95 \%$ confidence interval.


### Example: Mean Annual Earnings

- Here $\bar{x}=41413, \operatorname{se}(\bar{x})=s / \sqrt{n}=1952, n=171$, and $t_{170, .025}=1.974$.
- A $95 \%$ confidence interval $(\mathrm{Cl})$ is

$$
\begin{aligned}
\bar{x} \pm t_{n-1, \alpha / 2} \times(s / \sqrt{n}) & =41413 \pm 1.974 \times 1952 \\
& =41413 \pm 3853 \\
& =(37560,45266) .
\end{aligned}
$$

- A $95 \%$ confidence interval for population mean earnings of thirty year-old female full-time workers is
- (\$37,560, \$45,266)
- this was the result obtained earlier.


### Derivation of a $95 \%$ Confidence Intervals

- We derive a $95 \%$ confidence interval from first principles.
- For simplicity consider a sample with $n=61$, in which case $n-1=60$ and $t_{60, .025}=2.0003$. Thus

$$
\operatorname{Pr}\left[-2.0003<T_{60}<2.0003\right]=0.95 .
$$

- Round to $\operatorname{Pr}[-2<T<2]=0.95$ and substituting $T=\frac{\bar{X}-\mu}{S / \sqrt{n}}$ yields

$$
\operatorname{Pr}\left[-2<\frac{\bar{X}-\mu}{S / \sqrt{n}}<2\right]=0.95 .
$$

- Convert to an interval that is centered on $\mu$ as follows

$$
\begin{aligned}
\operatorname{Pr}\left[-2<\frac{\bar{X}-\mu}{S / \sqrt{n}}<2\right] & =0.95 \\
\operatorname{Pr}[-2 S / \sqrt{n}<\bar{X}-\mu<2 S / \sqrt{n}] & =0.95 \text{times } S / \sqrt{n} \\
\operatorname{Pr}[-\bar{X}-2 S / \sqrt{n}<-\mu<-\bar{X}+2 S / \sqrt{n}] & =0.95 \text{subtract } \bar{X} \\
\operatorname{Pr}[\bar{X}+2 S / \sqrt{n}>\mu>\bar{X}-2 S / \sqrt{n}] & =0.95 \text{times } -1 .
\end{aligned}
$$

### Derivation (continued)

- Re-ordering the final inequality yields

$$
\operatorname{Pr}[\bar{X}-2 \times S / \sqrt{n}<\mu<\bar{X}+2 S / \sqrt{n}]=0.95 .
$$

- Replace random variables by their observed values
- the interval $(\bar{x}-2 \times s / \sqrt{n}, \bar{x}+2 \times s / \sqrt{n})$ is called a $95 \%$ confidence interval for $\mu$.
- More generally with sample size $n$ the critical value is $t_{n-1, .025}$.
- A $95 \%$ confidence interval is $\left(\bar{x}-t_{n-1, .025} \times \operatorname{se}(\bar{x})\right.$, $\left.\bar{x}+t_{n-1, .025} \times \operatorname{se}(\bar{x})\right)$.
- This is the confidence interval formula given earlier.


### What Level of Confidence?

- Ideally narrow confidence intervals with high level of confidence.
- But trade-off: more confidence implies wider interval
- e.g. $100 \%$ confidence is $\mu$ in $(-\infty, \infty)$.
- What value of confidence should we use?
- no best value in general
- common to use a $95 \%$ confidence interval.
- A $\mathbf{1 0 0}(\mathbf{1}-\boldsymbol{\alpha}) \%$ percent confidence interval for the population mean is

$$
\bar{x} \pm t_{n-1, a / 2} \times(s / \sqrt{n}) .
$$

- $\alpha=0.05$ (so $\alpha / 2=0.025$ ) gives a $95 \%$ confidence interval as $100 \times(1-0.05)=95$.
- next most common are $90 \%(\alpha=0.10)$ and $99 \%(\alpha=0.01)$ confidence intervals


### Critical t values

- Table presents $t_{v, \alpha / 2}$ for various confidence levels ( $\alpha$ ) and $v=n-1$.
- The $95 \%$ confidence intervals critical values are bolded

| Confidence Level | $100(1-\alpha)$ | $90 \%$ | $\mathbf{9 5 \%}$ | $99 \%$ |
| :--- | :---: | ---: | ---: | ---: |
| Area in both tails | $\alpha$ | 0.10 | $\mathbf{0 . 0 5}$ | 0.01 |
| Area in single tail | $\alpha / 2$ | 0.05 | $\mathbf{0 . 0 2 5}$ | 0.005 |
| t value for $v=10$ | $t_{10, \alpha / 2}$ | 1.812 | $\mathbf{2 . 2 2 8}$ | 3.169 |
| t value for $v=30$ | $t_{30, \alpha / 2}$ | 1.697 | $\mathbf{2 . 0 4 2}$ | 2.750 |
| t value for $v=100$ | $t_{100, \alpha / 2}$ | 1.660 | $\mathbf{1 . 9 8 0}$ | 2.626 |
| t value for $v=\infty$ | $t_{\infty, \alpha / 2}$ | 1.645 | $\mathbf{1 . 9 6 0}$ | 2.576 |
| standard normal value | $z_{\alpha / 2}$ | 1.645 | $\mathbf{1 . 9 6 0}$ | 2.576 |

- Note that $t_{v, .025} \simeq 2$ for $v>30$.
- An approximate $95 \%$ confidence interval for $\mu$ is therefore a two-standard error interval
- the sample mean plus or minus two standard errors.


### Interpretation

- Interpretation of confidence intervals is conceptually difficult.
- The correct interpretation of a 95 percent confidence interval is that if constructed for each of an infinite number of samples then it will include $\mu 95 \%$ of the time
- of course we only have one sample.
- 1880 Census example (we know $\mu=24.13$ ) in Chapter 3
- First sample of size 25 : $95 \%$ confidence interval $(17.99,34.81)$
- Second sample: $95 \% \mathrm{Cl}(13.12,25.54)$, and so on.
- For the particular 100 samples drawn
- two samples had $95 \%$ confidence intervals that did not include $\mu$
$\star 20^{t h}$ sample had $95 \%$ interval $(8.57,23.90)$
$\star 50^{\text {th }}$ sample had $95 \%$ interval $(11.49,21.45)$
- so here $98 \%$ of the samples had $95 \%$ confidence interval that included $\mu$ (versus theory $95 \%$ ).


## 4.4 Two-Sided Hypothesis Tests

- A two-sided test or two-tailed test for the population mean is a test of the null hypothesis

$$
H_{0}: \mu=\mu^{*}
$$

where $\mu^{*}$ is a specified value for $\mu$, against the alternative hypothesis

$$
H_{a}: \mu \neq \mu^{*} .
$$

- In the next example $\mu^{*}=40000$.
- Called two-sided as the alternative hypothesis includes both $\mu>\mu^{*}$ and $\mu<\mu^{*}$.
- We need to either reject $H_{0}$ or not reject $H_{0}$.


### Significance Level of a Test

- A test either rejects or does not reject the null hypothesis.
- The decision made may be in error.
- A type $\mathbf{I}$ error occurs if $H_{0}$ is rejected when $H_{0}$ is true.
- e.g. $H_{0}$ is person is innocent. A type $I$ error is to reject $H_{0}$ and find the person guilty, when in fact the person was innocent.
- The significance level of a test, denoted $\alpha$, is the pre-specified maximum probability of a type I error that will be tolerated.
- Often $\alpha=0.05$. A $5 \%$ chance of making a type I error.

**Key Concept: Significance Level and Type I Error**

The significance level α is the pre-specified maximum probability of Type I error (rejecting H₀ when it's true) that we're willing to tolerate. Commonly α=0.05 (5% significance level), meaning we accept a 1-in-20 chance of incorrectly rejecting a true null hypothesis. Lower α reduces Type I errors but makes it harder to detect true effects (increases Type II errors).

### The t-test Statistic

- Obviously reject $H_{0}: \mu=\mu^{*}$ if $\bar{x}$ is a long way from $\mu^{*}$.
- Transform to $t=\left(\bar{x}-\mu^{*}\right) / \operatorname{se}(\bar{x})$ as this has known distribution.
- Equivalently reject $H_{0}$ : if the $t$ statistic is large in absolute value where

$$
t=\frac{\bar{x}-\mu^{*}}{\operatorname{se}(\bar{x})}=\frac{\bar{x}-\mu^{*}}{s / \sqrt{n}}
$$

- Example: Test whether or not population mean female earnings equal \$40, 000.
- Here $H_{0}: \mu=40000$ and $n=171, \bar{x}=41412, s=25527$, so $s e(\bar{x})=s / \sqrt{n}=1952$

$$
t=\frac{\bar{x}-\mu}{\operatorname{se}(\bar{x})}=\frac{41412-40000}{1952}=0.724 .
$$

- The $t$-statistic is a draw from the $T(170)$ distribution, since $n=171$.


### Rejection Using p-values

- How likely are we to obtain a draw from $T(170)$ that is $\geq|0.724|$ ?
- The $p$-value is the probability of observing a t-test statistic at least as large in absolute value as that obtained in the current sample.
- For a two-sided test of $H_{0}: \mu=\mu^{*}$ against $H_{a}: \mu \neq \mu^{*}$ the p -value is

$$
p=\operatorname{Pr}\left[\left|T_{n-1}\right| \geq|t|\right]
$$

- $H_{0}$ is rejected at significance level $\alpha$ if $p<\alpha$, and is not rejected otherwise.
- Earnings example
- $p=\operatorname{Pr}\left[\left|T_{170}\right| \geq 0.724\right]=0.470$.
- since $p>0.05$ we do not reject $H_{0}$.
- Left panel: $p$-value
- Right panel: critical value
![](https://cdn.mathpix.com/cropped/fc949097-0aa0-4241-b263-6c42fd6c818c-29.jpg?height=390&width=534&top_left_y=314&top_left_x=85)

Two-sided test: critical value approach
![](https://cdn.mathpix.com/cropped/fc949097-0aa0-4241-b263-6c42fd6c818c-29.jpg?height=359&width=534&top_left_y=345&top_left_x=641)

### Rejection using Critical Regions

- Alternative equivalent method is the following
- base rejection directly on the value of the $t$-statistic
- requires table of critical values rather than computer for p -values.
- A critical region or rejection region is the range of values of $t$ that would lead to rejection of $H_{0}$ at the specified significance level $\alpha$.
- For a two-sided test of $H_{0}: \mu=\mu^{*}$ against $H_{a}: \mu \neq \mu^{*}$, and for specified $\alpha$, the critical value $c$ is such that

$$
\left.c=t_{n-1, \alpha / 2} \text{(so equivalently } \operatorname{Pr}\left[\left|T_{n-1}\right| \geq c\right]=\alpha\right)
$$

- $H_{0}$ is rejected at significance level $\alpha$ if $|t|>c$, and is not rejected otherwise.
- Earnings example:
- if $\alpha=0.05$ then $c=t_{170,0.025}=1.974$.
- do not reject $H_{0}$ since $t=0.724$ and $|0.724|<1.974$.
- The critical value is illustrated in right panel of the preceding figure.


### Which Significance level?

- Decreasing the significance level $\alpha$
- decreases the area in the tails that defines the rejection region
- makes it less likely that $H_{0}$ is rejected.
- It is most common to use $\alpha=0.05$, called a test at the $5 \%$ significance level
- then a type $I$ error is made 1 in 20 times.
- This is a convention and in many applications other values of $\alpha$ may be warranted.
- e.g. What if $H_{0}$ : no nuclear war? Then use $\alpha>0.05$.
- Reporting $p$-values allows the reader to easily test using their own preferred value of $\alpha$.
- Further discussion under test power.


### Relationship to Confidence Intervals

- Two-sided tests can be implemented using confidence intervals.
- If the $H_{0}$ value $\mu^{*}$ falls inside the $100(1-\alpha)$ percent confidence interval then do not reject $H_{0}$ at level $\alpha$.
- Otherwise reject $H_{0}$ at significance level $\alpha$.


### Summary

- A summary of the preceding example is the following.

| Hypotheses | $H_{0}: \mu=40000 \quad H_{a}: \mu \neq 40000 \quad \alpha=0.05$ |
| :--- | :--- |
| Significance level | $\alpha=0.05$ |
| Sample data | $\bar{x}=41412, s=25527, n=171$ |
| Test statistic | $t=(41412-40000) /(25527 / \sqrt{171})=0.724$ |
| (1) p-value approach | $p=\operatorname{Pr}\left[\left\|T_{170}\right\| \geq\|0.724\|\right]=0.470$ <br> Do not reject $H_{0}$ at level .05 as $p>.05$ |
| (2) Critical value approach | $c=t_{170, .025}=1.974$ <br> Do not reject $H_{0}$ at level .05 as $\|t\|<c$. |

- The p -value and critical value approaches are alternative methods that lead to the same conclusion.

**Key Concept: P-values and Hypothesis Testing**

The p-value is the probability of observing a test statistic at least as extreme as the one obtained, assuming H₀ is true. For two-sided tests, p = Pr[|T_{n-1}| ≥ |t|]. Small p-values (p < α) provide strong evidence against H₀, leading to rejection. The p-value approach and critical value approach always give the same conclusion—they're just two equivalent ways to implement the same test.

## 4.5 Hypothesis Testing Example 1: Gasoline Prices

- Test at $\alpha=.05$ claim that the price of regular gasoline in Yolo County is neither higher nor lower than the norm for California.
- one day's data from a website that provides daily data on gas prices
- average California price that day was \$3.81
- $H_{0}: \mu=3.81$ is tested against $H_{a}: \mu \neq 3.81$.
- $n=32, \bar{x}=3.6697$ and $s=0.1510$.
- $t=(3.6697-3.81) /(0.1510 / \sqrt{32})=-5.256$.
- $p$ value method: $p=\operatorname{Pr}\left[\left|T_{31}\right|>5.256\right]=0.000$
- reject $H_{0}$ at level .05 since $p<.05$.
- Critical value method: $c=t_{31, .025}=2.040$.
- reject $H_{0}$ at level .05 since $|t|=5.256>c=2.040$.
- Reject the claim that reject the claim that population mean Yolo County gas price equals the California state-average price.


### Example 2: Male Earnings

- Test at $\alpha=.05$ the claim that population mean annual earnings for 30 year-old U.S. men with earnings in 2010 exceed \$50,000
- claim that > 50000 is set up as the alternative hypothesis
- $H_{0}: \mu \leq 50000$ is tested against $H_{a}: \mu>50000$.
- $n=191, \bar{x}=52353.93$ and $s=65034.74$.
- $t=(52353.93-50000) /(65034.74 / \sqrt{191})=0.5002$.
- $p$ value method: $p=\operatorname{Pr}\left[T_{190}>0.500\right]=0.310$.
- do not reject $H_{0}$ at level .05 since $p>.05$.
- Critical value method: $c=t_{190, .05}=1.653$.
- do not reject $H_{0}$ at level .05 since $t=0.500>c=1.653$.
- Do not reject the claim that population mean earnings exceed \$50,000.


### Example 3: Price Inflation

- Test at $\alpha=.05$ claim that U.S. real GDP per capita grew on average at $2.0 \%$ over the period 1960 to 2020
- use year-to-year percentage changes in U.S. real GDP per capita.
- $H_{0}: \mu=2.0$ tested against $H_{a}: \mu \neq 2.0$.
- $n=241, \bar{x}=1.9904$ and $s=2.1781$.
- $t=(1.9904-2.0) /(2.1781 / \sqrt{241})=-0.068$.
- $p$ value method: $p=\operatorname{Pr}\left[\left|T_{258}\right|>0.0680\right]=0.946$
- do not reject $H_{0}$ at level .05 since $p<.05$.
- Critical value method: $c=t_{241, .025}=1.970$
- do not reject $H_{0}$ at level .05 since $|t|=0.068<c=1.970$.
- Do not reject the claim that population mean growth was $2.0 \%$.


## 4.6 One-sided Directional Hypothesis Tests

- An upper one-tailed alternative test is a test of $H_{0}: \mu \leq \mu^{*}$ against $H_{a}: \mu>\mu^{*}$.
- A lower one-tailed alternative test is a test of $H_{0}: \mu \geq \mu^{*}$ against $H_{a}: \mu<\mu^{*}$.
- For one-sided tests the statement being tested is specified to be the alternative hypothesis.
- And if a new theory is put forward to supplant an old, the new theory is specified to be the alternative hypothesis.
- Example: Test claim that population mean earnings exceed \$40,000
- test $H_{0}: \mu \leq 40000$ against $H_{a}: \mu>40000$.


### P-Values and Critical Regions

- Use the usual $t$-test statistic $t=\left(\bar{x}-\mu^{*}\right) / \operatorname{se}(\bar{x})$.
- For an upper one-tailed alternative test
- $p=\operatorname{Pr}\left[T_{n-1} \geq t\right]$ is $p$-value
- $c=t_{n-1, \alpha}$ is critical value at significance level $\alpha$
- reject $H_{0}$ if $p<\alpha$ or, equivalently, if $t>c$.
- For a lower one-tailed alternative test
- $p=\operatorname{Pr}\left[T_{n-1} \leq t\right]$ is $p$-value
- $c=-t_{n-1, \alpha}$ is critical value at significance level $\alpha$
- $H_{0}$ if $p<\alpha$ or, equivalently, if $t<c$.


### Example: Mean Annual Earnings

- Evaluate the claim that the population mean exceeds \$40,000.
- Test of $H_{0}: \mu \leq 40000$ against $H_{a}: \mu>40000$
- the claim is specified to be the alternative hypothesis
- a detailed explanation is given next
- and we reject if $t$ is large and positive.
- From earlier $t=0.724$.
- $p$ value method: $p=\operatorname{Pr}\left[T_{170} \geq .724\right]=0.235$
- do not reject $H_{0}$ at level 0.05 since $p>0.05$.
- Critical value method: $c=t_{170, .05}=1.654$
- do not reject $H_{0}$ at level 0.05 since $t=0.724<c=1.654$.
- Left panel: $p$-value
- Right panel: critical value
![](https://cdn.mathpix.com/cropped/fc949097-0aa0-4241-b263-6c42fd6c818c-40.jpg?height=420&width=574&top_left_y=325&top_left_x=61)

One-sided test: critical v alue approach
![](https://cdn.mathpix.com/cropped/fc949097-0aa0-4241-b263-6c42fd6c818c-40.jpg?height=383&width=571&top_left_y=358&top_left_x=653)

### Specifying the Null Hypothesis in One-sided Test

- Suppose claim is that population mean earnings exceed \$40,000.
- Potential method 1: test $H_{0}: \mu \leq 40000$ against $H_{a}: \mu>40000$
- Reject $H_{0}$ if $\bar{x}$ quite a bit higher than 40000. e.g. 43,000.
- Then claim that $\mu>40000$ is supported if $\bar{x}>43000$.
- Potential method 2: test $H_{0}: \mu \geq 40000$ against $H_{a}: \mu<40000$
- Reject $H_{0}$ if $\bar{x}$ quite a bit smaller than than 40000 . e.g. 37,000 .
- So do not reject $H_{0}$ if $\bar{x}>37000$.
- Then claim that $\mu>40000$ is supported if $\bar{x}>37000$
- Much more likely to accept the claim than with method 1.
- The statistics philosophy: need strong evidence to support a claim
- the first specification is therefore used
- the statement being tested is specified to be the alternative hypothesis.

**Key Concept: One-sided vs. Two-sided Tests**

One-sided tests have directional alternatives: H₀: μ ≤ μ* vs. H_a: μ > μ* (upper tail) or H₀: μ ≥ μ* vs. H_a: μ < μ* (lower tail). The claim being tested is always specified as the alternative hypothesis, requiring strong evidence to support it. One-sided tests use half the tail area: p = Pr[T_{n-1} ≥ t] for upper tail tests, with critical value c = t_{n-1,α} (not t_{n-1,α/2} as in two-sided tests).

## 4.7 Generalize Confidence Intervals and Hypothesis Tests

- Consider general case of an estimate of a parameter
- with standard error the estimated standard deviation of the estimate
- generalizes $\bar{x}$ is an estimate of $\mu$ with standard error $\operatorname{se}(\bar{x})$.
- For the models and assumptions considered in this book

$$
t=\frac{\text{estimate} - \text{parameter}}{\text{standard error}} \sim T(v) \text{distribution}
$$

where the degrees of freedom $v$ vary with the setting.

- The $100(1-\alpha) \%$ confidence interval for the unknown parameter is

$$
\text{estimate} \pm t_{v, \alpha / 2} \times \text{standard error.}
$$

- Most often use $95 \%$ confidence level and $t_{v, .025} \simeq 2$ for $v>30$.
- So an approximate $95 \% \mathrm{Cl}$ is a two-standard error interval

$$
\text{estimate} \pm 2 \times \text{standard error.}
$$

- Margin of error in general is half the width of a confidence interval.
- For $95 \%$ confidence intervals, since $t_{v, .025} \simeq 2$,

$$
\text{Margin of error} \simeq 2 \times \text{Standard error.}
$$

### Generalization of Hypothesis Tests

- Two-sided test at significance level $\alpha$ of
- $H_{0}$ : a parameter equals a hypothesized value against
- $H_{a}$ : that it does not.
- Calculate the $t$-statistic

$$
t=\frac{\text{estimate} - \text{hypothesized parameter value}}{\text{standard error}} .
$$

- under $H_{0} t$ is the sample realization of a $T(v)$ random variable.
- Two-sided hypothesis test at significance level $\alpha$ :
- $p$-value approach: reject $H_{0}$ if $p<\alpha$ where $p=\operatorname{Pr}\left[\left|T_{v}\right|>t\right]$
- critical value approach: reject $H_{0}$ if $|t|>c$ where $c=t_{v, \alpha / 2}$ satisfies $\operatorname{Pr}\left[T_{v}>t_{v, \alpha / 2}\right]=\alpha$
- the two methods lead to the same conclusion.


## 4.8 Proportions Data

- Consider proportion of respondents voting Democrat.
- Code data as $x_{i}=1$ if vote Democrat and $x_{i}=0$ if vote Republican
- The sample mean $\bar{x}$ is the proportion voting Democrat
- The sample variance $s^{2}=n \bar{x}(1-\bar{x}) /(n-1)$
  - In this special case of binary data

- **Example:** 480 of 921 voters intend to vote Democrat (and 441 vote Republican)
- $\bar{x}=(480 \times 1+440 \times 0) / 921=0.5212$
- $s^{2}=921 \times 0.5212 \times(1-0.5212) / 920=0.2498$.


### Inference for Proportions Data

- View each outcome as result of random variable

$$
X=\left\{\begin{array}{lll}
1 & \text{with probability } p & \text{if vote Democrat} \\
0 & \text{with probability } 1-p & \text{if vote Republican}
\end{array}\right.
$$

- Then $\bar{X}$ has mean $p$ and variance $\sigma^{2} / n=p(1-p) / n$.
- Can do analysis using earlier results with the usual standard error of $\bar{x}$
- here $s^{2} / n=n \bar{x}(1-\bar{x}) /(n-1)=\bar{x}(1-\bar{x}) /(n-1)$
- But usually confidence intervals substitute $\bar{x}$ for $p$ in $\sigma^{2} / n=p(1-p) / n$
- so standard error of $\bar{x}$ is $\bar{x}(1-\bar{x}) / n$
- And hypothesis tests of $H_{0}: p=p^{*}$ also substitute for $p$ and use

$$
t=\frac{\bar{x}-p^{*}}{\sqrt{p^{*}\left(1-p^{*}\right) / n}}
$$

**Key Concept: Inference for Proportions**

For binary data (x_i = 1 or 0), the sample mean x̄ equals the sample proportion. The sample variance has the special form s² = nx̄(1-x̄)/(n-1). For confidence intervals, use standard error se(x̄) = √[x̄(1-x̄)/n]. For hypothesis tests of H₀: p = p*, use se = √[p*(1-p*)/n], substituting the hypothesized proportion p* rather than the sample proportion.

### Computing the p-value and Critical Value

- Example of computer commands to get $p$ and $c$
- for $t=t$, degrees of freedom $v$, and test at level $\alpha$
- Two-sided tests
- R: $p=2 *(1-\mathrm{pt}(|t|, v))$ and $c=\mathrm{qt}(1-\alpha / 2, v)$
- Python: `p = 2 * (1 - t.cdf(abs(t), v))` and `c = t.ppf(1 - alpha/2, v)` using `scipy.stats`
- Excel: $p=\operatorname{TDIST}(|t|, v, 2)$ and $c=\operatorname{TINV}(2 \alpha, v)$

---

## Key Takeaways

**Introduction to Statistical Inference (Section 4.1):**
- Statistical inference extrapolates from sample statistics to population parameters
- The sample mean x̄ is an unbiased estimator of the population mean μ: E[x̄] = μ
- The standard error se(x̄) = s/√n measures the precision of x̄ as an estimate of μ
- Confidence intervals provide a range of plausible values for μ given the sample data
- Hypothesis tests evaluate whether specific values of μ are consistent with the data
- Example: With n=171 female workers, x̄ = $41,413, s = $25,527, giving se(x̄) = $1,952
- 95% confidence interval for mean earnings: ($37,559, $45,266)
- Hypothesis test H₀: μ = $40,000 yields t = 0.724, p = 0.470 → do not reject H₀
- Methods developed for the mean μ generalize to inference on other parameters

**The t-statistic and t Distribution (Section 4.2):**
- For simple random samples: x̄ ~ (μ, σ²/n), meaning x̄ has mean μ and variance σ²/n
- The Central Limit Theorem: as n → ∞, the standardized variable Z = (x̄ - μ)/(σ/√n) ~ N(0,1)
- Since σ is unknown, replace with sample estimate s to get the t-statistic: t = (x̄ - μ)/(s/√n)
- The t-statistic follows the t distribution with (n-1) degrees of freedom: T ~ T(n-1)
- The t distribution is bell-shaped like the standard normal but with fatter tails
- As degrees of freedom increase, the t distribution converges to N(0,1)
- For n > 30, t_{n-1,0.025} ≈ 2, giving the "two-standard-error rule" for approximate 95% CIs
- The t(n-1) distribution is exact if data are normally distributed, otherwise it's an approximation
- R functions: 1-pt(t, v) for probabilities, qt(1-α, v) for critical values
- Python functions: `scipy.stats.t.cdf(t, v)` for probabilities, `scipy.stats.t.ppf(1-α, v)` for critical values

**Confidence Intervals (Section 4.3):**
- A 95% confidence interval for μ: x̄ ± t_{n-1,0.025} × se(x̄)
- General form: estimate ± critical value × standard error
- The critical value t_{n-1,α/2} satisfies Pr[|T_{n-1}| ≤ t_{n-1,α/2}] = 1 - α
- For 95% CI, α = 0.05, so α/2 = 0.025, giving confidence level 100(1-0.05)% = 95%
- Common confidence levels: 90% (α=0.10), 95% (α=0.05), 99% (α=0.01)
- Tradeoff: higher confidence → wider interval; narrow interval → less confidence
- 100% confidence gives useless interval (-∞, ∞)
- Interpretation: If we constructed 95% CIs for infinite samples, 95% would contain μ
- We only have one sample, so we're "95% confident" this particular interval contains μ
- Example: 95% CI for mean earnings = $41,413 ± 1.974 × $1,952 = ($37,560, $45,266)
- Margin of error ≈ 2 × standard error for 95% CIs (since t_{v,0.025} ≈ 2 for v > 30)

**Two-Sided Hypothesis Tests (Section 4.4):**
- Null hypothesis: H₀: μ = μ* tests whether μ equals a specified value μ*
- Alternative hypothesis: H_a: μ ≠ μ* (two-sided because includes both μ > μ* and μ < μ*)
- Test statistic: t = (x̄ - μ*)/se(x̄) = (x̄ - μ*)/(s/√n)
- Under H₀, t follows the T(n-1) distribution
- **Significance level α**: pre-specified maximum probability of Type I error (rejecting true H₀)
- Type I error: rejecting H₀ when it's true (false positive)
- Type II error: failing to reject H₀ when it's false (false negative, not controlled by α)
- Common significance level: α = 0.05 (5% level), accepting 1-in-20 chance of Type I error
- **P-value**: probability of observing test statistic at least as extreme as obtained, assuming H₀ true
- For two-sided test: p = Pr[|T_{n-1}| ≥ |t|]
- **P-value approach**: Reject H₀ if p < α; otherwise do not reject
- **Critical value approach**: Reject H₀ if |t| > c where c = t_{n-1,α/2}
- Both approaches give identical conclusions—they're equivalent methods
- Relationship to CIs: if μ* falls inside the 100(1-α)% CI, do not reject H₀ at level α
- Reporting p-values allows readers to test using their own preferred α

**Hypothesis Testing Examples (Section 4.5):**
- **Example 1 - Gasoline prices**: H₀: μ = $3.81, n=32, x̄=$3.67, s=$0.15, t=-5.256, p=0.000
  - Reject H₀ at 5% level: strong evidence Yolo County prices differ from California average
- **Example 2 - Male earnings**: H₀: μ ≤ $50,000 vs. H_a: μ > $50,000 (one-sided), n=191, t=0.500, p=0.310
  - Do not reject H₀: insufficient evidence that mean male earnings exceed $50,000
- **Example 3 - GDP growth**: H₀: μ = 2.0% vs. H_a: μ ≠ 2.0%, n=241, t=-0.068, p=0.946
  - Do not reject H₀: data consistent with 2.0% average annual growth rate
- These examples demonstrate typical applications across different contexts
- Large |t| values (far from 0) and small p-values (p < 0.05) lead to rejection
- Small |t| values (close to 0) and large p-values (p > 0.05) fail to reject H₀

**One-Sided Hypothesis Tests (Section 4.6):**
- **Upper one-tailed test**: H₀: μ ≤ μ* vs. H_a: μ > μ*
- **Lower one-tailed test**: H₀: μ ≥ μ* vs. H_a: μ < μ*
- The claim being tested is always specified as the alternative hypothesis (requires strong evidence)
- For upper tail: p = Pr[T_{n-1} ≥ t]; reject if t > c where c = t_{n-1,α} (not α/2!)
- For lower tail: p = Pr[T_{n-1} ≤ t]; reject if t < -c where c = t_{n-1,α}
- One-sided tests use only one tail, so critical values differ from two-sided tests
- Example: Testing μ > $40,000, t = 0.724, p = Pr[T_{170} ≥ 0.724] = 0.235 > 0.05 → do not reject
- Why put claim in H_a? Statistics requires strong evidence to support a claim
- Setting claim as H_a means we only accept it when evidence is compelling (low p-value)
- One-sided tests have more power than two-sided tests for detecting effects in the specified direction

**Generalization of Methods (Section 4.7):**
- General t-statistic: t = (estimate - parameter value) / standard error
- Under H₀, t ~ T(v) distribution where degrees of freedom v varies by setting
- General 100(1-α)% confidence interval: estimate ± t_{v,α/2} × standard error
- Approximate 95% CI: estimate ± 2 × standard error (for v > 30)
- General two-sided test at level α:
  - P-value approach: reject H₀ if p < α where p = Pr[|T_v| > |t|]
  - Critical value approach: reject H₀ if |t| > c where c = t_{v,α/2}
- These methods extend to regression coefficients, differences in means, correlation coefficients, etc.
- Margin of error ≈ 2 × standard error for 95% confidence intervals

**Inference for Proportions (Section 4.8):**
- For binary data: x_i = 1 (success) or x_i = 0 (failure), with population proportion p
- Sample mean x̄ equals the sample proportion: x̄ = (# successes)/n
- Sample variance: s² = nx̄(1-x̄)/(n-1) in this special case
- Random variable X has E[X] = p and Var[X] = p(1-p)
- Sample mean x̄ has E[x̄] = p and Var[x̄] = p(1-p)/n
- **For confidence intervals**: use se(x̄) = √[x̄(1-x̄)/n] (substitute x̄ for p in variance formula)
- **For hypothesis tests** of H₀: p = p*: use se = √[p*(1-p*)/n] (substitute p* not x̄)
- Example: 480 of 921 voters intend to vote Democrat: x̄ = 0.5212, s² = 0.2498
- Methods for proportions apply to: election polling, quality control, medical trial success rates
- All t-based inference methods (CIs, tests) apply to proportions data with appropriate standard errors

**Software Implementation:**
- Python: `scipy.stats.t` for probabilities and critical values, `ttest_1samp()` for hypothesis tests
- R functions: `pt()` for probabilities, `qt()` for critical values
- Excel functions: TDIST, TINV for t distribution calculations
- Always report: sample size n, sample mean x̄, standard deviation s, standard error se(x̄)
- For hypothesis tests, report: H₀ and H_a, significance level α, test statistic t, p-value, conclusion
- For confidence intervals, report: confidence level, point estimate, CI bounds

**Practical Guidelines:**
- Larger samples give smaller standard errors and narrower confidence intervals
- Standard error decreases with √n, so doubling precision requires quadrupling sample size
- α = 0.05 is conventional but not sacred; adjust based on consequences of errors
- Small p-values (p < 0.05) indicate statistical significance, not necessarily practical importance
- "Do not reject H₀" ≠ "accept H₀"; it means insufficient evidence against H₀
- Statistical significance vs. practical significance: large samples detect tiny, meaningless effects
- Always report point estimates and confidence intervals, not just hypothesis test results
- The t distribution is robust to moderate departures from normality, especially for large samples
- For very small samples (n < 15), normality assumption becomes more critical

---

### Some in-class Exercises

(1) Suppose observations in a sample of size 25 have mean 200 and standard deviation of 100 . Give the standard error of the sample mean.
(2) Suppose $n=100, \bar{x}=500$ and $s=400$. Provide an approximate $95 \%$ confidence interval for the population mean.
(1) Suppose observations in a sample of size 100 have mean 300 and standard deviation of 90 . Test the claim that the population mean equals 280 at the $5 \%$ significance level.


[^0]:    Similar to the standard normal but with fatter tails.

