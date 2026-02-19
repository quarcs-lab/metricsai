# ch09_Models_with_Natural_Logarithms.R
# Updated for online execution portability

########## OVERVIEW ##########

# R Program
# copyright C 2021 by A. Colin Cameron
# Used for "Analysis of Economics Data: An Introduction to Econometrics"
# by A. Colin Cameron (2021)

# To run you need file
#   AED_EARNINGS.DTA
#   AED_SP500INDEX.DTA
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
if (!require("jtools")) install.packages("jtools")
library(haven)
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

##########

# This R program does analysis for Chapter 9
#  9.1 NATURAL LOGARITHM FUNCTION
#  9.2 SEMI-ELASTICITIS AND ELASTICITIES
#  9.3 LOG-LINEAR, LOG-LOG AND LINEAR-LOG MODELS
#  9.4 EXAMPLE: EARNINGS AND EDUCATION
#  9.5 FURTHER USES OF THE NATURAL LOGARITHM
#  9.6 EXPONENTIAL FUNCTION

####  9.1 NATURAL LOGARITHM FUNCTION

# Table 9.1 - does not involve data analysis

####  9.2 SEMI-ELASTICITIS AND ELASTICITIES

####  9.3 LOG-LINEAR, LOG-LOG AND LINEAR-LOG MODELS

####  9.4 EXAMPLE: EARNINGS AND EDUCATION

# Read in the Stata data set
data.EARNINGS = load_data("AED_EARNINGS.DTA")

# Allow variables in database to be accessed simply by giving names
attach(data.EARNINGS)

# Summarize the data set
summary(data.EARNINGS)
head(data.EARNINGS)

# Create variables and add to data frame
lnearn = log(earnings)
data.EARNINGS$lnearn = lnearn
lneduc = log(education)
data.EARNINGS$lneduc = lneduc

# Table 9.2
table92vars = c("earnings", "lnearn", "education", "lneduc")
summary(data.EARNINGS[table92vars])

# Table 9.3
# Linear model
ols.linear <- lm(earnings ~ education)
summary(ols.linear)
# Nicer output
summ(ols.linear, digits=3)

# Log-linear Model
ols.loglin <- lm(lnearn ~ education)
summary(ols.loglin)
# Nicer output
summ(ols.loglin, digits=3)

# Log-log Model
ols.loglog <- lm(lnearn ~ lneduc)
summary(ols.loglog)
# Nicer output
summ(ols.loglog, digits=3)

# Linear-log Model
ols.linlog <- lm(earnings ~ lneduc)
summary(ols.linlog)
# Nicer output
summ(ols.linlog, digits=3)

# Figure 9.1 - first panel
plot(education,earnings, xlab="Years of completed schooling",
    ylab="Annual earnings(in dollars)",pch=19,main="Linear Model")
abline(ols.linear)
legend(5, 150000, c("Actual",  "Fitted"), lty=c(-1,1), pch=c(19,-1), bty="o")

# Figure 9.1 - second panel
plot(education,lnearn, xlab="Years of completed schooling",
    ylab="Log annual earnings",pch=19,main="Log-linear Model")
abline(ols.loglin)
legend(5, 12, c("Actual",  "Fitted"), lty=c(-1,1), pch=c(19,-1), bty="o")

png(file.path(images_dir, "ch09_fig1_earnings_education.png"), width=1200, height=600)
par(mfrow=c(1,2))
plot(education,earnings, xlab="Years of completed schooling",
    ylab="Annual earnings(in dollars)",pch=19,main="Linear Model")
abline(ols.linear)
legend(5, 150000, c("Actual",  "Fitted"), lty=c(-1,1), pch=c(19,-1), bty="o")
plot(education,lnearn, xlab="Years of completed schooling",
    ylab="Log annual earnings",pch=19,main="Log-linear Model")
abline(ols.loglin)
legend(5, 12, c("Actual",  "Fitted"), lty=c(-1,1), pch=c(19,-1), bty="o")
par(mfrow=c(1,1))
dev.off()

####  9.5 FURTHER USES OF THE NATURAL LOGARITHM

# Table 9.4 - does not entail data analysis

# Table 9.5 - does not entail data analysis

# Read in the Stata data set
rm(list=ls())
github_data_url <- "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/"
images_dir <- "images"
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
data.SP500INDEX = load_data("AED_SP500INDEX.DTA")
attach(data.SP500INDEX)
summary(data.SP500INDEX)
head(data.SP500INDEX)

# To predict exponential growth in the graph in levels
ols.logs <- lm(lnsp500 ~ year)
summary(ols.logs)
plnsp500 = predict(ols.logs)
# Correct for retransformation bias - see chapter 15.6
# First need rmse^2 the square of the root mean squared error
# Code here uses knowledge that k = 2
ResSS = c(crossprod(ols.logs$residuals))
MSE = ResSS / (length(ols.logs$residuals) - 2)
sqrt(MSE)
psp500 = exp(plnsp500)*exp(MSE/2)
MSE

## Figure 9.2 - first panel
plot(year, sp500, xlab="Year", ylab="S&P 500 Index", type="l",lty=1,
     main="Exponential trend in levels")
points(year, psp500, type="l",lty=2)

## Figure 9.2 - second panel
plot(year, lnsp500, xlab="Year", ylab="S&P 500 Index", type="l",lty=1,
     main="Linear trend in natural logarithms")
points(year, plnsp500, type="l",lty=2)

####  9.6 EXPONENTIAL FUNCTION

########## CLOSE OUTPUT

cat("Chapter 9 analysis complete.\n")
