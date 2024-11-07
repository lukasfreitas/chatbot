import streamlit as st
from back.main import generate_response

# Título do Chatbot
st.title("Chat Bot")
cont = st.container()

# Inicializa o estado da sessão para armazenar mensagens
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Olá! Como posso ajudar você hoje?"}
    ]

# Exibe o histórico de mensagens na interface
with cont:
    for m in st.session_state["messages"]:
        if m["role"] == 'user':
            st.chat_message("user").write(m["content"])
        elif m["role"] == "assistant":
            st.chat_message("assistant").write(m["content"])

# Campo de entrada para o usuário
prompt = st.chat_input("Digite sua mensagem:")

if prompt:
    # Adiciona a mensagem do usuário ao histórico
    st.session_state["messages"].append({
        "role": "user",
        "content": prompt
    })
    st.chat_message("user").write(prompt)

    # Placeholder para a resposta do bot
    placeholder = st.chat_message("assistant")

    # Chama o backend para obter a resposta processada
    response = generate_response(prompt)
    placeholder.write(response)

    # Adiciona a resposta do backend ao histórico de mensagens
    st.session_state["messages"].append({
        "role": "assistant",
        "content": response
    })

# Estilização para dispositivos móveis (opcional)
st.markdown(
    """
    <style>
    @media only screen and (max-width: 600px) {
        .st-emotion-cache-1eo1tir {
            padding-left: 0px;
            padding-right: 0px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)
