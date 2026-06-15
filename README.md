Here's some Geospatial Projects and Workflows: 

** 1. Dodder River Heatmap workflow **
   
This project pipelines water chemistry data from the EPA (Enviromental Protection Agency) to a time series visualistion using LeafMap.

The script first takes in 
   - Water Chemistry Data (Multiple CSV files - 10k+ rows each)
   - Water Sampling Location GeoJSON

Workflow: 
- Download Water Chemistry CSV by catchment.
  
- Create Pandas Dataframe for each location.
  
- Join to Monitoring Quality Stations based on StationID allowing spatial reference (Lat,Long)
  
- Format columns for name, CRS and data type (Time format)
  
- Pull data of interest (Choride used here) as data stored in long format.


It then visualises the data using a slider interface on top of a Leafmap display.

In order to incorporate the Data within a ARCGIS Online application, the workflow found here can be used: 
https://storymaps.arcgis.com/stories/9a1f42437d4a4a9aa4599219e058c688 

![mon_stations_dublin](https://github.com/user-attachments/assets/6d2fb626-0a29-423e-96fe-d68414d01c52)
