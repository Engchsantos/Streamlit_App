import pandas as pd
import yfinance as yf
import numpy as np

class Dashboard_controller:
    def __init__(self):
        pass

    def ajust_data(self, df):
        df['ds'] = pd.to_datetime(df['ds'])
        return df

    def calcula_semanal(self, df):
        semanal = df.set_index('ds').resample('1W').mean()['y']
        semanal = semanal.reset_index()
        return semanal

    def calcula_mensal(self, df):
        mensal = df.set_index('ds').resample('1M').mean()['y']
        mensal = mensal.reset_index()
        return mensal

    def calcula_anual(self, df):
        anual = df.set_index('ds').resample('1Y').mean()['y']
        anual = anual.reset_index()
        return anual

    def calcula_variacao(self, df):
        return ((df.y[0] - df.y[1]) / df.y[1]) * 100

    def calcula_volatilidade(self, df):
        df['vol'] = df['y'].pct_change()
        return df
    
    def prepara_cambio(self, dts):
        result = yf.download('USDBRL=X', start=dts.min(), end=dts.max(), interval='1d')
        cambio = result['Close'].sort_index(ascending=False).reset_index()
        cambio.rename(columns={'Date': 'data', 'USDBRL=X': 'valor'}, inplace=True)
        cambio['data'] = pd.to_datetime(cambio['data']).dt.tz_localize(None)
        df_cambio = pd.DataFrame({
            'data': pd.date_range(start=dts.min(), end=dts.max())
        })
        df_cambio = df_cambio.merge(cambio, how='left', on='data')
        df_cambio['valor'] = df_cambio['valor'].interpolate(method='linear')
        df_cambio['valor'] = df_cambio['valor'].fillna(method='bfill')
        df_retorno = pd.DataFrame({
            'data': pd.to_datetime(dts).dt.tz_localize(None)
        })
        df_retorno = df_retorno.merge(df_cambio, how='left', on='data')
        df_retorno['valor'] = df_retorno['valor'].interpolate(method='linear')
        df_retorno['valor'] = df_retorno['valor'].fillna(method='bfill')
        print(df_retorno)
        return df_retorno