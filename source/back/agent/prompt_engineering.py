from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence, RunnableLambda
from langchain.schema import HumanMessage, AIMessage  # Importa HumanMessage e AIMessage
from .general_flow import get_groq_cliente
from back.config import MODEL_ID
import streamlit as st

# Inicializa o cliente Groq
client = get_groq_cliente()

# Configura o buffer de memória para armazenar contexto e histórico de conversa
memory = ConversationBufferMemory(return_messages=True)  # Define para retornar as mensagens

# Template para identificar a intenção do usuário
intention_prompt = PromptTemplate(
    input_variables=["user_message"],
    template=(
        "Classifique a intenção do usuário com base na seguinte mensagem: "
        "\"{user_message}\". Determine qual das intenções abaixo melhor representa a mensagem e forneça apenas o número correspondente:\n\n"
        "(1) Informação factual: A mensagem do usuário compartilha um fato ou afirmação específica, "
        "como 'A capital do Brasil é Brasília' ou 'A empresa foi fundada em 2001'.\n"
        "(2) Preferência: A mensagem expressa uma preferência ou desejo pessoal do usuário, "
        "como 'Prefiro respostas formais' ou 'Gostaria de receber menos notificações'.\n"
        "(3) Feedback: O usuário fornece uma opinião ou avaliação, como 'O sistema está funcionando bem' "
        "ou 'A resposta anterior foi confusa'.\n"
        "(4) Correção de fato: O usuário corrige uma informação ou fato mencionado anteriormente, "
        "como 'A data correta é 2022, não 2021' ou 'Na verdade, a sede da empresa fica em São Paulo'.\n"
        "(5) Pergunta sobre histórico da conversa: O usuário pergunta sobre informações passadas da conversa, "
        "como 'Qual foi minha primeira mensagem?', 'O que eu disse antes?' ou 'Qual foi minha última mensagem?'."
    )
)

class PromptEngineeringLayer:
    def __init__(self):
        # Função auxiliar para chamada ao cliente Groq
        def groq_chat_completion(prompt_text):
            # Chama o modelo Groq com a mensagem formatada
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt_text}],
                model=MODEL_ID
            )
            return response.choices[0].message.content

        # Configura a cadeia de intenção usando RunnableLambda
        self.intention_chain = RunnableSequence(
            RunnableLambda(lambda inputs: intention_prompt.format(**inputs)),
            RunnableLambda(groq_chat_completion)
        )

    def process_user_message(self, user_message):
        # Adiciona a mensagem atual ao histórico antes de processar
        memory.save_context({"user": user_message}, {"bot": ""})  # Armazena a pergunta antes da resposta
        
        # Detecta a intenção do usuário
        intention = self.intention_chain.invoke({"user_message": user_message})
    
        # Verifica se a intenção detectada é "Pergunta sobre histórico" com uma condição mais restrita
        if "Pergunta sobre histórico" in intention:
            if any(keyword in user_message.lower() for keyword in ["primeira mensagem", "última mensagem", "mostrar histórico", "ver histórico"]):
                response = self.handle_history_question(user_message)
                return {"intention": "History Flow", "response": response}
            else:
                # Caso contenha "Pergunta sobre histórico", mas não seja sobre o histórico da conversa
                intention = "Informação factual"
    
        # Continua com outras intenções de forma normal
        if "Informação factual" in intention:
            response = "Informação armazenada com sucesso."
            memory.save_context({"user": user_message}, {"bot": response})
            return {"intention": "RAG Flow", "response": response}
    
        elif "Preferência" in intention:
            self.store_preference(user_message)
            return {"intention": "General Flow", "response": "Preferência armazenada com sucesso."}
    
        elif "Feedback" in intention or "Correção de fato" in intention:
            response = "Obrigado pelo feedback, mas isso não será armazenado como informação factual."
            memory.save_context({"user": user_message}, {"bot": response})
            return {"intention": "General Flow", "response": response}
    
        # Intenção não identificada
        response = "Intenção não identificada."
        memory.save_context({"user": user_message}, {"bot": response})
        return {"intention": "General Flow", "response": response}


    def handle_history_question(self, user_message):
        # Carrega o histórico do buffer de memória
        history = memory.load_memory_variables({}).get("history", [])

        # Verifica se a pergunta é sobre a "primeira" ou "última" mensagem
        if "primeira mensagem" in user_message.lower() and history:
            return f"Sua primeira mensagem foi: '{history[0].content}'"
        elif "última mensagem" in user_message.lower() and history:
            return f"Sua última mensagem foi: '{history[-1].content}'"
        elif "mostrar histórico" in user_message.lower() or "ver histórico" in user_message.lower():
            # Formata o histórico completo se o usuário pediu explicitamente
            formatted_history = "Aqui está o histórico de mensagens:\n\n"
            for msg in history:
                if isinstance(msg, HumanMessage):
                    formatted_history += f"Usuário: {msg.content}\n"
                elif isinstance(msg, AIMessage):
                    formatted_history += f"Bot: {msg.content}\n"
            return formatted_history if history else "Não tenho registro de mensagens anteriores."

        # Caso a pergunta não seja sobre o histórico, retorne uma resposta padrão
        return "Essa pergunta não está relacionada ao histórico. Posso ajudar com mais alguma coisa?"

    def store_preference(self, preference):
        memory.save_context({"user": preference}, {"bot": "Preferência registrada."})
