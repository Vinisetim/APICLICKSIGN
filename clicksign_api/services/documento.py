import json
import requests
from clicksign_api.config import BASE_URL, HEADERS
from clicksign_api.utils.base64_utils import gerar_base64_pdf

def criar_documento(id_envelope):
    """Cria um documento dentro do envelope"""

    url = f"https://sandbox.clicksign.com/api/v3/envelopes/{id_envelope}/documents"
    conteudo = gerar_base64_pdf()
    payload = {
        "data": {
            "type": "documents",
            "attributes": {
                "filename": "Multa.pdf",
                "content_base64": conteudo,
            }
        }
    }

    payload = json.dumps(payload)
    response = requests.post(url, data=payload, headers=HEADERS)

    if response.status_code == 201:
        print("Documento criado no envelope")
        data = response.json()
        return data["data"]["id"]
    else:
        print("Erro ao criar o documento")
        print("Status:", response.status_code)
        print("Resposta:", response.text)
        return None
