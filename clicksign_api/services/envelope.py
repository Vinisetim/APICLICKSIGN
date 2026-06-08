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

def ativar_envelope(envelope_id):
    url = f"{BASE_URL}/envelopes/{envelope_id}"
    payload = {
        "data":{
            "id": envelope_id,
            "type": "envelopes",
            "attributes": {
                "status": "running"
            }
        }
    }

    response = requests.put(url, json=payload, headers=HEADERS)

    if response.status_code in [200, 201]:
        print(f"Envelope Ativado com sucesso: {envelope_id}")
        return True
    else:
        print("Erro ao ativar envelope")
        print(f"status code: {response.status_code}")
        print(f"texto resposta: {response.text}")
        return False