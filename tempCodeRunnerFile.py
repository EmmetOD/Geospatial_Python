import pandas as pd 
import geopandas as gpd 
from shapely.geometry import Point

#Loading and transforming data

#Convert water data and stations into pandas dataframes 
water_data_raw = pd.read_csv('/Users/emmet/Desktop/WaterData/water_all_data.csv')
stations = pd.read_csv('/Users/emmet/Desktop/WaterData/stations.csv')
rivers = gpd.read_file('/Users/emmet/Desktop/WaterData/rivers.geojson')

print(rivers.head())