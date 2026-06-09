import requests
from clicksign_api.config import BASE_URL, HEADERS

def adicionar_signatario(envelope_id, nome, email):
    """Usa o endpoint de signatarios com o id do envelope para identificação para adicionar o signatário no envelope.
    Atualmente usa email como identificador
    """
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
                "name": str(nome).strip(),
                "email": email,
            }
        }
    }

    response = requests.post(url, json = payload, headers=HEADERS)


    if response.status_code == 201: #se a resposta for positiva
        data = response.json()

        #guarda informações do signatario
        nome_signatario = data["data"]["attributes"]["name"]
        email_signatario = data["data"]["attributes"]["email"]
        signer_id = data["data"]["id"]

        print(
            f"Signatário {nome_signatario} adicionado ao envelope "
            f"{envelope_id} com o e-mail {email_signatario}. "
            f"Signer ID: {signer_id}"
        )
        #retorno da função
        return signer_id

    #Se der erro
    print(f"Erro signer: {response.status_code}", response.text)
    return None
