import random
import time

import streamlit as st


# Streamed response emulator
def response_generator():
    response = random.choice(
        [
            "Hey there! Need help?",
            "Hi! What's up!",
            "Hello! Need assistance?",
            "Hey! Got a question?",
            "Hi there! How can I help?",
            "Hello! Looking for help?",
            "Hey! Need assistance? ",
            "Hi! Got any coding questions?",
            "Hello! Need help?",
            "Hey there! Any questions?",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


st.title("Chatbot")

st.markdown(
        "<p style='text-align: center; color:gray; font-size:24px'><b> Nesse espaço poderemos implantar um chatbot \
        sobre a análise dos dados que fizemos.</b> </p>",  unsafe_allow_html=True
    )


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator())
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
