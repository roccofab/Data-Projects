import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from src.Simulator_Engine import ProductionData_Generator as pdg
from src.Simulator_Engine import Consumption_Cost_Generator as cg

def test_generate_harvest_days():
    days = pdg.generate_harvest_days()
    current_year = pd.Timestamp.today().year
    #check if the returned value is a pandas Series
    assert isinstance(days, pd.Series), f"Expected pandas Series, got {type(days)}"
    #check if the function generate harvest days for each year from 2000 to current year
    assert len(days) == current_year - 2000 + 1
    #iterate over the generated days and check if they are within the expected range
    for i, val in enumerate(days):
        year = 2000 + i
        if year < 2015:
            assert 7 <= val <= 15
        else:
            assert 15 <= val <= 20
            
def test_generate_lost_plants_per_year():
    plants = pdg.generate_lost_plants_per_year()
    assert plants == 0 or (100 <= plants <= 1000)
    
def test_generate_plants_per_year():
    plants = pdg.generate_plants_per_year()
    # check if the output is a pandas Series
    assert isinstance(plants, pd.Series), f"Expected pandas Series, got {type(plants)}"
    # Check that all values are between 50000 and 100000
    assert plants.between(50000, 100000).all()
    #check if the function generate a maximum of 1000 plants per year
    increments = plants.diff().fillna(0)
    assert (increments <= 1000).all()
    
@patch("src.Simulator_Engine.ProductionData_Generator.DBConnection") # Mock the DBConnection class
def test_get_plants(mock_db):
    #test the get_plants function with a mock database connection
    try:
        mock_conn = MagicMock() # Create a mock connection object
        mock_cursor = MagicMock()  # Create a mock cursor object
        mock_conn.cursor.return_value = mock_cursor  # Mock the cursor method to return the mock cursor
        
        fake_data = [(2000, 55000), (2001, 56000)]  # Fake data to be returned by fetchall
        mock_cursor.fetchall.return_value = fake_data  # Mock fetchall to return fake data
        
        mock_db.return_value.get_mysql_connection.return_value = mock_conn 
        
        plants_df = pdg.get_plants()
        expected_df = pd.DataFrame(fake_data, columns=['year', 'plants_counter'])
        
        # Verify the output DataFrame
        assert isinstance(plants_df, pd.DataFrame), "Output is not a DataFrame"
        assert list(plants_df.columns) == ["year", "plants_counter"], "Incorrect DataFrame columns"
        assert len(plants_df) == 2, "Unexpected number of rows"
        assert plants_df.iloc[0]["year"] == 2000
        assert plants_df.iloc[1]["plants_counter"] == 56000

        # Ensure the SQL query was executed
        mock_cursor.execute.assert_called_once_with("SELECT year, plants_counter FROM production_data ORDER BY year ASC")
        mock_conn.close.assert_called_once()
    except Exception as e:
        pytest.fail(f"get_plants raised an exception: {e}")
        print(f"An error occurred while creating the MySQL connection: {e}")    
def test_generate_olive_harvest():
    plants = [50000,80000,90000]
    harvest_gross,harvest_net = pdg.generate_olive_harvest_qty(plants)
    #check if the output are two lists
    assert isinstance(harvest_gross, list), f"Expected list, got {type(harvest_gross)}"
    assert isinstance(harvest_net, list), f"Expected list, got {type(harvest_net)}"
    #check if the harvest net values are between 75% and 80% of the harvest gross values
    for g, n in zip(harvest_gross, harvest_net):
        assert 0.75 * g <= n <= 0.8 * g
  
@patch("src.Simulator_Engine.ProductionData_Generator.DBConnection") # Mock the DBConnection class        
def test_get_net_qty(mock_db):
    #test the get_net_qty function with a mock database connection
    try:
        mock_conn = MagicMock() # Create a mock connection object
        mock_cursor = MagicMock()  # Create a mock cursor object
        mock_conn.cursor.return_value = mock_cursor  # Mock the cursor method to return the mock cursor
        
        fake_data = [(2000, 30000), (2001, 40000)]  # Fake data to be returned by fetchall
        mock_cursor.fetchall.return_value = fake_data  # Mock fetchall to return fake data
        
        mock_db.return_value.get_mysql_connection.return_value = mock_conn # Mock the MySQL connection
        
        net_qty_df = pdg.get_net_qty()
        expected_df = pd.DataFrame(fake_data, columns=['year', 'net_qty'])
        
        # Verify the output DataFrame
        assert isinstance(net_qty_df, pd.DataFrame), "Output is not a DataFrame"
        assert list(net_qty_df.columns) == ["year", "net_qty"], "Incorrect DataFrame columns"
        assert len(net_qty_df) == 2, "Unexpected number of rows"
        assert net_qty_df.iloc[0]["year"] == 2000
        assert net_qty_df.iloc[1]["net_qty"] == 40000

        # Ensure the SQL query was executed
        mock_cursor.execute.assert_called_once_with("SELECT year, net_qty FROM production_data ORDER BY year ASC")
        mock_conn.close.assert_called_once()
    except Exception as e:
        pytest.fail(f"get_net_qty raised an exception: {e}")
        print(f"An error occurred while creating the MySQL connection: {e}")
    
@patch("src.Simulator_Engine.ProductionData_Generator.DBConnection")
@patch("src.Simulator_Engine.ProductionData_Generator.get_net_qty")    
def test_generate_oil_yield(mock_net_qty, mock_db):
    # Mock the get_net_qty function to return a predefined DataFrame
    fake_data = ({
        'year': [2000, 2001],
        'net_qty': [30000, 40000]
    })
    try:
        mock_net_qty.return_value = pd.DataFrame(fake_data) # Mocked return value

        mock_conn = MagicMock() # Create a mock connection object
        mock_cursor = MagicMock()  # Create a mock cursor object
        mock_conn.cursor.return_value = mock_cursor  # Mock the cursor method to return the mock cursor
        mock_db.return_value.get_mysql_connection.return_value = mock_conn # Mock the MySQL connection
        
        pdg.generate_oil_yield()
        
        # check if execute was called twice (once for each year)
        assert mock_cursor.execute.call_count == 2
        # check if commit was called once
        mock_conn.commit.assert_called_once()
        # check if resources were closed
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()
    except Exception as e:
        pytest.fail(f"generate_oil_yield raised an exception: {e}")
        print(f"An error occurred while generating oil yield: {e}")
        
def test_generate_oil_revenues_no_mock():
    df = pdg.generate_oil_revenues()
    # Check if the result is a DataFrame
    assert isinstance(df, pd.DataFrame)
    # Check if it has the expected columns
    assert list(df.columns) == ['year', 'oil_revenue']
    # Check if it has at least one row 
    assert len(df) > 0
    
@patch("src.Simulator_Engine.ProductionData_Generator.DBConnection")
@patch("src.Simulator_Engine.ProductionData_Generator.generate_oil_revenues")
def test_update_oil_revenue(mock_generate_oil_revenues, mock_db):
    fake_data = pd.DataFrame({
        'year': [2000, 2001],
        'oil_revenue': [600000.0, 750000.0]
    })
    try:
        mock_generate_oil_revenues.return_value = fake_data

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_db.return_value.get_mysql_connection.return_value = mock_conn

        pdg.update_oil_revenue_in_db()

        # check that execute was called for each year
        assert mock_cursor.execute.call_count == 2
        # check that commit was called
        mock_conn.commit.assert_called_once()
        # check that resources were closed
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()  
        
    except Exception as e:
        pytest.fail(f"update_oil_revenue_in_db raised an exception: {e}")
        print(f"An error occurred while updating oil revenue in DB: {e}")
        
@patch("src.Simulator_Engine.ProductionData_Generator.DBConnection")
def test_generate_surface_in_m2(mock_db):
    fake_data = [(2000, 50000), (2001, 60000)]
    try:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = fake_data
        mock_db.return_value.get_mysql_connection.return_value = mock_conn

        pdg.generate_surface_in_m2()

        # check that execute was called for each year 
        assert mock_cursor.execute.call_count == 3
        # check that commit was called
        mock_conn.commit.assert_called_once()
        # check that resources were closed
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()
    except Exception as e:
        pytest.fail(f"generate_surface_in_m2 raised an exception: {e}")
        print(f"An error occurred while generating surface in m2: {e}")
        
def test_generate_water_consumption():
    df = cg.generate_water_consumption()
    #check if the result is a DataFrame
    assert isinstance(df, pd.DataFrame)
    # check for columns
    assert 'irrigation_required_m3' in df.columns
    assert 'irrigation_expenses' in df.columns
    
def test_generate_fertilizer_consumption():
    df = cg.generate_fertilizer_consumption()
    #check if the result is a DataFrame
    assert isinstance(df, pd.DataFrame)
    # check for columns
    assert 'fertilizer_required_kg' in df.columns
    assert 'fertilizer_costs' in df.columns
    
def test_generate_pesticide_consumption():
    df = cg.generate_pesticide_consumption()
    #check if the result is a DataFrame
    assert isinstance(df, pd.DataFrame)
    # check for columns
    assert 'pesticide_required_kg' in df.columns
    assert 'pesticide_costs' in df.columns
    
def test_generate_maintenance_expenses():
    df = cg.generate_maintenance_expenses()
    assert isinstance(df, pd.DataFrame)
    assert 'maintenance_expenses' in df.columns
    
