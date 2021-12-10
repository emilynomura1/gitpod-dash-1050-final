import dash
from dash import dcc # dash core components

from dash import dash_table
from dash import dcc # dash core components
from dash import html
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H2(children='NFL Weather Data'),
    html.Img(src='/assets/nfl logo.jpg',width="210", height="118"),
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
    {"label": "Tampa Bay Buccanears", "value": "Buccanears"},
    {"label": "Tennessee Titans", "value": "Titans"},
    {"label": "Washington Football Team", "value": "Washington"},
            ],
            value='Select a team'
        ),
        html.Label(id='my_label1'),
 html.Button(
            id='submit-button',
            n_clicks=0,
            children='Submit',
            style={'fontSize':16}
        ),       
    
])


app.run_server(debug=True, host="0.0.0.0")