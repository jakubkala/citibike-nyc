import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np

from dash.dependencies import Input, Output
from plotly import graph_objs as go
from plotly.graph_objs import *
from datetime import datetime as dt

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
            children=[dcc.Graph(id='map'),
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