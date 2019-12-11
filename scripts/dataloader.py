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

def main():
    #~/IAD/semestr-1/PADR/citibike-tripdata/data ??
    #path = "../../../PADR/citibike-tripdata/data"
    #path = "./data/"

    df = load_data(path, files=['201801-citibike-tripdata.csv', '201807-citibike-tripdata.csv'])
    
if __name__ == "__main__":
    main()