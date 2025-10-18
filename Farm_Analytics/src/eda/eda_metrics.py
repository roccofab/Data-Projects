import numpy as np
from src.Simulator_Engine.Consumption_Cost_Generator import get_weather_data, get_production_data
from src.utils.date_utils import check_for_current_month
from src.data_acquisition.DBConnection import DBConnection
import pandas as pd
import datetime as dt
import mysql.connector
from mysql.connector import errors as msc_error

def get_consumption_data():
    try:
        db = DBConnection()
        conn = db.get_mysql_connection()
        query = "SELECT * FROM consumption_data"
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        print(f"Error retrieving consumption data: {e}")
        return pd.DataFrame()
    except msc_error.InterfaceError as e:
        print(f"MySQL database connection error: {e}")
        return pd.DataFrame()
    except msc_error.ProgrammingError as e:
        print(f"MySQL programming error while retrieving data from weather_data table: {e}")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error: {e}")
        return pd.DataFrame()
    finally:
            conn.close()

def get_data():
    weather_data = get_weather_data()
    production_data = get_production_data()
    consumption_data = get_consumption_data()
    return weather_data, production_data, consumption_data

def get_stats():
    weather_data, production_data, consumption_data = get_data()
    return weather_data.describe(), production_data.describe(), consumption_data.describe()

def aggregate_weather_data():
    """
    Aggregate daily weather data to yearly level.

    Returns:
        pd.DataFrame: Aggregated DataFrame with yearly weather features.
    """
    weather_data = get_weather_data()
    # Convert date column to datetime
    weather_data['date'] = pd.to_datetime(weather_data['date'], errors='coerce')
    weather_data['year'] = weather_data['date'].dt.year
    return weather_data.groupby('year').agg(
        avg_temp=('temperature_2m', 'mean'),
        total_precip=('precipitation', 'sum'),
        avg_wind=('wind_speed_10m', 'mean')
    ).reset_index()

def find_extreme_weather_years(db):
    """
    Get the years having extreme weather conditions from the weather_data table.
    - Retrieve data from weather_data table for each year and count the number od days for each year as days_in_year.
    
    - Calculate the ratio of cold days, windy days, and total precipitation to the days in year.
      The years having extreme weather conditions are determined based on specific weather criteria:
        - Cold days: More than 60 days  with temperature below 3°C: 
               
        - Windy days: More than 10 days with wind speed above 50 km/h: 
               
               
        - Total precipitation: Less than 300 mm or more than 700 mm
        
    -This data can be used as a loss factor in olive production simulation.
    
    Returns:
        list: A list of years with extreme weather conditions.
    """
    try:
        query = f"""
            SELECT
                YEAR(date) AS year,
                COUNT(*) AS days_in_year,
                SUM(CASE WHEN temperature_2m < 3 THEN 1 ELSE 0 END) AS cold_days,
                SUM(CASE WHEN wind_speed_10m > 50 THEN 1 ELSE 0 END) AS windy_days,
                SUM(precipitation) AS total_precip
            FROM weather_data
            GROUP BY YEAR(date)
        """
        df = pd.read_sql(query, db)

        bad_weather_years = df[
            (df['cold_days'] > 30) | 
            (df['windy_days'] > 10) | 
            (df['total_precip'] > 700) | 
            (df['total_precip'] < 300)
        ]['year'].tolist()
        return bad_weather_years
    except TypeError as e:
        print(f"TypeError in weather data: {e}")
        return []
    except Exception as e:
        print(f"Error in find_extreme_weather_years(db): {e}")
        return []

def harvest_efficiency_per_year():
    """
    Calculates the net yield per hectare for each year.
    Function first converts surface area from square meters to hectares,
      then calculates the net yield per hectare.
      
     Returns:
        pd.DataFrame: DataFrame with the year, surface area in hectares,
                      and the net yield per hectare.
    """
    try:
        df = get_production_data()
        current_year = dt.date.today().year
        current_month = dt.date.today().month
        #excludes the current year if the month of October has not yet been reached
        if current_month < 10:   
            df = df[df["year"] < current_year]
        df['surface_area_in_hectare'] = df['surface_area_in_m2'] / 10000
        df['net_yield_per_hectare'] = df['net_qty'] / df['surface_area_in_hectare']
        return df[['year', 'surface_area_in_hectare', 'net_yield_per_hectare']]
    except Exception as e:
        print(f"Error calculating harvest efficiency(harvest_efficiency_per_year()): {e}")
        return pd.DataFrame()

def avg_yield_per_plant():
    """
    Calculates the average yield per plant for each year.
    Function first calculates the average yield per plant.
    
    Returns:
        pd.DataFrame: DataFrame with the year and the average yield per plant.
    """
    try:
        df = get_production_data()
        df['avg_yield_per_plant'] = df['net_qty'] / df['plants_counter']
        return df[['year', 'avg_yield_per_plant']]
    except Exception as e:
        print(f"Error calculating average yield per plant(avg_yield_per_plant()): {e}")
        return pd.DataFrame()

def oil_yield_per_year():
    """
    Calculates the oil yield per hectare for each year.
    Function first converts surface area from square meters to hectares,
      then calculates the oil yield per hectare.

     Returns:
        pd.DataFrame: DataFrame with the year, surface area in hectares,
                      and the oil yield per hectare.
    """
    try:
        df = get_production_data().sort_values(by = 'year').copy()
        current_year = dt.date.today().year
        current_month = dt.date.today().month
        #excludes the current year if the month of October has not yet been reached
        if current_month < 10:   
            df = df[df["year"] < current_year]
            
        df['surface_area_in_hectare'] = df['surface_area_in_m2'] / 10000
        df['oil_yield_per_hectare'] = df['oil_yield'] / df['surface_area_in_hectare']
        return df[['year', 'surface_area_in_hectare', 'oil_yield_per_hectare']]
    except Exception as e:
        print(f"Error calculating oil yield per hectare(oil_yield_per_year()): {e}")
        return pd.DataFrame()
    
def weather_data_yearly_trend():
    try:
        df = get_weather_data().copy()
        df['date'] = pd.to_datetime(df['date'])
        df['year'] = df['date'].dt.year
        df = df.groupby('year').agg({
            'temperature_2m' : 'mean',
            'precipitation' : 'sum',
            'wind_speed_10m' : 'mean',
            'daylight_duration': 'mean'
        }).reset_index()
        
        #calculate trend
        df['temperature_trend'] = df['temperature_2m'].diff()
        df['total_precipitation_trend'] = df['precipitation'].diff()
        df['wind_speed_trend'] = df['wind_speed_10m'].diff()
        df['daylight_duration_trend'] = df['daylight_duration'].diff()
        
        return df[['year', 'temperature_trend', 'total_precipitation_trend', 'wind_speed_trend', 'daylight_duration_trend']]
    except Exception as e:
        print(f"Error calculating weather data trend(weather_data_trend()): {e}")
        return pd.DataFrame()

def oil_yield_trend():
    """
    Analyzes the trend of oil yield over the years.
    Function calculates the difference in oil yield per hectare then format the values with a plus/minus sign.
    
    Returns:
        pd.DataFrame: DataFrame with the year and the oil yield trend.
    """
    try:
        df = get_production_data().copy()
        current_year = dt.date.today().year
        current_month = dt.date.today().month
        #excludes the current year if the month of October has not yet been reached
        if current_month < 10:   
            df = df[df["year"] < current_year]
        df['diff'] = df['oil_yield_pct'].diff()
        df['oil_yield_trend'] = df['diff'].apply(lambda x : f"+{x:.2f}%" if x > 0 else (f"{x:.2f}%" if x < 0 else None if pd.isna(x) else 0))
        return df[['year', 'oil_yield_trend']]
    except Exception as e:
        print(f"Error calculating oil yield trend(oil_yield_trend()): {e}")
        return pd.DataFrame()

def oil_profit_trend():
    """
    Analyzes the trend of oil revenue over the years.
    Function calculates the difference between year revenue and year expenses then format the values with a plus/minus sign.
    
    Returns:
       pd.DataFrame: DataFrame with the year, oil revenue trend in € and oil revenue percentage.
    """
    try:
        production_data = get_production_data().copy()
        consumption_data = get_consumption_data().copy()
        df = pd.merge(production_data, consumption_data, on='year', how='inner')
        current_year = dt.date.today().year
        current_month = dt.date.today().month
        #excludes the current year if the month of October has not yet been reached
        if current_month < 10:   
            df = df[df["year"] < current_year]
        df["total_expenses"] = (
            df["irrigation_expenses"] +
            df["fertilizer_costs"] +
            df["pesticide_costs"] +
            df["maintenance_expenses"]
        )
        df['revenue'] = df['oil_revenue']-df['total_expenses']
        #format values
        df['revenue_€'] = df['revenue'].apply(lambda x: f"{x:+.2f}")
        #add the column revenue percentage and handle null values
        df['revenue_percentage'] = df.apply(
            lambda row: (row['revenue'] / row['oil_revenue'] * 100) if row['oil_revenue'] != 0 else 0,
            axis=1
        )
        #format values
        df['revenue_percentage'] = df['revenue_percentage'].apply(lambda x: f"{x:+.2f}%")
        
        return df[['year','revenue_€', 'revenue_percentage']]
    except Exception as e:
        print(f"Error calculating oil revenue trend(oil_revenue_trend()): {e}")
        return pd.DataFrame()

def avg_oil_per_plant():
    """
    Calculates the average oil yield per plant and the average percentage of oil per plant for each year:
       -Calculates the average oil yield per plant in kg
       -Calculates the average fruit yield per plant in kg
       -Calculates the average percentage of oil extracted from the fruits of the plants in kg and %.

    Returns:
        pd.DataFrame: DataFrame with the year,the average oil yield per plant in kg and the average percentage of oil extracted from the fruits of the plants.
    """
    try:
        df = get_production_data()
        current_year = dt.date.today().year
        current_month = dt.date.today().month
        #excludes the current year if the month of October has not yet been reached
        if current_month < 10:   
            df = df[df["year"] < current_year]
        df['avg_oil_per_plant'] = df['oil_yield'] / df['plants_counter']
        # average fruit yield per plant
        df['avg_fruit_per_plant'] = df['net_qty'] / df['plants_counter']

        # average percentage of oil per plant
        df['avg_oil_pct'] = (df['avg_oil_per_plant'] / df['avg_fruit_per_plant']) * 100
        
        return df[['year', 'avg_oil_per_plant', 'avg_oil_pct']]
    except Exception as e:
        print(f"Error calculating average oil per plant(avg_oil_per_plant()): {e}")
        return pd.DataFrame()

def top5_production_years():
    """
    Identifies the top 5 years with the highest net yield and oil yield.
    Integrates the number of plants, average temperature, sum of precipitations, average wind speed, and average daylight duration
      in the resulting 5 years with the lowest production.

    Returns:
        pd.DataFrame: DataFrame with the year, net yield, oil yield, avg_temperature, and sum_precipitations.
    """
    try:
        production_data = get_production_data().copy()
        weather_data = get_weather_data().copy()
        weather_data['date'] = pd.to_datetime(weather_data['date'])
        weather_data['year'] = weather_data['date'].dt.year
        avg_weather = weather_data.groupby('year').agg({
            'temperature_2m': 'mean',
            'wind_speed_10m': 'mean',
            'precipitation': 'sum',
            'daylight_duration': 'mean'
        }).reset_index()
        
        df = pd.merge(production_data,avg_weather, on = 'year', how = 'inner')
        
        top5 = df[['year','plants_counter', 'net_qty', 'oil_yield', 'temperature_2m','wind_speed_10m', 'precipitation','daylight_duration']].nlargest(5, 'net_qty')
        top5 = top5.rename(columns={'temperature_2m': 'avg_temperature', 'precipitation': 'sum_precipitations',
                                    'wind_speed_10m': 'avg_wind_speed', 'daylight_duration': 'avg_daylight_duration'
                                    })
        return top5
    except Exception as e:
        print(f"Error identifying top 5 production years(top5_production_years()): {e}")
        return pd.DataFrame()

def lowest5_production_years():
    """
    Identifies the lowest 5 years with the lowest net yield and oil yield excluding the current year
      if the harvest period has not yet been reached.
    Integrates the number of plants, average temperature, sum of precipitations, average wind speed, and average daylight duration
      in the resulting 5 years with the lowest production.

    Returns:
        pd.DataFrame: DataFrame with the year, net yield, oil yield, avg_temperature, and sum_precipitations.
    """
    try:
        production_data = get_production_data().copy()
        
        weather_data = get_weather_data().copy()
        weather_data['date'] = pd.to_datetime(weather_data['date'])
        weather_data['year'] = weather_data['date'].dt.year
        
        avg_weather = weather_data.groupby('year').agg({
            'temperature_2m': 'mean',
            'wind_speed_10m': 'mean',
            'precipitation': 'sum',
            'daylight_duration': 'mean'
        }).reset_index()
        
        df = pd.merge(production_data,avg_weather, on = 'year', how = 'inner')
        
        current_year = dt.date.today().year
        current_month = dt.date.today().month

        if current_month < 10:
            df = df[df['year'] != current_year]

        lowest5 = df[['year', 'plants_counter', 'net_qty', 'oil_yield', 'temperature_2m','wind_speed_10m', 'precipitation','daylight_duration']].nsmallest(5, 'net_qty')
        lowest5 = lowest5.rename(columns={'temperature_2m': 'avg_temperature', 'precipitation': 'sum_precipitations',
                                          'wind_speed_10m': 'avg_wind_speed', 'daylight_duration': 'avg_daylight_duration'
                                    })
        return lowest5
        
    except Exception as e:
        print(f"Error identifying lowest 5 production years(lowest5_production_years()): {e}")
        return pd.DataFrame()
    
def top5_highest_profit_years():
    """
    Identifies the top 5 years with the highest profit and 
      integrates the average temperature and sum of precipitations in the resulting 5 years with the highest profit.

    profit = oil_revenue - total_expenses

    Returns:
        pd.DataFrame: DataFrame with the year, oil revenue, total expenses, and profit.
    """
    try:
        production = get_production_data().copy()
        consumption = get_consumption_data().copy()
        df = pd.merge(production, consumption, on='year', how='inner')
        df['total_expenses'] = (
            df['irrigation_expenses'] +
            df['fertilizer_costs'] +
            df['pesticide_costs'] +
            df['maintenance_expenses']
        )
        df['profit'] = df['oil_revenue'] - df['total_expenses']
        return df[['year','oil_revenue','total_expenses','profit']].nlargest(5, 'profit')
    except Exception as e:
        print(f"Error identifying top 5 highest profit years(top5_highest_profit_years()): {e}")

def top5_lowest_profit_years():
    """
    Identifies the 5 years with the lowest profit and 
      integrates the average temperature and average precipitation in the resulting 5 years with the lowest profit.

    Returns:
        pd.DataFrame: DataFrame with the year, oil revenue, total expenses, and profit.
    """
    try:
        production = get_production_data().copy()
        consumption = get_consumption_data().copy()
        df = pd.merge(production, consumption, on='year', how='inner')
        current_year = dt.date.today().year
        current_month = dt.date.today().month
         
        #handle the current year
        if current_month < 10:
            df = df[df['year'] != current_year]
            
        df['total_expenses'] = (
            df['irrigation_expenses'] +
            df['fertilizer_costs'] +
            df['pesticide_costs'] +
            df['maintenance_expenses']
        )
        df['profit'] = df['oil_revenue'] - df['total_expenses']
        return df[['year','oil_revenue','total_expenses','profit']].nsmallest(5, 'profit')
    except Exception as e:
        print(f"Error identifying top 5 lowest profit years(top5_lowest_profit_years()): {e}")

def extreme_weather_years_vs_production():
    try:
        db = DBConnection().get_engine()
        bad_weather_years = find_extreme_weather_years(db)
        
        production_data = get_production_data().copy()
        weather_data = get_weather_data().copy()
        
        prod_in_extreme_years = production_data[production_data['year'].isin(bad_weather_years)]
        
        weather_data['date'] = pd.to_datetime(weather_data['date'])
        weather_data['year'] = weather_data['date'].dt.year
        weather_extreme = weather_data[weather_data['year'].isin(bad_weather_years)]
        
        avg_weather_extreme = weather_extreme.groupby('year').agg({
            'temperature_2m': 'mean',
            'wind_speed_10m': 'mean',
            'precipitation': 'sum',
            'daylight_duration': 'mean'
        }).reset_index()

        df = pd.merge(prod_in_extreme_years, avg_weather_extreme, on='year', how='inner')
        
        df = df.rename(columns = {'temperature_2m': 'avg_temperature', 'precipitation': 'sum_precipitations',
                                  'wind_speed_10m': 'avg_wind_speed', 'daylight_duration': 'avg_daylight_duration'})
        
        return df[['year', 'net_qty', 'oil_yield', 'avg_temperature', 'sum_precipitations', 'avg_wind_speed', 'avg_daylight_duration']]
    except Exception as e:
        print(f"Error in extreme_weather_years_vs_production(): {e}")
        return pd.DataFrame()

def harvestDays_vs_surface():
    """
    Analyzes the relationship between harvest days and surface area over the years.
    Function calculates the difference in harvest days and surface area then formats the values with a plus/minus sign.
    
    Returns:
        pd.DataFrame: DataFrame with the year, surface area trend, and harvest days trend.
    """
    try:
        df = get_production_data().sort_values(by = 'year').copy()
        
        current_year = dt.date.today().year
        current_month = dt.date.today().month
        
        #excludes the current year if the month of October has not yet been reached
        if current_month < 10:
            df = df[df["year"] < current_year]
        
        df['surface_diff'] = df['surface_area_in_m2'].diff()
        df['harvest_days_diff'] = df['harvest_days'].diff()
        
        
        df['harvest_days_diff'] = df.apply(
            lambda row: check_for_current_month(row['harvest_days_diff'], row['year']), axis=1
        )
        
        #format values
        df['surface_trend'] = df['surface_diff'].apply(lambda x : f"+{x:.2f}" if x > 0 else (f"-{x:.2f}" if x < 0 else None if pd.isna(x) else 0))
        df['harvest_days_trend'] = df['harvest_days_diff'].apply(lambda x : f"+{x:.2f}" if x > 0 else (f"-{x:.2f}" if x < 0 else None if pd.isna(x) else 0))
        
        return df[['year', 'surface_trend', 'harvest_days_trend']]
    except Exception as e:
        print(f"Error analyzing harvest days vs surface area (harvestDays_vs_surface()): {e}")
        return pd.DataFrame()

def yield_variability():
    """
    Analyzes the variability of net yield over the years by calculating the coefficient of variation (CV).
    
    Coefficient of Variation:
       CV = mean(net_qty)/std(net_qty)
    
    Higher CV value means less variability in net yield over the years.
    Lower CV value suggests high fluctations in net yield and more variability.
    
    Returns:
       float: Coefficient of Variation (CV) of net yield.
    """
    try:
        df = get_production_data().copy()
        current_year = dt.date.today().year
        current_month = dt.date.today().month
        
        # excludes the current year if the month of October has not yet been reached
        if current_month < 10:
           df = df[df['year'] != current_year]
            
        mean_yield = df['net_qty'].mean()
        std_yield = df['net_qty'].std()
        CV = mean_yield / std_yield if std_yield != 0 else np.nan
        return CV.round(2)
    except ZeroDivisionError as e:
        print(f"Error division by zero in yield variability (yield_variability()): {e}")
    except Exception as e:
        print(f"Error calculating yield variability (yield_variability()): {e}")
        return np.nan
    
def oil_revenue_variability():
    """
    Analyzes the variability of oil revenue over the years by calculating the coefficient of variation (CV).
    
    Coefficient of Variation:
       CV = mean(oil_revenue)/std(oil_revenue)
    
    Higher CV value means less variability in oil revenue over the years.
    Lower CV value suggests high fluctations in oil revenue and more variability.
    
    Returns:
       float: Coefficient of Variation (CV) of oil revenue.
    """
    try:
        df = get_production_data().copy()
        current_year = dt.date.today().year
        current_month = dt.date.today().month
        
        # excludes the current year if the month of October has not yet been reached
        if current_month < 10:
           df = df[df['year'] != current_year]
            
        mean_revenue = df['oil_revenue'].mean()
        std_revenue = df['oil_revenue'].std()
        CV = mean_revenue / std_revenue if std_revenue != 0 else np.nan
        return CV.round(2)
    except ZeroDivisionError as e:
        print(f"Error division by zero in oil revenue variability (oil_revenue_variability()): {e}")
    except Exception as e:
        print(f"Error calculating oil revenue variability (oil_revenue_variability()): {e}")
        return np.nan

def yield_growth_rate():
    """
    Calculates the annual growth rate of net yield between consecutive years.
    
    Annual Yield Growth Rate:
       AYGR = (Net Yield in Current Year - Net Yield in Previous Year) / Net Yield in Previous Year * 100

    Positive AYGR value means that the net yield has increased compared to the previous year.
    Negative AYGR value means that the net yield has decreased compared to the previous year.
    
    Returns:
       pd.DataFrame: DataFrame with the year and the annual yield growth rate.
    """
    try:
        df = get_production_data().sort_values(by = 'year').copy()
        current_year = dt.date.today().year
        current_month = dt.date.today().month
        #excludes the current year if the month of October has not yet been reached
        if current_month < 10:   
            df = df[df["year"] < current_year]

        df['net_yield_growth_rate'] = df['net_qty'].pct_change() * 100
        
        return df[['year', 'net_yield_growth_rate']]
    except Exception as e:
        print(f"Error calculating yield growth rate (yield_growth_rate()): {e}")
        return pd.DataFrame()

def avg_numplants_per_year():
    #find the average number of new plants grown each year
    try:
        df = get_production_data().sort_values(by = 'year').copy()
        df["new_plants"] = df["plants_counter"].diff().fillna(0)  # Calculate new plants per year by taking the difference between consecutive years
        df["new_plants"] = df["new_plants"].apply(lambda x: x if x > 0 else 0)  # Set negative values to 0
        return int(df["new_plants"].mean())
    except Exception as e:
        print(f"Error calculating average number of plants per year (avg_numplants_per_year()): {e}")
        return 0
def total_cost_per_year():
    """
    Calculates the total expenses per year by summing irrigation expenses, fertilization expenses, pesticide costs and maintenance expenses.

    Returns:
        pd.DataFrame: DataFrame with the year and the total expenses per year.
    """
    try:
        df = get_consumption_data().copy()
        current_year = dt.date.today().year
        current_month = dt.date.today().month
        #excludes the current year if the month of October has not yet been reached
        if current_month < 10:   
            df = df[df["year"] < current_year]
        df['total_expenses'] = df[['irrigation_expenses', 'fertilizer_costs', 'pesticide_costs', 'maintenance_expenses']].sum(axis = 1)
        return df[['year', 'total_expenses']]
    except Exception as e:
        print(f"Error calculating total cost per year (total_cost_per_year()): {e}")
        return pd.DataFrame()

def irrigation_efficiency_vs_yield():
    """
    Analyzes the relationship between water irrigation in m^3 and net yield in kg for each year.
    
    Irrigation efficiency is defined as:
        (net_qty / irrigation_water_used) * 100
    which represents how many kilograms of olives are produced per unit 
    of irrigation water, expressed as a percentage.
    
    Find the linear correlation between irrigation efficiency and net yield using the Pearson correlation coefficient:
       -1: perfect negative linear correlation
       0: no linear correlation
       1: perfect positive linear correlation
       
    

    Returns:
        pd.DataFrame: DataFrame with the year, irrigation efficiency(kg/m³ * 100), net yield and Pearson correlation coefficient.
    """
    try:
        consumption = get_consumption_data()
        production = get_production_data()

        # Merge DataFrames
        df = pd.merge(consumption, production, on="year", how="inner")
        current_year = dt.date.today().year
        current_month = dt.date.today().month
        #excludes the current year if the month of October has not yet been reached
        if current_month < 10:   
            df = df[df["year"] < current_year]

        df['irrigation_efficiency'] = df.apply(
            lambda row: (row['net_qty'] / row['irrigation_required_m3'] * 100) 
            if row['irrigation_required_m3'] > 0 else 0, 
            axis=1
        )
        correlation = df['irrigation_efficiency'].corr(df['net_qty'], method='pearson')

        return df[['year', 'irrigation_efficiency', 'net_qty']], correlation
    except ZeroDivisionError as e:
        print(f"ZeroDivisionError in irrigation efficiency vs yield (irrigation_efficiency_vs_yield()): {e}")
        return pd.DataFrame(), 0
    except Exception as e:
        print(f"Error calculating irrigation efficiency vs yield (irrigation_efficiency_vs_yield()): {e}")
        return pd.DataFrame(), 0

def most_expensive_year_vs_yield():
    """
    Find the most expensive year in terms of total expenses and get the corresponding net yield.

    Returns:
        pd.DataFrame: DataFrame with the year, the corresponding net yield and total expenses.
    """
    try:
        consumption = get_consumption_data()
        production = get_production_data()
        df = pd.merge(consumption,production, on="year", how="inner")
        df["total_expenses"] = (
            df["irrigation_expenses"] +
            df["fertilizer_costs"] +
            df["pesticide_costs"] +
            df["maintenance_expenses"]
        )

        # Find year with maximum expenses
        most_expensive_year = df["total_expenses"].idxmax()

        return pd.DataFrame({
            "year": [df.loc[most_expensive_year, 'year']],
            "net_yield": [df.loc[most_expensive_year, 'net_qty']],
            "total_expenses": [df.loc[most_expensive_year, 'total_expenses']]
        })
    except Exception as e:
        print(f"Error finding most expensive year vs yield (most_expensive_year_vs_yield()): {e}")
        return pd.DataFrame()
def least_expensive_years_vs_yield():
    """
    Find the least expensive year in terms of total expenses and get the corresponding net yield.

    Returns:
        pd.DataFrame: DataFrame with the year, the corresponding net yield and total expenses.
    """
    try:
        consumption = get_consumption_data()
        production = get_production_data()
        df = pd.merge(consumption,production, on = 'year', how = 'inner')
        current_year = dt.date.today().year
        current_month = dt.date.today().month
        #excludes the current year if the month of October has not yet been reached
        if current_month < 10:   
            df = df[df["year"] < current_year]

        df["total_expenses"] = (
            df["irrigation_expenses"] +
            df["fertilizer_costs"] +
            df["pesticide_costs"] +
            df["maintenance_expenses"]
        )
        
        least_expensive_year = df['total_expenses'].idxmin()
        return pd.DataFrame({
            "year": [df.loc[least_expensive_year, 'year']],
            "net_yield": [df.loc[least_expensive_year, 'net_qty']],
            "total_expenses": [df.loc[least_expensive_year, 'total_expenses']]
        })
    except Exception as e:
        print(f"Error finding least expensive years vs yield (least_expensive_years_vs_yield()): {e}")
        return pd.DataFrame()

def best_production_vs_treatments():
    """
    Find the best productive year in terms of net yield and get the corresponding amount of fertilizer used(kg), fertilization expenses,
    amount of pesticide used(kg) and pesticide costs.

    Returns:
        pd.DataFrame: DataFrame with the year, fertilizer_required_kg, fertilization_costs, pesticide_required_kg and pesticide_costs.
    """
    try:
        consumption = get_consumption_data()
        production = get_production_data()
        df = pd.merge(consumption,production, on = 'year', how='inner')
        best_production_year = df['net_qty'].idxmax()
        return pd.DataFrame({
            "year": [df.loc[best_production_year, 'year']],
            "fertilizer_required_kg": [df.loc[best_production_year, 'fertilizer_required_kg']],
            "fertilization_costs": [df.loc[best_production_year, 'fertilizer_costs']],
            "pesticide_required_kg": [df.loc[best_production_year, 'pesticide_required_kg']],
            "pesticide_costs": [df.loc[best_production_year, 'pesticide_costs']]
        })
    except Exception as e:
        print(f"Error finding best production vs treatments (best_production_vs_treatments()): {e}")
        return pd.DataFrame()

def least_productive_years_vs_treatments():
    """
    Find the least productive year in terms of net yield and get the corresponding amount of fertilizer used(kg), fertilization expenses,
    amount of pesticide used(kg) and pesticide costs.

    Returns:
        pd.DataFrame: DataFrame with the year, fertilizer_required_kg, fertilization_costs, pesticide_required_kg and pesticide_costs.
    """
    try:
        consumption = get_consumption_data()
        production = get_production_data()
        df = pd.merge(consumption,production, on = 'year', how = 'inner')
        least_production_year = df['net_qty'].idxmin()
        return pd.DataFrame({
            "year": [df.loc[least_production_year, 'year']],
            "fertilizer_required_kg": [df.loc[least_production_year, 'fertilizer_required_kg']],
            "fertilization_costs": [df.loc[least_production_year, 'fertilizer_costs']],
            "pesticide_required_kg": [df.loc[least_production_year, 'pesticide_required_kg']],
            "pesticide_costs": [df.loc[least_production_year, 'pesticide_costs']]
        })
    except Exception as e:
        print(f"Error finding least productive years vs treatments (least_productive_years_vs_treatments()): {e}")
        return pd.DataFrame()
    
def highest_revenue_year_vs_expenses():
    """
    Find the highest revenue year in terms of oil revenue and get the corresponding expenses.

    Returns:
        pd.DataFrame: DataFrame with the year, irrigation_costs, fertilization_costs, maintenance_expenses and pesticide_costs.
    """
    try:
        consumption = get_consumption_data()
        production = get_production_data()
        df = pd.merge(consumption,production, on = 'year', how = 'inner')
        highest_revenue_year = df['oil_revenue'].idxmax()
        return pd.DataFrame({
            "year": [df.loc[highest_revenue_year, 'year']],
            "irrigation_expenses": [df.loc[highest_revenue_year, 'irrigation_expenses']],
            "fertilization_expenses": [df.loc[highest_revenue_year, 'fertilizer_costs']],
            "maintenance_expenses": [df.loc[highest_revenue_year, 'maintenance_expenses']],
            "pesticide_costs": [df.loc[highest_revenue_year, 'pesticide_costs']]
        })
    except Exception as e:
        print(f"Error finding highest revenue year vs expenses (highest_revenue_year_vs_expenses()): {e}")
        return pd.DataFrame()

def cost_per_ton_yield():
    """
    Calculate the total expenses to produce one ton of net yield.
    
    Cost per Ton of Yield:
       CTY = Total Expenses / Total Net Yield / 1000
    
    Returns:
        pd.DataFrame: DataFrame with the year and the cost per ton of yield.
    """
    try:
        consumption = get_consumption_data()
        production = get_production_data()
        df = pd.merge(consumption, production, on='year', how='inner')
        current_year = dt.date.today().year
        current_month = dt.date.today().month
        #excludes the current year if the month of October has not yet been reached
        if current_month < 10:   
            df = df[df["year"] < current_year]
            
        df["total_expenses"] = (
            df["irrigation_expenses"] +
            df["fertilizer_costs"] +
            df["pesticide_costs"] +
            df["maintenance_expenses"]
        )
        df["net_qty_ton"] = df["net_qty"] / 1000  # Convert net yield from kg to tons
        df["cost_per_ton_yield"] = df["total_expenses"] / df["net_qty_ton"]
        return df[["year", "cost_per_ton_yield"]]
    except ZeroDivisionError as e:
        print(f"ZeroDivisionError in cost_per_ton_yield(): {e}")
    except Exception as e:
        print(f"Error in cost_per_ton_yield(): {e}")

def cost_per_kg_yield():
    """
    Calculate the total expenses to produce one Kilogram of net yield.
    
    Cost per Kg of Yield:
       CTY = Total Expenses / Total Net Yield
    
    Returns:
        pd.DataFrame: DataFrame with the year and the cost per kg of yield.
    """
    try:
        consumption = get_consumption_data()
        production = get_production_data()
        df = pd.merge(consumption, production, on='year', how='inner')
        current_year = dt.date.today().year
        current_month = dt.date.today().month
        #excludes the current year if the month of October has not yet been reached
        if current_month < 10:   
            df = df[df["year"] < current_year]
        df["total_expenses"] = (
            df["irrigation_expenses"] +
            df["fertilizer_costs"] +
            df["pesticide_costs"] +
            df["maintenance_expenses"]
        )
        df["cost_per_kg_yield"] = df["total_expenses"] / df["net_qty"]
        return df[["year", "cost_per_kg_yield"]]
    except ZeroDivisionError as e:
        print(f"ZeroDivisionError in cost_per_kg_yield(): {e}")
    except Exception as e:
        print(f"Error in cost_per_kg_yield(): {e}")

def cost_per_l_oil():
    """
    Calculate the total expenses to produce one liter of oil.
    
    Cost per Liter of Oil:
       COL = Total Expenses / Total Oil Yield
    
    Returns:
        pd.DataFrame: DataFrame with the year and the cost per liter of oil.
    """
    try:
        consumption = get_consumption_data()
        production = get_production_data()
        df = pd.merge(consumption, production, on='year', how='inner')
        current_year = dt.date.today().year
        current_month = dt.date.today().month
        #excludes the current year if the month of October has not yet been reached
        if current_month < 10:   
            df = df[df["year"] < current_year]
        df["total_expenses"] = (
            df["irrigation_expenses"] +
            df["fertilizer_costs"] +
            df["pesticide_costs"] +
            df["maintenance_expenses"]
        )
        df["cost_per_liter_oil"] = df["total_expenses"] / df["oil_yield"]
        return df[["year", "cost_per_liter_oil"]]
    except ZeroDivisionError as e:
        print(f"ZeroDivisionError in cost_per_liter_oil(): {e}")
    except Exception as e:
        print(f"Error in cost_per_liter_oil(): {e}")
        
def profit_per_hectare():
    """
    Calculate profit per hectare of surface:
      - Convert surface in m2 to hectares.
      - Profit = Total Oil Revenue - Total Expenses
      - Profit per hectare = Profit / Surface in hectares

    Returns:
        pd.DataFrame: DataFrame with the year and profit per hectare.
    """
    try:
        consumption = get_consumption_data()
        production = get_production_data()
        df = pd.merge(consumption, production, on='year', how='inner')
        current_year = dt.date.today().year
        current_month = dt.date.today().month
        #excludes the current year if the month of October has not yet been reached
        if current_month < 10:
            df = df[df['year'] < current_year]
        df['total_expenses'] = (
            df['irrigation_expenses'] +
            df['fertilizer_costs'] +
            df['pesticide_costs'] +
            df['maintenance_expenses']
        )
        df['revenue'] = df['oil_revenue'] - df['total_expenses']
        df['surface_hectares'] = df['surface_area_in_m2'] / 10000  # Convert m2 to hectares
        df['profit_per_hectare'] = df['revenue'] / df['surface_hectares']
        return df[['year', 'profit_per_hectare']]
    except ZeroDivisionError as e:
        print(f"ZeroDivisionError in profit_per_hectare(): {e}")
    except Exception as e:
        print(f"Error in profit_per_hectare(): {e}")

def annual_precipitation_vs_yield():
    """
    Analyze the correlation between annual_precipitation and gross yield-net yield.
    
    The function calculates the correlation coefficients between precipitation and both net and gross yields
       by using the pandas method corr() which by default calculates the Pearson correlation.
    Pearson correlation measures the **linear relationship** between two variables.
      Values range from -1 (perfect negative correlation) to +1 (perfect positive correlation),
      while 0 indicates no linear correlation.
      
    Returns:
        dict: A dictionary with the correlation coefficients.
    """
    try:
        weather_data = get_weather_data().copy()
        weather_data['date'] = pd.to_datetime(weather_data['date'])
        weather_data['year'] = weather_data['date'].dt.year
        
        production_data = get_production_data().copy()
        
        annual_precipitation = weather_data.groupby('year')['precipitation'].sum().reset_index()
        annual_precipitation = annual_precipitation.rename(columns={'precipitation': 'annual_precipitation'})
        df = pd.merge(production_data, annual_precipitation, on='year', how='left')
        
        net_prec_corr = df['annual_precipitation'].corr(df['net_qty'])
        gross_prec_corr = df['annual_precipitation'].corr(df['gross_qty'])
        return{
            "net yield - annual_precipitation_correlation": round(net_prec_corr,2),
            "gross yield - annual_precipitation_correlation": round(gross_prec_corr,2)
        }
    except Exception as e:
        print(f"Error in precipitation_vs_yield(): {e}")
        return {}
    
def annual_precipitation_vs_revenue():
    """
    Analyze the linear correlation between the two variables annual_precipitation and oil_revenue.
    
    Returns:
        dict: A dictionary with the correlation coefficients.
    """
    try:
        weather_data = get_weather_data().copy()
        weather_data['date'] = pd.to_datetime(weather_data['date'])
        weather_data['year'] = weather_data['date'].dt.year
        
        production_data = get_production_data().copy()
        
        annual_precipitation = weather_data.groupby('year')['precipitation'].sum().reset_index()
        annual_precipitation = annual_precipitation.rename(columns={'precipitation': 'annual_precipitation'})
        df = pd.merge(production_data, annual_precipitation, on='year', how='left')
        
        prec_revenue_corr = df['annual_precipitation'].corr(df['oil_revenue'])
        return {
            "annual_precipitation - oil revenue correlation": round(prec_revenue_corr, 2)
        }
    except Exception as e:
        print(f"Error in precipitation_vs_revenue(): {e}")
        return {}