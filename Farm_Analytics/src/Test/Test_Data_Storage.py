import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from src.data_acquisition.DBConnection import DBConnection
from src.data_acquisition.save_weather_data import save_df
from src.data_acquisition.save_production_data import generate_production_data_table
from src.data_acquisition.save_consumption_cost_data import generate_consumption_table

def test__new__singleton():
    """
    Test the singleton behavior of the DBConnection class.
    Ensures that multiple instances point to the same object.
    """
    try:
        instance1 = DBConnection()
        instance2 = DBConnection()
        assert instance1 is instance2, "DBConnection is not a singleton"
    except Exception as e:
        pytest.fail(f"DBConnection raised an exception: {e}")
        print(f"An error occurred while creating DBConnection instances: {e}")    
@patch("src.data_acquisition.DBConnection.create_engine")  #decorator for the framework unittest.mock to mock the create_engine function
def test_get_engine(mock_create_engine):
    """
    Test the get_engine method of the DBConnection class.
    Ensures that the engine is created only once and subsequent calls return the same engine instance.
    MagicMock is used to mock the create_engine function from SQLAlchemy to avoid actual database connections during testing.
    """
    try:
        db_conn = DBConnection()
        
        with patch('src.data_acquisition.DBConnection.create_engine') as mock_create_engine:
            mock_engine = MagicMock()
            mock_create_engine.return_value = mock_engine  # Mock the engine returned by create_engine
            
            engine1 = db_conn.get_engine()
            engine2 = db_conn.get_engine()
            
            assert engine1 is engine2, "get_engine did not return the same engine instance"
            mock_create_engine.assert_called_once(), "create_engine was called more than once"
            assert engine1 is mock_engine, "The returned engine is not the mocked engine"
    except Exception as e:
        pytest.fail(f"get_engine raised an exception: {e}")
        print(f"An error occurred while creating the engine: {e}")
        
@patch("mysql.connector.connect")  #decorator for the framework unittest.mock to mock the mysql.connector.connect function
def test_get_mysql_connection(mock_connect):
    try:
        db = DBConnection()
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn  # Mock the connection object

        conn = db.get_mysql_connection()
        mock_connect.assert_called_once()  # Ensure connect was called exactly once
        assert conn is mock_conn  # Ensure the returned connection is the mocked connection
    except Exception as e:
        pytest.fail(f"get_mysql_connection raised an exception: {e}")
        print(f"An error occurred while creating the MySQL connection: {e}")
        
@patch("src.data_acquisition.save_weather_data.DBConnection")  #decorator for the framework unittest.mock to mock the save_df function
def test_save_df(mock_db):
    """
    Test the save_df function to ensure it calls the correct methods on the SQLAlchemy engine.
    The database connection and engine are mocked to avoid real database interactions.
    """
    try:
        # Create a fake engine mock
        mock_engine = MagicMock()
        # When DBConnection().get_engine() is called, return the mock engine
        mock_db.return_value.get_engine.return_value = mock_engine

        # Sample DataFrame with required columns
        df = pd.DataFrame({
            'date': ['2025-10-10'],
            'temperature_2m': [20.5],
            'precipitation': [2.0],
            'wind_speed_10m': [5.1],
            'daylight_duration': [36000]
        })

        # Call the function under test
        save_df(df, table_name="test_weather")

        # Assert get_engine was called exactly once
        mock_db.return_value.get_engine.assert_called_once()
        
        # Assert to_sql was called on the mock engine with correct parameters
        mock_engine.execute.assert_not_called()  # Ensure execute is not called directly
    except Exception as e:
        pytest.fail(f"save_df raised an exception: {e}")
        print(f"An error occurred while saving the DataFrame: {e}")
        
@patch("src.data_acquisition.save_production_data.pdg.generate_surface_in_m2") #decorator to mock the generate_surface_in_m2 function
@patch("src.data_acquisition.save_production_data.pdg.generate_oil_yield")  #decorator to mock the generate_oil_yield function
@patch("src.data_acquisition.save_production_data.pdg.generate_olive_harvest_qty", return_value=([100.0], [80.0]))  #decorator to mock the generate_olive_harvest_qty function
@patch("src.data_acquisition.save_production_data.pdg.generate_harvest_days", return_value=[90])  #decorator to mock the generate_harvest_days function
@patch("src.data_acquisition.save_production_data.pdg.generate_plants_per_year", return_value=[100])  #decorator to mock the generate_plants_per_year function
@patch("src.data_acquisition.save_production_data.DBConnection")  #decorator to mock the DBConnection class
def test_generate_production_data_table(mock_db, mock_plants, mock_harvest, mock_olive, mock_oil, mock_surface):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor  # Mock the cursor
    mock_db.return_value.get_mysql_connection.return_value = mock_conn  # Mock the MySQL connection

    generate_production_data_table()

    mock_cursor.execute.assert_called()  # Check if execute was called
    mock_conn.commit.assert_called_once()  # Check if commit was called once
    mock_cursor.close.assert_called_once()  # Check if cursor was closed
    mock_conn.close.assert_called_once()  # Check if connection was closed
    
@patch("src.data_acquisition.save_consumption_cost_data.pcg.generate_water_consumption")  #decorator to mock the generate_water_consumption function
@patch("src.data_acquisition.save_consumption_cost_data.pcg.generate_fertilizer_consumption")  #decorator to mock the generate_fertilizer_consumption function
@patch("src.data_acquisition.save_consumption_cost_data.pcg.generate_pesticide_consumption")  #decorator to mock the generate_pesticide_consumption function
@patch("src.data_acquisition.save_consumption_cost_data.pcg.generate_maintenance_expenses")  #decorator to mock the generate_maintenance_expenses function
@patch("src.data_acquisition.save_consumption_cost_data.DBConnection")  #decorator to mock the DBConnection class
def test_generate_consumption_table(mock_db, mock_water, mock_fertilizer, mock_pesticide, mock_maintenance):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor  # Mock the cursor
    mock_db.return_value.get_mysql_connection.return_value = mock_conn  # Mock the MySQL connection

    # Mock dataframes returned by the data generation functions
    mock_water.return_value = pd.DataFrame({
        'year': [2025],
        'irrigation_required_m3': [500.0],
        'irrigation_expenses': [150.0],
        'maintenance_expenses': [300.0]
    })
    mock_fertilizer.return_value = pd.DataFrame({
        'year': [2025],
        'fertilizer_required_kg': [200.0],
        'fertilizer_costs': [80.0],
        'maintenance_expenses': [300.0]
    })
    mock_pesticide.return_value = pd.DataFrame({
        'year': [2025],
        'pesticide_required_kg': [50.0],
        'pesticide_costs': [40.0],
        'maintenance_expenses': [300.0]
    })
    mock_maintenance.return_value = pd.DataFrame({
        'year': [2025],
        'maintenance_expenses': [300.0]
    })

    generate_consumption_table()

    mock_cursor.execute.assert_called()  # Check if execute was called
    mock_conn.commit.assert_called_once()  # Check if commit was called once
    mock_cursor.close.assert_called_once()  # Check if cursor was closed
    mock_conn.close.assert_called_once()  # Check if connection was closed