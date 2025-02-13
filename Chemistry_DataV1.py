import pandas as pd 
import geopandas as gpd 
from shapely.geometry import Point
import leafmap
import ipyleaflet
from ipywidgets import IntSlider, VBox, Output
from IPython.display import display as ipy_display

# Load and prepare data 
dodder20 = pd.read_csv('/Users/emmet/Desktop/WaterData/Dodder_020.csv')
dodder30 = pd.read_csv('/Users/emmet/Desktop/WaterData/Dodder_030.csv')
dodder40 = pd.read_csv('/Users/emmet/Desktop/WaterData/Dodder_040.csv')
water_data_raw = pd.concat([dodder20, dodder30, dodder40], axis=0)

stations = pd.read_csv('/Users/emmet/Desktop/WaterData/stations.csv')
rivers = gpd.read_file('/Users/emmet/Desktop/WaterData/dublin_rivers.geojson')

water_data = water_data_raw.rename(columns={'MonitoringStationCode': 'StationID'}) 
stations = stations.rename(columns={'Latitude': 'latitude', 'Longitude': 'longitude'})

water_data["SampleDate"] = pd.to_datetime(water_data["SampleDate"], format="%d/%m/%Y")

geometry = [Point(xy) for xy in zip(stations["longitude"], stations["latitude"])]
geo_stations = gpd.GeoDataFrame(stations, geometry=geometry, crs="EPSG:4326")

full_data = geo_stations.merge(water_data, on="StationID")
ph_data = full_data[full_data["ParameterName"] == "pH"]

ph_median_monthly = ph_data.groupby([ph_data["SampleDate"].dt.to_period("M"), "StationID"]).agg({
    "Result": "median", 
    "latitude": "first", 
    "longitude": "first",
    "MonitoringStationName": "first"
}).reset_index()

ph_median_monthly["SampleDate"] = ph_median_monthly["SampleDate"].astype(str)
months = sorted(ph_median_monthly["SampleDate"].unique())

# Determine global min and max pH for consistent scaling
min_pH, max_pH = 6.8, 8.2

# Create map 
m = leafmap.Map(center=[53.3, -6.3], zoom=12)
m.add_basemap("CartoDB.DarkMatter")
m.add_gdf(rivers, layer_name="Rivers")
heatmap_layer = ipyleaflet.Heatmap()
heatmap_layer.blur = 50
heatmap_layer.radius = 50
heatmap_layer.max_zoom = 1
heatmap_layer.min_opacity = 0.7
heatmap_layer.gradient = {
    0.5: 'blue',
    0.7: 'green',
    1.0: 'red'
}
m.add_layer(heatmap_layer)

# Output widget for displaying pH values
output = Output()

# Slider widget
slider = IntSlider(min=0, max=len(months) - 1, step=1, description='Month:')

def update_visuals(change):
    current_period = months[slider.value]
    filtered_data = ph_median_monthly[ph_median_monthly["SampleDate"] == current_period].copy()
    
    # Normalize pH values using fixed scale
    filtered_data["scaled_pH"] = (filtered_data["Result"] - min_pH) / (max_pH - min_pH)
    filtered_data["scaled_pH"] = filtered_data["scaled_pH"].clip(0, 1)
    
    # Update heatmap layer
    heatmap_layer.locations = filtered_data[["latitude", "longitude", "scaled_pH"]].dropna().values.tolist()
    
    # Update output values
    with output:
        output.clear_output(wait=True)
        print(f"pH Values for {current_period}:")
        print(filtered_data[["MonitoringStationName", "Result"]].to_string(index=False))

slider.observe(update_visuals, names='value')

# Display map, slider, and output
ipy_display(m)
ipy_display(VBox([slider, output]))

# Initialize with first month
default_period = months[0]
default_data = ph_median_monthly[ph_median_monthly["SampleDate"] == default_period].copy()
default_data["scaled_pH"] = (default_data["Result"] - min_pH) / (max_pH - min_pH)
default_data["scaled_pH"] = default_data["scaled_pH"].clip(0, 1)
heatmap_layer.locations = default_data[["latitude", "longitude", "scaled_pH"]].dropna().values.tolist()
with output:
    print(f"pH Values for {default_period}:")
    print(default_data[["MonitoringStationName", "Result"]].to_string(index=False))
