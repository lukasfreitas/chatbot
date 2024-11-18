# source/back/agent/general_flow.py
"""
Gerenciamento do fluxo geral do agente.
Implementa interações genéricas com o modelo.
"""

from back.config import MODEL_ID
from back.groq_client import get_groq_client


def general_flow(prompt):
    """
    Gera uma resposta baseada no prompt fornecido.
    Utiliza o modelo definido no ambiente para completar as interações.
    """
    client_instance = get_groq_client()
    chat_completion = client_instance.chat.completions.create(
        messages=[
            {
                'role': 'user',
                'content': prompt,
            }
        ],
        model=MODEL_ID,
    )
    return chat_completion.choices[0].message.content
