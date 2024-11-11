# source/back/config.py
"""
Configurações do projeto.
Carrega variáveis de ambiente e define constantes para uso.
"""

import os

from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../.env'))


def get_env_variable(var_name, default=None):
    """Recupera a variável de ambiente ou retorna um valor padrão, caso fornecido."""
    value = os.getenv(var_name, default)
    if value is None:
        raise ValueError(
            f'A variável de ambiente {var_name} não está definida.'
        )
    return value


GROQ_API_KEY = get_env_variable('GROQ_API_KEY')
PINECONE_API_KEY = get_env_variable('PINECONE_API_KEY')
TAVILY_API_KEY = get_env_variable('TAVILY_API_KEY')
PINECONE_ENVIRONMENT = get_env_variable('PINECONE_ENVIRONMENT')
PINECONE_HOST = get_env_variable('PINECONE_HOST')
INDEX_NAME = get_env_variable('INDEX_NAME')
MODEL_ID = get_env_variable('MODEL_ID')
