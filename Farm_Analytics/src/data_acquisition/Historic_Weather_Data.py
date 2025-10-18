
from datetime import date
from http.client import responses
from urllib import response
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
"""
This module fetches historic weather data from the Open Meteo API for the location Bari, Italy.

It retrieves both hourly and daily weather data, including temperature, precipitation, wind speed, and daylight duration.

Open Meteo does not provide historical data and current data at the same time with a single API call, but it provides
   two different endpoints for historical data(/archive) and Weather forecast data up to 14 days ahead(/forecast).
   
The data returned from these endpoint is  processed and cleaned before being stored in a database and then
   they will be integrated with production data.
   
This module is designed to be modular, allowing for easy integration with other components of the weather data pipeline.

You dont't need to install any dependencies because they are already included in the dependencies.txt file and
        you can install them by running the command from the root project directory:
           pip install -r dependencies.txt
"""

def fetch_historic_data():
	"""
    Fetch historic weather data from the Open Meteo API for the location Bari,Italy(Latitude: 41.1207, Longitude: 16.8698).
    The `fetch_historic_data` function initializes a session with automatic caching and retry handling,
      requests the Open Meteo API for hourly and daily weather data,
      and processes the response to create two DataFrames: one for hourly data and another for daily data.
      
    In this file I only fetches data from the API, data processing and cleaning operations
       are done in Cleaning.py file for a better modularity of the program.

	Returns:
		hourly_dataframe (pd.DataFrame): A DataFrame containing hourly weather data(date,temperature_2m,precipitation,wind-speed_10m).
		daily_dataframe (pd.DataFrame): A DataFrame containing daily weather data(date,daylight_duration).
	"""
	#Session setup with automatic cache and retry
	cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
	retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
	openmeteo = openmeteo_requests.Client(session=retry_session)

	#API params
	url = "https://archive-api.open-meteo.com/v1/archive"
	params = {
	"latitude": 41.1207,  #Latitude for location Bari, Italy
	"longitude": 16.8698,  #Longitude for location Bari, Italy
	"start_date": "2000-01-01",  #start date is '1999-12-31'
	"end_date": date.today().strftime("%Y-%m-%d"),  #end date is the current date
	"daily": "daylight_duration",   # Daily daylight duration parameter
	"hourly": ["temperature_2m", "precipitation", "wind_speed_10m"],  #hourly parameters
	"timezone": "Europe/London",  
	}
	responses = openmeteo.weather_api(url, params=params)
	response = responses[0]
 
	#extract and process hourly data from the response
	hourly = response.Hourly()  
	hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy() # Extracting hourly temperature at 2m from the ground
	hourly_precipitation = hourly.Variables(1).ValuesAsNumpy()  # Extracting hourly precipitation
	hourly_wind_speed_10m = hourly.Variables(2).ValuesAsNumpy()  # Extracting hourly wind speed 
 
	# Create a DataFrame with the hourly data
	hourly_data = {"date": pd.date_range(
	start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),   
	end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = hourly.Interval()),  # Frequency of the data
	inclusive = "left"  # Include the start date in the range
	)}


	# add extracted data to the DataFrame hourly_dataframe
	hourly_data["temperature_2m"] = hourly_temperature_2m
	hourly_data["precipitation"] = hourly_precipitation
	hourly_data["wind_speed_10m"] = hourly_wind_speed_10m

	hourly_dataframe = pd.DataFrame(data = hourly_data)

	#extract and process daily data from the response
	daily = response.Daily()
	daily_daylight_duration = daily.Variables(0).ValuesAsNumpy()  #daylight duration is the only daily parameter
    
	daily_data = {
        "date": pd.date_range(
	       start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
	       end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
	       freq = pd.Timedelta(seconds = daily.Interval()),
	       inclusive = "left"
	    ),
	    "daylight_duration": daily_daylight_duration
    }
	#convert daily_data to a DataFrame
	daily_dataframe = pd.DataFrame(data=daily_data)
	return hourly_dataframe, daily_dataframe

def get_data():
    #this function call the function fetch_historic_data 
    return fetch_historic_data()