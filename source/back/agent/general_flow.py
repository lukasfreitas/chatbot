from back.config import GROQ_API_KEY, MODEL_ID
from groq import Groq


def create_general_chain():
    # Inicializa o cliente Groq com a chave da API
    client = Groq(api_key=GROQ_API_KEY)
    return client

cliente = create_general_chain()
def get_groq_cliente():
    return cliente
def general_flow(prompt):
    # Cria uma instância do cliente Groq
    client = get_groq_cliente()

    # Faz a requisição de conclusão de chat usando o modelo da Groq
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=MODEL_ID,  # Modelo definido no .env, como 'llama3-8b-8192'
    )

    # Retorna o conteúdo da resposta
    return chat_completion.choices[0].message.content
