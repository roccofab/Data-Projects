#DESCRIPTION:   Script for preliminary exploration of the 'mtcars' dataset.
#               The mtcars dataset is a built-in dataset in R that contains measurements on 11
#                    different attributes for 32 different cars.
#               I need to explore the dataset and its variables to find
#                  the variables that most influnce vehicles consumption in Miles per Gallon
#                   and performances
               

#VARIABLES:      mpg->Miles Per Gallon
#                cyl->Number of cylinders
#                disp->Displacement
#                hp->Horsepower
#                drat->Rear axle ratio
#                wt->weight(lbs)
#                qsec->1/4 mile time
#                vs->engine shape(0:V-shape, 1:straight)
#                am->transmission(0:Automatic, 1:Manual)
#                gear->Number of gears
#                carb->Number of carburetors

#MAIN PURPOSES:  1.Explore the dataset and its features.
#                2.Identify the variables that most influence the mpg variable by using
#                     scatter plots and boxplots.
#                3.Custom dataframe construction containing the main columns of mtcars dataset,
#                    explore the dataframe and use it to generate plots.

#                4.Scatter plot MilesPerGallon_cylinders to compare vehicles's number of cylinders and its consumtpion in miles per gallon:
#                     -Generally vehicles with fewer cylinders(smaller engines) can make more miles per gallon:
#                         4 cylinders vehicles can make from more than 20 miles to more than 30 miles per gallon.
#                         6 cylinders vehicles can make from more than 15 to less than 25 miles per gallon.
#                         8 cylinders vehicles can make from 10 to 20 miles per gallon.
#                     -CONCLUSION:Vehicles that have more cylinders consume more fuel than vehicles that have fewer cylinders.
#                                  The regression line is inclined downwards and this confirms that as the number of cylinders increases the efficiency in miles per gallon tends to decrease.

#                5.Scatter plot MilesPerGallon_Displacement:
#                    -Generally vehicles with larger engine displacement values have lower Miles Per Gallon ratings(high fuel consumption),
#                        and vehicles with smaller engine displacement values have higher Miles Per Gallon rating(low fuel consumption):
#                          -Vehicles that have displacement values fewer than 100 can make from 25 to more than 30 miles per gallon..
#                          -Vehicles that have displacement values between 100 and less than 200 can make from more than 15 to 25 miles per gallon.
#                          -Vehicles that have displacement values between 200 and 300 can make from 15 to less than 25 miles per gallon.
#                          -Vehicles that have displacement values between 300 and less than 400 can make from more than 10 to less than 20 miles per gallon.
#                          -Vehicles that have 400 and more than 400 displacement values can make from 10 to less than 20 miles per gallon.
#                     -OUTLIER VALUES:The plot show some vehicles with 400 and more than 400 displacement values that can make from 15 to less than 20 miles per gallon,
#                                          these vehicles deviate from the average trend identified by the regression line more than the other vehicles.
#                     CONCLUSION: Vehicles with more displacement values have higher consumption fuel and vehicles with less displacement values have fewer consumption fuel
#                                    but displacement isn't the only variable that affects fuel consumption in miles per gallon.
#                                    The regression line confirms the strong negative correlation between the two variables displacement and Miles per gallon.


#               6.Histogram MilesPerGallon:
#                   -Most vehicles have fuel consumption in miles per gallon from 15 to 20 miles per gallon(about 12 vehicles),
#                       6-7 vehicles have fuel consumption in miles per gallon from 20 to 25 miles per gallon,
#                       few vehicles have fuel consumption in miles per gallon of more than 30 miles per gallon,
#                       5-6 vehicles have fuel consumption in miles per gallon of less than 15 miles per gallon.
#                  -CONCLUSION:The histogram is skewed to the right(few very efficient cars, many cars with average consumption).

#               7.Histogram performances:
#                  -About 12-13 vehicles have performances values in range 35-45, about 10 vehicles have the performance value around 50,
#                       the vehicles with the lowest performances values are very few (about 1-2), the vehicles with the highest performances values are 3-4.
#                  -CONCLUSION:The most common performance value in vehicles is between 40 and 50, there is a high level of variation in performance values,
#                                 the histogram is skewed to the right.

#               8.MilesPerGallon-Performance scatterplot:
#                 -Generally vehicles with lower performance values have larger miles per gallon values(fewer fuel-consumption) and vehicles with larger perfromance values
#                     have lower miles per gallon values(larger fuel-consumption)this means that there is a negative correlation between the two variables but the plot
#                     contains many outlier values.
#                 -OUTLIER: The vehicle with mpg 15 and performance 90(it has the highest performance but a very low fuel-consumption value),
#                           the vehicle with mpg 30 and performance 30(it has high fuel-consumption value but low performances),
#                           ...
#                 -CONCLUSION:The plot show a reverse trend between fuel-consumption in miles per gallon and the power-to-weight ratio of vehicles(vehicles with the highest performances have
#                               higher fuel_consumpiton), however even if this trend is clear, there are some outlier values and therefore other variables influence fuel consumption.
#                               The regression line confirm the negative correlation between the two variables performance and miles per gallon but in this case
#                                    the negative correlation is not strong as for example displacement and miles per gallon variables so the only performance variable
#                                    is not enough to explain the variability in miles per gallon variable.


#               9.MilesPerGallon-horsepower scatterplot:
#                 -Generally vehicles with fewer horsepower have larger miles per gallon values(fewer fuel-consumption)
#                     and vehicles with more horsepower have lower miles per gallons values(larger fuel-consumption) so there's a negative correlation between the two variables.
#                 -CONCLUSION:The plot show the negative correlation between the variables miles per gallon and horsepower, the regression line is inclined downawards and that's confirm
#                                the negative correlation between the two variables, the points that deviate most from the regression line are vehicles
#                                with a much higher number of horsepower than the average but still have a very low mpg value and therefore these points are in line with the general trend.
#                                The plot has no outlier values so vehicles with high horsepower have low miles per gallon value(higher fuel-consumption) and vehicles with low horsepower
#                                have high miles per gallon values(lower fuel-consumption).
#                                Most of the points are clustered around the regression line and this means that horsepower is a strong predictor of the miles per gallon variable. 


#               10.MilesPerGallon-weight scatterplot:
#                  -Generally vehicles heavy vehicles have low miles per gallon values(higher fuel-consumption and light vehicles have high miles per gallon values(fewer fuel-consumption).
#                     Most vehicles have a weight between more than 2000lbs-4000lbs and miles per gallon values between 15 and less than 25.
#                     Vehicles that have a weight of more than 5000lbs have very low mpg values(very high fuel-consumption).
#                     A few vehicles deviate from the regression line but they're still in line with the general trend.
#                  -CONCLUSION: The ploth shows a very strong negative correlation between vehicle weight and Miles Per Gallon. The heavier the vehicle, the less fuel efficient it is.
#                               The points are almost all grouped around the regression line, this ploth have no outliers and therefore the weight variable as the horsepower variable is
#                               a strong predictor of the variable miles per gallon.


#               11.MilesPerGallon-QuarterMileTime scatterplot:
#                  -Generally the plot show a weakly increasing trend(positive correlation) between the two variables miles per gallon and quarter mile time: 
#                       as miles per gallon increases, quarter mile time tends to increase vehicles with lower fuel-consumption rating are slower than the vehicles with an higher-consumption
#                       rating. The plot show some outlier values.
#                  -OUTLIER: The vehicle with the mpg value between 20-25 and qsec value more than 22 is the fastest vehicle of the distribution and it has medium-high fuel-consumption value.
#                            The vehicle with the mpg value 20 and qsec value 20 and the vehicle with the mpg value 25 and qsec value 20.
#                            ...
#                  -CONCLUSION: The plot shows a weak positive correlation between the two variables but the correlation is not strong so there are other factors
                                that influence the two variables Miles per Gallon and Quarter Mile Time.

#               12.MilesPerGallon-Transmission boxplot:
#                  -Vehicles with manual transmission(1) have high miles per gallon values(fewer fuel consumption) and vehicles with automatic transmission(0) have lower miles per gallon
#                       values(higher fuel-consumption). The median value for vehicles with manual transmission is higher than vehicles with automatic transmission.
#                       The interquartile range is wider for manual transmission vehicles than for automatic transmission vehicles, meaning that there is more variability
#                           in miles per gallon fuel economy figures for manual transmission vehicles.
#                  -CONCLUSION: Vehicles with manal transmission(1) have lower fuel-consumption and vehicles with automatic transmission consume more fuel.

#               13.MilesPerGallon-EngineShape boxplot:
#                 -Vehicles with V-shaped engines(0) have lower median than vehicles with Straight engines(1) so the vehicles with V-shaped engines have higher fuel-consumption than vehicles 
#                     with straight engines.The interquartile range of vehicles with V-shaped engines is less wide than the interquartile range of vehicles with straight engines this means
#                     that the variability of fuel-consumption in V-shaped engines is less than the fuel-consumption variability in straight engines.
#                     The plot contains an outlier values between 20-25 mpg range,this outlier value represents a very efficient V-engined vehicle.
#                 -CONCLUSION:Cars with straight engines (1) have lower fuel-consumption than those with V engines (0).


#              14.MilesPerGallon-carburators boxplot:
#                 -Vehicles with 1 carburator: wide interquartile range and high median, this means that vehicles with 1 carburator have low fuel-consumption.
#                  Vehicles with 2 carburators: medium interquartile range and medium median, this means that these vehicles have a little bit lower fuel efficiency
#                      than those with 1 carburator.
#                  Vehicles with 3 carburators have low fuel-efficiency but less than vehicles with 1 or 2 carburators and the interquartile range is tight and this means that
#                      there is little variability about fuel consumption in 3-carb vehicles.  
#                  Vehicles with 4 carburators have lower fuel-efficiency than the vehicles with 1,2 or 3 carburators and in this category of vehicles there is high variability.
#                  Vehicles with 6 or 8 carburators are about 2 and they both have low fuel-efficiency.
#                -CONCLUSION: The  vehicles with 1 or 2 carburators are the most efficient about fuel-consumption and the vehicles with 6 or 8 carburatos are the least efficient.





library(dplyr)
library(corrplot)

setwd("C:/Users/lenovo/Desktop/python_tutorial/Analisi_Dati/RStudio/exercise/grafici")

data(mtcars)
str(mtcars)
head(mtcars)

#create matrix using dataset's columns mpg,hp,wt,carb:
mat = as.matrix(mtcars[, c('mpg', 'hp', 'wt', 'carb')])
mat


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
print(mtcars_df)
table(mtcars_df$gears == 5)
mtcars_df$performance = mtcars_df$horsepower/mtcars_df$weight  #add a new column performance to the dataframe
print(mtcars_df) 
dim(mtcars_df) #dataframe dimensions
dim(mtcars_df)[1]  #number of rows
dim(mtcars_df)[2]  #number of columns
arrange(mtcars_df,horsepower)  #sort df rows by horsepower


#Miles Per Gallon histogram:
png("Histogram_MilesPerGallon.png")
hist(mtcars_df$Miles_Per_Gallon, main = "Miles Per Gallon trend in the dataset")
dev.off()


#vehicles performances histogram:
png("histogram_performances.png")
hist(mtcars_df$performance, main = "performance values of the vehicles")
dev.off()



#Scatterplot mpg_cyl:
png("MilesPerGallon_cylinders.png")
plot(mtcars_df$Miles_Per_Gallon, mtcars_df$cylinders,
     col = "black",
     xlab = "mpg",
     ylab = "cyl",
     main = "Miles Per Gallon-Number of cylinders trend",
     pch = 19)
abline(lm(cylinders~Miles_Per_Gallon, data = mtcars_df), col = "red", lty = 2)
dev.off()


#Scatterplot mpg_disp:
png("MilesPerGallon_Displacement.png")
plot(mtcars_df$Miles_Per_Gallon, mtcars_df$displacement,
     col = "black",
     xlab = "mpg",
     ylab = "disp",
     main = "Miles Per Gallon-Displacement trend",
     pch = 19)
abline(lm(displacement~Miles_Per_Gallon, data = mtcars_df), col = "red", lty = 2)
dev.off()



#Miles per Gallon-perfomance scatter plot:
png("MilesPerGallon_Performance.png")
plot(mtcars_df$Miles_Per_Gallon,mtcars_df$performance,
     col = "black",
     xlab = "mpg",
     ylab = "performance",
     main = "Miles Per Gallon and  vehicle's power-to-weight ratio trend")
abline(lm(performance~Miles_Per_Gallon, data = mtcars_df), col = "red", lty = 2)
dev.off()


#Miles per Gallon-horsepower scatterplot:
png("MilesPerGallon_horsepower.png")
plot(mtcars_df$Miles_Per_Gallon,mtcars_df$horsepower,
     col = "black",
     xlab = "mpg",
     ylab = "hp",
     main = "Miles Per Gallon and vehicles's horsepower trend")
abline(lm(horsepower~Miles_Per_Gallon, data = mtcars_df), col = "red", lty = 2)
dev.off()


#Miles per Gallon-weight scatterplot:
png("MilesPerGallon_Weight.png")
plot(mtcars_df$Miles_Per_Gallon, mtcars_df$weight,
     col = "black",
     xlab = "mpg",
     ylab = "weight",
     main = "Miles Per Gallon and vehicles's weight")
abline(lm(weight~Miles_Per_Gallon, data = mtcars_df), col = "red", lty = 2)
dev.off()


#Miles Per Gallon-Quarter Mile Time:
png("MilesPerGallon-QuarterMileTime.png")
plot(mtcars_df$Miles_Per_Gallon, mtcars_df$Quarter_Mile_Time,
     col = "black",
     xlab = "mpg",
     ylab = "qsec",
     main = "Miles Per Gallon and vehicles's Quarter Mile Time")
abline(lm(Quarter_Mile_Time~Miles_Per_Gallon, data = mtcars_df), col = "red", lty = 2)
dev.off()


#cast the column Transmission(automatic/manual) to factor: 
transmission_factor = as.factor(mtcars_df$Transmission)
print(table(transmission_factor))

#MilesPerGallon-transmission type boxplot
png("MilesPerGallon_Transmission.png", width = 700)
boxplot(mtcars_df$Miles_Per_Gallon~transmission_factor, data = mtcars_df,
        col = "skyblue",
        main = "Miles Per Gallon distribution by transmission type(o-Automatic,1-Manual)",
        xlab = "transmission",
        ylab = "mpg")
dev.off()


#cast the column engine_shape(V-shaped engine, straight engine) to factor:
shape_factor = as.factor(mtcars_df$engine_shape)
print(table(shape_factor))

#MilesPerGallon_EngineShape boxplot:
png("MilesPerGallon_EngineShape.png", width = 700)
boxplot(mtcars_df$Miles_Per_Gallon~mtcars_df$engine_shape,
        col = "skyblue",
        main = "Miles Per Gallon distribution by engine shape(0-V shaped engine, 1-Straight engine)",
        xlab = "shape",
        ylab = "mpg")
dev.off()


#cast the column carburators to factor:
carb_factor = as.factor(mtcars_df$carburators)
print(table(shape_factor))

#MilesPerGallon_Carburators boxplot:
png("MilesPerGallon_Carburators.png", width = 700)
boxplot(mtcars_df$Miles_Per_Gallon~mtcars_df$carburators,
        col = "skyblue",
        main = "Miles Per Gallon distribution by number of carburators",
        xlab = "carburators",
        ylab = "mpg")
dev.off()


#Pie chart representation of vehicles divided into categories based on their miles per gallon consumption
mpg_categories = cut(mtcars_df$Miles_Per_Gallon,
                     breaks = c(10, 15, 20, 25, 30, Inf),
                     labels = c('(10, 15]', '(15, 20]', '(20, 25]', '(25, 30]', '>30'),
                     right = TRUE)
#count the number of vehicles in each category
category_counts = table(mpg_categories)
category_percentages = prop.table(category_counts) * 100
colors = c('red','blue','yellow', 'green', 'purple')
png('MilesPerGallon_Categories_PieChart.png', width = 1200, height = 1000)
pie(category_percentages,
    main = 'Percentage of vehicles based on miles per gallon fuel consumption',
    col = colors,
    cex = 1.8,
    labels = paste0(round(category_percentages, 1), '%'))  #show percentage as plot labels
#insert legend to the plot
legend('topright',
       legend = names(category_percentages),
       fill = colors,
       title = 'MPG Ranges',
       cex = 1.5)  

dev.off()


#main summary statistics of the numeric columns of the mtcars dataset:
#mpg, disp,hp,wt,gear, carb and performance
#represent the calculated statistics in a matrix:
mg_stats = c(mean(mtcars$mpg, na.rm = TRUE),
             median(mtcars$mpg, na.rm = TRUE),
             sd(mtcars$mpg, na.rm = TRUE))

disp_stats = c(mean(mtcars$disp, na.rm = TRUE),
               median(mtcars$disp, na.rm = TRUE),
               sd(mtcars$disp, na.rm = TRUE))

hp_stats = c(mean(mtcars$hp, na.rm = TRUE),
             median(mtcars$hp, na.rm = TRUE),
             sd(mtcars$hp, na.rm = TRUE))

wt_stats = c(mean(mtcars$wt, na.rm = TRUE),
             median(mtcars$wt, na.rm = TRUE),
             sd(mtcars$wt, na.rm = TRUE))

gear_stats = c(mean(mtcars$gear, na.rm = TRUE),
               median(mtcars$gear, na.rm = TRUE),
               sd(mtcars$gear, na.rm = TRUE))

carb_stats = c(mean(mtcars$carb, na.rm = TRUE),
               median(mtcars$carb, na.rm = TRUE),
               sd(mtcars$carb, na.rm = TRUE))

performance_stats = c(mean(mtcars_df$performance, na.rm = TRUE),
                  median(mtcars_df$performance, na.rm = TRUE),
                  sd(mtcars_df$performance, na.rm = TRUE))

stats_matrix = matrix(c(mg_stats,disp_stats,hp_stats,wt_stats,gear_stats,carb_stats,performance_stats),
                      nrow = 3,
                      byrow = FALSE)
colnames(stats_matrix) = c("Miles-Per-Gallon", "Displacement", "Horsepower", "Weight", "Gears", "Carburators", "Performance")
rownames(stats_matrix) = c("Mean", "Median", "Standard deviation")
print(stats_matrix)

