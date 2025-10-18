
from datetime import date
from src.data_acquisition import Historic_Weather_Data as hwd
from src.data_acquisition import Cleaning as c
from src.Simulator_Engine.ProductionData_Generator import update_oil_revenue_in_db
from src.data_acquisition import save_weather_data, save_production_data, save_consumption_cost_data
from src.eda import eda_metrics, eda_plots
import pandas as pd
import numpy as np
import requests
"""
hourly_df, daily_df = hwd.fetch_historic_data()
hourly_df, daily_df = c.handle_timezone(hourly_df, daily_df)
daily_df = c.handle_daylight_duration(daily_df)
merged_df = c.merge_dataframes(hourly_df, daily_df)
merged_df = c.handle_NaN_values(merged_df)
save_weather_data.save_df(merged_df, table_name="weather_data")


save_production_data.generate_production_data_table()
save_consumption_cost_data.generate_consumption_table()
update_oil_revenue_in_db()
"""


df = eda_metrics.harvest_efficiency_per_year()
print("Net Yield per Hectare:")
print(df)

df = eda_metrics.weather_data_yearly_trend()
print("Weather Data Yearly Trend:")
print(df)

df = eda_metrics.oil_yield_per_year()
print("Oil Yield per Hectare:")
print(df)

df = eda_metrics.oil_yield_trend()
print("Oil Yield Trend:")
print(df)

df = eda_metrics.oil_profit_trend()
print("Oil Profit Trends:")
print(df)

df = eda_metrics.avg_oil_per_plant()
print("Average Oil per Plant and Average Percentage of Oil Extracted from the Fruits of the Plants:")
print(df)

df = eda_metrics.top5_production_years()
print("Top 5 Production Years:")
print(df)

df = eda_metrics.lowest5_production_years()
print("Lowest 5 Production Years:")
print(df)

df = eda_metrics.top5_highest_profit_years()
print("Top 5 Highest Profit Years:")
print(df)

df = eda_metrics.top5_lowest_profit_years()
print("Top 5 Lowest Profit Years:")
print(df)

df = eda_metrics.extreme_weather_years_vs_production()
print("Extreme Weather Years vs Production:")
print(df)

df = eda_metrics.harvestDays_vs_surface()
print("Harvest Days vs Surface Area:")
print(df)

print("Coefficient of Variation of Net Yield:\n", eda_metrics.yield_variability())

print("Coefficient of Variation of Oil Revenue:\n", eda_metrics.oil_revenue_variability())

df = eda_metrics.yield_growth_rate()
print("Annual Net Yield Growth Rate:")
print(df)

df = eda_metrics.avg_numplants_per_year()
print("Average Number of New Plants per Year:")
print(df)

df = eda_metrics.total_cost_per_year()
print("Total Cost per Year:")
print(df)

df, correlation = eda_metrics.irrigation_efficiency_vs_yield()
print("Irrigation Efficiency vs Net Yield:")
print(df)

df = eda_metrics.most_expensive_year_vs_yield()
print("Most Expensive Year vs Yield:")
print(df)

df = eda_metrics.best_production_vs_treatments()
print("Best Production Year vs Soil Treatments:")
print(df)

df = eda_metrics.least_expensive_years_vs_yield()
print("Least Productive Year vs Expenses:")
print(df)

df = eda_metrics.highest_revenue_year_vs_expenses()
print("Highest Revenue Year vs Expenses:")
print(df)

df = eda_metrics.cost_per_ton_yield()
print("Cost per Ton of Yield:")
print(df)

df = eda_metrics.cost_per_kg_yield()
print("Cost per Kg of Yield:")
print(df)

df = eda_metrics.cost_per_l_oil()
print("Cost to Produce 1 Liter of Oil:")
print(df)

df = eda_metrics.profit_per_hectare()
print("Profit per Hectare:")
print(df)

corr_coeff = eda_metrics.annual_precipitation_vs_yield()
print("Precipitation vs Oil Yield Correlation Coefficients:")
print(corr_coeff)

corr_coeff = eda_metrics.annual_precipitation_vs_revenue()
print("Precipitation vs Oil Revenue Correlation Coefficients:")
print(corr_coeff)


"""
eda_plots.netyield_per_hectare_plot()
eda_plots.top_lowest_production_plot()
eda_plots.netyield_per_plant_plot()
eda_plots.oil_yield_trend_plot()
eda_plots.cost_per_liter_oil_plot()
eda_plots.cost_per_ton_yield_plot()
eda_plots.cost_per_kg_yield_plot()
eda_plots.oil_price_per_year()
eda_plots.profit_per_year_plot()
eda_plots.top_lowest_profit_plot()
eda_plots.profit_per_hectare_plot()
eda_plots.harvestDays_vs_surface_plot()
eda_plots.plants_per_year_plot()
eda_plots.expenses_per_year_plot()
eda_plots.mostExpensive_leastExpensive_years_plot()
eda_plots.treatments_expenses_years_plot()
eda_plots.fertilizer_required_years_plot()
eda_plots.pesticide_required_years_plot()
eda_plots.irrigation_required_years_plot()
eda_plots.prod_weather_corr_heatmap()
eda_plots.prod_cons_weather_corr_heatmap()
"""

