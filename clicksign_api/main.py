import time
from pathlib import Path
import requests
from clicksign_api.services.envelope import criar_envelope
from clicksign_api.services.signatario import adicionar_signatario
from clicksign_api.services.requisitos import criar_requisitos
from clicksign_api.services.documento import criar_documento
from clicksign_api.services.notificacao import notificar
from clicksign_api.config import HEADERS, BASE_URL

def ativar_envelope(envelope_id):
    url = f"{BASE_URL}/envelopes/{envelope_id}"

    payload = {
            "data": {
                "id": envelope_id,
                "type": "envelopes",
                "attributes": {
                    "status": "running"
                }
            }
        }
    response = requests.patch(url,json=payload, headers=HEADERS)
    if response.status_code in [200, 201]:
        print("envelope ativado")
    else:
        print("erro ao ativar envelope", response.status_code, response.text)



def main():
    caminho = Path("Documento/documento.pdf")

    if not caminho.exists():
        print("Documento não encontrado")
        return
    print(f"processando {caminho.name}")

    envelope_id, envelope_name = criar_envelope()
    print(envelope_name)
    print(envelope_id)
    if not envelope_id:

        return

    signer_id = adicionar_signatario(envelope_id)
    if not signer_id:
        return

    document_id = criar_documento(envelope_id, signer_id)
    if not document_id:
        return

    criar_requisitos(envelope_id, document_id, signer_id)

    url = f"{BASE_URL}/envelopes/{envelope_id}"
    response = requests.get(url, headers=HEADERS)

    print(response.json())

    import time
    time.sleep(5)

    ativar_envelope(envelope_id)

    notificar(envelope_id, signer_id)



if __name__ == "__main__":
    main()
