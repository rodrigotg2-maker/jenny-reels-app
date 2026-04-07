import os
from openai import OpenAI

def get_client():
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("No se encontró OPENAI_API_KEY en variables de entorno")

    return OpenAI(api_key=api_key)


def get_model_name():
    return os.getenv("OPENAI_MODEL", "gpt-4.1-mini")