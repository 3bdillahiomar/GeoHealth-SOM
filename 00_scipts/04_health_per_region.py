# In this script, we will count how many health facilities 
# are in each region and visualize the results using the shapefile. 
# We will use the same shapefile as in the previous script.

import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns

# File paths
health_facilities_shp = r"\conflict_climate_health\who_health_sites\WHO_health_sites.shp"
conflict_shp = r"\conflict_climate_health\conflict_data\total_fatalities\Somalia_Regions_with_Events.shp"
output_shp = r"\conflict_climate_health\conflict_data\total_fatalities\Somalia_Regions_with_Health_Events.shp"

# Load datasets
health_gdf = gpd.read_file(health_facilities_shp)  # Health facilities (points)
conflict_gdf = gpd.read_file(conflict_shp)  # Somalia admin boundaries with conflict data (polygons)

# Ensure CRS is consistent
if health_gdf.crs != conflict_gdf.crs:
    health_gdf = health_gdf.to_crs(conflict_gdf.crs)

# Spatial join: Assign health facilities to regions
health_joined = gpd.sjoin(health_gdf, conflict_gdf, how="left", predicate="within")
print(health_joined)

# Count health facilities per region
health_counts = health_joined.groupby("admin1").size().reset_index(name="health_facilities")
print(health_counts)

# Merge health facility counts with conflict data
conflict_gdf = conflict_gdf.merge(health_counts, on="admin1", how="left")
print(conflict_gdf)

# Fill missing values (regions with no health facilities) with 0
conflict_gdf["health_facilities"] = conflict_gdf["health_facilities"].fillna(0)
print(conflict_gdf.head)

# Save the updated shapefile
conflict_gdf.to_file(output_shp)

print(f"Processed shapefile saved at: {output_shp}")


# --- Visualization ---
fig, ax = plt.subplots(1, 1, figsize=(10, 8))

conflict_gdf.plot(column="health_facilities", 
                  cmap="Blues", 
                  linewidth=0.8, 
                  edgecolor="black",
                  legend=True,
                  legend_kwds={'label': "Number of Health Facilities",
                               'orientation': "vertical"},
                  ax=ax)

ax.set_title("Health Facilities per Region in Somalia", fontsize=14)
ax.set_axis_off()
plt.show()

###################################################################################################################################

import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Load processed data
shp_path = r"\conflict_climate_health\conflict_data\total_fatalities\Somalia_Regions_with_Health_Events.shp"
gdf = gpd.read_file(shp_path)
gdf.head()

# Convert to Pandas DataFrame for easier plotting
df = gdf[["admin1", "fatalities", "event_coun", "health_fac"]]
df.head()

# --- 📌 1. Choropleth Map: Health Facility Density ---
fig, ax = plt.subplots(1, 1, figsize=(10, 8))
gdf.plot(column="health_fac", cmap="Blues", linewidth=0.8, edgecolor="black", 
         legend=True, legend_kwds={'label': "Number of Health Facilities", 'orientation': "vertical"}, ax=ax)
ax.set_title("Health Facilities per Region in Somalia", fontsize=14)
ax.set_axis_off()
plt.show()

# --- 📌 2. Bar Chart: Comparing Fatalities vs Conflict Events ---
fig, ax = plt.subplots(figsize=(12, 6))
df_sorted = df.sort_values(by="fatalities", ascending=False)
sns.barplot(data=df_sorted, x="admin1", y="fatalities", color="red", label="Fatalities")
sns.barplot(data=df_sorted, x="admin1", y="event_coun", color="blue", alpha=0.6, label="Conflict Events")
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
ax.set_title("Fatalities vs. Conflict Events per Region")
ax.set_ylabel("Count")
ax.legend()
plt.show()

# --- 📌 3. Scatter Plot: Conflict Events vs. Health Facilities ---
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df, x="event_coun", y="health_fac", size="fatalities", hue="fatalities", 
                palette="coolwarm", sizes=(20, 300))
plt.xlabel("Conflict Events")
plt.ylabel("Health Facilities")
plt.title("Conflict Events vs. Health Facilities")
plt.legend(title="Fatalities")
plt.grid(True)
plt.show()

# --- 📌 4. Bubble Chart: Health Facilities vs. Fatalities ---
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x="health_fac", y="fatalities", size="event_coun", hue="event_coun", 
                palette="viridis", sizes=(20, 300))
plt.xlabel("Health Facilities")
plt.ylabel("Fatalities")
plt.title("Health Facilities vs. Fatalities (Bubble Size = Conflict Events)")
plt.legend(title="Conflict Events")
plt.grid(True)
plt.show()


import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Ensure correct column names
df = df.rename(columns={"health_fac": "health_facilities"})  # If needed

# --- 📌 1. Proportional Bar Chart ---
fig, ax = plt.subplots(figsize=(14, 6))

bar_width = 0.8  # Width of bars
regions = df["admin1"]

# Plot conflict events (negative for proportionality)
ax.bar(regions, -df["event_coun"], color="skyblue", label="Non-Fatal Events")
# Plot fatalities
ax.bar(regions, df["fatalities"], color="red", label="Fatalities")
# Plot health facilities (scaled to fit)
ax.bar(regions, df["health_facilities"] * 50, color="green", alpha=0.7, label="Health Facilities (Scaled)")

ax.set_xticklabels(regions, rotation=45, ha="right")
ax.set_title("Proportional Representation of Conflict Events, Fatalities & Health Facilities per Region")
ax.set_ylabel("Count (Health Facilities Scaled x50)")
ax.legend()
plt.show()

# --- 📌 2. Side-by-Side Bar Charts ---
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Conflict Events
axes[0].bar(df["admin1"], df["event_coun"], color="blue")
axes[0].set_title("Number of Conflict Events per Region")
axes[0].set_ylabel("Event Count")
axes[0].set_xticklabels(df["admin1"], rotation=45, ha="right")

# Fatalities
axes[1].bar(df["admin1"], df["fatalities"], color="red")
axes[1].set_title("Number of Fatalities per Region")
axes[1].set_ylabel("Fatalities Count")
axes[1].set_xticklabels(df["admin1"], rotation=45, ha="right")

# Health Facilities
axes[2].bar(df["admin1"], df["health_facilities"], color="green")
axes[2].set_title("Number of Health Facilities per Region")
axes[2].set_ylabel("Health Facility Count")
axes[2].set_xticklabels(df["admin1"], rotation=45, ha="right")

plt.tight_layout()
plt.show()

# --- 📌 3. Stacked Bar Chart ---
fig, ax = plt.subplots(figsize=(14, 6))
bar_width = 0.8

# Stacking the bars
p1 = ax.bar(df["admin1"], df["event_coun"], color="blue", label="Conflict Events")
p2 = ax.bar(df["admin1"], df["fatalities"], bottom=df["event_coun"], color="red", label="Fatalities")
p3 = ax.bar(df["admin1"], df["health_facilities"], bottom=df["event_coun"] + df["fatalities"], color="green", label="Health Facilities")

ax.set_xticklabels(df["admin1"], rotation=45, ha="right")
ax.set_title("Stacked Representation of Health Facilities, Conflict Events & Fatalities")
ax.set_ylabel("Total Count")
ax.legend()
plt.show()

####################################################################################################################################

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

# Ensure correct column names
df = df.rename(columns={"health_fac": "health_facilities"})  # If needed

# --- 📌 1. Correlation Heatmap ---
plt.figure(figsize=(8, 6))
sns.heatmap(df[["fatalities", "event_coun", "health_facilities"]].corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap: Conflict Events, Fatalities & Health Facilities")
plt.show()

# --- 📌 2. Scatter Plot Matrix (Pairplot) ---
sns.pairplot(df[["fatalities", "event_coun", "health_facilities"]], diag_kind="kde", palette="husl")
plt.suptitle("Pairwise Relationships: Conflict Events, Fatalities & Health Facilities", y=1.02)
plt.show()

# --- 📌 3. Multi-Axis Line Chart ---
fig, ax1 = plt.subplots(figsize=(12, 6))

# First Y-axis (Conflict Events & Fatalities)
ax1.set_xlabel("Region")
ax1.set_ylabel("Conflict Events & Fatalities")
ax1.plot(df["admin1"], df["event_coun"], color="blue", marker="o", label="Conflict Events", linestyle="dashed")
ax1.plot(df["admin1"], df["fatalities"], color="red", marker="s", label="Fatalities", linestyle="solid")
ax1.tick_params(axis="y")

# Second Y-axis (Health Facilities)
ax2 = ax1.twinx()
ax2.set_ylabel("Health Facilities")
ax2.plot(df["admin1"], df["health_facilities"], color="green", marker="D", label="Health Facilities", linestyle="dotted")
ax2.tick_params(axis="y")

fig.tight_layout()
ax1.set_xticklabels(df["admin1"], rotation=45, ha="right")
ax1.set_title("Multi-Axis Line Chart: Conflict Events, Fatalities & Health Facilities")

# Combine legends
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc="upper left")

plt.show()

# --- 📌 4. Radar Chart (Spider Chart) ---
from math import pi

# Normalize data for better visualization
df_norm = df.copy()
df_norm["fatalities"] = df["fatalities"] / df["fatalities"].max()
df_norm["event_coun"] = df["event_coun"] / df["event_coun"].max()
df_norm["health_facilities"] = df["health_facilities"] / df["health_facilities"].max()

categories = ["fatalities", "event_coun", "health_facilities"]
N = len(categories)

angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]  # Repeat first angle to close the circle

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

for i, row in df_norm.iterrows():
    values = row[categories].tolist()
    values += values[:1]  # Close the circle
    ax.plot(angles, values, linewidth=1, linestyle="solid", label=row["admin1"])
    ax.fill(angles, values, alpha=0.1)

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories)
ax.set_title("Radar Chart: Conflict Events, Fatalities & Health Facilities")
ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))

plt.show()


