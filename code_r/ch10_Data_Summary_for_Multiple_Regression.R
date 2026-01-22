# ch10_Data_Summary_for_Multiple_Regression.R - January 2026 For R
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
if (!require("sandwich")) install.packages("sandwich")
if (!require("jtools")) install.packages("jtools")
if (!require("huxtable")) install.packages("huxtable")
library(haven)
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
    
# This R program covers Chapter 10 of "Analysis of Economics Data"
#  10.1 EXAMPLE: HOUSE PRICE AND CHARACTERISTICS
#  10.2 TWO-WAY SCATTERPLOTS
#  10.3 CORRELATION
#  10.4 REGRESSION LINE
#  10.5 ESTIMATED PARTIAL EFFECTS 
#  10.6 MODEL FIT
#  10.7 COMPUTER OUTPUT FOLLOWING MULTIPLE REGRESSION
#  10.8 INESTIMABLE MODELS

############# DATA DESCRIPTION

# House sale price for 29 houses in Central Davis in 1999
#     29 observations on 9 variables 

####  10.1 EXAMPLE: HOUSE PRICE AND CHARACTERISTICS

# Read in the Stata data set from GitHub
data.HOUSE = load_data("AED_HOUSE.DTA")

# Allow variables in database to be accessed simply by giving names
attach(data.HOUSE)

# Summarize the data set
summary(data.HOUSE)

# Table 10.1
table101vars = c("price", "size", "bedrooms", "bathrooms", "lotsize",
      "age", "monthsold")
summary(data.HOUSE[table101vars])

# Table 10.2
data.HOUSE

# Regression with and without control
ols.onereg = lm(price ~ bedrooms)
summary(ols.onereg)
ols.tworeg = lm(price ~ bedrooms+size)
summary(ols.tworeg)

####  10.2 TWO-WAY SCATTERPLOTS

# Figure 10.1
pairs(~price+size+bedrooms+age,
   main="Simple Scatterplot Matrix")

####  10.3 CORRELATION

# Table 10.3
cor(cbind(price, size, bedrooms, bathrooms, lotsize, age, monthsold))

####  10.4 REGRESSION LINE

# Multivariate regression
ols.full = lm(price ~ size+bedrooms+bathrooms+lotsize+age+monthsold)
summary(ols.full)

# Nicer output
library(jtools)
summ(ols.full, digits=3)
summ(ols.full, digits=3, confint='TRUE')

# Demonstrate that can get from bivariate regression on a residual
ols.size = lm(size ~ bedrooms+bathrooms+lotsize+age+monthsold)
resid.size = resid(ols.size)
ols.biv = lm(price ~ resid.size)
summary(ols.biv)

####  10.6 MODEL FIT

# Summary after lm saves a number of quantitites
# $sigma is the root mean squared error (RMSE) = ResSS/(n-k)
# $r.squared is R2, adj.r.squared is adjusted R2, fstatistic is F statisic
# $df saves three things: (k, N-k, k*) where k is effective number of parameters
# and k*>=k is the number of regressors including possibly nonidentified 
# regressors if there is perfect collinearity
# so k = $df[1] and df = N-k = $df[2]

# R-squared is squared correlation between yhat and y
sum.full = summary(ols.full)
sum.full$r.squared
pprice = predict(ols.full)
summary(cbind(price,pprice))
cor = cor(cbind(price,pprice))[2,1]
cor^2
    
# Compute adjusted R-squared
# $nobs is N, $ncoeff is k, $df is N-k 
# Adjusted R-squared 
k = sum.full$df[1]
df = sum.full$df[2]
r2 = sum.full$r.squared
r2adj = r2 - ((k-1)/df)*(1-r2)
r2adj
sum.full$adj.r.squared

# Compute AIC and BIC manually
N = df + k
resSS = df*sum.full$sigma^2
# AIC as computed by many packages including Stata
aic = N*log(resSS/N) + N*(1+log(2*3.1415927)) + 2*k
aic
# AIC as computed by R drops the second term
aic_R = N*log(resSS/N) + 2*k
aic_R
extractAIC(ols.full)   # From summary(lm) output
# BIC as computed by many packages including Stata
bic = N*log(resSS/N) + N*(1+log(2*3.1415927)) + k*log(N)
bic

####  10.7 COMPUTER OUTPUT FOLLOWING REGRESSION

# The following combines output from two models in a single table
# It uses packages jtools which also needs huxtable for tables
library(huxtable)

# The two models
ols.full = lm(price ~ size+bedrooms+bathrooms+lotsize+age+monthsold)
summary(ols.full)
ols.small = lm(price ~ size)
summary(ols.small)

# Default includes standard errors
export_summs(ols.full, ols.onereg, scale = TRUE)
# This gives t-statistics
export_summs(ols.full, ols.onereg, scale = TRUE, 
             error_format = "({statistic})")
# This gives t-statistics and p-values
export_summs(ols.full, ols.onereg, scale = TRUE, 
    error_format = "({statistic}, p = {p.value})")
# This gives 95% confidence interval
export_summs(ols.full, ols.onereg, scale = TRUE,
             error_format = "[{conf.low}, {conf.high}]")
# And write to a text file - requires 'officer' package
# export_summs(ols.full, ols.small, scale = TRUE, to.file = "docx", file.name = "tables.docx")
# And can also write PDF ("PDF"), HTML ("HTML") or Excel ("xlsx").

####  10.8 INESTIMABLE MODELS

########## CLOSE OUTPUT

cat("\n", rep("=", 70), "\n")
cat("Chapter 10 analysis complete.\n")
cat(rep("=", 70), "\n")
