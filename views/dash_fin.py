import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as pl
import requests
import os
import sys
import subprocess
import yfinance as yf
import talib as ta



ticker = 'PETR3.SA'
petr3 = yf.Ticker(ticker)
df_petr3 = petr3.history(period='2y')

df = df_petr3
df.reset_index(inplace = True)
pd.to_datetime(df['Date'])


#semanal = df.Date.resample('1W').mean()['Close']
#semanal = semanal.reset_index()


#mensal = df.resample('1M').mean()['Close']
#mensal = mensal.reset_index()


#anual = df.resample('1Y').mean()['Close']
#anual = anual.reset_index()

st.title(ticker, anchor=False)

variacao = df.Close.iloc[-1] / df.Close.iloc[-2]

col1, col2, = st.columns(2)
col1.metric(label="Preço Atual", value=f"R$ {df.Close.iloc[-1]:,.2f}", delta=f"{variacao:,.2f}% variação")
col2.metric(label="Preço Anterior", value=f"R$ {df.Close.iloc[-2]:,.2f}")

st.header(f"Gráfico da evolução do preço", anchor=False)
#filtro de datas

dtinicial = df.Date.min().to_pydatetime()
dtfinal = df.Date.max().to_pydatetime()
intervalo = st.slider( "Selecione o período",
                      min_value=dtinicial,
                      max_value=dtfinal,
                      value=(dtinicial,dtfinal)

)

dados = df
select = df.Date.between(intervalo[0], intervalo[1])
dados = dados[select]



#plotando o gráfico

fig = pl.Figure(data=[pl.Candlestick(x=dados['Date'],
                open=dados['Open'],
                high=dados['High'],
                low=dados['Low'],
                close=dados['Close'])])
fig.update_layout(xaxis_rangeslider_visible=False)



figx = px.line(dados, x='Date',y = 'Close')
figx.update_layout(title = 'Preço da ação')
figx.update_xaxes(title = 'Data')
figx.update_yaxes(title = 'Valor R$')


#filtro de visualização
candle_graf = st.toggle(
    value=False, label="Candle", key="switch_visualization"
)
visual = fig if candle_graf else figx

st.plotly_chart(visual, use_container_width=False, theme="streamlit", key=None, on_select="ignore", selection_mode=('points', 'box', 'lasso'))

#Indicadores financeiros

st.header(f"Análise Técnica", anchor=False)



rsi = ta.RSI(dados['Close'], timeperiod=14)
slowk, slowd = ta.STOCH(dados['High'], dados['Low'], dados['Close'], fastk_period=9, slowk_period=6, slowk_matype=0, slowd_period=6, slowd_matype=0)
fastk, fastd = ta.STOCHF(dados['High'], dados['Low'], dados['Close'], fastk_period=5, fastd_period=3, fastd_matype=0)
fastk1, fastd1 = ta.STOCHRSI(dados['Close'], timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)
macd, macdsignal, macdhist = ta.MACD(dados['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
adx = ta.ADX(dados['High'], dados['Low'], dados['Close'], timeperiod=14)
will = ta.WILLR(dados['High'], dados['Low'], dados['Close'], timeperiod=14)
cci = ta.CCI(dados['High'], dados['Low'], dados['Close'], timeperiod=14)
atr = ta.ATR(dados['High'], dados['Low'], dados['Close'], timeperiod=14)
roc = ta.ROC(dados['Close'], timeperiod=14)
ult = ta.ULTOSC(dados['High'], dados['Low'], dados['Close'], timeperiod1=7, timeperiod2=14, timeperiod3=28)

ema13 = ta.EMA(dados['Close'], timeperiod=13)
min13 = ta.MIN(dados['Close'], timeperiod=13)
max13 = ta.MAX(dados['Close'], timeperiod=13)
bbmin13 = ema13-min13
bbmax13 = ema13-min13

#Calculando Highs /Lows

high = 0

indicadores = pd.DataFrame(
    {
        "Nome": ['1 - RSI(14)', '2 - STOCH(9,6)', '3 - STOCHRSI(14)', '4 - MACD(12,26)', 
                  '5 - ADX(14)', '6 - WILLIANS % R', '7 - CCI(14)', '8 - ATR(14)',
                    '9 - HIGHS/LOWS(14)', '10 - ULT OSCILATOR', '11 - ROC', '12 - BULL BEAR POWER (13)'],

        "Valor": [rsi.iloc[-1], slowd.iloc[-1],  fastk1.iloc[-1], macd.iloc[-1],
                adx.iloc[-1], will.iloc[-1], cci.iloc[-1], atr.iloc[-1], 
                high,  ult.iloc[-1], roc.iloc[-1], bbmin13.iloc[-1]],

        "Ação": ['1', '2', '3', '4','5', '6', '7','8', '9', '10','11', '12']
        
    }
)

#médias móveis

sma5 = ta.SMA(dados['Close'], timeperiod=5)
ema5 = ta.EMA(dados['Close'], timeperiod=5)
sma10 = ta.SMA(dados['Close'], timeperiod=10)
ema10 = ta.EMA(dados['Close'], timeperiod=10)
sma20 = ta.SMA(dados['Close'], timeperiod=20)
ema20 = ta.EMA(dados['Close'], timeperiod=20)
sma50 = ta.SMA(dados['Close'], timeperiod=50)
ema50 = ta.EMA(dados['Close'], timeperiod=50)
sma100 = ta.SMA(dados['Close'], timeperiod=100)
ema100 = ta.EMA(dados['Close'], timeperiod=100)
sma200 = ta.SMA(dados['Close'], timeperiod=200)
ema200 = ta.EMA(dados['Close'], timeperiod=200)

medias = pd.DataFrame(
    {
        "Nome": ['MA5', 'MA10', 'MA20', 'MA50', 'MA100', 'MA200'],
        "Simples": [sma5.iloc[-1], sma10.iloc[-1], sma20.iloc[-1], sma50.iloc[-1], sma100.iloc[-1], sma200.iloc[-1]],
        "Ação S": ['neutro', '--', '--', '--', '--', '--'],
        "Exponencial": [ema5.iloc[-1], ema10.iloc[-1], ema20.iloc[-1], ema50.iloc[-1], ema100.iloc[-1], ema200.iloc[-1]],
        "Ação E": ['neutro', '--', '--', '--', '--', '--']
        
    }
)

st.subheader(f"Médias móveis", anchor=False)
st.dataframe(
    medias,
    hide_index=True,
)

st.subheader(f"Indicadores", anchor=False)
st.dataframe(
    indicadores,
    hide_index=True,
)
