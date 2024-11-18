from back.config import GROQ_API_KEY
from groq import Groq


def create_general_chain():
    """
    Cria uma instância do cliente Groq com a chave de API configurada.
    """
    client = Groq(api_key=GROQ_API_KEY)
    return client


client = create_general_chain()


def get_groq_client():
    """
    Retorna a instância do cliente Groq.
    """
    return client
