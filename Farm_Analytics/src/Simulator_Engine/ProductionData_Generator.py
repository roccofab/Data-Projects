from src.eda import eda_metrics
from src.data_acquisition.DBConnection import DBConnection
from src.eda.eda_metrics import find_extreme_weather_years
import random
import datetime as dt
import pandas as pd
import mysql.connector
from mysql.connector import errors as msc_error
def generate_harvest_days():
    """
    Generates a list of harvest days since the year 2000 to the current year.
    The function creates a list of numbers between 7 and 15 for each year, representing the number of harvest days.
    """
    try:
        current_date = dt.date.today()
        harvest_days = []
        for year in range(2000, current_date.year + 1):
            if year >= 2015:  # introduces an increase in harvest days starting from 2015 (15-20 days)
                harvest_days.append(random.randint(15,20))
            else:
                harvest_days.append(random.randint(7,15))  #before 2015 the number of harvest days is between 7-15
        return pd.Series(harvest_days)
    except AttributeError as e:
        print(f"Error in the module datetime: {e}")
        return pd.Series(dtype=int)
    except Exception as e:
        print(f"Error in generate_harvest_days(): {e}")
        return pd.Series(dtype=int)

def generate_lost_plants_per_year():
    """
    This function generate a random number between 100 and 1000 with probability of 30% representing the lost plants for each year.
    The function is designed to introduce a loss factor inside generate_plants_per_year and making data simulation more realistic.
    """
    try:
        if random.random() < 0.3:
            return random.randint(100, 1000)
        return 0
    except Exception as e:
        print(f"Error in  generate_lost_plants_per_year(): {e}")
        return 0

def generate_plants_per_year():
    """
    Generates an incremental random number of plants for each year since 2000 to the current year.
    - The function creates a list of numbers representing the number of plants.
    
    - The function is designed to increment the random number(representing the number of plants) every year:
        it starts with a number between 50000 and 60000 for the year 2000,
        every year the number increases by a random value between 500-1000,
        a loss factor was introduced in the function.
        
    - If the total number of plants reach 100000, the function stop incrementing the number of plants.
    """
    try:
        current_date = dt.date.today()
        plants = []
        count = 0
        for year in range(2000, current_date.year + 1):
            # initialize 
            if year == 2000:
                count = random.randint(50000,60000)
                plants.append(count)
            else:
                # increment
                count += random.randint(500, 1000)
                # introduce lose factor
                lost = generate_lost_plants_per_year()
                count -= lost

            # introduce limits
            if count > 100000:
                count = 100000
            elif count < 0:
                count = 0
            
            plants.append(count)

        return pd.Series(plants)
    except Exception as e:
        print(f"Error in generate_plants_per_year(): {e}")
        return pd.Series(dtype=int)


def get_plants():
    """
    This function retrieves the simulated plant data from MySQL database for each year since 2000.
    
    Returns:
       pd.DataFrame: A DataFrame containing the year and plant_counter columns.
    """
    try:
        db = DBConnection()
        conn = db.get_mysql_connection()
        cursor = conn.cursor()
        query = "SELECT year, plants_counter FROM production_data ORDER BY year ASC"
        cursor.execute(query)
        result = cursor.fetchall()
        df = pd.DataFrame(result, columns = ['year', 'plants_counter'])
        return df
    except msc_error.InterfaceError as e:
        print(f"MySQL database connection error: {e}")
        return pd.DataFrame()
    except msc_error.ProgrammingError as e:
        print(f"MySQL programming error while retrieving data from production_data table: {e}")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error in get_plants(): {e}")
        return pd.DataFrame()
    finally:
        if conn:
            conn.close()


def generate_olive_harvest_qty(plants):
    """
    Calculate gross harvest quantity per year based on plants count and weather impact then from the calculated gross quantity get the net quantity.

    Each year has a specific number of plants and weather conditions that affect the harvest:
        - **Number of Plants**: retrieve plants count from MySQL by using get_plants() method.
        - **Base Yield per Plant**: The basic yield per plant ranges from 15 to 20 kilograms, this range was modeled using the uniform function from random module
                                    to generate continuous values within the specified bounds. 
        
        - **Gross Quantity**:  Computed as `base_yield * number_of_plants`.

        - **Weather Impact**: If the year is into the DataFrame of years with bad weather conditions then the gross quantity is reduced by 30%.
                              Years with extreme weather are determined by `find_extreme_weather_years`

        - **Net Quantity**: Determined as 75-80% of the final gross quantity, representing usable olives after processing losses.
        
    Args:
        num_plants (df): A DataFrame containing the number of plants for each year.
        
    Returns:
        gross_qty (list): A list of float values representing the gross olive harvest quantity for each year.
        net_qty (list): A list of float values representing the net olive harvest quantity for each year.
    """
    try:
        db = DBConnection()
        engine = db.get_engine()

        start_year = 2000
        years = range(start_year, start_year + len(plants))


        # Get the DataFrame of bad weather years
        bad_weather_years = find_extreme_weather_years(engine)
        
        # Initialize lists to hold the gross and net quantities
        gross_qty = []
        net_qty = []

        for year, plants in zip(years, plants):
            # Base yield per plant
            base_yield = random.uniform(15, 20)
            gross = plants * base_yield

            # reduction in case of bad weather
            if year in bad_weather_years:
                gross *= 0.7  # -30%

            gross_qty.append(gross)

            # calculate net quantity as 75-80% of gross quantity
            net_factor = random.uniform(0.75, 0.8)
            net_qty.append(gross * net_factor)

        return gross_qty, net_qty
    except (ValueError, TypeError) as e:
        print(f"Error calculating oil yield(generate_olive_harvest_qty()): {e}")
        return [], []
    except AttributeError as e:
        print(f"AttributeError in generate_olive_harvest_qty(): {e}")
        return [], []
    except Exception as e:
        print(f"Error in generate_olive_harvest_qty(): {e}")
        return [], []

def get_net_qty():
    """
    Retrieve the net olive harvest quantity for each year.
    
    Returns:
       pd.DataFrame: A DataFrame containing the year and net olive harvest quantity.
    """
    try:
        db = DBConnection()
        conn = db.get_mysql_connection()
        cursor = conn.cursor()
        query = "SELECT year, net_qty FROM production_data ORDER BY year ASC"
        cursor.execute(query)
        result = cursor.fetchall()
        return pd.DataFrame(result, columns=['year', 'net_qty'])
    except msc_error.InterfaceError as e:
        print(f"MySQL database connection error: {e}")
        return pd.DataFrame()
    except msc_error.ProgrammingError as e:
        print(f"MySQL programming error while retrieving data from production_data table: {e}")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error in get_net_qty(): {e}")
        return pd.DataFrame()
    finally:
        if conn:
            conn.close()

def generate_oil_yield():
    """
    Generate oil yield data based on net olive harvest quantity.
    
    The oil yield is calculated as a percentage of the net olive harvest quantity, the percentage of oil that can be extracted from the 
       net olive harvest is a random value between 15% and 20%.
    
    The function updates the production_data table in the MySQL database with the calculated oil yield and oil yield percentage for each year.

    Returns:
       None
    """
    try:
        db = DBConnection()
        conn = db.get_mysql_connection()
        cursor = conn.cursor()
        df = get_net_qty()
        # iterate over the DataFrame rows and calculate oil yield
        for year, net in zip(df['year'], df['net_qty']):
            if not net or net == 0:  # if the value is None or 0 set oil yield and oil yield percentage to 0
                oil, pct = 0, 0
            else:
                net = float(net)  #cast net from Decimal to float
                pct = random.uniform(0.15, 0.20)  # random oil yield percentage between 15% and 20%
                oil = net * pct  # calculate oil yield

            cursor.execute(
                """
                UPDATE production_data
                SET oil_yield = %s, oil_yield_pct = %s
                WHERE year = %s
                """,
                (0 if oil is None else round(oil, 2),
                0 if pct is None else round(pct, 4),
                int(year)) 
            )
        conn.commit()
    except (ValueError, TypeError) as e:
        print(f"Error in calculating oil yield(generate_oil_yield()): {e}")
    except Exception as e:
        print(f"Error in generate_oil_yield(): {e}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def generate_oil_revenues():
    """
    Generate oil price dynamically based on production and consumption imbalance:
        -Get production data and consumption data and merge them on the year column.
        
        -Set base Oil Price to 5.0.
        
        -Calculate average net olive harvest for each year and calculate the average total consumption for each year.
        
        -If the year net olive harvest < average olive harvest and year total consumption > average total consumption:
           increase the oil price of a random value between 2 and 3.
        else:
           set oil price to the base oil price(5.0).
           
        - Calculate total revenue = oil price * net_qty
           
    Returns:
        pd.DataFrame: DataFrame containing the year and oil price for each year.

    """
    try:
        production_data = eda_metrics.get_production_data()
        consumption_data = eda_metrics.get_consumption_data()  # funzione da fare se non c’è
        df = pd.merge(production_data, consumption_data, on="year", how="inner")
        
        base_price = 5.0
        
        avg_net_qty = df['net_qty'].mean()
        avg_total_consumption = df[['irrigation_expenses','fertilizer_costs', 'pesticide_costs','maintenance_expenses']].sum(axis = 1).mean()
        df['total_consumption'] = df[['irrigation_expenses','fertilizer_costs', 'pesticide_costs','maintenance_expenses']].sum(axis = 1)
        
        df['oil_price'] = base_price
        condition = (df['net_qty'] < avg_net_qty) & (df['total_consumption'] > avg_total_consumption)
        
        df.loc[condition, 'oil_price'] = [base_price + random.uniform(2,3) for count in range(condition.sum())]

        df['oil_revenue'] = df['oil_price'] * df['oil_yield']

        return df[['year', 'oil_revenue']]
    except (ValueError, TypeError) as e:
        print(f"Error in generating oil revenues(generate_oil_revenues()): {e}")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error in generate_oil_revenues(): {e}")
        return pd.DataFrame()

def update_oil_revenue_in_db():
    """
    Update oil_revenue column in the database.

    Returns:
        None
    """
    try:
        db = DBConnection()
        conn = db.get_mysql_connection()
        cursor = conn.cursor()
        df = generate_oil_revenues()
        for _, row in df.iterrows():
            year = int(row['year'])
            revenue = float(row['oil_revenue']) if pd.notna(row['oil_revenue']) else 0.0
            cursor.execute(
                """
                UPDATE production_data
                SET oil_revenue = %s
                WHERE year = %s
                """,
                (round(revenue, 2), year)
            )
        conn.commit()
    except (ValueError, TypeError) as e:
        print(f"Error updating oil revenue(update_oil_revenue_in_db()): {e}")
    except Exception as e:
        print(f"Error in update_oil_revenue_in_db: {e}")
    finally:
        cursor.close()
        conn.close()
        
def generate_surface_in_m2():
    """
    Update the surface area in square meters for each year in the production_data table.
    The total surface area is calculated by multiplying the number of plants by 18 m^2 that represents the surface area occupied by each plant.
    This function retrieves plant count data from the table and then calculates and updates the corresponding total surface area for each year.

    Returns:
        None
    """
    try:
        db = DBConnection()
        conn = db.get_mysql_connection()
        cursor = conn.cursor()
        query = "SELECT year, plants_counter FROM production_data ORDER BY YEAR ASC"
        cursor.execute(query)
        result = cursor.fetchall()
        
        surface_per_plant = 18
        for year, plants in result:
            if plants is None:
                plants = 0  # handle None values for plants
            total_surface_in_m2 = plants * surface_per_plant
            
            cursor.execute(
                """
                UPDATE production_data
                SET surface_area_in_m2 = %s
                WHERE year = %s
                """,
                (round(total_surface_in_m2, 2), int(year))
            )
        
        conn.commit()
    except (ValueError, TypeError) as e:
        print(f"Error in generate_surface_in_m2(): {e}")
    except Exception as e:
        print(f"Error in generate_surface_in_m2(): {e}")
    finally:
        cursor.close()
        conn.close()


        