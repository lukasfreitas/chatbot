# Chatbot Interativo com LangChain e Groq

Este projeto é um chatbot interativo desenvolvido com Streamlit, LangChain, e Groq. 

## Funcionalidades

- **Respostas baseadas no idioma do usuário**: O chatbot detecta automaticamente o idioma do usuário e responde no mesmo idioma, exceto se houver uma solicitação explícita para responder em outro idioma.
- **Engenharia de Prompt com Verificação de Intenção**: Utiliza LangChain e Groq para classificar mensagens dos usuários em categorias.
- **Consultas ao Histórico de Mensagens**: O chatbot é capaz de consultar o histórico de interações.
- **Integração com Tavily**: Utiliza a API Tavily para consultas com contexto especifico.
- **Configuração com Docker**: Totalmente encapsulado em um ambiente Docker para fácil implantação, portabilidade e consistência entre ambientes.
- **Integração com Pinecone**: Utiliza Pinecone para armazenamento e recuperação eficiente de dados vetoriais, otimizando consultas baseadas em embeddings.
- **Flexibilidade de Fluxos de Diálogo**: Gerenciamento de fluxos dinâmicos através do LangGraph, permitindo adaptação a diferentes cenários de interação.

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

### Exemplos de Entrada
**Tavily:** Você conhece a waproject ?

**Histórico:** Qual foi minha primeira mensagem ?

**Preferência** Me responda de forma mais formal.

**Geral:** Quem foi Alberto Santos-Dumont ?

## Tecnologias Utilizadas

- **LangChain** para o gerenciamento do fluxo de diálogo e integração com ferramentas de IA
- **Groq** para processamento avançado de linguagem natural utilizando LLMs
- **Streamlit** para criação de uma interface de usuário interativa e acessível
- **Docker** para encapsulamento, fácil implantação e garantia de portabilidade
- **LangGraph** para estruturação e execução de fluxos de interação dinâmicos
- **Pinecone** para armazenamento e recuperação eficiente de dados vetoriais
- **deep-translator** para tradução de respostas, garantindo suporte multilíngue
- **Python** como linguagem base para desenvolvimento de todas as funcionalidades

## Contribuição

Sinta-se à vontade para abrir issues ou pull requests para melhorar o projeto.

## Licença

Este projeto está sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.
