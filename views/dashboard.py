import streamlit as st
import pandas as pd
import plotly.express as px
from models.DataAccess_class import DataAccess
from controllers.Dashboard_controller import Dashboard_controller

consultor = DataAccess()
controller = Dashboard_controller()

df = consultor.get_brent_data()

df = controller.ajust_data(df=df)

diario = df.copy()
semanal = controller.calcula_semanal(df)
mensal = controller.calcula_semanal(df)
anual = controller.calcula_semanal(df)

df_temporal = []
df_temporal.append(diario)
df_temporal.append(semanal)
df_temporal.append(mensal)
df_temporal.append(anual)

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
    default=0
)

select = df_temporal[selection].ds.between(intervalo[0], intervalo[1])
dados = df_temporal[selection][select]



#plotando o gráfico
fig = px.line(dados, x='ds',y = 'y')
fig.update_layout(title = 'Preço do Petróleo Brent')
fig.update_xaxes(title = 'Data')
fig.update_yaxes(title = 'Valor US$')

st.plotly_chart(fig, use_container_width=False, theme="streamlit", key=None, on_select="ignore", selection_mode=('points', 'box', 'lasso'))