from src.data_acquisition.DBConnection import DBConnection
from src.Simulator_Engine import ProductionData_Generator as pdg
from src.utils.date_utils import check_for_current_month
import os
import mysql.connector
from mysql.connector import errors as msc_errors
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd


load_dotenv() #Load database login credentials from the .env file

def generate_production_data_table():
    """
    Create and populate the table production_data in MySQL database.
    This function only works if the table does not exists, if the table already exists an exception is thrown,
       if you need to generate new data for the production_table you first have to delete the production_data table from the MySQL database
       and then run the program...
    
    1. Get connection to the MySQL database by using mysql.connector from get_mysql_connection.
    
    2. Create the table production_data if it does not already exist.
    
    3. Generate production data starting from year 2000 to the current year:
        -number of plants (`plants_counter`)
        - harvest days (`harvest_days`)
        - gross and net quantities of olives harvested
        
    4. For each year:
        -if the year < current year: insert data.
        -if the year == current year: check for the current month by using check_for_current_month(the current month must be greater than 9)
            if current month > 9 then insert data
            else insert 0 for the current year.
            
    5. After inserting all data, calls additional functions to generate:
       - oil yield and oil yield percentage (`pdg.generate_oil_yield()`)
       - cultivated surface area (`pdg.generate_surface_in_m2()`)
        
        
    """
    try:
        #get MySQL engine connection
        db = DBConnection()
        conn = db.get_mysql_connection()
        cursor = conn.cursor()
        current_date = datetime.now().year

        #create table
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS production_data (
                    year INT PRIMARY KEY,
                    plants_counter INT NULL,
                    harvest_days INT NULL,
                    gross_qty DECIMAL(10,2) NULL,
                    net_qty DECIMAL(10,2) NULL,
                    oil_yield DECIMAL(10,2) NULL,
                    oil_yield_pct DECIMAL(5,4) NULL,
                    oil_revenue DECIMAL(10,2) NULL,
                    surface_area_in_m2 DECIMAL(10,2) NULL
                )
            """)
        except msc_errors.DatabaseError as e:
            print(f"Error creating production_data table: {e}")
            raise
        try:
            plants_data = pdg.generate_plants_per_year()    #  plants_counter pd.Series
            harvest_data = pdg.generate_harvest_days()      # harvest_days pd.Series
            gross_qty, net_qty = pdg.generate_olive_harvest_qty(plants_data)   # gross_qty and net_qty lists
        except Exception as e:
            print(f"Error while generating random data: {e}")
        
        years = range(2000, 2000 + len(plants_data))

        # Iterate over the years, plants, harvest_days,gross and net
        for year, plants_counter, harvest_days, gross, net in zip(years, plants_data, harvest_data, gross_qty, net_qty):
            try:
                print(year, plants_counter, harvest_days, gross, net)
                if year < current_date:
                    cursor.execute("""
                                INSERT INTO production_data (year, plants_counter, harvest_days, gross_qty, net_qty)
                                VALUES (%s, %s, %s, %s, %s)
                                """, (year, plants_counter, harvest_days, gross, net))
                    
                elif year == current_date:
                    plants_counter = check_for_current_month(plants_counter, year)
                    harvest_days   = check_for_current_month(harvest_days, year)
                    gross          = check_for_current_month(gross, year)
                    net            = check_for_current_month(net, year)
                    
                    cursor.execute("""
                    INSERT INTO production_data (year, plants_counter, harvest_days, gross_qty, net_qty)
                    VALUES (%s, %s, %s, %s, %s)
                    """, (year, plants_counter, harvest_days, gross, net))
            except msc_errors.DatabaseError as e:
                print(f"Error while entering data in the production_data table: {e}")
                continue
            except TypeError as e:
                print(f"Data type does not matches: {e}")
                continue
            except IndexError as e:
                print(f"IndexError during data zipping for year {year}: {e}")
                break
            except Exception as e:
                print(f"Error: {e}")
                continue

        try:
            conn.commit()
            pdg.generate_oil_yield()  #update columns oil yield percentage and oil yield in liters to the table
            pdg.generate_surface_in_m2()  #update surface area in square meters for each year
        except msc_errors.DatabaseError as e:
            print(f"Error while entering data in the production_data table: {e}")
            conn.rollback()
                
        print("Production data table created and populated successfully.")
    except msc_errors.InterfaceError as e:
        print(f"database connection error: {e}")
    except msc_errors.ProgrammingError as e:
        print(f"MySQL Programming Error (e.g., syntax error in query): {e}")
    except AttributeError as e:
        print(f"AttributeError 'conn' or 'cursor' might be None: {e}")
    except FileNotFoundError as e:
        print(f"FileNotFoundError: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # closes resources
        if cursor: 
            cursor.close()
            print("Cursor closed.")
        if conn: 
            conn.close()
            print("Connection closed.")