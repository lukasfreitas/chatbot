# Chatbot Interativo com LangChain e Groq

Este projeto é um chatbot interativo desenvolvido com Streamlit, LangChain, e Groq. O objetivo do chatbot é responder perguntas, armazenar preferências do usuário e realizar verificações de informações factuais, garantindo respostas personalizadas no idioma do usuário.

## Funcionalidades

- **Respostas baseadas no idioma do usuário**: O chatbot detecta automaticamente o idioma do usuário e responde no mesmo idioma, exceto se houver uma solicitação explícita para responder em outro idioma.
- **Engenharia de Prompt com Verificação de Intenção**: Utiliza LangChain e Groq para classificar mensagens dos usuários em tipos como informações factuais, preferências ou feedback.
- **Memória Persistente**: Armazena preferências e informações confirmadas, para fornecer uma interação mais personalizada em conversas futuras.
- **Configuração de Docker**: Implementado em um ambiente Docker para facilitar a implantação e o uso.

## Estrutura do Projeto

```plaintext
chatbot/
├── docker-compose.yml          # Configuração do Docker Compose
├── .env                        # Variáveis de ambiente
├── README.md                   # Documentação do projeto
├── source/
│   ├── back/
│   │   ├── main.py             # Função principal do backend para gerar respostas
│   │   ├── config.py           # Configurações gerais, como API keys
│   │   ├── agent/
│   │   │   ├── tool_graph.py   # Gerencia o fluxo de conversação
│   │   │   ├── prompt_engineering.py # Lógica de engenharia de prompt
│   ├── front/
│   │   ├── main.py             # Interface do chatbot usando Streamlit
│   │   ├── Dockerfile          # Dockerfile para o front (Streamlit)
└── requirements.txt            # Dependências do Python
```

## Configuração e Instalação

### Pré-requisitos

- Docker e Docker Compose
- Conta e chave de API do Groq

### Passos

1. Clone o repositório:

   ```bash
   git clone <url-do-repositorio>
   cd chatbot
   ```

2. Configure as variáveis de ambiente no arquivo `.env`:

   ```plaintext
   GROQ_API_KEY=YOUR_GROQ_API_KEY
   ```

3. Inicie o Docker Compose para subir os serviços:

   ```bash
   sudo docker-compose up --build
   ```

4. Acesse o chatbot em seu navegador na URL `http://localhost:8501`.

## Uso

### Interação com o Chatbot

1. Abra a interface no navegador.
2. Digite uma mensagem no campo de entrada e pressione Enter.
3. O chatbot detectará o idioma e a intenção da mensagem e responderá de acordo.

### Exemplos de Entrada

- Pergunta factual: "Qual é a capital do Brasil?"
- Preferência: "Prefiro um tom mais formal nas respostas."

## Estrutura de Código

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

## Problemas Conhecidos

- Depreciação de `LLMChain` no LangChain: Substituído por `RunnableSequence`.
- Erros de integração podem ocorrer devido a mudanças nas APIs do LangChain e Groq.

## Contribuição

Sinta-se à vontade para abrir issues ou pull requests para melhorar o projeto.

## Licença

Este projeto está sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.
