"""
Camada de engenharia de prompts.
Configura templates e processa intenções do usuário.
"""

import re

import streamlit as st
from back import config
from back.groq_client import get_groq_client
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.schema import AIMessage, HumanMessage
from langchain_core.runnables import RunnableLambda, RunnableSequence

client = get_groq_client()

log_process_data = dict({})

intention_prompt = PromptTemplate(
    input_variables=['user_message'],
    template=(
        'Classifique a intenção do usuário com base na seguinte mensagem: '
        '"{user_message}". Determine qual das intenções abaixo melhor representa a mensagem e forneça apenas o número correspondente:\n\n'
        '(1) Pergunta sobre o chat: O usuário está perguntando sobre histórico, resumo ou informações passadas da conversa.\n'
        '(2) Pergunta sobre a WaProject: O usuário está perguntando sobre contexto ou detalhes do empresa WaProject.\n'
        '(3) Conversa geral: A mensagem é uma conversa comum, sem relação específica com os dois tópicos anteriores.'
    ),
)


class PromptEngineeringLayer:
    """
    Classe para gerenciar prompts e intenções do usuário.
    Armazena o histórico de conversas e processa mensagens.
    """

    intention_label = {1: 'history_flow', 2: 'rag_flow', 3: 'general_flow'}

    def __init__(self):
        self.memory = ConversationBufferMemory(return_messages=True)

        def groq_chat_completion(prompt_text):
            response = client.chat.completions.create(
                messages=[{'role': 'user', 'content': prompt_text}],
                model=config.MODEL_ID,
            )
            return response.choices[0].message.content

        self.intention_chain = RunnableSequence(
            RunnableLambda(lambda inputs: intention_prompt.format(**inputs)),
            RunnableLambda(groq_chat_completion),
        )

    @staticmethod
    def is_nonsense_message(user_message):
        """
        Verifica se a mensagem é sem sentido com base em critérios básicos.

        Args:
            user_message (str): Mensagem enviada pelo usuário.

        Returns:
            bool: True se a mensagem for sem sentido, False caso contrário.
        """

        # Mensagens sem palavras reconhecíveis (apenas números ou caracteres aleatórios)
        if not re.search(r'[a-zA-Z]', user_message):
            return True

        # Mensagens com sequência de caracteres incoerentes
        if re.fullmatch(r'[^\w\s]+', user_message):
            return True

        return False

    def get_intent_id(self, raw_intent):
        """
        Identifica o número da intenção a partir da resposta do Groq.

        Args:
            raw_intent (str): Resposta do Groq.

        Returns:
            int: Número da intenção.
        """
        if '1' in raw_intent:
            return 1
        if '2' in raw_intent:
            return 2
        if '3' in raw_intent:
            return 3
        return None


def get_user_intent(self, user_message):
    """
    Processa a mensagem do usuário para determinar sua intenção e o fluxo associado.

    Este método salva o contexto da mensagem do usuário,
    invoca a cadeia de intenção para detectar a intenção associada à mensagem e mapeia
    a intenção detectada para um fluxo correspondente. Caso ocorra um erro durante o
    processamento, um fluxo padrão ('nonsense') é retornado.

    Args:
        user_message (str): A mensagem do usuário para análise de intenção.

    """
    try:
        self.memory.save_context({'user': user_message}, {'bot': ''})
        detected_intent = self.intention_chain.invoke(
            {'user_message': user_message}
        ).strip()
        current_flow = self.intention_label.get(
            self.get_intent_id(detected_intent), 'nonsense'
        )
        log_process_data.update({'raw_intent': detected_intent})
        return current_flow
    except Exception as e:
        st.warning(f'Erro ao processar intenção: {str(e)}')
        return 'nonsense'

    def handle_history_question(self, user_message):
        """
        Processa perguntas relacionadas ao histórico de conversas.
        Retorna o histórico formatado ou informações específicas.
        """
        history = self.memory.load_memory_variables({}).get('history', [])

        if 'primeira mensagem' in user_message.lower() and history:
            return f"Sua primeira mensagem foi: '{history[0].content}'"
        elif 'última mensagem' in user_message.lower() and history:
            return f"Sua última mensagem foi: '{history[-1].content}'"
        elif (
            'mostrar histórico' in user_message.lower()
            or 'ver histórico' in user_message.lower()
        ):
            formatted_history = 'Aqui está o histórico de mensagens:\n\n'
            for msg in history:
                if isinstance(msg, HumanMessage):
                    formatted_history += f'Usuário: {msg.content}\n'
                elif isinstance(msg, AIMessage):
                    formatted_history += f'Bot: {msg.content}\n'
            return (
                formatted_history
                if history
                else 'Não tenho registro de mensagens anteriores.'
            )

        return 'Essa pergunta não está relacionada ao histórico. Posso ajudar com mais alguma coisa?'

    def store_preference(self, preference):
        """
        Armazena as preferências do usuário no histórico de memória.
        """
        self.memory.save_context(
            {'user': preference}, {'bot': 'Preferência registrada.'}
        )
