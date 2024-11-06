import streamlit as st
from deep_translator import GoogleTranslator  # Usando o deep_translator
from langdetect import detect

from .agent.tool_graph import configure_tool_graph


def generate_response(prompt):
    # Armazena o idioma no session state se não estiver definido
    if "user_language" not in st.session_state:
        # Define o idioma detectado na primeira mensagem ou usa português como padrão
        st.session_state["user_language"] = detect(prompt) if detect(prompt) != "en" else "pt"
    
    detected_language = st.session_state["user_language"]

    # Verifica se há uma solicitação explícita para mudar o idioma
    if "em inglês" in prompt.lower():
        detected_language = "en"
        st.session_state["user_language"] = "en"  # Atualiza o idioma preferido do usuário
    elif "em português" in prompt.lower():
        detected_language = "pt"
        st.session_state["user_language"] = "pt"  # Atualiza o idioma preferido do usuário

    # Gera a resposta usando o grafo de ferramentas do LangChain
    response = configure_tool_graph(prompt)

    # Traduz a resposta para o idioma preferido, se necessário
    if detected_language != "en":
        response = GoogleTranslator(source='auto', target=detected_language).translate(response)

    return response
