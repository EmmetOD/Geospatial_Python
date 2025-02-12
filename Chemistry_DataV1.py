#Version 1 of water data visualisation 
# CRS: ING EPSG: 29902 

import pandas as pd 
import geopandas as gpd 
from shapely.geometry import Point
import leafmap
import matplotlib.pyplot as plt 


### Section 1 ###

## Loading and transforming data ## 

#Convert water data and stations into pandas dataframes 

water_data_raw = pd.read_csv('/Users/emmet/Desktop/WaterData/water_all_data.csv')
stations = pd.read_csv('/Users/emmet/Desktop/WaterData/stations.csv')
rivers = gpd.read_file('/Users/emmet/Desktop/WaterData/dublin_rivers.geojson')


#rename columns to allow for later join
water_data = water_data_raw.rename(columns={'MonitoringStationCode': 'StationID'}) 

water_data["SampleDate"] = pd.to_datetime(water_data["SampleDate"], format="%d/%m/%Y")


#Create point objects from Lat/Long columns 
geometry = [Point(xy) for xy in zip(stations["Longitude"], stations["Latitude"])]
geo_stations = gpd.GeoDataFrame(stations, geometry=geometry, crs="EPSG:29902")


#Outer Join (Merge) of two datasets for georeferenced chemistry data 
full_data = geo_stations.merge(water_data, on="StationID")

print(full_data.head())

# Create buffer around river polyline 
rivers_buffer50 = rivers.copy()
rivers_buffer50["geometry"] = rivers_buffer50.geometry.buffer(50)  # 50m buffer

#print(rivers_buffer50.head())

#Dataframes now in use:

#Geo-referenced Chemistry Data - full_data
#River Buffers - rivers_buffer50

full_data.plot()


### Section 2 ###

## Interpolation and time series handling ##





