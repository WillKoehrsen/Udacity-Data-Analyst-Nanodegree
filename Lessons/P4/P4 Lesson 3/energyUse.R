library(ggplot2)
source('multiplot.R')
# Set the correct working directory
setwd('Udacity-Data-Analyst-Nanodegree/Lessons/P4 Lesson 3/')
# Read the file into a dataframe
df <-  read.csv('energy use per person.csv', header=TRUE, row.names=1)
#Get a quick summary of the first year of the data
summary(df$X1960)
#Assign the names of the countries to an atomic character vector
country_names <- row.names(df)

# Loop through the row and assign each country to an atomic numeric vector
for (number in seq(1,length(country_names),1)){
  country_name <- country_names[number]
  assign(country_name, as.numeric(df[which(row.names(df)==country_names[number]),]))
}
average_energy_use = seq(1,length(colnames(df)),1)

# Find average energy use in each year of the dataset
for (number in seq(1,length(colnames(df)),1)){
  average_energy_use[number] <- mean(df[[colnames(df)[number]]], na.rm=TRUE)
}

# Create labels for plotting
labels = seq(1960,2011,1)

# Center all titles on plots
theme_update(plot.title = element_text(hjust = 0.5))

# Histogram for all countries in 1970
p1 <- qplot(x = X1970, data=df, binwidth=0.5, fill= I('darkorange'), color= I('black'),
      xlab = 'Energy Use per Person in TOE',
      ylab = 'Count of Countries',
      main = 'Energy Use in 1970')+
  scale_x_continuous(breaks=seq(0,20,2))

# Histogram for all countries in 1985
p2 <- qplot(x = X1985, data=df, binwidth=0.5, fill= I('darkorange'), color= I('black'),
      xlab = 'Energy Use per Person in TOE',
      ylab = 'Count of Countries',
      main = 'Energy Use in 1985')+
  scale_x_continuous(breaks=seq(0,20,2))

# Histogram for all countries in 2000
p3 <- qplot(x = X2000, data=df, binwidth=0.5, fill= I('darkorange'), color= I('black'),
            xlab = 'Energy Use per Person in TOE',
            ylab = ' Count of Countries',
            main = 'Energy Use in 2000')+
  scale_x_continuous(breaks=seq(0,20,2))

# Histogram for all countries in 2010
p4 <- qplot(x = X2010, data=df, binwidth=0.5, fill= I('darkorange'), color= I('black'),
            xlab = 'Energy Use per Person in TOE',
            ylab = 'Count of Countries',
            main = 'Energy Use in 2010')+
  scale_x_continuous(breaks=seq(0,20,2))

multiplot(p1,p2, p3, p4, cols =2)

# Plot several countries on the same graph over time
plot(x=labels, y=`Qatar`, type='l', col='blue', ylim=c(2,25),
     xlab ='', ylab='Energy Use per Person in TOE', lwd=2)
lines(labels, `Iceland`, col='green', lwd=2)
lines(labels, `United States`, col='red', lwd=2)
lines(labels, `Finland`, col = 'black',lwd=2)
lines(labels, `Japan`, col = 'magenta' , lwd=2)
lines(labels, `average_energy_use`, col='brown',lwd=2)
legend(1960, 22,legend=c("Qatar", "Iceland", "United States", "Finland", "Japan", "Average"),
       col=c("blue", "green", 'red', 'black', "magenta", 'brown'), lty=1, cex=0.8)
title('Energy Use by Country')


# Average energy use per person worldwide over time
qplot(x=labels, y=average_energy_use, geom='line', col = 'red',
      ylab = 'Energy Use per Person in TOE',
      xlab='', main = 'Worldwide Energy Use Per Person' , size=2)+
  scale_y_continuous(limits=c(1,4.5))+
  theme(legend.position='None')




