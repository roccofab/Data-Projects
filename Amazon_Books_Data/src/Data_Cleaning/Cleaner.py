import ast
import json
from src.Load_Data.Loader import load_dataset
import pandas as pd
import numpy as np
import re
from Normalization import Normalizer

""""
This module provides functions to clean a dataset:

- show_nan: Displays the count of missing values in each column.

"""

def show_nan(df):
    print("\nDataframe with null values:\n")
    return df.isnull().sum().sort_values(ascending=False)

def delete_columns(df):
    """
    delete columns with too many missing values that are not useful for analysis
    # errors='ignore' to avoid KeyError if column doesn't exist
    """
    columns = ['upc','answered_questions','department','delivery','domain','features','product_dimensions','video','colors','image',
               'date_first_available','model_number','description',
               'manufacturer','plus_content','buybox_seller','image_url','url','ISBN10']
    df.drop(columns = columns, inplace = True, errors = 'ignore') 
    
def handle_price(df):
    """
    Handle the columns initial_price,final_price,discount:
    
       First convert columns's values to numeric.
       
       Then find missing values.
       if initial_price is NaN, try to get it by summing final_price + discount,
         if final_price is NaN, try to get it by subtracting initial_price - discount,
         if discount is NaN, try to get it by subtracting initial_price - final_price,
         if one value is not valid(for example negative value, zero value, not a number or discount greater than initial_price),
             then remove the row.
        
        Finally check one more time for NaN values in the columns. 
    """
    
    df['initial_price'] = pd.to_numeric(df['initial_price'], errors = 'coerce') 
    df['final_price'] = pd.to_numeric(df['final_price'], errors = 'coerce')
    df['discount'] = pd.to_numeric(df['discount'], errors = 'coerce')
    
    # replace NaN values in the column initial price with the sum of final_price and discount
    df.loc[df['initial_price'].isna() & df['final_price'].notna() & df['discount'].notna(), 'initial_price'] = df['final_price'] + df['discount']
    # replace NaN values in the column final price with the difference of initial_price and discount
    df.loc[df['final_price'].isna() & df['initial_price'].notna() & df['discount'].notna(), 'final_price'] = df['initial_price'] - df['discount']
    # replace NaN values in the column discount with the difference of initial_price and final_price
    df.loc[df['discount'].isna() & df['initial_price'].notna() & df['final_price'].notna(), 'discount'] = df['initial_price'] - df['final_price']
    #remove rows with not valid values in the columns
    df = df[(df['initial_price'] > 0)
            & (df['final_price'] > 0)
            & (df['discount'] >= 0)
            & (df['final_price'] <= df['initial_price'])]
    
    #remove rows with initial_price,final_price and discount values that are NaN
    df = df[~(df['initial_price'].isna() & df['final_price'].isna() & df['discount'].isna())]
    
    # check one more time for NaN values in the columns
    print("\nRows with NaN values in the columns initial_price, final_price and discount:\n")
    print(df[['initial_price', 'final_price', 'discount']].isna().sum())
    return df

def handle_number_of_sellers(df):
    # Replace the NaN values in the column number_of_sellers with the mode value
    df['number_of_sellers'] = pd.to_numeric(df['number_of_sellers'], errors='coerce')
    mode_value = df['number_of_sellers'].mode().iloc[0]
    df['number_of_sellers'].fillna(mode_value, inplace = True)
    return df

def handle_format(df):
    #replace the NaN values in the column format with 'Other'
    df['format'] = df['format'].fillna('Other')
    return df

def get_book_format(df):
    """
    Extract the book format from the column 'format', save the value in a new column 'book_format' and then delete column 'format'.
    The column 'format' has list of dictionaries as values for example:
          [{"name":"Vinyl Bound","price":"$27.91","url":"/Hobbit-Lord-Rings-Deluxe-Pocket/dp/0544445783"},
           {"name":"Kindle","price":"$29.99","url":"/Chronicles-Narnia-Complete-7-Book-Collection-ebook/dp/B008LUYSAE"},
           {"name":"Hardcover","price":"$38.50","url":"/Diagnostic-Statistical-Manual-Disorders-Separate/dp/B09CPKZ65D"}
           {...}]
    
    The function only extract the first format from the list of dictionaries, price and url are not used.   
    """
    def get_format(value):
        try:
            formats = json.loads(value.replace("'", '"'))
            if isinstance(formats, list) and len(formats) > 0:
                return formats[0].get('name')
        except (json.JSONDecodeError, TypeError):
            pass   #continue if there is an error in parsing the JSON string
    df['book_format'] = df['format'].apply(get_format)
    df.drop(columns = ['format'], inplace = True, errors = 'ignore')  #delete the column 'format'
    return df

def handle_book_fomat(df):
    #replace the NaN values in the column 'book_format' with the mode value
    mode_format = df['book_format'].mode()[0]
    df['book_format'].fillna(mode_format, inplace = True)
    return df
def handle_best_sellers_rank(df):
    """
    Apply the function extract_info from the module Normalizer to the column 'best_sellers_rank'
       to extract the category and the rank of the book within that category.
       
    The best_sellers_rank column contains JSON-formatted strings representing lists of dictionaries, each with:
     - category: an Amazon category of the book (with a structure, separated by slashes /)
     - rank: the position of the book within that category
     
    The function extract the category and the rank of the book within that category,
      and save the extracted values in two new columns:
      - 'main_category'
      - 'main_rank'
    """
    df = Normalizer.normalize_best_sellers_rank(df)
    df.drop(columns=['best_sellers_rank'], inplace=True)
    return df
    

def handle_other_columns(df):
    """
    delete rows with NaN values in the columns:
      'item_weight', 'root_bs_rank', 'brand', best_sellers_rank'
    """
    columns = ['item_weight', 'root_bs_rank', 'brand', 'best_sellers_rank']
    for column in columns:
        df = df[df[column].notna()]
    return df


def parse_item_weight(df):
    """
    Extract numeric values from the 'item_weight' column and cast it from 'pounds|ounces to grams,
      if the value is not a number, it will be set to NaN.
      
    The function uses regex and groups to find the numeric value and the unit of measurement.
    """
    def get_value(value):
        if isinstance(value, str):
            match = re.search(r"([\d.]+)\s*(pounds|ounces)", value.lower())
            if match:
                weight = float(match.group(1))
                unit = match.group(2)
                if unit == "pounds":
                    return weight * 453.92  # Convert pounds to grams
                elif unit == "ounces":
                    return weight * 28.35  # Convert ounces to grams
        return np.nan  # Return None if no match found
    
    df['item_weight'] = df['item_weight'].apply(get_value)
    return df

def add_stock_columns(df):
    """
    Create two columns quantity_in_stock and is_in_stock based on the column availability.
    - If the availability string contains 'Only X left in stock', extract X and set it as quantity_in_stock.
    
    - If the availability string contains 'temporarily out of stock', 'this title will be
        released on', or 'out of stock', set quantity_in_stock to 0 (not available).
        
    - If the availability string contains 'in stock', 'usually ships within 2 to 3 weeks',
        or 'usually ships within 8 days', set quantity_in_stock to NaN (available).

    - If the availability string contains 'in stock', 'usually ships within 2 to 3 weeks',
        or 'usually ships within 8 days', set is_in_stock to 1 (available).
        
    - If the availability string contains 'temporarily out of stock', 'this title will be
        released on', or 'out of stock', set is_in_stock to 0 (not available).
        
    - If the availability string is empty or does not match any of the above conditions,
        set quantity_in_stock to NaN and is_in_stock to 0 (not available).
    """
    def get_quantity(value):
        if isinstance(value,str):
            match = re.search(r'Only (\d+) left in stock', value)
            if match:
                return int(match.group(1))
            if(
                'temporarily out of stock' in value.lower() 
                or 'this title will be released on' in value.lower()
                or 'out of stock' in value.lower()
            ):
                return 0
            
            if(
                'in stock' in value.lower()
                or 'usually ships within 2 to 3 weeks' in value.lower()
                or 'usually ships within 8 days' in value.lower()
                
            ):
                return np.nan
        return np.nan
    
    def get_is_in_stock(value):
        if isinstance(value, str):
          if (
            'temporarily out of stock' in value.lower()
            or 'this title will be released on' in value.lower()
            or 'out of stock' in value.lower()
          ):
            return 0 #not available(0)
          else:
            return 1  #available(1)
        return 0 
    
    df['quantity_in_stock'] = df['availability'].apply(get_quantity)
    df['is_in_stock'] = df['availability'].apply(get_is_in_stock)
    df.drop(columns=['availability'], inplace=True)
    return df

def handle_timestamp(df):
    """
    Convert the 'timestamp' column to datetime format and then to string format 'YYYY-MM-DD'.
    """
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
    return df

def handle_rating(df):
    """
    Convert the 'rating' column to numeric format.
    Values of the column 'rating' are strings in the format X out of stars,
      the function use regex to extract the value of X and cast it to float.
    """
    df['rating'] = df['rating'].astype(str).str.extract(r'(\d+\.\d+)')
    df['rating'] = df['rating'].astype(float)
    return df

def handle_categories(df):
    """
    Get the second and third value of the column 'categories' and it append using a dash(-).
    The column categories has lists of string as values, for example:
       ["Books","Literature & Fiction","Mythology & Folk Tales"]
       ["Books","Children's Books","Literature & Fiction"]
       ...
    """
    def get_category(value):
        try:
            cats = ast.literal_eval(value)
            if len(cats) >= 3:
                return f"{cats[1]} - {cats[2]}"
            elif len(cats) == 2:
                return cats[1]
        except Exception:
            pass
        return "Unknown category"
    df['categories'] = df['categories'].apply(get_category)
    return df

def find_outliers_iqr(df, columns):
    """
    Get outlier values for specific columns using Interquantile Range method.
    The Interquartile Range is a traditional statistical method that find the values to get outlier values of the variable into the entire dataset.

    Args:
        df (pd.DataFrame): Inpt datarame.
        columns (list): list of columns for the search.

    Returns:
        dict: A dictionary where the keys are the column names
              and the values are the DataFrames of the outliers found for that column.
    """
    outliers = {}
    for col in columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

           
            col_outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
            
            
            if not col_outliers.empty:
                outliers[col] = col_outliers[['asin', 'title', col, 'main_category', 'final_price', 'reviews_count']]
            else:
                outliers[col] = pd.DataFrame(columns=['asin', 'title', col, 'main_category', 'final_price', 'reviews_count'])
        else:
            print(f"The column '{col}' is not numerical.")
    return outliers
