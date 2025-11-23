# Data-Visualization-Assignment
Los Amigos / Netflix Movies And Tv Shows Streamlit Project
# Netflix Content Analysis Dashboard

## Project Description
[cite_start]This project is an interactive data visualization dashboard developed for the CEN445 Introduction to Data Visualization course[cite: 1]. [cite_start]The goal is to explore and visualize the Netflix Movies and TV Shows dataset using Python and Streamlit, providing meaningful insights through a variety of visualization techniques, including advanced methods[cite: 3, 4, 11, 12].

## Dataset Details
[cite_start]The dataset used in this project is the "Netflix Movies and TV Shows" dataset sourced from Kaggle[cite: 7]. It contains information about movies and TV shows available on Netflix as of 2021.

- **Dataset:** Netflix Movies and TV Shows
- **Source:** [Kaggle](https://www.kaggle.com/datasets/shivamb/netflix-shows)
- [cite_start]**Size:** 8807 rows, 12 columns [cite: 6]
- **Key Columns:**
    - `type`: Identifier for Movie or TV Show.
    - `title`: Title of the content.
    - `director`: Director(s) of the content.
    - `cast`: Actors involved in the content.
    - `country`: Country or countries where the content was produced.
    - `date_added`: Date the content was added to Netflix.
    - `release_year`: Original release year of the content.
    - `rating`: Content rating (e.g., TV-MA, PG-13).
    - `duration`: Duration of the content (in minutes for movies, seasons for TV shows).
    - `listed_in`: Genres the content falls under.
    - `description`: A brief summary of the content.

## Data Preprocessing
[cite_start]Before visualization, the raw dataset was cleaned and preprocessed to handle missing values and format data for analysis[cite: 8, 9].

Key preprocessing steps performed in `app.py`:
1.  **Handling Missing Values:** Missing values in `country`, `director`, and `cast` columns were filled with the placeholder 'Unknown'.
2.  **Date Formatting:** The `date_added` column was converted to datetime objects, and a new `year_added` column was extracted.
3.  **Duration Parsing:** The `duration` column was parsed to create two new numerical columns: `movie_duration_clean` (in minutes) for movies and `seasons_clean` (number of seasons) for TV shows.
4.  **Data Cleaning:** Rows with missing values in crucial columns like `rating`, `year_added`, or the cleaned duration columns were dropped to ensure data integrity for visualization.

## Installation and Setup Instructions
To run this project locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Install the required libraries:**
    Ensure you have Python installed. It is recommended to use a virtual environment. Install the dependencies using pip:
    ```bash
    pip install streamlit pandas plotly numpy
    ```

3.  **Run the Streamlit application:**
    Navigate to the project directory and execute the following command:
    ```bash
    streamlit run app.py
    ```
    [cite_start]The dashboard will open automatically in your default web browser[cite: 23].

## Project Structure
- [cite_start]`app.py`: The main Python script containing the Streamlit application code, data preprocessing logic, and visualization implementations[cite: 23].
- [cite_start]`netflix_titles.csv`: The dataset file used for the analysis[cite: 23].
- [cite_start]`README.md`: This file, providing an overview of the project, dataset, and setup instructions[cite: 23].

## Features and Visualizations
[cite_start]The dashboard includes a sidebar for interactivity, allowing users to filter the data based on content type, year added to Netflix, and content rating[cite: 14].

[cite_start]The dashboard presents a total of 9 visualizations, including 6 advanced and 3 simple types[cite: 11, 17]:

**Advanced Visualizations:**
1.  **Choropleth Map:** Distribution of content by country.
2.  **Treemap:** Hierarchical view of content genres.
3.  **Violin Plot:** Distribution of title lengths by rating.
4.  **Area Chart:** Cumulative content added over time.
5.  **Scatter Plot:** Relationship between content duration/seasons and release year.
6.  **Heatmap:** Relationship between top countries and top genres.

**Simple Visualizations:**
7.  **Bar Chart (Horizontal):** Top 10 directors by content count.
8.  **Bar Chart (Vertical):** Distribution of content ratings.
9.  **Pie Chart:** Proportion of Movies vs. TV Shows.

[cite_start]Each visualization is designed to provide unique insights and includes interactive features such as hover effects and zooming[cite: 12, 13].

