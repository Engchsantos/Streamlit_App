import streamlit as st
from controllers.Predicao_controller import Predicao_controller
from models.DataAccess_class import DataAccess

reader = DataAccess()
predicter = Predicao_controller()

data = reader.get_brent_data().head(1095) # 3 anos
data.columns = ['Data', 'Preço - petróleo bruto - Brent (FOB)']
df_predicao = predicter.realiza_predicao(data)
st.table(df_predicao)