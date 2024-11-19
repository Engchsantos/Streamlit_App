import pandas as pd

class DataAccess:
    def __init__(self):
        pass

    def get_brent_data(self):
        return pd.read_csv('data/df.csv')