library(dplyr)
library(vcd)
library(tidyr)
samplesize <- 300000
sex <- factor(floor(runif(n = samplesize, min = 0, max = 3)), labels = c("male", "female", "other"))
agegroup <- factor(floor(runif(n = samplesize, min = 0, max = 5)), labels = c("10s", "20s", "30s", "40s", "50s"))
d <- data.frame(sex, agegroup)

# 偏りのないデータ
ad_click1 <- d %>% mutate(
  click = factor(case_when(
    TRUE ~ rbinom(n(), 1, 0.003)
  )
  , labels = c('no', 'yes')
  )
)
# 偏りのあるデータ(交互作用なし)
ad_click2 <- d %>% mutate(
  click = factor(case_when(
    sex == 'female' ~ rbinom(n(), 1, 0.005)
    , TRUE ~ rbinom(n(), 1, 0.003)
  )
  , labels = c('no', 'yes')
  )
)
# 偏りのあるデータ(交互作用あり)
ad_click3 <- d %>% mutate(
  click = factor(case_when(
    sex == 'female' & agegroup == '20s' ~ rbinom(n(), 1, 0.005)
    , TRUE ~ rbinom(n(), 1, 0.003)
  )
  , labels = c('no', 'yes')
  )
)
# 偏りのあるデータ(単純作用+交互作用)
ad_click4 <- d %>% mutate(
  click = factor(case_when(
    sex == 'female' & agegroup == '20s' ~ rbinom(n(), 1, 0.005)
    , agegroup == '30s' ~ rbinom(n(), 1, 0.005)
    , TRUE ~ rbinom(n(), 1, 0.003)
  )
  , labels = c('no', 'yes')
  )
)

chisq_p.values <- function (d) {
  x <- d %>% group_by(sex, agegroup, click)　%>% summarise(count=n()) %>% spread(click, count)
  colnames(x) <- c('sex', 'agegroup', 'nonclick', 'click')
  x <- x %>% mutate(ctr = (click/(nonclick + click)))

  p.values <- c()
  p_sex <- c()
  p_agegroup <- c()
  p_nonclick <- c()
  p_click <- c()
  ctr <- c()
  for (i in 1:nrow(x)) {
    y <- rbind(x[i,3:4], x[-i,3:4] %>% summarize(nonclick=sum(nonclick), click=sum(click)))
    p_sex <- append(p_sex, sapply(x[i, 1], as.character))
    p_agegroup <- append(p_agegroup, sapply(x[i, 2], as.character))
    ctr <- append(ctr, sapply(x[i, 5], as.double))
    p.values <- append(p.values, chisq.test(y)$p.value)
    p_nonclick <- append(p_nonclick, x[i, 3])
    p_click <- append(p_click, x[i, 4])
  }
  x <- d %>% group_by(sex, click) %>% summarise(count=n()) %>% spread(click, count)
  colnames(x) <- c('sex', 'nonclick', 'click')
  x <- x %>% mutate(ctr = (click/(nonclick + click)))
  for (i in 1:nrow(x)) {
    y <- rbind(x[i,2:3], x[-i,2:3] %>% summarize(nonclick=sum(nonclick), click=sum(click)))
    p_sex <- append(p_sex, sapply(x[i, 1], as.character))
    p_agegroup <- append(p_agegroup, '*')
    p.values <- append(p.values, chisq.test(y)$p.value)
    ctr <- append(ctr, sapply(x[i, 4], as.double))
    p_nonclick <- append(p_nonclick, x[i, 2])
    p_click <- append(p_click, x[i, 3])
  }

  x <- d %>% group_by(agegroup, click) %>% summarise(count=n()) %>% spread(click, count)
  colnames(x) <- c('sex', 'nonclick', 'click')
  x <- x %>% mutate(ctr = (click/(nonclick + click)))
  for (i in 1:nrow(x)) {
    y <- rbind(x[i,2:3], x[-i,2:3] %>% summarize(nonclick=sum(nonclick), click=sum(click)))
    p_sex <- append(p_sex, "*")
    p_agegroup <- append(p_agegroup, sapply(x[i, 1], as.character))
    p.values <- append(p.values, chisq.test(y)$p.value)
    ctr <- append(ctr, sapply(x[i, 4], as.double))
    p_nonclick <- append(p_nonclick, x[i, 2])
    p_click <- append(p_click, x[i, 3])
  }

  return(data.frame(sex=p_sex, agegroup=p_agegroup, p.values, click=p_click, ctr) %>% mutate(
    mark=case_when(p.values < 0.01 ~ '**'
                   , p.values < 0.05 ~ '*'
                   , p.values < 0.01 ~ '+'
                   , TRUE ~ '')
  ))
}

chisq_p.values(ad_click1)
chisq_p.values(ad_click2)
chisq_p.values(ad_click3)
chisq_p.values(ad_click4)
