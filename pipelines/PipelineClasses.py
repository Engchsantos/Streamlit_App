import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class PrepareData(BaseEstimator, TransformerMixin):
    def __init__(self, feature_to_datatime='Data', feature_to_replace='Preço - petróleo bruto - Brent (FOB)'):
        self.feature_to_datatime = feature_to_datatime
        self.feature_to_replace = feature_to_replace
    
    def fit(self, df):
        return self
    
    def transform(self, df):
        df[self.feature_to_datatime] = pd.to_datetime(df[self.feature_to_datatime], format="%Y-%m-%d")
        df.set_index(self.feature_to_datatime, inplace=True)
        #df[self.feature_to_replace] = df[self.feature_to_replace].str.replace(',', '.').astype(float)
        df.dropna(inplace=True)
        df.sort_index(inplace=True, ascending=False)
        return df

class FillNANValues(BaseEstimator, TransformerMixin):
    def __init__(self, feature_to_fill='Preço - petróleo bruto - Brent (FOB)'):
        self.feature_to_fill = feature_to_fill
    
    def fit(self, df):
        return self
    
    def transform(self, df):
        df.sort_index(inplace=True, ascending=False)
        start_date = df.index[len(df.index) -1]
        end_date = df.index[0]
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        df = df.reindex(date_range)
        media_movel = df[self.feature_to_fill].rolling(window=30, min_periods=1).mean()
        df[self.feature_to_fill] = df[self.feature_to_fill].combine_first(media_movel)
        df = df[self.feature_to_fill].dropna()
        df.columns = ['ds', 'y']
        return df

class SomthDataIntervalValues(BaseEstimator, TransformerMixin):
    def __init__(self):
       return
    
    def fit(self, df):
        return self
    
    def transform(self, df):
        df = np.log(df) #escala logarítmica
        ma_log = df.rolling(7).mean() #média móvel
        df = (df - ma_log).dropna() #diferenciação
        df = pd.DataFrame(df)
        df['MA'] = ma_log
        df.sort_index(inplace=True, ascending=False)
        return df