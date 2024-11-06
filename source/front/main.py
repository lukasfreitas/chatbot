import streamlit as st
from back.main import generate_response

st.title("Chat Bot")
cont = st.container()

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Olá! Como posso ajudar você hoje?"}
    ]

with cont:
    for m in st.session_state["messages"]:
        if m["role"] == 'user':
            st.chat_message("user").write(m["content"])
        elif m["role"] == "assistant":
            st.chat_message("assistant").write(m["content"])

prompt = st.chat_input("Digite sua mensagem:")

if prompt:
    st.session_state["messages"].append({
        "role": "user",
        "content": prompt
    })
    st.chat_message("user").write(prompt)

    placeholder = st.chat_message("assistant")

    response = generate_response(prompt)
    placeholder.write(response)

    st.session_state["messages"].append({
        "role": "assistant",
        "content": response
    })

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
