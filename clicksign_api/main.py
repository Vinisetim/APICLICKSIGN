import requests
import base64
from pathlib import Path
import json
#---------------- Variáveis Globais ----------------#
url_envelope = "https://sandbox.clicksign.com/api/v3/envelopes"


headers = {
    "Accept": "application/json",
    "Content-Type": "application/vnd.api+json",
    "Authorization": "cac9712a-7fcc-41ea-bb71-7f7cf2bb214a"
}


basedir= Path(__file__).resolve().parent
caminho = basedir / "Documento" / "documento.pdf"


#criar envelopoes
def criar_envelope():
    """"Essa função vai criar o envelope (atribuir valores variáveis)"""

    payload = "{\"data\":{\"type\":\"envelopes\",\"attributes\":{\"name\":\"Envelope de Teste\",\"locale\":\"pt-BR\",\"auto_close\":true,\"remind_interval\":3,\"block_after_refusal\":false}}}"

    response = requests.post(url_envelope, data=payload, headers=headers)

    if response.status_code == 201:
        print("Envelope criado")
        data = response.json()
        return data["data"]["id"]
    elif response.status_code == 400:
        print("Erro ao criar o envelope")
    return None

def ativar_envelope():
    """"Função para Ativar o envelope. Só funciona quando passar por todas as etapas"""
    url = f"https://sandbox.clicksign.com/api/v3/envelopes/{id_envelope}/activate"
    response = requests.post(url, headers=headers)
    if response.status_code == 202:
        print("Envelope ativo")
    else:
        print("Erro ao ativar o envelope")
        print(response.status_code)

def gerar_base64_pdf():
    """"Conversão do arquivo da pasta 'Documentos' para base64"""
    if caminho.exists():
        with open(caminho, "rb") as f:
            base64_bytes = base64.b64encode(f.read()).decode("utf-8")
            print("Caminho gerado com base64")
            return f"data:application/pdf;base64,{base64_bytes}"
    else:
        print("Caminho nao existe")
        return ""





def criar_documento():
    """Cria um documento dentro do envelope"""

    url = f"https://sandbox.clicksign.com/api/v3/envelopes/{id_envelope}/documents"
    conteudo = gerar_base64_pdf()
    payload = {
        "data": {
            "type": "documents",
            "attributes": {
                "filename": "Multa.pdf",
                "content_base64": conteudo,
            }
        }
    }

    payload = json.dumps(payload)
    response = requests.post(url, data=payload, headers=headers)

    if response.status_code == 201:
        print("Documento criado no envelope")
        data = response.json()
        return data["data"]["id"]
    else:
        print("Erro ao criar o documento")
        print("Status:", response.status_code)
        print("Resposta:", response.text)
        return None

def listar_signatarios():
    """"Lista os signatários presentes no envelope"""
    url = f"https://sandbox.clicksign.com/api/v3/envelopes/{id_envelope}/signers"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print(response.json())
    elif response.status_code == 404:
        print("Erro ao listar os envelopes")

def adicionar_signatario():
    """Função para adcionar um signatario no envelope"""
    url = f"https://sandbox.clicksign.com/api/v3/envelopes/{id_envelope}/signers"

    signatario = "Vinicius Santos"
    email_signatario = "viniciusgueimis@gmail.com"
    payload = {
    "data": {
        "type": "signers",
        "attributes": {
            "has_documentation": False,
            "refusable": False,
            "group": 1,
            "location_required_enabled": False,
            "communicate_events": {
                "signature_request": "none",
                "signature_reminder": "none",
                "document_signed": "email"
            },
            "name": signatario,
            "email": email_signatario,
        }
    }
}
    payload = json.dumps(payload)
    response = requests.post(url, data=payload, headers=headers)

    if response.status_code ==  201:
        data = response.json()
        nome = data["data"]["attributes"]["name"]
        email = data["data"]["attributes"]["email"]
        id= data["data"]["id"]
        print(f"Signaário {nome} Adicionado no envelope {id_envelope} com o email {email}")
        print(response.text)
        return id
    else:
        print("Erro ao adicionar o signatario no envelope")
        print("Status:", response.status_code)
        return None


def criar_requisito():
    """Essa função cria um requisito para o envelope, vinculando um documento a um signatario"""

    url = f"https://sandbox.clicksign.com/api/v3/envelopes/{id_envelope}/requirements"

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
                        "id": id_documento
                    }
                },
                "signer": {
                    "data": {
                        "type": "signers",
                        "id": id_signatario
                    }
                }
            }
        }
    }
    payload_qualifica = json.dumps(payload_qualifica)
    response = requests.post(url, data=payload_qualifica, headers=headers)

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
                    "id": id_documento
                }
            },
            "signer": {
                "data": {
                    "type": "signers",
                    "id": id_signatario
                }
            }
        }
    }
}
    payload_autentica = json.dumps(payload_autentica)
    request2 = requests.post(url, data=payload_autentica, headers=headers)

    if response.status_code == 201:
        print("Requisito de qualificação criado no envelope")
    if request2.status_code == 201:
        print("requisito de autenticacao no envelope")



if __name__ == "__main__":
    id_envelope = criar_envelope()
    id_documento = criar_documento()
    print("id Documento: ", id_documento)
    id_signatario = adicionar_signatario()
    print("id Signatario",id_signatario)
    criar_requisito()
    ativar_envelope()