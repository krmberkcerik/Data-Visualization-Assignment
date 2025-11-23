import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import plotly.graph_objects as go

# Title
st.title("Netflix Data Analysis")

# Load the dataset
df = pd.read_csv('netflix_titles.csv')

df['title_length'] = df['title'].apply(lambda x: len(str(x).split()))

# Preprocess the data
df['date_added'] = pd.to_datetime(df['date_added'], format='mixed', errors='coerce')
df['year_added'] = df['date_added'].dt.year


# ----- Top 15 Countries Geographically -----
st.header("Top 15 Countries with The Most Content")

selected_type = st.radio(
    "Select content type for detailed analysis:",
    ("Movie", "TV Show"))

# Filter data for the currently selected type only (used for Map, Duration/Seasons, and Directors)
filtered_df = df[df['type'] == selected_type].copy()

# Split the 'country' column entries and count unique countries for the selected type
country_counts = filtered_df['country'].str.split(', ', expand=True).stack().value_counts().reset_index()
country_counts.columns = ['country', 'count']

# Select Top 15 countries and exclude 'Unknown' values
top_countries = country_counts[country_counts['country'] != 'Unknown'].head(15)

fig_map = px.choropleth(
    top_countries,
    locations='country',
    locationmode='country names',
    color='count',
    hover_name='country',
    color_continuous_scale=px.colors.sequential.Plasma,
    title=f'Source Country Distribution for {selected_type}' # Title reflects selected type
)
fig_map.update_layout(height=500, margin={"r":0,"t":50,"l":0,"b":0})
st.plotly_chart(fig_map, use_container_width=True)

st.markdown("""
**Insight:** This world map shows the countries with the highest content production (often dominated by the US and India) for the selected type.
""")

st.markdown("---")

# ----- Percentage of Movies vs TV Shows (Pie Chart) -----
st.header("Percentage of Movies vs TV Shows")
# Count the number of Movies and TV Shows
type_counts = df['type'].value_counts().reset_index()
type_counts.columns = ['type', 'count']

colors = ['#636EFA', '#00CC96']
fig_pie = px.pie(
    type_counts,
    names='type',
    values='count',
    hole=.3,
    color='type',
    color_discrete_sequence=colors
)
st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")

# ----- Titles per Year (Stacked Bar Chart) -----
st.header("Titles per Year")
# Count movies and tv shows per release year
counts = df.groupby(["release_year", "type"]).size().reset_index(name="count")

# Create stacked bar chart
chart = (
    alt.Chart(counts)
    .mark_bar()
    .encode(
        x=alt.X("release_year:O", title="Release Year"),
        y=alt.Y("count:Q", title="Number of Titles"),
        color=alt.Color("type:N", title="Type", scale=alt.Scale(domain=["Movie", "TV Show"], range=["orange", "blue"])),
        order=alt.Order("type", sort="ascending")
    )
    .properties(width="container", height=600)
)
st.altair_chart(chart, use_container_width=True)
"There is a clear increase in percentage of TV shows trend in recent years"

st.markdown("---")

# --- Content Rating Distribution (Bar Chart) ---
st.header("Top Content Rating Distribution")
# Count the occurrences of each rating
rating_counts = df['rating'].value_counts().reset_index()
rating_counts.columns = ['rating', 'count']

# Select the top 14 ratings instead of fixing the code
top_ratings = rating_counts.nlargest(14, 'count')

fig_rating = px.bar(
    top_ratings,
    x='rating',
    y='count',
    title='Top 14 Content Ratings by Count'
)
fig_rating.update_layout(xaxis={'categoryorder':'total descending'})
st.plotly_chart(fig_rating, use_container_width=True)

st.markdown("---")

# ----- Dynamic Chart: Movie Duration vs TV Show Seasons -----

selected_type_2 = st.radio(
    "Select content type for detailed analysis:",
    ("Movie", "TV Show"), key=2)

if selected_type_2 == 'Movie':
    st.header("Movie Duration vs. Release Year")
    # Filter for Movies (type = 'Movie') and remove null durations.
    movie_df = df[df['type'] == 'Movie'].dropna(subset=['duration'])
    
    # Extract duration in minutes for the plot
    movie_df['duration_minutes'] = movie_df['duration'].str.extract('(\d+)').astype(int)
    
    fig_scatter = px.scatter(
        movie_df,
        x='release_year',
        y='duration_minutes',
        color='duration_minutes',
        hover_data=['title', 'director'],
        title='Correlation Between Release Year and Movie Duration',
        labels={'release_year': 'Release Year', 'duration_minutes': 'Duration (Minutes)'},
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    
    st.plotly_chart(fig_scatter, use_container_width=True)
    st.markdown("---")
    
elif selected_type_2 == 'TV Show':
    # TV Show Season Count Distribution
    st.markdown("### TV Show Season Count Distribution (Bar Chart)")
    # Filter for TV Shows (type = 'TV Show')
    tv_df = df[df['type'] == 'TV Show'].dropna(subset=['duration'])
    
    # Extract season count
    tv_df['seasons'] = tv_df['duration'].str.extract('(\d+)').astype(int)
    
    season_counts = tv_df['seasons'].value_counts().reset_index()
    season_counts.columns = ['Season Count', 'count']
    
    fig_seasons = px.bar(
        season_counts.sort_values(by='Season Count'),
        x='Season Count',
        y='count',
        color='Season Count',
        title='Distribution of TV Shows by Season Count',
        labels={'count': 'Number of TV Shows'}
    )
    st.plotly_chart(fig_seasons, use_container_width=True)
    st.markdown("---")

# ----- Top Directors Horizontal Bar Chart -----
st.header(f"Top 10 Movie Directors")


# Split the 'director' column entries and count unique directors
director_counts = df['director'].str.split(', ', expand=True).stack().value_counts().reset_index()
director_counts.columns = ['Director', 'count']

# Select top 10 directors
top_directors = director_counts[director_counts['Director'] != 'Unknown'].head(10)

fig_director = px.bar(
    top_directors,
    x='count',
    y='Director',
    orientation='h',
    title=f'Favorite Directors of Netflix',
    labels={'Director': 'Director', 'count': 'Content Count'}
)
fig_director.update_traces(marker_color='#2ca02c') 

# y axis sorting
fig_director.update_layout(
    yaxis={'categoryorder':'total ascending'},
    showlegend=False
)
st.plotly_chart(fig_director, use_container_width=True)

st.markdown("---")

# ----- Country and Genre Relation Heatmap -----
st.header("Top Country and Genre Relation")

selected_type_3 = st.radio(
    "Select content type for detailed analysis:",
    ("Movie", "TV Show"), key=3)

filtered_df_3 = df[df['type'] == selected_type_3].copy()

# 1. Explode 'country' and 'listed_in' columns
country_genre = filtered_df_3.assign(country=filtered_df_3['country'].str.split(', ')).explode('country')
country_genre = country_genre.assign(genre=country_genre['listed_in'].str.split(', ')).explode('genre')

# 2. Identify Top 10 countries and genres
top_n_countries = country_genre['country'].value_counts().head(10).index
top_m_genres = country_genre['genre'].value_counts().head(10).index

# 3. Filter data to include only the top categories
heatmap_data = country_genre[
    (country_genre['country'] != 'Unknown') & 
    (country_genre['country'].isin(top_n_countries)) &
    (country_genre['genre'].isin(top_m_genres))
]

# 4. Create the pivot table (matrix) for the heatmap
heatmap_pivot = heatmap_data.pivot_table(index='country', columns='genre', aggfunc='size', fill_value=0)

# 5. Create the Plotly Heatmap
fig_heatmap = px.imshow(
    heatmap_pivot,
    text_auto=False,
    aspect="auto",
    color_continuous_scale="Aggrnyl_r", 
    title=f'Top 10 Country and Genre Relation for {selected_type_3}'
)
st.plotly_chart(fig_heatmap, use_container_width=True)
st.markdown("---")


# ----- Content Added By Year Area Chart -----
st.header("Content Added To Netflix By Year")

# Recalculate yearly_added data, dropping rows where date parsing failed (NaN year)
yearly_added = df.groupby(['year_added', 'type']).size().reset_index(name='count').dropna()

fig_area = px.area(
    yearly_added,
    x='year_added',
    y='count',
    color='type',
    line_group='type',
    title='Content Added To Netflix By Year',
    labels={'year_added': 'Year Added', 'count': 'Number of Content Added'},
    markers=True
)
fig_area.update_xaxes(tick0=2008, dtick=1)
st.plotly_chart(fig_area, use_container_width=True)
st.markdown("---")


# ----- Distribution of Title Lengths Violin Plot ------

st.header(" Distribution of Title Lengths by Age Restriction")


# 1. Data Preparation:
# Filter the dataframe for valid ratings do not select top 14
valid_ratings = ['TV-MA', 'R', 'PG-13', 'TV-14', 'TV-PG', 'NR', 'PG', 'G', 'TV-G', 'TV-Y7', 'TV-Y', 'NC-17', 'TV-Y7-FV']
plot_df_all = df[df['rating'].isin(valid_ratings)].copy()

# 2. Visualization:
fig_violin_all = px.violin(
    plot_df_all, 
    y="title_length", 
    x="rating", 
    color="rating", 
    box=True,
    points="all",
    hover_data=['title'],
    title="Distribution of Title Lengths Across All Content by Age Restriction",
    labels={'title_length': 'Title Length (By Words)', 'rating': 'Age Restriction'}
)

# 3. Customization: Remove legend and set explicit x-axis order
fig_violin_all.update_layout(
    showlegend=False,
    xaxis={'categoryorder':'array', 'categoryarray': valid_ratings} # Keeps the axis order organized
)
st.plotly_chart(fig_violin_all, use_container_width=True)
st.markdown("---")