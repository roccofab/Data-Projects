#import hdbscan
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors
import umap
from src.Normalization import Normalizer

"""
The file contains 3 book recommendation models based only on numerical and categorical features of the books in the dataset(content-based)
because the dataset does not contain user-book interaction data.

* 'filter_by_category': This basic filtering model suggest popular books (10 by default) in the same category as a book searched for by its asin code.
                        The model find book's category and then filtering,sorting by popularity(main_rank, reviews_count,rating) and returns the most relevant
                        books in that category.
                        Book is popular if it has a lower main_rank value, it has many reviews and it has high average rating.
                        

* 'knn_category_recommender': This content-based filtering model suggests books similar to a given one (identified by asin code) using the Nearest Neighbors
                               algorithm within the same category.
                              Filtering is done by calculating the Euclidean distance between books based on their normalized prices and
                                the number of normalized reviews,
                                returning the closest and therefore most similar books in terms of price and number of reviews.
                                
* 'kmeans-reccomender':     This content-based model suggests books similar to a given one (identified by its ASIN), based on final price and reviews count,
                              by using the K-Means clustering algorithm within the same category combined with dimensionality reduction via UMAP.
                            The k-means algorithm divides a dataset into k clusters by minimizing the intra-cluster distance.
                            This model first applies UMAP to reduce the dimensional data (price, reviews, category) to 2D and then K-Means
                               to group them into clusters, then it searches for books in the same cluster and category as the input, excluding the given book.
                            Finally, it returns the closest ones to the input in the new UMAP space as recommendations.
                           
                                
* 'notes': I'm not gonna delete outlier values for the columns that i've used in the models because statistically these values are outlier but can be interpreted
           as regualar values, for example the columns 'reviews_count' and 'reviews_normalized' has some outlier values
           that i got by applying the interquartile range, however  books with exceptionally high review counts often represent bestsellers
           or highly influential works, which are legitimate and crucial data points for content-based recommendations, not data errors.
           Their removal would skew the representation of book popularity and potentially diminish the quality of recommendations for popular titles.
           Same thing for the column 'final_price': in this case the outlier values represent books with a little bit higher final price than the average,
           but there are no books with a negative final price, a final price of $0 or books with an incredibly high price (e.g. $1000)
           that would represent true outlier values in that case.
"""
def filter_by_category(df, inp_asin, num_recs = 5):
    """
    Suggests the most popular books in the same category as a book the user searched for by ASIN code.
    The asin(Amazon Standard Identification Number) is a unique alphanumeric code that identifies each product on Amazon.
    The function doesn't work on the original dataframe but it works on a copy of it,
      extract the column's value 'main_category' of the row that matches to the asin code,
      filter books in the same category (excluding the book the user searched for),
      sort books by main_rank(ascending),reviews_count(descending) and rating(descending),
      then returns the dataframe with the results or an empty dataframe if the asin code is not correct or the category of the book is unique.
      

    Args:
        df (pd.Dataframe): dataframe that contains the cleaned data.
        inp_asin (str): input asin code.
        num_recs (int, optional): number of reccomended books to return.
        
    Returns:
        pd.DataFrame: A DataFrame containing the asin, title, rating, and category of recommended books.
    """
    df2 = df.copy()
    
    book =df2[df2['asin'] == inp_asin]
    if book.empty:
        print(f"{inp_asin} not found")
        return pd.DataFrame(columns = ['asin','title','main_category'])
    
    print(book[['title', 'main_category','final_price']])
    
    category = int(book['main_category'].iloc[0])

    same_category_books = df2[
        (df2['main_category'].astype(int) == category) &
        (df2['asin'] != inp_asin)
    ]
    
    
    if same_category_books.empty:
        print(f"No books in the category {category} available")
        return pd.DataFrame(columns=['asin', 'title', 'main_category'])
    
    recommended_books = same_category_books.sort_values(
        by=['main_rank', 'reviews_count', 'rating'],
        ascending=[True, False, False]
    )
    
    top_recommendations = recommended_books.head(num_recs)
    return top_recommendations[['asin', 'title', 'rating', 'main_category']]

def data_preprocessing(df):
    """
    Read the dataset containing cleaned data, make a copy, normalize columns 'initial_price', 'final_price', 'reviews_count',
    'number_of_sellers','main_category','main_rank','rating'.
    Normalization functions are defined with documentation in Normalization/Normalizer.py
    
    Args:
        data (str): _dataset path
        
    Returns:
        pd.DataFrame: DataFrame normalized
    """
    
    df2 = df.copy()
    
    df_norm = Normalizer.normalize_prices(df2)
    df_norm = Normalizer.normalize_reviews(df_norm)
    df_norm = Normalizer.normalize_rating(df_norm)
    df_norm = Normalizer.normalize_root_bs_rank(df_norm)
    df_norm = Normalizer.normalize_number_of_sellers(df_norm)
    
    #handle NaN values
    df_norm['final_price'].fillna(df_norm['final_price'].mean())
    df_norm['reviews_normalized'].fillna(df_norm['reviews_normalized'].mean())
    df_norm['main_rank'].fillna(df_norm['main_rank'].mean()) 
    df_norm['rating_normalized'].fillna(df_norm['rating_normalized'].mean())

    
    return df_norm

def knn_category_recommender(df, inp_asin, num_recs = 5):
    """
   Content-Based model to recommends books similar to a given one (identified by its ASIN), based on final price and review count,
    using the Nearest Neighbors algorithm within the same category.
   
   The Nearest Neighbors model is applied to the normalized columns 'final_price' and 'reviews_count' and 
    it calculates the Euclidean distance between books in this feature space and returns those closest
    to the selected book  that is, the most similar books in terms of price and reviews count.
    
   The method  returns the dataframe with the results or an empty dataframe if the asin code is not correct or the category of the book is unique.
   

    Args:
        df (pd.DataFrame):  A DataFrame containing normalized book data, including ASIN, final_price,
                           reviews_count, and main_category.
        inp_asin (str): input asin code.
        num_recs (int, optional): number of reccomended books to return.
        
    Returns:
        pd.DataFrame: A DataFrame containing the recommended books with relevant columns.
    """
    
    df2 = df.copy()
    
    # Check if the ASIN code is valid
    book = df2[df2['asin'] == inp_asin]
    if book.empty:
        print(f"{inp_asin} not found")
        return pd.DataFrame(columns=['asin', 'title', 'final_price', 'reviews_count', 'main_category'])
    
    # Extract book category
    category = book['main_category'].iloc[0]
    print(book[['title', 'final_price', 'main_category', 'reviews_count']])
    
    # Filter books in the same category excluding the input
    same_category_books = df2[
        (df2['main_category'] == category) & 
        (df2['asin'] != inp_asin)  
    ].copy()  
    
    if same_category_books.empty:
        print(f"No books in the category {category} available")
        return pd.DataFrame(columns=['asin', 'title', 'main_category'])
    
    # Prepare data for the model
    features = ['final_price', 'reviews_normalized']
    
    # Handle missing values without inplace
    same_category_books = same_category_books.dropna(subset=features).reset_index(drop=True)
    
    # Fit NearestNeighbors model
    knn = NearestNeighbors(n_neighbors=min(num_recs, len(same_category_books)), 
                          metric='euclidean')
    
    # Convert to numpy array to avoid feature names warning
    X = same_category_books[features].values
    knn.fit(X)
    
    # Get target book features
    target_book = book[features].values
    
    # Find nearest neighbors
    distances, indices = knn.kneighbors(target_book)
    
    # Get recommendations
    recommended = same_category_books.iloc[indices[0]]
    
    return recommended[['asin', 'title', 'final_price', 'reviews_count', 'main_category']]

"""
def hdbscan_reccomender(df, inp_asin, num_recs = 5):
   
    Content-Based model that recommends books similar to a given one (identified by its ASIN)
    using HDBSCAN clustering on UMAP-reduced numerical features.
    
    Given the ASIN of a book, this function:
    1. Extract the book by its asin code and check if the asin code is valid,
       then select the quantitative normalized variables on which to base the reccomandation model.
       
    2.Create the matrix X and initialize it with the values of the normalized variables, then reduce matrix to an array of 2 columns using
       umap, the two columns represent X and Y coordinates in the reduced space.
       UMAP preserve local similarities in high-dimensional data while enabling clustering.
       
    3. Applies the HDBSCAN algorithm on the reduced matrix,to group similar books based on the UMAP output.
       The algorithm assigns each book the cluster label, -1 if it is considered an outlier(noise).
    
    4. Adds the UMAP coordinates (umap_x, umap_y) and the number of clusters for each book to the DataFrame.
    
    5. Retrieves the book cluster requested by the user and other books in the same cluster excluding the same book the user searched for.
    
    6. Calculates the Euclidean distance between each book in the same cluster and the given input book,
       sorts books by increasing distance and takes the first num_recs and returns the dataframe with the columns 
       'asin', 'title', 'final_price', 'reviews_count', 'rating', 'main_category'.

    Args:
        df (_type_): _description_
        inp_asin (_type_): _description_
        num_recs (int, optional): _description_. Defaults to 10.
        
    Returns:
        pd.DataFrame: A DataFrame containing the recommended books with relevant columns.
    
    
    df2 = df.copy()
    
    #check if the asin code is valid
    book =df[df['asin'] == inp_asin]
    if book.empty:
        print(f"{inp_asin} not found")
        return pd.Dataframe(columns = ['asin','title','final_price','reviews_count','main_category'])
    
    #columns to use
    cols = ['final_price','reviews_normalized', 'main_rank','rating_normalized']
    
    X = df2[cols].values
    
    # Dimensionality reduction using umap
    reducer = umap.UMAP(n_components=2, random_state=42)
    X_umap = reducer.fit_transform(X)
    
    # Clustering
    clusterer = hdbscan.HDBSCAN(min_cluster_size=10)
    cluster_labels = clusterer.fit_predict(X_umap)

    df2['umap_x'] = X_umap[:, 0]
    df2['umap_y'] = X_umap[:, 1]
    df2['cluster'] = cluster_labels

    # Get cluster of the input book
    input_cluster = df2[df2['asin'] == inp_asin]['cluster'].values[0]

    #handle noise clusters
    if input_cluster == -1:
        print(f"No similar book found")
        return pd.DataFrame()

    # Filter other books in the same cluster
    same_cluster_books = df2[
        (df2['cluster'] == input_cluster) &
        (df2['asin'] != inp_asin)
    ]

    if same_cluster_books.empty:
        print(f"No other books found in cluster {input_cluster}.")
        return pd.DataFrame()

    # Compute distance in UMAP space
    input_coords = df2[df2['asin'] == inp_asin][['umap_x', 'umap_y']].values[0]
    same_cluster_books['distance'] = same_cluster_books.apply(
        lambda row: np.linalg.norm(np.array([row['umap_x'], row['umap_y']]) - input_coords),
        axis=1
    )

    # Return top-N closest in UMAP space
    recommended = same_cluster_books.sort_values(by='distance').head(num_recs)

    return recommended[['asin', 'title', 'final_price', 'reviews_count', 'rating', 'main_category']]
"""

def kmeans_reccomender(df,inp_asin,num_recs = 5):
    """
    Content-Based model to recommends books similar to a given one (identified by its ASIN), based on final price and reviews count,
     by using the K-Means clustering algorithm within the same category combined with dimensionality reduction via UMAP.
    
    K-Means is a simple and effective clustering algorithm that performs well when the data is dense and continuous (e.g., price, normalized rating).
    
    UMAP reduces the high-dimensional data into a 2D space while preserving structure.
    
    This combination (UMAP + KMeans) allows grouping similar books not just by direct feature similarity,
       but also by latent structure in the data, improving recommendation quality in complex  high-dimensional datasets.
       
    The function performs the following steps:
    
       - **ASIN Code validation:** if the input asin code is not valid, returns an empry dataframe with the selected columns.
       
       - **Columns selection:** 'title','final_price','main_category','reviews_count'.
       
       - **UMAP Reduction:** Reduces the feature space to 2 dimensions using UMAP, which preserve local and global structure of data.
       
       - **Clustering(KMeans):**  Applies K-Means clustering to group books into 10 distinct clusters based on their position in the UMAP space,
                                  the algorithm assign a cluster label to each book.
                                
       - **Neighbor Filtering:** Identify books within the same cluster, sharing the same category and exclude the input book.
       
       - **Reccomend the nearest books in the UMAP space:** Computes the Euclidean distance between the input book and all books in the same cluster/category
                                                            using UMAP coordinates.Returns the closest `num_recs` books as recommendations.
                                                            
     Args:
        df (pd.DataFrame):  A DataFrame containing normalized book data, including ASIN, final_price,
                           reviews_count, and main_category.
        inp_asin (str): input asin code.
        num_recs (int, optional): number of reccomended books to return.
        
    Returns:
        pd.DataFrame: A DataFrame containing the recommended books with relevant columns.
    """
    df2 = df.copy()
    
    #check if the asin code is valid
    book =df[df['asin'] == inp_asin]
    if book.empty:
        print(f"{inp_asin} not found")
        return pd.DataFrame(columns = ['asin','title','final_price','reviews_count','main_category'])
    
    print(book[['title','final_price','main_category', 'reviews_count']])
    
    #columns to use
    cols = ['final_price','reviews_normalized', 'main_category','rating_normalized']
    
    X = df2[cols].values
    
    # Dimensionality reduction using umap
    reducer = umap.UMAP(n_components=2, random_state=42)
    X_umap = reducer.fit_transform(X)
    
    # Clustering with K-Means
    kmeans = KMeans(n_clusters=10, random_state=42) 
    clusters = kmeans.fit_predict(X_umap)
    
    # Add UMAP coordinates and cluster labels to the DataFrame
    df2['umap_x'] = X_umap[:, 0]
    df2['umap_y'] = X_umap[:, 1]
    df2['cluster'] = clusters
    
    # find the cluster of the target book
    target_cluster = df2[df2['asin'] == inp_asin]['cluster'].values[0]
    target_category = book['main_category'].values[0]

    same_cluster = df2[
        (df2['cluster'] == target_cluster) &
        (df2['main_category'] == target_category) &
        (df2['asin'] != inp_asin)
    ].copy()

    if same_cluster.empty:
        print(f"No similar books found in cluster {target_cluster}.")
        return pd.DataFrame(columns=['asin', 'title', 'final_price', 'reviews_count', 'main_category'])

    # Calculate distances in UMAP space and recommend the nearest books in the UMAP space
    input_coords = df2[df2['asin'] == inp_asin][['umap_x', 'umap_y']].values[0]
    same_cluster.loc[:, 'distance'] = same_cluster.apply(
    lambda row: np.linalg.norm([row['umap_x'], row['umap_y']] - input_coords),
    axis=1
)
    recommended = same_cluster.sort_values('distance').head(num_recs) # Return top-N closest in UMAP space
    
    return recommended[['asin', 'title', 'final_price', 'reviews_count', 'rating', 'main_category']]


