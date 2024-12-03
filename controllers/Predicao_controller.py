import pandas as pd
import numpy as np
from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
from pipelines.PipelineClasses import PrepareData, FillNANValues, SomthDataIntervalValues
from sklearn.pipeline import Pipeline
import io

class Predicao_controller:
    def __init__(self):
        pass
    
    def to_excel(self, df):
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        processed_data = output.getvalue()
        return processed_data

    def calcula_erro(self, predicao, real, modelo):
        def symetric_mean_absolute_percentage_error(actual, predicted) -> float:
            return round( 
                np.mean( 
                    np.abs(predicted - actual) / 
                    ((np.abs(predicted) + np.abs(actual))/2) 
                )*100, 2
            )
            
        mae = mean_absolute_error(real, predicao)
        rmse = mean_squared_error(real, predicao)
        smape = symetric_mean_absolute_percentage_error(real, predicao)
        retorno = {
            'modelo': modelo,
            'mae': mae,
            'rmse': rmse,
            'smape %': smape
        }

        return retorno

    def process_pipeline_normalize_data(self, df):
        pipeline = Pipeline([
            ('data_prepator', PrepareData()),
            ('filler_nan_values', FillNANValues())
        ])
        df_pipeline = pipeline.fit_transform(df)
        return df_pipeline
    
    def realiza_predicao(self, df, tam_previsao=15, recorte_arima=365):

        def process_pipeline_arima(df):
            pipeline = Pipeline([
                ('data_prepator', PrepareData()),
                ('filler_nan_values', FillNANValues()),
                ('smother_data_interval', SomthDataIntervalValues())
            ])
            df_pipeline = pipeline.fit_transform(df)
            return df_pipeline
        
        def predicao_arima(df, tam_previsao, recorte_arima):
            df_pipeline = process_pipeline_arima(df.copy()).head(recorte_arima)
            df_arima = df_pipeline['Preço - petróleo bruto - Brent (FOB)'].reset_index()
            df_arima = df_arima.reset_index()
            df_arima['unique_id'] = 'Brent'
            df_arima.rename(columns={'index': 'ds', 'Preço - petróleo bruto - Brent (FOB)': 'y', 'unique_id': 'unique_id'}, inplace=True)
            df_arima = df_arima[['ds', 'y', 'unique_id']]

            model_a = StatsForecast(models=[AutoARIMA(season_length=7)], freq='D', n_jobs=-1) #instância
            model_a.fit(df_arima) #treinamento

            #Predições de teste
            forecast_dfa = model_a.predict(h=tam_previsao, level=[90])
            forecast_dfa.dropna(inplace=True)

            #preparação dos dados para plotagem
            valores_reais = self.process_pipeline_normalize_data(df.copy())[-7:]
            valores = pd.Series()
            for prediction in forecast_dfa.values:
                df_log = np.log(valores_reais) #escala logarítmica
                ma_log = df_log.rolling(7).mean() #média móvel
                valor = np.exp(prediction[1] + ma_log.iloc[-1])
                valores_reais = valores_reais[1:]
                valores_reais = pd.concat([valores_reais, pd.Series([valor])])
                valores = pd.concat([valores, pd.Series([valor])])
            dados_arima = forecast_dfa
            dados_arima['data'] = dados_arima['ds']
            dados_arima = dados_arima.set_index('ds')
            dados_arima['AutoARIMA_result_static'] = np.exp(dados_arima['AutoARIMA'] + df_pipeline['MA'].head(1).values[0])
            dados_arima['AutoARIMA_result_dynamic'] = valores.values
            dados_arima['AutoARIMA_result_mean'] = (dados_arima['AutoARIMA_result_dynamic'].values + dados_arima['AutoARIMA_result_static'].values)/2
            
            #salva dados de previsão para uso do tensorflow
            previsao_arima = pd.DataFrame(dados_arima['AutoARIMA_result_mean'].reset_index())
            previsao_arima.rename(columns={'AutoARIMA_result_mean': 'y'}, inplace=True)
            return previsao_arima

        def predicao_LSTM(df, previsao_arima, tam_previsao):
            df_tensorflow_arima = self.process_pipeline_normalize_data(df.copy())
            df_tensorflow_arima = pd.DataFrame(df_tensorflow_arima)
            df_tensorflow_arima.reset_index(inplace=True)
            df_tensorflow_arima.rename(columns={'index': 'ds', 'Preço - petróleo bruto - Brent (FOB)': 'y'}, inplace=True)
            df_tensorflow_arima = df_tensorflow_arima[['ds', 'y']]
            df_arima_tf = pd.concat([df_tensorflow_arima.copy()[['ds', 'y']], previsao_arima], axis=0)
            df_tensorflow = df_arima_tf.copy()
            df_tensorflow['ds'] = pd.to_datetime(df_tensorflow['ds'])

            # Ordenar por data
            df_tensorflow = df_tensorflow.sort_values('ds')

            # Resetar o índice
            df_tensorflow.reset_index(drop=True, inplace=True)

            # Normalizar os dados
            scaler = MinMaxScaler(feature_range=(0, 1))
            scaled_data = scaler.fit_transform(df_tensorflow[['y']])

            # Função para criar sequências de dados
            def create_sequences(data, seq_length):
                sequences = []
                labels = []
                for i in range(len(data) - seq_length):
                    seq = data[i:i + seq_length]
                    label = data[i + seq_length]
                    sequences.append(seq)
                    labels.append(label)
                return np.array(sequences), np.array(labels)

            # Definir o tamanho da sequência
            seq_length = 7

            # Criar sequências de treino
            X, y = create_sequences(scaled_data, seq_length)
            X_train, y_train = X[:-tam_previsao], y[:-tam_previsao]
            X_predict, y_predict = X[-tam_previsao:], y[-tam_previsao:]

            # Construir o modelo LSTM
            model = Sequential()
            model.add(LSTM(units=50, return_sequences=True, input_shape=(seq_length, 1)))
            model.add(LSTM(units=50))
            model.add(Dense(1))

            model.compile(optimizer='adam', loss='mean_absolute_error')

            # Treinar o modelo
            model.fit(X_train, y_train, epochs=20, batch_size=64)

            # Fazer predições
            predicted_prices = model.predict(X_predict)

            # Desnormalizar os dados
            predicted_prices = scaler.inverse_transform(predicted_prices)

            return predicted_prices
        
        df_predicao_arima = predicao_arima(df, tam_previsao=tam_previsao, recorte_arima=recorte_arima)
        df_predicao_final = predicao_LSTM(df, df_predicao_arima, tam_previsao=tam_previsao)

        return df_predicao_final
