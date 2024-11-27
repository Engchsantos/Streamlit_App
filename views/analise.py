import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df1 = pd.read_csv('data/producao_e_consumo.csv', skiprows=4, sep=',')
df2 = pd.read_csv('data/estoque.csv', skiprows=4, sep=',')
df3 = pd.read_csv('data/balanco_estoque.csv', skiprows=4, sep=',')


df1['Month'] = pd.to_datetime(df1['Month'])
df2['Month'] = pd.to_datetime(df2['Month'])
df3['Month'] = pd.to_datetime(df3['Month'])







st.title('Análise: Principais Influenciadores no Preço do Petróleo Brent')


st.markdown("<br></br><p style='text-align: center; color:red; font-size:50px'>O que você precisa saber:</p><br></br>",  unsafe_allow_html=True)



st.markdown(
        "<p style='text-align: justify; color:gray; font-size:25px'><b>O preço do petróleo Brent,\
              um benchmark global crucial para o mercado de petróleo, é determinado por uma complexa\
              interação de diversos fatores. Embora a dinâmica fundamental de oferta e demanda seja\
              o motor primário a longo prazo, forças externas e expectativas de mercado exercem uma\
              influência considerável, muitas vezes causando flutuações significativas e imprevisíveis\
             nos preços. </b></p>",  unsafe_allow_html=True
    )

st.markdown(
        "<p style='text-align: justify; color:gray; font-size:25px'>Alguns fatores se destacam como os maiores influenciadores: a dinâmica da oferta\
     e da demanda, os eventos geopolíticos e o risco inerente, a política de produção (tanto da OPEP quanto de outros grandes produtores), \
     níveis de estoques e a capacidade de armazenamento, e finalmente, as expectativas do mercado e a especulação. A compreensão da interação desses fatores é crucial\
      para analisar as tendências e as flutuações nos preços do petróleo Brent.</p>",  unsafe_allow_html=True
    )


st.subheader('Dinâmica de Oferta e Demanda:')

with st.expander("Mostrar / Ocultar - Explicação"):
    st.markdown(
            "<p style='text-align: justify; color:gray; font-size:14px'>Este é o princípio fundamental que rege o preço do petróleo Brent. Um aumento na demanda global por petróleo, impulsionado por crescimento econômico robusto em países como China e Índia, ou por um inverno rigoroso no Hemisfério Norte aumentando a demanda por aquecimento, levará a uma pressão de alta nos preços. Inversamente, uma queda na demanda global, como resultado de uma recessão econômica ou de uma adoção mais rápida de energias renováveis, causará uma pressão de baixa nos preços. Por exemplo, a pandemia de COVID-19 em 2020 levou a uma queda drástica na demanda global por petróleo, resultando em um colapso dos preços, mesmo com cortes na produção. Já um crescimento econômico vigoroso, especialmente em países emergentes, tende a aumentar a demanda e pressionar os preços para cima.</p>",  unsafe_allow_html=True
        )


fig = go.Figure()
fig.add_trace(go.Scatter(x=df1['Month'], y=df1['Total World Petroleum Production million barrels per day'],
                    mode='lines',
                    name='Produção'))
fig.add_trace(go.Scatter(x=df1['Month'], y=df1['Total World Petroleum Consumption million barrels per day'],
                    mode='lines+markers',
                    name='Consumo'))
fig.update_layout(title = 'Variação da Produção e Consumo Mundial de Petróleo')
fig.update_yaxes(title = 'Quantidade - mb/dia')


st.plotly_chart(fig, use_container_width=False, theme="streamlit", key=None, on_select="ignore", selection_mode=('points', 'box', 'lasso'))



st.subheader('Eventos Geopolíticos e Risco:')

with st.expander("Mostrar / Ocultar - Explicação"):
    st.markdown(
            "<p style='text-align: justify; color:gray; font-size:14px'>Eventos geopolíticos imprevisíveis podem causar flutuações significativas e repentinas nos preços do petróleo. Guerras, sanções internacionais, instabilidade política em países produtores importantes ou ameaças terroristas em instalações petrolíferas podem interromper o fornecimento de petróleo, reduzindo a oferta e levando a um aumento acentuado dos preços. Por exemplo, a invasão russa da Ucrânia em 2022 levou a temores de interrupções no fornecimento de energia da Rússia, resultando em um aumento significativo no preço do petróleo. Contrariamente, um acordo de paz ou uma redução da tensão geopolítica pode levar a uma queda nos preços, pois o mercado percebe um menor risco de interrupção no fornecimento.</p>",  unsafe_allow_html=True
        )


st.subheader('Política de Produção (OPEP e outros):')

with st.expander("Mostrar / Ocultar - Explicação"):
    st.markdown(
        "<p style='text-align: justify; color:gray; font-size:14px'>A produção de petróleo pelos países da OPEP e pelos grandes produtores não-OPEP desempenha um papel crucial na oferta global. Acordos da OPEP para reduzir a produção, muitas vezes para apoiar os preços, podem levar a um aumento nos preços do petróleo. A Arábia Saudita, por exemplo, frequentemente atua como um regulador, ajustando sua produção para influenciar os preços de mercado. Entretanto, se a OPEP aumentar a produção, ou se grandes produtores não-OPEP aumentarem sua produção de forma significativa (como ocorreu com os EUA no passado), a oferta aumenta, pressionando os preços para baixo. A cooperação entre a OPEP e países não-OPEP é crucial, e a falta de coordenação pode levar a flutuações abruptas nos preços.</p>",  unsafe_allow_html=True
        )


st.subheader('Níveis de Estoques e Capacidade de Armazenamento:')

with st.expander("Mostrar / Ocultar - Explicação"):
    st.markdown(
            "<p style='text-align: justify; color:gray; font-size:14px'>Os níveis de estoques de petróleo bruto e produtos refinados em todo o mundo atuam como um amortecedor para as flutuações de preços. Grandes estoques geralmente indicam uma oferta abundante, pressionando os preços para baixo. Baixos níveis de estoques podem levar a preocupações com escassez e podem aumentar os preços, mesmo com uma oferta estável. A capacidade de armazenamento também é um fator importante; se os estoques se aproximam da capacidade máxima, isso pode criar uma pressão adicional de baixa nos preços. Inversamente, se os níveis de estoques caírem abaixo de um certo nível considerado confortável, pode gerar preocupações sobre uma oferta insuficiente, impulsionando os preços.</p>",  unsafe_allow_html=True
        )

fig4 = go.Figure()
fig4.add_trace(go.Scatter(x=df2['Month'], y=df2['OECD Commercial Inventory million barrels'],
                    mode='lines',
                    name='Estoque'))
fig4.update_layout(title = 'Níveis mundial de estoque de petróleo')
fig4.update_yaxes(title = 'Quantidade - milhões de barris')



st.plotly_chart(fig4, use_container_width=False, theme="streamlit", key=None, on_select="ignore", selection_mode=('points', 'box', 'lasso'))

st.subheader('Expectativas do Mercado e Especulação:')
with st.expander("Mostrar / Ocultar - Explicação"):
    st.markdown(
            "<p style='text-align: justify; color:gray; font-size:14px'>As expectativas dos investidores e traders sobre futuros eventos, como mudanças na demanda ou na política de produção, podem influenciar significativamente os preços do petróleo. A especulação, particularmente no mercado de futuros, pode levar a grandes flutuações de preços, independentemente dos fundamentos de oferta e demanda. Notícias positivas sobre o crescimento econômico ou sobre novas tecnologias de energias renováveis podem levar a um aumento nos preços devido ao aumento da demanda esperada. Por outro lado, noticias negativas sobre a economia ou sobre um possível aumento significativo na oferta de petróleo no futuro podem levar os traders a venderem contratos futuros, causando uma queda nos preços, mesmo que a oferta e a demanda atuais permaneçam inalteradas.</p>",  unsafe_allow_html=True
        )