import pandas as pd
#load the dataset VAStra Store from the excel file to a pandas dataframe:

filename = r"dataset.csv"
def load_dataset(path, sheet_name = "VAStra Store"):
    """
    Load the dataset from the excel file to a pandas dataframe.
    
    Parameters:
    path (str): The path to the excel file.
    sheet_name (str): The name of the sheet to load. Default is "VAStra Store".
    
    Returns:
    pd.DataFrame: The loaded dataframe.
    """
    df = pd.read_excel(path, sheet_name=sheet_name)
    #change labels values
    df.index = range(1, len(df) + 1)
    df = df.drop('index', axis=1, errors='ignore')
    return df

def store_to_csv(path):
    """
    Store the dataset to dataset.csv file.
    
    Parameters:
    path (str): The path to the csv file.
    
    Returns:
    None
    """
    df = load_dataset(filename)
    df.to_csv(path, index=False)
    print(f"Dataset stored to {path}")
