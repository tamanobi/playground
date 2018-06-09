samplesize <- 1000
sex <- factor(floor(runif(n = samplesize, min = 0, max = 3)), labels = c("male", "female", "other"))
agegroup <- factor(floor(runif(n = samplesize, min = 0, max = 5)), labels = c("10s", "20s", "30s", "40s", "50s"))

a <- sapply(sex, function (x) {
  b <- 0
  if(x == 'male') b <- rbinom(n=1,size=1,prob = 0.7)
  else if (x == 'female') b <- rbinom(n=1,size=1,prob = 0.5)
  else b <- rbinom(n=1,size=1,prob = 0.1)
  return(b)
})

b <- sapply(agegroup, function (x) {
  c <- 0
  if (x == '30s') c <- rbinom(n=1,size=1,prob = 0.7)
  else c <- rbinom(n=1,size=1,prob = 0.5)
  return (c)
})

click_rate <- scale(x = (a+b), center=min(a+b), scale = (max(a+b) - min(a+b)))
click <- factor(ifelse(click_rate > 0.5, 1, 0), labels = c("n", "y"))
summary(click)
ad_click <- data.frame(click=click, sex=sex, agegroup)
write.table(x = ad_click,file = "data/ad_click.csv", sep = ',')
