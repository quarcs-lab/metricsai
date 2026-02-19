# ch02_Univariate_Data_Summary.R
# Updated for online execution portability

########## OVERVIEW ##########

# R Program
# copyright C 2021 by A. Colin Cameron
# Used for "Analysis of Economics Data: AN Introduction to Econometrics"
# by A. Colin Cameron (2021)

# To run you need file
#   AED_EARNINGS.DTA
#   AED_REALGDPPC.DTA
#   AED_HEALTHCATEGORIES.DTA
#   AED_FISHING.DTA
#   AED_MONTHLYHOMESALES.DTA
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
if (!require("moments")) install.packages("moments")
library(haven)
library(moments)

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

# This R program covers Chapter 2 of "Analysis of Economics Data"
#   2.1 SUMMARY STATISTICS FOR NUMERICAL DATA
#   2.2 CHARTS FOR NUMERICAL DATA
#   2.3 CHARTS FOR NUMERICAL DATA BY CATEGORY
#   2.4 SUMMARY AND CHARTS FOR CATEGORICAL DATA
#   2.5 DATA TRANSFORMATION
#   2.6 DATA TRANSFORMATION FOR TIME SERIES DATA

####  2.1 SUMMARY STATISTICS FOR NUMERICAL DATA

# Read in the Stata data set
data.EARNINGS = load_data("AED_EARNINGS.DTA")

# Allow variables in database to be accessed simply by giving names
attach(data.EARNINGS)

# Summarize the data set
summary(data.EARNINGS)

# Table 2.1
summary(earnings)
quantile(earnings)
mean(earnings)

# Skewness and kurtosis
skewness(earnings)
kurtosis(earnings)

# Figure 2.1 - skip as lengthy code

# Figure 2.2
boxplot(earnings,xlab="Annual earnings (in dollars)",pch=19)

# Way to directly write Figure 2.2 to file
png(file.path(images_dir, "ch02_fig2_boxplot.png"), width=800, height=600)
boxplot(earnings,xlab="Annual earnings (in dollars)",pch=19)
dev.off()

# Figure 2.3 - skip as lengthy code

#### 2.2  CHARTS FOR NUMERICAL DATA

# Table 2.2
summary(earnings)
earningsrange = 15000*floor(earnings/15000)
summary(earningsrange)
table(earningsrange)

# Figure 2.4
# Similar to text but not exact
# 13 bins of width 13500
hist(earnings,breaks=c(13500*0:13))
# Narrower bin width - 23 bins of width 7500
hist(earnings,breaks=c(7500*0:23))

# Figure 2.5
# Default kernel density estiamte in R
kdensity = density(earnings)
plot(kdensity)
# Select kernel and band width
kdensity = density(earnings,kernel=c("epanechnikov"),bw=11000)
plot(kdensity)

# Read in data for Figure 2.6
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
data.REALGDPPC = load_data("AED_REALGDPPC.DTA")
attach(data.REALGDPPC)
summary(data.REALGDPPC)

# Figure 2.6 - requires special Stata format command for horizontal axis
# R understates quarterly dates in daten
plot(daten, realgdppc, xlab="Year", ylab="Real GDP in 2012$", type="l")

#### 2.3  CHARTS FOR NUMERICAL DATA BY CATEGORY

# Read in data for Figure 2.7
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
data.HEALTHCATEGORIES = load_data("AED_HEALTHCATEGORIES.DTA")
attach(data.HEALTHCATEGORIES)
summary(data.HEALTHCATEGORIES)

# Table 2.3
data.HEALTHCATEGORIES

# Figure 2.7
barplot(as.vector(data.HEALTHCATEGORIES$expenditures),names.arg=data.HEALTHCATEGORIES$category,las=2,ylab="Expenditures in $billions")

png(file.path(images_dir, "ch02_fig7_barplot.png"), width=800, height=600)
barplot(as.vector(data.HEALTHCATEGORIES$expenditures),names.arg=data.HEALTHCATEGORIES$category,las=2,ylab="Expenditures in $billions")
dev.off()

# Figure 2.8 - more complicated as uses Stata spatial data commands

#### 2.4 SUMMARY AND CHARTS FOR CATEGORICAL DATA

# Read in data for Figure 2.9
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
data.FISHING = load_data("AED_FISHING.DTA")
attach(data.FISHING)
summary(data.FISHING)

# Table 2.4
freq = table(mode)
relfreq = table(mode) / nrow(data.FISHING)
relfreq
cbind(freq,relfreq)

# Figure 2.9
lbls = c("beach","pier","private","charter")
pct <- round(freq/sum(freq)*100)
lbls <- paste(lbls, pct) # add percents to labels
pie(freq,labels=lbls)

png(file.path(images_dir, "ch02_fig9_pie.png"), width=800, height=600)
pie(freq,labels=lbls)
dev.off()

#### 2.5 DATA TRANSFORMATION

# Read in data for Figure 2.10
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
data.EARNINGS = load_data("AED_EARNINGS.DTA")
attach(data.EARNINGS)
summary(data.EARNINGS)

lnearns = log(earnings)

# Figure 2.10
hist(earnings)
hist(lnearns)

# Following combines into one graph
png(file.path(images_dir, "ch02_fig10_histograms.png"), width=1200, height=600)
par(mfrow=c(1,2))
hist(earnings)
hist(lnearns)
par(mfrow=c(1,1))
dev.off()

#### 2.6 DATA TRANSFORMATIONS FOR TIME SERIES DATA

# Read in data for Figure 2.11
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
data.MONTHLYHOMESALES = load_data("AED_MONTHLYHOMESALES.DTA")
attach(data.MONTHLYHOMESALES)
summary(data.MONTHLYHOMESALES)

newdata <- data.MONTHLYHOMESALES[which(data.MONTHLYHOMESALES$year>=2005),]
summary(newdata)

# Figure 2.11 - Panel A
plot(daten, exsales, xlab="Year", ylab="Monthly Home Sales", type="l")
points(daten, exsales_ma11, type="l",lty=2)

# Figure 2.11 - Panel B
plot(daten, exsales, xlab="Year", ylab="Monthly Home Sales", type="l")
points(daten, exsales_sa, type="l",lty=2)

# Read in data for Figure 2.12
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
data.REALGDPPC = load_data("AED_REALGDPPC.DTA")
attach(data.REALGDPPC)
summary(data.REALGDPPC)

# Table 2.5 data - first and last observations
head(data.REALGDPPC, n=1)
tail(data.REALGDPPC, n=1)

# Figure 2.12 - panels A and B
plot(daten, gdp, xlab="Year", ylab="GDP in $ billions", type="l",lty=1)
points(daten, realgdp, type="l",lty=2)
plot(daten, gdppc, xlab="Year", ylab="GDP in $ billions", type="l",lty=1)
points(daten, realgdppc, type="l",lty=2)

# Following combines into one graph
png(file.path(images_dir, "ch02_fig12_gdp_comparison.png"), width=1200, height=600)
par(mfrow=c(1,2))
plot(daten, gdp, xlab="Year", ylab="GDP in $ billions", type="l",lty=1)
points(daten, realgdp, type="l",lty=2)
plot(daten, gdppc, xlab="Year", ylab="GDP in $ billions", type="l",lty=1)
points(daten, realgdppc, type="l",lty=2)
par(mfrow=c(1,1))
dev.off()

########## CLOSE OUTPUT

cat("Chapter 2 analysis complete.\n")
