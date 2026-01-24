# Chapter 3: The Sample Mean

## Learning Objectives

By the end of this chapter, you will be able to:

- Define random variables and distinguish between random variables (upper case) and their realizations (lower case)
- Calculate the mean, variance, and standard deviation of a random variable from its probability distribution
- Understand the sample mean $\bar{x}$ as a realization of the random variable $\bar{X}$
- Derive the mean and variance of the sample mean under simple random sampling assumptions
- Apply the Central Limit Theorem to show that $\bar{X}$ is approximately normally distributed for large samples
- Calculate and interpret the standard error of the sample mean se($\bar{X}$) = s/√n
- Distinguish between parameters, estimators, and estimates in statistical inference
- Evaluate estimators using criteria of unbiasedness, consistency, and efficiency
- Apply sampling methods to both experimental data (coin tosses) and real populations (Census data)
- Use statistical software to generate random samples and compute sample statistics

---


## 3.1 Random Variables

- A random variable is a variable whose value is determined by the outcome of an experiment.
- An experiment is an operation whose outcome cannot be predicted with certainty.
- Example: the experiment is tossing a coin and the random variable takes value 1 if heads and 0 if tails.
- Example: the experiment is randomly selecting a person from the population and the associated random variable takes value equal to their annual earnings.
- Standard notation
- $X$ (or $Y$ or $Z$ ) denotes a random variable
- $x$ (or $y$ or $z$ ) denotes the values taken by $X$ (or $Y$ or $Z$ ).


### Example: Coin toss

- Simplest case is a random variable that takes one of only two possible values.
- Consider toss of fair coin with $X=1$ if heads and $X=0$ if tails. Then

$$
X= \begin{cases}0 & \text { with probability } 0.5 \\ 1 & \text { with probability } 0.5 .\end{cases}
$$

### Mean of a Random Variable

- Mean of $X$, denoted $\mu$ or $\mu_{X}$
- is the probability-weighted average of all possible values of $X$ in the population.
- $\mu$ is also denoted $\mathrm{E}[X]$
- the expected value of the random variable $X$
- the long-run average value expected if we draw a value of $X$ at random, draw a second value of $X$ at random, and so on, and then obtain the average of these values.

$$
\begin{aligned}
\mu \equiv \mathrm{E}[X] & =x_{1} \times \operatorname{Pr}\left[X=x_{1}\right]+x_{2} \times \operatorname{Pr}\left[X=x_{2}\right]+\cdots \\
& =\sum_{x} x \cdot \operatorname{Pr}[X=x]
\end{aligned}
$$

- Note that
- $\sum_{x}$ means the sum over all possible values $x$ can take
- and the possible values of $x$ are denoted $x_{1}, x_{2}, x_{3}, \ldots$


### Example of Mean

- Fair coin toss: $X$ takes values 0 or 1 with equal probabilities

$$
\begin{aligned}
\mu & =\sum_{x} \times \times \operatorname{Pr}[X=x] \\
& =\operatorname{Pr}[X=0] \times 0+\operatorname{Pr}[X=1] \times 1 \\
& =0.5 \times 0+0.5 \times 1 \\
& =0.5
\end{aligned}
$$

- Unfair coin: $X=1$ with probability 0.6 and $X=0$ with probability 0.4
- $\mu=0 \times 0.4+1 \times 0.6=0.6$.


### Variance and Standard Deviation

- Variance $\sigma^{2}$
- measures the variability in $X$ around $\mu$
- equals the expected value of $(X-\mu)^{2}$, the squared deviation of $X$ from the mean $\mu$
- probability-weighted average of $x_{1}^{*}, x_{2}^{*}, \ldots$

$$
\begin{aligned}
\sigma^{2} & \equiv \mathrm{E}\left[(X-\mu)^{2}\right] \\
& =\left(x_{1}-\mu\right)^{2} \times \operatorname{Pr}\left[X=x_{1}\right]+\left(x_{2}-\mu\right)^{2} \times \operatorname{Pr}\left[X=x_{2}\right]+\cdots \\
& =\sum_{x}(x-\mu)^{2} \times \operatorname{Pr}[X=x] .
\end{aligned}
$$

- Population standard deviation $\sigma$ is square root of the variance
- measured in the same units as $X$.


### Example of Variance and Standard Deviation

- Fair coin toss: $X$ takes values 0 or 1 with equal probabilities so $\mu=0.5$.
- Variance

$$
\begin{aligned}
\sigma^{2} & =\sum_{x}(x-\mu)^{2} \times \operatorname{Pr}[X=x] \\
& =\operatorname{Pr}(0-0.5)^{2} \times[X=0]+(1-0.5)^{2} \times \operatorname{Pr}[X=1] \\
& =0.25 \times 0.5+0.25 \times 0.5 \\
& =0.25
\end{aligned}
$$

- Standard deviation

$$
\sigma=\sqrt{0.25} \simeq 0.5
$$

**Key Concept: Random Variables and Their Properties**

A random variable $X$ is a variable whose value is determined by the outcome of an unpredictable experiment. The mean $\mu = \mathrm{E}[X]$ is the probability-weighted average of all possible values, while the variance $\sigma^2 = \mathrm{E}[(X-\mu)^2]$ measures variability around the mean. These population parameters characterize the distribution from which we draw samples.

## 3.2 Random Samples

- A sample of size $n$ takes values denoted $x_{1}, \ldots, x_{n}$.
- These values are realizations or outcomes of the random variables $X_{1}, X_{2}, \ldots, X_{n}$.
- Example: four consecutive coin tosses with results tails, heads, heads and heads
- random variable $X_{1}$ has realized value $x_{1}=0$
- random variable $X_{2}$ takes value $x_{2}=1$
- random variable $X_{3}$ takes value $x_{3}=1$
- random variable $X_{4}$ takes value $x_{4}=1$.


### Sample Mean is a Random Variable

- Sample of size $n$ has observed values $x_{1}, x_{2}, \ldots, x_{n}$.
- These are realizations of the random variables $X_{1}, X_{2}, \ldots, X_{n}$.
- Sample mean is the average

$$
\bar{x}=\left(x_{1}+x_{2}+\cdots+x_{n}\right) / n=\frac{1}{n} \sum_{i=1}^{n} x_{i}
$$

- This is a realization of the random variable

$$
\bar{X}=\left(X_{1}+X_{2}+\cdots+X_{n}\right) / n=\frac{1}{n} \sum_{i=1}^{n} X_{i} .
$$

### Aside: Sample Variance and Standard Deviation

- Similarly any other sample statistic (such as the median) is a realization of a random variable
- In addition to the sample mean we focus on the sample variance and sample standard deviation.
- Sample variance is average of squared deviations of $x$ around $\bar{x}$
- not around $\mu$ since $\mu$ is unknown

$$
s^{2}=\frac{1}{n-1} \sum_{i=1}^{n}\left(x_{i}-\bar{x}\right)^{2}
$$

- The sample variance is a realization of the random variable

$$
S^{2}=\frac{1}{n-1} \sum_{i=1}^{n}\left(X_{i}-\bar{X}\right)^{2}
$$

- Taking the square root gives the sample standard deviation $s$ which is a realization of the random variable $S$.

**Key Concept: The Sample Mean as a Random Variable**

The observed sample mean $\bar{x}$ is a realization of the random variable $\bar{X} = (X_1 + \cdots + X_n)/n$. This fundamental insight means that $\bar{x}$ varies from sample to sample in a predictable way—its distribution can be characterized mathematically. This allows us to perform statistical inference about the population mean $\mu$.

## 3.3 Sample Generated from an Experiment: Coin Tosses

- We consider a simple experiment that generates many samples
- hence many sample means $\bar{x}$
- then summarize the resulting distribution of the many $\bar{x}$.
- Population: Outcomes from experiment of tossing a coin
- $X=1$ if heads and $X=0$ if tails
- Population mean $\mu=\mathrm{E}[X]=0.5$ and standard deviation $\sigma=0.5$.
- Sample: $n=30$
- random sample of size 30 from 30 coin tosses
- there are 10 heads and 20 tails, so $\bar{x}=10 / 30=0.333$
- histogram of this single sample is given in left panel of next slide.


### Example: Coin Tosses (continued)

- Left panel: $x$ 's from 1 sample of size 30 with 20 heads and 10 tails
- Right panel: $\bar{x}^{\prime} s$ for 400 samples of size 30

One Sample of Size 30
![](https://cdn.mathpix.com/cropped/72a3f87a-41ec-4ad3-a2db-effc82ed52f5-14.jpg?height=355&width=488&top_left_y=395&top_left_x=164)

400 Sample Means
![](https://cdn.mathpix.com/cropped/72a3f87a-41ec-4ad3-a2db-effc82ed52f5-14.jpg?height=355&width=485&top_left_y=395&top_left_x=690)

### Example: Coin Tosses (continued)

- Randomly draw 400 different samples, each of size 30
- then $\bar{x}_{1}=.333, \bar{x}_{2}=.500, \bar{x}_{3}=533, \ldots$.
- Histogram (plus kernel density estimate) for the 400 means from the 400 samples of size 30 is given in right panel of previous slide.
- Roughly centered on the population mean
  - The average of the 400 means is 0.499, close to $\mu=0.5$

- Much less variability in these 400 means than in the original population
  - The standard deviation of the 400 means is 0.086
  - Much less than the population standard deviation of $\sigma=0.5$

- The density estimate is roughly that of the normal


## 3.4 Properties of the Sample Mean

- The properties of $\bar{X}$ depend on the properties of $X_{1}, X_{2}, \ldots, X_{n}$
- such as the means and variances of $X_{1}, X_{2}, \ldots, X_{n}$
- and whether their values depend in part on other values.
- In this chapter we consider the simplest and standard set of assumptions in introductory statistics
- $X_{1}, X_{2}, \ldots, X_{n}$ have common mean $\mu$ and common variance $\sigma^{2}$
- $X_{1}, X_{2}, \ldots, X_{n}$ are statistically independent
  - Statistical independence means that the value taken by $X_{2}$, for example, is not influenced by the value taken by $X_{1}, X_{3}, \ldots, X_{n}$

- In later chapters we relax these assumptions
- e.g. regression allows for different means for different observations.


### Population Assumptions

- Population
- = set of all observations (or experimental outcomes).
- Sample
- = subset selected from the population.
- Properties of $\bar{x}$ depend on the random variable $\bar{X}$
- hence on assumptions about process generating $X_{1}, X_{2}, \ldots, X_{n}$.
- We assume a simple random sample where
- A. $X_{i}$ has common mean $\mu: \mathrm{E}\left[X_{i}\right]=\mu$ for all $i$.
- B. $X_{i}$ has common variance $\sigma^{2}: \operatorname{Var}\left[X_{i}\right]=\sigma^{2}$ for all $i$.
- C. $X_{i}$ is statistically independent of $X_{j}, i \neq j$.
- Shorthand notation: $X_{i} \sim\left(\mu, \sigma^{2}\right)$
- means $X_{i}$ are distributed with mean $\mu$ and variance $\sigma^{2}$.


### Mean and Variance of the Sample Mean

- Consider $\bar{X}=\left(X_{1}+X_{2}+\cdots+X_{n}\right) / n$ for $X_{i} \sim\left(\mu, \sigma^{2}\right)$.
- The (population) mean of the sample mean is

$$
\mu_{\bar{X}} \equiv \mathrm{E}[\bar{X}]=\mu .
$$

- The (population) variance of the sample mean is

$$
\sigma_{\bar{X}}^{2} \equiv \mathrm{E}\left[\left(\bar{X}-\mu_{\bar{X}}\right)^{2}\right]=\frac{\sigma^{2}}{n},
$$

- The (population) standard deviation is $\sigma_{\bar{X}}=\sigma / \sqrt{n}$.
- Sample mean is less variable than the underlying data
- since $\sigma_{\bar{X}}^{2}<\sigma^{2}$.
- Sample mean is close to $\mu$ as $n \rightarrow \infty$
- since $\mathrm{E}[\bar{X}]=\mu$ and variance $\sigma_{\bar{X}}^{2}=\sigma^{2} / n \rightarrow 0$ as $n \rightarrow \infty$.

**Key Concept: Mean and Variance of the Sample Mean**

Under simple random sampling (common mean $\mu$, common variance $\sigma^2$, independence), the sample mean $\bar{X}$ has mean $\mathrm{E}[\bar{X}] = \mu$ (unbiased) and variance $\operatorname{Var}[\bar{X}] = \sigma^2/n$ (decreases with sample size). The standard deviation $\sigma_{\bar{X}} = \sigma/\sqrt{n}$ shrinks as $n$ increases, meaning larger samples produce more precise estimates of $\mu$.

### Aside: Proof for Mean of the Sample Mean

- Recall

$$
\bar{X}=\left(X_{1}+X_{2}+\cdots+X_{n}\right) / n
$$

- Proof uses
- $\mathrm{E}[a X]=a \mathrm{E}[X]$
- $\mathrm{E}[X+Y]=\mathrm{E}[X]+\mathrm{E}[Y]$
and assumption A (common mean of $X_{i}$ ).
- Then

$$
\begin{aligned}
\mathrm{E}[\bar{X}] & =\mathrm{E}\left[\frac{1}{n}\left(X_{1}+X_{2}+\cdots+X_{n}\right)\right] \\
& =\frac{1}{n} \mathrm{E}\left[X_{1}+X_{2}+\cdots+X_{n}\right] \\
& =\frac{1}{n}\left\{\mathrm{E}\left[X_{1}\right]+\mathrm{E}\left[X_{2}\right]+\cdots+\mathrm{E}\left[X_{n}\right]\right\} \\
& =\frac{1}{n}\{\mu+\mu+\cdots+\mu\} \\
& =\mu .
\end{aligned}
$$

### Aside: Variance of the Population Mean

- Proof in Appendix B. 2 uses that
- $\operatorname{Var}[a X]=a^{2} \mathrm{E}[X]$ in general
- $\operatorname{Var}[X+Y]=\operatorname{Var}[X]+\operatorname{Var}[Y]$ for independent variables
- and assumptions A-C.
- Then

$$
\begin{aligned}
\operatorname{Var}[\bar{X}] & =\operatorname{Var}\left[\frac{1}{n}\left(X_{1}+X_{2}+\ldots+X_{n}\right)\right] \\
& =\left(\frac{1}{n}\right)^{2} \operatorname{Var}\left[X_{1}+X_{2}+\ldots+X_{n}\right] \\
& =\left(\frac{1}{n}\right)^{2}\left\{\operatorname{Var}\left[X_{1}\right]+\cdots+\operatorname{Var}\left[X_{n}\right]\right\} \\
& =\left(\frac{1}{n}\right)^{2} \sigma^{2}+\cdots+\left(\frac{1}{n}\right)^{2} \sigma^{2} \\
& =\left(\frac{1}{n}\right)^{2}\left\{\sigma^{2}+\cdots+\sigma^{2}\right\} \\
& =\left(\frac{1}{n}\right)^{2} \times n \sigma^{2} \\
& =\frac{1}{n} \sigma^{2}
\end{aligned}
$$

### Normal Distribution and the Central Limit Theorem

- We have shown to date that $\bar{X} \sim\left(\mu, \sigma^{2} / n\right)$
- In general, subtracting the mean and dividing by the standard deviation yields a random variable with mean 0 and variance 1 .
- So here the standardized variable

$$
Z=\frac{\bar{X}-\mu}{\sigma / \sqrt{n}} \sim(0,1) .
$$

- The central limit theorem (a remarkable result) proves normality as the sample size gets large

$$
Z \sim N(0,1) \text { as } n \rightarrow \infty .
$$

- The central limit theorem holds under assumptions A-C
- and also under some weaker conditions.

**Key Concept: The Central Limit Theorem**

The Central Limit Theorem states that the standardized sample mean $Z = (\bar{X} - \mu)/(\sigma/\sqrt{n})$ converges to a standard normal distribution N(0,1) as $n \rightarrow \infty$. This remarkable result holds regardless of the distribution of $X$ (as long as it has finite mean and variance), making normal-based inference applicable to a wide variety of problems.

### Normal Distribution (continued)

- Now convert back to the original $\bar{X}$.
- We have

$$
Z=\frac{\bar{X}-\mu}{\sigma / \sqrt{n}} \sim N(0,1) \text { as } n \rightarrow \infty .
$$

- Then $\bar{X}$ is approximately normally distributed in large samples

$$
\bar{X} \sim N\left(\mu, \sigma^{2} / n\right) \text { approximately for large } n .
$$

- We will use this result to do statistical inference on $\mu$.
- However, the variance $\sigma^{2} / n$ is unknown as $\sigma^{2}$ is unknown
- we will have to get an estimate
- replace $\sigma^{2}$ by its estimate $s^{2}$
- where $s$ is the sample standard deviation of $X$.


### Standard Error of the Sample Mean

- Estimated variance of $\bar{X}$ is

$$
s_{\bar{X}}^{2}=\frac{s^{2}}{n}=\frac{\frac{1}{n-1} \sum_{i}\left(x_{i}-\bar{x}\right)^{2}}{n},
$$

- Estimated standard deviation of $\bar{X}$

$$
s_{\bar{X}}=\frac{s}{\sqrt{n}}=\frac{\sqrt{\frac{1}{n-1} \sum_{i}\left(x_{i}-\bar{x}\right)^{2}}}{\sqrt{n}} .
$$

- $s_{\bar{X}}$ is called the standard error of the sample mean $\bar{X}$.
- The term "standard error" means estimated standard deviation
- various estimators each have a distinct standard error
- a reported "standard error" in computer output need not be $s_{\bar{X}}$.
- Use the notation

$$
\operatorname{se}(\bar{X})=s / \sqrt{n}
$$

**Key Concept: Standard Error**

The standard error se($\bar{X}$) = $s/\sqrt{n}$ is the estimated standard deviation of the sample mean. It measures the precision of $\bar{x}$ as an estimate of $\mu$. Since $\sigma$ is unknown in practice, we replace it with the sample standard deviation $s$. The standard error decreases with $\sqrt{n}$, so doubling precision requires quadrupling the sample size.

### Summary for the Sample Mean

(1) Sample values $x_{1}, \ldots, x_{n}$ are observed values of the random variables $X_{1}, \ldots, X_{n}$.
(2) Individual $X_{i}$ have common mean $\mu$ and variance $\sigma^{2}$ and are independent.
(3) Average $\bar{X}$ of $n$ draws of $X_{i}$ has mean $\mu$ and variance $\sigma^{2} / n$.
(4) Standardized statistic $Z=(\bar{X}-\mu) /(\sigma / \sqrt{n}) \sim(0,1)$ has mean 0 and variance 1.
(5) $Z$ is standard normal as size $n \rightarrow \infty$ by the central limit theorem.
(6) For large $n$ a good approximation is that $\bar{X} \sim N\left(\mu, \sigma^{2} / n\right)$
(1) The standard error of $\bar{X}$ equals $s / \sqrt{n}$, where "standard error" is general terminology for "estimated standard deviation".

## 3.5 Sampling from a Population: 1880 Census

- Now consider an example of sampling from a population.
- Population: $N=50,169,452$
- all people recorded as living in the U.S. in 1880
- the average age is 24.13 years, so $\boldsymbol{\mu}=\mathbf{2 4 . 1 3}$
- the standard deviation of age is 18.61 , so $\boldsymbol{\sigma}=\mathbf{1 8 . 6 1}$
- histogram is given in the next slide.


### Example: 1880 Census (continued)

- Population
- Probabilities decline with age (clearly not the normal)
- Peaks due to rounding at five and ten years

Entire 1880 Census
![](https://cdn.mathpix.com/cropped/72a3f87a-41ec-4ad3-a2db-effc82ed52f5-26.jpg?height=533&width=759&top_left_y=353&top_left_x=253)

### Example: 1880 Census (continued)

- Single sample: $n=25$
- random sample of size 25 from the entire U.S. population
- the average age is 27.84 , so $\overline{\mathbf{x}}=\mathbf{2 7 . 8 4}$
- the standard deviation of age is 20.71, so $\mathbf{s}=\mathbf{2 0 . 7 1}$
- these are similar to, but not exactly equal to, $\mu$ and $\sigma$
- histogram of $x^{\prime} s$ in a single sample is given in left panel of next slide.
- Many samples of size 25
- randomly draw 100 different samples, each of size 25
- then $\bar{x}_{1}=27.84, \bar{x}_{2}=19.40, \bar{x}_{3}=23.28$ years, $\ldots$.
- average of the 100 sample means is 23.78 , close to $\mu=24.13$.
- standard deviation of the 100 means is 3.76 , close to $\sigma / \sqrt{n}=18.61 / \sqrt{25}=3.72$.
- histogram of $\bar{x}^{\prime} s$ across 100 samples is given in right panel of next slide.


### Example: 1880 Census (continued)

- 100 different means from 100 different samples, each of size 25
- histogram (left) and kernel density estimate (right)
- looks like normal with mean $\mu$ and standard deviation much less than $\sigma$
![](https://cdn.mathpix.com/cropped/72a3f87a-41ec-4ad3-a2db-effc82ed52f5-28.jpg?height=433&width=538&top_left_y=387&top_left_x=82)
![](https://cdn.mathpix.com/cropped/72a3f87a-41ec-4ad3-a2db-effc82ed52f5-28.jpg?height=405&width=541&top_left_y=389&top_left_x=644)


## 3.6 Estimation of the Sample Mean

- Desire a good point estimate of population mean $\mu$
- why use $\bar{x}$ rather than some other estimate?
- A desirable estimator of $\mu$ has distribution
- centered on $\mu$
- with as little variability around $\mu$ as possible.


### Parameter, Estimator and Estimate

- A parameter is a constant that determines in part the distribution of $x$.
- An estimator is a method for estimating a parameter.
- An estimate is the particular value of the estimator obtained from the sample.
- For estimation of the mean of $X$ using the sample mean
- the parameter is $\mu$
- the estimator is the random variable $\bar{X}$
- the estimate is the sample value $\bar{x}$.


### Unbiased Estimators

- An unbiased estimator of a population parameter
- has expected value that equals the population parameter.
- The sample mean is unbiased for $\mu$
- since $\mathrm{E}[\bar{X}]=\mu$.


### Minimum Variance Estimators

- Other estimators may also be unbiased and consistent for $\mu$
- e.g. sample median in the case where $X$ is symmetrically distributed
- discriminate between such estimators using their variance.
- A best estimator or efficient estimator
- has minimum variance among the class of consistent estimators (or of unbiased estimators).
- Under assumptions A-C the sample mean has variance $\sigma^{2} / n$
- for $X$ that is normal, Bernoulli, binomial or Poisson no other unbiased estimator has lower variance
- for $X$ with other distributions the sample mean is often close to having the lowest variance
- generally the sample mean is used to estimate $\mu$.


### Consistent Estimators

- Consistency is a more advanced concept that considers behavior as the sample size goes to infinity.
- A consistent estimator of a population parameter
- is one that is almost certainly arbitrarily close to the population parameter as the sample size gets very large.
- A sufficient condition for consistency is
- any bias disappears as the sample size gets very large
- the variance goes to zero as the sample size gets very large
- The sample mean is consistent for $\mu$ under assumptions A-C
- it is unbiased
- the variance $\sigma_{\bar{X}}^{2}=\sigma^{2} / n \rightarrow 0$ as $n \rightarrow \infty$.

**Key Concept: Properties of Good Estimators**

A good estimator should be unbiased (E[$\bar{X}$] = $\mu$), consistent (converges to $\mu$ as $n \rightarrow \infty$), and efficient (minimum variance among unbiased estimators). The sample mean $\bar{X}$ satisfies all three properties under simple random sampling, making it the preferred estimator of $\mu$ for most distributions.

## 3.7 Samples other than Simple Random Samples

- Recall simple random sample means data are independent and from the same distribution.
- Representative Samples
- Still from same distribution but no longer statistically independent.
- Then can adapt methods using an alternative formula for $\operatorname{se}(\bar{x})$.
- Nonrepresentative samples
- Now different observations may have different $\mu$
- e.g. Survey readers of Golf Digest not representative of population.
- Big problem.
- Weighted mean can still be used if population weights are known
- $\pi_{i}=$ probability that $i^{t h}$ observation is included in the sample.
- sample weights $w_{i}=1 / \pi_{i}$
- weighted mean $\bar{x}_{w}=\left[\sum_{i=1}^{n} w_{i} x_{i}\right] /\left[\sum_{i=1}^{n} w_{i}\right]$.

**Key Concept: Nonrepresentative Samples**

Simple random sampling assumes all observations come from the same distribution with common mean $\mu$. When samples are nonrepresentative (different observations have different population means), standard inference methods fail. Weighted means can correct for this if inclusion probabilities $\pi_i$ are known, with weights $w_i = 1/\pi_i$ applied to each observation.

## 3.8 Computer Generation of a Random Variable

- A (pseudo) uniform random number generator
- creates values between 0 and 1
- any value between 0 and 1 is equally likely
- successive values appear to be independent of each other.
- To simulate 30 coin tosses
- draw 30 uniform random numbers
- result is heads if the uniform random number exceeds 0.5
- For Census example
- if uniform random number is between 0 and $1 / N$, where $N=$ 50,169,452, we choose the first person, etcetera
- The sequence depends on the starting value called the seed
- always set the seed (e.g. equal to 10101).


### Some in-class Exercises

(1) Suppose $X=100$ with probability 0.8 and $X=600$ with probability 0.2 . Find the mean, variance and standard deviation of $X$.
(2) Consider random samples of size 25 from the random variable $X$ that has mean 100 and variance 400 . Give the mean, variance and standard deviation of the mean $\bar{X}$.

---

## Key Takeaways

**Random Variables and Probability Distributions (Section 3.1):**
- A random variable $X$ is a variable whose value is determined by an unpredictable experimental outcome
- Standard notation: upper case ($X$, $Y$, $Z$) denotes random variables; lower case ($x$, $y$, $z$) denotes realized values
- The mean $\mu = \mathrm{E}[X]$ is the probability-weighted average of all possible values: $\mu = \sum_x x \cdot \operatorname{Pr}[X=x]$
- The variance $\sigma^2 = \mathrm{E}[(X-\mu)^2]$ measures variability around the mean: $\sigma^2 = \sum_x (x-\mu)^2 \cdot \operatorname{Pr}[X=x]$
- The standard deviation $\sigma = \sqrt{\sigma^2}$ is measured in the same units as $X$
- For a fair coin toss with $X \in \{0,1\}$: $\mu = 0.5$ and $\sigma = 0.5$
- For an unfair coin with Pr[$X=1$] = 0.6: $\mu = 0.6$ and $\sigma^2 = 0.24$

**Random Samples and the Sample Mean (Section 3.2):**
- Sample values $x_1, x_2, \ldots, x_n$ are realizations of random variables $X_1, X_2, \ldots, X_n$
- The sample mean $\bar{x} = (x_1 + \cdots + x_n)/n$ is a realization of the random variable $\bar{X} = (X_1 + \cdots + X_n)/n$
- Any sample statistic (mean, median, variance) is a realization of a random variable
- Sample variance: $s^2 = \frac{1}{n-1} \sum_{i=1}^n (x_i - \bar{x})^2$ (uses $n-1$ for unbiased estimation)
- Sample standard deviation: $s = \sqrt{s^2}$
- The "$n-1$" divisor (instead of $n$) corrects for downward bias when estimating $\sigma^2$ from sample data
- Both $s^2$ and $s$ are realizations of random variables $S^2$ and $S$

**Sampling Distribution Examples (Section 3.3):**
- Coin toss experiment: 400 samples of size 30, each produces a sample mean $\bar{x}$
- The 400 sample means have average 0.499 (close to population $\mu = 0.5$)
- The 400 sample means have standard deviation 0.086 (much less than population $\sigma = 0.5$)
- The distribution of sample means is approximately normal even though individual tosses are binary
- This illustrates that $\bar{X}$ varies less than $X$ and tends toward normality

**Simple Random Sampling Assumptions (Section 3.4):**
- Assumption A: Common mean - $\mathrm{E}[X_i] = \mu$ for all $i$
- Assumption B: Common variance - $\operatorname{Var}[X_i] = \sigma^2$ for all $i$
- Assumption C: Statistical independence - value of $X_i$ doesn't depend on values of other observations
- Shorthand notation: $X_i \sim (\mu, \sigma^2)$ means $X_i$ distributed with mean $\mu$ and variance $\sigma^2$
- These assumptions are relaxed in later chapters (e.g., regression allows different means)

**Mean and Variance of the Sample Mean (Section 3.4):**
- The sample mean $\bar{X}$ has population mean $\mu_{\bar{X}} = \mathrm{E}[\bar{X}] = \mu$ (unbiased)
- The sample mean has population variance $\sigma_{\bar{X}}^2 = \operatorname{Var}[\bar{X}] = \sigma^2/n$ (decreases with sample size)
- The sample mean has standard deviation $\sigma_{\bar{X}} = \sigma/\sqrt{n}$
- $\bar{X}$ is less variable than individual $X_i$ since $\sigma_{\bar{X}}^2 = \sigma^2/n < \sigma^2$
- As $n \rightarrow \infty$, $\bar{X}$ converges to $\mu$ because variance $\sigma^2/n \rightarrow 0$
- Proof uses linearity of expectation: $\mathrm{E}[\bar{X}] = \frac{1}{n}\{\mathrm{E}[X_1] + \cdots + \mathrm{E}[X_n]\} = \mu$
- Variance proof uses independence: $\operatorname{Var}[\bar{X}] = (\frac{1}{n})^2 \{\operatorname{Var}[X_1] + \cdots + \operatorname{Var}[X_n]\} = \frac{\sigma^2}{n}$

**Central Limit Theorem (Section 3.4):**
- Standardized variable: $Z = \frac{\bar{X} - \mu}{\sigma/\sqrt{n}}$ has mean 0 and variance 1
- Central Limit Theorem: $Z \sim N(0,1)$ as $n \rightarrow \infty$ (approximately normal for large samples)
- Therefore: $\bar{X} \sim N(\mu, \sigma^2/n)$ approximately for large $n$
- This holds regardless of the distribution of $X$ (as long as finite mean and variance exist)
- Remarkable result: normality emerges from averaging, even if $X$ itself is not normal
- The CLT holds under assumptions A-C and also under weaker conditions
- The CLT justifies using normal-based inference methods in a wide variety of applications

**Standard Error (Section 3.4):**
- Population variance $\sigma^2/n$ is unknown because $\sigma^2$ is unknown
- Replace $\sigma^2$ with sample variance $s^2$ to get estimated variance: $s_{\bar{X}}^2 = s^2/n$
- Standard error of $\bar{X}$: se($\bar{X}$) = $s/\sqrt{n}$ where $s$ is sample standard deviation
- "Standard error" means "estimated standard deviation" (general terminology for any estimator)
- Standard error measures precision of $\bar{x}$ as an estimate of $\mu$
- Smaller standard error means more precise estimate
- To halve the standard error, must quadruple the sample size (since se $\propto 1/\sqrt{n}$)
- Computer output may report various standard errors depending on which estimator is being used

**Census Data Example (Section 3.5):**
- Population: All 50,169,452 people in 1880 U.S. Census with $\mu = 24.13$ years, $\sigma = 18.61$ years
- Population distribution is not normal (declines with age, peaks at multiples of 5 due to rounding)
- Single sample of $n=25$: $\bar{x} = 27.84$, $s = 20.71$ (close but not equal to $\mu$ and $\sigma$)
- 100 samples of size 25: average of sample means = 23.78 (close to $\mu = 24.13$)
- Standard deviation of 100 sample means = 3.76 (close to theoretical $\sigma/\sqrt{n} = 18.61/\sqrt{25} = 3.72$)
- Distribution of sample means appears approximately normal despite non-normal population
- Demonstrates CLT: normality emerges even when population is far from normal

**Parameters, Estimators, and Estimates (Section 3.6):**
- Parameter: unknown constant determining the distribution (e.g., population mean $\mu$)
- Estimator: method/formula for estimating a parameter (e.g., random variable $\bar{X}$)
- Estimate: particular numerical value from a sample (e.g., realized value $\bar{x}$)
- Example: parameter is $\mu$, estimator is $\bar{X}$, estimate is $\bar{x} = 27.84$

**Unbiased Estimators (Section 3.6):**
- An estimator is unbiased if its expected value equals the parameter: $\mathrm{E}[\bar{X}] = \mu$
- The sample mean $\bar{X}$ is unbiased for $\mu$ under assumptions A-C
- Unbiasedness means "correct on average" - no systematic over- or under-estimation
- An estimator can be unbiased but still imprecise (high variance)

**Consistent Estimators (Section 3.6):**
- A consistent estimator converges to the parameter as $n \rightarrow \infty$
- Sufficient conditions for consistency: (1) any bias vanishes as $n \rightarrow \infty$, (2) variance $\rightarrow 0$ as $n \rightarrow \infty$
- The sample mean is consistent for $\mu$ because it's unbiased and $\operatorname{Var}[\bar{X}] = \sigma^2/n \rightarrow 0$
- Consistency is an asymptotic property (behavior as sample size grows without bound)

**Efficient Estimators (Section 3.6):**
- An efficient estimator has minimum variance among unbiased (or consistent) estimators
- Under assumptions A-C, the sample mean has variance $\sigma^2/n$
- For normal, Bernoulli, binomial, or Poisson distributions: $\bar{X}$ is the most efficient unbiased estimator
- For other distributions: $\bar{X}$ often has variance close to the minimum
- The sample median is also unbiased for symmetric distributions but usually has higher variance than $\bar{X}$
- Generally prefer $\bar{X}$ over other estimators due to its efficiency

**Nonrepresentative Samples (Section 3.7):**
- Simple random sample: independent observations from same distribution
- Representative sample: same distribution but not necessarily independent (can adjust se($\bar{x}$) formula)
- Nonrepresentative sample: different observations may have different $\mu$ (big problem!)
- Example: surveying Golf Digest readers doesn't represent general population
- Solution when inclusion probabilities $\pi_i$ are known: use weighted mean
- Sample weights: $w_i = 1/\pi_i$ (inverse of inclusion probability)
- Weighted mean: $\bar{x}_w = \left[\sum_{i=1}^n w_i x_i\right] / \left[\sum_{i=1}^n w_i\right]$
- Weighting corrects for over/under-representation of certain groups

**Computer Simulation (Section 3.8):**
- Pseudo-random number generator creates values between 0 and 1 that appear random
- All values between 0 and 1 equally likely (uniform distribution)
- Successive values appear independent
- Coin toss simulation: if uniform draw $> 0.5$ then heads ($X=1$), else tails ($X=0$)
- Census simulation: divide [0,1] into $N$ equal intervals, each representing one person
- Seed: starting value that determines the sequence of random numbers
- Always set seed for reproducibility (e.g., seed = 10101)
- Simulation example: simulate 400 samples of size 30, compute mean for each, analyze distribution

**Summary: Seven Key Results (Section 3.4):**
1. Sample values $x_1, \ldots, x_n$ are realizations of random variables $X_1, \ldots, X_n$
2. Under simple random sampling: $X_i$ have common mean $\mu$, variance $\sigma^2$, and are independent
3. Sample mean $\bar{X}$ has mean $\mu$ and variance $\sigma^2/n$
4. Standardized statistic $Z = (\bar{X} - \mu)/(\sigma/\sqrt{n})$ has mean 0 and variance 1
5. By CLT: $Z \sim N(0,1)$ as $n \rightarrow \infty$
6. For large $n$: $\bar{X} \sim N(\mu, \sigma^2/n)$ approximately
7. Standard error se($\bar{X}$) = $s/\sqrt{n}$ estimates the standard deviation of $\bar{X}$

---

