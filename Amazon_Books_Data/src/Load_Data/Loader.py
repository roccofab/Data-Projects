import pandas as pd

#load the dataset Amazon_popular_books_dataset.csv  to a pandas dataframe:
filename = r"C:\\Users\\lenovo\\Documents\\analytics\\Amazon_Books_Data\\Amazon_popular_books_dataset.csv"

def load_dataset(path):
    """Load the dataset from a CSV file into a pandas DataFrame.

    Args:
        path (str): The file path to the CSV file.
    """
    df = pd.read_csv(path)
    #change labels values
    df.index = range(1, len(df) + 1)
    df = df.drop('index', axis=1, errors='ignore')
    return df

