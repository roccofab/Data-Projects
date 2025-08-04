# Vehicle fuel consumption analysis dataset mtcars
### This basic data analysis project built in RStudio using the language R examine the factors primarily affecting fuel-consumption in 32 vehicles stored in the dataset mtcars. The data was extracted from the 1974 Motor Trend US magazine, and comprises fuel consumption and 10 aspects of automobile design and performance for 32 automobiles.The dataset is small and contains data from 1974 and therefore does not reflect the most modern current technologies.

## Goals:
- Investigate which variables have **the greatest impact on fuel-consumption in Miles per Gallon.**

- **Graphical identification** of the most influential variables on fuel-consumption through scatter plot and boxplot.

- Calculate the main **statistics** of the dataset.

- Once the variables that most influence fuel-consumption have been identified, analyze the **correlation** between these through bivariate analysis.

- Multivariate statistical analysis using **multiple linear regression** to quantify the combined impact of variables on fuel-consumption.

## Variables:
- **mpg:** fuel-consumption in Miles per Gallon
- **cyl:** number of cylinders(categorial variable)
- **disp:** displacement
- **hp:** horsepower
- **drat:** Rear Axle Ratio
- **wt:** weight
- **qsec:** Quarter Mile Time
- **vs:** engine shape(categorial variable)
- **am:** transmission(categorial variable)
- **gear:** number of gears(categorial variable)
- **carb:** number of carburators(categorial variable)
- **performance:** horsepower/weight(additional variable)

## Project structure:
```
.
├── PreAnalysis.R           # Dataset exploration and plots
├── CorrelationAnalysis.R   # Correlation analysis 
├── RegressionModel.R       # Linear regression model
├── grafici/               # Plots images
└── README.md           

```

## Prerequisites:
  - R

  - RStudio

  - Data source: Motor Trend US magazine (1974)
  
  - R packages: dplyr, corrplot, 

## Correlation:
#### Negative correlations:
- **weight(-0.87):** high
- **Cylinders(-0.85):** high
- **Displacement(-0.85):** high
- **Horsepower(-0.78):** high
- **Carburators(-0.55):** medium

#### Positive correlations:
- **Carburators(-0.55):** medium
- **Rear_axle_ration (0.68):** medium
- **Transmissione(0.60):** medium
- **engine_shape (0.66):** medium
- **Quarter_Mile_Time (0.42):** weak


## Regression Model:
#### The most significant variables predictors of the fuel-consumption in miles per gallon:
- **weight():** For every 1000lbs of weight, mpg values decreases by 4.5, the level of significance(p-value) for the coefficient weight is 0.0328*() < 0.05
- **horsepower():** For every increment of 1 horsepower, MPG decreases by 0.067 units, the level of significance(p-value) for the coefficient horsepower is 0.0405 < 0.05 
#### The model explains 88.56% of the MPG variability (R² = 0.8856).


## Charts:
### The charts are available in the directory "grafici/", the most relevants charts for the fuel-consumption analysis:
 - **Histogram of fuel-consumption in Miles per Gallon:** The histogram is skewed to the right(few very efficient cars, many cars with average consumption).
   
   <img src = "grafici\Histogram_MilesPerGallon.png" width = 220px height = 175px>


 
 - **Scatter plot MilesPerGallon_cylinders:** Vehicles that have more cylinders consume more fuel than vehicles that have fewer cylinders.
The regression line is inclined downwards and this confirms that as the number of cylinders increases the efficiency in miles per gallon tends to decrease.

   <img src = "grafici\MilesPerGallon_cylinders.png" width = 200px height = 175px>

 
 - **Scatter plot MilesPerGallon_Displacement:** Vehicles with more displacement values have higher fuel-consumption and vehicles with less displacement values have fewer consumption fuel but the plot has some outlier values, so displacement isn't the only variable that affects fuel consumption in miles per gallon. The regression line confirms the strong negative correlation between the two variables displacement and Miles per gallon.The regression analysis has demonstrated that the displacement variable does not explain well the mpg variable and this plot supports the hypothesis made in the regression analysis.
   
    <img src = "grafici\MilesPerGallon_Displacement.png" width = 200px height = 175px>



 
 - **MilesPerGallon-Performance scatterplot:** The plot show a reverse trend between fuel-consumption in miles per gallon and the power-to-weight ratio of vehicles(vehicles with the highest performances have higher fuel-consumpiton), however even if this trend is clear, there are some outlier values and therefore other variables influence fuel consumption.The regression line confirm the negative correlation between the two variables performance and miles per gallon but in this case the negative correlation is not strong as for example displacement and miles per gallon variables so the only performance variable is not enough to explain the variability in miles per gallon variable.This plot as the MilesPerGallon_Displacement plot confirm the regression analysis.

     <img src = "grafici\MilesPerGallon_Performance.png" width = 200px height = 175px>


 
 - **MilesPerGallon-horsepower scatterplot:** The plot show the negative correlation between the variables miles per gallon and horsepower, the regression line is inclined downawards and that's confirm the negative correlation between the two variables, the points that deviate most from the regression line are still in line with the general trend. The plot has no outlier values. Most of the points are clustered around the regression line and this means that horsepower is a strong predictor of the miles per gallon variable. This plot confirm the regression analysis: horsepower variable is a strong predictor of mpg variable

      <img src ="grafici\MilesPerGallon_horsepower.png" width = 200px height = 175px> 



 
 - **MilesPerGallon-weight scatterplot:** The ploth shows a very strong negative correlation between vehicle weight and Miles Per Gallon. The heavier the vehicle, the less fuel efficient it is. The points are almost all grouped around the regression line, this ploth have no outliers and therefore the weight variable as the horsepower variable is a strong predictor of the variable miles per gallon.

      <img src = "grafici\MilesPerGallon_Weight.png" width = 200px height = 175px>



 
 - **MilesPerGallon-QuarterMileTime scatterplot:** The plot shows a weak positive correlation between the two variables but the correlation is not strong so there are other factors that influence the two variables Miles per Gallon and Quarter Mile Time.

      <img src = "grafici\MilesPerGallon-QuarterMileTime.png" width = 200px height = 175px>


 
 - **MilesPerGallon-Transmission boxplot:** Vehicles with manual transmission(1) have high miles per gallon values(fewer fuel consumption) and vehicles with automatic transmission(0) have lower miles per gallon values(higher fuel-consumption). The median value for vehicles with manual transmission is higher than vehicles with automatic transmission. The interquartile range is wider for manual transmission vehicles than for automatic transmission vehicles, meaning that there is more variability in miles per gallon fuel economy figures for manual transmission vehicles.

      <img src = "grafici\MilesPerGallon_Transmission.png" width = 200px height = 175px>


 
 - **MilesPerGallon-EngineShape boxplot:** Vehicles with V-shaped engines(0) have lower median than vehicles with Straight engines(1) so the vehicles with V-shaped engines have higher fuel-consumption than vehicles with straight engines.The interquartile range of vehicles with V-shaped engines is less wide than the interquartile range of vehicles with straight engines this means that the variability of fuel-consumption in V-shaped engines is less than the fuel-consumption variability in straight engines.

    <img src = "grafici\MilesPerGallon_EngineShape.png" width = 200px height = 175px> 

 
 - **MilesPerGallon-carburators boxplot:** The  vehicles with 1 or 2 carburators are the most efficient about fuel-consumption and the vehicles with 6 or 8 carburatos are the least efficient.

    <img src = "grafici\MilesPerGallon_Carburators.png" width = 200px height = 175px>
     ### The most revelant plots are **MilesPerGallon-horsepower scatterplot** and **MilesPerGallon-weight scatterplot** because in this plots we can see a strong negative correlation and no outlier values and therefore they confirm the results of the correlation analysis and the regression model.

## Conclusion:
Weight and horsepower variables are the main predictors of the fuel-consumption in Miles per Gallon, the correlation between fuel consumption and other variables is explained by the weight and horsepower variables. The model explains 88.56% of the fuel consumption variability.