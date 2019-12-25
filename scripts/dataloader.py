import os
import pandas as pd
from tqdm import tqdm
import datetime as dt

class DataLoader():
    def __init__(self, path, files=None):
        """

        :param path: directory that contains data
        :param files: names of files to be loaded; if None: all data from directory will be read
        """
        self.path = path
        self.files = files

        return

    def load_data(self):

        dfs = []
        if self.files is not None:
            for filename in tqdm(self.files):
                df = pd.read_csv(os.path.join(self.path, filename))
                df.columns = [colname.lower() for colname in df.columns]
                dfs.append(df)
        else:
            for filename in tqdm(os.listdir(self.path)):
                if 'citibike-tripdata.csv' in filename:
                    df = pd.read_csv(os.path.join(self.path, filename))
                    df.columns = [colname.lower() for colname in df.columns]
                    dfs.append(df)

        res = pd.concat(dfs)

        res.columns = ['trip duration', 'start time', 'stop time', 'start station id',
       'start station name', 'start station latitude',
       'start station longitude', 'end station id', 'end station name',
       'end station latitude', 'end station longitude', 'bike id', 'user type',
       'birth year', 'gender']

        self.data = res

        return

    def load_stations(self):
        """
        returns stations list
        """
        names = ['station id', 'station name', 'station latitude', 'station longitude']

        # start stations
        start = self.data[['start station id',
                           'start station name',
                           'start station latitude',
                           'start station longitude']]

        start.columns = names

        # end stations
        end = self.data[['end station id',
                         'end station name',
                         'end station latitude',
                         'end station longitude']]

        end.columns = names

        return pd.concat([start, end]).drop_duplicates().reset_index(drop=True)

    def load_station_counts(self):
        """
        returns counts of bike rentals per station
        """

        df = self.data.copy()

        df['day'] = [i[0:10] for i in df['start time']]
        df['hour'] = [int(i[11:13]) for i in df['start time']]

        res = df.loc[:, ['start station id', 'day','hour']].groupby(
            ['start station id', 'day','hour']).size().reset_index().rename(
            columns={0: 'count'})

        res.columns = ['station id', 'date', 'hour', 'count']

        return res

def main():
    pass

if __name__ == "__main__":
    main()