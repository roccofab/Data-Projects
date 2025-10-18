import random
from src.data_acquisition.DBConnection import DBConnection
import pandas as pd
import mysql.connector
from mysql.connector import errors as msc_error
def get_weather_data():
    # Fetch weather data from the database
    conn = None
    try:
        db = DBConnection()
        conn = db.get_mysql_connection()
        query = "SELECT * FROM weather_data"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
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
        if conn:
            conn.close()


def get_production_data():
    # Fetch production data from the database
    conn = None
    try:
        db = DBConnection()
        conn = db.get_mysql_connection()
        query = "SELECT * FROM production_data"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
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
        if conn:
            conn.close()

    
def generate_water_consumption():
    """
   Calculate annual irrigation water requirements and irrigation expenses for olive production.
    
   The function uses weather data (daily precipitation) and production data 
    (cultivated surface area in m^2) to estimate yearly irrigation needs and irrigation expenses.
    The annual water requirement is set to 800 mm per hectare, and the water price is set to 0.3 € per cubic meter.
    Args:
       None
       
    Returns:
       pd.DataFrame: A DataFrame containing the irrigation water requirements in cubic meters for each year.
    """
    try:
        weather_data = get_weather_data()  # Fetch weather data
        production_data = get_production_data()  # Fetch production data
        ANNUAL_WATER_REQUIREMENT = 800  # in cubic meters per hectare
        WATER_PRICE_PER_M3 = 0.3  # default price in € per cubic meter
        mm_water_required = []  # list to store water requirements in mm for each year
        water_expenses = []

        # aggregate weather data by year
        weather_data['year'] =  pd.to_datetime(weather_data["date"]).dt.year
        # sum of daily precipitation for each year
        annual_precipitation = (weather_data.groupby('year')['precipitation']
                                .sum()
                                .reset_index()
                                .rename(columns={'precipitation': 'annual_precipitation_mm'})
        )

        # filter columns year and surface_area_in_m2 from production_data
        production_data = production_data[['year', 'surface_area_in_m2']]

        # Merge production and weather data
        merged_data = pd.merge(production_data, annual_precipitation, on='year', how='left')
        
        #calculate annual water requirement in mm
        for i in range(len(merged_data)):
            # Get annual precipitation and surface area for the current year
            annual_precipitation_mm = merged_data.loc[i, 'annual_precipitation_mm']
            surface_area = merged_data.loc[i, 'surface_area_in_m2']

            # Calculate water required for the current year by subtracting annual precipitation from the required amount
            water_required = max(ANNUAL_WATER_REQUIREMENT - annual_precipitation_mm, 0)
            
            #convert water required in millimetres to cubic meters
            water_required_m3 = water_required * surface_area / 1000
            mm_water_required.append(water_required_m3)
            
            # Calculate the cost of water for each year
            cost = water_required_m3 * WATER_PRICE_PER_M3
            water_expenses.append(cost)

        merged_data['irrigation_required_m3'] = mm_water_required
        merged_data['irrigation_expenses'] = water_expenses
        return merged_data
    except ValueError as e:
        print(f"data conversion error in generate_water_consumption(): {e}")
        return pd.DataFrame()
    except AttributeError as e:
        print(f"AttributeError 'conn' or 'cursor' might be None while generate_water_consumption() was trying to fetch weather data: {e}")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error in generate_water_consumption(): {e}")
        return pd.DataFrame()
    
def generate_fertilizer_consumption():
    """
    Generate fertilizer consumption data.
    
    I've simply calculated the fertilizer required in kg by multiplying the dosage of fertilizer per m2(0.03) with the surface area in m2.
    The fertilizer costs are then derived from the required amount and the cost per ton.

    Returns:
        pd.DataFrame: DataFrame containing all production_data and the additional columns fertilizer_required_kg and fertilizer_costs.
    """
    try:
        production_data = get_production_data()  # Fetch production data
        cost_per_ton = 600
        dosage_per_m2 = 0.03
        
        #get columns year and surface_area_in_m2 from production_data
        production_data = production_data[['year', 'surface_area_in_m2']]
        #calculate the dosage required for the total surface area
        production_data['fertilizer_required_kg'] = production_data['surface_area_in_m2'] * dosage_per_m2

        #calculate the total cost by multiplying the fertilizer costs per hectare
        production_data['fertilizer_costs'] = (production_data['fertilizer_required_kg'] / 1000) * cost_per_ton
        production_data['fertilizer_costs'] = production_data['fertilizer_costs'].round(2) 
        
        return production_data
    except ValueError as e:
        print(f"data conversion error in generate_fertilizer_consumption(): {e}")
        return pd.DataFrame()
    except AttributeError as e:
        print(f"AttributeError 'conn' or 'cursor' might be None while generate_fertilizer_consumption() was trying to fetch production data: {e}")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error in generate_fertilizer_consumption(): {e}")
        return pd.DataFrame()
def generate_pesticide_consumption():
    """
    Generate pesticide consumption data.
    
    I've simply calculated the pesticide required and its costs based on the surface area:
      - The pesticide required is calculated using a dosage of 0.01 kg/m2.
      - The costs are then derived from the required amount and the cost per ton.

    Returns:
        pd.DataFrame: DataFrame containing all production_data and the additional columns pesticide_required_kg and pesticide_costs.
    """
    try:
        production_data = get_production_data()  # Fetch production data
        cost_per_ton = 1000
        dosage_per_m2 = 0.01
        
        #get columns year and surface_area_in_m2 from production_data
        production_data = production_data[['year', 'surface_area_in_m2']]
        #calculate the dosage required for the total surface area
        production_data['pesticide_required_kg'] = production_data['surface_area_in_m2'] * dosage_per_m2

        #calculate the total cost by multiplying the pesticide costs per hectare
        production_data['pesticide_costs'] = (production_data['pesticide_required_kg'] / 1000) * cost_per_ton
        production_data['pesticide_costs'] = production_data['pesticide_costs'].round(2) 
        
        return production_data
    except ValueError as e:
        print(f"data conversion error in generate_pesticide_consumption(): {e}")
        return pd.DataFrame()
    except AttributeError as e:
        print(f"AttributeError 'conn' or 'cursor' might be None while generate_pesticide_consumption() was trying to fetch production data: {e}")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error in generate_pesticide_consumption(): {e}")
        return pd.DataFrame()
def generate_maintenance_expenses():
    """
    Generate maintenance expenses data.
    - Set base expenses to 3000.
    
    - Calculate surface maintenance expenses by multiplying the surface area in m2 with a random number between 0.02 and 0.025(maintenance coefficient surface),
         I've chosen this range based on typical maintenance costs in agriculture, if I chose a higher range, the prices would grow exponentially,
         this range allows me to keep the surface maintenance prices in a range of around 20,000 and 30,000.

    - Calculate plant maintenance expenses by multiplying the number of plants with a random number between 0.25 and 0.30(maintenance coefficient plants),
         this range allows me to keep the plant maintenance prices in a range of around 15000 and 20000.
         
    - Sum all expenses to get the total maintenance expenses.
    
    Returns:
        pd.DataFrame: DataFrame containing all production_data and the additional column maintenance_expenses.
    """
    try:
        production_data = get_production_data()
        base_expense = 3000  # Base maintenance expense in €(machinery manutention, plants and surface maintenance)

        # Calculate surface maintenance expenses based on surface area and a maintenance coefficient between 0.02-0.025
        maintenance_coeff_surface = random.uniform(0.02, 0.025)
        surface_exp = production_data['surface_area_in_m2'] * maintenance_coeff_surface

        # Calculate plant maintenance expenses based on the number of plants and a maintenance coefficient between 0.25-0.30
        maintenance_coeff_plants = random.uniform(0.25, 0.3)
        plants_exp = production_data['plants_counter'] * maintenance_coeff_plants

        production_data['maintenance_expenses'] = base_expense + surface_exp + plants_exp

        return production_data
    except ValueError as e:
        print(f"data conversion error in generate_maintenance_expenses(): {e}")
        return pd.DataFrame()
    except AttributeError as e:
        print(f"AttributeError 'conn' or 'cursor' might be None while generate_maintenance_expenses() was trying to fetch production data: {e}")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error in generate_maintenance_expenses(): {e}")
        return pd.DataFrame()