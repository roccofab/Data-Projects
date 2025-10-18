from src.data_acquisition.DBConnection import DBConnection
from src.Simulator_Engine import Consumption_Cost_Generator as pcg
import os
import mysql.connector
from mysql.connector import errors as msc_errors
from dotenv import load_dotenv
import datetime as dt
import pandas as pd

load_dotenv()

def generate_consumption_table():
    try:
        # get MySQL engine connection
        db = DBConnection()
        conn = db.get_mysql_connection()
        cursor = conn.cursor()
        
        #create table
        try:
            cursor.execute("""
                        CREATE TABLE IF NOT EXISTS consumption_data (
                            year INT PRIMARY KEY,
                            irrigation_required_m3 DECIMAL(10,2) NULL,
                            irrigation_expenses DECIMAL(10,2) NULL,
                            fertilizer_required_kg DECIMAL(12,2) NULL,
                            fertilizer_costs DECIMAL(12,2) NULL,
                            pesticide_required_kg DECIMAL(12,2) NULL,
                            pesticide_costs DECIMAL(12,2) NULL,
                            maintenance_expenses DECIMAL(12,2) NULL
                        )
                        """)
        except msc_errors.DatabaseError as e:
            print(f"Error creating consumption_data table: {e}")
            raise
        
        try:
            irrigation_data = pcg.generate_water_consumption()  # Get irrigation water requirements in cubic meters(pd.DataFrame)
            fertilizer_data = pcg.generate_fertilizer_consumption() # Get fertilizer consumption data(pd.DataFrame)
            pesticide_data = pcg.generate_pesticide_consumption()  # Get pesticide consumption data
            maintenance_data = pcg.generate_maintenance_expenses()  # Get maintenance expenses data
            maintenance_data = maintenance_data[['year', 'maintenance_expenses']]

            #merge data
            merged_data = pd.merge(irrigation_data, fertilizer_data, on="year", how="left")
            merged_data = pd.merge(merged_data, pesticide_data, on="year", how="left")
            merged_data = pd.merge(merged_data, maintenance_data, on="year", how="left")
        except Exception as e:
            print(f"Error while generating random data: {e}")

        for year, row in merged_data.iterrows():
            try:
                year = int(row['year'])
                irrigation_required = float(row['irrigation_required_m3'])
                irrigation_expenses = float(row['irrigation_expenses'])
                fertilizer_required = float(row['fertilizer_required_kg'])
                fertilizer_costs = float(row['fertilizer_costs'])
                pesticide_required = float(row['pesticide_required_kg'])
                pesticide_costs = float(row['pesticide_costs'])
                maintenance_expenses = float(row['maintenance_expenses'])

                cursor.execute("""
                            INSERT INTO consumption_data (year, irrigation_required_m3, irrigation_expenses, fertilizer_required_kg, fertilizer_costs, pesticide_required_kg, pesticide_costs, maintenance_expenses)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                            ON DUPLICATE KEY UPDATE irrigation_required_m3 = VALUES(irrigation_required_m3),
                                                    irrigation_expenses = VALUES(irrigation_expenses),
                                                    fertilizer_required_kg = VALUES(fertilizer_required_kg),
                                                    fertilizer_costs = VALUES(fertilizer_costs),
                                                    pesticide_required_kg = VALUES(pesticide_required_kg),
                                                    pesticide_costs = VALUES(pesticide_costs),
                                                    maintenance_expenses = VALUES(maintenance_expenses)
                            """, (year, irrigation_required, irrigation_expenses, fertilizer_required, fertilizer_costs,
                                    pesticide_required, pesticide_costs, maintenance_expenses))
            except msc_errors.DatabaseError as e:
                print(f"Error while entering data in the consumption_data table: {e}")
                continue
            except (ValueError, KeyError, TypeError) as e:
                print(f"Conversion error or missing data in row {row}: {e}")
                continue
            except IndexError as e:
                print(f"IndexError during data zipping for year {year}: {e}")
                break
            except Exception as e:
                print(f"Error: {e}")
                continue
        try:
            conn.commit()
            print("Consumption data table created and populated successfully.")
        except msc_errors.DatabaseError as e:
            print(f"Error in the final commit: {e}")
            conn.rollback()

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
        # Closes resources
        if cursor: 
            cursor.close()
            print("Cursor closed.")
        if conn: 
            conn.close()
            print("Connection closed.")

   