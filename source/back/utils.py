import streamlit as st


def info_logger(msg):
    with st.chat_message(
        'Info', avatar=':material/tv_options_input_settings:'
    ):
        st.write(msg)
