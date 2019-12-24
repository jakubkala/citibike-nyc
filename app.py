import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np

from dash.dependencies import Input, Output
from plotly import graph_objs as go
from plotly.graph_objs import *
from datetime import datetime as dt


#### Map
from scripts.dataloader import  DataLoader

#change path
dl = DataLoader("/home/jakubkala/IAD/semestr-1/PADR/citibike-tripdata/data",
                ["201701-citibike-tripdata.csv"])

dl.load_data()
stations = dl.load_stations()
station_counts = dl.load_station_counts()
station_counts = station_counts.merge(stations,how = 'inner', on='station id')
station_counts['label'] = station_counts['station name'] + " bikes rental count: " + station_counts['count'].astype('str')


spotify_green = '#1DB954'
token = 'pk.eyJ1IjoiZGFuaWVscG9uaWtvd3NraSIsImEiOiJjazRjempwb3owZ2N3M2xtMHBtZjZ6dGZ6In0.r99JQYbCq6Kevwj6DsWtGg'

fig = go.Figure(go.Scattermapbox(
        lon = station_counts['station longitude'],
        lat = station_counts['station latitude'],
        text = station_counts['label'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size = 9,
            color = spotify_green,
            opacity = station_counts['count']/station_counts['count'].max()
            # colorscale= 'brwnyl',
            # showscale = True, # jak sie ustali skale to pokazuje skale z boku
            # reversescale = True # odwraca skale kolorow
        )
    ))

fig.update_layout(
    autosize=True,
    hovermode='closest',
    mapbox=go.layout.Mapbox(
        accesstoken= token,
        bearing=0,
        center=go.layout.mapbox.Center(
            lat= stations.loc[0,'station latitude'],
            lon= stations.loc[0,'station longitude']
        ),
        pitch=0,
        zoom=11,
        style="dark"
    )
)

app = dash.Dash(__name__)

app.layout = html.Div(
    style={'border': '1px solid black'},
    children=[
        html.Div(
            className="row",
            #style={'width': '30%', 'float':'left', 'height':'100vh','border': '1px solid black'},
            children=[
                html.Div(
                    className='user-controls',
                    children=[
                        html.H2("citibike-nyc"),
                        html.P("Date Picker"),
                        html.Div(
                            className='date-dropdown-div',
                            children=[
                                dcc.DatePickerSingle(
                                    id='date-picker',
                                    min_date_allowed=dt(2018, 1, 1),
                                    max_date_allowed=dt(2018, 12, 31),
                                    initial_visible_month=dt(2018, 1, 1),
                                    date=dt(2018, 1, 1),
                                    display_format="MMMM, DD",
                                    style={"border": "0px solid black"}
                                )
                            ]
                        ),
                        html.P("Certain hour picker"),
                        html.Div(
                            className="certain-hour-picker",
                            children=[
                                dcc.Dropdown(
                                    id="hour-selector",
                                    options=[
                                        {
                                            "label": str(n) + ":00",
                                            "value": str(n),
                                        }
                                        for n in range(24)
                                    ],
                                    multi=False,
                                    placeholder="Select certain hours",
                                )
                            ]
                        ),
                        html.P('Location Picker'),
                        html.Div(
                            className='location-picker',
                            children=[
                                dcc.Dropdown(
                                    options=[
                                        {'label': 'A', 'value': 'A'},
                                        {'label': 'B', 'value': 'B'},
                                        {'label': 'C', 'value': 'C'}
                                    ],
                                    value='A'
                                )
                            ]
                        ),
                        html.P("Daniel Ponikowski \n Jakub Kała \n 2019")
                    ]
                )
            ]
    ),
        html.Div(
            #style={'width':'69%', 'float':'left','border': '1px solid black'},
            className="map-div",
            children=[dcc.Graph(id='map', figure=fig),
                      html.Div(
                          className="text-padding",
                          children=["Lorem Ipsumm"]
                      ),
                      dcc.Graph(id='plot')
                ]
        )]
)

if __name__ == '__main__':
    app.run_server(debug=False)