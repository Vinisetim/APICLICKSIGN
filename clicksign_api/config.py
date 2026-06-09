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

#Definido as variáveis do script com base nas variáveis de ambiente

#=======================================================================================================================
#CLICKSIGN
#=======================================================================================================================
BASE_URL = get_required_env("CLICKSIGN_BASE_URL")
CLICKSIGN_TOKEN = get_required_env("CLICKSIGN_TOKEN")
CLICKSIGN_TEMPLATE_KEY = get_required_env("CLICKSIGN_TEMPLATE_KEY")
EMAIL_TESTE = get_required_env("EMAIL_TESTE_CLICKSIGN")

#=======================================================================================================================
#SHAREPOINT
#=======================================================================================================================
SHAREPOINT_HOSTNAME = get_required_env("SHAREPOINT_HOSTNAME")
SHAREPOINT_SITE_PATH = get_required_env("SHAREPOINT_SITE_PATH")
SHAREPOINT_DRIVE_NAME = get_required_env("SHAREPOINT_DRIVE_NAME")
SHAREPOINT_FILE_PATH = get_required_env("SHAREPOINT_FILE_PATH")

#=======================================================================================================================
#Azure
#=======================================================================================================================
AZURE_TENANT_ID=get_required_env("AZURE_TENANT_ID")
AZURE_CLIENT_ID=get_required_env("AZURE_CLIENT_ID")
AZURE_CLIENT_SECRET=get_required_env("AZURE_CLIENT_SECRET")

#=======================================================================================================================
#Cabeçalho paradrão das requisições clicksign
#=======================================================================================================================
HEADERS = {
    "accept" : "application/json",
    "content-type" : "application/vnd.api+json",
    "Authorization" : CLICKSIGN_TOKEN,
}