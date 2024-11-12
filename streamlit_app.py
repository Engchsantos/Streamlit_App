import streamlit as st


# --- PAGE SETUP ---
sobre_page = st.Page(
    "views/sobre.py",
    title="Sobre",
    icon=":material/account_circle:",
    default=True,
)
inicio_page = st.Page(
    "views/inicio.py",
    title="Início",
    icon=":material/house:",
)
analise_page = st.Page(
    "views/analise.py",
    title="Análise",
    icon=":material/analytics:",
)
dashboard_page = st.Page(
    "views/dash.py",
    title="Dashboard IPEA",
    icon=":material/database:",
)
dashboard_fin_page = st.Page(
    "views/dash_fin.py",
    title="Dashboard Financeiro",
    icon=":material/monitoring:",
)
chatbot_page = st.Page(
    "views/chatbot.py",
    title="Chat Bot",
    icon=":material/smart_toy:",
)
# --- NAVIGATION SETUP [WITHOUT SECTIONS] ---
# pg = st.navigation(pages=[about_page, project_1_page, project_2_page])

# --- NAVIGATION SETUP [WITH SECTIONS]---
pg = st.navigation(
    {
        "Inicio": [inicio_page],
        "Menu": [sobre_page, analise_page, dashboard_page, dashboard_fin_page, chatbot_page],
    }
)


# --- SHARED ON ALL PAGES ---
st.logo("assets/logo.png")
st.sidebar.markdown("Acesse o código no [Github](https://github.com/Engchsantos/Streamlit_App)")


# --- RUN NAVIGATION ---
pg.run()