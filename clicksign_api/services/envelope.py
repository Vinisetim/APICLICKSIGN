import requests
from clicksign_api.config import BASE_URL, HEADERS

def criar_envelope(nome_envelope):
    url = f"{BASE_URL}/envelopes"

    payload = {
        "data": {
            "type": "envelopes",
            "attributes": {
                "name": nome_envelope,
                "locale": "pt-BR",
                "auto_close": True,
                "remind_interval": 3,
                "block_after_refusal": False
            }
        }
    }

    response = requests.post(url, json=payload, headers=HEADERS)

    if response.status_code == 201:
        identificador = response.json()["data"]["id"]
        name = response.json()["data"]["attributes"]["name"]
        print(f"Envelope com o nome {nome_envelope} com o id {identificador} criado com sucesso")
        return identificador, name

    print("Erro ao criar envelope:", response.status_code, response.text)
    return None
