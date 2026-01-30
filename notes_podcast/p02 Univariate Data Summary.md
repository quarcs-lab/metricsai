# Chapter 2: Univariate Data Summary

## Learning Objectives

By the end of this chapter, you will be able to:
- Calculate and interpret summary statistics (mean, median, standard deviation, quartiles)
- Understand measures of data distribution (skewness, kurtosis)
- Choose appropriate visualizations for different data types
- Create and interpret histograms, box plots, and kernel density estimates
- Apply data transformations (logarithms, z-scores, growth rates)
- Recognize when to use different chart types (histograms, line charts, bar charts, pie charts)

---

Imagine you're analyzing earnings data for 171 workers. You have 171 individual numbers ranging from just over 1,000 dollars to 172,000 dollars. How do you make sense of this? Listing all 171 values would overwhelm anyone. This is where summary statistics come in—powerful tools that compress entire datasets into just a few meaningful numbers that tell the story of your data.

## 2.1 Summary Statistics for Numerical Data

Before we dive into calculations, let's understand what we're working with. When we collect data, we get observations—individual measurements or values.

- Observations for a sample of size n are denoted: x-sub-1, x-sub-2, and so on up to x-sub-n.

- **Notation:**
  - x-sub-1 is the first observation, and x-sub-n is the n-th observation
  - For cross-section data, the typical observation is the i-th, denoted x-sub-i
  - For time series data, it's more customary to use the subscript t

**Example: Sample mean or average**

How do we calculate an average? Simply add up all the observations and divide by how many there are.

The sample mean, x-bar, equals the sum of all observations divided by n. In formula form: x-bar equals one over n, times the sum from i equals 1 to n of x-sub-i.

This summation notation is just shorthand. It says: "add up all the x values (that's the sum symbol), then divide by n."

### 2.1.1 Summary Statistics Example: Earnings

**Example 2.1**: Earnings of Full-Time Working Women

Let's work with real data: annual earnings of 171 full-time working women aged 30 in 2010. "Full-time" means working at least 35 hours per week for at least 48 weeks per year.

Here's what the summary statistics reveal (rounded to the nearest dollar):

**Central tendency:**
- Mean earnings: 41,413 dollars
- Median (50th percentile): 36,000 dollars

**Spread:**
- Standard deviation: 25,527 dollars
- Range: from 1,050 dollars minimum to 172,000 dollars maximum
- Lower quartile (25th percentile): 25,000 dollars
- Upper quartile (75th percentile): 50,000 dollars

**Distribution shape:**
- Skewness: 1.71 (strongly right-skewed—a few very high earners pull the mean above the median)
- Kurtosis: 7.32 (fat tails—more extreme values than a normal distribution)

Notice something important: the mean (41,413 dollars) exceeds the median (36,000 dollars). This signals right-skewness—a small number of high earners pull the average upward.

### 2.1.2 Measures of Central Tendency

When we want to describe a "typical" value in our dataset, we have several choices. Let's explore the two most important: mean and median.

**The Mean (Average)**

The mean is what most people call "the average." Add up all the values, then divide by how many there are.

Formula: x-bar equals one over n, times the sum from i equals 1 to n of x-sub-i.

**Example 2.2**: Calculating the Mean

For the sample 8, 3, 7, 6:
- Sum: 8 plus 3 plus 7 plus 6 equals 24
- Count: 4 observations
- Mean: 24 divided by 4 equals 6

**The Median (Midpoint)**

The median is the middle value when observations are ordered from smallest to largest. Half the data falls below the median, half above.

**Example (continued)**: Finding the Median

For the same sample 8, 3, 7, 6:
- First, order the values: 3, 6, 7, 8
- With 4 observations (even number), the median is the average of the two middle values
- Median: 6 plus 7, divided by 2, equals 6.5

**Other Measures (Less Common)**

- **Mid-range**: average of the smallest and largest values
- **Mode**: most frequently occurring value (rarely useful for continuous economic data)

In econometrics, we most often use the mean. But as we'll see, the median is crucial when data are skewed!

**Why This Matters**: The choice between mean and median has real consequences. Suppose you're reporting "average" income in a neighborhood. If one billionaire moves in, the mean skyrockets while the median barely changes. For policy discussions about typical workers' earnings, the median often tells a more honest story than the mean. This is why economists report both!

> **Key Concept**: The mean is sensitive to outliers, while the median is robust. For skewed distributions, always report both measures to give a complete picture of central tendency. When someone says "average," always ask: do they mean the mean or the median? The difference matters!


Now that we understand central tendency, let's tackle variability. How spread out are the data? Do most observations cluster tightly around the mean, or are they scattered widely?

### 2.1.3 Standard Deviation and Variance

**Sample Variance: Measuring Spread**

Variance measures how much observations deviate from the mean. Here's the intuition:
- Take each observation and subtract the mean (this is the deviation)
- Square each deviation (to make everything positive—otherwise negatives and positives cancel)
- Average these squared deviations

Formula: s-squared equals one over n minus 1, times the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared.

**Why "n minus 1" instead of "n"?** This divisor is called degrees of freedom. We use n minus 1 because we already used the data once to calculate the mean. This adjustment ensures our variance estimate is unbiased. Think of it as a penalty for estimating rather than knowing the true population mean.

**Example 2.3**: Calculating Variance and Standard Deviation

Let's work with the sample: 8, 3, 7, 6 (recall x-bar equals 6).

Step 1: Calculate each squared deviation
- 8 minus 6, squared, equals 4
- 3 minus 6, squared, equals 9
- 7 minus 6, squared, equals 1
- 6 minus 6, squared, equals 0

Step 2: Sum them: 4 plus 9 plus 1 plus 0 equals 14

Step 3: Divide by n minus 1: s-squared equals 14 divided by 3, which equals 4.66

**Sample Standard Deviation**

The problem with variance? It's in squared units (dollars-squared, years-squared—hard to interpret!). Solution: take the square root to get back to the original units.

Standard deviation: s equals the square root of s-squared.

For our example: s equals the square root of 4.66, which equals 2.16.

This means observations typically deviate from the mean by about 2.16 units.


### 2.1.4 Interpreting Standard Deviation

Standard deviation is abstract—what does "2.16 units of deviation" actually mean? Here's a practical guide.

**The Empirical Rule (for Normal Distributions)**

If your data follows a bell-shaped (normal) distribution, you can rely on this pattern:
- **68% of observations** fall within 1 standard deviation of the mean
- **95% of observations** fall within 2 standard deviations of the mean
- **99.7% of observations** fall within 3 standard deviations of the mean

**For Any Distribution**

Even if your data aren't normal, you can still say: **at least 75% of observations fall within 2 standard deviations of the mean**. This is guaranteed mathematically by Chebyshev's inequality.

One St. Dev.
![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-08.jpg?height=298&width=373&top_left_y=516&top_left_x=57)

Two St. Devs.
![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-08.jpg?height=298&width=375&top_left_y=516&top_left_x=446)

Three St. Devs.
![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-08.jpg?height=298&width=375&top_left_y=516&top_left_x=839)

> **Key Concept**: Standard deviation measures the typical distance of observations from the mean. For normal distributions, approximately 68% of data falls within 1 standard deviation, 95% within 2 standard deviations, and 99.7% within 3 standard deviations. This is known as the empirical rule.


### 2.1.5 Other Measures of Dispersion

While standard deviation is the workhorse, other dispersion measures serve specialized purposes.

**Coefficient of Variation (CV)**

Formula: CV equals s divided by x-bar.

This measures dispersion relative to the mean. Why is this useful? Because raw standard deviation can be misleading when comparing datasets with different scales.

**Example:** Comparing variability of incomes across countries. A standard deviation of 10,000 dollars is large if mean income is 20,000 dollars (CV equals 0.5), but small if mean income is 200,000 dollars (CV equals 0.05).

**Interquartile Range (IQR)**

The difference between the upper quartile (75th percentile) and lower quartile (25th percentile). This captures the range of the middle 50% of the data and is robust to outliers.

**Mean Absolute Deviation (MAD)**

Formula: one over n, times the sum from i equals 1 to n of the absolute value of x-sub-i minus x-bar.

This averages the absolute deviations from the mean (without squaring). It's more intuitive than variance but mathematically less convenient for statistical theory.


### 2.1.6 Quartiles, Deciles and Percentiles

These provide summaries of ordered data (in addition to the median):

- **Quartiles** split ordered data into fourths
  - Lower quartile: one-quarter of the data is below and three-quarters above
  - Upper quartile: three-quarters of the data is below and one-quarter above

- **Deciles** split ordered data into tenths
  - The ninth decile has nine-tenths of the data below and one-tenth above

- **Percentiles** split ordered data into hundredths
  - The 99th percentile has 99% of the data below and 1% above


### 2.1.7 Skewness

**Symmetry vs. Skewness**

A symmetric distribution looks the same on both sides of the mean—like folding a piece of paper, the two halves match perfectly. The normal distribution (bell curve) and t-distribution are symmetric.

But many economic variables aren't symmetric. They're **skewed**—lopsided with a long tail on one side.
![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-11.jpg?height=353&width=369&top_left_y=482&top_left_x=60)
![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-11.jpg?height=362&width=371&top_left_y=480&top_left_x=450)
![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-11.jpg?height=356&width=369&top_left_y=482&top_left_x=841)

**Measuring Skewness**

The skewness statistic is approximately: one over n, times the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, divided by s, all raised to the third power.

This averages the cubed z-scores (standardized values). Why cube? Because:
- Positive deviations cubed stay positive
- Negative deviations cubed stay negative
- Larger deviations get amplified

**Interpreting Skewness Values:**
- **Zero**: Symmetric distribution
- **Positive**: Right-skewed (long tail to the right)—common for prices, income, wealth
- **Negative**: Left-skewed (long tail to the left)—less common in economics

**Key Signal:** When data are skewed, the mean does NOT equal the median. The mean gets pulled toward the tail. For strongly right-skewed data (like the earnings example earlier), the mean exceeds the median.

**Quick Check**: Looking back at Example 2.1, the earnings data had skewness of 1.71 (positive). How does this align with the mean (41,413 dollars) and median (36,000 dollars)? [Pause] Exactly right—the mean exceeds the median, confirming right-skewness. A few very high earners pull the mean upward.

> **Key Concept**: Right-skewed data (positive skewness) dominates economics: earnings, prices, wealth. For highly skewed data, the median often represents the "typical" value better than the mean. Alternatively, applying a log transformation can convert skewed data into a more symmetric distribution, making standard statistical methods more appropriate.


### 2.1.8 Kurtosis

Kurtosis measures the "tailedness" of a distribution—how much probability mass sits in the extreme tails compared to a normal distribution.

**The Kurtosis Formula:**

Kurtosis approximately equals: one over n, times the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, divided by s, all raised to the fourth power.

This averages the z-scores raised to the fourth power. Why the fourth power? Because it amplifies extreme values even more than squaring or cubing. Observations far from the mean dominate this statistic.

**Excess Kurtosis**

The normal distribution has kurtosis of exactly 3. We usually report **excess kurtosis**, which subtracts this benchmark:

Excess kurtosis equals Kurtosis minus 3.

**Interpretation:**
- **Excess kurtosis = 0**: Tails like a normal distribution
- **Excess kurtosis > 0**: Fatter tails—more extreme values than expected under normality
- **Excess kurtosis < 0**: Thinner tails—fewer extreme values

**Why This Matters**: Fat tails are pervasive in finance and economics. Stock returns, for instance, have far more extreme crashes and rallies than a normal distribution predicts. Ignoring this can lead to catastrophic risk management failures—as the 2008 financial crisis demonstrated. Models assuming normality severely underestimate the probability of rare but devastating events.


### 2.1.9 Box Plot

A **box and whisker plot** (or simply **box plot**) packs multiple summary statistics into a single compact graphic. It's brilliant for spotting distribution shape and outliers at a glance.

**Anatomy of a Box Plot:**

- **Middle line in the box**: Median (50th percentile)
- **Box edges**: Lower quartile (25th percentile) and upper quartile (75th percentile)
- **Box height**: Interquartile range (IQR)—the middle 50% of the data
- **Whiskers (outer bars)**: Convention varies by software package:
  - **Option 1**: Extend to the minimum and maximum values
  - **Option 2 (more common)**: Extend to 1.5 times the IQR beyond the quartiles
    - Upper whisker: Upper quartile plus 1.5 times IQR
    - Lower whisker: Lower quartile minus 1.5 times IQR
    - **Dots beyond whiskers**: Flag potential outliers

![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-15.jpg?height=587&width=770&top_left_y=189&top_left_x=245)

> **Key Concept**: Summary statistics efficiently describe large datasets using measures of central tendency (mean, median) and dispersion (standard deviation, quartiles). For skewed data, the median is often more representative than the mean, and box plots provide a visual summary of key statistics including potential outliers.


We've summarized data with numbers (mean, median, standard deviation). But sometimes a picture truly is worth a thousand words. Let's explore how to visualize distributions.

## 2.2 Charts for Numerical Data

For cross-sectional data (observations at a single point in time), the **histogram** and **smoothed histogram** are your primary tools.

**Running Example:** We'll continue with our earnings data—171 full-time working women aged 30 in 2010. "Full-time" means at least 35 hours per week for at least 48 weeks per year.

A peek at the raw data shows variation: the first nine observations are 25,000, 40,000, 25,000, 38,000, 28,800, 31,000, 25,000, 20,000, and 83,000 dollars. The full dataset ranges from 1,050 dollars to 172,000 dollars.

Notice that earnings are typically rounded to nice numbers—nearest hundred, thousand, or ten thousand dollars. This is common with self-reported data.


### 2.2.1 Frequency Distribution (Tabulation in Ranges)

Looking at a summary of the data grouped into intervals of width 15,000 dollars: For example, 53 observations or 31% have earnings between 15,000 and 29,999 dollars. Breaking down the full distribution: 12 observations (7.0%) fall in the 0 to 14,999 range, 53 observations (31.0%) in the 15,000 to 29,999 range, 52 observations (30.4%) in the 30,000 to 44,999 range, 20 observations (11.7%) in the 45,000 to 59,999 range, 11 observations (6.4%) in the 60,000 to 74,999 range, 16 observations (9.4%) in the 75,000 to 89,999 range, 2 observations (1.2%) in the 90,000 to 104,999 range, 3 observations (1.8%) in the 105,000 to 119,999 range, 0 observations in the 120,000 to 134,999 range, 1 observation (0.6%) in the 135,000 to 149,999 range, 0 observations in the 150,000 to 164,999 range, and 1 observation (0.6%) in the 165,000 to 180,000 range.

### 2.2.2 Histogram

A histogram visualizes the frequency distribution. Here's how it works:

**Key Concepts:**
- **Bin**: An interval grouping similar values (e.g., 15,000 to 29,999 dollars)
- **Bin width**: The size of each interval (here: 15,000 dollars)
- **Number of bins**: How many intervals we create (here: 13 bins, approximately the square root of 171—a common rule of thumb)
- **Frequency**: Count of observations falling in each bin
- **Relative frequency**: Proportion or percentage in each bin

**The Histogram Graph:**
- **Horizontal axis**: Values or ranges of values
- **Vertical axis**: Frequency, relative frequency, or density (relative frequency divided by bin width)
- **Each bar**: Represents one bin, with height showing how many observations fall in that range


### 2.2.3 Choosing Bin Width

- Smaller bin width gives more detail
- Here we compare 15,000 dollar to 7,500 dollar bin width.
![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-19.jpg?height=352&width=556&top_left_y=389&top_left_x=77)
![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-19.jpg?height=353&width=570&top_left_y=388&top_left_x=641)


### 2.2.4 Kernel Density Estimates (Smoothed Histogram)

Continuous data like earnings have an underlying smooth density function—think of the bell-shaped normal distribution. Probabilities correspond to areas under the curve, and the total area under any density curve equals one (we'll explore this more in Chapter 5).

**What is a Kernel Density Estimate?**

A kernel density estimate smooths the histogram into a continuous curve. It accomplishes this through two techniques:

1. **Overlapping windows**: Instead of distinct bins, it uses rolling windows that overlap
2. **Weighted counting**: Observations near the window center get more weight than those at the edges

**Why Use This?** It produces a smooth estimate of the underlying distribution. We can then compare this estimate to theoretical densities (like the normal distribution) to see how well they match our data.


### 2.2.5 Choosing Window Width

- Larger window width or bin width leads to a smoother estimate.
![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-21.jpg?height=448&width=632&top_left_y=343&top_left_x=62)
![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-21.jpg?height=441&width=456&top_left_y=343&top_left_x=778)

> **Key Concept**: Kernel density estimates provide smooth approximations of the underlying distribution. Larger window widths create smoother estimates but may hide important features, while smaller windows preserve detail but may show more noise.


### 2.2.6 Line Charts for Time Series

- A standard chart for time series data is a line chart.
- A line chart plots the successive values of the data against the successive index values.
- This is useful for numerical data where interest lies in how the data change from one observation to the next.
- The leading application is to time series data, which has a natural ordering of the observations, namely time.
- The next slide shows a line chart for real gross domestic product (GDP) per capita in constant 2012 dollars from 1959 to 2019
- It indicates enormous improvement in living standards—per capita real GDP tripled over the sixty years
- It also shows dips due to recessions

![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-23.jpg?height=593&width=772&top_left_y=188&top_left_x=252)

> **Key Concept**: Histograms visualize distributions using bins whose width determines the level of detail. Kernel density estimates provide smooth approximations of the underlying distribution, while line charts are ideal for time series data to show trends and patterns over time.


So far we've visualized continuous numerical data (earnings spanning many values). But what about categorical data—values that fall into discrete groups? Let's explore appropriate visualizations for this different data type.

## 2.3 Charts for Numerical Data by Category

**Example:** U.S. health expenditures in 2018 totaled 3,653 billion dollars (18% of GDP). How was this distributed across spending categories?

Breaking it down:
- **Hospital Care**: 1,192 billion dollars (largest category)
- **Physician and Clinical Services**: 726 billion
- **Drugs and Supplies (Retail)**: 456 billion
- **Net Cost of Health Insurance**: 259 billion
- **Nursing Care**: 169 billion
- **Other categories** (Dental, Home Health, Government, Research, Equipment, etc.): Combined 851 billion

Each category represents a distinct type of expenditure. How do we visualize this clearly?

### 2.3.1 Bar Charts and Column Charts

- Bar charts are a standard chart for numerical categorical data.
- A bar chart provides a bar for each category, where the length of the bar is determined by the category's value.
- A column chart or vertical bar chart has values on the vertical axis and category on the horizontal axis.
- A horizontal bar chart has values on the horizontal axis and category on the vertical axis.

![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-26.jpg?height=556&width=760&top_left_y=206&top_left_x=251)

### 2.3.2 Spatial Maps

- We can plot data by geographic location against a geographic map.
- An example is average family size in each U.S. state in 2010, where darker shades correspond to larger families.

Average family size 2010
![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-27.jpg?height=453&width=1033&top_left_y=411&top_left_x=115)

> **Key Concept**: Bar charts and column charts effectively display categorical data by using bar length to represent values. Spatial maps add a geographic dimension, making patterns across regions immediately visible through color or shading intensity.


## 2.4 Summary and Charts for Categorical Data

- Example: Fishing site chosen by a sample of 1,182 fishers where there are four possible sites (categories).
- We summarize using a tabulation of frequencies.

Looking at the fishing site data: 134 fishers (11.34%) chose the Beach, 178 fishers (15.06%) chose the Pier, 418 fishers (35.36%) chose Private Boat, and 452 fishers (38.24%) chose Charter Boat. This shows that boat-based fishing, whether private or charter, is much more popular than shore-based fishing from beach or pier.

### 2.4.1 Pie Charts

- A pie chart splits a circle into slices where the area of each slice corresponds to the relative frequency of observations in each category.
- A pie chart with many categories can be made easier by: giving the slices in order of decreasing size, giving the associated headings in the same ordering in a separate legend, and using color rather than black-and-white.

![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-30.jpg?height=541&width=704&top_left_y=221&top_left_x=277)

> **Key Concept**: Categorical data is summarized using frequency tables showing counts and percentages. Pie charts display proportions visually, with slice area corresponding to relative frequency. However, bar charts are often preferred over pie charts for easier comparison of categories.


Sometimes raw data aren't in the best form for analysis. Transformation can reveal patterns, satisfy statistical assumptions, or enable meaningful comparisons. Let's explore the most important transformations in econometrics.

## 2.5 Data Transformations

### 2.5.1 Natural Logarithm Transformation

Remember our right-skewed earnings data? The mean (41,413 dollars) exceeded the median (36,000 dollars) because a few very high earners pulled the distribution rightward. Right-skewness is everywhere in economics: prices, income, wealth, firm size.

**The Solution:** Take the natural logarithm of the data. This compression transforms right-skewed distributions into approximately symmetric ones.
![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-31.jpg?height=348&width=544&top_left_y=372&top_left_x=91)
![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-31.jpg?height=349&width=537&top_left_y=372&top_left_x=651)

The left panel shows the original right-skewed earnings distribution. The right panel shows the log-transformed data—much more symmetric! We'll explore logarithms extensively in Chapter 9, including their powerful interpretation as percentage changes.


### 2.5.2 Standardized Scores (Z-Scores)

Imagine you want to compare a student's performance on two different tests: a math test (mean 70, standard deviation 10) and an English test (mean 85, standard deviation 15). The student scored 80 in math and 100 in English. Which performance was better relative to their peers?

Raw scores don't tell us—they're on different scales. Solution: **standardize** them!

**The Z-Score Formula:**

For each observation: z-sub-i equals x-sub-i minus x-bar, divided by s.

This subtracts the mean and divides by the standard deviation. The resulting z-scores have mean zero and standard deviation one across all observations.

**Interpretation:**
- **z = 0**: Exactly at the mean
- **z = 1**: One standard deviation above the mean
- **z = -2**: Two standard deviations below the mean

**Back to our example:**
- Math: z equals 80 minus 70, divided by 10, equals 1 (one SD above mean)
- English: z equals 100 minus 85, divided by 15, equals 1 (one SD above mean)

They're equally impressive! Z-scores put everything on a common scale.

**Why This Matters**: Z-scores enable apples-to-apples comparison when variables have different units or scales. In Chapter 3, we'll see that standardizing is also crucial for statistical inference—many test statistics are standardized versions of estimators. This transformation lets us use standard normal distribution tables regardless of the original data scale.

> **Key Concept**: Natural logarithm transformations convert right-skewed economic data (earnings, prices, wealth) to more symmetric distributions, facilitating analysis and satisfying normality assumptions. Z-scores standardize data to have mean 0 and standard deviation 1, enabling comparison across different scales—essential when comparing variables measured in different units or when conducting hypothesis tests.


The transformations we've discussed (logarithms and z-scores) work for any data type. But time series data—observations ordered chronologically—have unique patterns requiring specialized transformations. Let's explore these.

## 2.6 Data Transformations for Time Series

### 2.6.1 Moving Averages and Seasonal Adjustment

Economic time series often contain two types of variation we want to remove: short-term noise and predictable seasonal patterns.

**Moving Averages**

Smooth data by averaging over several consecutive time periods. This filters out high-frequency fluctuations, revealing the underlying trend.

**Seasonal Adjustment**

Remove recurring seasonal patterns (e.g., retail sales surge every December). Seasonal adjustment lets us see whether changes reflect genuine economic shifts or just the calendar.
![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-33.jpg?height=355&width=562&top_left_y=414&top_left_x=66)
![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-33.jpg?height=358&width=558&top_left_y=411&top_left_x=635)


### 2.6.2 Real and Per Capita Adjustments

Raw economic data can be misleading over time. Two critical adjustments:

**Real vs. Nominal (Inflation Adjustment)**

Nominal values are in current dollars. Real values adjust for price changes (inflation) using a price index. Comparing nominal GDP across decades is meaningless—you must use real GDP to see actual economic growth.

**Per Capita (Population Adjustment)**

Total values can grow simply because population grows. Per capita values (per person) reveal whether the average individual is better off. Real GDP might double, but if population also doubled, real GDP per capita stayed constant!
![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-34.jpg?height=438&width=551&top_left_y=353&top_left_x=74)
![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-34.jpg?height=446&width=549&top_left_y=348&top_left_x=639)


### 2.6.3 Growth Rates and Percentage Changes

**The Formula**

The one-period percentage change in x-sub-t equals: 100 times the quantity x-sub-t minus x-sub-t-minus-1, divided by x-sub-t-minus-1.

For quarterly data, we often annualize by multiplying by four to express growth at an annual rate.

**Critical Distinction: Percentage Points vs. Percentage Change**

Suppose the unemployment rate rises from 3% to 5%.

- **Correct**: The rate increased by **2 percentage points**
- **Incorrect**: There is a "2% increase" (which would mean 3% times 1.02 equals 3.06%)

Don't confuse additive changes (percentage points) with multiplicative changes (percentage changes)!

**Basis Points**

Very small changes use basis points: one basis point equals one-hundredth of a percentage point. So an interest rate increase from 3.00% to 3.25% is a 25 basis point increase.

**Logarithmic Approximation**

A powerful result (we'll prove this in Chapter 9): the percentage change in x approximately equals 100 times the change in ln(x).

That is: 100 times the quantity x-sub-t minus x-sub-t-minus-1, divided by x-sub-t-minus-1, approximately equals 100 times the quantity ln x-sub-t minus ln x-sub-t-minus-1.

This is why logarithms are so useful in econometrics—log differences give you growth rates directly!

> **Key Concept**: Time series data often requires transformations: moving averages smooth short-term fluctuations, seasonal adjustment removes recurring patterns, real values adjust for inflation, per capita values adjust for population, and growth rates measure proportionate changes. These transformations reveal underlying trends and enable meaningful comparisons over time.


## 2.8 Practice Exercises

(1) Obtain the sum from i equals 1 to 3 of the quantity 2 plus 3 times i-squared.
(2) Obtain the mean, variance and standard deviation for a sample with values 5, 2, 2.
(3) For a sample of size 500 from the normal distribution, approximately how many observations do you expect to be within two standard deviations of the mean?
(4) For a sample with mean 3 and variance 4, find the z-score for an observation with value 6.
(5) If x increases from 4 to 5, what is the percentage change in x?

---

## Key Takeaways

**Summary Statistics and Data Distributions:**
- Summary statistics (mean, median, standard deviation, quartiles) efficiently describe large datasets by quantifying central tendency and dispersion
- The mean is sensitive to outliers; the median is robust and preferred for skewed distributions
- Standard deviation measures typical distance from the mean; for normal distributions, 68% of data falls within 1 standard deviation, 95% within 2
- Skewness measures asymmetry (positive for right-skewed data common in economics like earnings and wealth)
- Kurtosis measures tail heaviness; excess kurtosis indicates fatter tails than the normal distribution
- Box plots visually summarize key statistics: median, quartiles, and potential outliers

**Visualizations for Different Data Types:**
- Histograms display distributions of numerical data using bins; bin width affects detail level (smaller bins show more detail but may be noisier)
- Kernel density estimates provide smooth approximations of underlying continuous distributions
- Line charts are ideal for time series data to reveal trends and patterns over time
- Bar charts and column charts effectively display categorical data, with bar length representing values
- Pie charts show proportions for categorical data, though bar charts often facilitate easier comparison
- Spatial maps add a geographic dimension, making regional patterns immediately visible

**Data Transformations and Their Applications:**
- Natural logarithm transformations convert right-skewed economic data (earnings, prices, wealth) to more symmetric distributions
- Z-scores standardize data to mean 0 and standard deviation 1, enabling comparison across different scales
- Moving averages smooth short-term fluctuations in time series data
- Seasonal adjustment removes recurring patterns to reveal underlying trends
- Real values adjust for price inflation; per capita values adjust for population size
- Growth rates measure proportionate changes; distinguish between percentage point changes and percentage changes
- For time series, the change in natural log approximates the proportionate change (useful property for growth rate calculations)

---
