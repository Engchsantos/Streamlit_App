import pandas as pd

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