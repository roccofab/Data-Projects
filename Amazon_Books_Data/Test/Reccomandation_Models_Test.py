import sys
import os
import pytest
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.Analysis import Reccomandation_Models
from src.Normalization import Normalizer
from src.Load_Data import Loader

path = "src/Data_Cleaning/cleaned_data.csv"

def test_filter_by_category():
    """
    Test the function filter_by_category,the test check 3 different cases:
       - Valid ASIN code: the dataset contains more of 1 book in the same category, 
                          the function should return a dataframe with at most 'num_recs' books of the same category 
                          excluded the book having input ASIN code.
                          
       - Not valid ASIN code: the input ASIN code is not valid and the function should return an empty DataFrame.
       
       - ASIN code with unique category: no other books share the category, the function should return an empty DataFrame.
       
    The function should return a DataFrame with columns 'main_rank'(ascending sort), 'reviews_count'(descending sort), 
       'main_category'(descending sort).
    """
    df = Loader.load_dataset(path)
    
    #Case 1: valid ASIN code and more than one book in the same category
    asin_valid = None
    for asin in df['asin'].unique():
        cat = df[df['asin'] == asin]['main_category'].iloc[0]
        same_cat_books = df[(df['main_category'] == cat) & (df['asin'] != asin)]
        if not same_cat_books.empty:
            asin_valid = asin
            break
        
    assert asin_valid is not None, "Not valid ASIN code"
    result = Reccomandation_Models.filter_by_category(df, asin_valid, num_recs=5)
    assert not result.empty, "Il risultato è vuoto per un ASIN valido"
    assert asin_valid not in result['asin'].values, "L'ASIN dato non dovrebbe essere nei risultati"
    assert all(result['main_category'] == df[df['asin'] == asin_valid]['main_category'].iloc[0])
    assert list(result.columns) == ['asin', 'title', 'rating', 'main_category']
    assert len(result) <= 5
    
    
    # Case 2: ASIN not valid
    result_invalid = Reccomandation_Models.filter_by_category(df, 'FAKE_ASIN_NOT_FOUND', num_recs=5)
    assert result_invalid.empty, "DataFrame is empty"
    assert list(result_invalid.columns) == ['asin', 'title', 'main_category'], \
        "Columns not valid for wrong ASIN code"
        
    # Case 3: ASIN with unique category
    asin_unique = None
    for asin in df['asin'].unique():
        cat = df[df['asin'] == asin]['main_category'].iloc[0]
        if len(df[df['main_category'] == cat]) == 1:
            asin_categoria_unica = asin
            break

    if asin_unique:
        result_unique = Reccomandation_Models.filter_by_category(df, asin_unique, num_recs=5)
        assert result_unique.empty, "DataFrame empty"
        assert list(result_unique.columns) == ['asin', 'title', 'main_category'], \
            "Columns not valid for unique category"
    else:
        print("Not valid ASIN code")    
        
        
def test_knn_category_reccomender():
    """
    To perform this test test I first identyfied a valid asin code in the dataset
      that has neighbors (books with similar final_price value and similar reviews_count value within the same category),
      if the asin code of a book that has no neighbors or an invalid asin code is taken as input, the function returns an empty dataframe and the test fails.
    """
    df = Loader.load_dataset(path)
    
    df = Reccomandation_Models.data_preprocessing(df)
    asin = "0060244887"
    result = Reccomandation_Models.knn_category_recommender(df, inp_asin=asin, num_recs=3)
    
    assert not result.empty
    assert 'asin' in result.columns


def test_kmeans_reccomender():
    """
    This test as the test_knn_category_reccomender only test the valid case(book with a valid asin code and neighbors within the same category).
    If the asin code is not valid or if the book has no neighbors within the same category the test fails.
    """
    df = Loader.load_dataset(path)
    df = Reccomandation_Models.data_preprocessing(df)

    asin = "0060244887"

    result = Reccomandation_Models.kmeans_reccomender(df, inp_asin=asin, num_recs=3)

    assert not result.empty
    assert 'asin' in result.columns
    