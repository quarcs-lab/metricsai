# ch08_Case_Studies_for_Bivariate_Regression.R
# Updated for online execution portability

########## OVERVIEW ##########

# R Program
# copyright C 2021 by A. Colin Cameron
# Used for "Analysis of Economics Data: AN Introduction to Econometrics"
# by A. Colin Cameron (2021)

# To run you need file
#   AED_HEALTH2009.DTA
#   AED_CAPM.DTA
#   AED_GDPUNEMPLOY.DTA
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
if (!require("sandwich")) install.packages("sandwich")
if (!require("jtools")) install.packages("jtools")
library(haven)
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

# This R program covers Chapter 8 of "Analysis of Economics Data"
#  8.1 HEALTH OUTCOMES ACROSS COUNTRIES
#  8.2 HEALTH EXPENDITURES ACROSS COUNTRIES
#  8.3 CAPM MODEL
#  8.4 OUTPUT AND UNEMPLOYMENT IN THE U.S.

########## DATA DESCRIPTION

# Several datasets used

########## 8.1 HEALTH OUTCOMES ACROSS COUNTRIES

# Read in the Stata data set
data.HEALTH2009 = load_data("AED_HEALTH2009.DTA")
attach(data.HEALTH2009)
summary(data.HEALTH2009)
head(data.HEALTH2009)

# Table 8.1
table81vars = c("hlthpc", "lifeexp", "infmort")
summary(data.HEALTH2009[table81vars])

# Key regression
ols.lifeexp = lm(lifeexp ~ hlthpc)
summary(ols.lifeexp)

# Nicer output
summ(ols.lifeexp, digits=3, confint = TRUE)

# Figure 8.1 Panel A
plot(hlthpc, lifeexp, xlab="Health Spending per capita (in $)",
     ylab="Life Expectancy (in years)", pch=19, main="Life Expectancy")
abline(ols.lifeexp)
legend(1.5, 8, c("Actual",  "Fitted"), lty=c(-1,1), pch=c(19,-1), bty="o")

png(file.path(images_dir, "ch08_fig1_lifeexp.png"), width=800, height=600)
plot(hlthpc, lifeexp, xlab="Health Spending per capita (in $)",
     ylab="Life Expectancy (in years)", pch=19, main="Life Expectancy")
abline(ols.lifeexp)
legend(1.5, 8, c("Actual",  "Fitted"), lty=c(-1,1), pch=c(19,-1), bty="o")
dev.off()

## Infant mortality

# Key regression
ols.infmort = lm(infmort ~ hlthpc)
summary(ols.infmort)

# Nicer output
summ(ols.infmort, digits=3, confint = TRUE)

# Figure 8.2 Panel B
plot(hlthpc, infmort, xlab="Health Spending per capita (in $)",
     ylab="Infant Mortality per 100 births", pch=19, main="Infant Mortality")
abline(ols.infmort)
legend(1.5, 8, c("Actual",  "Fitted"), lty=c(-1,1), pch=c(19,-1), bty="o")

# Heteroscedastic-robust standard errors
summ(ols.lifeexp, digits=3, robust = "HC1")
summ(ols.infmort, digits=3, confint = TRUE, robust = "HC1")

############ 8.2 HEALTH EXPENDITURES ACROSS COUNTRIES

# Same data as preceding

# Table 8.2
table82vars = c("gdppc", "hlthpc")
summary(data.HEALTH2009[table82vars])

# Key regression
ols.hlthpc = lm(hlthpc ~ gdppc)
summary(ols.hlthpc)

# Nicer output
summ(ols.hlthpc, digits=3, confint = TRUE)

# Figure 8.2 Panel A
plot(gdppc, hlthpc, xlab="GDP per capita (in $)",
     ylab="Health Spending per capita (in $)", pch=19, main="Linear Model")
abline(ols.hlthpc)
legend(1.5, 8, c("Actual",  "Fitted"), lty=c(-1,1), pch=c(19,-1), bty="o")

# Drop USA and Luxembourg for Figure 8.2
# This works for summary statistic
with(data.HEALTH2009[(data.HEALTH2009$code!="LUX") & (data.HEALTH2009$code!="USA"),],
    summary(hlthpc) )

# Figure 8.2 Panel B - I can get scatterplot but do not have line
with(data.HEALTH2009[(data.HEALTH2009$code!="LUX") & (data.HEALTH2009$code!="USA"),],
     plot(gdppc, hlthpc, xlab="GDP per capita (in $)",
     ylab="Health Spending per capita (in $)", pch=19, main="Drop USA and Luxembourg") )

# Heteroskedastic-robust standard errors
summ(ols.hlthpc, digits=3, robust = "HC1")
summ(ols.hlthpc, digits=3, confint = TRUE, robust = "HC1")

#########  8.3 CAPM MODEL

# Read in the data
rm(list=ls())
github_data_url <- "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/"
images_dir <- "images"
data.CAPM = load_data("AED_CAPM.DTA")
attach(data.CAPM)
summary(data.CAPM)
head(data.CAPM)

# Date begins with month 280 in may 1983

# Table 8.3
table83vars = c("rm", "rf", "rko", "rtgt", "rwmt", "rm_rf",
    "rko_rf", "rtgt_rf", "rwmt_rf")
summary(data.CAPM[table83vars])

# Figure 8.3 panel A
# for readability use only the last 20% of data in the first panel
# This begins with observation 285 which is monthly date = 565
with(data.CAPM[date>=565,],
    plot(date, rko_rf, xlab="Month", ylab="Excess returns",
    main="Excess returns over time", type="l", lty=1))
points(date, rm_rf, type="l", lty=2)

# Key regression
ols.capm = lm(rko_rf ~ rm_rf)
summary(ols.capm)
# Nicer output
summ(ols.capm, digits=4)

# Figure 8.3 Panel B
plot(rm_rf, rko_rf, xlab="Market excess return",
    ylab="Coca Cola excess return", pch=19, main="Coca Cola versus Market")
abline(ols.capm)
legend(1.5, 8, c("Actual",  "Fitted"), lty=c(-1,1), pch=c(19,-1), bty="o")

# Heteroscedastic-robust standard errors
summ(ols.capm, digits=3, robust = "HC1")

########## 8.4 OUTPUT AND UNEMPLOYMENT IN THE U.S.

# Read in the data
rm(list=ls())
github_data_url <- "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/"
images_dir <- "images"
data.GDPUNEMPLOY = load_data("AED_GDPUNEMPLOY.DTA")
attach(data.GDPUNEMPLOY)
summary(data.GDPUNEMPLOY)
head(data.GDPUNEMPLOY)

# Table 8.4
table84vars = c("rgdpgrowth", "uratechange")
summary(data.GDPUNEMPLOY[table84vars])

# Key regression
ols.okun = lm(rgdpgrowth ~ uratechange)
summary(ols.okun)
# Nicer output
summ(ols.okun, digits=3)

# Figure 8.4 Panel A
plot(uratechange, rgdpgrowth, xlab="Change in unemployment rate",
     ylab="Percentage change in real GDP", pch=19, main="Scatterplot of data")
abline(ols.okun)
legend(1.5, 8, c("Actual",  "Fitted"), lty=c(-1,1), pch=c(19,-1), bty="o")

# Get predictions
pgrowth = predict(ols.okun)

# Figure 8.4 Panel B
plot(year, rgdpgrowth, xlab="Year", ylab="Percentage change in real GDP",
          main="Real GDP Change over Time", type="l", lty=1)
points(year, pgrowth, type="l", lty=2)

# Heteroscedastic-robust standard errors
summ(ols.okun, digits=3, robust = "HC1")

########## CLOSE OUTPUT

cat("Chapter 8 analysis complete.\n")
