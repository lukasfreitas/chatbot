from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_core.runnables.base import RunnableSequence

from .general_flow import get_groq_cliente

# Inicializando o LLM com LangChain e Groq
llm = get_groq_cliente()

# Configurando o buffer de memória para armazenar informações persistentes
memory = ConversationBufferMemory()

# Template para validar a intenção e tipo de mensagem do usuário
intention_prompt = PromptTemplate(
    input_variables=["user_message"],
    template=(
        "Classifique a intenção do usuário com base na seguinte mensagem: "
        "{user_message}. Indique se é uma: (1) Informação factual, (2) Preferência, "
        "(3) Feedback ou (4) Correção de fato."
    )
)

# Template para confirmação de fatos
fact_verification_prompt = PromptTemplate(
    input_variables=["fact_statement"],
    template=(
        "Confirme se a seguinte afirmação é verdadeira: {fact_statement}. "
        "Responda com 'Verdadeiro' ou 'Falso' e uma breve explicação."
    )
)

# Configura o gerador de intenção e a verificação de fatos usando RunnableSequence
class PromptEngineeringLayer:
    def __init__(self):
        # Usando RunnableSequence diretamente
        self.intention_chain = RunnableSequence([intention_prompt, llm])
        self.verification_chain = RunnableSequence([fact_verification_prompt, llm])

    def process_user_message(self, user_message):
        # Detecta a intenção da mensagem
        intention = self.intention_chain.invoke({"user_message": user_message})
        
        if "Informação factual" in intention:
            # Verifica a veracidade do fato
            verification = self.verification_chain.invoke({"fact_statement": user_message})
            if "Verdadeiro" in verification:
                self.store_information(user_message)
                return "Informação armazenada com sucesso."
            else:
                return "Informação não armazenada. Verificação falhou."

        elif "Preferência" in intention:
            # Armazena a preferência sem validação de veracidade
            self.store_preference(user_message)
            return "Preferência armazenada com sucesso."

        elif "Feedback" in intention or "Correção de fato" in intention:
            return "Obrigado pelo feedback, mas isso não será armazenado como informação factual."

    def store_information(self, information):
        # Armazena informações válidas
        memory.save_context({"user": information}, {"bot": "Informação confirmada e armazenada."})

    def store_preference(self, preference):
        # Armazena preferências diretamente
        memory.save_context({"user": preference}, {"bot": "Preferência registrada."})

