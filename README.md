# Data Science Web Application Project - NFL Weather Data

## Introduction
This project is for the [Brown University Data Science](https://www.brown.edu/initiatives/data-science/masters-degree) Master's course, DATA 1050 - Data Engineering. The purpose of the project is to develop a database-backed website that provides the results of a particular data science project.

The online data source we use is [nflweather.com](https://www.nflweather.com/en/). It is incrementally updated throughout the day, and provides a list of NFL games that are going to be played in a week. The teams playing, weather forecast, and wind speed is provided. When a game is completed, the final score is uploaded to the website. All 18 weeks of the NFL season are included on the website, but the homepage url will navigate the user to the current week. The historical data in our database is from a publicly-available NFL weather project that compiled data from NFL games and merged it with weather data. The raw historical data can be downloaded [here](https://raw.githubusercontent.com/Nolanole/NFL-Weather-Project/master/all_games_weather.csv). Credit goes to [Josh Mancuso](https://github.com/Nolanole) for this data.

We used Supabase for the backend of this project. Particularly, to house the historical database and to build the new database for the current NFL season. We cleaned the historical data in a Jupyter notebook and uploaded it to Supabase. A new database is populated when the web application is run. We extract data from the current week. Only completed games with final scores are added to the new database. A unique event ID is created using the year, week number, home team, and away team. Before the data is appended to populate the new database, we check if the unique ID is already present in the database to avoid duplicate entries when the app is run multiple times in the same week rather than just at the end of the week.

Plotly Dash was used to create the front-end web application. A dropdown box requires the user to select a particular NFL team. Information about that team’s game is displayed according to certain elements about the game:
- If the game has already been played
- If the game is being played in a dome
- If the game has not been played yet
If the game has not been played yet, the percentage of games the team has won in similar weather conditions is displayed along with a filtered table of the most recent games in the historical database played by the same team in similar weather conditions. This last aspect of the web application summarizes the historical data in a new and interesting way according to user input and information extracted from current weather data. 

## Technologies Used
- Python version [3.8.12](https://docs.python.org/release/3.8.12/)
- [Plotly Dash](https://dash.plotly.com/)
- [Supabase](https://supabase.com/docs)
