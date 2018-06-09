ad_click <- read.table(file = 'data/ad_click.csv', header = TRUE, sep=',')
head(ad_click)

# Visualization
crosstab <- xtabs(~ click + agegroup + sex, data=ad_click)
pairs(crosstab, lower_panel = pairs_assoc, shade=TRUE) # https://www.slideshare.net/KumarP34/using-r-for-customer-segmentation
# If the number of variables is about 3
vcd::mosaic(click ~ agegroup | sex, data=ad_click, shad=TRUE)

# Multiple Regression
## Multiple regression analysis can not be applied to qualitative variables.
##   ad_click.lm <- lm(formula = click ~ sex + agegroup, data=ad_click)
##   summary(ad_click.lm)

# Logistic Regression
ad_click.glm <- glm(formula = click ~ sex + agegroup, data = ad_click, family="binomial")
summary(ad_click.glm)

# odds ratio
exp(coef(ad_click.glm))

