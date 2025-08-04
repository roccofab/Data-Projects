import pandas as pd
import numpy as np
from scipy import stats



"""
The file includes:
  - Basic statistical analysis for numerical variables.
  
  - Frequency distributions for categorical variables.
  
  - Price and discount analysis.
  
  - Books Availability Analysis.
  
  - Correlation Analysis.
  
  - Cluster Analysis.
"""

def price_stats(df):
    #basic statistics analysis for column 'initial_price' and 'final_price'
    
    stats = {
        "Avg. Initial Price" : df['initial_price'].mean(),
        "Avg. Price" : df['final_price'].mean(),
        "Max Price" : df['final_price'].max(),
        "Min Price" : df['final_price'].min(), 
        "Price Range": df['final_price'].max() - df['final_price'].min(),
    }
    return stats

def discount_stats(df):
    #basic statistical analysis for column 'discount'
    
    discount_pct = (df['discount'] / df['initial_price']) * 100
    stats = {
        "Avg. Discount Amount": df['discount'].mean(),
        "Median Discount Amount": df['discount'].median(),
        "Max Discount Amount": df['discount'].max(),
        "Min Discount Amount": df['discount'].min(),
        "Avg. Discount %": discount_pct.mean(),
        "Median Discount %": discount_pct.median(),
        "Max Discount %": discount_pct.max(),
        "Min Discount %": discount_pct.min()
    }
    return stats

def availability_stats(df):
    #basic statistical analysis for column 'quantity_in_stock'
    stats = {
        "Total Available": df['quantity_in_stock'].sum(),
        "Total Not Available": df['quantity_in_stock'].count() - df['quantity_in_stock'].sum(),
        "Percentage Available": df['quantity_in_stock'].mean() * 100
    }
    return stats

def rating_stats(df):
    #basic statistical analysis for column 'rating'
    stats = {
        "Avg. Rating" : df['rating'].mean(),
        "Min Rating" : df['rating'].min(),
        "Max Rating" : df['rating'].max(),
        "Median Rating" : df['rating'].median(),
        "Rating Std. Dev." : df['rating'].std(),
        "Rating Variance" : df['rating'].var()
    }
    return stats
    
def reviews_count_stats(df):
    #basic statistical analysis for column 'reviews_count'
    stats = {
        "Avg. Reviews Count" : df['reviews_count'].mean(),
        "Min Reviews Count" : df['reviews_count'].min(),
        "Max Reviews Count" : df['reviews_count'].max(),
        "Median Reviews Count" : df['reviews_count'].median(),
        "Reviews Count Std. Dev." : df['reviews_count'].std(),
        "Reviews Count Variance" : df['reviews_count'].var()
    }
    return stats

def books_per_category(df):
    #count the number of books in each category:
    num_books = df.groupby('categories').size().reset_index(name = 'count')
    return num_books

def top10_most_popular(df):
    """
    Popularity based filter that select the 10 most popular titles based on the columns:
       - main_rank: main metric for the popularity of a book, lower main rank values mean higher book popularity.
       - reviews_count: a larger number of reviews means that the book is more popular than books with lower number of reviews.
       - rating
    The function uses a dataframe 'popular_books' where the rows are sorted in the following way:
       the column 'main_rank' is sorted in descending order because lower main rank values mean higher book popularity,
       the columns 'reviews_count' and 'rating' are sorted in ascending order,
       the function then drop duplicates from the 'isbn' column to get unique books and select the first 10 rows from the dataframe.
         
    """
    popular_books = df.sort_values(
        by=['main_rank', 'reviews_count', 'rating'],
        ascending=[True, False, False]
    )
    #drop duplicates from 'isbn' column 
    popular_books = popular_books.drop_duplicates(subset=['asin'])
    #select the 10 most popular books
    top10 = popular_books.head(10)
    #select the columns 'isbn', 'title' and 'rating' from the dataframe
    result = top10[['asin', 'title', 'rating']]
    
    return result.to_string(index = False)

def top10_discounted_products(df):
    """
    Returns the top 10 most discounted products.
    
    Args:
        df (pd.DataFrame): Input dataframe containing product data
        
    Returns:
        pd.DataFrame: DataFrame with top 10 discounted products containing:
            - brand
            - title
            - book_format
            - quantity_in_stock
            - discount_percentage
    """
    
    df['discount_pct'] = (df['discount'] / df['initial_price']) * 100
    top10 = df.sort_values('discount_pct', ascending = False).head(10).round(2)

    result = top10[['brand','title','discount_pct']].reset_index(drop = True)

    return result

def avg_discount_per_category(df):
    # calculate the average discount percentage per category
    df['discount_pct'] = (df['discount'] / df['initial_price']) * 100
    avg_discount = df.groupby('categories').agg(
        avg_discount_pct=('discount_pct', 'mean')
    ).reset_index()
    return avg_discount.round(2).sort_values('avg_discount_pct', ascending=False).reset_index(drop=True)

def avg_discount_per_format(df):
    # calculate the average discount percentage per book format
    df['discount_pct'] = (df['discount'] / df['initial_price']) * 100
    avg_discount = df.groupby('book_format').agg(
        avg_discount_pct=('discount_pct', 'mean')
    ).reset_index()
    return avg_discount.round(2).sort_values('avg_discount_pct', ascending=False).reset_index(drop=True)

def avg_discount_per_rating(df):
    # calculate the average discount percentage per rating
    df['discount_pct'] = (df['discount'] / df['initial_price']) * 100
    avg_discount = df.groupby('rating').agg(
        avg_discount_pct=('discount_pct', 'mean')
    ).reset_index()
    return avg_discount.round(2).sort_values('avg_discount_pct', ascending=False).reset_index(drop=True)

def avg_discount_per_rating_count(df):
    # calculate the average discount percentage per reviews count
    df['discount_pct'] = (df['discount'] / df['initial_price']) * 100
    avg_discount = df.groupby('reviews_count').agg(
        avg_discount_pct=('discount_pct', 'mean')
    ).reset_index()
    return avg_discount.round(2).sort_values('avg_discount_pct', ascending=True).reset_index(drop=True).head(10)


def discount_vs_availability(df):
    """
    Analyze the relationship between discount and availability:
       - Percentage of books with discount under 10% available.
       - Percentage of books with discount between 10% and 20% available.
       - Percentage of books with discount between 20% and 30% available.
       - Percentage of books with discount over 30% available.
    Returns a DataFrame with the results.
    """
    bins = [0, 10, 20, 30, float('inf')]
    labels = ['< 10%', '10%-20%', '20%-30%', '30%+']
    # Create a new column 'discount_range' based on the 'discount_pct'
    df['discount_range'] = pd.cut((df['discount'] / df['initial_price']) * 100, bins=bins, labels=labels, right=False)
    # count the number of books in each discount range and availability status
    availability_counts = df.groupby(['discount_range', 'is_in_stock']).size().unstack(fill_value=0)
    #calculate the percentage of availability
    availability_percentage = (availability_counts.div(availability_counts.sum(axis=1), axis=0) 
                               * 100).reset_index().round(2)
    availability_percentage.columns.name = None  # Remove the name of the index
    # Rename the columns
    availability_percentage.columns = [
        'discount_range', 
        'percentage_not_available_in_stock', 
        'percentage_available_in_stock'
    ]
    return availability_percentage.round(2).reset_index(drop=True)

def top10_cheapest_per_category(df, n = 10):
    #get the top 10 least expensive average price per 'categories' and the number of books in each category
    avg_price = df.groupby('categories').agg(
        avg_final_price=('final_price', 'mean'),  #average final price for the category
        count=('final_price', 'count')  #number of books in the category
    ).reset_index()
    avg_price['avg_final_price'] = avg_price['avg_final_price'].round(2)
    top_n = avg_price.nsmallest(n, 'avg_final_price').sort_values(['avg_final_price', 'categories'])
    return top_n[['categories', 'avg_final_price', 'count']].reset_index(drop = True)

def top10_most_expensive_category(df, n = 10):
    #get the top 10 most expensive average price per 'categories' and the number of books in each category
    avg_price = df.groupby('categories').agg(
        avg_final_price=('final_price', 'mean'),
        count=('final_price', 'count')
    ).reset_index()
    avg_price['avg_final_price'] = avg_price['avg_final_price'].round(2)
    top_n = avg_price.nlargest(n, 'avg_final_price').sort_values(['avg_final_price', 'categories'], ascending=[False, True])
    return top_n[['categories', 'avg_final_price', 'count']].reset_index(drop = True)

def top10_most_rated(df, n = 10):
    # get the top 10 most rated books based on 'reviews_count'
    return df.sort_values('reviews_count', ascending=False).head(n)[['title', 'reviews_count']]

def top10_bestsellers(df):
    # Get the top 10 best-seller books based on 'main_rank'
    return df.sort_values('main_rank').head(10)[['seller_name']]


def availability_vs_price(df):
    """
    Analyze the relationship between availability('is_in_stock') and price('final_price):
       - Percentage of books under 10$ available.
       - Percentage of books between 10$ and 20$ available.
       - Percentage of books between 20$ and 30$ available.
       - Percentage of books over 30$ available.
    Returns a DataFrame with the results.
    """
    bins = [0, 10, 20, 30, float('inf')]
    labels = ['< $10', '$10-$20', '$20-$30', '$30+']
    # Create a new column 'price_range' based on the 'final_price'
    df['price_range'] = pd.cut(df['final_price'], bins=bins, labels=labels, right=False)
    # count the number of books in each price range and availability status
    availability_counts = df.groupby(['price_range', 'is_in_stock']).size().unstack(fill_value=0)
    #calculate the percentage of availability
    availability_percentage = (availability_counts.div(availability_counts.sum(axis=1), axis=0) 
                               * 100).reset_index().round(2)
    availability_percentage.columns.name = None  # Remove the name of the index
    # Rename the columns
    availability_percentage.columns = [
        'price_range', 
        'percentage_not_available_in_stock', 
        'percentage_available_in_stock'
    ]
    return availability_percentage

def reviews_count_vs_price(df):
    """
    Analyze the average price of books grouped by the number of reviews ranges:
      - 0-1000 reviews
      - 1000-5000 reviews
      - 10000-50000 reviews
    """
    bins = [0,10000,20000,30000,40000,50000, float('inf')]
    labels = ['0-10000',  '10000-20000','20000-30000','30000-40000','40000-50000', '50000+']
    df['num_reviews_range'] = pd.cut(df['reviews_count'], bins=bins, labels=labels, right=False)
    avg_price = df.groupby('num_reviews_range')['final_price'].mean().reset_index()
    return avg_price.sort_values('final_price', ascending=False).reset_index(drop=True).round(2)

def avg_price_per_seller(df):
    #calculate the average price of the books per seller
    avg_price = df.groupby('seller_name')['final_price'].mean().reset_index()
    return avg_price.sort_values('final_price', ascending=False).reset_index(drop=True).round(2)

def num_books_per_seller(df):
    #calculate the top 10 sellers with the most books in stock
    num_books = df.groupby('seller_name')['quantity_in_stock'].sum().reset_index()
    return num_books.sort_values('quantity_in_stock', ascending=False).reset_index(drop=True).head(10)

def numerical_variables_correlation(df):
    """
    Calculate the linear correlation between the numerical variables:
      - 'initial_price'
        - 'final_price'
        - 'discount'
        - discount_pct
        - rating
        - reviews_count
    """
    cols = ['initial_price', 'final_price', 'discount', 'discount_pct', 'rating',
            'reviews_count',  'item_weight', 'quantity_in_stock']
    return df[cols].corr(method='pearson').round(2)





  

