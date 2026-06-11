import requests
import re
from clicksign_api.config import BASE_URL, HEADERS

def formatar_telefone(telefone):
    """
    Limpa o telefone vindo da planilha, mantendo apenas números.

    Exemplo:
    (11) 97564-9922 -> 11975649922
    """

    return re.sub(r"\D", "", str(telefone))


def adicionar_signatario(envelope_id, nome, telefone):
    """Usa o endpoint de signatarios com o id do envelope para identificação para adicionar o signatário no envelope.
    Tentativa de envio de notificação por sms
    """
    url = f"{BASE_URL}/envelopes/{envelope_id}/signers"

    telefone_formatado = formatar_telefone(telefone)

    payload = {
        "data": {
            "type": "signers",
            "attributes": {
                "has_documentation": False,
                "refusable": False,
                "group": 1,
                "location_required_enabled": False,

                "communicate_events": {
                    "signature_request": "sms",
                    "signature_reminder": "none",
                    "document_signed": "whatsapp"
                },
                "name": str(nome).strip(),
                "phone_number": telefone_formatado,
            }
        }
    }

    print("DEBUG payload signatário SMS:", payload)
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
