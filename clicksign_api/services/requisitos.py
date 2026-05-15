import requests
from clicksign_api.config import BASE_URL, HEADERS
def criar_requisitos(envelope_id, document_id, signer_id):
    """Essa função cria um requisito para o envelope, vinculando um documento a um signatario"""

    url = f"{BASE_URL}/envelopes/{envelope_id}/requirements"

    payload_qualifica = {
        "data": {
            "type": "requirements",
            "attributes": {
                "action": "agree",
                "role": "sign"
            },
            "relationships": {
                "document": {
                    "data": {
                        "type": "documents",
                        "id": document_id
                    }
                },
                "signer": {
                    "data": {
                        "type": "signers",
                        "id": signer_id
                    }
                }
            }
        }
    }
    response = requests.post(url, json=payload_qualifica, headers=HEADERS)

    payload_autentica = {
    "data": {
        "type": "requirements",
        "attributes": {
            "action": "provide_evidence",
            "auth": "email"
        },
        "relationships": {
            "document": {
                "data": {
                    "type": "documents",
                    "id": document_id
                }
            },
            "signer": {
                "data": {
                    "type": "signers",
                    "id": signer_id
                }
            }
        }
    }
}
    request2 = requests.post(url, json=payload_autentica, headers=HEADERS)

    if response.status_code == 201:
        print("Requisito de qualificação criado no envelope")
    if request2.status_code == 201:
        print("requisito de autenticacao no envelope")
