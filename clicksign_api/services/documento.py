from datetime import datetime
import math
import requests
from clicksign_api.config import BASE_URL, HEADERS


templake_key = "df8c6ebc-5db3-4186-b1ee-cf3cd8fb2a7e"

def limpar_valor(valor):
    """Função para limpar o valor do documento"""
    if valor is None:
        return ""

    if isinstance(valor, float) and math.isnan(valor):
        return ""

    return str(valor).strip()


def formatar_data(valor):
    """Função para formatar datas no documento"""
    if valor is None:
        return ""

    if isinstance(valor, float) and math.isnan(valor):
        return ""

    if hasattr(valor, "strftime"):
        return valor.strftime("%d/%m/%Y")

    return str(valor).strip()

def formatar_moeda(valor):
    """Função para formatar moeda no documento"""
    if valor is None:
        return ""

    if isinstance(valor, float) and math.isnan(valor):
        return ""

    try:
        numero = float(valor)
        return f"{numero:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except ValueError:
        return str(valor).strip()

def montar_dados_template(multa):

    dados_template = {
        "AIT": limpar_valor(multa.get("AIT")),
        "DATA_MULTA": formatar_data(multa.get("data_infracao")),
        "HORA_MULTA": limpar_valor(multa.get("hora_infracao")),
        "PLACA": limpar_valor(multa.get("placa")),
        "NOME": limpar_valor(multa.get("motorista")),
        "CPF": limpar_valor(multa.get("cpf")),
        "VALOR": formatar_moeda(multa.get("valor")),
        "MES_MULTA": formatar_data(multa.get("DESCONTORAPARTIR")),
        "DATA_DOCUMENTO": datetime.now().strftime("%d/%m/%Y"),
        "PARCELAS": limpar_valor(multa.get("PARCELAS")),
    }

    return dados_template




def criar_documento(envelope_id, multa):
    """Cria um documento dentro do envelope usando os dados da multa"""

    url = f"{BASE_URL}/envelopes/{envelope_id}/documents"

    print("DEBUG envelope_id:", repr(envelope_id))
    print("DEBUG URL documento:", url)


    dados_template = montar_dados_template(multa)

    nome_arquivo = f"vale_multa_{dados_template['AIT']}.docx"
    print("DEBUG filename:", repr(nome_arquivo))

    payload = {
        "data": {
            "type": "documents",
            "attributes": {
                "filename": nome_arquivo,
                "template": {
                    "key": templake_key,
                    "data": dados_template,
                }
            }
        }
    }
    response = requests.post(url, json=payload, headers=HEADERS)

    if response.status_code == 201:
        print("Documento criado no envelope")
        data = response.json()
        document_id = data["data"]["id"]
        return document_id

    print("Erro ao criar o documento")
    print("Status:", response.status_code)
    print("Resposta:", response.text)
    return None

