from pathlib import Path
from urllib.parse import quote

import msal
import requests

from clicksign_api.config import (
    SHAREPOINT_HOSTNAME,
    SHAREPOINT_SITE_PATH,
    SHAREPOINT_DRIVE_NAME,
    SHAREPOINT_FILE_PATH,
    AZURE_TENANT_ID,
    AZURE_CLIENT_ID,
    AZURE_CLIENT_SECRET,
)

GRAPH_BASE_URL = "https://graph.microsoft.com/v1.0/"
GRAPH_SCOPE = ["https://graph.microsoft.com/.default"]

def obter_token_graph():
    """Usar o endpoit do msal para obter o token do Graph Usando os ids da Azure"""
    authority = f"https://login.microsoft.com/{AZURE_TENANT_ID}"

    app = msal.ConfidentialClientApplication(
        client_id=AZURE_CLIENT_ID,
        client_credential=AZURE_CLIENT_SECRET,
        authority=authority,
    )
    resultado = app.acquire_token_for_client(scopes=GRAPH_SCOPE)


    if "acess_token" not in resultado:
        raise RuntimeError(
            f"Erro ao obter token do Graph{resultado}"
        )
    return resultado["access_token"]

def montar_header_graph():
    """Usa o token do msal para a autorização do Graph"""
    token = obter_token_graph()
    return {"Authorization": f"Bearer {token}"}

def obter_site_id(headers):
    """Busca o ID do site sharepoint para usar nos próximos endpoints"""
    site_url = (
        f"{GRAPH_BASE_URL}sites/"
        f"{SHAREPOINT_HOSTNAME}:{SHAREPOINT_SITE_PATH}"
    )
    response = requests.get(site_url, headers=headers)

    if response.status_code != 200:
        raise RuntimeError(
            f"Erro ao obter id do site"
            f"Status code: {response.status_code}"
            f"Resposta: {response.text}"
        )
    return response.json()["id"]

def obter_drive_id(site_id, headers):
    """Busca o id da pasta do sharepoint com o arquivo xlsx"""
    drive_url = f"{GRAPH_BASE_URL}/sites/{site_id}/drives"

    response = requests.get(drive_url, headers=headers)

    if response.status_code != 200:
        raise RuntimeError(
            "Erro ao listar drives do site"
            f"Status code: {response.status_code}"
            f"Resposta: {response.text}"
        )
    #Lista de drives
    drives = response.json().get("value", [])

    #Procura um drive com o nome igual o que buscamos
    for drive in drives:
        if drive.get("name") == SHAREPOINT_DRIVE_NAME:
            #se achar retorna o ID
            return drive["id"]

    #se não achar lista os drives usando uma compreensão
    nomes_encontrados = [drive.get("name") for drive in drives]

    #debug de erro
    raise RuntimeError(
        f"Drive '{SHAREPOINT_DRIVE_NAME}' nao encontrado"
        f"Drives Encontrados: {nomes_encontrados}"
    )


def baixar_planilha_sharepoint(destino_local):
    """Função que vai usar os ids obtidos para achar o arquivo do sharepoint"""
    headers = montar_header_graph()
    site_id = obter_site_id(headers)
    drive_id = obter_drive_id(site_id, headers)

    #Usa o caminho do arquivo do sharepoint tratando caracteres especiais, mas mantendo a barra
    caminho_arquivo = quote(SHAREPOINT_FILE_PATH, safe="/")

    #monta a url do download
    download_url = (
        f"{GRAPH_BASE_URL}drives/{drive_id}"
        f"/root:/{caminho_arquivo}/content"
    )

    print("Baixando planilha do sharepoint...")
    print(f"Arquivo do sharepoint:{SHAREPOINT_FILE_PATH}")
    print(f"Destino Local: {destino_local}")

    #usa o endpoint do dowload para baixar o arquivo
    response = requests.get(download_url, headers=headers)

    #debug de erro
    if response.status_code != 200:
        raise RuntimeError(
            f"Erro ao baixar planilha do sharepoint"
            f"Status code: {response.status_code}"
            f"Resposta: {response.text}"
        )

    #define o local do arquivo na máquina, cria o diretório se necessário
    destino_local = Path(destino_local)
    destino_local.mkdir(parents=True, exist_ok=True)

    with open(destino_local, "wb") as arquivo:
        arquivo.write(response.content)

    print("Planilha baixada com sucesso")

    #retorna o local do arquivo baixado no fim da função
    return destino_local