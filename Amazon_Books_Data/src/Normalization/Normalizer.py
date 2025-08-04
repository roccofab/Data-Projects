import pandas as pd
import numpy as np
from sklearn.calibration import LabelEncoder
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import json

"""
This module provide functions to normalize numerical columns in the amazon_book_dataset.csv.
A new dataset with normalized columns wille be created in the folder src/Normalization/normalized_data.csv,
   and the original dataset in the folder src/Data_Cleaning will not be changed.
Data normalization allows to compare different numerical columns on the same scale, and it helps to improve the performance of machine learning algorithms.

- Min-Max scaling for price-related columns
- Log transformation followed by Z-score standardization for highly skewed columns (e.g., reviews_count)
- Inverted Min-Max scaling for ranking-related columns (e.g., root_bs_rank)
- Z-score standardization for columns with limited variance (e.g., number_of_sellers)
"""

def normalize_prices(df):
    """
    Normalize the price columns in the DataFrame using Min-Max scaling from sklearn..
    This function scales the 'initial_price' and 'final_price' columns to a range of
       [0, 1] by applying Min-Max normalization.
    That's useful for comparing prices across different books on a common scale.
    """
    df2 = df.copy()
    price_columns = ['initial_price', 'final_price']
    scaler = MinMaxScaler()
    df2[['final_price', 'initial_price']] = scaler.fit_transform(df2[['final_price', 'initial_price']])
    return df2

def normalize_reviews(df):
    """
    Create a new column 'reviews_normalized' by applying a log transformation followed by Z-score standardization.
    The values of the column 'reviews_count' vary from a range of tens up to thousands(skewed distribution),
       log transformation helps to make the values of column 'reviews_count' more normal
       and the Z-score tranformation works better on normalized data.
    """
    df2 = df.copy()
    df2['log_reviews'] = np.log1p(df2['reviews_count'])  
    mean = df2['log_reviews'].mean()
    std = df2['log_reviews'].std()
    df2['reviews_normalized'] = (df2['log_reviews'] - mean) / std
    return df2

def normalize_root_bs_rank(df):
    """
    The column root_bs_rank represent a classification of books(ranking),
      where a lower rank means a better position(for example rank 1 is the best).
    These values range from 1 to hundreds thousands, so we need to invert the values
      to make the best rank equal to 1 and the worst rank equal to 0.
    Then we apply Min-Max scaling to normalize the values between 0 and 1.
    The ranking value is useful for quantitative analysis.
    """
    df['root_bs_rank_inverted'] = -df['root_bs_rank']
    scaler = MinMaxScaler()
    df['root_bs_rank_normalized'] = scaler.fit_transform(df[['root_bs_rank_inverted']])
    return df

def normalize_number_of_sellers(df):
    """
    Number of sellers is a column with limited variance, so we can use Z-score standardization,
       generally the values range from 1 to 20.
    The Z-score standardization transforms the values to have a mean of 0 and a standard deviation of 1. 
    """
    df['number_of_sellers_norm'] = StandardScaler().fit_transform(df[['number_of_sellers']])
    return df

def normalize_best_sellers_rank(df):
    """
    Extract book category and rank from the best_sellers_rank column.
    
    The best_sellers_rank column contains JSON-formatted strings representing lists of dictionaries, each with:
     - category: an Amazon category of the book (with a structure, separated by slashes /)
     - rank: the position of the book within that category
     
    The function extract the category and the rank of the book within that category,
      and save the extracted values in two new columns:
      - 'main_category'
      - 'main_rank'
      
    Then normalize the column 'main_category' using LabelEncoding from sklearn, and normalize
       the column 'main_rank' using Min-Max scaling.
    Label econding is used to convert categorical values into numerical values.
    
    Returns the updated DataFrame with normalized columns.
    """
    def extract_info(x):
        try:
            data = json.loads(x)
            if isinstance(data, list) and len(data) > 0:
                return data[0].get('category'), data[0].get('rank')
        except (json.JSONDecodeError, TypeError, IndexError):
            pass
        return None, None

    df[['main_category', 'main_rank']] = df['best_sellers_rank'].apply(
        lambda x: pd.Series(extract_info(x))
    )

    # Normalize main_category using Label Encoding
    le = LabelEncoder()
    df['main_category'] = le.fit_transform(df['main_category'].astype(str))

    # Normalize main_rank
    df['main_rank'] = pd.to_numeric(df['main_rank'], errors='coerce')
    scaler = MinMaxScaler()
    df['main_rank'] = scaler.fit_transform(df[['main_rank']])

    return df

def normalize_rating(df):
    """
    Convert all values of the column rating into numeric and then create a new column rating_normalized having all values of the rating column
       converted in a scale 0-1, this can be achieved by dividing the rating value by the maximum rating value(5.0).
       This data transformation makes data into a common range, which is essential when using machine learning algorithms and it makes 
       the rating comparable with other normalized features.
    """
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    df['rating_normalized'] = df['rating'] / 5.0
    return df


