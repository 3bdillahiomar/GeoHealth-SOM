# RO1. To analyze the impact of armed conflicts on the health facility coverage in Somalia.
# How do armed conflicts affect the geographical distribution and accessibility of health facilities in Somalia? 
# (SpatioTemperol)



import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import folium
from shapely.geometry import Point


# File paths
health_facilities_path = r"\conflict_climate_health\who_health_sites\WHO_health_sites.shp"
admin_boundaries_path = r"\conflict_climate_health\00_Boundaries\SOM_Adminbnda_Adm2_Regions\SOM_Adminbnda_Adm2_Regions_UNOCHA.shp"
conflict_data_path = r"\conflict_climate_health\ACLED\ACLED_Somalia_Fatalities.shp"

# Load data
health_gdf = gpd.read_file(health_facilities_path)
admin_gdf = gpd.read_file(admin_boundaries_path)
conflict_gdf = gpd.read_file(conflict_data_path)

# Read the first 5 rows of the health facilities GeoDataFrame
#print(health_gdf.head())
#print(admin_gdf.head())
#print(conflict_gdf.head())

# Ensure consistent CRS
target_crs = "EPSG:4326"  # WGS 84
health_gdf = health_gdf.to_crs(target_crs)
admin_gdf = admin_gdf.to_crs(target_crs)
conflict_gdf = conflict_gdf.to_crs(target_crs)

# Plot conflicts and health facilities
fig, ax = plt.subplots(figsize=(12, 8))
admin_gdf.plot(ax=ax, color="lightgrey", edgecolor="black")
health_gdf.plot(ax=ax, color="blue", markersize=5, label="Health Facilities")
conflict_gdf.plot(ax=ax, color="red", markersize=10, label="Conflict Events")
plt.legend()
plt.title("Health Facility Distribution & Conflict Zones in Somalia")
plt.show()

#########################################################################################
# Create a map of health facilities and conflict events per region
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import folium
from shapely.geometry import Point

# ---- File Paths ----
health_sites_path = r"\conflict_climate_health\who_health_sites\WHO_health_sites.shp"
admin_boundaries_path = r"\conflict_climate_health\00_Boundaries\SOM_Adminbnda_Adm2_Regions\SOM_Adminbnda_Adm2_Regions_UNOCHA.shp"
conflict_data_path = r"\conflict_climate_health\ACLED\ACLED_Somalia_Fatalities.shp"

# ---- Load Data ----
health_gdf = gpd.read_file(health_sites_path)
admin_gdf = gpd.read_file(admin_boundaries_path)
conflict_gdf = gpd.read_file(conflict_data_path)

# Print column names for debugging
print("Conflict Data Columns:", conflict_gdf.columns)

# ---- Ensure CRS Consistency ----
target_crs = "EPSG:4326"  # WGS 84
health_gdf = health_gdf.to_crs(target_crs)
admin_gdf = admin_gdf.to_crs(target_crs)
conflict_gdf = conflict_gdf.to_crs(target_crs)

# ---- Convert to GeoDataFrames ----
# Fix column references based on conflict dataset
health_gdf["geometry"] = health_gdf.apply(lambda row: Point(float(row["Long"]), float(row["Lat"])), axis=1)
conflict_gdf["geometry"] = conflict_gdf.apply(lambda row: Point(float(row["longitude"]), float(row["latitude"])), axis=1)

# ---- Spatial Join to Assign Regions ----
health_gdf = gpd.sjoin(health_gdf, admin_gdf, how="left", predicate="within")
conflict_gdf = gpd.sjoin(conflict_gdf, admin_gdf, how="left", predicate="within")

# ---- Aggregate Data per Region ----
region_health_counts = health_gdf.groupby("admin1Name").size().reset_index(name="Health_Facilities")
region_conflict_counts = conflict_gdf.groupby("admin1Name").size().reset_index(name="Conflicts")

# ---- Merge Aggregated Data into Administrative Boundaries ----
admin_gdf = admin_gdf.merge(region_health_counts, on="admin1Name", how="left").fillna(0)
admin_gdf = admin_gdf.merge(region_conflict_counts, on="admin1Name", how="left").fillna(0)

# ---- Static Map ----
fig, ax = plt.subplots(figsize=(12, 8))
admin_gdf.plot(column="Health_Facilities", cmap="Blues", edgecolor="black", linewidth=0.5, legend=True, ax=ax)
admin_gdf.plot(column="Conflicts", cmap="Reds", edgecolor="black", linewidth=0.5, alpha=0.5, legend=True, ax=ax)
plt.title("Health Facilities & Conflict Events Per Region in Somalia")
plt.show()

# can you make chart for the number of health facilities and conflict events per region?
# ---- Bar Chart ----
fig, ax = plt.subplots(figsize=(12, 8))
admin_gdf.plot(x="admin1Name", y="Health_Facilities", kind="bar", ax=ax, color="blue", legend=True)
admin_gdf.plot(x="admin1Name", y="Conflicts", kind="bar", ax=ax, color="red", alpha=0.5, legend=True)
plt.title("Health Facilities & Conflict Events Per Region in Somalia")
plt.show()


