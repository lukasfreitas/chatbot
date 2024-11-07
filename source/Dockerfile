# Usa uma imagem leve do Python
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Atualiza o pip e instala o Streamlit diretamente
RUN pip install --upgrade pip && \
    pip install streamlit \
    groq \
    langchain \
    langgraph \
    langchain-community \
    langchain_core \
    pinecone-client \
    requests \
    tavily-python \
    python-dotenv \
    langchain-groq \
    langdetect \
    deep_translator

# Copia o diretório completo do código para o container
COPY . /app/source

# Configura o PYTHONPATH para incluir o diretório /app/source
ENV PYTHONPATH="${PYTHONPATH}:/app/source"

# Expõe a porta padrão do Streamlit
EXPOSE 8501

# Comando para rodar a aplicação
CMD ["streamlit", "run", "source/front/main.py", "--server.port=8501", "--server.address=0.0.0.0"]