from typing import Annotated

import streamlit as st
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

from .general_flow import general_flow
from .index_site import index_site_content
from .rag_flow import rag_flow
from .prompt_engineering import PromptEngineeringLayer, memory


class State(TypedDict):
    messages: Annotated[list, add_messages]


# Instancia a camada de engenharia de prompt
prompt_layer = PromptEngineeringLayer()


def select_flow(intention: str) -> str:
    """Escolhe o fluxo de acordo com a intenção detectada."""
    if "Informação factual" in intention:
        return "RAG Flow"
    elif "History Flow" in intention:
        return "History Flow"
    else:
        return "General Flow"

tool_graph = StateGraph(state_schema=State)


def start(state: State, prompt: str) -> str:
    # Processa o prompt inicial com a camada de engenharia de prompt
    intention_response = prompt_layer.process_user_message(prompt)

    # Verifica se a intenção retornada é um dicionário com uma resposta sobre o histórico
    if (
        isinstance(intention_response, dict)
        and intention_response.get("intention") == "History Flow"
    ):
        # Adiciona a resposta de histórico ao estado de mensagens e retorna diretamente
        state["messages"].append(intention_response["response"])
        return END  # Indica que o fluxo de histórico está concluído

    # Caso contrário, continua com a lógica normal
    state["messages"].append(f"Intenção detectada: {intention_response}")

    # Seleciona o fluxo com base na intenção
    selected_flow = select_flow(intention_response)
    state["messages"].append(f"Fluxo selecionado: {selected_flow}")
    return selected_flow


def rag_flow_state(state: State, prompt: str) -> str:
    # Executa a indexação de conteúdo
    index_site_content(
        prompt,
        [
            "https://software.waproject.com.br/",
            "https://www.waproject.com.br/",
        ],
    )
    # Executa o fluxo RAG e registra a resposta no histórico
    response = rag_flow(prompt)
    state["messages"].append(f"Resposta do RAG: {response}")
    return END


def general_flow_state(state: State, prompt: str) -> str:
    # Executa o fluxo geral e registra a resposta no histórico
    response = general_flow(prompt)
    state["messages"].append(response)
    return END


def end(state: State) -> str:
    # Imprime o histórico de mensagens para depuração
    print("Fluxo concluído. Mensagens acumuladas:")
    for message in state["messages"]:
        print(message)
    return state["messages"][-1] if state["messages"] else "Sem resposta"


def configure_tool_graph(prompt: str) -> str:
    # Inicializa o estado e define o ponto inicial no grafo
    initial_state = {"messages": []}
    current_state = START

    # Processa o fluxo com base nos estados até alcançar o estado de finalização (END)
    while current_state != END:
        if current_state == START:
            current_state = start(initial_state, prompt)
        elif current_state == "RAG Flow":
            current_state = rag_flow_state(initial_state, prompt)
        elif current_state == "General Flow":
            current_state = general_flow_state(initial_state, prompt)

    # Conclui e retorna a última resposta
    return end(initial_state)
