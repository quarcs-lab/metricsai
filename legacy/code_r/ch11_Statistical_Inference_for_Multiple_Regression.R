# ch11_Statistical_Inference_for_Multiple_Regression.R - January 2026 For R
# Updated for online execution portability

########## OVERVIEW ##########

# R Program
# copyright C 2021 by A. Colin Cameron (original code)
# Updated: 2026 for portability
# Used for "Analysis of Economics Data: An Introduction to Econometrics"
# by A. Colin Cameron (2021)

# Data is streamed directly from GitHub - no local files needed
# Works in RStudio Cloud, Posit Cloud, and any online R environment

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
if (!require("car")) install.packages("car")
if (!require("sandwich")) install.packages("sandwich")
if (!require("jtools")) install.packages("jtools")
if (!require("huxtable")) install.packages("huxtable")

library(haven)
library(car)
library(sandwich)
library(jtools)
library(huxtable)

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
    
# This R program covers Chapter 11 of "Analysis of Economics Data"
#  11.1 PROPERTIES OF THE LEAST SQUARES ESTIMATOR
#  11.2 ESTIMATORS OF MODEL PARAMETERS
#  11.3 CONFIDENCE INTERVALS
#  11.4 HYPOTHESIS TESTS ON A SINGLE PARAMETER
#  11.5 JOINT HYPOTHESIS TESTS
#  11.6 F STATISTIC UNDER ASSUMPTIONS 1-4
#  11.7 PRESENTATION OF REGRESSION RESULTS

############# DATA DESCRIPTION

# House sale price for 29 houses in Central Davis in 1999
#     29 observations on 9 variables 

####  11.1 - 11.4 EXAMPLE: HOUSE PRICE AND CHARACTERISTICS

# Read in the Stata data set from GitHub
data.HOUSE = load_data("AED_HOUSE.DTA")

# Allow variables in database to be accessed simply by giving names
attach(data.HOUSE)

# Summarize the data set
summary(data.HOUSE)

# Table 11.1 - not produced by statistical package

# Table 11.2
# Multiple regression
ols = lm(price ~ size+bedrooms+bathrooms+lotsize+age+monthsold)
summary(ols)

# Confidence intervals
library(jtools)
summ(ols, digits=3, confint = TRUE) 

# Confidence interval manually for size
coef=summary(ols)$coefficients["size",1]
sterror=summary(ols)$coefficients["size",2]
df = summary(ols)$df[2]
N = length(price)
cbind(coef,sterror,df)
coef + c(-1,1)*sterror*qt(0.975, df)

# Test that beta_size = 50 against beta_size not = 50
coef=summary(ols)$coefficients["size",1]
sterror=summary(ols)$coefficients["size",2]
cbind(coef,sterror)
N = length(size)
t = (coef - 50)/sterror
p = 2*(1-pt(abs(t),N-2))
tcrit = qt(.975,N-2)
print("t statistic, p-value, critical value")
cbind(t, p, tcrit)

#####  11.5 JOINT HYPOTHESIS TESTS

# Figure 11.1 - does not entail data analysis

# Table 11.3 - does not entail data analysis 

# Joint significance of all coefficients
# Included in complete OLS output
# And can do the following
# $nobs is N, $ncoeff is k, $df is N-k
ols.full = lm(price ~ size+bedrooms+bathrooms+lotsize+age+monthsold)
sum.full = summary(ols.full)
F = sum.full$fstatistic
k = sum.full$df[1]
df = sum.full$df[2]
critval = qf(.95,k-1,df)
pval = 1 - pf(F,k-1,df)
cbind(F[1], pval[1], critval)

# Joint test of zero coeffs for bedrooms bathrooms lotsize age monthsold
library(car)
linearHypothesis(ols.full,c("bedrooms=0", "bathrooms=0", "lotsize",
      "age=0", "monthsold=0"))

#### 11.6 F STATISTIC UNDER ASSUMPTIONS 1-4

# Summary after lm saves a number of quantitites
# $sigma is the root mean squared error (RMSE) = ResSS/(n-k)
# $r.squared is R2, adj.r.squared is adjusted R2, $fstatistic is F statisic
# $df saves three things: (k, N-k, k*) where k is effective number of parameters
# and k*>=k is the number of regressors including possibly nonidentified 
# regressors if there is perfect collinearity
# so k = $df[1] and df = N-k = $df[2]

sum.full = summary(ols.full)

# Compute adjusted R-squared
# $nobs is N, $ncoeff is k, $df is N-k
# Adjusted R-squared
k = sum.full$df[1]
df = sum.full$df[2]
rsq = sum.full$r.squared
s = sum.full$sigma
cbind(k,df,rsq,s)
# Since s^2 = ResSS/(N-k) we have ResSS = (N-k)*s^2
ResSS = df*s^2
# Since Rsq = 1 - (ResSS / TotSS) use TotSS = ResSS / (1 - Rsq)
TotSS = ResSS / (1 - rsq)
# And ExpSS = TotSS - ResSS
ExpSS = TotSS - ResSS
cbind(ResSS, ExpSS, TotSS)
Foverall = (ExpSS/(k-1)) / (ResSS/df)
critval = qf(.95,k-1,df)
pval = 1 - pf(Foverall[1],k-1,df)
cbind(Foverall[1], pval[1], critval)

# Subset test where drop bedrooms bathrooms lotsize age monthsold
# Unrestricted model
ols.unrest = lm(price ~ size+bedrooms+bathrooms+lotsize+age+monthsold)
sum.unrest = summary(ols.unrest)
k_u = sum.unrest$df[1]
df_u = sum.unrest$df[2]
s_u = sum.unrest$sigma
ResSS_u = df_u*s_u^2
# Restricted model
ols.rest = lm(price ~ size) 
sum.rest = summary(ols.rest)
k_r = sum.rest$df[1]
df_r = sum.rest$df[2]
s_r = sum.rest$sigma
ResSS_r = df_r*s_r^2
q = k_u - k_r
Fstat = ((ResSS_r-ResSS_u)/q) / (ResSS_u/df_u)
critval = qf(.95,q,df_u)
pval = 1 - pf(Fstat[1],q,df_u)
cbind(Fstat[1], pval[1], critval)

#### 11.7 PRESENTATION OF REGRESSION RESULTS


# The following combines output from two models in a single table
# It uses packages jtools which also needs huxtable for tables
library(jtools)
library(huxtable)

# The two models
ols.full = lm(price ~ size+bedrooms+bathrooms+lotsize+age+monthsold)
summary(ols.full)
ols.small = lm(price ~ size)
summary(ols.small)

# The following uses default standard errors
# For heteroskedastic-robust standard errors add  , robust = "HC1"

# Default includes standard errors
export_summs(ols.full, ols.small, scale = TRUE)
# This gives t-statistics
export_summs(ols.full, ols.small, scale = TRUE, 
             error_format = "({statistic})")
# This gives t-statistics and p-values
export_summs(ols.full, ols.small, scale = TRUE, 
    error_format = "({statistic}, p = {p.value})")
# This gives 95% confidence interval
export_summs(ols.full, ols.small, scale = TRUE,
             error_format = "[{conf.low}, {conf.high}]")
# And write to a text file - requires 'officer' package
# export_summs(ols.full, ols.small, scale = TRUE, to.file = "docx", file.name = "tables.docx")
# And can also write PDF ("PDF"), HTML ("HTML") or Excel ("xlsx").

########## ANALYSIS COMPLETE ##########

cat("\n", rep("=", 70), "\n")
cat("ANALYSIS COMPLETE\n")
cat(rep("=", 70), "\n")
cat("\nFigures saved to:", images_dir, "\n")
cat("Tables saved to:", tables_dir, "\n")

# Detach database
detach(data.HOUSE)
