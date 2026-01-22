# ch06_The_Least_Squares_Estimator.R
# Updated for online execution portability

########## OVERVIEW ##########

# R Program
# copyright C 2021 by A. Colin Cameron
# Used for "Analysis of Economics Data: AN Introduction to Econometrics"
# by A. Colin Cameron (2021)

# To run you need file
#   AED_GENERATEDDATA.DTA
#   AED_GENERATEDREGRESSION.DTA
#   AED_CENSUSREGRESSIONS.DTA
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

# This R program covers Chapter 6 of "Analysis of Economics Data"
#  6.1 POPULATION AND SAMPLE
#  6.2 EXAMPLES OF SAMPLING FROM A POPULATION
#  6.3 PROPERTIES OF THE LEAST SQUARES ESTIMATOR
#  6.4 ESTIMATORS OF MODEL PARAMETERS

########## DATA DESCRIPTION

# Two datasets are generated
# The third comes from analysis of the 1880 U.S. Census

####  6.1 POPULATION AND SAMPLE

# Figure 6.1 for error versus residual - uses no data

####  6.2 EXAMPLES OF SAMPLING FROM A POPULATION

# Read in the Stata data set
data.GENERATEDDATA = load_data("AED_GENERATEDDATA.DTA")

# Allow variables in database to be accessed simply by giving names
attach(data.GENERATEDDATA)

# Summarize the data set
summary(data.GENERATEDDATA)

# Table 6.1
head(data.GENERATEDDATA)

# Figure 6.2: panel A
olsEyx <- lm(Eygivenx ~ x)
summary(olsEyx)
plot(x, y, xlab="Regressor x", ylab="Dependent variable y", pch=19, main="Population line E[y|x]=1+2x")
abline(olsEyx)
legend(1.5, 8, c("Actual",  "Fitted"), lty=c(-1,1), pch=c(19,-1), bty="o")

# Way to directly write Figure 6.2 panel A to file
png(file.path(images_dir, "ch06_fig2_population.png"), width=800, height=600)
plot(x, y, xlab="Regressor x", ylab="Dependent variable y", pch=19, main="Population line E[y|x]=1+2x")
abline(olsEyx)
legend(1.5, 8, c("Actual",  "Fitted"), lty=c(-1,1), pch=c(19,-1), bty="o")
dev.off()

# Figure 6.2: panel B
olsyx <- lm(y ~ x)
summary(olsyx)
plot(x, y, xlab="Regressor x", ylab="Dependent variable y",pch=19, main = "Regression line yhat=2.81+1.05x" )
abline(olsyx)
legend(1.5, 8, c("Actual",  "Fitted"), lty=c(-1,1), pch=c(19,-1), bty="o")

# Three regressions from the same model
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
set.seed(12345)
u = runif(30,min=0,max=1)
x1 = rnorm(30,3,1)
u1 = rnorm(30,0,2)
y1 = 1 + 2*x1 + u1
x2 = rnorm(30,3,1)
u2 = rnorm(30,0,2)
y2 = 1 + 2*x2 + u2
x3 = rnorm(30,3,1)
u3 = rnorm(30,0,2)
y3 = 1 + 2*x3 + u3
ols1 <- lm(y1 ~ x1)
summary(ols1)
ols2 <- lm(y2 ~ x2)
summary(ols2)
ols3 <- lm(y3 ~ x3)
summary(ols3)

# Figure 6.3 - three panels
plot(x1, y1, pch=19, main = "Sample 1" )
abline(ols1)
plot(x2, y2, pch=19, main = "Sample 2" )
abline(ols2)
plot(x3, y3, pch=19, main = "Sample 3" )
abline(ols3)

# Generated data: results of regression on 400 samples of size 30
github_data_url <- "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/"
images_dir <- "images"
data.GENERATEDREGRESSIONS = load_data("AED_GENERATEDREGRESSIONS.DTA")
attach(data.GENERATEDREGRESSIONS)
summary(data.GENERATEDREGRESSIONS)
head(data.GENERATEDREGRESSIONS)

# Figure 6.4: Panel A
hist(slope, freq=FALSE, xlab="slope", main="Generated data: 400 slopes")
lines(density(slope))

# Figure 6.4: Panel B
hist(intercept, prob=TRUE, xlab="intercept", main="Generated data: 400 intercepts")
lines(density(intercept))

# Census data: results of regression on 400 samples of size 120
data.CENSUSREGRESSIONS = load_data("AED_CENSUSREGRESSIONS.DTA")
attach(data.CENSUSREGRESSIONS)
summary(data.CENSUSREGRESSIONS)
head(data.CENSUSREGRESSIONS)

# Figure 6.5: Panel A
hist(slope, freq=FALSE, xlab="slope", main="Census data: 400 slopes")
lines(density(slope))

# Figure 6.5: Panel B
hist(intercept, prob=TRUE, xlab="intercept", main="Census data: 400 intercepts")
lines(density(intercept))

########## CLOSE OUTPUT

cat("Chapter 6 analysis complete.\n")
