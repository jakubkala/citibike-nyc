import os
import pandas as pd
from tqdm import tqdm


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
                dfs.append(pd.read_csv(os.path.join(self.path, filename)))
        else:
            for filename in tqdm(os.listdir(self.path)):
                if 'citibike-tripdata.csv' in filename:
                    dfs.append(pd.read_csv(os.path.join(self.path, filename)))

        self.data = pd.concat(dfs)

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

def main():
    pass

if __name__ == "__main__":
    main()