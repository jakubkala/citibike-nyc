import os
import pandas as pd
from tqdm import tqdm

def load_data(path, files = None):
    """

    :param path: directory that contains data
    :param files: names of files to be loaded; if None: all data from directory will be read
    :return:
    """

    dfs = []
    if files is not None:
        for filename in tqdm(files):
            dfs.append(pd.read_csv(os.path.join(path, filename)))
    else:
        for filename in tqdm(os.listdir(path)):
            if 'citibike-tripdata.csv' in filename:
                dfs.append(pd.read_csv(os.path.join(path, filename)))

    return pd.concat(dfs)


def load_stations(df):
    """
    returns stations list
    """
    names = ['station id', 'station name', 'station latitude', 'station longitude']

    # start stations
    start = df[['start station id',
                'start station name',
                'start station latitude',
                'start station longitude']]
    start.columns = names

    # end stations
    end = df[['end station id',
              'end station name',
              'end station latitude',
              'end station longitude']]
    end.columns = names

    return pd.concat([start, end]).drop_duplicates().reset_index(drop=True)


def main():
    #~/IAD/semestr-1/PADR/citibike-tripdata/data ??
    #path = "../../../PADR/citibike-tripdata/data"
    #path = "./data/"

    #df = load_data(path, files=['201801-citibike-tripdata.csv', '201807-citibike-tripdata.csv'])
    pass
if __name__ == "__main__":
    main()