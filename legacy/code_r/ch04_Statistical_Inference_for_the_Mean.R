# ch04_Statistical_Inference_for_the_Mean.R
# Updated for online execution portability

########## OVERVIEW ##########

# R Program
# copyright C 2021 by A. Colin Cameron
# Used for "Analysis of Economics Data: AN Introduction to Econometrics"
# by A. Colin Cameron (2021)

# To run you need file
#   AED_EARNINGS.DTA
#   AED_GASPRICE.DTA
#   AED_EARNINGSMALE.DTA
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
library(haven)

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

# This R program covers Chapter 4 of "Analysis of Economics Data"
#   4.1 EXAMPLE: MEAN ANNUAL EARNINGS
#   4.2 t STATISTIC AND t DISTRIBUTION
#   4.3 CONFIDENCE INTERVALS
#   4.4 TWO-SIDED HYPOTHESIS TESTS
#   4.5 TWO-SIDED HYPOTHESIS TEST EXAMPLES
#   4.6 ONE-SIDED DIRECTIONAL HYPOTHESIS TESTS
#   4.7 GENERALIZATIONS OF CONFIDENCE INTERVALS AND HYPOTHESIS TESTS
#   4.8 PROPORTIONS DATA

########## DATA DESCRIPTION

#  (1) Annual Earnings for 171 women age 30 years in 2010 Full-time workers
#  (2) Gasoline price per gallon at 32 service stations
#  (3) Annual Earnings for 191 men age 30 years in 2010 Full-time workers
#  (4) Quarterly data on U.S. real GDP per capita from 1959Q1 to 2020Q1

#### 4.1 EXAMPLE: MEAN ANNUAL EARNINGS

# Read in the Stata data set
data.EARNINGS = load_data("AED_EARNINGS.DTA")
# Allow variables in database to be accessed simply by giving names
attach(data.EARNINGS)
# Summarize the data set
summary(data.EARNINGS)

# Summary statistics
summary(earnings)
sd(earnings)

# 95% Confidence interval
t.test(earnings)$"conf.int"

# Hypothesis test
t.test(earnings, mu=40000)

####  4.2 t Statistic and t DISTRIBUTION

# Plot standard normal and t densities with 4 and 30 degrees of freedom

# Figure 4.1 Panel A  t(4) and standard normal
x <- seq(-4, 4, length=100)
hx <- dnorm(x)
labels <- c("t with df = 5", "standard normal")
plot(x, hx, type="l", lty=2, lwd=2, xlab="x value",
     ylab="Density", main="t(4) and standard normal")
lines(x, dt(x,4), lty=1, lwd=2)
legend("topright", inset=.02, title="Distributions",
       labels, lwd=2, lty=c(1, 2))

# Figure 4.1 Panel B  t(30) and standard normal
labels <- c("t with df = 30", "standard normal")
plot(x, hx, type="l", lty=2, lwd=2, xlab="x value",
     ylab="Density", main="t(30) and standard normal")
lines(x, dt(x,20), lty=1, lwd=2)
legend("topright", inset=.02, title="Distributions",
       labels, lwd=2, lty=c(1, 2))

# Figure 4.2
# Illustrates critical values for t(170)
# Not reproduced in R

#### 4.3 CONFIDENCE INTERVALS

summary(earnings)

# 95% Confidence interval
t.test(earnings)$"conf.int"

# 90% and 99% confidence intervals
t.test(earnings, conf.level=0.90)$"conf.int"
t.test(earnings, conf.level=0.99)$"conf.int"

# Confidence interval manually
mean = mean(earnings)
sd = sd(earnings)
N = length(earnings)
sterror = sd/sqrt(N)
tcrit = qt(.975,N-1)
intwidth = tcrit*sterror
print("95% confidence interval = ")
cbind(mean - intwidth, mean + intwidth)

#### 4.4 TWO-SIDED HYPOTHESIS TEST

# Test H0: mu = 40000 against HA: mu not = 40000
t.test(earnings, mu = 40000)

# Same two-sided test done manually
mu0 = 40000
mean = mean(earnings)
sd = sd(earnings)
N = length(earnings)
sterror = sd/sqrt(N)
t = (mean-mu0)/sterror
p = 2*(1-pt(abs(t),N-1))
# Equivalent is 2*pt(t,N-1,lower.tail=FALSE)
tcrit = qt(.975,N-1)
print("t statistic, p-value, critical value")
cbind(t, p, tcrit)

# Figure 4.3 shows two-sided tests graphically
# Not reproduced in R

####   4.5 TWO-SIDED HYPOTHESIS TEST EXAMPLES

# Gasoline price September 2 2013 from sactogasprices.com part of GasBuddy.com
rm(list=ls())
github_data_url <- "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/"
library(haven)
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
data.GASPRICE = load_data("AED_GASPRICE.DTA")
attach(data.GASPRICE)
summary(data.GASPRICE)
summary(price)

# Test H0: mu = 3.81 against HA: mu not = 3.81
t.test(price, mu = 3.81)
t = (3.6697-3.81)/(0.1510/sqrt(32))
p = 2*(1-pt(abs(t),31))
tcrit = qt(.975,31)
cbind(t, p, tcrit)

# Male Earnings 2010 30 year old full time workers
data.EARNINGSMALE = load_data("AED_EARNINGSMALE.DTA")
attach(data.EARNINGSMALE)
summary(data.EARNINGSMALE)
summary(earnings)

# Test H0: mu = 50000 against HA: mu not = 50000
t.test(earnings, mu=50000)
t = (52353.93-50000)/(65034.74/sqrt(191))
p = 2*(1-pt(abs(t),190))
tcrit= qt(.975,190)
cbind(t, p, tcrit)

# Growth in real GDP per capita
data.REALGDPPC = load_data("AED_REALGDPPC.DTA")
attach(data.REALGDPPC)
summary(data.REALGDPPC)
summary(growth)

# Test H0: mu = 2.0 against HA: mu not = 2.0
t.test(growth, mu=2.0)
t = (1.9904-2.0)/(2.1781/sqrt(241))
p = 2*(1-pt(abs(t),241))
tcrit= qt(.975,241)
cbind(t, p, tcrit)

#### 4.6 ONE-SIDED DIRECTIONAL HYPOTHESIS TESTS

t.test(earnings, mu=50000, alternative = "less")

# Figure 4.4 shows one-sided test graphically
# Not reproduced in R

data.EARNINGS = load_data("AED_EARNINGS.DTA")
attach(data.EARNINGS)
summary(data.EARNINGS)
summary(earnings)

# Test H0: mu < 40000 against HA: mu >= 40000
t.test(earnings, mu=40000, alternative = "greater")

# Same one-sided test done manually
mu0 = 40000
mean = mean(earnings)
sd = sd(earnings)
N = length(earnings)
sterror = sd/sqrt(N)
t = (mean-mu0)/sterror
p = 1-pt(abs(t),N-1)
# Equivalent is pt(t,N-1,lower.tail=FALSE)
tcrit = qt(.95,N-1)
print("t statistic, p-value, critical value")
cbind(t, p, tcrit)

#### 4.7 GENERALIZATIONS OF CONFIDENCE INTERVALS AND HYPOTHESIS TESTS

#### 4.8 PROPORTIONS DATA

# Confidence interval
mean = (480*1+441*0)/921
sterror = sqrt( (mean*(1-mean)) / 921)
print("mean and standard error")
cbind(mean, sterror)
print("95% CI")
cbind(mean-1.964*sterror, mean+1.964*sterror)

# Test mu = 0.50
sterrorH0 = sqrt( (0.5*(1-0.5)) / 921)
t = (mean - 0.5) / sterrorH0
p = 2*(1-pnorm(abs(t)))
tcrit = 1.96
print("t statistic, p-value, critical value")
cbind(t, p, tcrit)

########## CLOSE OUTPUT

cat("Chapter 4 analysis complete.\n")
