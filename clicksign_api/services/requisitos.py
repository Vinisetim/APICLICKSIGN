import requests
from clicksign_api.config import BASE_URL, HEADERS

def criar_requisitos(envelope_id, document_id, signer_id, role = "sign", auth = "email"):
    """Essa função cria um requisito para o envelope, vinculando um documento a um signatario.
    Está separada em duas etapas, uma de autenticação e uma Assinatura, no fim retorna o id dos requisitos.
    """

    url = f"{BASE_URL}/envelopes/{envelope_id}/requirements"

    payload_assinatura = {
        "data": {
            "type": "requirements",
            "attributes": {
                "action": "agree",
                "role": role
            },
            "relationships": {
                "document": {"data": {"type": "documents", "id": document_id}},
                "signer": {"data": {"type": "signers", "id": signer_id}}
            }
        }
    }

    response_assinatura = requests.post(url, json=payload_assinatura, headers=HEADERS)

    if response_assinatura.status_code != 201:
        print("Erro ao criar requisito de assinatura")
        print("Status:", response_assinatura.status_code)
        print("Resposta:", response_assinatura.text)
        return None, None

    requirement_assinatura_id = response_assinatura.json()["data"]["id"]

    payload_autenticacao = {
        "data": {
            "type": "requirements",
            "attributes": {
                "action": "provide_evidence",
                "auth": auth
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

    response_autenticacao = requests.post(url, json=payload_autenticacao, headers=HEADERS)

    if response_autenticacao.status_code != 201:
        print("Erro ao criar requisito de autenticação")
        print("Status:", response_autenticacao.status_code)
        print("Resposta:", response_autenticacao.text)
        return requirement_assinatura_id, None

    requirement_autenticacao_id = response_autenticacao.json()["data"]["id"]

    print(f"Requisito de autenticação criado: {requirement_autenticacao_id}")
    print(f"Requisito de assinatura criado: {requirement_assinatura_id}")

    return requirement_assinatura_id, requirement_autenticacao_id

