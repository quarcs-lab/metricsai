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

## 2.1 Summary Statistics for Numerical Data

**In this section:**
- 2.1.1 Summary statistics example
- 2.1.2 Measures of central tendency (mean, median)
- 2.1.3 Standard deviation and variance
- 2.1.4 Interpreting standard deviation
- 2.1.5 Other dispersion measures (CV, IQR, MAD)
- 2.1.6 Quartiles, deciles, and percentiles
- 2.1.7 Skewness
- 2.1.8 Kurtosis
- 2.1.9 Box plots

- Observations for a sample of size $n$ are denoted:

$$
x_{1}, x_{2}, \ldots, x_{n}
$$

- **Notation:**
  - $x_{1}$ is the first observation, $\ldots, x_{n}$ is the $n^{\text{th}}$ observation
  - Cross-section data: typical observation is the $i^{\text{th}}$, denoted $x_{i}$
  - Time series data: more customary to use the subscript $t$

- **Example: Sample mean or average**

$$
\bar{x}=\frac{x_{1}+x_{2}+\ldots+x_{n}}{n}=\frac{1}{n} \sum_{i=1}^{n} x_{i}
$$

### 2.1.1 Summary Statistics Example: Earnings

**Example 2.1**: Earnings of Full-Time Working Women

Summary statistics, rounded to the nearest dollar, for the earnings data on full-time working women aged 30 in 2010:

| Statistic | Value |
| :--- | ---: |
| Mean | 41,413 |
| Standard deviation | 25,527 |
| Minimum | 1,050 |
| Maximum | 172,000 |
| Number of Observations | 171 |
| Variance | $651,630,282$ |
| Upper quartile (75th percentile) | 50,000 |
| Median (50th percentile) | 36,000 |
| Lower quartile | 25,000 |
| Skewness | 1.71 |
| Kurtosis | 7.32 |

### 2.1.2 Measures of Central Tendency

- **Mean**: the average

$$
\bar{x}=\left(x_{1}+x_{2}+\ldots+x_{n}\right) / n=\frac{1}{n} \sum_{i=1}^{n} x_{i}
$$

**Example 2.2**: Calculating the Mean
- Sample $\{8,3,7,6\}$ then $\bar{x}=(8+3+7+6) / 4=6$

- **Median**: mid-point of the ordered observations
  - e.g., Sample $\{8,3,7,6\}$ when ordered is $\{3,6,7,8\}$
  - Median is average of the middle two values $=(6+7) / 2=6.5$

- **Other measures:**
  - Mid-range: average of the smallest and largest values
  - Mode: most common value (not useful for continuous data)

- Most often the mean is used

> **Key Concept**: The mean is sensitive to outliers, while the median is robust. For skewed distributions, always report both measures.


### 2.1.3 Standard Deviation and Variance

- **Sample variance:**

$$
s^{2}=\frac{\left[\left(x_{1}-\bar{x}\right)^{2}+\ldots+\left(x_{n}-\bar{x}\right)^{2}\right]}{(n-1)}=\frac{1}{n-1} \sum_{i=1}^{n}\left(x_{i}-\bar{x}\right)^{2}
$$

- The divisor $(n-1)$ is called the degrees of freedom
  - Only $(n-1)$ terms in the sum can vary since the $x_{i}$ are linked by $\bar{x}=\frac{1}{n} \sum_{i=1}^{n} x_{i}$

**Example 2.3**: Calculating Variance and Standard Deviation
- Sample $\{8,3,7,6\}$ has $n=4$ and $\bar{x}=6$
- $s^{2}=\frac{1}{3}\left[(8-6)^{2}+(3-6)^{2}+(7-6)^{2}+(6-6)^{2}\right]=14 / 3=4.66$

- **Sample standard deviation:** $s=\sqrt{s^{2}}$
  - Take square root to get back to same units as $x$
  - Sample $\{8,3,7,6\}$ has $s=\sqrt{s^{2}}=\sqrt{4.66}=2.16$


### 2.1.4 Interpreting Standard Deviation

- Standard deviation is difficult to understand physically
- As a guide, use the fact that if data are normally distributed then 68%, 95%, 99.7% are within 1, 2 and 3 standard deviations of the mean
- For any distribution, at least 75% are within 2 standard deviations of the mean

One St. Dev.
![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-08.jpg?height=298&width=373&top_left_y=516&top_left_x=57)

Two St. Devs.
![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-08.jpg?height=298&width=375&top_left_y=516&top_left_x=446)

Three St. Devs.
![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-08.jpg?height=298&width=375&top_left_y=516&top_left_x=839)

> **Key Concept**: Standard deviation measures the typical distance of observations from the mean. For normal distributions, approximately 68% of data falls within 1 standard deviation, 95% within 2 standard deviations.


### 2.1.5 Other Measures of Dispersion

- We most often use the standard deviation

- **Coefficient of variation:** $\mathrm{CV}=s / \bar{x}$
  - Dispersion relative to the mean

- **Interquartile range**
  - Difference between upper and lower quartiles

- **Mean absolute deviation:** $\frac{1}{n} \sum_{i=1}^{n}\left|x_{i}-\bar{x}\right|$
  - Average absolute deviation about the mean


### 2.1.6 Quartiles, Deciles and Percentiles

These provide summaries of ordered data (in addition to the median):

- **Quartiles** split ordered data into fourths
  - Lower quartile: one-quarter below and three-quarters above
  - Upper quartile: three-quarters below and one-quarter above

- **Deciles** split ordered data into tenths
  - Ninth decile: nine-tenths below and one-tenth above

- **Percentiles** split ordered data into hundredths
  - 99th percentile: 99% below and 1% above


### 2.1.7 Skewness

- **Symmetry**
  - The density is the same when reflected about the mean
  - Normal and t distributions are examples

- **Skewness**: not symmetric
![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-11.jpg?height=353&width=369&top_left_y=482&top_left_x=60)
![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-11.jpg?height=362&width=371&top_left_y=480&top_left_x=450)
![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-11.jpg?height=356&width=369&top_left_y=482&top_left_x=841)
- Skewness statistic: Approximately

$$
\text { Skew } \simeq \frac{1}{n} \sum_{i=1}^{n}\left(\frac{x_{i}-\bar{x}}{s}\right)^{3} .
$$

- The average of the z-score $\left(\frac{x_{i}-\bar{x}}{s}\right)$ raised to third power
  - Where z-score is standardized to have mean 0 and variance 1

- Zero if no skewness
- Positive if right-skewed (e.g., prices, income) and negative if left-skewed
- With skewed data mean $\neq$ median
- For very skewed data may wish to use the median in addition to, or in place of, the mean

> **Key Concept**: Right-skewed data (positive skewness) is common in economics: earnings, prices, wealth. For highly skewed data, consider using the median or applying a log transformation.


### 2.1.8 Kurtosis

- Kurtosis statistic: Approximately

$$
\text { Kurt } \simeq \frac{1}{n} \sum_{i=1}^{n}\left(\frac{x_{i}-\bar{x}}{s}\right)^{4}
$$

- the average of the z -score $\left(\frac{x_{i}-\bar{x}}{s}\right)$ raised to fourth power.
- Excess kurtosis measures kurtosis relative to the normal distribution which has Kurt $=3$

$$
\text { ExcessKurt }=\text { Kurt }-3 .
$$

- View positive excess kurtosis as fatter tails than normal.
- Since measure involves $\left(x_{i}-\bar{x}\right)^{4}$ outliers get a lot of weight
- financial returns data often have fat tails.


### 2.1.9 Box Plot

- A box and whisker plot or, more simply, a box plot
- provides in a simple graphic some of the key summary statistics.
- Median is the middle line.
- Upper and lower quartiles are the lines surrounding the median.
- Outer bars vary with the statistical package
  - Sometimes the minimum and maximum
  - Sometimes the following is used to indicate outliers:
    - Upper bar is upper quartile plus 1.5 times the inter-quartile range
    - Lower bar is lower quartile minus 1.5 times the inter-quartile range
    - Dots are observations outside these bars

![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-15.jpg?height=587&width=770&top_left_y=189&top_left_x=245)

> **Key Concept**: Summary statistics efficiently describe large datasets using measures of central tendency (mean, median) and dispersion (standard deviation, quartiles). For skewed data, the median is often more representative than the mean, and box plots provide a visual summary of key statistics.


## 2.2 Charts for Numerical Data

- Standard charts for cross-section data are histogram and smoothed histogram.
- Example: Annual earnings of a sample of 171 female full-time workers aged 30 years in 2010
- full-time is 35 or more hours per week and 48 or more weeks per year.
- The first nine observations are
- $25000,40000,25000,38000,28800,31000,25000,20000,83000$.
- Earnings range from $\$ 1,050$ to $\$ 172,000$.
- Earnings are generally reported to the nearest hundred or thousand or ten thousand dollars.


### 2.2.1 Frequency Distribution (Tabulation in Ranges)

- Summary of data grouped into intervals of width $\$ 15,000$
- e.g. 53 observations or $31 \%$ have earnings between $\$ 15,000$ and \$29,999.

| Range (or bin) | Frequency | Relative frequency (\%) |
| :--- | :--- | :--- |
| 0-14,999 | 12 | 7.0 |
| 15,000-29,999 | 53 | 31.0 |
| 30,000-44,999 | 52 | 30.4 |
| 45,000-59,999 | 20 | 11.7 |
| 60,000-74,999 | 11 | 6.4 |
| 75,000-89,999 | 16 | 9.4 |
| 90,000-104,999 | 2 | 1.2 |
| 105,000-119,999 | 3 | 1.8 |
| 120,000-134,999 | 0 | 0.0 |
| 135,000-149,999 | 1 | 0.6 |
| 150,000-164,999 | 0 | 0.0 |
| 165,000-180,000 | 1 | 0.6 |

### 2.2.2 Histogram

- The preceding table summarizes the data grouped into intervals of width \$15,000
- each interval is called a bin; here there are 13 bins $\simeq \sqrt{171}$.
- each bin is of equal bin width of $\$ 15,000$.
- frequency is the number of observations that fall into a given bin
- relative frequency is the proportion (or percentage) that fall into a given bin
- A histogram is a graph of the frequency distribution
- horizontal axis: values or range of values
- vertical axis: frequency or relative frequency or density (the relative frequency divided by the bin width)


### 2.2.3 Choosing Bin Width

- Smaller bin width gives more detail
- Here we compare $\$ 15,000$ to $\$ 7,500$ bin width.
![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-19.jpg?height=352&width=556&top_left_y=389&top_left_x=77)
![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-19.jpg?height=353&width=570&top_left_y=388&top_left_x=641)


### 2.2.4 Kernel Density Estimates (Smoothed Histogram)

- Continuous data such as earnings data have an underlying continuous density
  - e.g., the normal distribution (a bell-shaped density)
  - Probabilities are determined by areas under the curve
  - Total area under a density is one; see Appendix 5.A

- A kernel density estimate is a commonly-used estimate of a density
- It is a smoothed histogram that smooths in two ways:
  - Uses rolling bins (or windows) that overlap rather than being distinct
  - Count the fraction of the sample within each bin with more weight given to observations at the window center and less to observations at the window ends
- Can compare kernel density estimate to a proposed continuous density for the data such as normal


### 2.2.5 Choosing Window Width

- Larger window width or bin width leads to smoother estimate.
![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-21.jpg?height=448&width=632&top_left_y=343&top_left_x=62)
![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-21.jpg?height=441&width=456&top_left_y=343&top_left_x=778)

> **Key Concept**: Kernel density estimates provide smooth approximations of the underlying distribution. Larger window widths create smoother estimates but may hide important features.


### 2.2.6 Line Charts for Time Series

- A standard chart for time series data is a line chart.
- A line chart plots the successive values of the data against the successive index values.
- Useful for numerical data where interest lies in how the data change from one observation to the next.
- Leading application is to time series data
- these have a natural ordering of the observations, namely time.
- Next slide shows line chart for real gross domestic product (GDP) per capita in constant 2012 dollars from 1959 to 2019
- Indicates enormous improvement in living standards
  - Per capita real GDP tripled over the sixty years
- Also shows dips due to recessions

![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-23.jpg?height=593&width=772&top_left_y=188&top_left_x=252)

> **Key Concept**: Histograms visualize distributions using bins whose width determines the level of detail. Kernel density estimates provide smooth approximations of the underlying distribution, while line charts are ideal for time series data to show trends and patterns over time.


## 2.3 Charts for Numerical Data by Category

- U.S. health expenditures in 2018 of \$3,653 billion (18\% of GDP)
- broken into its main subcomponents.

| Category | Amount (\$ billions) |
| :--- | :--- |
| Hospital Care | 1192 |
| Physician and Clinical Services | 726 |
| Dental | 136 |
| Other Professional | 104 |
| Other Health and Personal | 192 |
| Home Health Care | 102 |
| Nursing Care | 169 |
| Drugs and Supplies (Retail Sales) | 456 |
| Government Administration | 48 |
| Net Cost of Health Insurance | 259 |
| Government Public Health | 94 |
| Noncommercial Research | 53 |
| Structures and Equipment | 122 |

### 2.3.1 Bar Charts and Column Charts

- Bar charts are a standard chart for numerical categorical data.
- A bar chart
- provides a bar for each category
- the length of the bar is determined by the category's value.
- A column chart or vertical bar chart
- values on the vertical axis
- category on the horizontal axis.
- A horizontal bar chart
- values on the horizontal axis
- category on the vertical axis.

![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-26.jpg?height=556&width=760&top_left_y=206&top_left_x=251)

### 2.3.2 Spatial Maps

- Plot data by geographic location against a geographic map.
- Example is average family size in each U.S. state in 2010
- darker shades correspond to larger families.

Average family size 2010
![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-27.jpg?height=453&width=1033&top_left_y=411&top_left_x=115)

> **Key Concept**: Bar charts and column charts effectively display categorical data by using bar length to represent values. Spatial maps add a geographic dimension, making patterns across regions immediately visible.


## 2.4 Summary and Charts for Categorical Data

- Example: Fishing site chosen by a sample of 1,182 fishers
- there are four possible sites (categories).
- Summarize using a Tabulation of frequencies.

| Category | Frequency | Relative frequency (\%) |
| :--- | :---: | :---: |
| Beach | 134 | 11.34 |
| Pier | 178 | 15.06 |
| Private Boat | 418 | 35.36 |
| Charter Boat | 452 | 38.24 |

### 2.4.1 Pie Charts

- A pie chart splits a circle into slices
- the area of each slice corresponds to the relative frequency of observations in each category.
- A pie chart with many categories can be made easier by
- giving the slices in order of decreasing size
- giving the associated headings, in the same ordering, in a separate legend.
- using color rather than black-and-white.

![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-30.jpg?height=541&width=704&top_left_y=221&top_left_x=277)

> **Key Concept**: Categorical data is summarized using frequency tables showing counts and percentages. Pie charts display proportions visually, with slice area corresponding to relative frequency. Bar charts are often preferred over pie charts for easier comparison of categories.


## 2.5 Data Transformations

### 2.5.1 Natural Logarithm Transformation

- Many economic series are right-skewed: prices, income, wealth, ...
- Natural logarithm converts right-skewed data to a more symmetric distribution.
![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-31.jpg?height=348&width=544&top_left_y=372&top_left_x=91)
![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-31.jpg?height=349&width=537&top_left_y=372&top_left_x=651)
- Advantages of using natural logarithm are given in Chapter 9.


### 2.5.2 Standardized Scores (Z-Scores)

- Standardized scores (or z-scores)
- Consider sample with sample mean $\bar{x}$ and standard deviation $s$
- subtract the mean and divide by the sample standard deviation
- so

$$
z_{i}=\frac{x_{i}-\bar{x}}{s}, \quad i=1, \ldots, n
$$

- Then $z_{1}, \ldots, z_{n}$ has mean $\bar{z}=0$ and sample standard deviation one.
- Useful for comparing series that are scaled differently
- e.g. test scores on two different tests.
- If e.g. $z_{i}=-3$ then $x_{i}$ was 3 standard deviations below the mean.

> **Key Concept**: Natural logarithm transformations convert right-skewed economic data (earnings, prices, wealth) to more symmetric distributions, facilitating analysis. Z-scores standardize data to have mean 0 and standard deviation 1, enabling comparison across different scales.


## 2.6 Data Transformations for Time Series

### 2.6.1 Moving Averages and Seasonal Adjustment

- Moving averages: smooth by averaging over several successive periods.
- Seasonal adjustment: smooth by adjusting for seasonal variation.
![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-33.jpg?height=355&width=562&top_left_y=414&top_left_x=66)
![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-33.jpg?height=358&width=558&top_left_y=411&top_left_x=635)


### 2.6.2 Real and Per Capita Adjustments

- Real and nominal data: adjust for price inflation.
- Per capita data: adjust for population size.
![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-34.jpg?height=438&width=551&top_left_y=353&top_left_x=74)
![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-34.jpg?height=446&width=549&top_left_y=348&top_left_x=639)


### 2.6.3 Growth Rates and Percentage Changes

- The one-period percentage change in $x_{t}$ is $100 \times \frac{x_{t}-x_{t-1}}{x_{t-1}}$.
- This is often converted to an annualized rate
  - e.g., for quarterly data the quarterly change is multiplied by four.
- Distinguish between percentage point change and percentage change
  - Suppose the growth rate increases from 3 percent to 5 percent
  - Correct: the growth rate increased by two percentage points
  - Incorrect: there is a 2 percent increase in the growth rate (which means an increase from 3.0 percent to $3.0 \times 1.02=3.06$ percent)
- Very small changes are described in basis points
  - A basis point is one-hundredth of a percentage point
- An approximation (explained in Chapter 9.1) is
  - Proportionate change in $x=$ level change in natural log of $x$
  - So percentage change in $x_{t} \equiv 100 \times \frac{x_{t}-x_{t-1}}{x_{t-1}} \simeq 100 \times\left(\ln x_{t}-\ln x_{t-1}\right)$

> **Key Concept**: Time series data often requires transformations: moving averages smooth short-term fluctuations, seasonal adjustment removes recurring patterns, real values adjust for inflation, per capita values adjust for population, and growth rates measure proportionate changes. These transformations reveal underlying trends and enable meaningful comparisons.


## 2.8 Practice Exercises

(1) Obtain $\sum_{i=1}^{3}\left(2+3 i^{2}\right)$.
( ) Obtain the mean, variance and standard deviation for a sample with values $5,2,2$.
(1) For a sample of size 500 from the normal distribution, approximately how many observations do you expect to be within two standard deviations of the mean?
(1) For a sample with mean 3 and variance 4 find the z -score for an observation with value 6 .
(1) If $x$ increases from 4 to 5 what is the percentage change in $x$ ?

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

