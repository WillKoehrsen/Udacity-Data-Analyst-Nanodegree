getwd()
getwd()
setwd('Udacity-Data-Analyst-Nanodegree/')
setwd('Lessons/')
setwd('P4 Lesson 3/')
list.files()

install.packages('ggplot2')
library(ggplot2)
df = read.csv('Electricity Generation per capita.csv', header=TRUE, row.names=1)
qplot(x=X1990, data=df, binwidth=2000)
summary(df)

which(rownames(df)=='United States')

all_countries <- rownames(df)
all_countries[1]

for (number in seq(1,length(all_countries),1)){
  row_num <- which(rownames(df)== all_countries[number])
  country_name <- (all_countries[number])
  print(country_name)
  assign(country_name, as.numeric(df[row_num,]))
  
}
colnames(df)
labels <- seq(1990,2008,1)
str(Ukraine)
Ukraine <- as.numeric(Ukraine[1,])
qplot(Ukraine, geom='line')
Ukraine
plot(x = labels, y = Ukraine)+
  scale_x_continuous(breaks=seq(1990,2008,1))

qplot(x=labels, y=`United States`, geom='line') + 
  scale_x_continuous(breaks=seq(1990, 2008, 1))

labels[length(labels)]
