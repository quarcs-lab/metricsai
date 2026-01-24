# Chapter 1: Analysis of Economics Data

## Learning Objectives

By the end of this chapter, you will be able to:
- Distinguish between descriptive analysis and statistical inference
- Identify different types of data (continuous, discrete, categorical)
- Understand the difference between observational and experimental data
- Recognize the three main data collection methods (cross-section, time series, panel)
- Understand the basic concept of regression analysis
- Navigate the structure and organization of this textbook

---

## 1.1 Statistical Methods

- There are two aspects to statistical analysis of data:

- **Descriptive analysis**
  - Mean, median, standard deviation, ...
  - Graphs and charts such as histograms and bar charts

- **Statistical inference**
  - Extrapolate from the sample to the population
  - Often using confidence intervals and/or hypothesis tests
  - This is more challenging than data summary

- Much of this book entails statistical inference.

> **Key Concept**: Descriptive analysis summarizes data using statistics and visualizations, while statistical inference uses sample data to draw conclusions about the broader population. Most econometric analysis involves statistical inference.


## 1.2 Types of Data

- There are broad types of data:

- **Numerical data that are continuous**
  - e.g., GDP, earnings

- **Numerical data that are discrete**
  - e.g., number of doctor visits by an individual in one year

- **Categorical data**
  - e.g., employed, unemployed or out of the labor force

- The book focuses on continuous numerical data
  - This is the data type usually analyzed in economics
  - More advanced courses adapt the methods of this book to the other types of data


### 1.2.1 Observational vs Experimental Data

- **Observational data**
  - Based on observed behavior in an uncontrolled environment
  - Economics data are most often observational

- **Experimental data**
  - Observations on the results of experiments that can be controlled by the investigator

  - It is difficult to establish causal effects using observational data
    - e.g., in determining the causal effect of a college degree on earnings we need to control for individual self-selection into college
  - Advanced econometrics research seeks to estimate causal relationships even with observational data

- The book focuses on measuring association (not causation) using observational data
  - Causal methods are presented in Ch. 17 and in some case studies in Ch. 13

> **Key Concept**: Economics primarily uses observational data where we observe behavior in uncontrolled settings. Unlike experimental data where conditions can be controlled, observational data requires careful methods to establish relationships and, when possible, causal effects.


### 1.2.2 Three Types of Data Collection

Distinguish between three types of data collection:

- **Cross-section**
  - Individuals (people, firms, countries, ...) at a point in time
  - Denoted by subscript $i=1, \ldots, n$, e.g., $x_{i}$

- **Time series**
  - Over time for the same individual (stock price, US GDP, ...)
  - Denoted by subscript $t=1, \ldots, T$, e.g., $x_{t}$

- **Panel data** (or longitudinal data)
  - Individuals over time
  - Denoted by subscripts $i$ and $t$, e.g., $x_{it}$

- The same basic statistical methods apply in all cases
  - But each has its own special considerations for statistical inference
  - Notably computing standard errors (the precision of estimates)
  - And has its own special considerations for model specification

- We focus on cross-section data
  - This is the simplest and most common case

> **Key Concept**: The three main types of data collection are cross-section (multiple individuals at one time), time series (one individual over time), and panel data (multiple individuals over time). Each type requires different considerations for statistical inference, particularly for computing standard errors.

## 1.3 Regression Analysis

- Economic data analysis focuses on regression analysis

**Example 1.1**: House Price and Size

Relationship between house price ($y$) and house size in square feet ($x$) for 29 sales (covered in detail in Chapters 5-7):
- Slope is 74, so one more square foot is associated with $74 higher price

![](https://cdn.mathpix.com/cropped/19aa47c9-f2c6-457a-b9b1-534d2014d725-08.jpg?height=507&width=680&top_left_y=358&top_left_x=297)

> **Key Concept**: Regression analysis quantifies the relationship between variables. In a bivariate regression, the slope coefficient tells us how much the outcome variable ($y$) changes when the explanatory variable ($x$) increases by one unit.


## 1.4 Book Outline

- **Univariate data** (Chapters 2-4)
  - Single series $x$
  - Covered in introductory statistics

- **Bivariate data** (Chapters 5-9)
  - Two series $y$ and $x$
  - Regression line is $y=b_{1}+b_{2} x$

- **Multivariate data** (Chapters 10-15)
  - Many series
  - Regression line is $y=b_{1}+b_{2} x_{2}+b_{3} x_{3}+\cdots+b_{k} x_{k}$

- **Further Topics** (Chapters 16-17)

> **Key Concept**: The textbook progresses from simple to complex: univariate analysis (one variable), bivariate regression (two variables), to multivariate regression (many variables). This structure builds understanding systematically.

## 1.5 Background

- **Summation notation** is used throughout
  - $\sum_{i=1}^{n} x_{i}=x_{1}+x_{2}+\cdots+x_{n}$

**Example 1.2**: Summation Notation
- $\sum_{i=1}^{3}(2+3 / i)=(2+3 / 1)+(2+3 / 2)+(2+3 / 3)=11.5$

- **Calculus** is used occasionally but is not essential
  - Let $\Delta y$ denote the change in $y$ and $\Delta x$ denote the change in $x$
  - Then $\Delta y / \Delta x$ is the change in $y$ when $x$ changes by one unit
  - The derivative $d y / d x$ equals $\Delta y / \Delta x$ as $\Delta x \rightarrow 0$

- **Natural logarithms and exponentials** are used (Chapter 9)

- **Expected values** are used (Chapter 3). In particular:
  - Population mean: $\mu=\mathrm{E}[X]$
  - Population variance: $\sigma^{2}=\mathrm{E}\left[(X-\mu)^{2}\right]$

> **Key Concept**: Econometric analysis requires basic mathematical tools: summation notation (Σ) for aggregating data, calculus for understanding rates of change, natural logarithms for modeling growth and elasticities, and expected values for describing population distributions. These tools appear throughout the text but are not essential to understand the core concepts.

## 1.6 Key Learning Tool

- **Learning-by-doing**
  - Do data examples using an econometrics or statistical package
  - Do chapter exercises and course assignments

> **Key Concept**: Learning econometrics requires active engagement with data and software. Reading about statistical methods is insufficient—you must practice by running analyses, interpreting results, and completing exercises. Hands-on experience with econometric packages (Python, R) is essential for developing practical skills.

---

## Key Takeaways

**Statistical Methods and Data Types:**
- Econometrics uses two main approaches: descriptive analysis (summarizing data) and statistical inference (drawing population conclusions from samples)
- Economic data are primarily continuous and numerical, though categorical and discrete data are also important
- Economics relies mainly on observational data, making causal inference more challenging than with experimental data
- The three data collection methods are cross-section (individuals at one time), time series (one individual over time), and panel data (individuals over time)
- Each data type requires different considerations for statistical inference, particularly when computing standard errors
- This book focuses on continuous numerical data and cross-section analysis as the foundation for more advanced methods

**Regression Analysis and Course Structure:**
- Regression analysis is the primary tool in econometrics, quantifying how outcome variables (y) vary with explanatory variables (x)
- The slope coefficient in regression measures the association: how much y changes when x increases by one unit
- The textbook follows a pedagogical progression: univariate → bivariate → multivariate analysis
- Early chapters (2-4) cover statistical foundations with single variables
- Middle chapters (5-9) introduce bivariate regression with two variables
- Later chapters (10-15) extend to multiple regression with many variables
- Advanced topics (16-17) cover model diagnostics, panel data, time series, and causal inference

**Prerequisites and Learning Approach:**
- Summation notation (Σ) is used throughout the text to express formulas concisely
- Calculus concepts (derivatives, rates of change) appear occasionally but are not essential
- Natural logarithms and exponentials are covered in Chapter 9 for modeling growth and elasticities
- Expected values (E[X]) are fundamental for defining population parameters like means and variances
- The most effective learning strategy is "learning-by-doing" through hands-on data analysis
- Regular practice with econometric software and completion of exercises is essential for mastery

---

