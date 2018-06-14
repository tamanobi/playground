# install.packages(c("dplyr", "tidyr"))
library(dplyr)
library(tidyr)
ad_click <- read.table(file = 'data/ad_click.csv', header = TRUE, sep=',')
head(ad_click)
summary(ad_click)

# makedummies' cause generate "res" column instead "click" column.
# We shouldn't use makedummies library when target frame contains boolean columns.
# tmp <- data.frame(a = factor(c('y', 'n')), b = factor(c('y', 'n')))
# makedummies::makedummies(tmp)

dummy <- makedummies::makedummies(ad_click)
head(dummy)
head(d)
df <- dplyr::tbl_df(dummy)
(ctr_df <- df %>% dplyr::group_by(
  sex_male
  , sex_other
  , agegroup_20s
  , agegroup_30s
  , agegroup_40s
  , agegroup_50s
  ) %>% dplyr::summarise(y=sum(res==1), n=sum(res==0)) %>% dplyr::mutate(ctr = y/(y+n)) %>% arrange(desc(ctr)))
# (ctr_df %>% tidyr::gather(key = sex, value = ctr, sex_male, sex_other) %>% tidyr::gather(key = agegroup, value = ctr, agegroup_20s, agegroup_30s, agegroup_40s, agegroup_50s) %>% select(-c('ctr')) %>% dplyr::mutate(ctr = y/(y+n)))
(temp <- ctr_df %>% tidyr::gather(key = sex, value = ctr, sex_male, sex_other) %>% tidyr::gather(key = agegroup, value = ctr, agegroup_20s, agegroup_30s, agegroup_40s, agegroup_50s) %>% select(-c('ctr', 'y', 'n')))
# https://oku.edu.mie-u.ac.jp/~okumura/stat/140921.html
# pred <- predict.glm(ad_click.glm, newdata = a, type="response") # get probabilty to be type="response".
test <- expand.grid(sex=levels(ad_click$sex), agegroup=levels(ad_click$agegroup)) # http://rishida.hatenablog.com/entry/2013/08/13/173849
pred <- predict.glm(ad_click.glm, newdata = test, type="response") # get probabilty to be type="response".
ctr_pred <- cbind(makedummies::makedummies(test), pred_ctr=pred)
dplyr::inner_join(ctr_df , ctr_pred)
