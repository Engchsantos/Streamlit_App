# Análise e Previsão do Preço do Petróleo Brent

Este projeto oferece uma solução abrangente que combina **análise histórica**, **previsões de preço** e um **dashboard interativo** sobre o petróleo Brent. Utilizando dados históricos do IPEA e técnicas avançadas de machine learning, a ferramenta proporciona insights estratégicos para empresas do setor energético.

## Objetivo  
Desenvolver uma aplicação interativa que permita:
- **Analisar dados históricos** para identificar tendências e padrões.
- **Visualizar dashboards interativos** que facilitam o entendimento do mercado.
- **Prever flutuações no preço do Brent**, apoiando a gestão de riscos e oportunidades.

## Etapas do Projeto  
### 1. Pipeline de Transformação de Dados  
- **Preparação**: Limpeza e formatação dos dados, com remoção de valores nulos.  
- **Preenchimento de Lacunas**: Inclusão de datas ausentes para consistência temporal.  
- **Suavização**: Estacionarização dos dados para adequação ao modelo ARIMA.  

### 2. Modelagem  
Implementação do modelo híbrido **ARIMA + LSTM**, onde:
- O **ARIMA** captura tendências gerais.
- O **LSTM** refina as previsões considerando padrões históricos.

### 3. Desenvolvimento da Aplicação  
- Construída com **Streamlit**, utilizando o padrão **MVC (Model, View, Controller)** para organização e escalabilidade.  
- Integração com **Firebase** para atualizações dinâmicas de dados, eliminando a necessidade de novos deploys para cada atualização.

### 4. Visualização e Interatividade  
- Dashboards interativos com análises históricas detalhadas e previsões em tempo real.  
- Integração de API para consulta de dados atualizados sobre o dólar e o preço do petróleo.

## Tecnologias Utilizadas  
- **Streamlit**: Para o desenvolvimento da interface interativa.  
- **Firebase**: Para o gerenciamento dinâmico de dados de previsão.  
- **Python**: Para tratamento de dados e modelagem preditiva.  

## Resultados  
A aplicação combina **análises históricas detalhadas**, **previsões confiáveis** e uma **interface amigável** para facilitar o acesso às informações. Essa abordagem integrada apoia decisões estratégicas com base em dados sólidos e projeções confiáveis.

## Links  
- **Aplicação**: [Streamlit App](https://appapp-9mbfydgpo7kmcptfg8jrwd.streamlit.app/)
