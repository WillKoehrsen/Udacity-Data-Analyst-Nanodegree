data(diamonds)
df <- diamonds

library(ggplot2)
library(dplyr)

df<-diamonds
summary(df)

carat_groups <- group_by(df, carat)
x_groups <- group_by(df, x)

theme_update(plot.title = element_text(hjust = 0.5))
ggplot(aes(x=x, y= price), data=df) +
  geom_point(color='red') + coord_cartesian(xlim=c(3,9.5))  +
  labs(legend.title=element_blank())

with(df, cor.test(x,price, method='pearson'))
with(df, cor.test(y,price, method='pearson'))
with(df, cor.test(z,price, method='pearson'))

ggplot(aes(x=z, y= price), data=df) +
  geom_point(color='yellow') + coord_cartesian(xlim=c(3,6.5)) 

ggplot(aes(x=depth, y=price), data=df) + geom_point(alpha=1/100, color='turquoise') + 
  scale_x_continuous(breaks=seq(58,66,1)) + coord_cartesian(xlim=c(58,66))

with(df, cor.test(depth, price, method='pearson'))

ggplot(aes(x=carat, y=price), data=subset(diamonds, carat < quantile(carat, probs=0.99) & price < quantile(price, probs=0.99)))+
  geom_point(color='peru', alpha = 1/10)


df$volume <- with(df, x*y*z)
ggplot(aes(x=volume, y=price), data=df) + geom_point(color='orange') + 
  coord_cartesian(xlim=c(0,500))

with(subset(df, volume!= 0 & volume<= 800), cor.test(volume, price))

library(ggplot2)
library(dplyr)

ggplot(aes(x=volume, y=price), data=subset(df, volume != 0 & volume <= 800)) + 
  geom_point(color='red') + coord_cartesian(xlim=c(0,500)) + 
  geom_smooth(method='lm', linetype = 4)

clarity_groups <- group_by(df, clarity)
df_by_clarity <- summarize(clarity_groups,
                           mean_price = mean(price),
                           median_price = median(price),
                           min_price = min(price),
                           max_price = max(price),
                           n = n())


head(df_by_clarity, 8)

color_groups <- group_by(df, color)
diamonds_mp_by_color <- summarize(color_groups,
                                  mean_price= mean(price))

diamonds_mp_by_clarity <- summarize(clarity_groups,
                                    mean_price = mean(price))

cut_groups <- group_by(df, cut)
diamonds_mp_by_cut <- summarize(cut_groups, 
                                mean_price = mean(price))

p1 <- ggplot(aes(x = clarity, y= mean_price), data = diamonds_mp_by_clarity) +
  geom_bar(stat='identity', color='red') + labs(x='Clarity (I1 is worst)')
  ggtitle('Mean Price by Clarity')
p2 <- ggplot(aes(x = color, y= mean_price), data = diamonds_mp_by_color) +
  geom_bar(stat='identity' , color='green') + labs(x='Clarity (J is worst)')
  ggtitle('Mean Price by Color')
  
p3 <- ggplot(aes(x = cut, y= mean_price), data = diamonds_mp_by_cut) +
  geom_bar(stat='identity' , color='pink') + labs(x='Cut of Diamond')
  ggtitle('Mean Price by Color')
  
library(gridExtra)
grid.arrange(p1, p2, p3, ncol=2)


ggplot(aes(x=carat, y=price), data=df) + geom_point(color='orange')
?ggplot


?quantile
?diamonds
