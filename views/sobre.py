import streamlit as st

from forms.contact import contact_form


@st.experimental_dialog("Contato")
def show_contact_form():
    contact_form()


# --- HERO SECTION ---
col1, col2, col3 = st.columns(3, gap="small", vertical_alignment="center")
with col1:
    st.image("./assets/foto.png", width=230)

with col2:
    st.title("Carlos Santos", anchor=False)
    st.write(
        "Engenheiro civil, estudante de Análise de dados e Gestão de Projetos."
    )
    if st.button("✉️ Contato"):
        show_contact_form()
with col3:
    st.write(        """
        - 10+ anos de experiência em gestão de projetos de engenharia civil
        - Planejamento e gestão utilizando Excel e MS Project
        - Estudante de análise de dados com Python, SQL, Power BI e Streamlit""")
