import requests
from clicksign_api.config import BASE_URL, HEADERS

def adicionar_signatario(envelope_id, nome = "Vinicius Santos", email = "viniciusgueimis@gmail.com"):

    url = f"{BASE_URL}/envelopes/{envelope_id}/signers"

    payload = {
        "data": {
            "type": "signers",
            "attributes": {
                "has_documentation": False,
                "refusable": False,
                "group": 1,
                "location_required_enabled": False,

                "communicate_events": {
                    "signature_request": "email",
                    "signature_reminder": "email",
                    "document_signed": "email"
                },
                "name": nome,
                "email": email,
            }
        }
    }

    response = requests.post(url, json = payload, headers=HEADERS)

    if response.status_code == 201:
        data = response.json()
        nome = data["data"]["attributes"]["name"]
        email = data["data"]["attributes"]["email"]
        identificador = data["data"]["id"]
        print(f"Signaário {nome} Adicionado no envelope {envelope_id} com o email {email} e o identificador {identificador}")

        return response.json()["data"]["id"]

    print(f"Erro signer: {response.status_code}")
    return None
