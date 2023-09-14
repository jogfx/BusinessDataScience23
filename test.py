import streamlit as st
import pandas as pd
import altair as alt

# Function to load the dataset
@st.cache  # Cache the function to enhance performance
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
scatter_plot = alt.Chart(filtered_df).mark_circle().encode(
    x=alt.X('created_year:O',
            axis=alt.Axis(format='d')),
    y='subscribers',
    tooltip=[
        alt.Tooltip('created_year:O', title='Started in'),
        alt.Tooltip('years_since_creation:Q', title='Age (years)'),
        'subscribers',
        'Youtuber'
    ]
).properties(
    width=600,
    height=400
).configure_mark(
    opacity=0.6
).interactive()

# Display the plot in Streamlit
st.title("YouTube Channel Analysis")
st.write("Scatter Plot showing the relationship between Year Created and Subscribers")

# Create a column layout for questions and answers
col1, col2 = st.columns(2)  # Adjust the column widths as needed

# Define the questions and answers
questions = [
    "1. Is there a noticeable trend in the scatterplot?",
    "2. What is the strength and direction of the correlation between creation year and subscribers?",
    "3. Are there any outliers in the data?",
    "4. How does the number of uploads relate to subscribers?",
    "5. What insights can we gather about the distribution of channels by channel type?"
]

answers = [
    "There appears to be a slight positive trend in the scatterplot, indicating that channels created more recently tend to have slightly higher subscribers.",
    f"The correlation coefficient between the year of creation and subscribers is approximately {correlation:.2f}, indicating a weak negative correlation.",
    "To answer this question, we can analyze the distribution of data points that fall significantly far from the general trend in the scatterplot.",
    "A deeper analysis of the relationship between the number of uploads and subscribers is required to provide insights.",
    "We can create a histogram or bar chart to visualize the distribution of channels by channel type."
]

# Loop through questions and answers
for i, question in enumerate(questions):
    expander = col1.expander(question)
    with expander:
        expander.write(answers[i])

# Display the scatter plot in the second column
col2.title("Scatter Plot")
col2.write("Scatter Plot showing the relationship between Year Created and Subscribers")
col2.altair_chart(scatter_plot)

# Display the correlation coefficient
col2.write(f"Correlation Coefficient between Year Created and Subscribers: {correlation:.2f}")