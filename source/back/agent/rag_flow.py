import unicodedata

import streamlit as st
from back.config import INDEX_NAME
from back.pinecone_client import get_index
from back.tavily_client import get_tavily_client

from .general_flow import general_flow


class TextProcessor:
    """
    Classe responsável por processar textos. Oferece métodos para:
    - Criar embeddings a partir de texto.
    - Limpar e normalizar identificadores de texto.
    - Dividir conteúdo em segmentos menores.
    """

    @staticmethod
    def create_embedding(text, dimension=1536):
        """
        Gera um embedding para um texto fornecido com base em valores numéricos
        correspondentes aos caracteres.

        Args:
            text (str): Texto de entrada.
            dimension (int): Dimensão do embedding. Padrão: 1536.

        Returns:
            list[float]: Embedding gerado com os valores normalizados.
        """
        embedding = [float(ord(char) % 256) for char in text[:dimension]]
        if len(embedding) < dimension:
            embedding.extend([0.0] * (dimension - len(embedding)))
        return embedding

    @staticmethod
    def clean_id(text):
        """
        Remove caracteres especiais de um texto e os substitui por '_',
        garantindo compatibilidade com ASCII.

        Args:
            text (str): Texto a ser processado.

        Returns:
            str: Texto limpo e normalizado.
        """
        text = (
            unicodedata.normalize('NFKD', text)
            .encode('ascii', 'ignore')
            .decode('ascii')
        )
        return ''.join(char if char.isalnum() else '_' for char in text)

    @staticmethod
    def split_content(raw_content, max_segment_length=1000):
        """
        Divide um texto em segmentos menores com base no comprimento máximo especificado.

        Args:
            raw_content (str): Texto bruto a ser dividido.
            max_segment_length (int): Comprimento máximo de cada segmento. Padrão: 1000.

        Returns:
            list[str]: Lista de segmentos de texto.
        """
        segments = []
        while len(raw_content) > max_segment_length:
            segments.append(raw_content[:max_segment_length])
            raw_content = raw_content[max_segment_length:]
        if raw_content:
            segments.append(raw_content)
        return segments


class PineconeIndexer:
    """
    Classe responsável pela interação com o Pinecone.
    Oferece métodos para indexação de segmentos e consulta ao índice.
    """

    def __init__(self, index_name):
        """
        Inicializa a classe com um índice Pinecone específico.

        Args:
            index_name (str): Nome do índice Pinecone.
        """
        self.index = get_index(index_name)

    def index_segments(self, raw_content, url):
        """
        Indexa segmentos de texto no Pinecone, gerando IDs únicos e metadados.

        Args:
            raw_content (str): Conteúdo bruto a ser indexado.
            url (str): URL associada ao conteúdo.
        """
        segments = TextProcessor.split_content(raw_content)
        for i, segment in enumerate(segments):
            vector_id = f'{TextProcessor.clean_id(url)}_{i}'
            embedding = TextProcessor.create_embedding(segment)
            metadata = {'url': url, 'content': segment}
            self.index.upsert(
                vectors=[
                    {
                        'id': vector_id,
                        'values': embedding,
                        'metadata': metadata,
                    }
                ]
            )

    def query_index(self, prompt, top_k=3):
        """
        Realiza uma consulta no índice Pinecone com base em um prompt.

        Args:
            prompt (str): Prompt usado para gerar o embedding da consulta.
            top_k (int): Número de resultados relevantes a serem retornados.

        Returns:
            dict: Resultados da consulta, incluindo metadados relevantes.
        """
        embedding = TextProcessor.create_embedding(prompt)
        return self.index.query(
            vector=embedding, top_k=top_k, include_metadata=True
        )


class RagFlow:
    """
    Classe que orquestra o fluxo RAG (Recuperação e Geração).
    Combina extração de informações, indexação e geração de respostas.
    """

    def __init__(self, tavily_client, indexer, max_response_length=5000):
        """
        Inicializa o fluxo RAG com um cliente Tavily e um indexador Pinecone.

        Args:
            tavily_client: Instância do cliente Tavily.
            indexer (PineconeIndexer): Instância do indexador Pinecone.
            max_response_length (int): Comprimento máximo permitido para a resposta.
        """
        self.tavily_client = tavily_client
        self.indexer = indexer
        self.max_response_length = max_response_length

    def process_urls(self, urls_to_search, index_data=True):
        """
        Extrai conteúdo das URLs fornecidas e, opcionalmente, as indexa.

        Args:
            urls_to_search (list[str]): URLs para extração de dados.
            index_data (bool): Se True, os dados extraídos serão indexados.

        Returns:
            dict: Dados extraídos das URLs ou None se a extração falhar.
        """
        search_data = self.tavily_client.extract(urls=urls_to_search)
        if not search_data['results']:
            st.write(
                'Não foi possível extrair informações das URLs fornecidas.'
            )
            return None

        if index_data:
            for result in search_data['results']:
                raw_content = result.get('raw_content', '')
                if not raw_content:
                    st.write(
                        'Aviso: Conteúdo bruto está vazio para a URL:',
                        result.get('url', 'unknown'),
                    )
                    continue
                self.indexer.index_segments(
                    raw_content, result.get('url', 'unknown')
                )
        return search_data

    def generate_response(self, prompt):
        """
        Gera uma resposta com base no prompt e nos dados extraídos.

        Args:
            prompt (str): Pergunta do usuário.
            search_data (dict): Dados extraídos e processados.

        Returns:
            str: Resposta gerada ou mensagem de erro.
        """
        response = self.indexer.query_index(prompt)
        relevant_contents = [
            match.get('metadata', {}).get('content', '').strip()
            for match in response['matches']
            if match.get('metadata', {}).get('content', '')
        ]

        total_length = 0
        truncated_contents = []
        for content in relevant_contents:
            if (
                total_length + len(content) + len(prompt)
                > self.max_response_length
            ):
                break
            truncated_contents.append(content)
            total_length += len(content)

        if not truncated_contents:
            return 'Desculpe, não consegui encontrar informações relevantes para sua pergunta.'

        truncated_text = ' '.join(truncated_contents)
        groq_prompt = f'{prompt}\n\nBaseado nas informações a seguir, responda de forma clara e objetiva:\n\n{truncated_text}'
        return general_flow(prompt=groq_prompt)

    def execute(self, prompt, urls_to_search, index_data=True):
        """
        Executa o fluxo RAG completo: extração, indexação e geração de resposta.

        Args:
            prompt (str): Pergunta do usuário.
            urls_to_search (list[str]): URLs a serem processadas.
            index_data (bool): Se True, os dados extraídos serão indexados.

        Returns:
            str: Resposta gerada.
        """
        search_data = self.process_urls(urls_to_search, index_data)
        if not search_data:
            return 'Não foi possível processar as URLs fornecidas.'
        return self.generate_response(prompt, search_data)


def rag_flow(prompt, urls_to_search, index_data=True, max_length=5000):
    """
    Função para simplificar o uso do fluxo RAG.

    Args:
        prompt (str): Pergunta do usuário.
        urls_to_search (list[str]): URLs a serem processadas.
        index_data (bool): Se True, os dados extraídos serão indexados.
        max_length (int): Comprimento máximo permitido para a resposta.

    Returns:
        str: Resposta gerada.
    """
    tavily_client = get_tavily_client()
    indexer = PineconeIndexer(INDEX_NAME)
    rag = RagFlow(tavily_client, indexer, max_response_length=max_length)
    return rag.execute(prompt, urls_to_search, index_data=index_data)
