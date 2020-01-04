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

### Model
from sklearn.externals import joblib

model = joblib.load("scripts/rf.pkl")



### Hover Data
import json
import re

#change path
dl = DataLoader("data",
                ["201701-citibike-tripdata.csv"])

dl.load_data()
stations = dl.load_stations()
station_counts = dl.load_station_counts()
station_counts = station_counts.merge(stations,how = 'inner', on='station id')
station_counts['label'] = station_counts['station name'] + " bikes rental count: " + station_counts['count'].astype('str')

station_hour_count = station_counts['count'].groupby([station_counts['station name'],
                              station_counts['hour'],station_counts['date']]).sum().reset_index()



locations = {'Brooklyn':{'lat':40.650002,'lon':-73.94997},
            'Central Park':{'lat':40.785091,'lon':-73.968285},
            'Lower Manhattan':{'lat': 40.723008, 'lon':-74.000633},
            'Brooklyn Bridge': {'lat':40.706086, 'lon':-73.996864}}




spotify_green = '#1DB954'
token = 'pk.eyJ1IjoiZGFuaWVscG9uaWtvd3NraSIsImEiOiJjazRjempwb3owZ2N3M2xtMHBtZjZ6dGZ6In0.r99JQYbCq6Kevwj6DsWtGg'

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
                                    min_date_allowed=dt(2017, 1, 1),
                                    max_date_allowed=dt(2019, 12, 31),
                                    initial_visible_month=dt(2018, 1, 1),
                                    date=dt(2017, 1, 1),
                                    display_format="MMMM D, YYYY",
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
                                    id = 'location-picker',
                                    options = [
                                        {'label':k,'value':k}
                                        for k in locations
                                    ],
                                    value='A'
                                )
                            ]
                        ),
                        html.P('Start Station Picker'),
                        html.Div(
                            className='start-station',
                            children=[
                                dcc.Dropdown(
                                    id = 'start-station',
                                    options = [
                                        {'label':station, 'value':station}
                                        for station in station_counts['station name'].drop_duplicates()
                                    ]
                                )
                            ]
                        ),
                        html.P('End Station Picker'),
                        html.Div(
                            className='end-station',
                            children=[
                                dcc.Dropdown(
                                    id='end-station',
                                    options=[
                                        {'label': station, 'value': station}
                                        for station in station_counts['station name'].drop_duplicates()
                                    ]
                                )
                            ]
                        ),
                        html.P("Select ride time"),
                        html.Div(
                            className="certain-hour-picker",
                            children=[
                                dcc.Dropdown(
                                    id="ride-time",
                                    options=[
                                        {
                                            "label": str(n) + ":00",
                                            "value": str(n),
                                        }
                                        for n in range(24)
                                    ],
                                    multi=False,
                                    placeholder="Select ride time",
                                )
                            ]
                        ),
                        html.P(id="predict-time"),
                        html.P(id="click-data"),
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

## Update map
@app.callback(
    Output("map", "figure"),
    [
        Input("date-picker", "date"),
        Input("hour-selector","value"),
        Input("location-picker","value")
    ],
)
def update_graph(datePicked,hourPicked,LocationPicked):

    zoom = 12.0

    ## Location
    if LocationPicked == 'A':
        latInitial = 40.7272
        lonInitial = -73.991251
    elif isinstance(LocationPicked,str):
        latInitial = locations[LocationPicked]['lat']
        lonInitial = locations[LocationPicked]['lon']
    else:
        latInitial = 40.7272
        lonInitial = -73.991251


    bearing = 0

    ## Date
    date_picked = datePicked[0:10]


    ## Hour
    if hourPicked is None:
        hourPicked = [i for i in range(0,24)]
    else:
        hourPicked = [int(hourPicked)]

    selectedhour = [i in hourPicked for i in station_counts.hour]

    pickedData = station_counts.loc[(station_counts.date == date_picked) & (selectedhour)  ,:]


    fig = go.Figure(go.Scattermapbox(
        lon=pickedData['station longitude'],
        lat=pickedData['station latitude'],
        text=pickedData['label'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=9,
            color=spotify_green,
            opacity=pickedData['count'] / pickedData['count'].max()
            # colorscale= 'brwnyl',
            # showscale = True, # jak sie ustali skale to pokazuje skale z boku
            # reversescale = True # odwraca skale kolorow
        )
    ))

    fig.update_layout(
        autosize=True,
        hovermode='closest',
        mapbox=go.layout.Mapbox(
            accesstoken=token,
            bearing=bearing,
            center=go.layout.mapbox.Center(
                lat=latInitial,
                lon=lonInitial
            ),
            pitch=0,
            zoom=zoom,
            style="dark"
        )
    )

    return fig


## Predict time
@app.callback(Output("predict-time","children"),
              [
                  Input("start-station","value"),
                  Input("end-station","value"),
                      Input("ride-time", "value")
              ])
def update_predict_time(start_station,end_station,hourPicked):
    start_station_info = stations.loc[stations['station name'] == start_station, :]
    end_station_info = stations.loc[stations['station name'] == end_station, :]
    to_predict = pd.DataFrame({'start station latitude': start_station_info['station latitude'].values,
                               'start station longitude': start_station_info['station longitude'].values,
                               'end station latitude': end_station_info['station latitude'].values,
                               'end station longitude': end_station_info['station longitude'].values,
                               'hour': [hourPicked]})

    y_pred = np.round(model.predict(to_predict)[0],2)

    return "Przedwidywany czas jazdy: " + str(y_pred) + " minut."


@app.callback(Output('plot','figure'),
              [
                  Input("date-picker", "date"),
                  Input('map','hoverData')
              ])
def ClickData(datePicked,hoverData):

    date_picked = datePicked[0:10]



    start = ' "text": "'
    end = ' bikes'
    try:
        x = json.dumps(hoverData, indent=2)
        res = x.split(start)[1].split(end)[0]
    except IndexError:
        res = '1 Ave & E 16 St'

    to_plot = station_hour_count.loc[
              (station_hour_count['station name'] == res) & (station_hour_count['date'] == date_picked) ,
              :]

    hour = [i for i in range(25)]

    count = []

    for i in hour:
        if i in to_plot.hour.values:
            count.append(to_plot.loc[to_plot.hour.values == i, 'count'].values[0])
        else:
            count.append(0)

    df = pd.DataFrame({'hour': hour,
                       'count': count})

    fig = go.Figure(data = [go.Bar(
        x=df['hour'],
        y=df['count'],
        marker_color = spotify_green)])

    fig.update_layout(
        title_text = 'Count barplot for: ' + res + " station " + date_picked
    )

    return fig


if __name__ == '__main__':
    app.run_server(debug=False)