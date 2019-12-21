import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np

from dash.dependencies import Input, Output
from plotly import graph_objs as go
from plotly.graph_objs import *
from datetime import datetime as dt

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__)
#server = app.server




from dataloader import DataLoader

### Obróbka danych
dataloader = DataLoader("../data/",["201901-citibike-tripdata.csv"])
dataloader.load_data()
station_counts = dataloader.load_station_counts()
station = dataloader.load_stations()
station = station_counts.merge(station,how = 'inner', right_on='station id', left_on = 'start station id')
station_20190101_16 = station.loc[(station.hour == 16) & (station.day == '2019-01-01') & (station['count'] > 5),:]
station_20190101_16['text'] = station_20190101_16['station name'] + " count: " + station_20190101_16['count'].astype('str')



### Mapa
import plotly.graph_objects as go

spotify_green = '#1DB954'
token = 'pk.eyJ1IjoiZGFuaWVscG9uaWtvd3NraSIsImEiOiJjazRjempwb3owZ2N3M2xtMHBtZjZ6dGZ6In0.r99JQYbCq6Kevwj6DsWtGg'

fig = go.Figure(go.Scattermapbox(
        lon = station_20190101_16['station longitude'],
        lat = station_20190101_16['station latitude'],
        text = station_20190101_16['text'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size = 9,
            color = spotify_green,
            opacity = station_20190101_16['count']/station_20190101_16['count'].max()
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
            lat= station.loc[0,'station latitude'],
            lon= station.loc[0,'station longitude']
        ),
        pitch=0,
        zoom=11,
        style="dark"
    )
)


# #wrapper {
#     width: 500px;
#     border: 1px solid black;
#     overflow: hidden; /* add this to contain floated children */
# }
# #first {
#     width: 300px;
#     float:left; /* add this */
#     border: 1px solid red;
# }
# #second {
#     border: 1px solid green;
#     float: left; /* add this */
# }

app.layout = html.Div(

    style={'border': '1px solid black'},

    children=[
        html.Div(
            className="row",
            style={'width': '30%', 'float':'left', 'height':'100vh','border': '1px solid black'},
            children=[
                html.Div(
                    className='user-controls',
                    children=[
                        html.H2("CITIBIKE NYC"),
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
                                    display_format="MM-DD",
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
                        )
                    ]
                )
            ]
    ),
        html.Div(

            style={'width':'69%','style':'dark','float':'left','height':'100vh','border': '1px solid black'},
            className="2nd-div",
            children=[html.Div(
                          className="text-padding",
                          children=["Map"]
                      ),
                dcc.Graph(id='map',figure = fig)
                ,

                      html.Div(
                          className="text-padding",
                          children=["Lorem Ipsumm"]
                      ),
                      dcc.Graph(id='plot')
                ]
        )]
)

if __name__ == '__main__':
    app.run_server(debug=True)