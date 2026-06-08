import requests
from clicksign_api.config import BASE_URL, HEADERS

def notificar(envelope_id, signer_id):
    url = f"{BASE_URL}/envelopes/{envelope_id}/signers/{signer_id}/notifications"

    payload = {
        "data": {
            "type": "notifications",
            "attributes": {}
        }
    }

    response = requests.post(url, json=payload, headers=HEADERS)

    if response.status_code in (200, 201, 202):
        print("Signatario notificado com sucesso")
        print(response.status_code)
        return True

    print("Erro notificar:", response.text)
    print(response.status_code)
    return False