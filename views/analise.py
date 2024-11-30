import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from models.DataAccess_class import DataAccess

consultor = DataAccess()

df1 = pd.read_csv('data/producao_e_consumo.csv', skiprows=4, sep=',')
df2 = pd.read_csv('data/estoque.csv', skiprows=4, sep=',')
df3 = pd.read_csv('data/balanco_estoque.csv', skiprows=4, sep=',')


df1['Month'] = pd.to_datetime(df1['Month'])
df2['Month'] = pd.to_datetime(df2['Month'])
df3['Month'] = pd.to_datetime(df3['Month'])
df_analise_historica = consultor.get_brent_data()
df_analise_historica['ds'] = pd.to_datetime(df_analise_historica['ds'])

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
    
st.subheader(f"Veja o impacto desses fatores nos principais períodos de oscilação do preço do petróleo Brent", divider='gray')

dados = df_analise_historica
option_map = {
    0: "1990-1991",
    1: "2003-2008",
    2: "2008-2009",
    3: "2014-2016",
    4: "2020-2022"
}
selection = st.segmented_control(
    "Selecione o período para saber mais",
    options=option_map.keys(),
    format_func=lambda option: option_map[option],
    selection_mode="single",
)

titulo=''
resumo=''
if selection == 0:
    select = df_analise_historica.ds.between('1990-01-01', '1991-12-31')
    dados = dados[select]
    titulo = 'Guerra do Golfo'
    resumo = 'A invasão do Kuwait pelo Iraque em agosto de 1990 levou a um aumento abrupto nos preços do petróleo, que ultrapassaram US$ 40 por barril, devido ao temor de interrupções no fornecimento.'

if selection == 1:
    select = df_analise_historica.ds.between('2003-01-01', '2008-12-31')
    dados = dados[select]
    titulo = 'Crise Energética'
    resumo = 'A crescente demanda de países como China e Índia, aliada a tensões no Oriente Médio, resultou em uma escalada nos preços do petróleo, que atingiram um pico histórico de US$ 147 por barril em julho de 2008. '

if selection == 2:
    select = df_analise_historica.ds.between('2008-01-01', '2009-12-31')
    dados = dados[select]
    titulo = 'Crise Financeira Global'
    resumo = 'A crise financeira de 2008 provocou uma queda acentuada na demanda por petróleo, fazendo com que os preços despencassem de US$ 147 em julho de 2008 para cerca de 32 dolares por barril em dezembro do mesmo ano.'

if selection == 3:
    select = df_analise_historica.ds.between('2014-01-01', '2016-12-31')
    dados = dados[select]
    titulo = 'Produção Exacerbada'
    resumo = 'Um aumento na produção de petróleo de xisto nos Estados Unidos e a decisão da OPEP de não reduzir a produção levaram a um excesso de oferta, resultando em uma queda nos preços de mais de 70% entre 2014 e 2016.'

if selection == 4:
    select = df_analise_historica.ds.between('2019-07-01', '2021-12-31')
    dados = dados[select]
    titulo = 'Pandemia Covid-19'
    resumo = 'A pandemia causou uma redução drástica na demanda global por petróleo, levando os preços a níveis historicamente baixos. Em abril de 2020, os contratos futuros do WTI chegaram a ser negociados em valores negativos pela primeira vez na história.'

#plotando o gráfico

fig = px.line(dados, x='ds',y = 'y')
fig.update_layout(title = titulo)
fig.update_xaxes(title = 'Data')
fig.update_yaxes(title = 'Preço Petróleo Brent US$')

st.plotly_chart(fig, use_container_width=False, theme="streamlit", key=None, on_select="ignore", selection_mode=('points', 'box', 'lasso'))
with st.expander("Mostrar / Ocultar - Explicação"):
    st.write(resumo)



########################### CÓDIGO PARA COLOCAR NO FINAL DA PÁGINA 'DASHBOARD IPEA' ##########################

#st.header(f"Impacto de eventos atuais", divider='gray')
st.subheader(f"Impacto de eventos atuais - Reeleição de Donald Trump")

st.write("A eleição de Donald Trump em 2024 gerou expectativas de mudanças significativas no mercado de petróleo bruto após sua posse em 2025. Analistas preveem que as políticas energéticas propostas por Trump possam impactar os preços do petróleo.")

st.image("https://s2-g1.glbimg.com/_rSWXGSgqWm6tTtlZWnHM5NpMqQ=/0x0:5900x3935/1008x0/smart/filters:strip_icc()/i.s3.glbimg.com/v1/AUTH_59edd422c0c84a879bd37670ae4f538a/internal_photos/bs/2024/1/G/7BXzf1T1AIqTD4nmPA4g/rc2hsaapm3bo-carlos-barria-reuters.jpg"
            ,width=600,caption="Donald Trump reeleito como presidente dos EUA")

expl = "Durante seu primeiro mandato com inicio em 2018, Trump apoiou expansão da produção doméstica de petróleo e gás. Como resultado, a produção de petróleo dos EUA atingiu recordes, transformando o país em um dos maiores exportadores globais. Esse aumento na oferta pressionou os preços para baixo, principalmente em períodos de menor demanda global."
with st.expander("Impacto da primeira eleição de Trump em 2017"):
    st.write(expl)
    dados = df_analise_historica
    select = df_analise_historica.ds.between('2018-01-01', '2021-12-31')
    dados = dados[select]
    fig = px.line(dados, x='ds',y = 'y')
    fig.update_layout(title = 'Oscilação do preço do petróleo durante o primeiro mandato de Trump')
    fig.update_xaxes(title = 'Data')
    fig.update_yaxes(title = 'Preço Petróleo Brent US$')
    st.plotly_chart(fig, use_container_width=False, theme="streamlit", key=None, on_select="ignore", selection_mode=('points', 'box', 'lasso'))

with st.expander("Cenário esperado para próxima eleição"):
    st.write("O cenário esperado para o próximo ano não será muito diferente:")
    st.write("Aumento na oferta: Trump prometeu expandir a produção de petróleo nos EUA, o que pode criar excedentes no mercado.")
    st.write("Demanda global fraca: Especialmente com o enfraquecimento econômico em regiões como a China, reduzindo a pressão sobre os preços.")
    st.write("Flexibilização fiscal: Incentivos aos combustíveis fósseis podem estimular mais produção, pressionando ainda mais os preços.")