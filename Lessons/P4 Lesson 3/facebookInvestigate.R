getwd()
setwd('..
      ')

setwd('..')
setwd('..')
getwd()
setwd('P4 Lesson 3')
wd.files()
files.list()
file.show()
list.files()

facebookData = read.csv('pseudo_facebook.tsv', sep='\t')
library(ggplot2)
str(facebookData)
names(facebookData)
row.names(facebookData)
fd = facebookData

qplot(x = dob_day, data=facebookData) +
  scale_x_continuous(breaks=1:31)

theme_set(theme_minimal(12))


qplot(facebookData$dob_year)
names(facebookData)
qplot(facebookData$likes)



ggplot(aes(x=dob_day),data=facebookData)+
  geom_histogram(binwidth=1) +
  scale_x_continuous(breaks=1:31) +
  facet_wrap(~dob_month, ncol =3)

summary(facebookData$tenure)
summary(facebookData$friend_count)
qplot(facebookData$friend_count, binwidth=50) +
  scale_x_continuous(limits=c(1,1000), breaks=seq(0,1000,100)) +
  facet_wrap(~gender, ncol=2)

qplot(x=friend_count, data=facebookData, binwidth=50) + 
  scale_x_continuous(limits=c(1,1000), breaks=seq(0,1000,100))+
  facet_grid(gender~.)
  
ggplot(aes(x=friend_count),data=subset(facebookData, !is.na(gender))) + 
  geom_histogram(binwidth=50) + 
  scale_x_continuous(limits=c(1,1000), breaks=seq(0,1000,100))+
  facet_wrap(~gender)

summary(subset(facebookData, gender=male))
(facebookData[facebookData$friend_count > 500, ])
table(facebookData$gender)
?by
by(facebookData$friend_count, facebookData$gender, summary)

by(facebookData$tenure, facebookData$gender, summary)
        
qplot(x = tenure/365, data=facebookData, binwidth = 0.5,
      xlab= 'Number of Years Using Facebook',
      ylab = 'Frequency Count of Users',
      color=I('black'), fill=I('DarkOrange')) +
        scale_x_continuous(breaks=seq(0,7.5,1), lim=c(0,7.5))


qplot(x=facebookData$age, binwidth=1,
      xlab = 'Age of User',
      ylab = 'Frequency Count of Users',
      color = I('black'), fill = I('firebrick')) + 
        scale_x_continuous(lim=c(13,120), breaks=seq(15,120,15))

summary(facebookData$age)
summary(facebookData$tenure/365)

summary(log10(facebookData$friend_count + 1))

install.packages('gridExtra')
library(gridExtra)

# Define individual plots

# Original representation of Friend Count
p1 <- qplot(x=friend_count, data=facebookData, fill=I('red'), color=I('black'), bins=20) + 
  scale_x_continuous(lim=c(0,1000), breaks=seq(0,1000,50))
# Log10 of friend count
p2 <- qplot(x=log10(friend_count + 1), data=facebookData, color=I('black'), bins = 20,
            xlab = 'log10 of Friend Count',
            fill = I('brown')) + 
  scale_x_continuous(breaks=seq(0,4,0.5))
  
# SQRT of friend count
p3 <- qplot(x=sqrt(friend_count), data=facebookData, color=I('black'),bins = 20,
           xlab = 'sqrt of Friend Count',
           fill = I('orange')) + 
  scale_x_continuous(lim=c(0,60), breaks = seq(0,60,5))

grid.arrange(p1,p2,p3,ncol=1)

qplot(x= friend_count, data=subset(facebookData, !is.na(gender)),
      binwidth = 5) + 
  scale_x_continuous(lim=c(0,1000), breaks=seq(0,1000,50)) + 
  facet_wrap(~gender)

qplot(x= friend_count, y= ..density.., 
      data=subset(facebookData, !is.na(gender)),
      xlab = 'Friend Count',
      ylab = 'Proportion of Users',
      binwidth = 5, geom='freqpoly', color=gender) + 
  scale_x_continuous(lim=c(0,1000), breaks=seq(0,1000,50)) 

rm(x)

males = subset(facebookData, !is.na(gender) & gender=='male', friend_count)
females = subset(facebookData, !is.na(gender) & gender=='female', friend_count)

qplot(x = www_likes, data=subset(facebookData, !is.na(gender))) + 
  facet_wrap(~gender)

qplot(x = www_likes, y=..density.., data=subset(facebookData, !is.na(gender)),
      geom='freqpoly', color=gender, binwidth = 20,
      xlab = 'Number of Likes on Web',
      ylab = 'Proportion of Users with Number of Likes') + 
  scale_x_continuous(lim=c(0,250),breaks=seq(0,250,50))

males = subset(facebookData, !is.na(gender) & gender=='male',  www_likes)
females = subset(facebookData, !is.na(gender) & gender=='female',www_likes)


by(facebookData$www_likes, facebookData$gender, summary)
by(facebookData$www_likes, facebookData$gender, sum)

qplot(x = gender, y = friend_count, data = subset(facebookData, !is.na(gender)), 
      geom = 'boxplot')+
  coord_cartesian(ylim=c(0,1000))

by(facebookData$friend_count, facebookData$gender, summary)

by(facebookData$friendships_initiated, facebookData$gender, summary)

qplot(x = gender, y = friendships_initiated, data=subset(facebookData, !is.na(gender)),
      geom = 'boxplot')+
  coord_cartesian(ylim=c(0,200))

mobile_checkin <- NA
facebookData$mobile_checkin <- ifelse(facebookData$mobile_likes>0, 1, 0)
facebookData$mobile_checkin <- factor(facebookData$mobile_checkin)

summary(facebookData$mobile_checkin)
nrow(facebookData[facebookData$mobile_checkin ==1,])/ length(facebookData$mobile_checkin)
sum(facebookData$mobile_checkin==1)/ length(facebookData$mobile_checkin) * 100

