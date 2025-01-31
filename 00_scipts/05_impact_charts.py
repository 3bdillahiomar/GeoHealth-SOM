# In this script, we will create a bar chart to visualize the number of conflict events and fatalities per year.

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define file path
conflict_data_path = r"\conflict_climate_health\ACLED\ACLED_Somalia_Fatalities.shp"

# Load the conflict dataset
gdf = gpd.read_file(conflict_data_path)

# Ensure the 'year' column exists
if "year" not in gdf.columns:
    raise ValueError("The dataset does not contain a 'year' column.")

# Count conflicts per year
conflict_counts = gdf["year"].value_counts().sort_index()

# Convert to DataFrame for plotting
df_conflicts = pd.DataFrame({"Year": conflict_counts.index, "Count": conflict_counts.values})

# --- 📌 Plot the Bar Chart ---
plt.figure(figsize=(12, 6))
sns.barplot(data=df_conflicts, x="Year", y="Count", color="skyblue")

# Formatting
plt.xticks(rotation=45, ha="right")
plt.xlabel("Year", fontsize=12)
plt.ylabel("Count", fontsize=12)
plt.title("Number of Conflicts per Year", fontsize=14, fontweight="bold")

# Custom grid styling
plt.grid(True, linestyle="--", linewidth=0.7, color="purple", alpha=0.3)

plt.show()

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define file path for EMDAT data
emdat_data_path = r"\conflict_climate_health\conflict_data\emdat.csv"

# Load EMDAT dataset
df_emdat = pd.read_csv(emdat_data_path)

# Ensure the 'DisNo.' column exists
if "DisNo." not in df_emdat.columns:
    raise ValueError("The dataset does not contain a 'DisNo.' column.")

# Extract the year (first 4 characters) from 'DisNo.'
df_emdat["Year"] = df_emdat["DisNo."].astype(str).str[:4].astype(int)

# Count disasters per year
disaster_counts = df_emdat["Year"].value_counts().sort_index()

# Convert to DataFrame for plotting
df_disasters = pd.DataFrame({"Year": disaster_counts.index, "Count": disaster_counts.values})

# --- 📌 Plot the Bar Chart ---
plt.figure(figsize=(12, 6))
sns.barplot(data=df_disasters, x="Year", y="Count", color="lightcoral", alpha=0.7)

# Formatting
plt.xticks(rotation=45, ha="right")
plt.xlabel("Year", fontsize=12)
plt.ylabel("Number of Disasters", fontsize=12)
plt.title("Number of Disasters per Year (EMDAT - Somalia)", fontsize=14, fontweight="bold")

# Custom grid styling
plt.grid(True, linestyle="--", linewidth=0.7, color="purple", alpha=0.3)

plt.show()



#########################################################################################################################################

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import plotly.express as px

# Define file path for EMDAT data
emdat_data_path = r"\conflict_climate_health\conflict_data\emdat.csv"

# Load EMDAT dataset
df_emdat = pd.read_csv(emdat_data_path)

# Ensure required columns exist
required_columns = ["DisNo.", "Disaster Type"]
for col in required_columns:
    if col not in df_emdat.columns:
        raise ValueError(f"Missing column: {col} in the dataset.")

# Extract the year (first 4 characters) from 'DisNo.'
df_emdat["Year"] = df_emdat["DisNo."].astype(str).str[:4].astype(int)

# Count occurrences of each disaster type per year
disaster_trend = df_emdat.groupby(["Year", "Disaster Type"]).size().reset_index(name="Count")

# --- 📌 1. Heatmap: Disaster Frequency Over Time ---
plt.figure(figsize=(12, 6))
heatmap_data = disaster_trend.pivot(index="Disaster Type", columns="Year", values="Count").fillna(0)
sns.heatmap(heatmap_data, cmap="coolwarm", linewidths=0.5, annot=True, fmt=".0f")

plt.title("Disaster Frequency Over Time (Heatmap)", fontsize=14, fontweight="bold")
plt.xlabel("Year")
plt.ylabel("Disaster Type")
plt.show()

# --- 📌 2. Line Chart with Trend ---
plt.figure(figsize=(12, 6))
sns.lineplot(data=disaster_trend, x="Year", y="Count", hue="Disaster Type", marker="o")

plt.title("Disaster Trends Over Time (Line Chart)", fontsize=14, fontweight="bold")
plt.xlabel("Year")
plt.ylabel("Number of Disasters")
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend(title="Disaster Type", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.show()

# --- 📌 3. Stacked Area Chart ---
plt.figure(figsize=(12, 6))
disaster_trend_pivot = disaster_trend.pivot(index="Year", columns="Disaster Type", values="Count").fillna(0)
disaster_trend_pivot.plot.area(alpha=0.6, colormap="tab10")

plt.title("Disaster Type Distribution Over Time (Stacked Area Chart)", fontsize=14, fontweight="bold")
plt.xlabel("Year")
plt.ylabel("Number of Disasters")
plt.grid(True, linestyle="--", alpha=0.5)
plt.show()

# --- 📌 4. Word Cloud: Most Common Disaster Types ---
plt.figure(figsize=(8, 6))
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(" ".join(df_emdat["Disaster Type"]))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Most Common Disaster Types (Word Cloud)", fontsize=14, fontweight="bold")
plt.show()

# --- 📌 5. Sankey Diagram: Disaster Flow Analysis ---
fig = px.sankey(
    disaster_trend, 
    node=dict(label=list(disaster_trend["Disaster Type"].unique()) + list(disaster_trend["Year"].astype(str).unique())),
    link=dict(
        source=[list(disaster_trend["Disaster Type"].unique()).index(x) for x in disaster_trend["Disaster Type"]],
        target=[len(disaster_trend["Disaster Type"].unique()) + list(disaster_trend["Year"].astype(str).unique()).index(str(y)) for y in disaster_trend["Year"]],
        value=disaster_trend["Count"]
    )
)
fig.update_layout(title_text="Disaster Type Flow Over Time (Sankey Diagram)")
fig.show()


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define file path for EMDAT data
emdat_data_path = r"\conflict_climate_health\conflict_data\emdat.csv"

# Load EMDAT dataset
df_emdat = pd.read_csv(emdat_data_path)

# Ensure the 'Disaster Type' column exists
if "Disaster Type" not in df_emdat.columns:
    raise ValueError("The dataset does not contain a 'Disaster Type' column.")

# Count occurrences of each disaster type
disaster_counts = df_emdat["Disaster Type"].value_counts()

# Convert to DataFrame for visualization
df_disasters = pd.DataFrame({"Disaster Type": disaster_counts.index, "Count": disaster_counts.values})

# --- 📌 Improved Bar Chart: Disaster Types ---
plt.figure(figsize=(12, 7))
sns.barplot(data=df_disasters, x="Count", y="Disaster Type", palette="coolwarm", edgecolor="black")

# Formatting
plt.xlabel("Number of Disasters", fontsize=13, fontweight="bold")
plt.ylabel("Disaster Type", fontsize=13, fontweight="bold")
plt.title("Disaster Types in Somalia (EMDAT Data)", fontsize=15, fontweight="bold")
plt.grid(axis="x", linestyle="--", alpha=0.5)

# Show values on bars
for index, value in enumerate(df_disasters["Count"]):
    plt.text(value + 0.5, index, str(value), va="center", fontsize=12, fontweight="bold")

plt.show()


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define file path for EMDAT data
emdat_data_path = r"\conflict_climate_health\conflict_data\emdat.csv"

# Load EMDAT dataset
df_emdat = pd.read_csv(emdat_data_path)

# Ensure the 'Disaster Type' column exists
if "Disaster Type" not in df_emdat.columns:
    raise ValueError("The dataset does not contain a 'Disaster Type' column.")

# Count occurrences of each disaster type
disaster_counts = df_emdat["Disaster Type"].value_counts()

# Convert to DataFrame for visualization
df_disasters = pd.DataFrame({"Disaster Type": disaster_counts.index, "Count": disaster_counts.values})

# --- 📌 Improved Bar Chart: Disaster Types (Using Qualitative Colors) ---
plt.figure(figsize=(12, 7))

# Use a qualitative color palette (Set2, Dark2, or Paired)
sns.barplot(data=df_disasters, x="Count", y="Disaster Type", palette="Set2", edgecolor="black")

# Formatting
plt.xlabel("Number of Disasters", fontsize=13, fontweight="bold")
plt.ylabel("Disaster Records", fontsize=13, fontweight="bold")
plt.title("Disaster Types in Somalia (EMDAT Database)", fontsize=15, fontweight="bold")
plt.grid(axis="x", linestyle="--", alpha=0.5)

# Show values on bars
for index, value in enumerate(df_disasters["Count"]):
    plt.text(value + 0.5, index, str(value), va="center", fontsize=12, fontweight="bold")

plt.show()


