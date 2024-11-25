import streamlit as st
from streamlit_js_eval import streamlit_js_eval
import pandas as pd
import plotly.express as px
from controllers.Predicao_controller import Predicao_controller
from models.DataAccess_class import DataAccess

reader = DataAccess()
predicter = Predicao_controller()

# Função para carregar e processar os dados com cache
@st.cache_data
def carregar_dados():
    data = reader.get_brent_data().head(1095)  # 3 anos
    data.columns = ['Data', 'Preço - petróleo bruto - Brent (FOB)']
    dados_trabalhados = predicter.process_pipeline_normalize_data(data.copy()).reset_index(name='Preço - petróleo bruto - Brent (FOB)')
    dados_trabalhados.rename(columns={'index': 'Data'}, inplace=True)
    return dados_trabalhados

# Função para calcular a validação do modelo com cache
@st.cache_data
def calcular_validacao(dados_trabalhados):
    df_validacao = pd.DataFrame(predicter.realiza_predicao(dados_trabalhados.copy().head(1080)), columns=['valor'])
    df_validacao['data'] = dados_trabalhados.copy().tail(15)['Data'].values
    df_validacao['data'] = pd.to_datetime(df_validacao['data']).dt.date
    df_validacao['valor_real'] = dados_trabalhados.copy().tail(15)['Preço - petróleo bruto - Brent (FOB)'].values
    df_validacao['valor_predito'] = df_validacao['valor'].map("{:.4f}".format).astype('float64')
    erros = predicter.calcula_erro(predicao=df_validacao['valor_predito'], real=df_validacao['valor_real'], modelo='ARIMA + LSTM')
    return df_validacao, erros

# Função para realizar a predição futura com cache
@st.cache_data
def calcular_predicao_futura(dados_trabalhados):
    start_date = pd.to_datetime(dados_trabalhados['Data'].iloc[-1])
    datas = pd.date_range(start=start_date, periods=16, freq='D')  # 15 dias de previsão
    df_predicao = pd.DataFrame(predicter.realiza_predicao(dados_trabalhados.copy()), columns=['valor'])
    df_predicao['data'] = datas[1:]
    df_predicao['data'] = pd.to_datetime(df_predicao['data']).dt.date
    df_predicao['valor'] = df_predicao['valor'].map("{:.4f}".format).astype('Float64')
    return df_predicao

@st.cache_data
def plota_info_inicial(dados_trabalhados):#informações iniciais
    ultima_atualizacao = dados_trabalhados['Data'].iloc[-1].date()
    st.title("Predição do Petróleo Brent")
    st.markdown(
        f"<p style='font-size: 14px; color: gray;'><em>Última atualização da base: {ultima_atualizacao}</em></p>", 
        unsafe_allow_html=True
    )
    st.markdown("""
        Nesta página, você encontrará análises detalhadas para apoiar suas decisões de investimento no mercado de petróleo. Apresentamos:

        - **Validação do Modelo:** Inclui cálculos de erro e gráficos comparativos entre os valores reais e previstos, permitindo avaliar a precisão do modelo.
        - **Predições Futuras:** Uma tabela (download) e um gráfico projetam os valores futuros do petróleo Brent com base em nosso modelo de predição.

        Use essas informações para obter insights valiosos e acompanhar as tendências do mercado com confiança. Caso tenha dúvidas ou precise de suporte, entre em contato com nossa equipe.
        """)
    
@st.cache_data    
def plota_info_validacao(df_validacao, erros):#Plota os dados de validação de performance do modelo
    with st.expander("Mostrar/Esconder - Dados de performance do modelo"):
        st.subheader("Performance do modelo")
        st.text("""Analise o desempenho do modelo com base nos últimos 15 dias de dados. Essa avaliação permite observar como o modelo se comporta ao realizar previsões comparáveis aos valores reais. Utilize essa validação para determinar a confiabilidade do modelo em cenários similares. Caso os cálculos de erro ultrapassem os limites aceitáveis, recomendamos entrar em contato com a equipe de cientistas de dados para revisar e ajustar o modelo, garantindo maior precisão nas previsões futuras.""")
        st.markdown("#### Tabela de Erros")
        st.table(erros)
        fig = px.line(
            df_validacao,
            x="data",
            y=["valor_predito", "valor_real"],
            labels={"value": "Valor", "data": "Data"},
            title="Comparação: Predição x Valor Real"
        )
        fig.update_layout(
            xaxis_title="Data",
            yaxis_title="Valor",
            legend_title="Legenda",
            hovermode="x unified"
        )
        st.plotly_chart(fig, use_container_width=True)

@st.cache_data
def plota_info_predicao(df_predicao):#Plota os dados de predição dos próximos 15 dias
    fig = px.line(
        df_predicao,
        x="data",
        y=["valor"],
        labels={"value": "Valor", "data": "Data"},
        title="Predição do petróleo Brent (15 dias)"
    )
    fig.update_layout(
        xaxis_title="Data",
        yaxis_title="Valor",
        legend_title="Legenda",
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)

# Carregar e processar os dados
dados_trabalhados = carregar_dados()
df_validacao, erros = calcular_validacao(dados_trabalhados)
df_predicao = calcular_predicao_futura(dados_trabalhados)
plota_info_inicial(dados_trabalhados)
plota_info_validacao(df_validacao, erros)
plota_info_predicao(df_predicao)

col1, col2 = st.columns(2)

#Download de predição
with col1:
    excel_data = predicter.to_excel(df_predicao)
    st.download_button(
        label="Baixar Excel",
        data=excel_data,
        file_name="predicao_petroleo.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# Botão para atualizar o cache
with col2:
    if st.button("Atualizar informações"):
        st.cache_data.clear()
        st.cache_resource.clear()
        streamlit_js_eval(js_expressions="parent.window.location.reload()")