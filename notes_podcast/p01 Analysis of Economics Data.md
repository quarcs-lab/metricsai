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

Think of statistical analysis as having two complementary jobs. First, we describe what we see in our data. Second, we use that data to make broader claims about the world.

- **Descriptive analysis**
  - Mean, median, standard deviation, ...
  - Graphs and charts such as histograms and bar charts
  - Answers: "What does this particular dataset show?"

- **Statistical inference**
  - Extrapolate from the sample to the population
  - Often using confidence intervals and/or hypothesis tests
  - This is more challenging than data summary
  - Answers: "What can we say beyond this dataset?"

Much of this book focuses on statistical inference—learning to make reliable generalizations from limited data.

> **Key Concept**: Descriptive analysis summarizes data using statistics and visualizations. Statistical inference goes further, using sample data to draw conclusions about the broader population. Think of it this way: descriptive analysis tells you what happened in your data; inference tells you what that means for the world beyond your data.

**Why This Matters**: Economists rarely have data on entire populations. We sample 1,000 people to understand millions, or study 100 firms to learn about thousands. Statistical inference gives us the tools to make these leaps responsibly.

Now that we understand what statistical methods do, let's explore the different types of data we'll work with.

## 1.2 Types of Data

Not all data are created equal. The type of data you have determines which statistical tools you can use.

- **Numerical data that are continuous**
  - Can take any value within a range
  - Examples: GDP, earnings, temperature, weight
  - Most common in economics

- **Numerical data that are discrete**
  - Can only take specific integer values
  - Example: number of doctor visits by an individual in one year
  - You can have 0, 1, 2, or 3 visits, but not 2.5 visits

- **Categorical data**
  - Represents categories, not numbers
  - Example: employed, unemployed, or out of the labor force
  - We can count people in each category, but can't average the categories themselves

This book focuses on continuous numerical data—the data type most commonly analyzed in economics. More advanced courses adapt these methods to handle discrete and categorical data.


### 1.2.1 Observational vs Experimental Data

Within these data types, we also distinguish between how the data were collected.

- **Observational data**
  - Based on observed behavior in an uncontrolled environment
  - Economics data are most often observational
  - Example: We observe people's college degrees and earnings, but we didn't assign who goes to college

- **Experimental data**
  - Observations from experiments controlled by the investigator
  - Example: A medical trial where researchers randomly assign patients to treatment or placebo
  - Less common in economics because we can't randomly assign major life decisions

Here's the challenge: it's difficult to establish causal effects using observational data. Consider the college-earnings relationship. Do college graduates earn more because of their degree, or because people who choose college were already different (more motivated, better connected, etc.)? We call this the self-selection problem.

Advanced econometrics research seeks to estimate causal relationships even with observational data, using clever techniques we'll explore later.

This book focuses on measuring association (not causation) using observational data. We'll learn how strong the relationship is between variables, even if we can't always prove one causes the other. Causal methods appear in Chapter 17 and in some case studies in Chapter 13.

> **Key Concept**: Economics primarily uses observational data—we observe behavior in uncontrolled settings rather than conducting experiments. This makes establishing causation difficult. For example, college graduates earn more than non-graduates, but is this because college increases earnings, or because people who attend college were already different? Most of this book focuses on measuring associations reliably, leaving causal inference for advanced chapters.


### 1.2.2 Three Types of Data Collection

Beyond what we measure, we also care about when and whom we measure. There are three fundamental data structures:

- **Cross-section**
  - Snapshot of many individuals at a single point in time
  - Example: Survey 1,000 workers in 2024, recording each person's earnings
  - We use subscript i (i equals 1 through n) to index individuals
  - Notation example: x-sub-i means "the value of x for person i"

- **Time series**
  - Track one individual (or entity) over many time periods
  - Example: US GDP measured quarterly from 1990 to 2024
  - We use subscript t (t equals 1 through T) to index time periods
  - Notation example: x-sub-t means "the value of x at time t"

- **Panel data** (also called longitudinal data)
  - Track many individuals over multiple time periods
  - Example: Survey the same 1,000 workers every year from 2020 to 2024
  - We use two subscripts: i for individuals and t for time
  - Notation example: x-sub-i-t means "the value of x for person i at time t"

The same basic statistical methods apply to all three data structures. However, each has special considerations. Cross-section data assume observations are independent—person A's earnings don't affect person B's. Time series data violate this assumption because today's GDP is correlated with yesterday's. This affects how we compute standard errors—our measure of estimate precision.

This book focuses on cross-section data, the simplest and most common case. Later chapters extend these methods to panel and time series data.

> **Key Concept**: Data structures matter for statistical inference. Cross-section data give us many individuals at one time (i indexes people). Time series data track one individual over time (t indexes periods). Panel data combine both (i and t). Each structure requires different assumptions about independence, which affects how we measure the precision of our estimates.

## 1.3 Regression Analysis

Now that we understand data types and structures, let's preview the main analytical tool we'll use throughout this book: regression analysis.

Regression analysis is the workhorse of econometrics. It answers questions like: "How much does an additional year of education increase earnings?" or "How sensitive is consumer spending to interest rate changes?"

**Example 1.1**: House Price and Size

Imagine you're house hunting and notice that bigger houses cost more. But how much more, exactly? We can answer this precisely using regression analysis.

The scatter plot below shows data from 29 house sales. Each dot represents one house, with size (in square feet) on the horizontal axis and price (in dollars) on the vertical axis. The line running through the dots is our regression line—the best-fitting straight line through this cloud of points.

![](https://cdn.mathpix.com/cropped/19aa47c9-f2c6-457a-b9b1-534d2014d725-08.jpg?height=507&width=680&top_left_y=358&top_left_x=297)

The slope of this line is 74. This number tells us that each additional square foot of house size is associated with a 74 dollar increase in price, on average. So if you compare two houses that differ by 100 square feet, you'd expect the larger one to cost about 7,400 dollars more.

We'll cover regression in detail in Chapters 5-7, but this example gives you the basic idea: regression quantifies relationships between variables.

> **Key Concept**: Regression analysis quantifies relationships between variables by fitting a line (or curve) through data points. The slope coefficient tells us how much the outcome variable (y) changes when the explanatory variable (x) increases by one unit. In our house example, the slope of 74 means each additional square foot is associated with a 74 dollar price increase.


## 1.4 Book Outline

Now that you understand the landscape of econometric data and methods, let's map out the journey ahead. This book follows a pedagogical progression from simple to complex.

- **Univariate data** (Chapters 2-4)
  - Work with a single variable: x
  - Topics covered in introductory statistics courses
  - Example: Analyzing the distribution of incomes

- **Bivariate data** (Chapters 5-9)
  - Examine relationships between two variables: y and x
  - Regression line: y equals b-one plus b-two times x
  - Example: How house price (y) relates to size (x)

- **Multivariate data** (Chapters 10-15)
  - Handle many variables simultaneously
  - Regression line: y equals b-one plus b-two times x-two, plus b-three times x-three, and so on
  - Example: How house price depends on size, bedrooms, location, and age

- **Further Topics** (Chapters 16-17)
  - Model diagnostics and checking assumptions
  - Panel data and time series methods
  - Causal inference with observational data

> **Key Concept**: This book builds skills progressively. Start with one variable (univariate), then two variables (bivariate regression), then many variables (multiple regression). This scaffolding approach ensures you master each level before adding complexity. Think of it like learning to cook: master boiling water before attempting a soufflé.

## 1.5 Background

Before diving into econometrics, let's preview the mathematical tools you'll encounter. Don't worry—we'll introduce each tool gradually when needed. For now, just get familiar with the basic ideas.

**Summation Notation**

When we add up many numbers, writing "x-sub-1 plus x-sub-2 plus x-sub-3" gets tedious. Summation notation provides a shorthand. The expression "the sum from i equals 1 to n of x-sub-i" means:
- Start with i equals 1, take x-sub-1
- Then i equals 2, add x-sub-2
- Continue until i equals n, add x-sub-n

This compact notation lets us write formulas concisely without endless "plus" symbols.

**Example 1.2**: Summation Notation

Let's calculate: the sum from i equals 1 to 3 of the quantity 2 plus 3 divided by i.

Breaking this down:
- When i equals 1: 2 plus 3 divided by 1 equals 5
- When i equals 2: 2 plus 3 divided by 2 equals 3.5
- When i equals 3: 2 plus 3 divided by 3 equals 3

Total: 5 plus 3.5 plus 3 equals 11.5

**Calculus**

Calculus appears occasionally but isn't essential for understanding core concepts.

The key idea: delta-y divided by delta-x measures "rise over run"—how much y changes when x increases by one unit. The derivative refines this by asking: how much does y change for infinitesimally small changes in x? This gives us instantaneous rates of change.

If you haven't studied calculus, don't worry. We'll explain intuitions whenever derivatives appear.

**Natural Logarithms and Exponentials**

These tools help us model growth rates and percentage changes. We'll introduce them properly in Chapter 9.

**Expected Values**

Expected values describe population characteristics. Think of them as "what we'd get on average if we could observe the entire population."

Key definitions:
- Population mean: mu equals E of X (the expected value of X)
  - This is the average value we'd get if we measured X for everyone
- Population variance: sigma-squared equals E of the quantity X minus mu, all squared
  - This measures how spread out the population values are

We'll explore expected values thoroughly in Chapter 3.

> **Key Concept**: Econometric analysis uses mathematical tools as a language for precision. Summation notation (sigma) lets us write "add these up" concisely. Calculus helps us understand rates of change. Expected values describe population characteristics. Don't be intimidated—these tools are just shorthand for intuitive ideas. Focus on understanding the concepts, and the notation will become familiar with practice.

## 1.6 Key Learning Tool

Here's the truth about learning econometrics: you can't master it by just reading. Imagine trying to learn piano by reading about music theory—you'd understand the concepts intellectually but couldn't actually play. Econometrics is the same. You must practice with real data.

- **Learning-by-doing**
  - Work through data examples using econometric software (Python, R, Stata, etc.)
  - Complete chapter exercises and course assignments
  - Don't just read the solutions—run the code yourself and experiment
  - When something doesn't work, debug it. Mistakes teach more than successes.

Start small. Run the example code. Change one number and see what happens. Make mistakes and fix them. Over time, you'll develop the intuition that separates those who understand econometrics from those who merely memorized formulas.

> **Key Concept**: Econometrics is a hands-on skill. Reading about regression won't make you competent—you must analyze data yourself. Think of this textbook as a cookbook: the recipes are here, but you need to actually cook to become a chef. Dedicate time to working with data in Python, R, or your preferred software. The struggle of figuring out why code doesn't run or why results look strange is where real learning happens.

**Quick Check**: Before moving to Chapter 2, ask yourself: Do I have access to statistical software? Have I set up my workspace? Can I load a simple dataset? If not, take time now to get your tools ready. You'll need them starting in Chapter 2.

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
- The textbook follows a pedagogical progression: univariate analysis leads to bivariate regression leads to multivariate analysis
- Early chapters (2-4) cover statistical foundations with single variables
- Middle chapters (5-9) introduce bivariate regression with two variables
- Later chapters (10-15) extend to multiple regression with many variables
- Advanced topics (16-17) cover model diagnostics, panel data, time series, and causal inference

**Prerequisites and Learning Approach:**
- Summation notation (sigma) is used throughout the text to express formulas concisely
- Calculus concepts (derivatives, rates of change) appear occasionally but are not essential
- Natural logarithms and exponentials are covered in Chapter 9 for modeling growth and elasticities
- Expected values (E of X) are fundamental for defining population parameters like means and variances
- The most effective learning strategy is "learning-by-doing" through hands-on data analysis
- Regular practice with econometric software and completion of exercises is essential for mastery

---
