import dash
from dash import dcc # dash core components
from dash import dash_table
from dash import html
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output, State
import os
from supabase import create_client, Client
import requests
from bs4 import BeautifulSoup
import datetime
import plotly.express as px


# connection to db
url = "https://umydpehqhuatmhhyntgv.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYW5vbiIsImlhdCI6MTYzOTA3NzkyNywiZXhwIjoxOTU0NjUzOTI3fQ.jwZqMtdCVOWqhc73uaxYomYvF6lbxxTLcWIQp4gSFoY"
supabase: Client = create_client(url, key)

# get historical data
data = supabase.table('historical_data').select('*').execute()
historical = pd.DataFrame(data.get("data", []))
test = pd.DataFrame()
historical.avg_wind= pd.to_numeric(historical.avg_wind)
historical.precipitation= historical.precipitation.astype(int)

#reading in website data
df = pd.read_html("http://www.nflweather.com/")[0]

# fill na's and add a timestamp 
df = df.fillna(0)
df['date_pulled'] = str(datetime.datetime.now())

# convert to dict, nsert to raw_data db
dfd = df.to_dict('records')
supabase.table('raw_data').insert(dfd).execute()
assert data.get("status_code") in (200, 201)

# clean data
df = df[['Away', 'Home','Time (ET)','TV', 'Forecast', "Extended Forecast",'Wind']]
response = requests.get("http://www.nflweather.com/")
soup = BeautifulSoup(response.content, "html.parser")
header = soup.find_all('h1')
week = str(header[1])
current_week = week.split("\n")[1].strip(" ").strip(" Forecast")
df['unique_event_id'] = str(datetime.date.today().year)+"-"+current_week+ "-" + df['Home'] + "-" + df['Away']
df[['Temp','Weather_Forecast']]=df.Forecast.str.split("f",expand=True)
df[['WindSpeed','toDrop']]=df.Wind.str.split("m",expand=True)
df['Precipitation'] = np.where(((df.Weather_Forecast.str.find("Rain") == 1) | (df.Weather_Forecast.str.find("Snow")== 1)), 1, 0)
df = df[['unique_event_id','Away','Home','Time (ET)','Temp','Weather_Forecast' ,'WindSpeed','Precipitation']]

finished = df[df['Time (ET)'].str.contains('Final')]
future = df[~(df['Time (ET)'].str.contains('Final'))]

# get the processed data, load into df
data = supabase.table('processed_data').select('*').execute()
processed = pd.DataFrame(data.get("data", []))

rows_to_add = []

# iterate through rows
for index, row in finished.iterrows():
    
    # check if processed is empty
    if len(processed) == 0:
        rowd = row.to_dict()
        rows_to_add.append(rowd)
    
    # if unique event id already in processed, continue
    elif row['unique_event_id'] in processed['unique_event_id'].unique():
        continue
    
    # else, add the row to list of rows to append
    else:
        rowd = row.to_dict()
        rows_to_add.append(rowd)
        
# insert to db
supabase.table('processed_data').insert(rows_to_add).execute()
assert data.get("status_code") in (200, 201)

app = dash.Dash(__name__)

app.layout = html.Div([
    
    html.Div(
        className="app-header",
        children=[
            html.Div('NFL Weather Data', className="app-header--title")
        ]
    ),
    html.Img(src='/assets/nfl logo.jpg', width="150", height="250", className="center",style={"padding": "10px"}),
    
    html.Div(id='intro',style={"padding": "10px",'fontSize':14}, children = "Welcome to our NFL Weather Data app. This app looks at how each team does in the forecasted weather conditions for their next game, based on data from the 2010-2017 seasons. "),
    html.Div(children=[    
    html.Label("Select your team: "),
    dcc.Dropdown(
        
        id = 'my_dropdown1',
        options= [
    {"label": "Arizona Cardinals", "value": 'Cardinals'},
    {"label": "Atlanta Falcons", "value": 'Falcons'},
    {"label": "Baltimore Ravens", "value": "Ravens"},
    {"label": "Buffalo Bills", "value": "Bills"},
    {"label": "Carolina Panthers", "value": "Panthers"},
    {"label": "Chicago Bears", "value": "Bears"},
    {"label": "Cinncinati Bengals", "value": "Bengals"},
    {"label": "Cleveland Browns", "value": "Browns"},
    {"label": "Dallas Cowboys", "value": "Cowboys"},
    {"label": "Denver Broncos", "value": "Broncos"},
    {"label": "Detroit Lions", "value": "Lions"},
    {"label": "Green Bay Packers", "value": "Packers"},
    {"label": "Houston Texans", "value": "Texans"},
    {"label": "Indianapolis Colts", "value": "Colts"},
    {"label": "Jacksonville Jaguars", "value": "Jaguars"},
    {"label": "Kansas City Chiefs", "value": "Chiefs"},
    {"label": "Las Vegas Raiders", "value": "Raiders"},
    {"label": "Los Angeles Chargers", "value": "Chargers"},
    {"label": "Los Angeles Rams", "value": "Rams"},
    {"label": "Miami Dolphins", "value": "Dolphins"},
    {"label": "Minnesota Vikings", "value": "Vikings"},
    {"label": "New England Patriots", "value": "Patriots"},
    {"label": "New Orleans Saints", "value": "Saints"},
    {"label": "New York Giants", "value": "Giants"},
    {"label": "New York Jets", "value": "Jets"},
    {"label": "Philadelphia Eagles", "value": "Eagles"},
    {"label": "Pittsburgh Steelers", "value": "Steelers"},
    {"label": "San Francisco 49ers", "value": "49ers"},
    {"label": "Seattle Seahawks", "value": "Seahawks"},
    {"label": "Tampa Bay Buccaneers", "value": "Buccaneers"},
    {"label": "Tennessee Titans", "value": "Titans"},
    {"label": "Washington Football Team", "value": "Washington"},
            ],
            value='Select a team'
        ),
        html.Label(id='my_label1',style={"margin-bottom": "20px"}),
    html.Button(
            id='submit-button',
            n_clicks=0,
            children='Submit',
            style={'fontSize':16},
            
        ),       
    
    ], className="center"),
    html.Div(id='result',style={"padding": "10px"}),
    
    html.Div([
        dash_table.DataTable(
            id='table',
            columns=[{"name": str(i), "id": str(i)} for i in test.columns],
            data=test.to_dict('records')
        )
    ]),

    html.Div([

		], id="bar-chart")
])



@app.callback(
    [Output('result', 'children'),
    Output(component_id='table', component_property='columns'),
    Output(component_id='table', component_property='data'),
    Output(component_id='bar-chart', component_property='children')],
    Input(component_id='submit-button', component_property='n_clicks'),
    State(component_id='my_dropdown1', component_property='value'),
    State(component_id='bar-chart', component_property='children')
 
)

def pickATeam(n_clicks, input_my_dropdown1, bar_chart):
    if (n_clicks == 0):
        test = pd.DataFrame()
        stringret = "Please select a team."
        #dispret = {'display': 'none'}
        table_cols = [{"name": str(i), "id": str(i)} for i in test.columns]
        table_records = test.to_dict('records')
        chart = None
        return (stringret, table_cols, table_records, chart)
    
    if (df[(df.Home == input_my_dropdown1)|(df.Away == input_my_dropdown1)].shape[0] == 0):
        stringret = "Your team has a bye this week."
        #dispret = {'display': 'none'}
        test = pd.DataFrame()
        table_cols = [{"name": str(i), "id": str(i)} for i in test.columns]
        table_records = test.to_dict('records')
        chart = None
        return (stringret, table_cols, table_records, chart)

    if (finished[(finished.Home == input_my_dropdown1)|(finished.Away == input_my_dropdown1)].shape[0] != 0):
        target = finished[(finished.Away == input_my_dropdown1) | (finished.Home == input_my_dropdown1)]
        home = target['Home'].iat[0]
        away = target['Away'].iat[0]
        score = target['Time (ET)'].iat[0]
        stringret = "Your team has already played. The {} were the away team and the {} were the home team. {}".format(away, home, score)
        #dispret = {'display': 'none'}
        test = pd.DataFrame()
        table_cols = [{"name": str(i), "id": str(i)} for i in test.columns]
        table_records = test.to_dict('records')
        chart = None
        return (stringret, table_cols, table_records, chart)
    
    target = future[(future.Away == input_my_dropdown1) | (future.Home == input_my_dropdown1)]
    team = historical[(historical.home == input_my_dropdown1)|(historical.away == input_my_dropdown1)]
    if (target.Temp.values[0] == "DOME"):
        comparable = team[team.stadium=='dome']
        x = round(comparable[comparable.winner == input_my_dropdown1].shape[0]/comparable.shape[0],2)
        percentage = "{:.0%}".format(x)
        stringret = "Your team is playing in a dome. In the 2010-2017 seasons, they won {} percent of games they have played in a dome. Below are the results of up to 10 of the most recent games (through the 2017 season) the team has played in a dome:".format(percentage)
        comparable = comparable.drop(columns = ["unique_event_id","avg_temp","avg_wind", "precipitation"]).tail(10)
        table_cols = [{"name": str(i), "id": str(i)} for i in comparable.columns]
        table_records = comparable.to_dict('records')

        all_comp = historical[historical.stadium=='dome']
        winners = all_comp.groupby(by='winner').count()['date']
        aways = all_comp.groupby(by='away').count()['date']
        homes = all_comp.groupby(by='home').count()['date']

        temp = pd.merge(winners, aways, how='outer', left_index=True, right_index=True)
        final = pd.merge(temp, homes, how='outer', left_index=True, right_index=True)
        final = final.rename(columns = {'date_x': 'wins', 'date_y': 'away_games', 'date': 'home_games'})
        final = final.fillna(0)
        final['games'] = final['away_games'] + final['home_games']
        final['win_pct'] = final['wins'] / final['games']
        final = final.sort_values('win_pct', ascending=False)
        if 'tie' in final.index:
            final = final.drop('tie')

        if bar_chart:
            bar_chart[0] = px.bar(final, y="win_pct", title="Winning Percentage of All Teams in Domes")
        else:
            bar_chart = [
				dcc.Graph(
					figure=px.bar(final, y="win_pct", title="Winning Percentage of All Teams in Domes")
                )
            ]
        
    else:
        target.Temp = target.Temp.astype(float)
        target.WindSpeed = target.WindSpeed.astype(float)
        uptemp = (target.Temp.values[0]+5)
        lowtemp = (target.Temp.values[0]-5)
        upwind = (target.WindSpeed.values[0]+5)
        lowwind = (target.WindSpeed.values[0]-5)
        comparable = team[(team.avg_temp > lowtemp)&(team.avg_temp < uptemp)&(team.precipitation==target.Precipitation.values[0])&(team.avg_wind < upwind )&(team.avg_wind > lowwind )]
        
        x = round(comparable[comparable.winner == input_my_dropdown1].shape[0]/comparable.shape[0],2)
        percentage = "{:.0%}".format(x)
        stringret = "Your team has won {} percent of games in comparable weather conditions in the 2010-2017 seasons. Below are results of up to 10 of the most recent games (through the 2017 season) in comparable conditions: ".format(percentage)
        comparable = comparable.drop(columns = ["unique_event_id"]).tail(10)
        table_cols = [{"name": str(i), "id": str(i)} for i in comparable.columns]
        table_records = comparable.to_dict('records')

        winners = comparable.groupby(by='winner').count()['date']
        aways = comparable.groupby(by='away').count()['date']
        homes = comparable.groupby(by='home').count()['date']

        temp = pd.merge(winners, aways, how='outer', left_index=True, right_index=True)
        final = pd.merge(temp, homes, how='outer', left_index=True, right_index=True)
        final = final.rename(columns = {'date_x': 'wins', 'date_y': 'away_games', 'date': 'home_games'})
        final = final.fillna(0)
        final['games'] = final['away_games'] + final['home_games']
        final['win_pct'] = final['wins'] / final['games']
        final = final.sort_values('win_pct', ascending=False)
        final = final.drop('tie')

        if bar_chart:
            bar_chart[0] = px.bar(final, y="win_pct", title="Winning Percentage of All Teams in Comparable Weather Conditions")
        else:
            bar_chart = [
				dcc.Graph(
					figure=px.bar(final, y="win_pct", title="Winning Percentage of All Teams in Comparable Weather Conditions")
                )
            ]
    
    return (stringret, table_cols, table_records, bar_chart)

app.run_server(debug=True, host="0.0.0.0")