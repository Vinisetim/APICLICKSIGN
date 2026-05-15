import requests
from clicksign_api.config import BASE_URL, HEADERS

def criar_envelope():
    url = f"{BASE_URL}/envelopes"

    payload = {
        "data": {
            "type": "envelopes",
            "attributes": {
                "name": "Envelope de Teste",
                "locale": "pt-BR",
                "auto_close": True,
                "remind_interval": 3,
                "block_after_refusal": False
            }
        }
    }

    response = requests.post(url, json=payload, headers=HEADERS)

    if response.status_code == 201:
        return response.json()["data"]["id"]

    print("Erro ao criar envelope:", response.status_code, response.text)
    return None
