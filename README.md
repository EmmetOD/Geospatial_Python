Heres some Geospatial Projects and Workflows: 

1. Dodder River Heatmap workflow
   
This project pipes water chemistry data from the EPA (Enviromental Protection Agency) to a time series visualistion using LeafMap.

The script first takes in 
   - Water Chemistry Data (Multiple CSV files - 10k rows each)
   - Water Sampling Location GeoJSON

Operations 
- Read CSVs into Pandas Dataframes
- Merge Dataframes
- Join Dataframes to Sampling Location GeoJSON based on monitoring station name
- 



