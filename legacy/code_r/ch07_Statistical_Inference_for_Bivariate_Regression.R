# ch07_Statistical_Inference_for_Bivariate_Regression.R
# Updated for online execution portability

########## OVERVIEW ##########

# R Program
# copyright C 2021 by A. Colin Cameron
# Used for "Analysis of Economics Data: AN Introduction to Econometrics"
# by A. Colin Cameron (2021)

# To run you need file
#   AED_HOUSE.DTA
#   AED_REALGDPPC.DTA
# in your directory

########## SETUP ##########

# Clear the workspace
rm(list=ls())

# Set random seed for reproducibility
set.seed(42)

# GitHub data URL
github_data_url <- "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/"

# Create output directories (optional - for saving figures and tables locally)
images_dir <- "images"
tables_dir <- "tables"
dir.create(images_dir, showWarnings = FALSE, recursive = TRUE)
dir.create(tables_dir, showWarnings = FALSE, recursive = TRUE)

# Load required libraries (install if needed)
if (!require("haven")) install.packages("haven")
if (!require("MASS")) install.packages("MASS")
if (!require("lmtest")) install.packages("lmtest")
if (!require("car")) install.packages("car")
if (!require("sandwich")) install.packages("sandwich")
if (!require("jtools")) install.packages("jtools")
library(haven)
library(MASS)
library(lmtest)
library(car)
library(sandwich)
library(jtools)

# Function to load data from GitHub
load_data <- function(filename) {
  url <- paste0(github_data_url, filename)
  tryCatch({
    read_dta(url)
  }, error = function(e) {
    message("Error loading from GitHub: ", e$message)
    message("Attempting to load from local directory...")
    read_dta(file.path("../data_stata", filename))
  })
}

############

# This R program covers Chapter 7 of "Analysis of Economics Data"
#   7.1 EXAMPLE: HOUSE PRICE AND SIZE
#   7.2 THE T STATISTIC
#   7.3 CONFIDENCE INTERVALS
#   7.4 TESTS OF STATISTICAL SIGNIFICANCE
#   7.5 TWO-SIDED HYPOTHESIS TESTS
#   7.6 ONE-SIDED DIRECTIONAL HYPOTHESIS TESTS
#   7.7 ROBUST STANDARD ERRORS

########## DATA DESCRIPTION

# House sale price for 29 houses in Central Davis in 1999
#     29 observations on 9 variables

#### 7.1 EXAMPLE: HOUSE PRICE AND SIZE

# Read in the Stata data set
data.HOUSE = load_data("AED_HOUSE.DTA")

# Allow variables in database to be accessed simply by giving names
attach(data.HOUSE)

# Summarize the data set
summary(data.HOUSE)
head(data.HOUSE)

# Table 7.1
ols <- lm(price ~ size)
summary(ols)

# For confidence interval use confint function in MASS package
confint(ols)

# Nicer output
summ(ols, digits=3)
# Nicer output with confidence interval
summ(ols, digits=3, confint = TRUE)

#### 7.3 CONFIDENCE INTERVALS

# Previous calculated manually

# coefficients[2,1] is b for 2nd regressor (after the intercept)
# coefficients[2,2] is se for 2nd regressor (after the intercept)
# Here that is size
# And more easily can use the variable name
# So coefficients["size",1]

coef=summary(ols)$coefficients["size",1]
sterror=summary(ols)$coefficients["size",2]
N = length(price)
cbind(coef,sterror,N)
coef + c(-1,1)*sterror*qt(0.975, N-2)

# Example with artificial data
x = c(1, 2, 3, 4, 5)
y = c(1, 2, 2, 2, 3)
olsxy = lm(y ~ x)
summary(olsxy)
coef=summary(olsxy)$coefficients["x",1]
sterror=summary(olsxy)$coefficients["x",2]
N = length(x)
cbind(coef,sterror,N)
coef + c(-1,1)*sterror*qt(0.975, N-2)

#### 7.4 TESTS OF STATISTICAL SIGNIFICANCE

# Read in the Stata data set
data.HOUSE = load_data("AED_HOUSE.DTA")
attach(data.HOUSE)
summary(data.HOUSE)
head(data.HOUSE)

ols <- lm(price ~ size)
summary(ols)

##### 7.5 TWO-SIDED HYPOTHESIS TESTS

ols <- lm(price ~ size)
summary(ols)

# For individual tests and CI's use coeftest and coefci in package lmtest
coeftest(ols)
coefci(ols)

# Two-sided Test that slope coefficient of size = 90 manually
coef=summary(ols)$coefficients["size",1]
sterror=summary(ols)$coefficients["size",2]
cbind(coef,sterror)
N = length(size)
t = (coef - 90)/sterror
p = 2*(1-pt(abs(t),N-2))
tcrit = qt(.975,N-2)
print("t statistic, p-value, critical value")
cbind(t, p, tcrit)

# Two-sided Test that slope = 90 using linearHypothesis in car
linearHypothesis(ols,c("size=90"))

#### 7.6 ONE-SIDED HYPOTHESIS TESTS

# Use previous test
# Halve the two-sided p-value provided
# t>0 for an upper one-tailed alternative
# t<0 for a lower one-tailed alternative

####  7.7 ROBUST STANDARD ERRORS

# Heteroskedastic robust
ols <- lm(price ~ size)
summary(ols)

robvar <- vcovHC(ols, type = "HC1")
coefci(ols, vcov = robvar)
coeftest(ols, vcov = robvar)

########## CLOSE OUTPUT

cat("Chapter 7 analysis complete.\n")
