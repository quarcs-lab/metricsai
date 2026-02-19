# ch05_Bivariate_Data_Summary.R
# Updated for online execution portability

########## OVERVIEW ##########

# R Program
# copyright C 2021 by A. Colin Cameron
# Used for "Analysis of Economics Data: AN Introduction to Econometrics"
# by A. Colin Cameron (2021)

# To run you need file
#   AED_HOUSE.DTA
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
if (!require("KernSmooth")) install.packages("KernSmooth")
library(haven)
library(KernSmooth)

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

# This R program covers Chapter 5 of "Analysis of Economics Data"
#  5.1 EXAMPLE: HOUSE PRICE AND SIZE
#  5.2 TWO-WAY TABULATION
#  5.3 TWOWAY SCATTER PLOT
#  5.4 SAMPLE CORRELATION
#  5.5 REGRESSION LINE
#  5.6 MEASURES OF MODEL FIT
#  5.7 COMPUTER OUTPUT FOLLOWING REGRESSION
#  5.8 PREDICTION AND OUTLYING OBSERVATIONS
#  5.9 REGRESSION AND CORRELATION
#  5.10 CAUSATION
#  5.11 NONPARAMETRIC REGRESSION

########## DATA DESCRIPTION

# House sale price for 29 houses in Central Davis in 1999
#     29 observations on 9 variables

####  5.1 EXAMPLE: HOUSE PRICE AND SIZE

# Read in the Stata data set
data.HOUSE = load_data("AED_HOUSE.DTA")

# Allow variables in database to be accessed simply by giving names
attach(data.HOUSE)

# Summarize the data set
summary(data.HOUSE)

# Table 5.1
data.HOUSE

# Table 5.2
summary(price)
quantile(price)
mean(price)

summary(size)
quantile(size)
mean(size)

#### 5.2 TWO-WAY TABULATION

# Create categorical variables
pricerange = price
pricerange = ifelse(price<249999, 1, 2)

sizerange = size
for (i in 1:length(sizerange)) {
    if (size[i] >= 2400) {
        sizerange[i] = 3
    }
    else if ((size[i] >= 1800)&(size[i] <= 2399)) {
        sizerange[i] = 2
    }
    else {
        sizerange[i] = 1
    }
}
# Table 5.3
table(pricerange,sizerange)

# Table 5.4 - with expected frequencies
table(pricerange,sizerange)

####  5.3 TWOWAY SCATTER PLOT

# Figure 5.1 First panel
plot(size, price, xlab="House size in square feet", ylab="House sale price in dollars", pch=19)

# Way to directly write Figure 5.1 first panel to file
png(file.path(images_dir, "ch05_fig1_scatter.png"), width=800, height=600)
plot(size, price, xlab="House size in square feet", ylab="House sale price in dollars", pch=19)
dev.off()

####  5.4 CORRELATION

# Figure 5.1 Second panel
plot(size, price, xlab="House size in square feet", ylab="House sale price in dollars", pch=19)
abline(253910, 0)
abline(v = 1883)

# Covariance
cov(data.HOUSE[,1:2])
cov(price,size)

# Correlation coefficient
cor(data.HOUSE[,1:2])

# Plot of four cases of correlation using generated data
# Clear the workspace
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

# Set the seed number
set.seed(12345)

# Generate random data
x = rnorm(30,3,1)
u1 = rnorm(30,0,0.8)
y1 = 3 + x +u1
u2 = rnorm(30,0,2)
y2 = 3 + x + u2
y3 = 5 + u2
y4 = 10 - x - u2

cor(cbind(x,y1,y2,y3,y4))

# Figure 5.2 - four separate panels
github_data_url <- "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/"
images_dir <- "images"

plot(x,y1,pch=19)
legend(3.6,5.5, "r=.78", box.lwd=0)

plot(x,y2,pch=19)
legend(3.6,4.5, "r=.54", box.lwd=0)

plot(x,y3,pch=19)
legend(3.6,4.2, "r=.07", box.lwd=0)

plot(x,y4,pch=19)
legend(3.6,12, "r=-.54", box.lwd=0)

# Figure 5.2 - panels combined
png(file.path(images_dir, "ch05_fig2_correlation.png"), width=1200, height=800)
par(mfrow=c(2,2))
plot(x,y1,pch=19)
legend(3.6,5.5, "r=.78", box.lwd=0)
plot(x,y2,pch=19)
legend(3.6,4.5, "r=.54", box.lwd=0)
plot(x,y3,pch=19)
legend(3.6,4.3, "r=.07", box.lwd=0)
plot(x,y4,pch=19)
legend(3.6,12, "r=-.54", box.lwd=0)
par(mfrow = c(1,1))
dev.off()

####  5.5 REGRESSION

# Return to house price data
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
data.HOUSE = load_data("AED_HOUSE.DTA")
attach(data.HOUSE)

# Linear regression
ols = lm(price~size)
summary(ols)

# Figure 5.3
# Illustration created by a word processor.

# Figure 5.4
plot(size,price, xlab="House size in square feet", ylab="House sale price in dollars",pch=19)
abline(ols)
legend(2400, 270000, c("Actual",  "Fitted"), lty=c(-1,1), pch=c(19,-1), bty="o")

# Intercept-only regression compared to the sample mean
ols.1 = lm(price~1)
summary(ols.1)
mean(price)

####  5.6 MEASURES OF MODEL FIT

# Clear the workspace
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

x = 1:5

# Generate random data
set.seed(123456)
epsilon = rnorm(5,0,2)
y = 1 + 2*x + epsilon
cbind(x, epsilon, y)
summary(y)
ols.2 = lm(y~x)
summary(ols.2)
py = predict(ols.2)
resid = y - py    # ALTERNATIVELY resid = resid(ols.2)
cbind(x, epsilon, y, py, resid)

# Figure 5.5 - Panels A and B
plot(x,y,pch=17)
abline(8.017, 0)

plot(x,py,pch=19)
abline(8.017, 0)

####  5.7 COMPUTER OUTPUT FOLLOWING OLS REGRESSION

# Nothing

####  5.8 PREDICTION AND OUTLYING OBSERVATIONS

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
data.HOUSE = load_data("AED_HOUSE.DTA")
attach(data.HOUSE)

ols = lm(price~size)
predict(ols, data.frame(size = 2000))

####  5.9 REGRESSION AND CORRELATION

# Nothing

####  5.10 CAUSATION

attach(data.HOUSE)

# Reverse regression
reverse = lm(size~price)
summary(reverse)

####  5.11 COMPUTATIONS FOR CORRELATION AND REGRESSION

# Create artificial data
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
x = 1:5
y = c(1,2,2,2,3)
cbind(x,y)

# Hand calculations - see text

# Check hand calculations
ols.3 = lm(y~x)
summary(ols.3)

cor(cbind(x,y)[,1:2])
cor(x,y)^2

# Figure 5.5
plot(x,y, xlab="x", ylab="y", pch=19)
abline(ols.3)
legend(1.0, 3.0, c("Actual",  "Fitted"), lty=c(-1,1), pch=c(19,-1), bty="o")

####  5.12 NONPARAMETRIC REGRESSION

github_data_url <- "https://raw.githubusercontent.com/quarcs-lab/data-open/master/AED/"
data.HOUSE = load_data("AED_HOUSE.DTA")
attach(data.HOUSE)

ols = lm(price~size)
summary(ols)

# Solid line is OLS
# Dotted line is Lowess
# Dashed line is local constant with normal kernel
plot(size,price, xlab="House size in sq. feet", ylab="House sale price in $",pch=19)
abline(ols)
lines(lowess(size,price), lty=3)
lines(ksmooth(size,price, "normal", bandwidth = 1000), lty=2)

# For local linear use kernsmooth package and locpoly command
plot(size,price, xlab="House size in sq. feet", ylab="House sale price in $",pch=19)
abline(ols)
lines(lowess(size,price), lty=3)
lines(locpoly(size, price, bandwidth = 2000, kernel="epan"), lty=2)

########## CLOSE OUTPUT

cat("Chapter 5 analysis complete.\n")
