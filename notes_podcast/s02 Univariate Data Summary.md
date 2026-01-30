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

- Observations for a sample of size n are denoted: x-sub-1, x-sub-2, and so on up to x-sub-n.

- **Notation:**
  - x-sub-1 is the first observation, and x-sub-n is the n-th observation
  - For cross-section data, the typical observation is the i-th, denoted x-sub-i
  - For time series data, it's more customary to use the subscript t

- **Example: Sample mean or average**

The sample mean, x-bar, equals the sum of x-sub-1 plus x-sub-2 plus dot-dot-dot plus x-sub-n, all divided by n. Using summation notation, this is one over n, times the sum from i equals 1 to n of x-sub-i.

### 2.1.1 Summary Statistics Example: Earnings

**Example 2.1**: Earnings of Full-Time Working Women

Looking at summary statistics, rounded to the nearest dollar, for earnings data on full-time working women aged 30 in 2010: The mean earnings are 41,413 dollars with a standard deviation of 25,527 dollars. Earnings range from a minimum of 1,050 dollars to a maximum of 172,000 dollars. The sample contains 171 observations. The variance is 651,630,282 dollars-squared. The upper quartile (75th percentile) is 50,000 dollars, the median (50th percentile) is 36,000 dollars, and the lower quartile is 25,000 dollars. The skewness measure is 1.71, indicating right-skewed data, and kurtosis is 7.32, suggesting fat tails.

### 2.1.2 Measures of Central Tendency

- **Mean**: the average

The mean, x-bar, equals the sum of x-sub-1 plus x-sub-2 plus dot-dot-dot plus x-sub-n, divided by n, which we can write using summation notation as one over n, times the sum from i equals 1 to n of x-sub-i.

**Example 2.2**: Calculating the Mean
- For the sample 8, 3, 7, 6, the mean x-bar equals 8 plus 3 plus 7 plus 6, all divided by 4, which equals 6.

- **Median**: mid-point of the ordered observations
  - For example, the sample 8, 3, 7, 6 when ordered becomes 3, 6, 7, 8
  - The median is the average of the middle two values, which equals 6 plus 7, divided by 2, which equals 6.5

- **Other measures:**
  - Mid-range: average of the smallest and largest values
  - Mode: most common value (not useful for continuous data)

- Most often the mean is used

> **Key Concept**: The mean is sensitive to outliers, while the median is robust. For skewed distributions, always report both measures to give a complete picture of central tendency.


### 2.1.3 Standard Deviation and Variance

- **Sample variance:**

The sample variance, s-squared, equals the sum of squared deviations from the mean, divided by n minus 1. In formula form: s-squared equals the sum of the quantity x-sub-1 minus x-bar, all squared, plus dot-dot-dot plus the quantity x-sub-n minus x-bar, all squared, divided by n minus 1. Using summation notation: one over n minus 1, times the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, all squared.

- The divisor n minus 1 is called the degrees of freedom
  - Only n minus 1 terms in the sum can vary since the x-sub-i values are linked by the constraint that x-bar equals one over n times the sum of all x-sub-i

**Example 2.3**: Calculating Variance and Standard Deviation
- The sample 8, 3, 7, 6 has n equals 4 and x-bar equals 6
- s-squared equals one over 3, times the quantity: 8 minus 6, all squared, plus 3 minus 6, all squared, plus 7 minus 6, all squared, plus 6 minus 6, all squared. This equals 14 divided by 3, which equals 4.66.

- **Sample standard deviation:** s equals the square root of s-squared
  - We take the square root to get back to the same units as x
  - For the sample 8, 3, 7, 6, we have s equals the square root of s-squared, which equals the square root of 4.66, which equals 2.16


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

> **Key Concept**: Standard deviation measures the typical distance of observations from the mean. For normal distributions, approximately 68% of data falls within 1 standard deviation, 95% within 2 standard deviations, and 99.7% within 3 standard deviations. This is known as the empirical rule.


### 2.1.5 Other Measures of Dispersion

- We most often use the standard deviation

- **Coefficient of variation:** CV equals s divided by x-bar
  - This measures dispersion relative to the mean

- **Interquartile range**
  - The difference between upper and lower quartiles

- **Mean absolute deviation:** one over n, times the sum from i equals 1 to n of the absolute value of x-sub-i minus x-bar
  - This is the average absolute deviation about the mean


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

- **Symmetry**
  - The density is the same when reflected about the mean
  - Normal and t distributions are examples

- **Skewness**: not symmetric
![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-11.jpg?height=353&width=369&top_left_y=482&top_left_x=60)
![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-11.jpg?height=362&width=371&top_left_y=480&top_left_x=450)
![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-11.jpg?height=356&width=369&top_left_y=482&top_left_x=841)

The skewness statistic is approximately: one over n, times the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, divided by s, all raised to the third power.

- This is the average of the z-score (which is x-sub-i minus x-bar, divided by s) raised to the third power
  - Where the z-score is standardized to have mean 0 and variance 1

- The skewness is zero if there is no skewness
- It's positive if right-skewed (examples include prices and income) and negative if left-skewed
- With skewed data, the mean does not equal the median
- For very skewed data, you may wish to use the median in addition to, or in place of, the mean

> **Key Concept**: Right-skewed data (positive skewness) is common in economics: earnings, prices, wealth. For highly skewed data, consider using the median or applying a log transformation to make the distribution more symmetric.


### 2.1.8 Kurtosis

The kurtosis statistic is approximately: one over n, times the sum from i equals 1 to n of the quantity x-sub-i minus x-bar, divided by s, all raised to the fourth power.

- This is the average of the z-score (x-sub-i minus x-bar, divided by s) raised to the fourth power.
- Excess kurtosis measures kurtosis relative to the normal distribution which has Kurt equals 3

Excess kurtosis equals Kurt minus 3.

- We view positive excess kurtosis as indicating fatter tails than the normal distribution.
- Since the measure involves x-sub-i minus x-bar raised to the fourth power, outliers get a lot of weight
- Financial returns data often have fat tails.


### 2.1.9 Box Plot

- A box and whisker plot, or more simply a box plot, provides in a simple graphic some of the key summary statistics.
- The median is the middle line.
- The upper and lower quartiles are the lines surrounding the median.
- The outer bars vary with the statistical package:
  - Sometimes they represent the minimum and maximum
  - Sometimes the following convention is used to indicate outliers:
    - The upper bar is the upper quartile plus 1.5 times the inter-quartile range
    - The lower bar is the lower quartile minus 1.5 times the inter-quartile range
    - Dots are observations outside these bars

![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-15.jpg?height=587&width=770&top_left_y=189&top_left_x=245)

> **Key Concept**: Summary statistics efficiently describe large datasets using measures of central tendency (mean, median) and dispersion (standard deviation, quartiles). For skewed data, the median is often more representative than the mean, and box plots provide a visual summary of key statistics including potential outliers.


## 2.2 Charts for Numerical Data

- Standard charts for cross-section data are the histogram and smoothed histogram.
- Example: Annual earnings of a sample of 171 female full-time workers aged 30 years in 2010, where full-time is defined as 35 or more hours per week and 48 or more weeks per year.
- The first nine observations are: 25,000, 40,000, 25,000, 38,000, 28,800, 31,000, 25,000, 20,000, and 83,000 dollars.
- Earnings range from 1,050 dollars to 172,000 dollars.
- Earnings are generally reported to the nearest hundred or thousand or ten thousand dollars.


### 2.2.1 Frequency Distribution (Tabulation in Ranges)

Looking at a summary of the data grouped into intervals of width 15,000 dollars: For example, 53 observations or 31% have earnings between 15,000 and 29,999 dollars. Breaking down the full distribution: 12 observations (7.0%) fall in the 0 to 14,999 range, 53 observations (31.0%) in the 15,000 to 29,999 range, 52 observations (30.4%) in the 30,000 to 44,999 range, 20 observations (11.7%) in the 45,000 to 59,999 range, 11 observations (6.4%) in the 60,000 to 74,999 range, 16 observations (9.4%) in the 75,000 to 89,999 range, 2 observations (1.2%) in the 90,000 to 104,999 range, 3 observations (1.8%) in the 105,000 to 119,999 range, 0 observations in the 120,000 to 134,999 range, 1 observation (0.6%) in the 135,000 to 149,999 range, 0 observations in the 150,000 to 164,999 range, and 1 observation (0.6%) in the 165,000 to 180,000 range.

### 2.2.2 Histogram

- The preceding table summarizes the data grouped into intervals of width 15,000 dollars
- Each interval is called a bin; here there are 13 bins, approximately equal to the square root of 171.
- Each bin is of equal bin width of 15,000 dollars.
- Frequency is the number of observations that fall into a given bin
- Relative frequency is the proportion (or percentage) that fall into a given bin
- A histogram is a graph of the frequency distribution with the horizontal axis showing values or range of values, and the vertical axis showing frequency or relative frequency or density (the relative frequency divided by the bin width)


### 2.2.3 Choosing Bin Width

- Smaller bin width gives more detail
- Here we compare 15,000 dollar to 7,500 dollar bin width.
![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-19.jpg?height=352&width=556&top_left_y=389&top_left_x=77)
![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-19.jpg?height=353&width=570&top_left_y=388&top_left_x=641)


### 2.2.4 Kernel Density Estimates (Smoothed Histogram)

- Continuous data such as earnings data have an underlying continuous density, for example the normal distribution which is a bell-shaped density. Probabilities are determined by areas under the curve, and the total area under a density is one (see Appendix 5.A).

- A kernel density estimate is a commonly-used estimate of a density
- It is a smoothed histogram that smooths in two ways:
  - It uses rolling bins (or windows) that overlap rather than being distinct
  - It counts the fraction of the sample within each bin with more weight given to observations at the window center and less to observations at the window ends
- We can compare the kernel density estimate to a proposed continuous density for the data, such as the normal distribution


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


## 2.3 Charts for Numerical Data by Category

Looking at U.S. health expenditures in 2018 totaling 3,653 billion dollars (18% of GDP), broken into its main subcomponents: Hospital Care accounts for 1,192 billion dollars, the largest category. Physician and Clinical Services account for 726 billion, Dental for 136 billion, Other Professional for 104 billion, Other Health and Personal for 192 billion, Home Health Care for 102 billion, Nursing Care for 169 billion, Drugs and Supplies through Retail Sales for 456 billion, Government Administration for 48 billion, Net Cost of Health Insurance for 259 billion, Government Public Health for 94 billion, Noncommercial Research for 53 billion, and Structures and Equipment for 122 billion dollars. These categories show how healthcare spending is distributed across different types of services and infrastructure.

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


## 2.5 Data Transformations

### 2.5.1 Natural Logarithm Transformation

- Many economic series are right-skewed: prices, income, wealth, and so on.
- The natural logarithm converts right-skewed data to a more symmetric distribution.
![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-31.jpg?height=348&width=544&top_left_y=372&top_left_x=91)
![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-31.jpg?height=349&width=537&top_left_y=372&top_left_x=651)
- Advantages of using natural logarithm are given in Chapter 9.


### 2.5.2 Standardized Scores (Z-Scores)

- Standardized scores, or z-scores, are useful for comparing series that are scaled differently
- Consider a sample with sample mean x-bar and standard deviation s
- We subtract the mean and divide by the sample standard deviation, so that z-sub-i equals x-sub-i minus x-bar, divided by s, for i equals 1 through n

- Then the z-scores z-sub-1 through z-sub-n have mean zero and sample standard deviation one.
- This is useful for comparing series that are scaled differently, for example test scores on two different tests.
- If for example z-sub-i equals negative 3, then x-sub-i was 3 standard deviations below the mean.

> **Key Concept**: Natural logarithm transformations convert right-skewed economic data (earnings, prices, wealth) to more symmetric distributions, facilitating analysis. Z-scores standardize data to have mean 0 and standard deviation 1, enabling comparison across different scales—useful when comparing test scores or measurements in different units.


## 2.6 Data Transformations for Time Series

### 2.6.1 Moving Averages and Seasonal Adjustment

- Moving averages smooth by averaging over several successive periods.
- Seasonal adjustment smooths by adjusting for seasonal variation.
![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-33.jpg?height=355&width=562&top_left_y=414&top_left_x=66)
![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-33.jpg?height=358&width=558&top_left_y=411&top_left_x=635)


### 2.6.2 Real and Per Capita Adjustments

- Real and nominal data: adjust for price inflation.
- Per capita data: adjust for population size.
![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-34.jpg?height=438&width=551&top_left_y=353&top_left_x=74)
![](https://cdn.mathpix.com/cropped/ce1742d8-4c04-44c0-9abd-85e107d473e1-34.jpg?height=446&width=549&top_left_y=348&top_left_x=639)


### 2.6.3 Growth Rates and Percentage Changes

- The one-period percentage change in x-sub-t is 100 times the quantity x-sub-t minus x-sub-t-minus-1, divided by x-sub-t-minus-1.
- This is often converted to an annualized rate—for example, for quarterly data the quarterly change is multiplied by four.
- We distinguish between percentage point change and percentage change:
  - Suppose the growth rate increases from 3 percent to 5 percent
  - Correct: the growth rate increased by two percentage points
  - Incorrect: there is a 2 percent increase in the growth rate (which would mean an increase from 3.0 percent to 3.0 times 1.02, which equals 3.06 percent)
- Very small changes are described in basis points, where a basis point is one-hundredth of a percentage point
- An approximation (explained in Chapter 9.1) is that the proportionate change in x equals the level change in natural log of x. So the percentage change in x-sub-t, which is defined as 100 times the quantity x-sub-t minus x-sub-t-minus-1, divided by x-sub-t-minus-1, is approximately equal to 100 times the quantity ln x-sub-t minus ln x-sub-t-minus-1.

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
