import re

import streamlit as st
import requests  # pip install requests


WEBHOOK_URL = st.secrets["WEBHOOK_URL"]


def is_valid_email(email):
    # Basic regex pattern for email validation
    email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(email_pattern, email) is not None


def contact_form():
    with st.form("contact_form"):
        name = st.text_input("Nome")
        email = st.text_input("E-mail")
        message = st.text_area("Mensagem")
        submit_button = st.form_submit_button("Enviar")

    if submit_button:
        if not WEBHOOK_URL:
            st.error("Serviço de E-mail indisponível. Tente mais tarde.", icon="📧")
            st.stop()

        if not name:
            st.error("Por favor, informe o nome.", icon="🧑")
            st.stop()

        if not email:
            st.error("Por favor, informe o E-mail.", icon="📨")
            st.stop()

        if not is_valid_email(email):
            st.error("Por favor, informe um E-mail válido.", icon="📧")
            st.stop()

        if not message:
            st.error("Por favor, escreva uma mensagem.", icon="💬")
            st.stop()

        # Prepare the data payload and send it to the specified webhook URL
        data = {"email": email, "name": name, "message": message}
        response = requests.post(WEBHOOK_URL, json=data)

        if response.status_code == 200:
            st.success("Mensagem enviada com sucesso! 🎉", icon="🚀")
        else:
            st.error("Ocorreu um erro no envio.", icon="😨")
