import os
from dotenv import load_dotenv

load_dotenv()

def get_required_env(nome_variavel):
    """Função para definir valores usando variáveis de ambiente"""
    valor = os.getenv(nome_variavel)

    if not valor:
        raise RuntimeError(
            f"Variável de ambiente obrigatória não encontrada"
        )

    return valor

BASE_URL = get_required_env("CLICKSIGN_BASE_URL")
CLICKSIGN_TOKEN = get_required_env("CLICKSIGN_TOKEN")
CLICKSIGN_TEMPLATE_KEY = get_required_env("CLICKSIGN_TEMPLATE_KEY")
EMAIL_TESTE = get_required_env("EMAIL_TESTE_CLICKSIGN")

HEADERS = {
    "accept" : "application/json",
    "content-type" : "application/vnd.api+json",
    "Authorization" : CLICKSIGN_TOKEN,
}