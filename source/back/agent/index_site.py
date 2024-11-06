import re

from back.config import INDEX_NAME
from back.pinecone_client import get_index
from back.tavily_client import get_tavily_client


def clean_id(text):
    return re.sub(r'[^\x00-\x7F]+', '_', text)

def index_site_content(query, links=None):
    # Obtém a instância de TavilyClient
    tavily_client = get_tavily_client()

    # Adiciona links ao contexto, se fornecidos
    context = query
    if links:
        links_text = "\n".join(f"- {link}" for link in links)
        context += f"\n\nLinks para referência:\n{links_text}"

    # Executa a consulta para obter o contexto baseado na query e links fornecidos
    context = tavily_client.get_search_context(query=context)

    # Obtém o índice do Pinecone utilizando get_index
    index = get_index(INDEX_NAME)

    # Gera o embedding do contexto - converte o conteúdo textual em um vetor de floats
    if isinstance(context, str):
        embedding = [float(ord(char) % 256) for char in context[:1536]]
    else:
        embedding = [float(value) for value in context['embedding']]

    vector_id = clean_id(query)
    metadata = {"query": query, "source": "Tavily", "links": links if links else []}

    # Faz o upsert do embedding no Pinecone
    index.upsert([(vector_id, embedding, metadata)])
    print("Conteúdo indexado com sucesso.")
