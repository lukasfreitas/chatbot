"""
Gerenciamento do grafo de ferramentas.
Seleciona o fluxo apropriado com base na intenção do usuário e processa interações.
"""

from langgraph.graph import END, START, StateGraph
from typing_extensions import TypedDict

from .general_flow import general_flow
from .prompt_engineering import PromptEngineeringLayer, log_process_data
from .rag_flow import rag_flow


class State(TypedDict):
    """
    Representa o estado do grafo contendo mensagens acumuladas.
    """

    messages: list


prompt_layer = PromptEngineeringLayer()

tool_graph = StateGraph(state_schema=State)


def start(state: State, prompt: str) -> str:
    """
    Inicia o grafo processando o prompt inicial e selecionando o fluxo apropriado.
    """
    intention = prompt_layer.get_user_intent(prompt)

    state['messages'].append(f'Intenção detectada: {intention}')
    state['messages'].append(f'Fluxo selecionado: {intention}')
    return intention


def rag_flow_state(state: State, prompt: str) -> str:
    """
    Executa o fluxo RAG, indexando conteúdo e retornando respostas relevantes.
    """
    response = rag_flow(
        prompt,
        [
            'https://software.waproject.com.br/',
            'https://www.waproject.com.br/',
        ],
    )
    log_process_data.update({'rag_response': response})
    state['messages'].append(response)
    return END


def general_flow_state(state: State, prompt: str) -> str:
    """
    Executa o fluxo geral e armazena a resposta gerada.
    """
    response = general_flow(prompt)
    state['messages'].append(response)
    return END


def history_flow_state(state: State, prompt: str) -> str:
    """
    Processa perguntas relacionadas ao histórico de conversas.
    """
    responde = prompt_layer.handle_history_question(prompt)
    state['messages'].append(responde)
    return END


def nonsense_flow_state(state: State) -> str:
    """
    Executa o fluxo de mensagens sem sentido.
    Responde ao usuário pedindo para reformular sua mensagem.
    """
    response = 'Desculpe, não consegui entender sua mensagem. Por favor, reformule ou envie outra pergunta.'
    state['messages'].append(response)
    return END


def end(state: State) -> str:
    """
    Finaliza o grafo e retorna a última mensagem acumulada.
    """
    print('Fluxo concluído. Mensagens acumuladas:')
    for message in state['messages']:
        print(message)
    return state['messages'][-1] if state['messages'] else 'Sem resposta'


def configure_tool_graph(prompt: str) -> str:
    """
    Configura e executa o grafo de ferramentas com base no prompt inicial.

    Args:
        prompt (str): Prompt fornecido pelo usuário.

    Returns:
        str: Resposta final gerada pelo grafo.
    """
    initial_state = {'messages': []}
    current_state = START

    while current_state != END:
        if current_state == START:
            current_state = start(initial_state, prompt)
        elif current_state == 'nonsense':
            current_state = nonsense_flow_state(initial_state)
        elif current_state == prompt_layer.intention_label[1]:
            current_state = history_flow_state(initial_state, prompt)
        elif current_state == prompt_layer.intention_label[2]:
            current_state = rag_flow_state(initial_state, prompt)
        elif current_state == prompt_layer.intention_label[3]:
            current_state = general_flow_state(initial_state, prompt)
    return end(initial_state)
