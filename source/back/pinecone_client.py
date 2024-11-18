# source/back/pinecone_client.py
"""
Cliente Pinecone para operações de indexação e busca vetorial.
Configura o cliente e os índices necessários.
"""

from pinecone import Pinecone, ServerlessSpec

from .config import PINECONE_API_KEY, PINECONE_ENVIRONMENT

pc = Pinecone(api_key=PINECONE_API_KEY)


def get_index(index_name, dimension=1536):
    """
    Obtém ou cria um índice no Pinecone.
    Verifica se o índice existe; caso contrário, cria com as especificações fornecidas.
    """
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric='cosine',
            spec=ServerlessSpec(cloud='aws', region=PINECONE_ENVIRONMENT),
        )
    return pc.Index(index_name)
