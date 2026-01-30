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

In Chapter 5, we learned to draw a regression line through our data. But a crucial question remains: How does this sample line relate to the true relationship in the population? If we drew a different sample, would we get a different line? (Yes!) And if so, how much would it vary? These questions lead us to the statistical theory of regression—understanding the OLS estimator as a random variable with predictable properties.

## 6.1 Population Model: Conditional Mean of y given x

When we fit a regression line to sample data, we get b-one plus b-two times x. This is our estimate. But what's the truth in the population?

We assume the **population model** is also a line, but with unknown parameters:

beta-one plus beta-two times x

where beta (Greek letter) denotes unknown population parameters. Why Greek letters? By convention, we use Greek for population parameters (what we want to know) and Roman letters for sample estimates (what we calculate).

**More formally**: We assume the **conditional mean** of y is linear in x:

The expected value of Y given X equals x, equals beta-one plus beta-two times x.

**What is this conditional mean?** It's the probability-weighted average of all possible y values for a given x value.

**Example**: Earnings conditional on years of schooling. For people with 12 years of education, earnings vary—some earn 30,000 dollars, others 50,000, others 80,000. The conditional mean is the average earnings across all people with 12 years of education. We assume this average changes linearly as education changes.

**How this extends Chapter 3**: In Chapter 3, we worked with the expected value of Y—the unconditional mean, averaging over all observations regardless of any other variable. Here, the expected value of Y given X equals x is a **conditional** mean—the average of Y for observations with a specific x value. This allows the mean to vary with x.


### Population Conditional Mean (continued)

Our **key assumption**: The conditional mean is linear in x.

The expected value of Y given X equals x, equals beta-one plus beta-two times x.

Or using simpler notation (mixing uppercase and lowercase):

The expected value of y given x equals beta-one plus beta-two times x.

**Important caveat**: Linearity is an assumption, not a mathematical fact. In general, conditional means need not be linear!

**Example of a linear conditional mean** (Case 1):

Suppose the conditional means are:
- E of Y given X equals 1 equals 5
- E of Y given X equals 2 equals 7
- E of Y given X equals 3 equals 9

Notice the pattern: each increase in X by 1 unit increases the conditional mean by 2 units. This is linear! We can write this as: E of Y given X equals x equals 3 plus 2 times x.

**Example of a nonlinear conditional mean** (Case 2):

Now suppose:
- E of Y given X equals 1 equals 5
- E of Y given X equals 2 equals 7 (increase of 2)
- E of Y given X equals 3 equals 12 (increase of 5!)

The increases aren't constant. This violates linearity. No straight line can fit this pattern perfectly.

**What do we do about nonlinearity?** We'll tackle that in Chapter 9 using transformations like logarithms. For now, we assume linearity holds—or at least provides a good approximation.


### Error Term

Here's a key insight: Individual observations don't fall exactly on the population line. We don't have:

y equals beta-one plus beta-two times x (not exact!)

Instead, we have:

E of y given x equals beta-one plus beta-two times x (on average)

**What's the difference?** Individual y values deviate from this conditional mean. We call this deviation the **error term** u.

**Formal definition**:

u equals y minus the expected value of y given x, which equals y minus the quantity beta-one plus beta-two times x.

Rearranging:

y equals beta-one plus beta-two times x, plus u

**Why can't we see u?** Because beta-one and beta-two are unknown! We've never observed the entire population, so we don't know where the population line is. Without the population line, we can't calculate the errors relative to it.

### Error Term versus Residual - a crucial distinction

This is one of the most important (and confusing!) conceptual distinctions in regression. Pay close attention:

**Error term u** (unobserved):
- The distance between y and the **unknown population line** (beta-one plus beta-two times x)
- Shown as distance to the solid line in the left panel below
- We can never see u because we don't know beta-one and beta-two

**Residual e** (observed):
- The distance between y and the **known fitted line** (b-one plus b-two times x)
- Shown as distance to the dashed line in the right panel below
- We CAN see e because we calculated b-one and b-two from our sample

![](https://cdn.mathpix.com/cropped/1db1a0ef-9c44-414f-9671-ab8a889b52b7-08.jpg?height=449&width=516&top_left_y=397&top_left_x=75)
![](https://cdn.mathpix.com/cropped/1db1a0ef-9c44-414f-9671-ab8a889b52b7-08.jpg?height=445&width=480&top_left_y=399&top_left_x=712)

**Think of it this way**: Errors are theoretical (relative to the unknowable truth). Residuals are empirical (relative to our estimate from the data).


### Error Term is assumed to have mean zero

We've established that:

y equals beta-one plus beta-two times x, plus u

But what properties should the error term u have? The most important assumption is that **errors average to zero at each x value**.

**The assumption**:

The expected value of u given x equals zero.

**What this means intuitively**:
- For any given x value (say, years of education equals 12), some observations will have positive errors (earnings above the line)
- Other observations will have negative errors (earnings below the line)
- But on average, across all people with education equals 12, the errors balance out to zero

**Why this assumption matters**: It ensures the population line is truly centered at the conditional mean!

**Here's the proof**:

Start with: y equals beta-one plus beta-two times x, plus u

Take expectations conditional on x:

The expected value of y given x equals the expected value of the quantity beta-one plus beta-two times x, plus u, all given x.

Since beta-one plus beta-two times x is not random (it's just a number once we condition on x), we can pull it outside:

This equals beta-one plus beta-two times x, plus the expected value of u given x.

Now use our assumption that the expected value of u given x equals zero:

This equals beta-one plus beta-two times x, plus zero, which equals beta-one plus beta-two times x.

**Conclusion**: The zero conditional mean assumption ensures the population regression line correctly represents the conditional mean of y given x. Without this assumption, our line would be systematically too high or too low!

> **Key Concept**: The population regression line E of y given x equals beta-one plus beta-two times x describes how the average value of y varies with x. The error term u equals y minus E of y given x captures individual deviations from this average. The assumption that the expected value of u given x equals zero is crucial—it ensures errors balance out at every x value, making our regression line correctly centered. This zero conditional mean assumption is the foundation for unbiased OLS estimation.

### Population Conditional Variance of y given x

We've established that errors have mean zero at each x value. But how spread out are they? This matters because **error variability determines the precision of our estimates**.

Think of it this way: If observations are tightly clustered around the population line (small error variance), we can estimate the line precisely. If observations are scattered far from the line (large error variance), our estimates will be noisy and imprecise.

**The homoskedasticity assumption**: We assume the error variance is **constant** across all x values:

The variance of u given x equals sigma-u-squared

This assumption has a fancy name: **homoskedasticity** (pronounced "homo-skeh-das-TIS-ity").

**Etymology**:
- "Homos" is Greek for "same"
- "Skedastic" comes from the Greek word for "scattering" or "dispersing"
- Together: "same scattering"—the errors scatter equally at all x values

**What this means visually**: Imagine looking at a scatterplot with the population regression line. Homoskedasticity means the vertical spread of points around the line is the same whether x equals 1, x equals 10, or x equals 100. The "cloud" of points has constant width.

**Can this assumption be relaxed?** Absolutely! In fact, it often IS relaxed in practice. Heteroskedasticity (varying error variance) is common in economic data. We'll learn how to handle this in later chapters using robust standard errors.

**Why does variance of y equal variance of u?**

Since y equals beta-one plus beta-two times x, plus u, and the only random component (given x) is u, all the variability in y comes from u. Therefore:

The variance of y given x equals the variance of u given x, which equals sigma-u-squared.

**Bottom line**: Greater error variance means noisier data, which leads to less precise estimates. This is why we care about sigma-u-squared—it directly affects the reliability of our regression coefficients.

> **Key Concept**: Homoskedasticity assumes constant error variance across all x values: the variance of u given x equals sigma-u-squared for all x. This simplifies statistical formulas and is a standard assumption in introductory regression. The error term is the only source of randomness in y given x, so the variance of y given x also equals sigma-u-squared. Greater error variance means more noise and less precise estimates. While homoskedasticity is often violated in real data, we can use robust standard errors to account for this—a topic for later chapters.

### Summary: From Univariate to Bivariate Analysis

Let's connect this back to what we learned in Chapter 3. We're generalizing from one variable to two variables.

**Univariate analysis** (Chapter 3):
- We have a simple random sample: y-sub-1, y-sub-2, through y-sub-n
- Each observation has the same distribution:

Y-sub-i is distributed with mean mu and variance sigma-squared.

- The mean is constant—it doesn't depend on anything else

**Regression analysis** (this chapter):
- We have pairs of observations: (x-sub-1, y-sub-1), (x-sub-2, y-sub-2), through (x-sub-n, y-sub-n)
- Now the mean of y **depends on x**:

y-sub-i given x-sub-i is distributed with mean beta-one plus beta-two times x-sub-i, and variance sigma-u-squared.

**What changed?**
- **Mean**: Was constant (mu), now varies with x (beta-one plus beta-two times x)
- **Variance**: Still constant (sigma-u-squared) under homoskedasticity

**Why this matters**: Regression lets us model how one variable (earnings) varies with another (education). Univariate analysis only tells us the average earnings across everyone. Regression tells us how average earnings change as education changes. This is the power of conditional analysis!

> **Key Concept**: Regression extends univariate analysis by allowing the mean to vary with x. In univariate analysis, every Y-sub-i has the same mean mu. In regression, y-sub-i given x-sub-i has a mean that depends on x-sub-i through the linear function beta-one plus beta-two times x-sub-i. The variance remains constant at sigma-u-squared under homoskedasticity. This conditional framework lets us model relationships between variables—how y changes with x—rather than just describing y in isolation.

## 6.2 Examples of Sampling from a Population

We've established the theoretical framework. Now let's see it in action! Just as we did in Chapter 3 with the sample mean, we'll demonstrate OLS properties using simulation and real data.

**Two complementary experiments**:

**Experiment 1: Computer-generated data**
- Generate 400 samples from a known model: y equals beta-one plus beta-two times x, plus u
- Since we set beta-one and beta-two ourselves, we know the truth
- Run regression on each sample to get 400 estimates of b-one and b-two
- Compare these estimates to the known truth

**Experiment 2: Real population data**
- Draw 400 samples from the U.S. 1880 Census (males aged 60-69)
- The full census gives us the population regression line (the truth)
- Run regression on each sample
- See how sample estimates vary around this population truth

**What we'll discover** (spoiler alert!):
- The average of the 400 slope estimates is very close to the true beta-two ✓ (unbiasedness)
- The 400 slope estimates form an approximately normal distribution ✓ (Central Limit Theorem)
- The same patterns hold for the intercept b-one

These experiments mirror what we did in Chapter 3 for the sample mean, but now applied to regression coefficients. Let's dive in!


### Single Sample Generated from an Experiment

Let's start simple with just 5 observations. This lets us see exactly what's happening.

**The true population model** (what we set up):

y equals 1 plus 2 times x, plus u

where:
- beta-one equals 1 (true intercept)
- beta-two equals 2 (true slope—each unit increase in x increases y by 2 on average)
- u is distributed normal with mean zero and variance 4
- x takes values: 1, 2, 3, 4, 5

**Note**: We're adding the assumption that errors are normally distributed. This isn't required for unbiasedness, but it helps with exact (not just approximate) inference in small samples.

**Generating one sample**:

Using a random number generator, we drew 5 error terms. Here's what we got:

| Obs | x | E(y|x) | u (error) | y (observed) |
|-----|---|--------|-----------|--------------|
| 1 | 1 | 3 | 1.69 | 4.69 |
| 2 | 2 | 5 | -0.32 | 4.68 |
| 3 | 3 | 7 | -2.51 | 4.49 |
| 4 | 4 | 9 | -1.63 | 7.37 |
| 5 | 5 | 11 | -2.39 | 8.61 |

**What happened?** The expected values follow the line 1 plus 2 times x perfectly. But each observation gets a random error, pulling it above or below the line. Observation 1 got a positive error (1.69), pushing y above 3. Observation 3 got a negative error (-2.51), pulling y below 7.

**Fitting the regression**:

When we run OLS on these 5 points, we get:

Sample regression line: y-hat equals 2.81 plus 1.05 times x

**Crucial observation**: Our estimates (b-one equals 2.81, b-two equals 1.05) are NOT equal to the true parameters (beta-one equals 1, beta-two equals 2). This is sampling variability! We got unlucky with this particular sample—the negative errors for x equals 3, 4, 5 flattened our fitted slope.

Population line
![](https://cdn.mathpix.com/cropped/1db1a0ef-9c44-414f-9671-ab8a889b52b7-14.jpg?height=395&width=537&top_left_y=426&top_left_x=81)

Regression line
![](https://cdn.mathpix.com/cropped/1db1a0ef-9c44-414f-9671-ab8a889b52b7-14.jpg?height=395&width=545&top_left_y=426&top_left_x=643)

> **Key Concept**: A single sample produces estimates b-one and b-two that typically differ from the true population parameters beta-one and beta-two due to sampling variability. In this example, the population line is y equals 1 plus 2 times x (beta-one equals 1, beta-two equals 2), but the sample of 5 observations yields y-hat equals 2.81 plus 1.05 times x (b-one equals 2.81, b-two equals 1.05). This illustrates that sample estimates are random variables that vary from sample to sample.

### Many Samples Generated from an Experiment

One sample showed us that estimates vary from the truth. But how much do they vary? And do they vary randomly or systematically? To answer this, we need many samples.

**Updated experiment** (larger sample, random x):

Same population model:

y equals 1 plus 2 times x, plus u

where:
- beta-one equals 1, beta-two equals 2 (same true parameters)
- u is distributed normal with mean zero and variance 4 (same error distribution)
- **New**: x is now drawn from a standard normal distribution (mean 0, variance 1)
- **New**: Sample size is n equals 30 (instead of 5)

**Why random x?** This makes the experiment more realistic. In economics, we rarely control x values—we observe them in the wild.

### Three Generated Samples yield three different lines

Before analyzing 400 samples, let's look at just three to build intuition.

Below are scatterplots and fitted regression lines from three different samples, each with 30 observations. Notice what varies:
- The scatter of points differs (different random errors)
- The fitted lines have different intercepts and slopes
- But all three fitted lines are reasonably close to the true line (1 plus 2 times x)

Sample 1
![](https://cdn.mathpix.com/cropped/1db1a0ef-9c44-414f-9671-ab8a889b52b7-16.jpg?height=282&width=348&top_left_y=424&top_left_x=84)

Sample 2
![](https://cdn.mathpix.com/cropped/1db1a0ef-9c44-414f-9671-ab8a889b52b7-16.jpg?height=282&width=346&top_left_y=424&top_left_x=463)

Sample 3
![](https://cdn.mathpix.com/cropped/1db1a0ef-9c44-414f-9671-ab8a889b52b7-16.jpg?height=287&width=349&top_left_y=423&top_left_x=839)

> **Key Concept**: Three different random samples from the same population produce three different regression lines, illustrating sampling variability. Each sample yields different estimates of beta-one and beta-two, but all estimates cluster around the true population values. This demonstrates that the OLS estimators b-one and b-two are random variables whose distributions depend on the sampling process.

### 400 Generated Samples of Size 30

Now for the full experiment! We generated 400 different samples, each with 30 observations, and ran regression on each. This gives us 400 different b-one estimates and 400 different b-two estimates.

**The results are striking**:

**Left panel - Distribution of 400 slope estimates**:
- True parameter: beta-two equals 2.0
- Average of 400 estimates: 1.979
- **Difference**: Only 0.021! The estimates are centered almost perfectly on the truth.

**Right panel - Distribution of 400 intercept estimates**:
- True parameter: beta-one equals 1.0
- Average of 400 estimates: 1.039
- **Difference**: Only 0.039! Again, nearly perfect centering.

![](https://cdn.mathpix.com/cropped/1db1a0ef-9c44-414f-9671-ab8a889b52b7-17.jpg?height=402&width=529&top_left_y=407&top_left_x=89)

Generated data: 400 Intercepts
![](https://cdn.mathpix.com/cropped/1db1a0ef-9c44-414f-9671-ab8a889b52b7-17.jpg?height=372&width=529&top_left_y=436&top_left_x=654)

**Three crucial observations**:

**1. Unbiasedness confirmed**: Individual samples gave us estimates far from the truth (remember b-two equals 1.05 from our first sample?). But on average across many samples, we hit the target. This is exactly what unbiasedness means!

**2. Approximate normality**: Both histograms look like bell curves—the normal distribution. This demonstrates the Central Limit Theorem. Even though individual errors are random, the **average behavior** of our estimates is predictable and normal.

**3. Variability is real**: The estimates don't all equal 2.0 and 1.0. They vary! Some samples gave b-two around 1.7, others around 2.3. This sampling variability is unavoidable. But we can measure and account for it using standard errors (coming in Section 6.3).

> **Key Concept**: Repeating the sampling process 400 times reveals the sampling distribution of OLS estimators. The average of 400 slope estimates (1.979) nearly equals the true beta-two (2.0), demonstrating unbiasedness—OLS is correct on average. The approximately normal shape of both distributions confirms the Central Limit Theorem applies to regression coefficients, not just sample means. Individual estimates vary due to different random samples, but this variation follows a predictable, normal pattern.

### Many Samples Generated from a Finite Population

Now let's move from computer-generated data to real population data—the 1880 U.S. Census.

**The population**: A complete enumeration of everyone living in the United States in 1880.

**Our focus**: Men aged 60 to 70 years (population size: 1,058,475 men)

**The relationship we're studying**:
- y equals labforce (labor force participation)
  - Equals 1 if in the labor force
  - Equals 0 if not in the labor force
- x equals age (ranging from 60 to 70 years)

**Population statistics**:
- Overall labor force participation rate: 0.8945 (89.45% were working!)
- This was 1880—no Social Security, no retirement pensions. Most older men had to keep working.

**The question**: Does labor force participation decline with age even among these older workers? Let's find out.

### Population Regression Line

Since we have the **entire population** (all 1,058,475 men), we can calculate the true population regression line. This is rare! Usually we never know the population truth.

**The population regression model**:

labforce equals beta-one plus beta-two times age

**Fitting this to all 1,058,475 observations**, we get:

labforce equals 1.593 minus 0.0109 times age

**Interpreting the coefficients**:
- Intercept: beta-one equals 1.593 (hypothetical participation rate at age 0—not meaningful here)
- **Slope: beta-two equals negative 0.0109** (this is what matters!)

**What does the slope tell us?** Each additional year of age reduces the probability of labor force participation by 0.0109, or by **1.09 percentage points**.

**Example**: Compare a 60-year-old to a 65-year-old:
- 5-year age difference
- Predicted participation drop: 5 times 0.0109 equals 0.0545 (about 5.5 percentage points lower)

This negative relationship makes intuitive sense—even in 1880, as men aged from 60 to 70, some retired or became unable to work.

> **Key Concept**: With the complete 1880 Census population of 1,058,475 men aged 60-70, we can calculate the true population regression line: labforce equals 1.593 minus 0.0109 times age. This gives us beta-two equals negative 0.0109, meaning each additional year reduces labor force participation probability by 1.09 percentage points. Having the full population lets us treat this as the benchmark "truth" against which sample estimates will be compared—just like we knew the true parameters in our computer simulation.

### 400 Samples of Size 200

Now the experiment! We randomly drew 400 samples of size 200 from this population of over one million men, and ran regression on each sample.

**Why size 200?** Because the regression fit is poor (R-squared approximately 0.01)—age alone doesn't explain much variation in labor force participation. With weak relationships, we need larger samples to get stable estimates.

**The results** (histograms of 400 estimates):

**Left panel - Distribution of 400 slope estimates**:
- True population parameter: beta-two equals negative 0.0109
- Average of 400 sample estimates: negative 0.0115
- **Difference**: Only 0.0006! Nearly perfect centering despite the weak relationship.

**Right panel - Distribution of 400 intercept estimates**:
- True population parameter: beta-one equals 1.593
- Average of 400 sample estimates: 1.636
- **Difference**: About 0.04—very close

![](https://cdn.mathpix.com/cropped/1db1a0ef-9c44-414f-9671-ab8a889b52b7-20.jpg?height=405&width=533&top_left_y=416&top_left_x=87)

Census data: 400 Intercepts
![](https://cdn.mathpix.com/cropped/1db1a0ef-9c44-414f-9671-ab8a889b52b7-20.jpg?height=375&width=532&top_left_y=446&top_left_x=653)

**Key observations**:

**1. Unbiasedness in real data**: Just like with computer-generated data, OLS is unbiased. The averages of our 400 estimates are very close to the population truth. This works even with messy real data!

**2. Approximate normality with binary y**: Labor force participation is binary (0 or 1), not continuous. Yet the distributions of slope and intercept estimates still look approximately normal. The Central Limit Theorem is robust!

**3. Works despite poor fit**: R-squared is only 0.01—age explains just 1% of the variation in labor force participation. Yet our estimates are still unbiased and approximately normal. OLS properties don't require a good fit!

> **Key Concept**: Real-world validation with 1880 Census data confirms OLS properties. Drawing 400 samples of size 200 shows: (1) Unbiasedness—average estimates nearly equal population parameters despite weak relationship, (2) Approximate normality—both distributions are bell-shaped even though the outcome is binary (0 or 1), and (3) Robustness—these properties hold even when R-squared is tiny (0.01). This demonstrates that OLS theory applies broadly, not just to idealized settings with perfect data and strong relationships.

## 6.3 Properties of the Least Squares Estimator

We've seen empirically that OLS works—estimates center on the truth and follow normal distributions. Now let's prove it mathematically. What are the theoretical properties of the OLS slope estimator?

**Recall the OLS slope formula** from Chapter 5:

b-two equals the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, times the quantity y-sub-i minus y-bar, all divided by the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared.

This looks like just arithmetic. But remember: y-sub-i is random (it contains the error u-sub-i). Different samples give different y values, hence different b-two values. So **b-two is a random variable**.

**Our goal**: Characterize this random variable. Specifically, find:
1. The expected value of b-two (Is it unbiased?)
2. The variance of b-two (How much does it vary?)
3. The distribution of b-two (Can we use normal-based inference?)

### A Key Mathematical Result

Here's a crucial algebraic trick. If we assume the population model is y-sub-i equals beta-one plus beta-two times x-sub-i, plus u-sub-i, we can rewrite the OLS formula as:

b-two equals beta-two plus the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, times u-sub-i, all divided by the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared.

**What does this mean?** The OLS estimate b-two equals the true parameter beta-two **plus** a weighted sum of the errors!

**Why this matters**: When we condition on the x values (treat them as fixed), the **only source of randomness** is the errors u-sub-i. This means:
- The expected value of b-two depends on the expected value of the errors
- The variance of b-two depends on the variance of the errors
- The distribution of b-two depends on the distribution of the errors

So everything hinges on what we assume about u-sub-i. Let's state those assumptions clearly.

> **Key Concept**: The OLS estimator can be decomposed as b-two equals beta-two plus a weighted sum of errors. This reveals that b-two is a random variable whose properties depend entirely on the error term u-sub-i. When we treat the regressors x-sub-i as fixed (conditioning on them), all randomness comes from errors. Understanding b-two's statistical properties therefore requires making assumptions about how errors behave.

### Data Assumptions

Before we even get to error assumptions, we need basic requirements for the data itself.

**Assumption D1: Variation in x**

We must have variation in the regressor. Formally: the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared, must be strictly greater than zero.

**What this means**: Not all x values can be the same. If x-sub-i equals x-bar for all i (everyone has the same education level, for example), we can't estimate how y changes with x. There's nothing to compare!

**Why it matters**: The OLS formula has this sum in the denominator. If it equals zero, we'd be dividing by zero—undefined!

**Assumption D2: Minimum sample size**

We need at least 3 observations for bivariate regression. With only 2 points, any line fits perfectly (two points determine a line), leaving no residuals to estimate the error variance.

**These are technical requirements**, not statistical assumptions. They just ensure the formulas work.


### Population Assumptions: The Big Four

Now for the crucial assumptions about the population model and errors. Everything we prove depends on these.

**Assumption 1: Correct Linear Model**

The population model is:

y-sub-i equals beta-one plus beta-two times x-sub-i, plus u-sub-i for all i.

**What this means**: The true relationship is linear, and we've specified it correctly. There are no missing variables, no wrong functional form.

**Assumption 2: Zero Conditional Mean Error**

The error has mean zero conditional on x:

The expected value of u-sub-i given x-sub-i equals zero for all i.

**What this means**: Errors average to zero at every x value. There's no correlation between x and u.

**Why this matters**: Violations cause **bias**. If high-x observations tend to have positive errors, OLS will incorrectly attribute that pattern to the slope. This is the omitted variable problem!

**Together, Assumptions 1-2 ensure**:

The expected value of y-sub-i given x-sub-i equals beta-one plus beta-two times x-sub-i.

These are the **essential** assumptions for unbiasedness. We'll maintain them throughout.

**Assumption 3: Homoskedasticity**

The error variance is constant across x values:

The variance of u-sub-i given x-sub-i equals sigma-u-squared for all i.

**What this means**: Error variability doesn't depend on x. The "scatter" around the line is the same whether x is small or large.

**Assumption 4: Independence**

Errors for different observations are independent:

u-sub-i is independent of u-sub-j for all i not equal to j.

**What this means**: One person's error doesn't affect another's. This is natural for cross-section data (person A's earnings surprise doesn't affect person B's).

**About Assumptions 3-4**: These affect variance calculations and standard errors, but NOT unbiasedness. We can (and often do) relax them using robust standard errors. More on this in Section 6.3 and Chapters 7 and 12.

> **Key Concept**: The four OLS assumptions form a hierarchy of importance. Assumptions 1-2 (correct linear model and zero conditional mean error) are **essential**—violations cause bias and inconsistency. Assumptions 3-4 (homoskedasticity and independence) are **helpful but not essential**—violations affect standard errors but not the slope estimates themselves. In practice, we maintain 1-2 strictly and relax 3-4 using robust methods. This is why omitted variables (violating Assumption 2) are so dangerous, while heteroskedasticity (violating Assumption 3) is merely inconvenient.

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

This is one of the most practical questions in regression: What determines how precise our slope estimate is?

**The answer is in the formula**. Recall the standard error of b-two:

The standard error of b-two equals the square root of s-e-squared divided by the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared.

**Smaller standard error means better precision**. So we want to:
- **Minimize the numerator** (s-e-squared)
- **Maximize the denominator** (sum of squared x deviations)

This gives us three actionable insights:

**Factor 1: Model fit**

**Better precision when**: s-e-squared is smaller (model fits well, residuals are small)

**Intuition**: If observations cluster tightly around the regression line, we can pinpoint the slope precisely. If they're scattered far from the line, the slope is uncertain.

**Example**: Regressing height on shoe size (strong relationship, small residuals) gives more precise slope estimates than regressing income on astrological sign (weak relationship, large residuals).

**Factor 2: Sample size**

**Better precision when**: n is larger (many observations)

**Intuition**: More data means more information. With 1,000 observations, we can estimate the slope much more precisely than with 10.

**How much better?** The sum from i equals 1 to n of the quantity x-sub-i minus x-bar squared grows roughly proportionally to n. So the standard error decreases roughly with one over the square root of n. To halve the standard error, you need **four times** the data!

**Factor 3: Regressor variation**

**Better precision when**: x values are widely scattered (high variance of x)

**Intuition**: Compare two datasets, both with n equals 100:
- **Dataset A**: Education ranges from 10 to 12 years (narrow range)
- **Dataset B**: Education ranges from 0 to 20 years (wide range)

Dataset B lets us see how earnings change across a much broader education spectrum, giving clearer evidence about the slope.

**Think of it geometrically**: With x values tightly clustered, small changes in the fitted line barely affect fit. With x values spread out, the line is "anchored" at both ends, making the slope more stable.

**Practical implications**:

When **designing studies**, aim for:
- Large samples (maximize n)
- Wide variation in x (sample across the full range of the explanatory variable)
- Good model specification (minimize unexplained variation)

When **analyzing existing data**, recognize that:
- Weak relationships (large s-e) yield imprecise estimates—don't over-interpret small coefficients
- Small samples need extra caution—standard errors will be large
- Limited variation in x (everyone has similar values) makes slope estimation difficult

> **Key Concept**: Three factors determine OLS precision: (1) Model fit—smaller residuals (s-e) mean more precise estimates; (2) Sample size—larger n reduces standard errors by approximately one over the square root of n; and (3) Regressor variation—wider spread in x values provides more information about the slope. These factors are multiplicative: a small sample with weak fit and limited x variation produces very imprecise estimates, while a large sample with good fit and wide x variation yields highly precise slopes. When planning studies, maximize sample size and x variation; when analyzing data, report standard errors to communicate precision honestly.

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