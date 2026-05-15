import json
import requests
from clicksign_api.config import BASE_URL, HEADERS
from clicksign_api.utils.base64_utils import gerar_base64_pdf

def criar_documento(id_envelope, signer_id):
    """Cria um documento dentro do envelope"""

    url = f"https://sandbox.clicksign.com/api/v3/envelopes/{id_envelope}/documents"
    conteudo = gerar_base64_pdf()

    payload = {
        "data": {
            "type": "documents",
            "attributes": {
                "filename": "modelo_vale.docx",
                "template": {
                    "key": "df8c6ebc-5db3-4186-b1ee-cf3cd8fb2a7e",
                    "data": {}
                }
            }
        }
    }

    response = requests.post(url, json=payload, headers=HEADERS)

    if response.status_code == 201:
        print("Documento criado no envelope")
        data = response.json()
        return data["data"]["id"]
    else:
        print("Erro ao criar o documento")
        print("Status:", response.status_code)
        print("Resposta:", response.text)
        return None
