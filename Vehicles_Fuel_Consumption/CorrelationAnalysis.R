#DESCRIPTION:    Correlation analysis between the numeric variables of the 
#                   mtcars dataset.
#                Find the variables that are most correlated with the miles per gallon(mpg) variable
#                   using the correlation matrix.
#                The values inside the correlation matrix represents the pearson correlation coefficient
#                    which estimates the strength and linear correlation between two numerical variables.
#                Variables with a correlation coefficient close to 1 have a strong positive linear correlation and
#                    the variables with a correlation coefficient close to -1 have a strong negative linear correlation.
#                Based on the linear regression analysis I've identified the variables that most influence the mpg consumption:
#                     hp->horsepower
#                     wt->weight(lbs)

#RESULTS:          
#                Strong/medium Negative Correlations with Miles_Per_Gallon (mpg):
#                      -weight(-0.87):high
#                      -cylinders (-0.85): high
#                      -displacement (-0.85):high
#                      -horsepower (-0.78):high
#                      -carburators (-0.55): medium

#                Strong/medium positive Correlation with Miles_Per_Gallon (mpg):
#                      -carburators (-0.55): medium
#                      -Rear_axle_ration (0.68): medium
#                      -Transmissione(0.60): medium
#                      -engine_shape (0.66): medium
#                      -Quarter_Mile_Time (0.42): weak

#CONCLUSION:      The correlation matrix provides an estimation of the bivariate analysis(between two variables at a time). 
#                 In the linear regression model i've identyfied the variables weight and horsepower as the most significant for the fuel-consumption in miles per gallon
#                   and some variables(cylinders, carburators, displacement, transmission...) that are not significant for the fuel-consumption in miles per gallon,
#                     however the correlation between fuel-consumption in miles per gallon and non significant variables is high/medium, This is caused by multicollinearity
#                     for example displacement and cylinders  variables are not statistically significant for the fuel-consumption in miles per gallon(p-value > 0.05) but the
#                        correlation with mpg is high, that' because the effect of having more cylinders or a larger displacement is already "explained" in large part
#                           by the reason that these cars tend to be heavier and/or more powerful.
#                     


library(dplyr)
library(corrplot)
setwd("C:/Users/lenovo/Desktop/python_tutorial/Analisi_Dati/RStudio/exercise/grafici")




name_cars = rownames(mtcars)
name_cars


#dataframe
mtcars_df = data.frame(model = name_cars, Miles_Per_Gallon = mtcars$mpg,
                cylinders = mtcars$cyl,displacement=mtcars$disp,
                horsepower=mtcars$hp, weight = mtcars$wt,
                Rear_axle_ration = mtcars$drat,gears = mtcars$gear,
                Quarter_Mile_Time = mtcars$qsec,Transmission = mtcars$am,engine_shape = mtcars$vs,
                carburators = mtcars$carb)
mtcars_df$performance = mtcars_df$horsepower/mtcars_df$weight


variables = mtcars_df %>%
  select(Miles_Per_Gallon,cylinders,displacement,horsepower,Rear_axle_ration,weight,Quarter_Mile_Time,engine_shape,Transmission,gears,carburators)
corr_matrix = cor(variables)
png("heatmap_correlation.png", width = 1200, height = 950)
corrplot(corr_matrix,
         method = "shade",
         type = "full",
         order = "hclust",   #group variables with similar values
         tl.col = "black",   #labels color
         tl.cex = 2.0,       #font size
         number.cex = 1.8,    #coefficients font size   
         tl.srt = 45,        #rotation of the labels
         addCoef.col = "dark green",   #correlation coefficients color 
         cl.pos = "r")
dev.off() 


