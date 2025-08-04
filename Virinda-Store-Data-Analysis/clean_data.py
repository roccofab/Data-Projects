import numpy as np
import pandas as pd
#introduce missing values into the loaded dataset and show how to handle missing values
def introduce_nan(df):
    df.loc[10:12, 'Age'] = np.nan
    df.loc[50:52, 'SKU'] = np.nan
    df.loc[100:102, 'Status'] = np.nan
    df.loc[20:22, 'Age'] = None
    df.loc[30:32, 'ship-state'] = None
    df.loc[40:42, 'Status'] = None
    return df
    
def show_values_nan(df):
    print("\nDataframe with null values:\n")
    return df.isnull().sum()

def fill_missing_Age_values(df):
    #replace NaN value of the column Age with mean value of the column Age:
    mean_age = df['Age'].mean()
    df['Age'].fillna(mean_age, inplace=True)
    print("\nRows of the column Age with NaN values:\n")
    return df.isna().sum()

def fill_missing_shipState(df):
    #replace NaN value of the column ship-state with mode value of the column ship-state:
    mode_ship_state = df['ship-state'].mode()[0]
    df['ship-state'].fillna(mode_ship_state, inplace=True)
    print("\nRows with NaN values in the column ship-state:\n")
    return df.isna().sum()

def fill_missing_status(df):
    df['Status'].fillna('Unknown', inplace=True)
    print("\nRows with NaN values in the column Status:\n")
    return df.loc[df['Status'] == 'Unknown', 'Status']

def fill_missing_SKU(df):
    df['SKU'].fillna('Unknown', inplace = True)
    print("\nRows with NaN values in the column SKU:\n")
    return df.loc[df['SKU'] == 'Unknown', 'SKU']

    
    