import os
import pandas as pd
from src.data_acquisition.DBConnection import DBConnection
"""
Setting MySQL connection parameters from environment variables.
This allows for secure storage of sensitive information like database credentials.
Steps to follow:
   
    1. Ensure you have MySQL installed and running by typing `mysql --version` in your terminal.
    2. Navigate in the root project directory and install the required Python packages by running the command:
         pip install -r dependencies.txt
    3. Log in to your MySQL database using a MySQL client and create a database named agri_sud by running the following command:
        CREATE DATABASE agri_sud;
    4. Create a `.env` file in the same directory as this script.
    5. Add the following lines to the `.env` file:
        
        DB_HOST=localhost
        DB_PORT=3306    
        DB_USER=your_username
        DB_PASSWORD=your_password
        DB_NAME=your_database_name
    6. Replace `your_username`, `your_password`, and `your_database_name` with your actual database credentials.
    
    
Note: You don't need to install any dependencies because they are already included in the dependencies.txt file and
      you can install them by running the command
          pip install -r dependencies.txt
"""
def save_df(df, table_name = "weather_forecast_data"):
    db = DBConnection()
    engine = db.get_engine()
    cols = ['date', 'temperature_2m', 'precipitation', 'wind_speed_10m', 'daylight_duration']
    MySQL_df = df[cols]
    MySQL_df.to_sql(table_name, con=engine, if_exists='replace', index=False)
    print(f"Data successfully saved into {table_name} table.")