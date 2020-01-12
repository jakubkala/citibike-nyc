from dataloader import DataLoader
import pandas as pd

dl = DataLoader("~/IAD/semestr-1/PADR/citibike-tripdata/data",
                ["201701-citibike-tripdata.csv",
                 "201704-citibike-tripdata.csv",
                 "201707-citibike-tripdata.csv",
                 "201710-citibike-tripdata.csv",
                 ])
dl.load_data()
X = dl.data.sample(5000)
del dl

X = X.loc[(X['trip duration'] > 120) &
          (X['trip duration'] < 7200) &
          (1 - pd.isnull(X['birth year'])) &
          (X['birth year'] > 1880),:]
X['start time'] = pd.to_datetime(X['start time'])
X['age'] = 2017 - X['birth year']
X['hour'] = X['start time'].dt.hour

X = X.loc[:,['trip duration','age','hour']]
X.to_csv("./data/distplot_data.csv")