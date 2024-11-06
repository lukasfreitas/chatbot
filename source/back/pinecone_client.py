# pinecone_client.py
from pinecone import Pinecone, ServerlessSpec

from .config import PINECONE_API_KEY, PINECONE_ENVIRONMENT

# Inicializa o cliente Pinecone uma vez
pc = Pinecone(api_key=PINECONE_API_KEY)

# Define o índice com as especificações, caso ele não exista
def get_index(index_name, dimension=1536):
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region=PINECONE_ENVIRONMENT
            )
        )
    return pc.Index(index_name)
