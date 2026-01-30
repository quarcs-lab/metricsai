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

Imagine you flip a coin and get heads. Was this outcome predictable? No—it's random. But here's an interesting question: if you flip the coin many times and take the average, will that average be predictable? The surprising answer is yes. This chapter explores how randomness at the individual level transforms into predictability at the aggregate level—a fundamental insight that makes statistical inference possible.

## 3.1 Random Variables

Think about flipping a coin. Before you flip, you don't know whether you'll get heads or tails. This uncertainty is what makes it a random variable.

- A **random variable** is a variable whose value is determined by the outcome of an experiment
- An **experiment** is any operation whose outcome cannot be predicted with certainty
- Example 1: Toss a coin. Let X equal 1 if heads and 0 if tails. The value of X is random.
- Example 2: Randomly select a person from the population. Let X equal their annual earnings. Again, X is random—we don't know whose earnings we'll observe until after we select.

**Standard notation** (important to remember):
- Upper case (X, Y, or Z) denotes a random variable—something we haven't observed yet
- Lower case (x, y, or z) denotes actual values—what we observe after the experiment


### Example: Coin Toss

Let's start with the simplest possible random variable: one that takes only two values.

Consider tossing a fair coin. Define X equals 1 if we get heads and X equals 0 if we get tails. Then:

X equals 0 with probability 0.5, and X equals 1 with probability 0.5.

This is a binary random variable—it can only be 0 or 1.

### Mean of a Random Variable

Now here's a key question: What's the "average" value of this random variable? Since we haven't flipped yet, we can't say we'll get heads or tails. But we can calculate the expected value—what we'd get on average if we flipped many times.

The **population mean** (denoted mu, pronounced "mew") is the probability-weighted average of all possible values. Think of it as:
- Take each possible value
- Multiply it by how likely it is
- Add them all up

More formally, mu is also called the **expected value of X**. It's the long-run average if we repeated the experiment infinitely many times.

**Formula**: mu equals the expected value of X, which we calculate as:
- x-sub-1 times the probability that X equals x-sub-1
- plus x-sub-2 times the probability that X equals x-sub-2
- plus all other terms

Or more compactly: mu equals the sum over all possible values x of the quantity x times the probability that X equals x.

**Note on notation**: "The sum over all x" means we add up one term for each possible value the variable can take. These possible values are labeled x-sub-1, x-sub-2, x-sub-3, and so on.


### Example of Mean

**Fair coin toss**: X takes values 0 or 1 with equal probabilities (0.5 each).

Let's calculate mu step by step:
- When X equals 0 (tails): contribute 0 times 0.5 equals 0
- When X equals 1 (heads): contribute 1 times 0.5 equals 0.5
- Sum these contributions: mu equals 0 plus 0.5, which equals 0.5

So the expected value of a fair coin toss is 0.5—right between 0 and 1, which makes intuitive sense for a fair coin.

**Unfair coin**: What if the coin is biased? Suppose X equals 1 with probability 0.6 and X equals 0 with probability 0.4.

Now:
- When X equals 0: contribute 0 times 0.4 equals 0
- When X equals 1: contribute 1 times 0.6 equals 0.6
- Sum: mu equals 0.6

The expected value shifted toward 1 because heads (X equals 1) is now more likely.


### Variance and Standard Deviation

The mean tells us the "center" of a distribution. But how spread out are the values? That's what variance measures.

The **variance** (denoted sigma-squared, pronounced "sigma-squared") measures how much X varies around its mean mu. Think of it as the average squared distance from the mean.

Why squared distances? Because if we just averaged the distances (X minus mu), positive and negative deviations would cancel out. Squaring makes everything positive.

**Formula**: sigma-squared equals the expected value of the quantity X minus mu, all squared.

Breaking this down:
- Take each possible value x
- Find how far it is from the mean: (x minus mu)
- Square this distance: (x minus mu) squared
- Weight by probability: (x minus mu) squared times probability that X equals x
- Sum over all possible values

More compactly: sigma-squared equals the sum over all x of the quantity (x minus mu) squared times the probability that X equals x.

The **population standard deviation** is sigma equals the square root of sigma-squared. We take the square root to get back to the original units of X. If X is measured in dollars, sigma is also in dollars (while sigma-squared is in dollars-squared, which is harder to interpret).


### Example of Variance and Standard Deviation

**Fair coin toss**: X takes values 0 or 1 with equal probabilities, so we already know mu equals 0.5.

**Calculating variance** step by step:
- When X equals 0 (tails): squared deviation is (0 minus 0.5) squared equals 0.25
  - Weight by probability: 0.25 times 0.5 equals 0.125
- When X equals 1 (heads): squared deviation is (1 minus 0.5) squared equals 0.25
  - Weight by probability: 0.25 times 0.5 equals 0.125
- Sum these: sigma-squared equals 0.125 plus 0.125, which equals 0.25

**Standard deviation**: sigma equals the square root of 0.25, which equals 0.5.

Notice something interesting: for this binary variable, the standard deviation (0.5) equals the mean (0.5). This is a special property of variables that take only values 0 and 1 with equal probability.

> **Key Concept**: A random variable X has values determined by unpredictable experiments. The mean mu (the expected value of X) is the probability-weighted average of all possible values—it tells us the "center." The variance sigma-squared (the expected value of X minus mu, all squared) measures spread around the mean—it tells us the "variability." Together, these two parameters characterize the population distribution from which we draw samples.

## 3.2 Random Samples

Let's connect our abstract definition of random variables to the practical task of collecting data.

When we collect a sample of size n, we get n observations. We denote these values x-sub-1, x-sub-2, up through x-sub-n. Each of these is a **realization**—the outcome we actually observed—of a random variable.

**Example: Coin tosses**

Imagine you toss a coin four times and record the results: tails, heads, heads, heads.

Before you tossed, each outcome was uncertain. We described this uncertainty with random variables X-sub-1, X-sub-2, X-sub-3, and X-sub-4.

After you tossed, you got specific results:
- First toss (tails): random variable X-sub-1 realized value x-sub-1 equals 0
- Second toss (heads): random variable X-sub-2 realized value x-sub-2 equals 1
- Third toss (heads): random variable X-sub-3 realized value x-sub-3 equals 1
- Fourth toss (heads): random variable X-sub-4 realized value x-sub-4 equals 1

This is the key distinction: Capital letters represent the uncertainty **before** the experiment. Lowercase letters represent the actual results **after** the experiment.


### Sample Mean is a Random Variable

Here's where things get interesting. When we calculate a sample mean, we're doing more than simple arithmetic. We're creating a new random variable.

**Before collecting data**: We have random variables X-sub-1, X-sub-2, through X-sub-n. The sample mean is itself a random variable:

X-bar equals the quantity X-sub-1 plus X-sub-2 plus dot-dot-dot plus X-sub-n, all divided by n.

More compactly: X-bar equals one over n times the sum from i equals 1 to n of X-sub-i.

**After collecting data**: We have realized values x-sub-1, x-sub-2, through x-sub-n. The observed sample mean is:

x-bar equals the quantity x-sub-1 plus x-sub-2 plus dot-dot-dot plus x-sub-n, all divided by n.

Or: x-bar equals one over n times the sum from i equals 1 to n of x-sub-i.

This observed value x-bar is one realization of the random variable X-bar. If we drew a different sample, we'd get a different x-bar!

**Why does this matter?** Because X-bar is a random variable, it has a probability distribution. We can characterize its mean, variance, and shape. This is what makes statistical inference possible.

### Aside: Sample Variance and Standard Deviation

Just as the sample mean is a random variable, so is every other sample statistic. Two particularly important ones are the sample variance and sample standard deviation.

The **sample variance** measures spread in our data. It's the average squared deviation of observations from the sample mean:

s-squared equals one over n minus 1, times the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared.

Notice we measure deviations from x-bar (the sample mean), not from mu (the population mean). Why? Because we don't know mu—that's what we're trying to estimate!

Also notice the divisor is n minus 1, not n. This "degrees of freedom" adjustment corrects for a subtle bias. We'll discuss this more in later chapters.

This observed s-squared is a realization of the random variable:

S-squared equals one over n minus 1, times the sum from i equals 1 to n of the quantity X-sub-i minus X-bar, all squared.

The **sample standard deviation** is simply the square root:

s equals the square root of s-squared, which is a realization of S equals the square root of S-squared.

Like the sample mean, these statistics vary from sample to sample. Their variability is predictable and can be characterized mathematically.

> **Key Concept**: The observed sample mean x-bar is just one realization of the random variable X-bar. Before we collect data, X-bar is uncertain—it could take many possible values depending on which observations we happen to select. After collecting data, we get a specific value x-bar. Because X-bar is a random variable, it has a probability distribution with knowable properties (mean, variance, shape). This is the foundation of statistical inference: understanding how estimates vary across possible samples.

## 3.3 Sample Generated from an Experiment: Coin Tosses

We've learned that X-bar is a random variable with its own distribution. But what does this distribution actually look like? Let's use a simple experiment to find out.

**The experiment setup:**

Imagine tossing a fair coin repeatedly. We'll treat this as our "population."
- Population: All possible coin toss outcomes
- X equals 1 if heads, X equals 0 if tails
- Population mean: mu equals 0.5
- Population standard deviation: sigma equals 0.5

Now let's draw a sample of size n equals 30 (toss the coin 30 times).

**One sample result:**

Suppose we get 10 heads and 20 tails. The sample mean is:

x-bar equals 10 divided by 30, which equals 0.333.

The histogram of this single sample appears in the left panel below. It shows only two bars—one at 0 (tails) and one at 1 (heads)—because individual tosses can only be 0 or 1.


### Example: Coin Tosses (continued)

The figures below illustrate a fundamental concept in statistics.

**Left panel**: Shows individual observations (the x's) from ONE sample of size 30.
- We got 20 tails (x equals 0) and 10 heads (x equals 1)
- Sample mean: x-bar equals 0.333
- Only two possible values, very spread out

**Right panel**: Shows sample means (the x-bar's) from 400 DIFFERENT samples, each of size 30.
- Each sample gives one x-bar
- We now have 400 different x-bar values
- Much more concentrated around 0.5

One Sample of Size 30
![](https://cdn.mathpix.com/cropped/72a3f87a-41ec-4ad3-a2db-effc82ed52f5-14.jpg?height=355&width=488&top_left_y=395&top_left_x=164)

400 Sample Means
![](https://cdn.mathpix.com/cropped/72a3f87a-41ec-4ad3-a2db-effc82ed52f5-14.jpg?height=355&width=485&top_left_y=395&top_left_x=690)

### Example: Coin Tosses (continued)

**The full experiment:**

We repeated the sampling process 400 times. Each time, we tossed the coin 30 times and calculated the sample mean. This gave us 400 different sample means:
- First sample: x-bar-sub-1 equals 0.333
- Second sample: x-bar-sub-2 equals 0.500
- Third sample: x-bar-sub-3 equals 0.533
- And so on...

The right panel in the previous figure shows a histogram (with a smooth kernel density estimate) of these 400 sample means. Notice three striking features:

**1. Centered on the population mean:**

The average of the 400 sample means is 0.499—extremely close to the true population mean mu equals 0.5. Individual samples vary (we got values from about 0.30 to 0.70), but on average they're right on target. This demonstrates **unbiasedness** in action.

**2. Much less variable than individual observations:**

The standard deviation of the 400 sample means is only 0.086. Compare this to the population standard deviation sigma equals 0.5. The sample means are clustered much more tightly than individual coin tosses. Averaging reduces variability!

**3. Approximately normal shape:**

The smooth curve overlaid on the histogram looks like a bell curve—the normal distribution. This is remarkable because individual coin tosses are binary (0 or 1), yet their averages form a smooth, symmetric, bell-shaped distribution. This is the **Central Limit Theorem** in action, which we'll explore next.


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

Here's where things get interesting. We know individual observations vary randomly. But what about their average?

Recall that X-bar equals the quantity X-sub-1 plus X-sub-2 plus dot-dot-dot plus X-sub-n, all divided by n. Each X-sub-i is random, so X-bar is also random. What are its properties?

**Two remarkable results:**

**Result 1: The mean of X-bar equals mu**

The expected value of X-bar (denoted mu-sub-X-bar) equals mu—the same as the population mean.

What does this mean? On average, across all possible samples we could draw, the sample mean equals the population mean. Individual samples might give values above or below mu, but they average out to mu. We call this property "unbiasedness."

**Result 2: The variance of X-bar equals sigma-squared over n**

The variance of X-bar (denoted sigma-sub-X-bar squared) equals sigma-squared divided by n.

This is profound. The sample mean is LESS variable than individual observations. How much less? By a factor of n.

Example: If individual observations have variance 100 and we sample n equals 25 people, the sample mean has variance 100 divided by 25 equals 4. Averaging reduces variability!

**Standard deviation**: sigma-sub-X-bar equals sigma divided by the square root of n.

Notice what happens as n increases:
- Larger samples give less variable sample means
- As n approaches infinity, variance approaches zero
- This means X-bar gets arbitrarily close to mu with large enough samples

This is why statisticians love large samples—they produce more precise estimates.

> **Key Concept**: The sample mean X-bar has two key properties. First, it's unbiased: the expected value of X-bar equals mu. On average, it hits the target. Second, it becomes more precise with larger samples: the variance of X-bar equals sigma-squared over n. Doubling the sample size cuts variance in half (or cuts standard deviation by the square root of 2). This is why "bigger is better" in sampling.

### Aside: Proof for Mean of the Sample Mean

**Want to see why the expected value of X-bar equals mu?** Here's the mathematical proof. (Feel free to skip if you prefer intuition over algebra!)

**Starting point**: X-bar equals the sum of X-sub-1 through X-sub-n, all divided by n.

**Tools we'll use**:
- Rule 1: The expected value of a constant times X equals that constant times the expected value of X
- Rule 2: The expected value of X plus Y equals the expected value of X plus the expected value of Y
- Assumption A: Each X-sub-i has the same expected value mu

**Proof in steps**:

Step 1: Start with the expected value of X-bar.
- E of X-bar equals E of the quantity one over n times the sum of all X-sub-i

Step 2: Use Rule 1 to pull one over n outside the expected value operator.
- This gives: one over n times E of the sum of all X-sub-i

Step 3: Use Rule 2 to break the sum into individual expected values.
- This gives: one over n times the quantity E of X-sub-1 plus E of X-sub-2 plus ... plus E of X-sub-n

Step 4: Use Assumption A to replace each expected value with mu.
- This gives: one over n times the quantity mu plus mu plus ... plus mu (n times)

Step 5: Simplify.
- one over n times n times mu equals mu

**Conclusion**: E of X-bar equals mu. The sample mean is unbiased!

### Aside: Variance of the Sample Mean

**How do we prove that Var of X-bar equals sigma-squared over n?** Here's the mathematical derivation. (Again, skip if you prefer the intuition!)

**Tools we'll use**:
- Rule 1: Var of a constant times X equals that constant squared times Var of X
- Rule 2: Var of X plus Y equals Var of X plus Var of Y (when X and Y are independent)
- Assumption B: Each X-sub-i has variance sigma-squared
- Assumption C: The X-sub-i's are independent

**Proof in steps**:

Step 1: Start with Var of X-bar.
- Var of X-bar equals Var of the quantity one over n times the sum of all X-sub-i

Step 2: Use Rule 1 to pull the constant one over n outside (and square it).
- This gives: one over n-squared times Var of the sum of all X-sub-i

Step 3: Use Rule 2 and independence to break the variance of the sum.
- This gives: one over n-squared times the quantity Var of X-sub-1 plus ... plus Var of X-sub-n

Step 4: Use Assumption B to replace each variance with sigma-squared.
- This gives: one over n-squared times the quantity sigma-squared plus ... plus sigma-squared (n times)

Step 5: Simplify.
- one over n-squared times n times sigma-squared equals sigma-squared over n

**Conclusion**: Var of X-bar equals sigma-squared over n. Larger samples have smaller variance!

### Normal Distribution and the Central Limit Theorem

We've established that X-bar has mean mu and variance sigma-squared over n. But what's its *shape*—its full probability distribution?

This is where one of statistics' most beautiful results comes in: the **Central Limit Theorem (CLT)**.

**Setting up the standardized variable:**

Before stating the CLT, we need to standardize X-bar. Standardizing means subtracting the mean and dividing by the standard deviation. This creates a variable with mean 0 and standard deviation 1.

For X-bar, the standardized version is:

Z equals the quantity X-bar minus mu, all divided by the quantity sigma over the square root of n.

This Z has mean 0 and variance 1 by construction (verify this as an exercise!).

**The Central Limit Theorem:**

Here's the remarkable result: as n gets large, Z becomes approximately normally distributed.

More precisely: Z is distributed approximately as N with mean 0 and variance 1, for large n.

**Why is this remarkable?** Because it doesn't matter what distribution X originally came from! X could be uniform, exponential, binomial—anything with finite mean and variance. As long as we take enough observations and average them, that average becomes approximately normal.

This works under our assumptions A-C (common mean, common variance, independence), and even under some weaker conditions.

> **Key Concept**: The Central Limit Theorem is one of the most important results in statistics. It says that sample means from ANY distribution (with finite mean and variance) become approximately normally distributed as sample size increases. This is why the normal distribution appears everywhere in statistics—not because data are normal, but because averages of data are approximately normal. This makes normal-based inference (confidence intervals, hypothesis tests) applicable to a huge variety of problems.

### Normal Distribution (continued)

**Converting back to X-bar:**

We know Z is approximately normal with mean 0 and variance 1. But we care about X-bar, not Z. How can we describe X-bar's distribution?

Since Z equals the quantity X-bar minus mu, all divided by the quantity sigma over the square root of n, we can work backwards. If Z is approximately N with mean 0 and variance 1, then:

X-bar is approximately N with mean mu and variance sigma-squared over n, for large n.

This is what we'll use for statistical inference on mu!

**There's one catch:** The variance sigma-squared over n depends on sigma-squared, which is unknown in practice. We've never observed the entire population, so we don't know sigma-squared.

**Solution**: Replace sigma-squared with an estimate. We'll use s-squared, the sample variance, computed from our data. This leads us to the standard error.


### Standard Error of the Sample Mean

We know that X-bar has standard deviation sigma over the square root of n. But sigma is unknown—we don't know the population standard deviation. What do we do?

We **estimate** it using our sample data!

**Estimated variance of X-bar**:

Replace sigma-squared with s-squared (the sample variance) to get:

s-sub-X-bar squared equals s-squared over n

where s-squared equals one over n minus 1 times the sum over i of the quantity x-sub-i minus x-bar, all squared.

**Estimated standard deviation of X-bar**:

Take the square root to get:

s-sub-X-bar equals s over the square root of n

This estimated standard deviation has a special name: the **standard error**.

**Terminology note**: "Standard error" is statistics jargon for "estimated standard deviation." Any estimator has a standard error. When you see "standard error" in statistical output, it's telling you about precision. Smaller standard error means more precise estimates.

**Common notation**: se of X-bar equals s over the square root of n

Remember: Standard error decreases with the square root of n. Want half the standard error? You need four times the sample size!

> **Key Concept**: The standard error se of X-bar equals s over the square root of n measures how precise our sample mean is as an estimate of mu. It's the sample-based version of sigma over the square root of n (which we can't calculate because sigma is unknown). The standard error tells us: "If we repeated this sampling process, the sample mean would typically vary from the true mean by about se." Smaller standard errors mean more reliable estimates.

### Summary for the Sample Mean

Let's recap the key results we've established:

**1. Random variables and realizations**:
- Sample values x-sub-1 through x-sub-n are observed outcomes
- These are realizations of random variables X-sub-1 through X-sub-n

**2. Assumptions (simple random sample)**:
- Each X-sub-i has the same mean mu and variance sigma-squared
- Observations are independent of each other

**3. Mean and variance of X-bar**:
- The sample mean X-bar has mean mu (unbiased!)
- The sample mean X-bar has variance sigma-squared over n (more precise with larger n)

**4. Standardization**:
- Z equals the quantity X-bar minus mu, all divided by sigma over the square root of n
- This standardized version has mean 0 and variance 1

**5. Central Limit Theorem**:
- As n goes to infinity, Z becomes standard normal
- This means X-bar is approximately normal with mean mu and variance sigma-squared over n for large samples

**6. Standard error**:
- Since sigma is unknown, we estimate it with s
- Standard error: se of X-bar equals s over the square root of n
- This measures the precision of our estimate

Now let's see these ideas in action with real data.

## 3.5 Sampling from a Population: 1880 Census

We've worked with coin tosses—a simple but artificial example. Let's now apply these ideas to real population data.

**The population**: The 1880 U.S. Census recorded every person living in the United States.
- Population size: N equals 50,169,452 people
- Average age: mu equals 24.13 years (we know this because we have the full population!)
- Standard deviation: sigma equals 18.61 years

This is a rare situation where we actually know the population parameters. We can use this to verify that our sampling theory works in practice.
- histogram is given in the next slide.


### Example: 1880 Census (continued)

- Population
- Probabilities decline with age (clearly not the normal)
- Peaks due to rounding at five and ten years

Entire 1880 Census
![](https://cdn.mathpix.com/cropped/72a3f87a-41ec-4ad3-a2db-effc82ed52f5-26.jpg?height=533&width=759&top_left_y=353&top_left_x=253)

### Example: 1880 Census (continued)

**One sample of size 25**:

Let's draw a random sample of 25 people from the 1880 Census population.
- Sample mean age: x-bar equals 27.84 years
- Sample standard deviation: s equals 20.71 years

Notice these are close to, but not exactly equal to, the population values (mu equals 24.13 and sigma equals 18.61). That's the nature of random sampling—each sample is different!

**What happens with many samples?**

To see how sample means behave, let's repeat this experiment 100 times—drawing 100 different random samples, each with 25 people.

Results across the 100 samples:
- First sample: x-bar-sub-1 equals 27.84
- Second sample: x-bar-sub-2 equals 19.40
- Third sample: x-bar-sub-3 equals 23.28
- And so on...

**Checking our theory**:

Now let's see if the theory holds up:
- Average of the 100 sample means: 23.78
  - Theory predicts: mu equals 24.13 ✓ (very close!)
- Standard deviation of the 100 sample means: 3.76
  - Theory predicts: sigma over the square root of n equals 18.61 divided by 5 equals 3.72 ✓ (almost perfect!)

The theory works! The histogram of sample means is shown in the next figure.


### Example: 1880 Census (continued)

- 100 different means from 100 different samples, each of size 25
- histogram (left) and kernel density estimate (right)
- looks like normal with mean mu and standard deviation much less than sigma
![](https://cdn.mathpix.com/cropped/72a3f87a-41ec-4ad3-a2db-effc82ed52f5-28.jpg?height=433&width=538&top_left_y=387&top_left_x=82)
![](https://cdn.mathpix.com/cropped/72a3f87a-41ec-4ad3-a2db-effc82ed52f5-28.jpg?height=405&width=541&top_left_y=389&top_left_x=644)


## 3.6 Estimation of the Sample Mean

We want a good point estimate of the population mean mu. But why use x-bar? Why not use the sample median, or the midpoint between the minimum and maximum, or something else?

To answer this, we need criteria for what makes an estimator "good." A desirable estimator should:
- Be centered on the true parameter (no systematic error)
- Have as little variability around the parameter as possible (high precision)

Let's formalize these ideas.

### Parameter, Estimator and Estimate

First, let's clarify three terms that sound similar but mean different things:

**Parameter**: A fixed (but unknown) population characteristic.
- Example: mu (the true population mean age in 1880)

**Estimator**: A formula or method for estimating a parameter from sample data.
- Example: X-bar (the sample mean)—a random variable before we collect data

**Estimate**: The actual numerical value we get when we apply the estimator to our specific sample.
- Example: x-bar equals 27.84 years (what we computed from our particular sample of 25 people)

Think of it this way: The parameter is what we want to know. The estimator is our strategy. The estimate is our answer.

### Unbiased Estimators

An **unbiased estimator** has no systematic error. On average, across all possible samples, it hits the target.

**Formal definition**: An estimator is unbiased if its expected value equals the parameter.

**Example**: The sample mean X-bar is unbiased for mu because E of X-bar equals mu.

**Analogy**: Imagine shooting arrows at a bullseye. An unbiased shooter might miss left or right on any given shot, but their shots average to the center. A biased shooter consistently misses in one direction.

The sample mean is like the unbiased shooter—individual samples vary, but on average they hit mu.

### Efficient Estimators (Minimum Variance)

Being unbiased isn't enough. We also want precision—an estimator that doesn't vary too much from sample to sample.

Among unbiased estimators, we prefer the one with the smallest variance. This is called the **efficient estimator** or **best estimator**.

**Why does the sample mean win?**

For many common distributions (normal, Bernoulli, binomial, Poisson), the sample mean has variance sigma-squared over n. No other unbiased estimator beats this. Even for other distributions, the sample mean is usually very close to having minimum variance.

**What about the median?** The sample median is also unbiased for symmetric distributions, but it generally has higher variance than the mean. The mean uses all the data; the median only uses the middle value(s). Using more information typically gives better estimates.

**Bottom line**: This is why we use the sample mean—it's hard to beat!

### Consistent Estimators

Consistency asks: "If we could keep increasing the sample size forever, would our estimator eventually nail down the true parameter?"

**Formal definition**: A consistent estimator converges to the true parameter as sample size approaches infinity.

**Sufficient conditions for consistency**:
1. Any bias vanishes as n goes to infinity
2. Variance goes to zero as n goes to infinity

**The sample mean is consistent** because:
- It's unbiased (no bias to begin with)
- Its variance sigma-squared over n goes to zero as n goes to infinity

**Intuition**: With infinite data, we'd know mu exactly. Consistency says our estimator approaches this ideal as we get more data.

> **Key Concept**: A good estimator should be unbiased (E of X-bar equals mu), efficient (minimum variance among unbiased estimators), and consistent (converges to mu as n grows). The sample mean X-bar satisfies all three criteria under simple random sampling. It has no systematic error, uses information efficiently, and improves with more data. This triple win is why the sample mean is the standard estimator for mu across virtually all of statistics.

## 3.7 Samples other than Simple Random Samples

Our analysis so far has assumed **simple random sampling**: observations are independent and come from the same distribution (with common mean mu and variance sigma-squared). But real-world sampling is often more complex. Let's explore what happens when these assumptions don't hold.

### Representative but Dependent Samples

Sometimes observations come from the same distribution but aren't statistically independent.

**Example**: Surveying people in the same household. Each person's income comes from the same income distribution, but family members' incomes are correlated—if one earns high income, others in the household might too.

**Good news**: The sample is still representative (same distribution). We can still use the sample mean x-bar.

**Adjustment needed**: The standard error formula changes. Independence matters for calculating se of x-bar. When observations are correlated, we need an alternative formula that accounts for the correlation structure. We'll cover this in later chapters.


### Nonrepresentative Samples: The Big Problem

A much more serious issue arises when different observations have different population means. This is a **nonrepresentative sample**.

**Example: Golf Digest readers**

Suppose you want to estimate average income in the United States, so you survey readers of Golf Digest magazine.

**The problem**: Golf Digest readers aren't typical Americans. They likely have higher incomes on average (golf is expensive!). If mu-sub-golfer equals 90,000 dollars but mu-sub-population equals 50,000 dollars, your sample mean will systematically overestimate the population mean.

This is **sampling bias**—your estimate is wrong in a predictable direction. No amount of additional data will fix this. Surveying 10,000 Golf Digest readers doesn't help if they're all unrepresentative!

**The fix**: If we know the **inclusion probabilities**—how likely each type of person is to appear in our sample—we can use weighted averages to correct the bias.


### Weighted Means: The Solution

When inclusion probabilities are known, we can fix nonrepresentative samples using weights.

**Definitions**:
- pi-sub-i equals the probability that person i is included in the sample
- w-sub-i equals 1 over pi-sub-i is the sampling weight for person i

**Intuition**: If Golf Digest readers have inclusion probability 0.10 (10% chance of being sampled) while non-readers have probability 0.01 (1% chance), we should down-weight Golf Digest readers by using w equals 1 over 0.10 equals 10, and up-weight non-readers by using w equals 1 over 0.01 equals 100.

**Weighted mean formula**:

x-bar-sub-w equals the quantity the sum from i equals 1 to n of w-sub-i times x-sub-i, all divided by the quantity the sum from i equals 1 to n of w-sub-i.

This weighted mean corrects for over-representation of some groups and under-representation of others.

**Important caveat**: This only works if we **know** the inclusion probabilities. In practice, we often don't know them precisely, which is why **good study design**—selecting a genuinely representative sample—is so critical. Statistics can't save you from a fundamentally flawed sampling strategy!

> **Key Concept**: Simple random sampling assumes observations are independent and have the same population mean mu. When observations are correlated but still representative, we can adjust standard error formulas. When samples are nonrepresentative—different groups have different means—we face serious bias. If inclusion probabilities are known, weighted means (with weights w-sub-i equals 1 over pi-sub-i) can correct this bias. But the best approach is to design representative samples from the start, since statistical fixes can't compensate for fundamentally biased sampling.

## 3.8 Computer Generation of a Random Variable

You might wonder: "How did we generate those 400 coin-toss samples or draw random people from the 1880 Census?" The answer is computer simulation, which has become an essential tool for understanding and demonstrating statistical concepts.

### The Foundation: Uniform Random Number Generators

Modern statistical software relies on **pseudo-random number generators** that create values between 0 and 1 with two key properties:

**Property 1: Uniformity**
- Any value between 0 and 1 is equally likely
- Think of it as spinning a perfectly calibrated wheel where every point on the wheel has the same chance

**Property 2: Independence**
- Each generated number doesn't depend on the previous ones
- Just like real coin tosses, past outcomes don't influence future outcomes

**Why "pseudo"?** These aren't truly random—they're generated by mathematical formulas. But they're good enough to behave like truly random numbers for practical purposes.

### Simulating Coin Tosses

How do we turn uniform random numbers into coin tosses?

**Simple rule**: Draw a uniform random number between 0 and 1.
- If the number exceeds 0.5, call it heads (X equals 1)
- If the number is 0.5 or below, call it tails (X equals 0)

**To simulate 30 tosses**: Draw 30 uniform random numbers and apply this rule to each.

**Example**:
- Draw 0.73 → exceeds 0.5 → heads
- Draw 0.21 → below 0.5 → tails
- Draw 0.89 → exceeds 0.5 → heads
- And so on...

This is exactly how we generated the 400 samples of 30 tosses in Section 3.3!

### Simulating Census Sampling

The same logic works for more complex examples, like drawing random people from the 1880 Census.

**The approach**: Divide the interval from 0 to 1 into N equal segments, where N equals 50,169,452 (the population size). Each segment represents one person in the census.

**Selection rule**:
- If the uniform random number falls between 0 and 1 over N, select person 1
- If it falls between 1 over N and 2 over N, select person 2
- And so on...

This gives every person an equal chance of being selected—a genuine simple random sample!

### The Importance of Seeds

There's one catch with pseudo-random number generators: they need a starting point, called a **seed**.

**What's a seed?** A number that initializes the random number generator. The same seed always produces the same sequence of "random" numbers.

**Why this matters**:
- **Reproducibility**: Setting the seed (e.g., seed equals 10101) lets others replicate your exact results
- **Debugging**: If something goes wrong, you can re-run the simulation with the same seed to investigate
- **Transparency**: Readers can verify your work by using the same seed

**Best practice**: Always set the seed at the beginning of your simulation code. Document what seed you used. This turns "random" analysis into reproducible science.

**Example in practice**: When we generated those 400 coin-toss samples in Section 3.3, we set a seed first. That's why the figures show specific histograms—someone else using the same seed would get identical results.


### Some in-class Exercises

(1) Suppose X equals 100 with probability 0.8 and X equals 600 with probability 0.2. Find the mean, variance and standard deviation of X.
(2) Consider random samples of size 25 from the random variable X that has mean 100 and variance 400. Give the mean, variance and standard deviation of the mean X-bar.

---

## Key Takeaways

**Random Variables and Probability Distributions (Section 3.1):**

Understanding random variables is the foundation of statistical thinking. Here are the key ideas:

- A **random variable X** represents uncertainty—its value depends on unpredictable experimental outcomes
- **Notation convention**: Upper case (X, Y, Z) for random variables before observation; lower case (x, y, z) for realized values after observation
- The **mean** mu (expected value of X) is the probability-weighted average of all possible values: mu equals the sum over x of x times the probability that X equals x
- The **variance** sigma-squared (expected value of X minus mu squared) measures how spread out values are: sigma-squared equals the sum over x of the quantity x minus mu squared times the probability that X equals x
- The **standard deviation** sigma (square root of sigma-squared) measures spread in the original units of X
- **Example - fair coin**: With X taking values 0 or 1 with equal probability, mu equals 0.5 and sigma equals 0.5
- **Example - unfair coin**: With probability of heads equals 0.6, we get mu equals 0.6 and sigma-squared equals 0.24

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

The Central Limit Theorem is arguably the most important result in statistics. Here's what it tells us:

- **Standardization first**: Create Z equals the quantity X-bar minus mu, all divided by sigma over the square root of n, which has mean 0 and variance 1
- **The remarkable result**: As n grows large, Z becomes approximately normally distributed with mean 0 and variance 1
- **Converting back to X-bar**: This means X-bar is approximately normal with mean mu and variance sigma-squared over n for large samples
- **The magic**: This works **regardless of what X looks like**! X could be binary, skewed, discrete—doesn't matter. As long as it has finite mean and variance, averages become normal
- **Why it matters**: Normality emerges from averaging itself, not from the original data being normal. This is why normal-based methods (confidence intervals, hypothesis tests) work so widely
- **Technical note**: The CLT holds under assumptions A-C (common mean, common variance, independence) and even under weaker conditions
- **Practical impact**: The CLT is why statistical inference is possible across countless applications, from opinion polls to medical trials to quality control

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

This real-world example confirms our theory works in practice:

- **The population**: All 50,169,452 people in the 1880 U.S. Census, with mu equals 24.13 years and sigma equals 18.61 years
- **Important**: The population distribution is NOT normal—it declines with age and has spikes at multiples of 5 (rounding effects)
- **One sample** (n equals 25): Gave x-bar equals 27.84 and s equals 20.71—close to, but not exactly, the population values
- **100 samples** (each n equals 25):
  - Average of the 100 sample means: 23.78 (very close to mu equals 24.13) ✓
  - Standard deviation of the 100 sample means: 3.76 (very close to theoretical sigma over the square root of n equals 3.72) ✓
- **The distribution** of sample means looks approximately normal, despite the non-normal population
- **What this proves**: The Central Limit Theorem isn't just theory—it actually works! Even with a skewed, non-normal population, sample means become approximately normal. This is why we can use normal-based methods in real applications

**Parameters, Estimators, and Estimates (Section 3.6):**

These three terms sound similar but mean very different things. Keep them straight:

- **Parameter**: The unknown truth we want to know—a fixed constant like population mean mu
- **Estimator**: Our strategy for estimating the parameter—a random variable like X-bar (before collecting data)
- **Estimate**: The actual number we calculated from our specific sample—a realized value like x-bar equals 27.84 (after collecting data)
- **Think of it this way**: The parameter is our target. The estimator is our method of aiming. The estimate is where our shot landed
- **Example**: We want to know mu (parameter). We decide to use the sample mean X-bar (estimator). We collect data and get x-bar equals 27.84 (estimate)

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

Being unbiased isn't enough—we also want precision. Here's why the sample mean wins:

- **Definition**: An efficient estimator achieves minimum variance among unbiased estimators—it's as precise as possible
- **The sample mean's performance**: Under assumptions A-C, X-bar has variance sigma-squared over n
- **When it's optimal**: For normal, Bernoulli, binomial, and Poisson distributions, X-bar is provably the best unbiased estimator—nothing beats it
- **When it's near-optimal**: For most other distributions, X-bar has variance very close to the theoretical minimum
- **Comparison to alternatives**: The sample median is also unbiased for symmetric distributions, but typically has higher variance than X-bar because it uses less information (only the middle values, not all the data)
- **Bottom line**: X-bar uses all the data efficiently, which is why it's the default choice across statistics

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
