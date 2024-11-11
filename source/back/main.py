"""
Módulo principal do backend.
Gerencia o fluxo de execução do chatbot.
"""

import streamlit as st
from deep_translator import GoogleTranslator
from langdetect import detect

from .agent.tool_graph import configure_tool_graph


def generate_response(prompt):
    """
    Gera uma resposta com base no prompt fornecido pelo usuário.
    Detecta o idioma do usuário e ajusta a resposta de acordo com a preferência.

    Args:
        prompt (str): Texto da mensagem fornecida pelo usuário.

    Returns:
        str: Resposta traduzida e ajustada de acordo com o idioma preferido do usuário.
    """
    try:
        if 'user_language' not in st.session_state:
            detected = detect(prompt)
            st.session_state['user_language'] = (
                detected if detected in ['pt', 'en'] else 'en'
            )

        detected_language = st.session_state['user_language']

        if 'em inglês' in prompt.lower():
            detected_language = 'en'
            st.session_state['user_language'] = 'en'
        elif 'em português' in prompt.lower():
            detected_language = 'pt'
            st.session_state['user_language'] = 'pt'

        response = configure_tool_graph(prompt)

        if detected_language != 'en':
            response = GoogleTranslator(
                source='auto', target=detected_language
            ).translate(response)

        return response

    except Exception as e:
        st.error(f'Ocorreu um erro ao gerar a resposta: {e}')
        return 'Desculpe, algo deu errado ao processar sua mensagem.'
