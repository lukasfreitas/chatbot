# rag_flow.py

from back.config import INDEX_NAME
from back.tavily_client import get_tavily_client
from back.pinecone_client import get_index

def create_manual_embedding(text):
    return [float(ord(char) % 256) for char in text[:1536]]

def rag_flow(prompt):
    tavily_client = get_tavily_client()
    context = tavily_client.get_search_context(query=prompt)

    index = get_index(INDEX_NAME)
    embedding = create_manual_embedding(context) if isinstance(context, str) else [float(value) for value in context['embedding']]

    response = index.query(vector=embedding, top_k=3)

    # Extrai informações com conteúdo relevante
    result_texts = []
    for match in response['matches']:
        content = match.get('metadata', {}).get('content', 'Sem conteúdo disponível')
        result_texts.append(f"Score: {match['score']} - ID: {match['id']} - Content: {content}")

    response_text = "\n".join(result_texts)
    return response_text

