# Chapter 4: Statistical Inference for the Mean

## Learning Objectives

By the end of this chapter, you will be able to:

- Understand how to extrapolate from sample mean x-bar to population mean mu using statistical inference
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
- Mean: sample mean x-bar
- Std. Dev.: standard error s measures the precision of x-bar as an estimate of mu.
- The next slides present methods for statistical inference on mu that are explained in detail in the remainder of the chapter.

**Key Concept: Sample Mean as Estimator**

The sample mean x-bar is an unbiased estimator of the population mean mu: the expected value of x-bar equals mu. The standard error se of x-bar equals s divided by the square root of n, which measures the precision of x-bar as an estimate of mu. With sample size n equals 171 and standard deviation s equals 25,527, the standard error is 1,952, indicating moderate precision in our estimate of mean earnings.

### 95% Confidence Interval for the Mean

- A 95 percent confidence interval for a parameter is a range of likely values that the parameter lies in with 95 percent confidence.
- 95 percent Confidence interval for mu:

Mean estimation
Number of obs equals 171

|  | Mean | Std. Err. | [95% Conf. Interval] |  |
| :--- | ---: | ---: | :--- | ---: |
| earnings | 41412.69 | 1952.103 | 37559.21 | 45266.17 |

- **Key statistics:**
  - Mean: sample mean x-bar is the estimate of mu
  - Std. Err: standard error measures the precision of x-bar as an estimate of mu
    - This equals s divided by the square root of n, which equals 25527.05 divided by the square root of 171, which equals 1952.1

### 95% Confidence Interval Calculation

- In general a confidence interval is

estimate plus-or-minus critical value times standard error

- Here we consider the population mean mu.
- The estimate is x-bar equals 41412.69
- The standard error measures the precision of x-bar as an estimate of mu
- se of x-bar equals s divided by the square root of n, which equals 25527.05 divided by the square root of 171, which equals 1952.1.
- The 95 percent critical value is approximately 2
- more precisely here c equals 1.974 as the probability that the absolute value of T-sub-170 is less than or equal to 1.974 equals 0.95.
- The 95 percent confidence interval is then

x-bar plus-or-minus c times se of x-bar, which equals 41412.69 plus-or-minus 1.974 times 1952.1, which equals the interval from 37559 to 45266.

### Critical Value for the Confidence Interval

- For mu use the T distribution with n minus 1 degrees of freedom
- very similar to standard normal distribution except with fatter tails.
- Let T-sub-n-minus-1 denote a random variable that is T of n minus 1 distributed.
- The critical value c for a 95 percent conf. interval is that value for which
- the probability that the absolute value of T-sub-n-minus-1 is less than or equal to c equals 0.95
- equivalently the probability that T-sub-n-minus-1 is greater than or equal to c equals 0.05 divided by 2, which equals 0.025.

Critical value for 95% conf. int.
![](https://cdn.mathpix.com/cropped/fc949097-0aa0-4241-b263-6c42fd6c818c-07.jpg?height=414&width=603&top_left_y=477&top_left_x=406)

### Hypothesis test on the Mean

- As illustrative example test whether or not mu equals 40,000.

One-sample t test

| Variable | Obs | Mean | Std. Err. | Std. Dev. | [95% Conf. Interval] |  |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| earnings | 171 | 41412.69 | 1952.103 | 25527.05 | 37559.21 | 45266.17 |


| mean = mean(earnings) |  | t equals 0.7237 |
| :--- | :--- | :--- |
| H-naught: mean equals 40000 |  | degrees of freedom equals 170 |
| H-a: mean less than 40000 | H-a: mean not equal to 40000 | H-a: mean greater than 40000 |
| Pr of T less than t equals 0.7649 | Pr of absolute value of T greater than absolute value of t equals 0.4703 | Pr of T greater than t equals 0.2351 |

- We test H-naught: mu equals 40000 against H-a: mu not equal to 40000.
- The test statistic is t equals 0.7237.
- The p-value is 0.4703 (as we test against H-a: mu not equal to 40000).
- Since p is greater than 0.05 we do not reject H-naught: mu equals 40000 at level 0.05.


### Hypothesis test calculation

- In general a t test statistic is

t equals the quantity estimate minus hypothesized value, divided by standard error.

- Here

t equals the quantity x-bar minus mu-naught, divided by se of x-bar, which equals the quantity 41412.69 minus 40000, divided by 1952.1, which equals 0.7237

- The p-value is the probability of observing a value at least as large as this in absolute value.
- Here p equals the probability that the absolute value of T-sub-170 is greater than or equal to 0.7237, which equals 0.4703.
- Since this probability exceeds 0.05 we do not reject H-naught.

**Key Concept: Confidence Intervals and Hypothesis Tests**

A 95% confidence interval provides a range of plausible values for mu: estimate plus-or-minus critical value times standard error. A hypothesis test uses the t-statistic t equals the quantity x-bar minus mu-naught, divided by se of x-bar, to evaluate whether a hypothesized value mu-naught is consistent with the data. The p-value measures how extreme the observed t-statistic is under H-naught. Here, with t equals 0.724 and p equals 0.470, we do not reject H-naught: mu equals 40,000 at the 5% level.

## 4.2 t Statistic and t distribution

- Estimate mu using x-bar which is the sample value of draw of the random variable X-bar
- So far we have the expected value of X-bar equals mu and the variance of X-bar equals sigma-squared over n for a simple random sample.
- For confidence intervals and hypothesis tests on mu we need a distribution
- under certain assumptions X-bar is normally distributed
- but with variance that depends on the unknown sigma-squared
- we replace sigma-squared by the estimate s-squared
- this leads to use of the t-statistic and the t distribution

[^0]
### Normal Distribution and the Central Limit Theorem

- We assume a simple random sample where
- A. X-sub-i has common mean mu: the expected value of X-sub-i equals mu for all i.
- B. X-sub-i has common variance sigma-squared: the variance of X-sub-i equals sigma-squared for all i.
- C. Statistical independence: X-sub-i is statistically independent of X-sub-j, i not equal to j.
- Then X-bar is distributed with mean mu and variance sigma-squared over n, i.e. X-bar has mean mu and variance sigma-squared over n.
- Under these assumptions the standardized variable Z equals the quantity X-bar minus mu, divided by the quantity sigma over the square root of n, is distributed with mean 0 and variance 1.
- The central limit theorem (a remarkable result) states that if additionally the sample size is large, Z is normally distributed

Z equals the quantity X-bar minus mu, divided by the quantity sigma over the square root of n, is distributed as N of 0 comma 1 as n approaches infinity.

### The t-statistic

- Now replace the unknown sigma-squared by an estimator S-squared equals 1 over n minus 1 times the sum from i equals 1 to n of the quantity X-sub-i minus X-bar, all squared.

T equals the quantity X-bar minus mu, divided by the quantity S over the square root of n

- The distribution for T is complicated. The standard approximation is T has the t distribution with n minus 1 degrees of freedom

T is distributed as T of n minus 1

- Comments
- different degrees of freedom correspond to different t distributions
- the term degrees of freedom is used because X-bar equals 1 over n times the sum from i equals 1 to n of X-sub-i implies that only n minus 1 terms in the sum are free to vary
- T is distributed as T of n minus 1 exactly in the very special case that X-sub-i's are normally distributed
- otherwise T is not T of n minus 1 exactly but is the standard approximation.

**Key Concept: The t Distribution**

The t distribution is similar to the standard normal N of 0 comma 1 but with fatter tails. The t-statistic T equals the quantity X-bar minus mu, divided by the quantity S over the square root of n, follows a t distribution with n minus 1 degrees of freedom. As n increases, the t distribution approaches the standard normal distribution. For n greater than 30, t-sub-n-minus-1 comma 0.025 is approximately 2, giving the "two-standard-error rule" for approximate 95% confidence intervals.

### The t -statistic (continued)

- In summary, inference on mu is based on the sample t-statistic is

t equals the quantity x-bar minus mu, divided by se of x-bar, which equals the quantity x-bar minus mu, divided by the quantity s over the square root of n,

- x-bar is the sample mean
- se of x-bar is the standard error of x-bar
- s is the sample standard deviation.
- The statistic t is viewed as a realization of the T of n minus 1 distribution.


### The t Distribution

- t distribution has probability density function that is bell-shaped
- The probability that a is less than T which is less than b is the area under the curve between a and b
- The t distribution has fatter tails than the standard normal.
- T-sub-v denotes a random variable that has the T of v distribution.
- Different values of v correspond to different T distributions
- t-sub-infinity is the same as N of 0 comma 1.
![](https://cdn.mathpix.com/cropped/fc949097-0aa0-4241-b263-6c42fd6c818c-14.jpg?height=436&width=546&top_left_y=470&top_left_x=76)
![](https://cdn.mathpix.com/cropped/fc949097-0aa0-4241-b263-6c42fd6c818c-14.jpg?height=439&width=546&top_left_y=470&top_left_x=641)


### Probabilities for the t Distribution

- Probabilities are the area under the t probability density function.
- e.g. the probability that a is less than T which is less than b is the area under the curve from a to b
- Computing these probabilities requires a computer.
- The R function 1 minus pt of t comma v gives the probability that T-sub-v is greater than t
- e.g. the probability that T-sub-170 is greater than 0.724 equals 1 minus pt of 0.724 comma 170, which equals 0.235.
- Python: `1 - t.cdf(t, v)` using `scipy.stats` gives the probability that T-sub-v is greater than t


### Inverse Probabilities for the t Distribution

- For confidence intervals we need to find the inverse probability
- called a critical value.
- Definition: the inverse probability or critical value c equals t-sub-v comma alpha is that value such that the probability that a T of v distributed random variable exceeds t-sub-v comma alpha equals alpha.

The probability that T-sub-v is greater than t-sub-v comma alpha equals alpha

- i.e. the area in the right tail beyond t-sub-v comma alpha equals alpha.
- Example: the probability that T-sub-170 is greater than 1.654 equals 0.05, so c equals t-sub-170 comma 0.05 equals 1.654.
- The R function is qt of 1 minus a comma v, e.g. qt of 0.95 comma 170 equals 1.654.
- Python: `t.ppf(1-a, v)` using `scipy.stats` gives the critical value


### Inverse probabilities (continued)

- Left panel: the probability that T-sub-170 is greater than 1.654 equals 0.05, so t-sub-170 comma 0.05 equals 1.654.
- Right panel: the probability that negative 1.974 is less than T-sub-170 which is less than 1.974 equals 0.05
using the probability that T-sub-170 is greater than 1.974 equals 0.025 and t-sub-170 comma 0.025 equals 1.974.
![](https://cdn.mathpix.com/cropped/fc949097-0aa0-4241-b263-6c42fd6c818c-17.jpg?height=394&width=536&top_left_y=398&top_left_x=85)
![](https://cdn.mathpix.com/cropped/fc949097-0aa0-4241-b263-6c42fd6c818c-17.jpg?height=394&width=536&top_left_y=398&top_left_x=640)


## 4.3 Confidence Intervals

- For simplicity focus on 95 percent confidence intervals.
- A 95 percent confidence interval for the population mean is

x-bar plus-or-minus t-sub-n-minus-1 comma 0.025 times se of x-bar,

- x-bar is the sample mean
- t-sub-n-minus-1 comma 0.025 is exceeded by a T of n minus 1 random variable with probability 0.025
- se of x-bar equals s over the square root of n is the standard error of the sample mean.
- The area in the tails is 0.025 plus 0.025 equals 0.05
- leaving area 0.95 in the middle
- hence a 95 percent confidence interval.


### Example: Mean Annual Earnings

- Here x-bar equals 41413, se of x-bar equals s over the square root of n equals 1952, n equals 171, and t-sub-170 comma 0.025 equals 1.974.
- A 95 percent confidence interval (CI) is

Starting with x-bar plus-or-minus t-sub-n-minus-1 comma alpha over 2 times the quantity s over the square root of n, this equals 41413 plus-or-minus 1.974 times 1952, which equals 41413 plus-or-minus 3853, which gives the interval from 37560 to 45266.

- A 95 percent confidence interval for population mean earnings of thirty year-old female full-time workers is
- the interval from \$37,560 to \$45,266
- this was the result obtained earlier.


### Derivation of a 95% Confidence Intervals

- We derive a 95 percent confidence interval from first principles.
- For simplicity consider a sample with n equals 61, in which case n minus 1 equals 60 and t-sub-60 comma 0.025 equals 2.0003. Thus

the probability that negative 2.0003 is less than T-sub-60 which is less than 2.0003 equals 0.95.

- Round to the probability that negative 2 is less than T which is less than 2 equals 0.95, and substituting T equals the quantity X-bar minus mu, divided by the quantity S over the square root of n, yields

the probability that negative 2 is less than the quantity X-bar minus mu divided by the quantity S over the square root of n which is less than 2 equals 0.95.

- Convert to an interval that is centered on mu as follows

Starting with the probability that negative 2 is less than the quantity X-bar minus mu divided by the quantity S over the square root of n which is less than 2 equals 0.95,
then the probability that negative 2 times S over the square root of n is less than X-bar minus mu which is less than 2 times S over the square root of n equals 0.95, after multiplying by S over the square root of n,
then the probability that negative X-bar minus 2 times S over the square root of n is less than negative mu which is less than negative X-bar plus 2 times S over the square root of n equals 0.95, after subtracting X-bar,
then the probability that X-bar plus 2 times S over the square root of n is greater than mu which is greater than X-bar minus 2 times S over the square root of n equals 0.95, after multiplying by negative 1.

### Derivation (continued)

- Re-ordering the final inequality yields

the probability that X-bar minus 2 times S over the square root of n is less than mu which is less than X-bar plus 2 times S over the square root of n equals 0.95.

- Replace random variables by their observed values
- the interval from x-bar minus 2 times s over the square root of n to x-bar plus 2 times s over the square root of n is called a 95 percent confidence interval for mu.
- More generally with sample size n the critical value is t-sub-n-minus-1 comma 0.025.
- A 95 percent confidence interval is the interval from x-bar minus t-sub-n-minus-1 comma 0.025 times se of x-bar to x-bar plus t-sub-n-minus-1 comma 0.025 times se of x-bar.
- This is the confidence interval formula given earlier.


### What Level of Confidence?

- Ideally narrow confidence intervals with high level of confidence.
- But trade-off: more confidence implies wider interval
- e.g. 100 percent confidence is mu in the interval from negative infinity to positive infinity.
- What value of confidence should we use?
- no best value in general
- common to use a 95 percent confidence interval.
- A 100 times 1 minus alpha percent confidence interval for the population mean is

x-bar plus-or-minus t-sub-n-minus-1 comma a over 2 times the quantity s over the square root of n.

- alpha equals 0.05 (so alpha over 2 equals 0.025) gives a 95 percent confidence interval as 100 times 1 minus 0.05 equals 95.
- next most common are 90 percent (alpha equals 0.10) and 99 percent (alpha equals 0.01) confidence intervals


### Critical t values

- Table presents t-sub-v comma alpha over 2 for various confidence levels (alpha) and v equals n minus 1.
- The 95 percent confidence intervals critical values are bolded

| Confidence Level | 100 times 1 minus alpha | 90% | 95% | 99% |
| :--- | :---: | ---: | ---: | ---: |
| Area in both tails | alpha | 0.10 | 0.05 | 0.01 |
| Area in single tail | alpha over 2 | 0.05 | 0.025 | 0.005 |
| t value for v equals 10 | t-sub-10 comma alpha over 2 | 1.812 | 2.228 | 3.169 |
| t value for v equals 30 | t-sub-30 comma alpha over 2 | 1.697 | 2.042 | 2.750 |
| t value for v equals 100 | t-sub-100 comma alpha over 2 | 1.660 | 1.980 | 2.626 |
| t value for v equals infinity | t-sub-infinity comma alpha over 2 | 1.645 | 1.960 | 2.576 |
| standard normal value | z-sub-alpha over 2 | 1.645 | 1.960 | 2.576 |

- Note that t-sub-v comma 0.025 is approximately 2 for v greater than 30.
- An approximate 95 percent confidence interval for mu is therefore a two-standard error interval
- the sample mean plus or minus two standard errors.


### Interpretation

- Interpretation of confidence intervals is conceptually difficult.
- The correct interpretation of a 95 percent confidence interval is that if constructed for each of an infinite number of samples then it will include mu 95 percent of the time
- of course we only have one sample.
- 1880 Census example (we know mu equals 24.13) in Chapter 3
- First sample of size 25: 95 percent confidence interval from 17.99 to 34.81
- Second sample: 95 percent CI from 13.12 to 25.54, and so on.
- For the particular 100 samples drawn
- two samples had 95 percent confidence intervals that did not include mu
- the 20th sample had 95 percent interval from 8.57 to 23.90
- the 50th sample had 95 percent interval from 11.49 to 21.45
- so here 98 percent of the samples had 95 percent confidence interval that included mu (versus theory 95 percent).


## 4.4 Two-Sided Hypothesis Tests

- A two-sided test or two-tailed test for the population mean is a test of the null hypothesis

H-naught: mu equals mu-star

where mu-star is a specified value for mu, against the alternative hypothesis

H-a: mu not equal to mu-star.

- In the next example mu-star equals 40000.
- Called two-sided as the alternative hypothesis includes both mu greater than mu-star and mu less than mu-star.
- We need to either reject H-naught or not reject H-naught.


### Significance Level of a Test

- A test either rejects or does not reject the null hypothesis.
- The decision made may be in error.
- A type I error occurs if H-naught is rejected when H-naught is true.
- e.g. H-naught is person is innocent. A type I error is to reject H-naught and find the person guilty, when in fact the person was innocent.
- The significance level of a test, denoted alpha, is the pre-specified maximum probability of a type I error that will be tolerated.
- Often alpha equals 0.05. A 5 percent chance of making a type I error.

**Key Concept: Significance Level and Type I Error**

The significance level alpha is the pre-specified maximum probability of Type I error (rejecting H-naught when it's true) that we're willing to tolerate. Commonly alpha equals 0.05 (5% significance level), meaning we accept a 1-in-20 chance of incorrectly rejecting a true null hypothesis. Lower alpha reduces Type I errors but makes it harder to detect true effects (increases Type II errors).

### The t-test Statistic

- Obviously reject H-naught: mu equals mu-star if x-bar is a long way from mu-star.
- Transform to t equals the quantity x-bar minus mu-star, divided by se of x-bar, as this has known distribution.
- Equivalently reject H-naught: if the t statistic is large in absolute value where

t equals the quantity x-bar minus mu-star, divided by se of x-bar, which equals the quantity x-bar minus mu-star, divided by the quantity s over the square root of n

- Example: Test whether or not population mean female earnings equal \$40,000.
- Here H-naught: mu equals 40000 and n equals 171, x-bar equals 41412, s equals 25527, so se of x-bar equals s over the square root of n equals 1952

t equals the quantity x-bar minus mu, divided by se of x-bar, which equals the quantity 41412 minus 40000, divided by 1952, which equals 0.724.

- The t-statistic is a draw from the T of 170 distribution, since n equals 171.


### Rejection Using p-values

- How likely are we to obtain a draw from T of 170 that is greater than or equal to the absolute value of 0.724?
- The p-value is the probability of observing a t-test statistic at least as large in absolute value as that obtained in the current sample.
- For a two-sided test of H-naught: mu equals mu-star against H-a: mu not equal to mu-star, the p-value is

p equals the probability that the absolute value of T-sub-n-minus-1 is greater than or equal to the absolute value of t

- H-naught is rejected at significance level alpha if p is less than alpha, and is not rejected otherwise.
- Earnings example
- p equals the probability that the absolute value of T-sub-170 is greater than or equal to 0.724, which equals 0.470.
- since p is greater than 0.05 we do not reject H-naught.
- Left panel: p-value
- Right panel: critical value
![](https://cdn.mathpix.com/cropped/fc949097-0aa0-4241-b263-6c42fd6c818c-29.jpg?height=390&width=534&top_left_y=314&top_left_x=85)

Two-sided test: critical value approach
![](https://cdn.mathpix.com/cropped/fc949097-0aa0-4241-b263-6c42fd6c818c-29.jpg?height=359&width=534&top_left_y=345&top_left_x=641)

### Rejection using Critical Regions

- Alternative equivalent method is the following
- base rejection directly on the value of the t-statistic
- requires table of critical values rather than computer for p-values.
- A critical region or rejection region is the range of values of t that would lead to rejection of H-naught at the specified significance level alpha.
- For a two-sided test of H-naught: mu equals mu-star against H-a: mu not equal to mu-star, and for specified alpha, the critical value c is such that

c equals t-sub-n-minus-1 comma alpha over 2 (so equivalently the probability that the absolute value of T-sub-n-minus-1 is greater than or equal to c equals alpha)

- H-naught is rejected at significance level alpha if the absolute value of t is greater than c, and is not rejected otherwise.
- Earnings example:
- if alpha equals 0.05 then c equals t-sub-170 comma 0.025 equals 1.974.
- do not reject H-naught since t equals 0.724 and the absolute value of 0.724 is less than 1.974.
- The critical value is illustrated in right panel of the preceding figure.


### Which Significance level?

- Decreasing the significance level alpha
- decreases the area in the tails that defines the rejection region
- makes it less likely that H-naught is rejected.
- It is most common to use alpha equals 0.05, called a test at the 5 percent significance level
- then a type I error is made 1 in 20 times.
- This is a convention and in many applications other values of alpha may be warranted.
- e.g. What if H-naught: no nuclear war? Then use alpha greater than 0.05.
- Reporting p-values allows the reader to easily test using their own preferred value of alpha.
- Further discussion under test power.


### Relationship to Confidence Intervals

- Two-sided tests can be implemented using confidence intervals.
- If the H-naught value mu-star falls inside the 100 times 1 minus alpha percent confidence interval then do not reject H-naught at level alpha.
- Otherwise reject H-naught at significance level alpha.


### Summary

- A summary of the preceding example is the following.

| Hypotheses | H-naught: mu equals 40000, H-a: mu not equal to 40000, alpha equals 0.05 |
| :--- | :--- |
| Significance level | alpha equals 0.05 |
| Sample data | x-bar equals 41412, s equals 25527, n equals 171 |
| Test statistic | t equals the quantity 41412 minus 40000, divided by the quantity 25527 over the square root of 171, which equals 0.724 |
| (1) p-value approach | p equals the probability that the absolute value of T-sub-170 is greater than or equal to the absolute value of 0.724, which equals 0.470. Do not reject H-naught at level 0.05 as p is greater than 0.05 |
| (2) Critical value approach | c equals t-sub-170 comma 0.025 equals 1.974. Do not reject H-naught at level 0.05 as the absolute value of t is less than c. |

- The p-value and critical value approaches are alternative methods that lead to the same conclusion.

**Key Concept: P-values and Hypothesis Testing**

The p-value is the probability of observing a test statistic at least as extreme as the one obtained, assuming H-naught is true. For two-sided tests, p equals the probability that the absolute value of T-sub-n-minus-1 is greater than or equal to the absolute value of t. Small p-values (p less than alpha) provide strong evidence against H-naught, leading to rejection. The p-value approach and critical value approach always give the same conclusion—they're just two equivalent ways to implement the same test.

## 4.5 Hypothesis Testing Example 1: Gasoline Prices

- Test at alpha equals 0.05 claim that the price of regular gasoline in Yolo County is neither higher nor lower than the norm for California.
- one day's data from a website that provides daily data on gas prices
- average California price that day was \$3.81
- H-naught: mu equals 3.81 is tested against H-a: mu not equal to 3.81.
- n equals 32, x-bar equals 3.6697 and s equals 0.1510.
- t equals the quantity 3.6697 minus 3.81, divided by the quantity 0.1510 over the square root of 32, which equals negative 5.256.
- p value method: p equals the probability that the absolute value of T-sub-31 is greater than 5.256, which equals 0.000
- reject H-naught at level 0.05 since p is less than 0.05.
- Critical value method: c equals t-sub-31 comma 0.025 equals 2.040.
- reject H-naught at level 0.05 since the absolute value of t equals 5.256 is greater than c equals 2.040.
- Reject the claim that reject the claim that population mean Yolo County gas price equals the California state-average price.


### Example 2: Male Earnings

- Test at alpha equals 0.05 the claim that population mean annual earnings for 30 year-old U.S. men with earnings in 2010 exceed \$50,000
- claim that greater than 50000 is set up as the alternative hypothesis
- H-naught: mu less than or equal to 50000 is tested against H-a: mu greater than 50000.
- n equals 191, x-bar equals 52353.93 and s equals 65034.74.
- t equals the quantity 52353.93 minus 50000, divided by the quantity 65034.74 over the square root of 191, which equals 0.5002.
- p value method: p equals the probability that T-sub-190 is greater than 0.500, which equals 0.310.
- do not reject H-naught at level 0.05 since p is greater than 0.05.
- Critical value method: c equals t-sub-190 comma 0.05 equals 1.653.
- do not reject H-naught at level 0.05 since t equals 0.500 is greater than c equals 1.653.
- Do not reject the claim that population mean earnings exceed \$50,000.


### Example 3: Price Inflation

- Test at alpha equals 0.05 claim that U.S. real GDP per capita grew on average at 2.0 percent over the period 1960 to 2020
- use year-to-year percentage changes in U.S. real GDP per capita.
- H-naught: mu equals 2.0 tested against H-a: mu not equal to 2.0.
- n equals 241, x-bar equals 1.9904 and s equals 2.1781.
- t equals the quantity 1.9904 minus 2.0, divided by the quantity 2.1781 over the square root of 241, which equals negative 0.068.
- p value method: p equals the probability that the absolute value of T-sub-258 is greater than 0.0680, which equals 0.946
- do not reject H-naught at level 0.05 since p is less than 0.05.
- Critical value method: c equals t-sub-241 comma 0.025 equals 1.970
- do not reject H-naught at level 0.05 since the absolute value of t equals 0.068 is less than c equals 1.970.
- Do not reject the claim that population mean growth was 2.0 percent.


## 4.6 One-sided Directional Hypothesis Tests

- An upper one-tailed alternative test is a test of H-naught: mu less than or equal to mu-star against H-a: mu greater than mu-star.
- A lower one-tailed alternative test is a test of H-naught: mu greater than or equal to mu-star against H-a: mu less than mu-star.
- For one-sided tests the statement being tested is specified to be the alternative hypothesis.
- And if a new theory is put forward to supplant an old, the new theory is specified to be the alternative hypothesis.
- Example: Test claim that population mean earnings exceed \$40,000
- test H-naught: mu less than or equal to 40000 against H-a: mu greater than 40000.


### P-Values and Critical Regions

- Use the usual t-test statistic t equals the quantity x-bar minus mu-star, divided by se of x-bar.
- For an upper one-tailed alternative test
- p equals the probability that T-sub-n-minus-1 is greater than or equal to t is p-value
- c equals t-sub-n-minus-1 comma alpha is critical value at significance level alpha
- reject H-naught if p is less than alpha or, equivalently, if t is greater than c.
- For a lower one-tailed alternative test
- p equals the probability that T-sub-n-minus-1 is less than or equal to t is p-value
- c equals negative t-sub-n-minus-1 comma alpha is critical value at significance level alpha
- H-naught if p is less than alpha or, equivalently, if t is less than c.


### Example: Mean Annual Earnings

- Evaluate the claim that the population mean exceeds \$40,000.
- Test of H-naught: mu less than or equal to 40000 against H-a: mu greater than 40000
- the claim is specified to be the alternative hypothesis
- a detailed explanation is given next
- and we reject if t is large and positive.
- From earlier t equals 0.724.
- p value method: p equals the probability that T-sub-170 is greater than or equal to 0.724, which equals 0.235
- do not reject H-naught at level 0.05 since p is greater than 0.05.
- Critical value method: c equals t-sub-170 comma 0.05 equals 1.654
- do not reject H-naught at level 0.05 since t equals 0.724 is less than c equals 1.654.
- Left panel: p-value
- Right panel: critical value
![](https://cdn.mathpix.com/cropped/fc949097-0aa0-4241-b263-6c42fd6c818c-40.jpg?height=420&width=574&top_left_y=325&top_left_x=61)

One-sided test: critical v alue approach
![](https://cdn.mathpix.com/cropped/fc949097-0aa0-4241-b263-6c42fd6c818c-40.jpg?height=383&width=571&top_left_y=358&top_left_x=653)

### Specifying the Null Hypothesis in One-sided Test

- Suppose claim is that population mean earnings exceed \$40,000.
- Potential method 1: test H-naught: mu less than or equal to 40000 against H-a: mu greater than 40000
- Reject H-naught if x-bar quite a bit higher than 40000. e.g. 43,000.
- Then claim that mu is greater than 40000 is supported if x-bar is greater than 43000.
- Potential method 2: test H-naught: mu greater than or equal to 40000 against H-a: mu less than 40000
- Reject H-naught if x-bar quite a bit smaller than than 40000. e.g. 37,000.
- So do not reject H-naught if x-bar is greater than 37000.
- Then claim that mu is greater than 40000 is supported if x-bar is greater than 37000
- Much more likely to accept the claim than with method 1.
- The statistics philosophy: need strong evidence to support a claim
- the first specification is therefore used
- the statement being tested is specified to be the alternative hypothesis.

**Key Concept: One-sided vs. Two-sided Tests**

One-sided tests have directional alternatives: H-naught: mu less than or equal to mu-star vs. H-a: mu greater than mu-star (upper tail) or H-naught: mu greater than or equal to mu-star vs. H-a: mu less than mu-star (lower tail). The claim being tested is always specified as the alternative hypothesis, requiring strong evidence to support it. One-sided tests use half the tail area: p equals the probability that T-sub-n-minus-1 is greater than or equal to t for upper tail tests, with critical value c equals t-sub-n-minus-1 comma alpha (not t-sub-n-minus-1 comma alpha over 2 as in two-sided tests).

## 4.7 Generalize Confidence Intervals and Hypothesis Tests

- Consider general case of an estimate of a parameter
- with standard error the estimated standard deviation of the estimate
- generalizes x-bar is an estimate of mu with standard error se of x-bar.
- For the models and assumptions considered in this book

t equals the quantity estimate minus parameter, divided by standard error, is distributed as T of v distribution

where the degrees of freedom v vary with the setting.

- The 100 times 1 minus alpha percent confidence interval for the unknown parameter is

estimate plus-or-minus t-sub-v comma alpha over 2 times standard error.

- Most often use 95 percent confidence level and t-sub-v comma 0.025 is approximately 2 for v greater than 30.
- So an approximate 95 percent CI is a two-standard error interval

estimate plus-or-minus 2 times standard error.

- Margin of error in general is half the width of a confidence interval.
- For 95 percent confidence intervals, since t-sub-v comma 0.025 is approximately 2,

Margin of error is approximately 2 times Standard error.

### Generalization of Hypothesis Tests

- Two-sided test at significance level alpha of
- H-naught: a parameter equals a hypothesized value against
- H-a: that it does not.
- Calculate the t-statistic

t equals the quantity estimate minus hypothesized parameter value, divided by standard error.

- under H-naught, t is the sample realization of a T of v random variable.
- Two-sided hypothesis test at significance level alpha:
- p-value approach: reject H-naught if p is less than alpha where p equals the probability that the absolute value of T-sub-v is greater than t
- critical value approach: reject H-naught if the absolute value of t is greater than c where c equals t-sub-v comma alpha over 2 satisfies the probability that T-sub-v is greater than t-sub-v comma alpha over 2 equals alpha
- the two methods lead to the same conclusion.


## 4.8 Proportions Data

- Consider proportion of respondents voting Democrat.
- Code data as x-sub-i equals 1 if vote Democrat and x-sub-i equals 0 if vote Republican
- The sample mean x-bar is the proportion voting Democrat
- The sample variance s-squared equals n times x-bar times 1 minus x-bar, all divided by n minus 1
  - In this special case of binary data

- **Example:** 480 of 921 voters intend to vote Democrat (and 441 vote Republican)
- x-bar equals the quantity 480 times 1 plus 440 times 0, all divided by 921, which equals 0.5212
- s-squared equals 921 times 0.5212 times the quantity 1 minus 0.5212, all divided by 920, which equals 0.2498.


### Inference for Proportions Data

- View each outcome as result of random variable

X equals 1 with probability p if vote Democrat, and equals 0 with probability 1 minus p if vote Republican

- Then X-bar has mean p and variance sigma-squared over n equals p times 1 minus p, all divided by n.
- Can do analysis using earlier results with the usual standard error of x-bar
- here s-squared over n equals n times x-bar times 1 minus x-bar, divided by n minus 1, which equals x-bar times 1 minus x-bar, all divided by n minus 1
- But usually confidence intervals substitute x-bar for p in sigma-squared over n equals p times 1 minus p, all divided by n
- so standard error of x-bar is the square root of x-bar times 1 minus x-bar, all divided by n
- And hypothesis tests of H-naught: p equals p-star also substitute for p and use

t equals the quantity x-bar minus p-star, divided by the square root of the quantity p-star times 1 minus p-star, all divided by n

**Key Concept: Inference for Proportions**

For binary data (x-sub-i equals 1 or 0), the sample mean x-bar equals the sample proportion. The sample variance has the special form s-squared equals n times x-bar times 1 minus x-bar, all divided by n minus 1. For confidence intervals, use standard error se of x-bar equals the square root of x-bar times 1 minus x-bar, all divided by n. For hypothesis tests of H-naught: p equals p-star, use se equals the square root of p-star times 1 minus p-star, all divided by n, substituting the hypothesized proportion p-star rather than the sample proportion.

### Computing the p-value and Critical Value

- Example of computer commands to get p and c
- for t equals t, degrees of freedom v, and test at level alpha
- Two-sided tests
- R: p equals 2 times the quantity 1 minus pt of the absolute value of t comma v, and c equals qt of 1 minus alpha over 2 comma v
- Python: `p = 2 * (1 - t.cdf(abs(t), v))` and `c = t.ppf(1 - alpha/2, v)` using `scipy.stats`
- Excel: p equals TDIST of the absolute value of t comma v comma 2, and c equals TINV of 2 times alpha comma v

---

## Key Takeaways

**Introduction to Statistical Inference (Section 4.1):**
- Statistical inference extrapolates from sample statistics to population parameters
- The sample mean x-bar is an unbiased estimator of the population mean mu: the expected value of x-bar equals mu
- The standard error se of x-bar equals s over the square root of n, which measures the precision of x-bar as an estimate of mu
- Confidence intervals provide a range of plausible values for mu given the sample data
- Hypothesis tests evaluate whether specific values of mu are consistent with the data
- Example: With n equals 171 female workers, x-bar equals \$41,413, s equals \$25,527, giving se of x-bar equals \$1,952
- 95% confidence interval for mean earnings: from \$37,559 to \$45,266
- Hypothesis test H-naught: mu equals \$40,000 yields t equals 0.724, p equals 0.470, therefore do not reject H-naught
- Methods developed for the mean mu generalize to inference on other parameters

**The t-statistic and t Distribution (Section 4.2):**
- For simple random samples: x-bar is distributed with mean mu and variance sigma-squared over n, meaning x-bar has mean mu and variance sigma-squared over n
- The Central Limit Theorem: as n approaches infinity, the standardized variable Z equals the quantity x-bar minus mu, divided by the quantity sigma over the square root of n, is distributed as N of 0 comma 1
- Since sigma is unknown, replace with sample estimate s to get the t-statistic: t equals the quantity x-bar minus mu, divided by the quantity s over the square root of n
- The t-statistic follows the t distribution with n minus 1 degrees of freedom: T is distributed as T of n minus 1
- The t distribution is bell-shaped like the standard normal but with fatter tails
- As degrees of freedom increase, the t distribution converges to N of 0 comma 1
- For n greater than 30, t-sub-n-minus-1 comma 0.025 is approximately 2, giving the "two-standard-error rule" for approximate 95% CIs
- The T of n minus 1 distribution is exact if data are normally distributed, otherwise it's an approximation
- R functions: 1 minus pt of t comma v for probabilities, qt of 1 minus alpha comma v for critical values
- Python functions: `scipy.stats.t.cdf(t, v)` for probabilities, `scipy.stats.t.ppf(1-α, v)` for critical values

**Confidence Intervals (Section 4.3):**
- A 95% confidence interval for mu: x-bar plus-or-minus t-sub-n-minus-1 comma 0.025 times se of x-bar
- General form: estimate plus-or-minus critical value times standard error
- The critical value t-sub-n-minus-1 comma alpha over 2 satisfies the probability that the absolute value of T-sub-n-minus-1 is less than or equal to t-sub-n-minus-1 comma alpha over 2 equals 1 minus alpha
- For 95% CI, alpha equals 0.05, so alpha over 2 equals 0.025, giving confidence level 100 times 1 minus 0.05 percent equals 95%
- Common confidence levels: 90% (alpha equals 0.10), 95% (alpha equals 0.05), 99% (alpha equals 0.01)
- Tradeoff: higher confidence leads to wider interval; narrow interval leads to less confidence
- 100% confidence gives useless interval from negative infinity to positive infinity
- Interpretation: If we constructed 95% CIs for infinite samples, 95% would contain mu
- We only have one sample, so we're "95% confident" this particular interval contains mu
- Example: 95% CI for mean earnings equals \$41,413 plus-or-minus 1.974 times \$1,952, which equals the interval from \$37,560 to \$45,266
- Margin of error approximately equals 2 times standard error for 95% CIs (since t-sub-v comma 0.025 is approximately 2 for v greater than 30)

**Two-Sided Hypothesis Tests (Section 4.4):**
- Null hypothesis: H-naught: mu equals mu-star tests whether mu equals a specified value mu-star
- Alternative hypothesis: H-a: mu not equal to mu-star (two-sided because includes both mu greater than mu-star and mu less than mu-star)
- Test statistic: t equals the quantity x-bar minus mu-star, divided by se of x-bar, which equals the quantity x-bar minus mu-star, divided by the quantity s over the square root of n
- Under H-naught, t follows the T of n minus 1 distribution
- **Significance level alpha**: pre-specified maximum probability of Type I error (rejecting true H-naught)
- Type I error: rejecting H-naught when it's true (false positive)
- Type II error: failing to reject H-naught when it's false (false negative, not controlled by alpha)
- Common significance level: alpha equals 0.05 (5% level), accepting 1-in-20 chance of Type I error
- **P-value**: probability of observing test statistic at least as extreme as obtained, assuming H-naught true
- For two-sided test: p equals the probability that the absolute value of T-sub-n-minus-1 is greater than or equal to the absolute value of t
- **P-value approach**: Reject H-naught if p is less than alpha; otherwise do not reject
- **Critical value approach**: Reject H-naught if the absolute value of t is greater than c where c equals t-sub-n-minus-1 comma alpha over 2
- Both approaches give identical conclusions—they're equivalent methods
- Relationship to CIs: if mu-star falls inside the 100 times 1 minus alpha percent CI, do not reject H-naught at level alpha
- Reporting p-values allows readers to test using their own preferred alpha

**Hypothesis Testing Examples (Section 4.5):**
- **Example 1 - Gasoline prices**: H-naught: mu equals \$3.81, n equals 32, x-bar equals \$3.67, s equals \$0.15, t equals negative 5.256, p equals 0.000
  - Reject H-naught at 5% level: strong evidence Yolo County prices differ from California average
- **Example 2 - Male earnings**: H-naught: mu less than or equal to \$50,000 vs. H-a: mu greater than \$50,000 (one-sided), n equals 191, t equals 0.500, p equals 0.310
  - Do not reject H-naught: insufficient evidence that mean male earnings exceed \$50,000
- **Example 3 - GDP growth**: H-naught: mu equals 2.0% vs. H-a: mu not equal to 2.0%, n equals 241, t equals negative 0.068, p equals 0.946
  - Do not reject H-naught: data consistent with 2.0% average annual growth rate
- These examples demonstrate typical applications across different contexts
- Large absolute value of t (far from 0) and small p-values (p less than 0.05) lead to rejection
- Small absolute value of t (close to 0) and large p-values (p greater than 0.05) fail to reject H-naught

**One-Sided Hypothesis Tests (Section 4.6):**
- **Upper one-tailed test**: H-naught: mu less than or equal to mu-star vs. H-a: mu greater than mu-star
- **Lower one-tailed test**: H-naught: mu greater than or equal to mu-star vs. H-a: mu less than mu-star
- The claim being tested is always specified as the alternative hypothesis (requires strong evidence)
- For upper tail: p equals the probability that T-sub-n-minus-1 is greater than or equal to t; reject if t is greater than c where c equals t-sub-n-minus-1 comma alpha (not alpha over 2!)
- For lower tail: p equals the probability that T-sub-n-minus-1 is less than or equal to t; reject if t is less than negative c where c equals t-sub-n-minus-1 comma alpha
- One-sided tests use only one tail, so critical values differ from two-sided tests
- Example: Testing mu greater than \$40,000, t equals 0.724, p equals the probability that T-sub-170 is greater than or equal to 0.724 equals 0.235, which is greater than 0.05, therefore do not reject
- Why put claim in H-a? Statistics requires strong evidence to support a claim
- Setting claim as H-a means we only accept it when evidence is compelling (low p-value)
- One-sided tests have more power than two-sided tests for detecting effects in the specified direction

**Generalization of Methods (Section 4.7):**
- General t-statistic: t equals the quantity estimate minus parameter value, divided by standard error
- Under H-naught, t is distributed as T of v distribution where degrees of freedom v varies by setting
- General 100 times 1 minus alpha percent confidence interval: estimate plus-or-minus t-sub-v comma alpha over 2 times standard error
- Approximate 95% CI: estimate plus-or-minus 2 times standard error (for v greater than 30)
- General two-sided test at level alpha:
  - P-value approach: reject H-naught if p is less than alpha where p equals the probability that the absolute value of T-sub-v is greater than the absolute value of t
  - Critical value approach: reject H-naught if the absolute value of t is greater than c where c equals t-sub-v comma alpha over 2
- These methods extend to regression coefficients, differences in means, correlation coefficients, etc.
- Margin of error approximately equals 2 times standard error for 95% confidence intervals

**Inference for Proportions (Section 4.8):**
- For binary data: x-sub-i equals 1 (success) or x-sub-i equals 0 (failure), with population proportion p
- Sample mean x-bar equals the sample proportion: x-bar equals number of successes divided by n
- Sample variance: s-squared equals n times x-bar times 1 minus x-bar, all divided by n minus 1, in this special case
- Random variable X has expected value of X equals p and variance of X equals p times 1 minus p
- Sample mean x-bar has expected value of x-bar equals p and variance of x-bar equals p times 1 minus p, all divided by n
- **For confidence intervals**: use se of x-bar equals the square root of x-bar times 1 minus x-bar, all divided by n (substitute x-bar for p in variance formula)
- **For hypothesis tests** of H-naught: p equals p-star: use se equals the square root of p-star times 1 minus p-star, all divided by n (substitute p-star not x-bar)
- Example: 480 of 921 voters intend to vote Democrat: x-bar equals 0.5212, s-squared equals 0.2498
- Methods for proportions apply to: election polling, quality control, medical trial success rates
- All t-based inference methods (CIs, tests) apply to proportions data with appropriate standard errors

**Software Implementation:**
- Python: `scipy.stats.t` for probabilities and critical values, `ttest_1samp()` for hypothesis tests
- R functions: `pt()` for probabilities, `qt()` for critical values
- Excel functions: TDIST, TINV for t distribution calculations
- Always report: sample size n, sample mean x-bar, standard deviation s, standard error se of x-bar
- For hypothesis tests, report: H-naught and H-a, significance level alpha, test statistic t, p-value, conclusion
- For confidence intervals, report: confidence level, point estimate, CI bounds

**Practical Guidelines:**
- Larger samples give smaller standard errors and narrower confidence intervals
- Standard error decreases with the square root of n, so doubling precision requires quadrupling sample size
- alpha equals 0.05 is conventional but not sacred; adjust based on consequences of errors
- Small p-values (p less than 0.05) indicate statistical significance, not necessarily practical importance
- "Do not reject H-naught" does not equal "accept H-naught"; it means insufficient evidence against H-naught
- Statistical significance vs. practical significance: large samples detect tiny, meaningless effects
- Always report point estimates and confidence intervals, not just hypothesis test results
- The t distribution is robust to moderate departures from normality, especially for large samples
- For very small samples (n less than 15), normality assumption becomes more critical

---

### Some in-class Exercises

(1) Suppose observations in a sample of size 25 have mean 200 and standard deviation of 100. Give the standard error of the sample mean.
(2) Suppose n equals 100, x-bar equals 500 and s equals 400. Provide an approximate 95 percent confidence interval for the population mean.
(1) Suppose observations in a sample of size 100 have mean 300 and standard deviation of 90. Test the claim that the population mean equals 280 at the 5 percent significance level.


[^0]:    Similar to the standard normal but with fatter tails.
