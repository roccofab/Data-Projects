import sys
import os
import pytest
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.Analysis import BookDataAnalysis
from src.Load_Data import Loader

path = "src/Data_Cleaning/cleaned_data.csv"

@pytest.fixture(scope="module")
def load_df():  
    return Loader.load_dataset(path)

def test_top10_most_popular(load_df):
#verify if the function filter the top10 most popular book by main_rank,reviews_count, rating and returns 10 books and the expected columns
   result = BookDataAnalysis.top10_most_popular(load_df)
   lines = result.strip().split('\n')
   assert len(lines) - 1 == 10, f"Rows: {len(lines)}"  #exclude the header
   header = lines[0].lower()
   expected_cols = ['asin', 'title', 'rating']
   missing = [col for col in expected_cols if col not in header]
   assert not missing, f"Missing columns: {missing}"
   
def test_top10_discounted_products(load_df):
#verify if the function filter the top10 most discounted books by discount_pct and returns 10 books and the expected columns
   result = BookDataAnalysis.top10_discounted_products(load_df)
   assert len(result)  == 10, f"Rows: {len(result)}"
   expected_cols = ['brand','title','discount_pct']
   missing = [col for col in expected_cols if col not in result.columns]
   assert not missing, f"Missing columns: {missing}"

def test_top10_cheapest_per_category(load_df):
    result = BookDataAnalysis.top10_cheapest_per_category(load_df)
    assert len(result) == 10, f"Rows: {len(result)}"
    
    expected_cols = ['categories', 'avg_final_price', 'count']
    missing = [col for col in expected_cols if col not in result.columns]
    assert not missing, f"Missing columns: {missing}"
    
    #check if the result is sorted in ascending order by avg_final_price
    prices = result['avg_final_price'].tolist()
    assert prices == sorted(prices), f"Prices not sorted in ascending order: {prices}"
    
def test_top10_most_expensive_category(load_df):
    result = BookDataAnalysis.top10_most_expensive_category(load_df)
    assert len(result) == 10, f"Rows: {len(result)}"
    
    expected_cols = ['categories', 'avg_final_price', 'count']
    missing = [col for col in expected_cols if col not in result.columns]
    assert not missing, f"Missing columns: {missing}"
   
    #check if the result is sorted in ascending order by avg_final_price
    prices = result['avg_final_price'].tolist()
    assert prices == sorted(prices, reverse=True), f"Prices not sorted in descending order: {prices}"
    
def test_num_books_per_seller(load_df):
    result = BookDataAnalysis.num_books_per_seller(load_df)
    assert len(result) == 10, f"Rows: {len(result)}"
    
    expected_cols = ['seller_name', 'quantity_in_stock']
    missing = [col for col in expected_cols if col not in result.columns]
    assert not missing, f"Missing columns: {missing}"
    
def test_avg_discount_per_category(load_df):
    #check if the resulting dataframe has the expected columns and it is not empty then Check the correct descending sorting of the discount_pct column
    result = BookDataAnalysis.avg_discount_per_category(load_df)
    assert list(result.columns) == ['categories', 'avg_discount_pct'], \
        f"Columns: {result.columns}"
        
    assert not result.empty, "DataFrame is empty."

    # Verifica che la colonna sia ordinata in ordine decrescente
    discounts = result['avg_discount_pct'].tolist()
    assert discounts == sorted(discounts, reverse=True), "Values are not sorted in descending order"
    
def test_avg_discount_per_format(load_df):
    result = BookDataAnalysis.avg_discount_per_format(load_df)
    assert list(result.columns) == ['book_format', 'avg_discount_pct'], \
        f"Columns: {result.columns}"
        
    assert not result.empty, "DataFrame is empty"
    
    assert result['avg_discount_pct'].is_monotonic_decreasing, "Values are not sorted in descending order"
    
def test_avg_discount_per_rating(load_df):
    result = BookDataAnalysis.avg_discount_per_rating(load_df)
    assert list(result.columns) == ['rating', 'avg_discount_pct'], \
        f"Columns: {result.columns}"
        
    assert not result.empty, "DataFrame is empty"
    
    """
    Alternative to the function monotic_decreasing/monotic_increasing:
    
        assert (result['avg_discount_pct'].diff().dropna() >= 0).all(), *\*
           "avg_discount_pct is not in ascending order"

    """
    assert result['avg_discount_pct'].is_monotonic_decreasing, "Values are not sorted in descending order"
    
def test_avg_discount_per_rating_count(load_df):
    result = BookDataAnalysis.avg_discount_per_rating_count(load_df)
    assert list(result.columns) == ['reviews_count', 'avg_discount_pct'], \
        f"Columns: {result.columns}"
        
    assert not result.empty, "Dataframe is empty"
    
    assert result['avg_discount_pct'].is_monotonic_increasing, "Values are not sorted in ascending order"
    
def test_discount_vs_availability(load_df):
    df = BookDataAnalysis.discount_vs_availability(load_df)
    
    # Check type and columns
    assert isinstance(df, pd.DataFrame), "Return DataFrame"
    expected_cols = ['discount_range', 'percentage_not_available_in_stock', 'percentage_available_in_stock']
    assert list(df.columns) == expected_cols, f"Columns mismatch: {df.columns}"
    
    # Check percent ranges
    for col in expected_cols[1:]:
        assert df[col].between(0, 100).all(), f"{col} has values out of [0,100] range"
    
    # Check sums approx 100%
    sums = df['percentage_not_available_in_stock'] + df['percentage_available_in_stock']
    assert all(abs(s - 100) < 1e-5 for s in sums), "Percentages do not sum up to 100"

def test_availability_vs_price(load_df):
    df = BookDataAnalysis.availability_vs_price(load_df)
    
    
    assert isinstance(df, pd.DataFrame), "Return  DataFrame"
    expected_cols = ['price_range', 'percentage_not_available_in_stock', 'percentage_available_in_stock']
    assert list(df.columns) == expected_cols, f"Columns mismatch: {df.columns}"
    
   
    for col in expected_cols[1:]:
        assert df[col].between(0, 100).all(), f"{col} has values out of [0,100] range"
    
    
    sums = df['percentage_not_available_in_stock'] + df['percentage_available_in_stock']
    assert all(abs(s - 100) < 1e-5 for s in sums), "Percentages do not sum up to 100"
