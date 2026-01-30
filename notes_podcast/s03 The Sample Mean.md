# Chapter 3: The Sample Mean

## Learning Objectives

By the end of this chapter, you will be able to:

- Define random variables and distinguish between random variables (upper case) and their realizations (lower case)
- Calculate the mean, variance, and standard deviation of a random variable from its probability distribution
- Understand the sample mean x-bar as a realization of the random variable X-bar
- Derive the mean and variance of the sample mean under simple random sampling assumptions
- Apply the Central Limit Theorem to show that X-bar is approximately normally distributed for large samples
- Calculate and interpret the standard error of the sample mean se of X-bar equals s over the square root of n
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
- X (or Y or Z) denotes a random variable
- x (or y or z) denotes the values taken by X (or Y or Z).


### Example: Coin toss

- Simplest case is a random variable that takes one of only two possible values.
- Consider toss of fair coin with X equals 1 if heads and X equals 0 if tails. Then

X equals 0 with probability 0.5, and equals 1 with probability 0.5.

### Mean of a Random Variable

- Mean of X, denoted mu or mu-sub-X
- is the probability-weighted average of all possible values of X in the population.
- mu is also denoted the expected value of X
- the expected value of the random variable X
- the long-run average value expected if we draw a value of X at random, draw a second value of X at random, and so on, and then obtain the average of these values.

mu defined as the expected value of X equals x-sub-1 times the probability that X equals x-sub-1, plus x-sub-2 times the probability that X equals x-sub-2, plus dot-dot-dot, which equals the sum over all x of x times the probability that X equals x.

- Note that
- the sum over x means the sum over all possible values x can take
- and the possible values of x are denoted x-sub-1, x-sub-2, x-sub-3, and so on


### Example of Mean

- Fair coin toss: X takes values 0 or 1 with equal probabilities

mu equals the sum over x of x times the probability that X equals x, which equals the probability that X equals 0 times 0, plus the probability that X equals 1 times 1, which equals 0.5 times 0 plus 0.5 times 1, which equals 0.5

- Unfair coin: X equals 1 with probability 0.6 and X equals 0 with probability 0.4
- mu equals 0 times 0.4 plus 1 times 0.6, which equals 0.6.


### Variance and Standard Deviation

- Variance sigma-squared
- measures the variability in X around mu
- equals the expected value of the quantity X minus mu squared, the squared deviation of X from the mean mu
- probability-weighted average of x-sub-1-star, x-sub-2-star, and so on

sigma-squared defined as the expected value of the quantity X minus mu squared, equals the quantity x-sub-1 minus mu squared times the probability that X equals x-sub-1, plus the quantity x-sub-2 minus mu squared times the probability that X equals x-sub-2, plus dot-dot-dot, which equals the sum over x of the quantity x minus mu squared times the probability that X equals x.

- Population standard deviation sigma is square root of the variance
- measured in the same units as X.


### Example of Variance and Standard Deviation

- Fair coin toss: X takes values 0 or 1 with equal probabilities so mu equals 0.5.
- Variance

sigma-squared equals the sum over x of the quantity x minus mu squared times the probability that X equals x, which equals the quantity 0 minus 0.5 squared times the probability that X equals 0, plus the quantity 1 minus 0.5 squared times the probability that X equals 1, which equals 0.25 times 0.5 plus 0.25 times 0.5, which equals 0.25

- Standard deviation

sigma equals the square root of 0.25, which is approximately 0.5

**Key Concept: Random Variables and Their Properties**

A random variable X is a variable whose value is determined by the outcome of an unpredictable experiment. The mean mu equals the expected value of X is the probability-weighted average of all possible values, while the variance sigma-squared equals the expected value of the quantity X minus mu squared measures variability around the mean. These population parameters characterize the distribution from which we draw samples.

## 3.2 Random Samples

- A sample of size n takes values denoted x-sub-1 through x-sub-n.
- These values are realizations or outcomes of the random variables X-sub-1, X-sub-2 through X-sub-n.
- Example: four consecutive coin tosses with results tails, heads, heads and heads
- random variable X-sub-1 has realized value x-sub-1 equals 0
- random variable X-sub-2 takes value x-sub-2 equals 1
- random variable X-sub-3 takes value x-sub-3 equals 1
- random variable X-sub-4 takes value x-sub-4 equals 1.


### Sample Mean is a Random Variable

- Sample of size n has observed values x-sub-1, x-sub-2 through x-sub-n.
- These are realizations of the random variables X-sub-1, X-sub-2 through X-sub-n.
- Sample mean is the average

x-bar equals the quantity x-sub-1 plus x-sub-2 plus dot-dot-dot plus x-sub-n, all divided by n, which equals one over n times the sum from i equals 1 to n of x-sub-i

- This is a realization of the random variable

X-bar equals the quantity X-sub-1 plus X-sub-2 plus dot-dot-dot plus X-sub-n, all divided by n, which equals one over n times the sum from i equals 1 to n of X-sub-i.

### Aside: Sample Variance and Standard Deviation

- Similarly any other sample statistic (such as the median) is a realization of a random variable
- In addition to the sample mean we focus on the sample variance and sample standard deviation.
- Sample variance is average of squared deviations of x around x-bar
- not around mu since mu is unknown

s-squared equals one over n minus 1, times the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared

- The sample variance is a realization of the random variable

S-squared equals one over n minus 1, times the sum from i equals 1 to n of the quantity X-sub-i minus X-bar, all squared

- Taking the square root gives the sample standard deviation s which is a realization of the random variable S.

**Key Concept: The Sample Mean as a Random Variable**

The observed sample mean x-bar is a realization of the random variable X-bar equals the quantity X-sub-1 plus dot-dot-dot plus X-sub-n, all divided by n. This fundamental insight means that x-bar varies from sample to sample in a predictable way—its distribution can be characterized mathematically. This allows us to perform statistical inference about the population mean mu.

## 3.3 Sample Generated from an Experiment: Coin Tosses

- We consider a simple experiment that generates many samples
- hence many sample means x-bar
- then summarize the resulting distribution of the many x-bar.
- Population: Outcomes from experiment of tossing a coin
- X equals 1 if heads and X equals 0 if tails
- Population mean mu equals the expected value of X equals 0.5, and standard deviation sigma equals 0.5.
- Sample: n equals 30
- random sample of size 30 from 30 coin tosses
- there are 10 heads and 20 tails, so x-bar equals 10 divided by 30, which equals 0.333
- histogram of this single sample is given in left panel of next slide.


### Example: Coin Tosses (continued)

- Left panel: x's from 1 sample of size 30 with 20 heads and 10 tails
- Right panel: x-bar's for 400 samples of size 30

One Sample of Size 30
![](https://cdn.mathpix.com/cropped/72a3f87a-41ec-4ad3-a2db-effc82ed52f5-14.jpg?height=355&width=488&top_left_y=395&top_left_x=164)

400 Sample Means
![](https://cdn.mathpix.com/cropped/72a3f87a-41ec-4ad3-a2db-effc82ed52f5-14.jpg?height=355&width=485&top_left_y=395&top_left_x=690)

### Example: Coin Tosses (continued)

- Randomly draw 400 different samples, each of size 30
- then x-bar-sub-1 equals 0.333, x-bar-sub-2 equals 0.500, x-bar-sub-3 equals 0.533, and so on.
- Histogram (plus kernel density estimate) for the 400 means from the 400 samples of size 30 is given in right panel of previous slide.
- Roughly centered on the population mean
  - The average of the 400 means is 0.499, close to mu equals 0.5

- Much less variability in these 400 means than in the original population
  - The standard deviation of the 400 means is 0.086
  - Much less than the population standard deviation of sigma equals 0.5

- The density estimate is roughly that of the normal


## 3.4 Properties of the Sample Mean

- The properties of X-bar depend on the properties of X-sub-1, X-sub-2 through X-sub-n
- such as the means and variances of X-sub-1, X-sub-2 through X-sub-n
- and whether their values depend in part on other values.
- In this chapter we consider the simplest and standard set of assumptions in introductory statistics
- X-sub-1, X-sub-2 through X-sub-n have common mean mu and common variance sigma-squared
- X-sub-1, X-sub-2 through X-sub-n are statistically independent
  - Statistical independence means that the value taken by X-sub-2, for example, is not influenced by the value taken by X-sub-1, X-sub-3 through X-sub-n

- In later chapters we relax these assumptions
- e.g. regression allows for different means for different observations.


### Population Assumptions

- Population
- equals set of all observations (or experimental outcomes).
- Sample
- equals subset selected from the population.
- Properties of x-bar depend on the random variable X-bar
- hence on assumptions about process generating X-sub-1, X-sub-2 through X-sub-n.
- We assume a simple random sample where
- A. X-sub-i has common mean mu: the expected value of X-sub-i equals mu for all i.
- B. X-sub-i has common variance sigma-squared: the variance of X-sub-i equals sigma-squared for all i.
- C. X-sub-i is statistically independent of X-sub-j, for i not equal to j.
- Shorthand notation: X-sub-i is distributed with mean mu and variance sigma-squared
- means X-sub-i are distributed with mean mu and variance sigma-squared.


### Mean and Variance of the Sample Mean

- Consider X-bar equals the quantity X-sub-1 plus X-sub-2 plus dot-dot-dot plus X-sub-n, all divided by n, for X-sub-i distributed with mean mu and variance sigma-squared.
- The (population) mean of the sample mean is

mu-sub-X-bar defined as the expected value of X-bar equals mu.

- The (population) variance of the sample mean is

sigma-sub-X-bar squared, defined as the expected value of the quantity X-bar minus mu-sub-X-bar, all squared, equals sigma-squared over n.

- The (population) standard deviation is sigma-sub-X-bar equals sigma divided by the square root of n.
- Sample mean is less variable than the underlying data
- since sigma-sub-X-bar squared is less than sigma-squared.
- Sample mean is close to mu as n goes to infinity
- since the expected value of X-bar equals mu and variance sigma-sub-X-bar squared equals sigma-squared over n goes to 0 as n goes to infinity.

**Key Concept: Mean and Variance of the Sample Mean**

Under simple random sampling (common mean mu, common variance sigma-squared, independence), the sample mean X-bar has mean the expected value of X-bar equals mu (unbiased) and variance the variance of X-bar equals sigma-squared over n (decreases with sample size). The standard deviation sigma-sub-X-bar equals sigma over the square root of n shrinks as n increases, meaning larger samples produce more precise estimates of mu.

### Aside: Proof for Mean of the Sample Mean

- Recall

X-bar equals the quantity X-sub-1 plus X-sub-2 plus dot-dot-dot plus X-sub-n, all divided by n

- Proof uses
- the expected value of a times X equals a times the expected value of X
- the expected value of X plus Y equals the expected value of X plus the expected value of Y
and assumption A (common mean of X-sub-i).
- Then

The expected value of X-bar equals the expected value of the quantity one over n times the quantity X-sub-1 plus X-sub-2 plus dot-dot-dot plus X-sub-n, which equals one over n times the expected value of the quantity X-sub-1 plus X-sub-2 plus dot-dot-dot plus X-sub-n, which equals one over n times the quantity the expected value of X-sub-1 plus the expected value of X-sub-2 plus dot-dot-dot plus the expected value of X-sub-n, which equals one over n times the quantity mu plus mu plus dot-dot-dot plus mu, which equals mu.

### Aside: Variance of the Population Mean

- Proof in Appendix B.2 uses that
- the variance of a times X equals a-squared times the expected value of X in general
- the variance of X plus Y equals the variance of X plus the variance of Y for independent variables
- and assumptions A-C.
- Then

The variance of X-bar equals the variance of the quantity one over n times the quantity X-sub-1 plus X-sub-2 plus dot-dot-dot plus X-sub-n, which equals the quantity one over n squared times the variance of the quantity X-sub-1 plus X-sub-2 plus dot-dot-dot plus X-sub-n, which equals the quantity one over n squared times the quantity the variance of X-sub-1 plus dot-dot-dot plus the variance of X-sub-n, which equals the quantity one over n squared times sigma-squared plus dot-dot-dot plus the quantity one over n squared times sigma-squared, which equals the quantity one over n squared times the quantity sigma-squared plus dot-dot-dot plus sigma-squared, which equals the quantity one over n squared times n times sigma-squared, which equals one over n times sigma-squared

### Normal Distribution and the Central Limit Theorem

- We have shown to date that X-bar is distributed with mean mu and variance sigma-squared over n
- In general, subtracting the mean and dividing by the standard deviation yields a random variable with mean 0 and variance 1.
- So here the standardized variable

Z equals the quantity X-bar minus mu, all divided by the quantity sigma over the square root of n, is distributed with mean 0 and variance 1.

- The central limit theorem (a remarkable result) proves normality as the sample size gets large

Z is distributed as normal with mean 0 and variance 1, as n goes to infinity.

- The central limit theorem holds under assumptions A-C
- and also under some weaker conditions.

**Key Concept: The Central Limit Theorem**

The Central Limit Theorem states that the standardized sample mean Z equals the quantity X-bar minus mu, all divided by the quantity sigma over the square root of n, converges to a standard normal distribution N with mean 0 and variance 1, as n goes to infinity. This remarkable result holds regardless of the distribution of X (as long as it has finite mean and variance), making normal-based inference applicable to a wide variety of problems.

### Normal Distribution (continued)

- Now convert back to the original X-bar.
- We have

Z equals the quantity X-bar minus mu, all divided by the quantity sigma over the square root of n, is distributed as normal with mean 0 and variance 1, as n goes to infinity.

- Then X-bar is approximately normally distributed in large samples

X-bar is distributed as normal with mean mu and variance sigma-squared over n, approximately for large n.

- We will use this result to do statistical inference on mu.
- However, the variance sigma-squared over n is unknown as sigma-squared is unknown
- we will have to get an estimate
- replace sigma-squared by its estimate s-squared
- where s is the sample standard deviation of X.


### Standard Error of the Sample Mean

- Estimated variance of X-bar is

s-sub-X-bar squared equals s-squared over n, which equals the quantity one over n minus 1 times the sum over i of the quantity x-sub-i minus x-bar squared, all divided by n.

- Estimated standard deviation of X-bar

s-sub-X-bar equals s over the square root of n, which equals the square root of the quantity one over n minus 1 times the sum over i of the quantity x-sub-i minus x-bar squared, all divided by the square root of n.

- s-sub-X-bar is called the standard error of the sample mean X-bar.
- The term "standard error" means estimated standard deviation
- various estimators each have a distinct standard error
- a reported "standard error" in computer output need not be s-sub-X-bar.
- Use the notation

se of X-bar equals s over the square root of n

**Key Concept: Standard Error**

The standard error se of X-bar equals s over the square root of n is the estimated standard deviation of the sample mean. It measures the precision of x-bar as an estimate of mu. Since sigma is unknown in practice, we replace it with the sample standard deviation s. The standard error decreases with the square root of n, so doubling precision requires quadrupling the sample size.

### Summary for the Sample Mean

(1) Sample values x-sub-1 through x-sub-n are observed values of the random variables X-sub-1 through X-sub-n.
(2) Individual X-sub-i have common mean mu and variance sigma-squared and are independent.
(3) Average X-bar of n draws of X-sub-i has mean mu and variance sigma-squared over n.
(4) Standardized statistic Z equals the quantity X-bar minus mu, all divided by the quantity sigma over the square root of n, is distributed with mean 0 and variance 1.
(5) Z is standard normal as size n goes to infinity by the central limit theorem.
(6) For large n a good approximation is that X-bar is distributed as normal with mean mu and variance sigma-squared over n
(7) The standard error of X-bar equals s over the square root of n, where "standard error" is general terminology for "estimated standard deviation".

## 3.5 Sampling from a Population: 1880 Census

- Now consider an example of sampling from a population.
- Population: N equals 50,169,452
- all people recorded as living in the U.S. in 1880
- the average age is 24.13 years, so mu equals 24.13
- the standard deviation of age is 18.61, so sigma equals 18.61
- histogram is given in the next slide.


### Example: 1880 Census (continued)

- Population
- Probabilities decline with age (clearly not the normal)
- Peaks due to rounding at five and ten years

Entire 1880 Census
![](https://cdn.mathpix.com/cropped/72a3f87a-41ec-4ad3-a2db-effc82ed52f5-26.jpg?height=533&width=759&top_left_y=353&top_left_x=253)

### Example: 1880 Census (continued)

- Single sample: n equals 25
- random sample of size 25 from the entire U.S. population
- the average age is 27.84, so x-bar equals 27.84
- the standard deviation of age is 20.71, so s equals 20.71
- these are similar to, but not exactly equal to, mu and sigma
- histogram of x's in a single sample is given in left panel of next slide.
- Many samples of size 25
- randomly draw 100 different samples, each of size 25
- then x-bar-sub-1 equals 27.84, x-bar-sub-2 equals 19.40, x-bar-sub-3 equals 23.28 years, and so on.
- average of the 100 sample means is 23.78, close to mu equals 24.13.
- standard deviation of the 100 means is 3.76, close to sigma over the square root of n equals 18.61 divided by the square root of 25, which equals 3.72.
- histogram of x-bar's across 100 samples is given in right panel of next slide.


### Example: 1880 Census (continued)

- 100 different means from 100 different samples, each of size 25
- histogram (left) and kernel density estimate (right)
- looks like normal with mean mu and standard deviation much less than sigma
![](https://cdn.mathpix.com/cropped/72a3f87a-41ec-4ad3-a2db-effc82ed52f5-28.jpg?height=433&width=538&top_left_y=387&top_left_x=82)
![](https://cdn.mathpix.com/cropped/72a3f87a-41ec-4ad3-a2db-effc82ed52f5-28.jpg?height=405&width=541&top_left_y=389&top_left_x=644)


## 3.6 Estimation of the Sample Mean

- Desire a good point estimate of population mean mu
- why use x-bar rather than some other estimate?
- A desirable estimator of mu has distribution
- centered on mu
- with as little variability around mu as possible.


### Parameter, Estimator and Estimate

- A parameter is a constant that determines in part the distribution of x.
- An estimator is a method for estimating a parameter.
- An estimate is the particular value of the estimator obtained from the sample.
- For estimation of the mean of X using the sample mean
- the parameter is mu
- the estimator is the random variable X-bar
- the estimate is the sample value x-bar.


### Unbiased Estimators

- An unbiased estimator of a population parameter
- has expected value that equals the population parameter.
- The sample mean is unbiased for mu
- since the expected value of X-bar equals mu.


### Minimum Variance Estimators

- Other estimators may also be unbiased and consistent for mu
- e.g. sample median in the case where X is symmetrically distributed
- discriminate between such estimators using their variance.
- A best estimator or efficient estimator
- has minimum variance among the class of consistent estimators (or of unbiased estimators).
- Under assumptions A-C the sample mean has variance sigma-squared over n
- for X that is normal, Bernoulli, binomial or Poisson no other unbiased estimator has lower variance
- for X with other distributions the sample mean is often close to having the lowest variance
- generally the sample mean is used to estimate mu.


### Consistent Estimators

- Consistency is a more advanced concept that considers behavior as the sample size goes to infinity.
- A consistent estimator of a population parameter
- is one that is almost certainly arbitrarily close to the population parameter as the sample size gets very large.
- A sufficient condition for consistency is
- any bias disappears as the sample size gets very large
- the variance goes to zero as the sample size gets very large
- The sample mean is consistent for mu under assumptions A-C
- it is unbiased
- the variance sigma-sub-X-bar squared equals sigma-squared over n goes to 0 as n goes to infinity.

**Key Concept: Properties of Good Estimators**

A good estimator should be unbiased (the expected value of X-bar equals mu), consistent (converges to mu as n goes to infinity), and efficient (minimum variance among unbiased estimators). The sample mean X-bar satisfies all three properties under simple random sampling, making it the preferred estimator of mu for most distributions.

## 3.7 Samples other than Simple Random Samples

- Recall simple random sample means data are independent and from the same distribution.
- Representative Samples
- Still from same distribution but no longer statistically independent.
- Then can adapt methods using an alternative formula for se of x-bar.
- Nonrepresentative samples
- Now different observations may have different mu
- e.g. Survey readers of Golf Digest not representative of population.
- Big problem.
- Weighted mean can still be used if population weights are known
- pi-sub-i equals probability that i-th observation is included in the sample.
- sample weights w-sub-i equals 1 over pi-sub-i
- weighted mean x-bar-sub-w equals the quantity the sum from i equals 1 to n of w-sub-i times x-sub-i, all divided by the quantity the sum from i equals 1 to n of w-sub-i.

**Key Concept: Nonrepresentative Samples**

Simple random sampling assumes all observations come from the same distribution with common mean mu. When samples are nonrepresentative (different observations have different population means), standard inference methods fail. Weighted means can correct for this if inclusion probabilities pi-sub-i are known, with weights w-sub-i equals 1 over pi-sub-i applied to each observation.

## 3.8 Computer Generation of a Random Variable

- A (pseudo) uniform random number generator
- creates values between 0 and 1
- any value between 0 and 1 is equally likely
- successive values appear to be independent of each other.
- To simulate 30 coin tosses
- draw 30 uniform random numbers
- result is heads if the uniform random number exceeds 0.5
- For Census example
- if uniform random number is between 0 and 1 over N, where N equals 50,169,452, we choose the first person, etcetera
- The sequence depends on the starting value called the seed
- always set the seed (e.g. equal to 10101).


### Some in-class Exercises

(1) Suppose X equals 100 with probability 0.8 and X equals 600 with probability 0.2. Find the mean, variance and standard deviation of X.
(2) Consider random samples of size 25 from the random variable X that has mean 100 and variance 400. Give the mean, variance and standard deviation of the mean X-bar.

---

## Key Takeaways

**Random Variables and Probability Distributions (Section 3.1):**
- A random variable X is a variable whose value is determined by an unpredictable experimental outcome
- Standard notation: upper case (X, Y, Z) denotes random variables; lower case (x, y, z) denotes realized values
- The mean mu equals the expected value of X is the probability-weighted average of all possible values: mu equals the sum over x of x times the probability that X equals x
- The variance sigma-squared equals the expected value of the quantity X minus mu squared measures variability around the mean: sigma-squared equals the sum over x of the quantity x minus mu squared times the probability that X equals x
- The standard deviation sigma equals the square root of sigma-squared is measured in the same units as X
- For a fair coin toss with X in the set 0, 1: mu equals 0.5 and sigma equals 0.5
- For an unfair coin with the probability that X equals 1 equals 0.6: mu equals 0.6 and sigma-squared equals 0.24

**Random Samples and the Sample Mean (Section 3.2):**
- Sample values x-sub-1, x-sub-2 through x-sub-n are realizations of random variables X-sub-1, X-sub-2 through X-sub-n
- The sample mean x-bar equals the quantity x-sub-1 plus dot-dot-dot plus x-sub-n, all divided by n, is a realization of the random variable X-bar equals the quantity X-sub-1 plus dot-dot-dot plus X-sub-n, all divided by n
- Any sample statistic (mean, median, variance) is a realization of a random variable
- Sample variance: s-squared equals one over n minus 1 times the sum from i equals 1 to n of the quantity x-sub-i minus x-bar squared (uses n minus 1 for unbiased estimation)
- Sample standard deviation: s equals the square root of s-squared
- The "n minus 1" divisor (instead of n) corrects for downward bias when estimating sigma-squared from sample data
- Both s-squared and s are realizations of random variables S-squared and S

**Sampling Distribution Examples (Section 3.3):**
- Coin toss experiment: 400 samples of size 30, each produces a sample mean x-bar
- The 400 sample means have average 0.499 (close to population mu equals 0.5)
- The 400 sample means have standard deviation 0.086 (much less than population sigma equals 0.5)
- The distribution of sample means is approximately normal even though individual tosses are binary
- This illustrates that X-bar varies less than X and tends toward normality

**Simple Random Sampling Assumptions (Section 3.4):**
- Assumption A: Common mean - the expected value of X-sub-i equals mu for all i
- Assumption B: Common variance - the variance of X-sub-i equals sigma-squared for all i
- Assumption C: Statistical independence - value of X-sub-i doesn't depend on values of other observations
- Shorthand notation: X-sub-i is distributed with mean mu and variance sigma-squared means X-sub-i distributed with mean mu and variance sigma-squared
- These assumptions are relaxed in later chapters (e.g., regression allows different means)

**Mean and Variance of the Sample Mean (Section 3.4):**
- The sample mean X-bar has population mean mu-sub-X-bar equals the expected value of X-bar equals mu (unbiased)
- The sample mean has population variance sigma-sub-X-bar squared equals the variance of X-bar equals sigma-squared over n (decreases with sample size)
- The sample mean has standard deviation sigma-sub-X-bar equals sigma over the square root of n
- X-bar is less variable than individual X-sub-i since sigma-sub-X-bar squared equals sigma-squared over n is less than sigma-squared
- As n goes to infinity, X-bar converges to mu because variance sigma-squared over n goes to 0
- Proof uses linearity of expectation: the expected value of X-bar equals one over n times the quantity the expected value of X-sub-1 plus dot-dot-dot plus the expected value of X-sub-n equals mu
- Variance proof uses independence: the variance of X-bar equals the quantity one over n squared times the quantity the variance of X-sub-1 plus dot-dot-dot plus the variance of X-sub-n equals sigma-squared over n

**Central Limit Theorem (Section 3.4):**
- Standardized variable: Z equals the quantity X-bar minus mu, all divided by the quantity sigma over the square root of n, has mean 0 and variance 1
- Central Limit Theorem: Z is distributed as normal with mean 0 and variance 1, as n goes to infinity (approximately normal for large samples)
- Therefore: X-bar is distributed as normal with mean mu and variance sigma-squared over n, approximately for large n
- This holds regardless of the distribution of X (as long as finite mean and variance exist)
- Remarkable result: normality emerges from averaging, even if X itself is not normal
- The CLT holds under assumptions A-C and also under weaker conditions
- The CLT justifies using normal-based inference methods in a wide variety of applications

**Standard Error (Section 3.4):**
- Population variance sigma-squared over n is unknown because sigma-squared is unknown
- Replace sigma-squared with sample variance s-squared to get estimated variance: s-sub-X-bar squared equals s-squared over n
- Standard error of X-bar: se of X-bar equals s over the square root of n, where s is sample standard deviation
- "Standard error" means "estimated standard deviation" (general terminology for any estimator)
- Standard error measures precision of x-bar as an estimate of mu
- Smaller standard error means more precise estimate
- To halve the standard error, must quadruple the sample size (since se is proportional to 1 over the square root of n)
- Computer output may report various standard errors depending on which estimator is being used

**Census Data Example (Section 3.5):**
- Population: All 50,169,452 people in 1880 U.S. Census with mu equals 24.13 years, sigma equals 18.61 years
- Population distribution is not normal (declines with age, peaks at multiples of 5 due to rounding)
- Single sample of n equals 25: x-bar equals 27.84, s equals 20.71 (close but not equal to mu and sigma)
- 100 samples of size 25: average of sample means equals 23.78 (close to mu equals 24.13)
- Standard deviation of 100 sample means equals 3.76 (close to theoretical sigma over the square root of n equals 18.61 divided by the square root of 25 equals 3.72)
- Distribution of sample means appears approximately normal despite non-normal population
- Demonstrates CLT: normality emerges even when population is far from normal

**Parameters, Estimators, and Estimates (Section 3.6):**
- Parameter: unknown constant determining the distribution (e.g., population mean mu)
- Estimator: method/formula for estimating a parameter (e.g., random variable X-bar)
- Estimate: particular numerical value from a sample (e.g., realized value x-bar)
- Example: parameter is mu, estimator is X-bar, estimate is x-bar equals 27.84

**Unbiased Estimators (Section 3.6):**
- An estimator is unbiased if its expected value equals the parameter: the expected value of X-bar equals mu
- The sample mean X-bar is unbiased for mu under assumptions A-C
- Unbiasedness means "correct on average" - no systematic over- or under-estimation
- An estimator can be unbiased but still imprecise (high variance)

**Consistent Estimators (Section 3.6):**
- A consistent estimator converges to the parameter as n goes to infinity
- Sufficient conditions for consistency: (1) any bias vanishes as n goes to infinity, (2) variance goes to 0 as n goes to infinity
- The sample mean is consistent for mu because it's unbiased and the variance of X-bar equals sigma-squared over n goes to 0
- Consistency is an asymptotic property (behavior as sample size grows without bound)

**Efficient Estimators (Section 3.6):**
- An efficient estimator has minimum variance among unbiased (or consistent) estimators
- Under assumptions A-C, the sample mean has variance sigma-squared over n
- For normal, Bernoulli, binomial, or Poisson distributions: X-bar is the most efficient unbiased estimator
- For other distributions: X-bar often has variance close to the minimum
- The sample median is also unbiased for symmetric distributions but usually has higher variance than X-bar
- Generally prefer X-bar over other estimators due to its efficiency

**Nonrepresentative Samples (Section 3.7):**
- Simple random sample: independent observations from same distribution
- Representative sample: same distribution but not necessarily independent (can adjust se of x-bar formula)
- Nonrepresentative sample: different observations may have different mu (big problem!)
- Example: surveying Golf Digest readers doesn't represent general population
- Solution when inclusion probabilities pi-sub-i are known: use weighted mean
- Sample weights: w-sub-i equals 1 over pi-sub-i (inverse of inclusion probability)
- Weighted mean: x-bar-sub-w equals the quantity the sum from i equals 1 to n of w-sub-i times x-sub-i, all divided by the quantity the sum from i equals 1 to n of w-sub-i
- Weighting corrects for over/under-representation of certain groups

**Computer Simulation (Section 3.8):**
- Pseudo-random number generator creates values between 0 and 1 that appear random
- All values between 0 and 1 equally likely (uniform distribution)
- Successive values appear independent
- Coin toss simulation: if uniform draw greater than 0.5 then heads (X equals 1), else tails (X equals 0)
- Census simulation: divide the interval from 0 to 1 into N equal intervals, each representing one person
- Seed: starting value that determines the sequence of random numbers
- Always set seed for reproducibility (e.g., seed equals 10101)
- Simulation example: simulate 400 samples of size 30, compute mean for each, analyze distribution

**Summary: Seven Key Results (Section 3.4):**
1. Sample values x-sub-1 through x-sub-n are realizations of random variables X-sub-1 through X-sub-n
2. Under simple random sampling: X-sub-i have common mean mu, variance sigma-squared, and are independent
3. Sample mean X-bar has mean mu and variance sigma-squared over n
4. Standardized statistic Z equals the quantity X-bar minus mu, all divided by the quantity sigma over the square root of n, has mean 0 and variance 1
5. By CLT: Z is distributed as normal with mean 0 and variance 1, as n goes to infinity
6. For large n: X-bar is distributed as normal with mean mu and variance sigma-squared over n, approximately
7. Standard error se of X-bar equals s over the square root of n estimates the standard deviation of X-bar

---
