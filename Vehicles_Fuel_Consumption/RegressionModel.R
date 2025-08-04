#DESCRIPTION:       Try to understand how the most significant variables on the variability of consumption in mpg identified in the PreAnalysis.r script
#                          influence in a combined way the fuel-consumption in miles per gallon(mpg).
#                   In the PreAnalysis.R script I identyfied some strong numeric predictors and numeric categorial predictors of the variable mpg:
#                     hp->horsepower
#                     wt->weight(lbs)
#                     disp->displacement
#                     cyl->cylinders
#                     am->transmission(0:Automatic,1:Manual)
#                     vs->engine shape(0:V-shape, 1:straight)
#                     carb->number of carburators
#                     cyl->cylinders

#SUMMARY:            -RESIDUALS: Min(-3.9158), 1Q(-1.2188),Median(0.0000), 3Q(0.9443), Max(4.5717) are simmetrically distributed around 0 
#                                so the model represents well the correlation between the variables.

#                    -COEFFICIENTS(NON-CATEGORIAL):
#                       ->weight:For every 1,000 lb increase in weight, MPG decreases by 4,536 units(Estimate:  -4.53649).
#                                The standard error of 1.97065(Std.error: 1.97065) means that the estimation of the coefficient weight is a little bit uncertain.        
#                                The level of significance for the coefficient is 0.0328*(): 0.0328 < 0.05 therefore the null hypothesis that the weight
#                                     is not statistically significant can be rejected.
#                                The ratio between the estimate of the coefficient weight and its standard error is -2.302(t value: -2.302) and that means the p-value is significant because
#                                     the value is far from 0.

#                      ->horsepower:For every increment of 1 horsepower, MPG decreases by 0.067 units(Estimate: -0.06713).
#                                   The standard error of 0.03053(Std. Error: 0.03053) means that the estimate of the coefficient is more certain than the estimate of the weight variable.
#                                   The level of significance for the coefficient  is 0.0405*(p-value:0.0405*): 0.0405 < 0.05 therefore the null hypotesis that the horsepower is not
#                                      statistically significant can be rejected.
#                                   The ratio between the estimate of the coefficient horsepower and its standard error is -2.199(t value:-2.199) < 0 and that means the p-value is significant.

#                      ->displacement:For every increment of 1 for the displacement variable,the MPG increases by 0.033 units(Estimate: 0.033).
#                                     The standard error of 0.02610(Std. Error: 0.02610) means that the estimate of the coefficient is certain.
#                                     The level of significance for the coefficient is 0.2099(p-value:0.2099) > 0.05 therefore the coefficient displacement IS NOT STATISTICALLY SIGNIFICANT.
#                                     The ratio between the estimate of the coefficient displacement and its standard error is 1.298(t value: 1.298) > 0 so the value is closer to 0 than
#                                         the others and that means the displacement coefficient IS NOT SIGNIFICANT FOR THIS REGRESSION MODEL.    

#                      -COEFFICIENTS(CATEGORIAL):
#                         R always choose the first level of a factor for example it choose the level 4 cylinders for the factor cylinders.
#                         ->cylinders6:Cars with 6 cylinders generally have 3.85MPG less than the cars with 4 cylinders(Estimate: -3.85392).
#                                      The p-value is 0.1074 > 0 so the coefficient cylinders6 IS NOT SIGNIFICANT IN THIS REGRESSION MODEL.
#                         ->cylinders8:Cars with 8 cylinders generally have 2.66MPG less than the cars with 4 cylinders(Estimate: -2.65776).
#                                      The p-value is 0.6007 > 0.05 so the coefficient cylinders8 IS NOT SIGNIFICANT FOR THIS REGRESSION MODEL.
#                         The effect of the number of cylinders in the vehicles has no effect on the fuel-consumption i  miles per gallon.

                          ->Transmission1 (Estimate: 2.00751, p-value: 0.3105): Cars with manual transmission(1) generally have 2.01MPG more than cars with automatic transmission(0).
#                                                                               p-value > 0.05 so the coefficient transmission IS NOT STATISTICALLY SIGNIFICANT FOR THIS REGRESSION MODEL.


#                         ->engine_shape1 (Estimate: 2.63785, Pr(>|t|): 0.2654): Cars with straight engines(1) generally have 2.63785 more than cars with V-shape engines.
#                                                                                p-value > 0.05 so the coefficient engine_shape IS NOT STATISTICALLY SIGNIFICANT FOR THIS REGRESSION MODEL.

 
#                         ->(carburators2,carburators3,carburators4,carburators6,carburators8):
#                                All carburetor levels (relative to the reference carburetor level1) have very high p-values,so the number of carburetors
#                                   IS NOT STATISTICALLY SIGNIFICANT in predicting MPG when considering the other variables in the model.


#                    -RESIDUALS STANDARD ERROR:  2.603 on 19 degrees of freedom means that on average, the model's predictions deviate from the actual MPG values by about 2,603 units.

#                    -MULTIPLE R-SQUARED: 0.8856, ADJUSTER R-SQUARED: 0.8134 means that this linear regression model can explain the 88.56% of the MPG variability,
#                                                                     however some non-significant variables such as cylinders,transmission,engine_shape,carburators has any contribute
#                                                                     for the MPG variability so the adjuster r-squared value is lower than the other one even if by a little.


#                   -F-STATISTICS: 12.26 ON 12 AND 19 DF, P-VALUE: 1.616e-06:
#                          the p-value is about  0.000001616 this value is much lower than 0.05 that means the model is STATISTICALLY SIGNIFICANT.


#CONCLUSION:        The strongest predictors variables of the fuel-consumption in miles per gallon(mpg) are non categorial numeric variables:
#                          -weight:For every 1000lbs of weight, mpg values decreases by 4.5.
#                          -horsepower:For every 1 horsepower, mpg values decreases by 0.067.
#                   The non significant predictors variables are mainly categorial numeric variables:
#                          -displacement: For every increment of 1 for the displacement variable,the MPG increases by only 0.033 units, the p-value is greater than 0.05, so the displacement
#                                           variable is not a predictor of the MPG variable This is probably because its effect on fuel-consumption
#                                           is already explained by weight and horsepower, with which displacement is strongly correlated. 
#                                           This behavior is also visible in the scatterplot(PreAnalysis.R).

#                          -cylinders:the MPG differences between 4, 6, and 8 cylinders are not statistically significant.

#                          -transmission: Manual transmission cars(1) show a little bit higher MPG than automatic(0),but the difference is not statistically significant.

#                          -engine_shape: this categorial variables also is not statistically significant.

#                          -cylinders: It does not have a statistically significant impact on fuel consumption in mpg.

#                   If the goal is to reduce the  fuel-consumption(increase MPG) for the vehicles in the dataset mtcars, the most effective practices are:
#                        -reduce the weight of the vehicles.
#                        -reduce the power of the engines.



#create a vector containing the names of the cars: in the mtcars dataset the names of the cars represent the row names
name_cars = rownames(mtcars)
name_cars


#dataframe
mtcars_df = data.frame(model = name_cars, Miles_Per_Gallon = mtcars$mpg,
                cylinders = mtcars$cyl,displacement=mtcars$disp,
                horsepower=mtcars$hp, weight = mtcars$wt,
                Rear_axle_ration = mtcars$drat,gears = mtcars$gear,
                Quarter_Mile_Time = mtcars$qsec,Transmission = mtcars$am,engine_shape = mtcars$vs,
                carburators = mtcars$carb)
mtcars_df$performance = mtcars_df$horsepower/mtcars_df$weight  #add a new column performance


#cast the categorial variables of the mtcars_df to factors
mtcars_df$Transmission = as.factor(mtcars_df$Transmission)  #(0,1)
mtcars_df$engine_shape = as.factor(mtcars_df$engine_shape)  #(0,1)
mtcars_df$cylinders = as.factor(mtcars_df$cylinders)  # (4, 6, 8)
mtcars_df$carburators = as.factor(mtcars_df$carburators)  #(1,2,3,4,6,8)


#Multiple linear regression model using the function lm():
regression_model = lm(Miles_Per_Gallon ~ weight + horsepower + displacement + cylinders + Transmission + engine_shape + carburators, data = mtcars_df)
#get the summary about the regression_model:
summary(regression_model)
