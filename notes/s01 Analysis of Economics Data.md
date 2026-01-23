# Chapter 1: Analysis of Economics Data

- This book provides an introduction to **econometrics**
  - Uses a subset of statistical methods
  - Most notably **regression analysis**
  - An outcome $y$ varies with one or more variables

- The book emphasizes economic interpretation of economics-related data

##  Outline

(1) Statistical Methods
(2) Types of Data
(3) Regression Analysis
(4) Overview

### 1.1 Statistical Methods

- There are two aspects to statistical analysis of data:

- **Descriptive analysis**
  - Mean, median, standard deviation, ...
  - Graphs and charts such as histograms and bar charts

- **Statistical inference**
  - Extrapolate from the sample to the population
  - Often using confidence intervals and/or hypothesis tests
  - This is more challenging than data summary

- Much of this book entails statistical inference.


### 1.2 Types of Data

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


#### Observational vs Experimental Data

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


#### Three Types of Data Collection

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


### 1.3 Regression Analysis

- Economic data analysis focuses on regression analysis

- Example in Chapters 5-7: relationship between house price ($y$) and house size in square feet ($x$) for 29 sales
  - Slope is 74, so one more square foot is associated with $74 higher price

![](https://cdn.mathpix.com/cropped/19aa47c9-f2c6-457a-b9b1-534d2014d725-08.jpg?height=507&width=680&top_left_y=358&top_left_x=297)


### 1.4 Book Outline

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


### 1.5 Background

- **Summation notation** is used throughout
  - $\sum_{i=1}^{n} x_{i}=x_{1}+x_{2}+\cdots+x_{n}$
  - e.g., $\sum_{i=1}^{3}(2+3 / i)=(2+3 / 1)+(2+3 / 2)+(2+3 / 3)=11.5$

- **Calculus** is used occasionally but is not essential
  - Let $\Delta y$ denote the change in $y$ and $\Delta x$ denote the change in $x$
  - Then $\Delta y / \Delta x$ is the change in $y$ when $x$ changes by one unit
  - The derivative $d y / d x$ equals $\Delta y / \Delta x$ as $\Delta x \rightarrow 0$

- **Natural logarithms and exponentials** are used (Chapter 9)

- **Expected values** are used (Chapter 3). In particular:
  - Population mean: $\mu=\mathrm{E}[X]$
  - Population variance: $\sigma^{2}=\mathrm{E}\left[(X-\mu)^{2}\right]$


### 1.6 Key Learning Tool

- **Learning-by-doing**
  - Do data examples using an econometrics or statistical package
  - Do chapter exercises and course assignments

