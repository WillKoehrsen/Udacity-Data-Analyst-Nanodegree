# P4 Lesson 5 problem set

library(ggplot2)
library(dplyr)



data(diamonds)
df <- diamonds


# Facet wrap creates a new plot for each value in columm
ggplot(aes(x = price),  data = df) + geom_histogram(aes(fill= cut), bins = 20, color='black') + facet_wrap(~clarity) + 
  scale_fill_brewer(type='qual')

ggplot(aes(x = price),  data = df) + geom_histogram(aes(fill= cut), bins = 20, color='black') + facet_wrap(~color)  + 
  scale_fill_brewer(type='qual')

?diamonds
# Table: width of top of diamond relative to widest point

ggplot(aes(x = table, y=price) , data=df) + geom_point(aes(color=cut), alpha = 1/10) + coord_cartesian(xlim=c(50,70)) + 
  scale_x_continuous(breaks=seq(50,70,2))

