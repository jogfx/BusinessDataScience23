import streamlit as st
import pandas as pd
import geopandas as gpd
import numpy as np
import seaborn as sns
import altair as alt
import matplotlib.pyplot as plt
from shapely import Point
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

# Function to load the dataset
@st.cache_data  # Cache the function to enhance performance
def load_data():
    # Define the file path
    file_path = 'https://raw.githubusercontent.com/jogfx/BusinessDataScience23/main/global_youtube_data_2023.csv'
    
    # Load the CSV file into a pandas dataframe
    df = pd.read_csv(file_path)

    # Drop irrelevant columns
    df = df[['Title', 'Youtuber', 'subscribers', 'video views', 'uploads', 'channel_type', 'created_year', 'lowest_monthly_earnings', 'highest_monthly_earnings', 'Country', 'Longitude', 'Latitude']]

    # Handling missing values
    median_year = df['created_year'].median()
    df['created_year'].fillna(median_year, inplace=True)

    type_mode = df['channel_type'].mode()[0]
    df['channel_type'].fillna(type_mode, inplace=True)

    country_mode = df['Country'].mode()[0]
    df['Country'].fillna(country_mode, inplace=True)

    longitude_mode = df['Longitude'].mode()[0]
    df['Longitude'].fillna(longitude_mode, inplace=True)

    latitude_mode = df['Latitude'].mode()[0]
    df['Latitude'].fillna(latitude_mode, inplace=True)

    return df

# Load the data using the defined function
df = load_data()

# Suppress the warning
pd.options.mode.chained_assignment = None

# Filter the DataFrame to include data from 2000 to 2023
filtered_df = df[(df['created_year'] >= 2000) & (df['created_year'] <= 2023)]

# Calculate correlation for the filtered data
correlation = filtered_df['created_year'].corr(filtered_df['subscribers'])

# Calculate years since channel was created
current_year = 2023  # You can adjust this to the current year
filtered_df['years_since_creation'] = current_year - filtered_df['created_year']

# Create a scatter plot using Altair with customized tooltips, interactivity, and formatted x-axis
base_chart = alt.Chart(filtered_df).mark_circle(size=80, color='blue').encode(
    x=alt.X('created_year:O',
            axis=alt.Axis(title='Started in', format='d', labelAngle=0)),
    y=alt.Y('subscribers:Q',
            axis=alt.Axis(title='Subscribers', format=',s')),
    tooltip=[
        alt.Tooltip('created_year:O', title='Started in'),
        alt.Tooltip('years_since_creation:Q', title='Age (years)', format='.0f'),
        alt.Tooltip('subscribers:Q', title='Subscribers', format=','),
        'Youtuber'
    ]
)

# Create a selection for highlighting points on click
selection = alt.selection_single(on='click', empty='all', nearest=True, fields=['created_year'])

# Apply selection to the base chart
selected_chart = base_chart.add_selection(selection)

# Create a chart for comparing selected points
comparison_chart = base_chart.transform_filter(selection).mark_circle(
    color='red',
    size=120,
    opacity=0.7
)

# Combine the charts and configure interactivity
scatter_plot = (selected_chart | comparison_chart).resolve_scale(color='independent')

# Display the plot in Streamlit
st.title("YouTube Channel Analysis")
st.write("Scatter Plot showing the relationship between Year Created and Subscribers")

# Create a Streamlit container for the side table
selected_data = st.container()

# Display the correlation coefficient
st.write(f"Correlation Coefficient between Year Created and Subscribers: {correlation:.2f}")

# Create a dynamic table to show selected data
with selected_data:
    st.write("Selected Data:")
    nearest = selection['nearest']
    selected_year = nearest['nearest']['created_year'] if nearest else None
    
    if selected_year is not None:
        selected_points = filtered_df[filtered_df['created_year'] == selected_year].reset_index(drop=True)
        st.table(selected_points[['Youtuber', 'created_year', 'years_since_creation', 'subscribers']])

# Display the scatter plot
st.altair_chart(scatter_plot)
