# Use as.Date to convert character strings to Date objects in ISO 8601 standard date
# ISO 8601 : YYYY-mm-dd, as.character will convert back to character
# %Y is full year, %y is year without leading two digits, %B is spelled out month
# format = " " is format of incoming character
# origin is used with numeric dates from excel (origin="1899-12-30")
# format(date, altered_format) is used to change the format of a Date object
# format can be used in many other ways
# To use format with dates, first argument must be date object and second is format
# In format(Date object, tz="CST") use tz=timezone
# Sys.Date(): YYYY-mm-dd and Sys.time(): YYYY-mm-dd hh:mm:ss tz

dates <- c("05/28/14", "04/12/94", "09/02/36")

betterDates <- as.Date(dates, "%m/%d/%y")
betterDates

dates <- c("05/27/84", "07/07/05", "08/17/20")
betterDates <- as.Date(dates, "%m/%d/%y")

# Simply convert to date objects
dates <- c("2010-05-01", "2004-03-15")
Exer1Dates <- as.Date(dates)

# Convert from format to standard YYYY-mm-dd (ISO 8601)
Exer2Dates <- as.Date("07/19/98", "%m/%d/%y")

# origin = converts dates from Windows Excel
# Microsoft Excel mistakenly records 1900 as a leap year
as.Date(c(31539, 31540, 31541), origin="1899-12-30")

# Convert into date objects
dates <- c("02/07/10", "02/23/10", "02/08/10", "02/14/10", "02/10/10")
Exer4Dates <- as.Date(dates, format="%m/%d/%y")

# Mean of date object (use rm.na = TRUE)
mean_date <- mean(Exer4Dates, rm.na = TRUE)

# Max of date object
max_date <- max(Exer4Dates)

# Convert into a date object
as.Date(c("10/25/2005","06/08/1971"), format="%m/%d/%Y")

# Convert date to character data
chrDates = as.character(Exer4Dates)

# Print today's date in format "%B %d %Y" (%B is full month spelled out)
format(Sys.Date(),  "%B %d %Y")

# Print today's date with time zone set to Hawaii Standard Time
format(Sys.time(), tz="MST")


