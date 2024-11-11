# source/back/tavily_client.py
"""
Cliente Tavily para geração de embeddings e busca de contexto.
Configura o cliente utilizando a chave de API.
"""

from back.config import TAVILY_API_KEY
from tavily import TavilyClient

_tavily_client = None


def get_tavily_client():
    """
    Obtém uma instância única do cliente Tavily.
    Inicializa o cliente se ainda não existir.
    """
    global _tavily_client
    if _tavily_client is None:
        _tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
    return _tavily_client
