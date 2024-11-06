from typing import Annotated

import streamlit as st
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

from .general_flow import general_flow
from .index_site import index_site_content
from .rag_flow import rag_flow


class State(TypedDict):
    messages: Annotated[list, add_messages]

def select_flow(prompt: str) -> str:
    keywords = ["waproject", "produto", "serviço", "empresa", "site", "contato"]
    return "RAG Flow" if any(keyword in prompt.lower() for keyword in keywords) else "General Flow"

tool_graph = StateGraph(state_schema=State)

def start(state: State, prompt: str) -> str:
    state["messages"].append(f"Recebido o prompt: {prompt}")
    return select_flow(prompt)

def rag_flow_state(state: State, prompt: str) -> str:
    index_site_content(prompt, [
        "https://www.waproject.com.br/software",
        "https://www.waproject.com.br/cases/motorola-edge"
    ])
    response = rag_flow(prompt)
    state["messages"].append(f"Resposta do RAG: {response}")
    return END

def general_flow_state(state: State, prompt: str) -> str:
    response = general_flow(prompt)
    state["messages"].append(response)
    return END

def end(state: State) -> str:
    print("Fluxo concluído. Mensagens acumuladas:")
    for message in state["messages"]:
        print(message)
    return state["messages"][-1] if state["messages"] else "Sem resposta"

def configure_tool_graph(prompt: str) -> str:
    initial_state = {"messages": []}
    current_state = START
    while current_state != END:
        if current_state == START:
            current_state = start(initial_state, prompt)
        elif current_state == "RAG Flow":
            current_state = rag_flow_state(initial_state, prompt)
        elif current_state == "General Flow":
            current_state = general_flow_state(initial_state, prompt)
    return end(initial_state)
