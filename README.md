# Chatbot Interativo com LangChain e Groq

Este projeto é um chatbot interativo desenvolvido com Streamlit, LangChain, e Groq. O objetivo do chatbot é responder perguntas, armazenar preferências do usuário e realizar verificações de informações factuais, garantindo respostas personalizadas no idioma do usuário.

## Funcionalidades

- **Respostas baseadas no idioma do usuário**: O chatbot detecta automaticamente o idioma do usuário e responde no mesmo idioma, exceto se houver uma solicitação explícita para responder em outro idioma.
- **Engenharia de Prompt com Verificação de Intenção**: Utiliza LangChain e Groq para classificar mensagens dos usuários em tipos como informações factuais, preferências ou feedback.
- **Consultas ao historico de mensagens**: O chatbot detecta é capaz de consultar o historico de mensagens
- **Configuração de Docker**: Implementado em um ambiente Docker para facilitar a implantação e o uso.

## Configuração e Instalação

### Pré-requisitos

- Docker e Docker Compose
- Chaves para o .env

### Como obter as chaves de ambiente
- #### Para configurar corretamente o projeto, você precisará de algumas chaves de API e variáveis específicas. Abaixo estão os passos para obter cada uma delas:

##### GROQ_API_KEY

- Acesse o site oficial da Groq e crie uma conta, caso ainda não tenha.
- Após o login, vá até a seção de configurações de API para gerar sua chave de API.   
- Substitua YOUR_GROQ_API_KEY pelo valor da chave gerada.
  
##### PINECONE_API_KEY, PINECONE_ENVIRONMENT e PINECONE_HOST

- Acesse Pinecone e crie uma conta, caso ainda não tenha.
- No painel, navegue até a seção de API Keys e crie uma chave de API.
- Após gerar a chave, copie o valor e substitua PINECONE_API_KEY pelo valor copiado.
- Para PINECONE_ENVIRONMENT, use o valor do ambiente fornecido no painel do Pinecone (por exemplo, us-west1-gcp).
- Para PINECONE_HOST, você também encontrará essa informação no painel do Pinecone, geralmente indicado como o endpoint do seu índice.

##### TAVILY_API_KEY

- Acesse o site oficial da Tavily e crie uma conta, caso ainda não tenha.
- Após o login, navegue até as configurações de API para obter sua chave de API Tavily.
- Substitua TAVILY_API_KEY pela chave que você gerou.

#### INDEX_NAME

- Defina um nome único para o índice no Pinecone, que será usado para armazenar os embeddings.
- Esse nome pode ser qualquer string válida. Certifique-se de que o índice está configurado no painel do Pinecone antes de iniciar o projeto.

#### MODEL_ID
- Este projeto desenvolvido utilizando o modelo "llama3-groq-8b-8192-tool-use-preview". Certifique-se de que possui acesso a esse modelo na sua conta Groq.

### Passos

1. Clone o repositório:

   ```bash
   git clone https://github.com/lukasfreitas/chatbot
   cd chatbot
   ```

2. Configure as variáveis de ambiente no arquivo `.env`:

   ```plaintext
   GROQ_API_KEY=YOUR_GROQ_API_KEY
   GROQ_API_KEY=
   PINECONE_API_KEY=
   PINECONE_ENVIRONMENT=
   PINECONE_HOST=
   TAVILY_API_KEY=
   INDEX_NAME=
   MODEL_ID=llama3-groq-8b-8192-tool-use-preview
   ```

3. Inicie o Docker Compose para subir o serviço:

   ```bash
   sudo docker-compose up --build
   ```

4. Acesse o chatbot em seu navegador na URL `http://localhost:8501`.

## Uso dos fluxos
**Tavily:** WaProject é uma software house ?

**Histórico:** Qual foi minha primeira mensagem ?

**Preferência** Gostaria que você me respondesse de forma mais formal.

**Geral:** Qual foi minha primeira mensagem ?


### Interação com o Chatbot

1. Abra a interface no navegador.
2. Digite uma mensagem no campo de entrada e pressione Enter.
3. O chatbot detectará o idioma e a intenção da mensagem e responderá de acordo.

### Exemplos de Entrada

- Pergunta factual: "Qual é a capital do Brasil?"

### Engenharia de Prompt

A engenharia de prompt está implementada em `prompt_engineering.py` e usa templates de LangChain para classificar a intenção da mensagem do usuário. Com `RunnableSequence`, o projeto processa verificações factuais e armazena informações conforme necessário.

```python
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables.base import RunnableSequence

class PromptEngineeringLayer:
    def __init__(self):
        # Configuração dos prompts e verificação
        ...
```

## Tecnologias Utilizadas

- **LangChain** e **Groq** para gerenciamento do fluxo de diálogo e processamento de linguagem natural
- **Streamlit** para interface de usuário
- **Docker** para encapsulamento e fácil implantação

## Contribuição

Sinta-se à vontade para abrir issues ou pull requests para melhorar o projeto.

## Licença

Este projeto está sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.
