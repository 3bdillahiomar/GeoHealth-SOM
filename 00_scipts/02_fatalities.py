# In this script, we will merge the ACLED different columns into the Somalia Admin Boundaries shapefile.

import geopandas as gpd
import pandas as pd

# Define file paths
acled_shp = r"\conflict_climate_health\conflict_data\ACLED_original_data\ACLED_Somalia_Fatalities.shp"
somalia_admin_shp = r"\conflict_climate_health\conflict_data\total_fatalities\00_conflict_total_fatalities.shp"
output_shp = r"\conflict_climate_health\conflict_data\total_fatalities\Somalia_Regions_with_Events.shp"

# Load the ACLED conflict data (point data)
acled_gdf = gpd.read_file(acled_shp)

# Load the Somalia administrative boundaries (polygon data)
somalia_admin_gdf = gpd.read_file(somalia_admin_shp)

# Ensure both GeoDataFrames have the same CRS (Coordinate Reference System)
if acled_gdf.crs != somalia_admin_gdf.crs:
    acled_gdf = acled_gdf.to_crs(somalia_admin_gdf.crs)

# Read the ACLED data columns
print("ACLED Columns:", acled_gdf.columns)

# Read the Somalia Admin Boundaries columns
print("Somalia Admin Columns:", somalia_admin_gdf.columns)

# Perform a spatial join to link conflict events with administrative regions
acled_joined = gpd.sjoin(acled_gdf, somalia_admin_gdf, how="left", predicate="within")
print("Columns in acled_joined after spatial join:", acled_joined.columns)

# Rename columns for clarity
acled_joined = acled_joined.rename(columns={"admin1_left": "admin1"})  # Use ACLED's admin1
somalia_admin_gdf = somalia_admin_gdf.rename(columns={"admin1_right": "admin1"})  # Use Somalia Regions' admin1

# Ensure "admin1" exists before grouping
print("Unique values in acled_joined['admin1']:", acled_joined["admin1"].unique())

# Count the number of conflict events per "admin1" region
events_per_admin = acled_joined.groupby("admin1").size().reset_index(name="event_count")

# Merge the event count with Somalia admin boundaries
somalia_admin_gdf = somalia_admin_gdf.merge(events_per_admin, on="admin1", how="left")

# Fill missing values (regions with no events) with 0
somalia_admin_gdf["event_count"] = somalia_admin_gdf["event_count"].fillna(0)

# Keep only required columns
somalia_admin_gdf = somalia_admin_gdf[["OBJECTID_1", "admin1Name", "admin1Pcod", "admin1", "fatalities", "event_count", "geometry"]]

# Print column names for debugging
print("Columns in somalia_admin_gdf after merge:", somalia_admin_gdf.columns)

# Save the result as a new shapefile
somalia_admin_gdf.to_file(output_shp)

print(f"Processed shapefile saved at: {output_shp}")