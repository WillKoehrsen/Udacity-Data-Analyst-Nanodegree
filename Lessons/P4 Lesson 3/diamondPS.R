library(ggplot2)
data(diamonds)

summary(diamonds)
str(diamonds)
levels(diamonds$color)

qplot(x=price, data=diamonds)+
  facet_wrap(~color)
qplot(x= price, data=diamonds, geom='freqpoly', color=color)

str(diamonds)
levels(diamonds$color)
?diamonds

qplot(x=price, data=diamonds, binwidth=1000, color=I('black'), fill=I('darkorange'))+
  scale_x_continuous(breaks=seq(0,20000, 2500))

summary(diamonds$price)
IQR_price <- as.integer(summary(diamonds$price)[5] - summary(diamonds$price)[2])
qu1_price <- as.integer(summary(diamonds$price)[2])
qu3_price <- as.integer(summary(diamonds$price)[5])
qu3_price + 3*IQR_price
high_outliers = subset(diamonds, price > (qu3_price + 3*IQR_price))
low_outliers = subset(diamonds, price < (qu1_price - 3*IQR_price))
summary(diamonds$price)

nrow(subset(diamonds, price >= 15000))

qplot(x=price, data=diamonds, binwidth=50, color=I('black'), fill=I('turquoise'))+
  scale_x_continuous(breaks=seq(300,2000,100)) + 
  coord_cartesian(xlim=c(300,2000))

summary(subset(diamonds, price < 2000, price))
summary(diamonds$price)
?diamonds

qplot(x=price, data=diamonds, binwidth=1000, color=I('black'), fill=I('yellow'))+
  facet_wrap(~cut)

by(diamonds$price, diamonds$cut, summary, digits = max(getOption('digits')))

?facet_wrap
qplot(x=price, data= diamonds)+
facet_wrap(~cut, scales='free_y')

qplot(x=log10(diamonds$price/diamonds$carat), data=diamonds, binwidth=0.05,
      color=I('black'), fill=I('cyan'),
      xlab='Price Per Carat Log10 Scale')+
  facet_wrap(~cut, scales='free_y')+
  scale_x_continuous(lim=c(3,4),breaks=seq(3,4,0.1))

qplot(x=cut, y=price, data=diamonds, geom='boxplot') + 
  coord_cartesian(ylim=c(300,10000))

by(diamonds$price, diamonds$clarity, summary, digits=max(getOption('digits')))

qplot(x=color, y=price, data=diamonds, geom='boxplot')+
  coord_cartesian(ylim=c(300,10000))

