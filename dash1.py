import streamlit as st
import pandas as pd
import plotly.express as px


df = pd.read_csv('data/df.csv')

df['ds'] = pd.to_datetime(df['ds'])

semanal = df.set_index('ds').resample('1W').mean()['y']
semanal = semanal.reset_index()


mensal = df.set_index('ds').resample('1M').mean()['y']
mensal = mensal.reset_index()


anual = df.set_index('ds').resample('1Y').mean()['y']
anual = anual.reset_index()

st.title(f"Petróleo Brent", anchor=False)

variacao = df.y[0] / df.y[1]

col1, col2, = st.columns(2)
col1.metric(label="Preço Atual", value=f"US$ {df.y[0]:,.2f}", delta=f"{variacao:,.2f}% variação")
col2.metric(label="Preço Anterior", value=f"US$ {df.y[1]:,.2f}")

st.header(f"Gráfico da evolução do preço", anchor=False)
#filtro de datas

dtinicial = df.ds.min().to_pydatetime()
dtfinal = df.ds.max().to_pydatetime()
intervalo = st.slider( "Selecione o período",
                      min_value=dtinicial,
                      max_value=dtfinal,
                      value=(dtinicial,dtfinal)

)

dados = df
select = df.ds.between(intervalo[0], intervalo[1])
dados = dados[select]


#filtro de visualização

option_map = {
    0: "Dia",
    1: "Sem",
    2: "Mes",
    3: "Ano",
}
selection = st.segmented_control(
    "Visualização",
    options=option_map.keys(),
    format_func=lambda option: option_map[option],
    selection_mode="single",
)

if selection == 0:

    dados = df
    select = df.ds.between(intervalo[0], intervalo[1])
    dados = dados[select]

if selection == 1:

    dados = semanal
    select = semanal.ds.between(intervalo[0], intervalo[1])
    dados = dados[select]

if selection == 2:

    dados = mensal
    select = mensal.ds.between(intervalo[0], intervalo[1])
    dados = dados[select]

if selection == 3:

    dados = anual
    select = anual.ds.between(intervalo[0], intervalo[1])
    dados = dados[select]



#plotando o gráfico


fig = px.line(dados, x='ds',y = 'y')
fig.update_layout(title = 'Preço do Petróleo Brent')
fig.update_xaxes(title = 'Data')
fig.update_yaxes(title = 'Valor US$')

st.plotly_chart(fig, use_container_width=False, theme="streamlit", key=None, on_select="ignore", selection_mode=('points', 'box', 'lasso'))
