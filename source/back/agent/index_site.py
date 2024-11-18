"""
Gerenciamento de indexação de conteúdo e consulta com integração ao fluxo de RAG.
"""

from back.config import INDEX_NAME
from back.pinecone_client import get_index
from back.tavily_client import get_tavily_client

from .rag_flow import rag_flow


def clean_id(text):
    """
    Limpa o ID removendo caracteres especiais e substituindo-os por '_'.

    Args:
        text (str): Texto a ser limpo.

    Returns:
        str: Texto limpo.
    """
    import re

    cleaned_text = re.sub(r'[^\w]', '_', text)
    cleaned_text = re.sub(
        r'_+', '_', cleaned_text
    )  # Remove sublinhados consecutivos
    return cleaned_text.strip('_')


def index_site_content(prompt, urls_to_search):
    """
    Indexa o conteúdo das URLs fornecidas e retorna uma resposta baseada no RAG Flow.

    Args:
        prompt (str): Prompt fornecido pelo usuário.
        urls_to_search (list): URLs a serem indexadas.

    Returns:
        str: Resposta gerada com base no conteúdo indexado.
    """
    tavily_client = get_tavily_client()

    search_data = tavily_client.extract(urls=urls_to_search)
    if not search_data['results']:
        return 'Não foi possível extrair informações das URLs fornecidas.'

    index = get_index(INDEX_NAME)
    for result in search_data['results']:
        raw_content = result.get('raw_content', '')
        vector_id = clean_id(result.get('url', 'unknown'))
        embedding = rag_flow(prompt, urls_to_search)
        metadata = {
            'url': result.get('url', 'unknown'),
            'content': raw_content,
        }
        index.upsert([(vector_id, embedding, metadata)])

    response = rag_flow(prompt, urls_to_search)
    return response
