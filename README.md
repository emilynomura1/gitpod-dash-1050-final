# Data Science Web Application Project - NFL Weather Data

## Introduction
This project is for the [Brown University Data Science](https://www.brown.edu/initiatives/data-science/masters-degree) Master's course, DATA 1050 - Data Engineering. The purpose of the project is to develop a database-backed website that provides the results of a particular data science project.

The online data source we use is [nflweather.com](https://www.nflweather.com/en/). It is incrementally updated throughout the day, and provides a list of NFL games that are going to played in a week. The teams playing, weather forecast, and wind speed is provided. When a game is completed, the final score is uploaded to the website. All 18 weeks of the NFL season are included on the website, but the homepage url will navigate the user to the current week. Historical data from the website can be found in the [analytics tab](https://www.nflweather.com/en/archive), which provides links to data from 2009-2020.

The historical data in our database is from a publicly-available NFL weather project that compiled data from NFL games and merged this with weather data. The raw historical data we use can be downloaded [here](https://raw.githubusercontent.com/Nolanole/NFL-Weather-Project/master/all_games_weather.csv). Credit goes to [Josh Mancuso](https://github.com/Nolanole) for this data.

We use Supabase for the backend of this project. Particularly, to house the historical database and to build the new database with data from [nflweather.com](https://www.nflweather.com/en/). Plotly dash was used to create the front-end web application.

## Technologies Used
- Python version [3.8.12](https://docs.python.org/release/3.8.12/)
- [Plotly Dash](https://dash.plotly.com/)
- [Supabase](https://supabase.com/docs)
