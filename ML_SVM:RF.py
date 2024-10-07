import numpy as np
import rasterio
from rasterio.features import rasterize
from shapely.geometry import mapping
from sklearn.model_selection import train_test_split
import geopandas as gpd
import warnings

# Ignore Shapely deprecation warnings
warnings.filterwarnings('ignore')

# Function to load and process the geospatial training data
def load_geospatial_data(train_data_path, raster_path):
    """
    Loads the geospatial training data, rasterizes the training points, and prepares the samples and labels.
    
    Parameters:
    - train_data_path: Path to the shapefile containing training points.
    - raster_path: Path to the raster image (e.g., Sentinel-2).
    
    Returns:
    - train_samples: Flattened array of the raster data.
    - train_labels: Corresponding labels for the training data.
    - s2_meta: Metadata of the raster image.
    """
    # Load the GeoDataFrame (training points with labels)
    train_data = gpd.read_file(train_data_path)

    # Get unique class labels
    class_labels = np.unique(train_data['Class'])
    
    # Load the raster image
    with rasterio.open(raster_path) as src:
        s2_data = src.read()   # Read the raster data
        s2_meta = src.meta     # Get metadata of the raster
        crs = src.crs          # Coordinate reference system
        print(f'Coordinate Reference System: {crs}')
    
    # Rasterize the training points to create a mask
    train_mask = rasterize(
        [(mapping(point), class_label) for point, class_label in zip(train_data.geometry, train_data['Class'])],
        out_shape=s2_data.shape[1:], 
        transform=src.transform, 
        fill=-1, 
        dtype='int16'
    )
    
    # Flatten the raster image into a 2D array
    s2_data_2d = s2_data.reshape(s2_data.shape[0], -1).T
    
    # Extract the training samples and corresponding labels
    train_samples = s2_data_2d[train_mask.flatten() != -1]
    train_labels = train_mask.flatten()[train_mask.flatten() != -1]

    return train_samples, train_labels, s2_meta

# Function to split data into training and testing sets
def split_train_test(train_samples, train_labels, test_size=0.1):
    """
    Splits the data into training and testing sets.
    
    Parameters:
    - train_samples: Array of training data samples.
    - train_labels: Array of corresponding labels for the training samples.
    - test_size: Proportion of the data to be used for testing.
    
    Returns:
    - X_train: Training samples.
    - X_test: Testing samples.
    - y_train: Training labels.
    - y_test: Testing labels.
    """
    X_train, X_test, y_train, y_test = train_test_split(
        train_samples, train_labels, test_size=test_size, random_state=42, stratify=train_labels
    )
    return X_train, X_test, y_train, y_test

# Main function to run the data loading and splitting process
def main():
    """
    Main execution function that loads geospatial data, processes it, and splits it into training and testing sets.
    """
    # File paths (replace with actual paths)
    train_data_path = 'path_to_training_points.shp'  
    raster_path = 'LillyBandsOBIADSM1.tif'

    # Load and process the geospatial data
    train_samples, train_labels, s2_meta = load_geospatial_data(train_data_path, raster_path)
    
    # Split the data into train and test sets
    X_train, X_test, y_train, y_test = split_train_test(train_samples, train_labels)
    
    # Print the sizes of training and testing sets
    print(f'Training set size: {X_train.shape[0]}')
    print(f'Testing set size: {X_test.shape[0]}')

# Entry point
if __name__ == '__main__':
    main()
