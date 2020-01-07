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
        month_count = {}
        number_of_bike = {}
        dfs = []

        columnnames = ['trip duration', 'start time', 'stop time', 'start station id',
       'start station name', 'start station latitude',
       'start station longitude', 'end station id', 'end station name',
       'end station latitude', 'end station longitude', 'bike id', 'user type',
       'birth year', 'gender']

        if self.files is not None:
            for filename in tqdm(self.files):
                df = pd.read_csv(os.path.join(self.path, filename))
                df.columns = [colname.lower() for colname in df.columns]
                df.columns = columnnames
                dfs.append(df)
                month_count[filename[0:6]] = df.shape[0]
                number_of_bike[filename[0:6]] = df['bike id'].drop_duplicates().shape[0]

        else:
            for filename in tqdm(os.listdir(self.path)):
                if 'citibike-tripdata.csv' in filename:
                    df = pd.read_csv(os.path.join(self.path, filename))
                    df.columns = [colname.lower() for colname in df.columns]
                    df.columns = columnnames
                    dfs.append(df)
                    month_count[filename[0:6]] = df.shape[0]
                    number_of_bike[filename[0:6]] = df['bike id'].drop_duplicates().shape[0]

        res = pd.concat(dfs).reset_index(drop = True)



        self.data = res
        self.month_count = month_count
        self.number_of_bike = number_of_bike
        
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
        df2 = self.data.copy()

        df2['start time'] = pd.to_datetime(df2['start time'])

        df['hour'] = df2['start time'].dt.hour
        df['day'] = df2['start time'].dt.date.astype('str')

        res = df.loc[:, ['start station id', 'day','hour']].groupby(
            ['start station id', 'day','hour']).size().reset_index().rename(
            columns={0: 'count'})

        res.columns = ['station id', 'date', 'hour', 'count']

        return res

    def load_end_station_counts(self):
        """
        returns counts of bike rentals per station
        """

        df = self.data.copy()
        df2 = self.data.copy()

        df2['stop time'] = pd.to_datetime(df2['stop time'])

        df['hour'] = df2['stop time'].dt.hour
        df['day'] = df2['stop time'].dt.date.astype('str')

        res = df.loc[:, ['end station id', 'day','hour']].groupby(
            ['end station id', 'day','hour']).size().reset_index().rename(
            columns={0: 'count'})

        res.columns = ['station id', 'date', 'hour', 'count']

        return res




def main():
    pass

if __name__ == "__main__":
    main()