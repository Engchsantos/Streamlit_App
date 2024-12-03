import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from models.DataAccess_class import DataAccess
from controllers.Dashboard_controller import Dashboard_controller

consultor = DataAccess()
controller = Dashboard_controller()

df = consultor.get_brent_data()

df = controller.ajust_data(df=df)

diario = df.copy()
semanal = controller.calcula_semanal(df)
mensal = controller.calcula_mensal(df)
anual = controller.calcula_anual(df)

df_temporal = []
df_temporal.append(diario)
df_temporal.append(semanal)
df_temporal.append(mensal)
df_temporal.append(anual)

df_prod_consumo = pd.read_csv('data/prod_consumo.csv', sep=',', skiprows=4)
df_prod_consumo.columns = ('mes', 'producao', 'consumo')
df_prod_consumo['mes'] = pd.to_datetime(df_prod_consumo['mes'])
df_prod_consumo_passado = df_prod_consumo[df_prod_consumo['mes']<='2023-12-01']
df_prod_consumo_futuro = df_prod_consumo[df_prod_consumo['mes']>='2024-11-01']

st.title(f"Petróleo Brent", anchor=False)
st.text("Esta tela apresenta uma análise financeira detalhada do petróleo Brent, com dados históricos e insights gráficos sobre tendências de preços, variações semanais e indicadores-chave. Explore visualizações interativas para acompanhar o desempenho do mercado e tomar decisões informadas com base em dados atualizados.")

# Filtros
st.subheader("Filtros:", anchor=False)
option_map = {
    0: "Dia",
    1: "Sem",
    2: "Mes",
    3: "Ano",
}
selection = st.segmented_control(
    "Sazonalidade:",
    options=option_map.keys(),
    format_func=lambda option: option_map[option],
    selection_mode="single",
    default=0
)

dtinicial = pd.to_datetime('2020-01-01').to_pydatetime()
dtfinal = df.ds.max().to_pydatetime()
intervalo = st.slider( "Selecione o período",
                      min_value=dtinicial,
                      max_value=dtfinal,
                      value=(dtinicial,dtfinal)

)
if selection is None:
    select = df_temporal[0].ds.between(intervalo[0], intervalo[1])
    df_filtered = df_temporal[0][select].sort_values(by='ds', ascending=False).reset_index(drop=True)
else:
    select = df_temporal[selection].ds.between(intervalo[0], intervalo[1])
    df_filtered = df_temporal[selection][select].sort_values(by='ds', ascending=False).reset_index(drop=True)

evolucao_temporal = df_filtered.copy()
volatilidade = controller.calcula_volatilidade(df_filtered)



#plotando o gráfico
st.subheader(f"Gráfico da evolução do preço", anchor=False)
variacao = controller.calcula_variacao(evolucao_temporal)
col1, col2, = st.columns(2)
col1.metric(label="Preço Atual", value=f"US$ {evolucao_temporal.y[0]:,.2f}", delta=f"{variacao:,.2f}% variação")
col2.metric(label="Preço Anterior", value=f"US$ {evolucao_temporal.y[1]:,.2f}")
cambio_dolar = controller.prepara_cambio(dts=evolucao_temporal['ds'])
fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=evolucao_temporal['ds'],
        y=evolucao_temporal['y'],
        mode='lines+markers',
        name='Brent Price (USD)',
        line=dict(color='blue')
    )
)
fig.add_trace(
    go.Scatter(
        x=cambio_dolar['data'],
        y=cambio_dolar['valor'],
        mode='lines+markers',
        name='USD/BRL',
        line=dict(color='green'),
        yaxis='y2'
    )
)
fig.update_layout(
    title='Preço do Brent e Cotação do Dólar (USD/BRL)',
    xaxis=dict(title='Date'),
    yaxis=dict(
        title='Brent Price (USD)',
        titlefont=dict(color='blue'),
        tickfont=dict(color='blue')
    ),
    yaxis2=dict(
        title='USD/BRL',
        titlefont=dict(color='green'),
        tickfont=dict(color='green'),
        overlaying='y',
        side='right'
    ),
    legend=dict(x=0, y=1),
    hovermode='x'
)
st.plotly_chart(fig)

#plotando o gráfico
st.subheader(f"Gráfico da evolução da volatilidade", anchor=False)
volatilidade_total = volatilidade['vol'].std()
col1, = st.columns(1)
col1.metric(label="Volatilidade", value=f"US$ {volatilidade_total:,.2f}")
fig = px.line(volatilidade, x='ds',y = 'vol')
fig.update_layout(title = 'Preço do Petróleo Brent')
fig.update_xaxes(title = 'Data')
fig.update_yaxes(title = 'Valor US$')
st.plotly_chart(fig, use_container_width=False, theme="streamlit", key='volatilidades', on_select="ignore", selection_mode=('points', 'box', 'lasso'))


fig8 = go.Figure()
fig8.add_trace(go.Scatter(x=df_prod_consumo_futuro['mes'], y=df_prod_consumo_futuro['producao'],
                    mode='lines',
                    name='Produção'))
fig8.add_trace(go.Scatter(x=df_prod_consumo_futuro['mes'], y=df_prod_consumo_futuro['consumo'],
                    mode='lines',
                    name='Consumo'))
fig8.update_layout(title = 'Previsão de Oferta e Demanda')
fig8.update_yaxes(title = 'Quantidade - milhões de barris')



st.plotly_chart(fig8, use_container_width=False, theme="streamlit", key=None, on_select="ignore", selection_mode=('points', 'box', 'lasso'))
st.markdown("<p style='text-align: center; color:gray; font-size:12px'>Fonte: U.S. Energy Information Administration (EIA)</p>",  unsafe_allow_html=True)