import streamlit as st

st.title('Sobre')


st.markdown("<br></br><p style='text-align: center; color:red; font-size:50px'>TechChallenge - Fase 4</p><br></br>",  unsafe_allow_html=True)

st.markdown(
        "<p style='text-align: justify; color:gray; font-size:25px'><b>Tech Challenge é um projeto da pós-graduação em Data Analytics da FIAP, que engloba os conhecimentos obtidos nas disciplinas das fases. Nessa fase, o objetivo foi simular que fomos contratados para uma consultoria, e nosso trabalho foi analisar os dados de preço do petróleo Brent para um grande cliente do segmento, desenvolver um dashboard interativo para gerar insights relevantes para tomada de decisão e construir de um modelo de Machine Learning para fazer a previsão do preço do petróleo.</b></p>",  unsafe_allow_html=True
    )

st.markdown(
        "<p style='text-align: justify; color:gray; font-size:25px'>Para desenvolver esse projeto, foi indicada a base de dados do site do IPEA, onde a partir de uma análise preliminar, definimos os modelos que seriam estudados. Para complementar a análise, fizemos pesquisas sobre a influência do contexto geopolítico e econômico na variação do preço do petróleo.</p>",  unsafe_allow_html=True
    )
st.markdown(
        "<p style='text-align: justify; color:gray; font-size:25px'>Utilizamos uma variedade de modelos de machine learning, incluindo modelos clássicos de séries temporais e a combinação deles, para construir um sistema de previsão robusto. O modelo final apresentou um RMSE de 1.91, superando os modelos anteriores.</p>",  unsafe_allow_html=True
    )

st.markdown(
        "<p style='text-align: justify; color:gray; font-size:25px'>No final, construímos essa apresentação com a utilização da biblioteca Streamlit, onde disponibilizamos o resultado do nosso trabalho.<b><i> Os códigos utilizados para construção desse projeto estão disponíveis no Github. Lá você terá acesso a informações detalhadas sobre o projeto.</i></b></p>",  unsafe_allow_html=True
    )