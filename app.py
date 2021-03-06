# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np

from dash.dependencies import Input, Output
from plotly import graph_objs as go
from datetime import datetime as dt

#### Map
from scripts.dataloader import  DataLoader

### Model
from sklearn.externals import joblib
from tqdm import tqdm
import json
import plotly.express as px


model = joblib.load("scripts/rf.pkl")

# dist_plot data
X = pd.read_csv("data/to_app/distplot_data.csv").sample(1000000)


slider_min  = html.Div([
    dcc.Slider(
        id='slider-min',
        min=0,
        max=100,
        step=1,
        value=10,
        marks = {i:str(i) for i in range(0,100,10)}
    )])


slider_max  = html.Div([
    dcc.Slider(
        id='slider-max',
        min=0,
        max=100,
        step=1,
        value=25,
        marks = {i:str(i) for i in range(0,100,5)},
        vertical = False
    )])

slider = html.Div([
    dcc.RangeSlider(
        id='slider',
        min=0,
        max=100,
        step=1,
        value=[25, 55],
        marks = {i:str(i) for i in range(0,100,10)}
    )
])

sector_picker = html.Div(
    className='sector_picker',
    children=[
        dcc.Dropdown(
            id = 'sector',
            options = [
                {'label':sec, 'value':sec}
                for sec in range(0,10)
            ]
        )
    ]
)

#####

stations = {}
station_counts = {}
station_hour_count = {}
end_station_hour_count = {}

for year in range(2013,2020):
    if year == 2013:
        for i in tqdm(range(8,13)):
            if i < 10:
                file = str(year) + "0" + str(i)
            else:
                file = str(year) + str(i)
            stations[file] = pd.read_csv("data/to_app/stations" + file + ".csv")
    elif year == 2019:
        for i in tqdm(range(1,12)):
            if i < 10:
                file = str(year) + "0" + str(i)
            else:
                file = str(year) + str(i)
            stations[file] = pd.read_csv("data/to_app/stations" + file + ".csv")

    else:
        for i in tqdm(range(1,13)):
            if i < 10:
                file = str(year) + "0" + str(i)
            else:
                file = str(year) + str(i)
            stations[file] = pd.read_csv("data/to_app/stations" + file + ".csv")



for year in range(2016,2019):
    for i in tqdm(range(1,13)):
        if i < 10:
            file = str(year) + "0" + str(i)
        else:
            file = str(year) + str(i)
        station_counts[file] = pd.read_csv("data/to_app/station_counts" + file + ".csv")
        station_hour_count[file] = pd.read_csv("data/to_app/station_hour_count" + file + ".csv")
        end_station_hour_count[file] = pd.read_csv("data/to_app/end_station_hour_count" + file + ".csv")

locations = {'Brooklyn':{'lat':40.650002,'lon':-73.94997},
            'Central Park':{'lat':40.785091,'lon':-73.968285},
            'Lower Manhattan':{'lat': 40.723008, 'lon':-74.000633},
            'Brooklyn Bridge': {'lat':40.706086, 'lon':-73.996864}}




spotify_green = '#1DB954'
token = 'pk.eyJ1IjoiZGFuaWVscG9uaWtvd3NraSIsImEiOiJjazRjempwb3owZ2N3M2xtMHBtZjZ6dGZ6In0.r99JQYbCq6Kevwj6DsWtGg'

app = dash.Dash(__name__)

# Date picker
date_picker = html.Div(
    className='date-dropdown-div',
    children=[
        dcc.DatePickerSingle(
            id='date-picker',
            min_date_allowed=dt(2016, 1, 1),
            max_date_allowed=dt(2019, 12, 31),
            initial_visible_month=dt(2018, 1, 1),
            date=dt(2018, 1, 1),
            display_format="MMMM D, YYYY",
            style={"border": "0px solid black"}
        )
    ]
)

# Hour picker
hour_picker = html.Div(
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
            multi=True,
            placeholder="Select certain hours",
        )
    ]
)

# Location Picker
location_picker = html.Div(
    className='location-picker',
    children=[
        dcc.Dropdown(
            id = 'location-picker',
            options = [
                {'label':k,'value':k}
                for k in locations],
            value='A'
        )
    ]
)

# Start station picker
start_station_picker = html.Div(
    className='start-station',
    children=[
        dcc.Dropdown(
            id = 'start-station',
            options = [
                {'label':station, 'value':station}
                for station in station_counts["201801"]['station name'].drop_duplicates()
            ]
        )
    ]
)
# End station picker
end_station_picker = html.Div(
    className='end-station',
    children=[
        dcc.Dropdown(
            id='end-station',
            options=[
                {'label': station, 'value': station}
                for station in station_counts["201801"]['station name'].drop_duplicates()
            ]
        )
    ]
)

# Ride time
ride_time = html.Div(
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
)


# Map tab
map_div = html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                # Left control panel
                html.Div(
                    className='user-controls',
                    children=[
                        html.H2("citibike-nyc"),

                        html.P("Date"),
                        date_picker,

                        html.P("Time"),
                        hour_picker,

                        html.P('Location'),
                        location_picker,

                        html.P('Start Station'),
                        start_station_picker,

                        html.P('End Station'),
                        end_station_picker,

                        html.P("Ride time"),
                        ride_time,

                        html.P(id="predict-time"),
                        html.P(id="click-data"),
                        html.P(id = 'hour-test')
                    ]
                )
            ]
        ),
        html.Div(
            className="map-div",
            children=[dcc.Graph(id='map'),
                      html.Div(
                          id = 'title-plot',
                          className="text-padding",
                          children=["Lorem Ipsumm"]
                      ),
                      dcc.Graph(id='plot'),
                      ]
        )
    ]
)

## Insight tab
from plotly.subplots import make_subplots

weather = pd.read_csv("data/to_app/weather_data_1617.csv")
count_by_day2017 = pd.read_csv("data/to_app/count_by_day2017.csv")
count_by_day2016 = pd.read_csv("data/to_app/count_by_day2016.csv")
count_by_day = pd.concat([count_by_day2016,count_by_day2017]).sort_values(['day']).reset_index(drop = True)



fig = make_subplots(
    rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.02,
    print_grid=False,specs=[[{"secondary_y": False}],[{"secondary_y": True}]]
)

fig.add_trace(
    go.Scatter(x=weather.loc[:,'date'],
               y=weather.loc[:,'average temperature'].values,
               name = "temperature", marker = dict(color = spotify_green)
    ),
    row=2, col=1,secondary_y=False
)

fig.add_trace(
    go.Bar(
        x=weather.loc[:,'date'],
        y=weather.loc[:,'snow depth'].values,
        name = 'snow',marker = dict(color = "white")
    ),
    row = 2, col = 1,secondary_y=True
)

fig.add_trace(
    go.Bar(
        x=weather.loc[:,'date'],
        y=weather.loc[:,'precipitation'].values,
        name = 'rain',marker = dict(color = "blue")
    ),
    row = 2, col = 1,secondary_y=True
)



fig.add_trace(go.Scatter(x=count_by_day.loc[:,'day'].values,
                         y=count_by_day.loc[:,'count'].values,
                         name = "rides count",
                         marker = dict(color = 'red'))
              ,row=1, col=1)


fig.update_layout(height=600, width=800)
fig.update_xaxes(title_text='Date', color=spotify_green)
fig.update_yaxes(title_text='Value', color=spotify_green)

fig['layout']['yaxis2'].update(showgrid=False,zeroline=False)
fig['layout']['yaxis1'].update(showgrid=False,zeroline=False)
fig['layout']['xaxis2'].update(showgrid=False,zeroline=False)
fig['layout']['xaxis1'].update(showgrid=False,zeroline=False)
fig['layout']['yaxis3'].update(showgrid=False,zeroline=False)
fig.layout.plot_bgcolor = '#1E1E1E'
fig.layout.paper_bgcolor = '#1E1E1E'

citibike_popularity = pd.read_csv("data/basic_stats.csv")
citibike_popularity['date'] = pd.to_datetime(citibike_popularity['miesiac'], format="%Y%m")

fig_popularity = go.Figure(
    data= [go.Scatter(x=citibike_popularity.loc[:, "date"],
                      y=citibike_popularity.loc[:, "liczba_jazd"].values,
                      marker=dict(color=spotify_green))
           ])

fig_popularity.layout.plot_bgcolor = '#1E1E1E'
fig_popularity.layout.paper_bgcolor = '#1E1E1E'
fig_popularity['layout']['yaxis'].update(showgrid=False,zeroline=False)
fig_popularity['layout']['xaxis'].update(showgrid=False,zeroline=False)
fig_popularity.update_xaxes(title_text='Date', color=spotify_green)
fig_popularity.update_yaxes(title_text='Count', color=spotify_green)


##########################################################################
latInitial = 40.7272
lonInitial = -73.991251

data = [go.Scattermapbox(
    lat=stations['201308'].loc[:, 'station latitude'],
    lon=stations['201308'].loc[:, 'station longitude'],
    mode='markers',
    marker=dict(size=10, color=spotify_green,
                opacity=0.7)
)
]

layout = go.Layout(width=800,
                   autosize=True,
                   hovermode='closest',
                   mapbox=dict(accesstoken=token,
                               bearing=0,
                               center=dict(lat=latInitial,
                                           lon=lonInitial),
                               pitch=0,
                               zoom=9,
                               style='dark'
                               )
                   )

frames = [dict(data=[dict(type='scattermapbox',
                          lat=list(v['station latitude']),
                          lon=list(v['station longitude']))],
               traces=[0],
               name=k
               ) for k, v in stations.items()]

sliders = [dict(steps=[dict(method='animate',
                            args=[[k],
                                  dict(mode='immediate',
                                       frame=dict(duration=24, redraw=False),
                                       transition=dict(duration=0)
                                       )
                                  ],
                            label=k[0:4] + "-" + k[4:6]
                            ) for k, v in stations.items()],
                transition=dict(duration=0),
                x=0,  # slider starting position
                y=0,
                currentvalue=dict(font=dict(size=12),
                                  prefix='Point: ',
                                  visible=True,
                                  xanchor='center'),
                len=1.0)
           ]

layout.update(margin=dict(t=0, b=0, l=0, r=0),
              updatemenus=[dict(type='buttons', showactive=False,
                                y=0,
                                x=1.05,
                                xanchor='right',
                                yanchor='top',
                                pad=dict(t=0, r=10),
                                buttons=[dict(label='Play',
                                              method='animate',
                                              args=[None,
                                                    dict(frame=dict(duration=100,
                                                                    redraw=True),
                                                         transition=dict(duration=0),
                                                         fromcurrent=True,
                                                         mode='immediate'
                                                         )
                                                    ]
                                              )
                                         ]
                                )
                           ],
              sliders=sliders)

animation_station = go.Figure(data=data, layout=layout, frames=frames)

animation_station.layout.plot_bgcolor = '#1E1E1E'
animation_station.layout.paper_bgcolor = '#1E1E1E'






stacje17 = ['20170' + str(i) if i < 10 else '2017' + str(i) for i in range(1,13)  ]
stacje17 = pd.concat([stations[i] for i in stacje17]).drop_duplicates()
clust = joblib.load("scripts/KMeans.pkl")
stacje17['label'] = clust.predict(stacje17.loc[:,['station latitude','station longitude']])
to_draw = pd.DataFrame({"lat":stacje17.loc[:,'station latitude'],
                       "lon":stacje17.loc[:,'station longitude'],
                       "label":clust.predict(stacje17.loc[:,['station latitude','station longitude']])}
                      ).drop_duplicates()

fig_sector = go.Figure(go.Scattermapbox(
        lat = stacje17['station latitude'],
        lon = stacje17['station longitude'],
        text = stacje17['label'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size = 9,
            color = stacje17['label'],
            opacity = 0.7)
    ))

fig_sector.update_layout(
    margin=dict(t=0, b=0, l=0, r=0),
    autosize=True,
    hovermode='closest',
    mapbox=go.layout.Mapbox(
        accesstoken= token,
        bearing=0,
        center=go.layout.mapbox.Center(
            lat= stacje17.loc[0,'station latitude'],
            lon= stacje17.loc[0,'station longitude']
        ),
        pitch=0,
        zoom=11,
        style="dark"
    )
)

fig_sector.layout.plot_bgcolor = '#1E1E1E'
fig_sector.layout.paper_bgcolor = '#1E1E1E'
sektor_data = pd.read_csv("data/to_app/sektory.csv")


# Application layout

app.layout = html.Div([
    dcc.Tabs(
        id='tabs',
        children=[
            dcc.Tab(label='Map', children=[
                map_div
            ]),
            dcc.Tab(label='Insights', children=[
                html.Div(id='insight-tab',
                         children = [
                            html.P("Citibike popularity over time"),
                            dcc.Graph(figure=fig_popularity, id='popularity'),

                             html.P("Citibike popularity vs weather"),
                            dcc.Graph(figure=fig, id='weather'),

                            html.P("Age vs time of day"),
                            dcc.Graph(id='distplot'),
                            html.P("Age:"),
                            slider,

                             html.P("Stations"),
                             dcc.Graph(figure=animation_station, id='animation-station'),

                             html.P("Clustered areas of NYC"),
                            dcc.Graph(figure=fig_sector, id="NY-sector"),
                            sector_picker,
                            dcc.Graph(id="rides-from_sector"),
                            html.P("")
                         ],
                         style={"display":"table",
                                "width":"50%",
                                "margin":"0 auto"})

            ]),
        ])
])

## Update map
@app.callback(
    Output("map", "figure"),
    [
        Input("date-picker", "date"),
        Input("hour-selector","value"),
        Input("location-picker","value"),
        Input("start-station", "value"),
        Input("end-station", "value"),

    ],
)
def update_graph(datePicked,hourPicked,LocationPicked,start_station,end_station):

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

    station_counts_loc = station_counts[str(date_picked[0:4]) + str(date_picked[5:7])]

    ## Hour
    if hourPicked is None:
        hourPicked = [i for i in range(0,24)]
    elif len(hourPicked) > 0:
        hourPicked = [int(i) for i in hourPicked]
    else:
        hourPicked = [i for i in range(24)]

    selectedhour = [i in hourPicked for i in station_counts_loc.hour]

    pickedData = station_counts_loc.loc[(station_counts_loc.date == date_picked) & (selectedhour)  ,:]

    colors = ["blue" if pickedData['station name'].values[i] == start_station else "red" if
    pickedData['station name'].values[i] == end_station else spotify_green for i in range(pickedData.shape[0])]


    fig = go.Figure(go.Scattermapbox(
        lon=pickedData['station longitude'],
        lat=pickedData['station latitude'],
        text=pickedData['label'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=9,
            color=colors,
            opacity=pickedData['count'] / pickedData['count'].max()
        )
    ))

    fig.update_layout(
        autosize=True,
        hovermode='closest',
        margin=dict(t=0, b=0, l=0, r=0),
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

    stations_loc = stations['201801']
    if isinstance(start_station,str) and isinstance(end_station,str) and isinstance(hourPicked,str):
        start_station_info = stations_loc.loc[stations_loc['station name'] == start_station, :]
        end_station_info = stations_loc.loc[stations_loc['station name'] == end_station, :]
        to_predict = pd.DataFrame({'start station latitude': start_station_info['station latitude'].values,
                               'start station longitude': start_station_info['station longitude'].values,
                               'end station latitude': end_station_info['station latitude'].values,
                               'end station longitude': end_station_info['station longitude'].values,
                               'hour': [int(hourPicked)]})

        y_pred = np.round(model.predict(to_predict)[0],2)
    else:
        y_pred = 0

    if end_station == start_station:
        y_pred = 0
        
    return "Estimated ride time: " + str(y_pred) + " minutes."


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

    station_hour_count_local = station_hour_count[str(date_picked[0:4]) + str(date_picked[5:7])]

    end_station_hour_count_local = end_station_hour_count[str(date_picked[0:4]) + str(date_picked[5:7])]

    to_plot = station_hour_count_local.loc[
              (station_hour_count_local['station name'] == res) & (station_hour_count_local['date'] == date_picked) ,
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


    to_plot2 = end_station_hour_count_local.loc[
              (end_station_hour_count_local['station name'] == res) & (end_station_hour_count_local['date'] == date_picked) ,
              :]

    hour = [i for i in range(25)]

    count2 = []

    for i in hour:
        if i in to_plot2.hour.values:
            count2.append(-to_plot2.loc[to_plot2.hour.values == i, 'count'].values[0])
        else:
            count2.append(0)

    df2 = pd.DataFrame({'hour': hour,
                       'count': count2})



    fig = go.Figure(data = [
        go.Bar(name = 'Rentals', x=df['hour'], y=df['count'],marker_color = spotify_green),
        go.Bar(name = 'Returns', x=df2['hour'], y=df2['count'], marker_color='red')]
    )

    fig.update_layout(
        barmode = 'group',
        margin=dict(t=0, b=2, l=2, r=0),
        xaxis=dict(showgrid=False, zeroline=False,color = spotify_green,title_text = "Hour"),
        yaxis=dict(showgrid=False, zeroline=False,color = spotify_green,title_text = "Count")
    )

    fig.layout.plot_bgcolor = '#1E1E1E'
    fig.layout.paper_bgcolor = '#1E1E1E'

    return fig

@app.callback(Output('title-plot','children'),
              [
                  Input("date-picker", "date"),
                  Input('map','hoverData')
              ])
def title_plot_update(datePicked,hoverData):
    start = ' "text": "'
    end = ' bikes'
    try:
        x = json.dumps(hoverData, indent=2)
        res = x.split(start)[1].split(end)[0]
    except IndexError:
        res = '1 Ave & E 16 St'

    date_picked = datePicked[0:10]

    return 'Count barplot for: ' + res + " station " + date_picked,


@app.callback(Output('distplot','figure'),
              [
                  Input('slider', 'value')
              ])
def updateDistPlot(value):

    min_age, max_age = value

    scale = ['#1E1E1E'] + px.colors.sequential.Viridis
    Y = X.loc[(X.age > min_age) & (X.age <= max_age), :]
    if Y.shape[0] > 10000:
        Y = Y.sample(10000)

    x = Y.loc[:, 'age']
    y = Y.loc[:, 'hour']

    trace1 = go.Scatter(
        x=x, y=y, mode='markers', name='points',
        marker=dict(color=scale[0], size=1, opacity=0.4)
    )
    trace2 = go.Histogram2dcontour(
        x=x, y=y, name='density', ncontours=25,
        colorscale=scale, reversescale=False, showscale=False
    )
    trace3 = go.Histogram(
        x=x, name='x density',
        marker=dict(color=spotify_green),
        yaxis='y2'
    )
    trace4 = go.Histogram(
        y=y, name='y density', marker=dict(color=spotify_green),
        xaxis='x2'
    )
    data = [trace1, trace2, trace3, trace4]

    layout = go.Layout(
        showlegend=False,
        autosize=False,
        # width=600,
        # height=550,
        xaxis=dict(
            domain=[0, 0.85],
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            domain=[0, 0.85],
            showgrid=False,
            zeroline=False
        ),
        margin=dict(
            t=50
        ),
        hovermode='closest',
        bargap=0,
        xaxis2=dict(
            domain=[0.85, 1],
            showgrid=False,
            zeroline=False
        ),
        yaxis2=dict(
            domain=[0.85, 1],
            showgrid=False,
            zeroline=False
        )
    )

    fig = go.Figure(data=data, layout=layout)
    fig.update_xaxes(title_text='Age', color=spotify_green)
    fig.update_yaxes(title_text='Hour', color=spotify_green)
    fig.layout.plot_bgcolor = '#1E1E1E'
    fig.layout.paper_bgcolor = '#1E1E1E'
    fig.update_layout(
        margin=dict(t=0, b=0, l=0, r=0))
    return fig

@app.callback(Output('rides-from_sector','figure'),
              [
                  Input('sector','value')
              ])
def sector_map(sector):
    if sector is None:
        sector = 3
    def to_map(i):
        df_0 = sektor_data.loc[sektor_data.sektor == i, :]
        count_0 = df_0.groupby('end station id').size().reset_index().rename(columns={0: 'counts'})
        df_1 = stacje17.merge(count_0, left_on='station id', right_on='end station id')
        to_plot = pd.DataFrame({'lat': df_1['station latitude'],
                                'lon': df_1['station longitude'],
                                'opacity': df_1.counts / df_1.counts.max(),
                                'color': df_1.label,
                                'text': ["sektor: " + str(df_1.label[j]) + " count: " + str(df_1.counts[j])
                                         for j in range(0, df_1.shape[0])]}).drop_duplicates()
        return to_plot

    to_plot = to_map(sector)

    fig = go.Figure(go.Scattermapbox(
            lat = to_plot['lat'],
            lon = to_plot['lon'],
            text = to_plot['text'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size = 9,
                color = to_plot.color,
                opacity = to_plot.opacity)
        ))

    fig.update_layout(
        margin=dict(t=0, b=0, l=0, r=0),
        autosize=True,
        hovermode='closest',
        mapbox=go.layout.Mapbox(
            accesstoken= token,
            bearing=0,
            center=go.layout.mapbox.Center(
                lat= to_plot.lat[0],
                lon= to_plot.lon[0]
            ),
            pitch=0,
            zoom=11,
            style="dark"
        )
    )

    fig.layout.plot_bgcolor = '#1E1E1E'
    fig.layout.paper_bgcolor = '#1E1E1E'

    return fig



if __name__ == '__main__':
    app.run_server(debug=True)