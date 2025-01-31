# We will generate a time-series (animated) map to visualize how conflicts evolve 
# over time, while health facilities remain constant.
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---- File Paths ----
health_sites_path = r"\conflict_climate_health\who_health_sites\WHO_health_sites.shp"
conflict_data_path = r"\conflict_climate_health\ACLED\ACLED_Somalia_Fatalities.shp"

# ---- Load Data ----
health_gdf = gpd.read_file(health_sites_path)
conflict_gdf = gpd.read_file(conflict_data_path)

# ---- Convert Dates for Time-Series Analysis ----
conflict_gdf["event_date"] = pd.to_datetime(conflict_gdf["event_date"], errors="coerce")
conflict_gdf["year"] = conflict_gdf["event_date"].dt.year  # Extract year

# ---- Conflict Trends Over Time ----
plt.figure(figsize=(12, 6))
sns.lineplot(data=conflict_gdf.groupby("year").size().reset_index(name="conflicts"), x="year", y="conflicts", marker="o", color="red")
plt.title("Conflict Trends in Somalia (Yearly)", fontsize=14)
plt.xlabel("Year", fontsize=12)
plt.ylabel("Number of Conflicts", fontsize=12)
plt.grid(True)
plt.show()

# ---- Fatalities Distribution ----
plt.figure(figsize=(12, 6))
sns.histplot(conflict_gdf["fatalities"], bins=30, kde=True, color="purple")
plt.title("Distribution of Fatalities in Conflicts", fontsize=14)
plt.xlabel("Fatalities per Conflict", fontsize=12)
plt.ylabel("Frequency", fontsize=12)
plt.grid(True)
plt.show()

# ---- Conflict Hotspots by Region ----
plt.figure(figsize=(12, 6))
region_conflicts = conflict_gdf.groupby("admin1").size().reset_index(name="conflicts")
sns.barplot(data=region_conflicts.sort_values("conflicts", ascending=False), x="conflicts", y="admin1", palette="coolwarm")
plt.title("Top Conflict Hotspots by Region", fontsize=14)
plt.xlabel("Number of Conflicts", fontsize=12)
plt.ylabel("Region", fontsize=12)
plt.grid(axis="x")
plt.show()

# ---- Health Facilities vs. Conflicts Per Region ----
health_counts = health_gdf.groupby("Admin1").size().reset_index(name="Health_Facilities")
merged_df = pd.merge(region_conflicts, health_counts, left_on="admin1", right_on="Admin1", how="left").fillna(0)

plt.figure(figsize=(10, 6))
sns.regplot(data=merged_df, x="Health_Facilities", y="conflicts", scatter_kws={"s": 50, "color": "blue"}, line_kws={"color": "red"})
plt.title("Health Facilities vs. Conflict Events", fontsize=14)
plt.xlabel("Number of Health Facilities", fontsize=12)
plt.ylabel("Number of Conflicts", fontsize=12)
plt.grid(True)
plt.show()


##########################################################################################

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd

# ---- Load Conflict Data ----
conflict_data_path = r"\conflict_climate_health\ACLED\ACLED_Somalia_Fatalities.shp"
conflict_gdf = gpd.read_file(conflict_data_path)

# ---- Aggregate Conflict Counts Per Region ----
conflict_counts = conflict_gdf.groupby("admin1").size().reset_index(name="conflicts")
conflict_counts = conflict_counts.sort_values("conflicts", ascending=False)  # Sort for better visualization

# ---- Convert Data for Polar Plot ----
regions = conflict_counts["admin1"].tolist()
conflicts = conflict_counts["conflicts"].tolist()

angles = np.linspace(0, 2 * np.pi, len(regions), endpoint=False).tolist()
conflicts += conflicts[:1]  # Close the circle
angles += angles[:1]  # Close the circle

# ---- Create Polar Chart ----
sns.set_style("whitegrid")
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})

ax.plot(angles, conflicts, color='orange', linewidth=2)  # Line Plot
ax.fill(angles, conflicts, color='orange', alpha=0.3)  # Fill the area

# ---- Format Chart ----
ax.set_xticks(angles[:-1])  # Set region names at correct angles
ax.set_xticklabels(regions, fontsize=12, fontweight="bold", rotation=30, ha="right")
ax.set_yticklabels(["0", "10", "20", "30", "40", "50", "60"], fontsize=10)

plt.title("Conflict Events per Region in Somalia", fontsize=14, fontweight="bold")
plt.show()
