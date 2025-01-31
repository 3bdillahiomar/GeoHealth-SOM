# In this script, we will create a bar chart to visualize the number of conflict events and fatalities per region.

import geopandas as gpd
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Load the shapefile
file_path = r"\conflict_climate_health\conflict_data\total_fatalities\Somalia_Regions_with_Events.shp"
data = gpd.read_file(file_path)

# Convert GeoDataFrame to DataFrame
df = pd.DataFrame(data)

# Verify the data contains the necessary columns
print(df.columns)  # This line helps you verify the column names

# Create separate bar charts for events and fatalities
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16, 6))

# Plot for conflict events
sns.barplot(ax=axes[0], data=df, x='admin1', y='event_coun', color='blue')
axes[0].set_title('Number of Conflict Events per Region')
axes[0].set_xlabel('Region')
axes[0].set_ylabel('Event Count')
axes[0].tick_params(axis='x', rotation=45)

# Plot for fatalities
sns.barplot(ax=axes[1], data=df, x='admin1', y='fatalities', color='red')
axes[1].set_title('Number of Fatalities per Region')
axes[1].set_xlabel('Region')
axes[1].set_ylabel('Fatalities Count')
axes[1].tick_params(axis='x', rotation=45)

# Improve layout
plt.tight_layout()
plt.show()

# Stacked Bar Chart with Proportional Representation

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import geopandas as gpd

# Load and prepare data
file_path = file_path
data = gpd.read_file(file_path)
df = pd.DataFrame(data)

# Create a new column for non-fatal events
df['non_fatal_events'] = df['event_coun'] - df['fatalities']

# Plotting
fig, ax = plt.subplots(figsize=(12, 6))
df[['non_fatal_events', 'fatalities']].set_index(df['admin1']).plot(kind='bar', stacked=True, ax=ax, color=['skyblue', 'red'])
ax.set_title('Proportional Representation of Conflict Events and Fatalities per Region')
ax.set_xlabel('Region')
ax.set_ylabel('Count')
plt.xticks(rotation=45)
plt.legend(['Non-Fatal Events', 'Fatalities'])
plt.tight_layout()
plt.show()

import plotly.express as px
import pandas as pd
import geopandas as gpd

# Load and prepare data
file_path = file_path
data = gpd.read_file(file_path)
df = pd.DataFrame(data)

# Creating the bubble chart
fig = px.scatter(df, x="admin1", y="event_coun", size="fatalities", color="admin1",
                 hover_name="admin1", size_max=60, title="Interactive Bubble Chart of Events and Fatalities")
fig.update_layout(xaxis_title="Region", yaxis_title="Number of Events")
fig.show()


import geopandas as gpd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the shapefile
file_path = r"\conflict_climate_health\conflict_data\total_fatalities\Somalia_Regions_with_Events.shp"
data = gpd.read_file(file_path)

# Prepare the data for Seaborn
# Use 'admin1' for region names, 'event_coun' for event counts, and 'fatalities' for fatality counts
data_melted = data.melt(id_vars=['admin1'], value_vars=['event_coun', 'fatalities'], var_name='Type', value_name='Count')

# Create the plot with seaborn for a horizontal layout
plt.figure(figsize=(12, 6))
ax = sns.barplot(data=data_melted, y='admin1', x='Count', hue='Type', palette=['#3498db', '#e74c3c'])

# Add labels and title
plt.ylabel('Region')  # Label for y-axis
plt.xlabel('Count')  # Label for x-axis
plt.title('Proportional Representation of Conflict Events and Fatalities per Region')

# Display the plot
plt.tight_layout()
plt.show()


################################################################################################################################
import geopandas as gpd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the shapefile
file_path = r"\conflict_climate_health\conflict_data\total_fatalities\Somalia_Regions_with_Events.shp"
data = gpd.read_file(file_path)

# Prepare the data for Seaborn with custom legend labels
# Rename the columns in the DataFrame to have more descriptive labels
data.rename(columns={'event_coun': 'Number of Events', 'fatalities': 'Fatalities'}, inplace=True)

# Melt the DataFrame with new legend names
data_melted = data.melt(id_vars=['admin1'], value_vars=['Number of Events', 'Fatalities'], var_name='Type', value_name='Count')

# Create the plot with seaborn for a horizontal layout
plt.figure(figsize=(12, 6))
ax = sns.barplot(data=data_melted, y='admin1', x='Count', hue='Type', palette=['#3498db', '#e74c3c'])

# Add labels and title
plt.ylabel('Region')  # Label for y-axis
plt.xlabel('Count')  # Label for x-axis
plt.title('Proportional Representation of Conflict Events and Fatalities per Region')

# Optionally, you can modify the legend directly if needed:
# ax.legend(title='Event Type')

# Display the plot
plt.tight_layout()
plt.show()


import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# Sample data generation (replace this with your actual data loading method)
data = pd.DataFrame({
    'bill_length_mm': np.random.normal(loc=45, scale=5, size=150),
    'bill_depth_mm': np.random.normal(loc=18, scale=3, size=150),
    'flipper_length_mm': np.random.normal(loc=200, scale=12, size=150),
    'body_mass_g': np.random.normal(loc=4500, scale=800, size=150),
    'species': np.random.choice(['Adelie', 'Chinstrap', 'Gentoo'], 150)
})

# Create the pairplot
g = sns.pairplot(data, hue='species', kind='scatter', diag_kind='kde',
                 plot_kws={'alpha': 0.6, 's': 80, 'edgecolor': 'k'},
                 diag_kws={'shade': True})

# Adjust the style and aesthetics
g.fig.suptitle('Comparison of Physical Traits by Penguin Species', y=1.02)
plt.show()


