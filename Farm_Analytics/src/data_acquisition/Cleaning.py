import pandas as pd
pd.set_option('display.float_format', '{:.2f}'.format) # round float values to 2 decimal places
def handle_timezone(hourly_df, daily_df):
    """
    Handle values for the column date in the DataFrames hourly_df and daily_df.
    The columns date in both DataFrames are datetime64[ns,UTC] type,
      the function converts them to datetime64[ns] object to remove the timezone information and get only the date part.
    Args:
        hourly_df (pd.DataFrame): DataFrame having hourly weather data.
        daily_df (pd.DataFrame): DataFrame having daily weather data.
    Returns:
        hourly_df (pd.DataFrame): DataFrame having date column converted to datetime64[ns] type.
        daily_df (pd.DataFrame): DataFrame having date column converted to datetime64[ns] type.
    """
    hourly_df = hourly_df.copy()
    daily_df = daily_df.copy()
    hourly_df["date"] = pd.to_datetime(hourly_df["date"]).dt.date
    daily_df["date"] = pd.to_datetime(daily_df["date"]).dt.date
    return hourly_df, daily_df

def handle_daylight_duration(daily_df):
    # convert the column daylight_duration in daily_df from seconds to hours
    daily_df = daily_df.copy()
    daily_df["daylight_duration"] = daily_df["daylight_duration"] / 3600
    return daily_df


def merge_dataframes(hourly_df, daily_df):
    # Merge the hourly and daily DataFrames on the date column.
    merged_df = pd.merge(hourly_df, daily_df, on="date", how="outer")
    return merged_df

def get_NaN_values(merged_df):
    #get the sum of the NaN values in each column of the merged DataFrame.
    return merged_df.isna().sum()

def handle_NaN_values(merged_df):
    #fill NaN values of the column daylight_duration with the mean of the column.
    mean = merged_df["daylight_duration"].mean()
    merged_df["daylight_duration"].fillna(mean, inplace=True)
    return merged_df
