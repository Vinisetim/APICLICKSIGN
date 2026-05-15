
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

def detalhes_envelope():
    url = f"https://sandbox.clicksign.com/api/v3/envelopes/{id_envelope}"

    response = requests.get(url, headers=headers)
    print(response.text)

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

    response = requests.post(url, data=json.dumps(payload), headers=headers)

    if response.status_code ==  201:
        data = response.json()
        nome = data["data"]["attributes"]["name"]
        email = data["data"]["attributes"]["email"]
        identificador = data["data"]["id"]
        print(f"Signaário {nome} Adicionado no envelope {id_envelope} com o email {email}")
        print(response.text)
        print(identificador)
        return identificador
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
    response = requests.post(url, json=payload_qualifica, headers=headers)

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
    request2 = requests.post(url, json=payload_autentica, headers=headers)

    if response.status_code == 201:
        print("Requisito de qualificação criado no envelope")
    if request2.status_code == 201:
        print("requisito de autenticacao no envelope")


def notificar_signatario():
    """Função para notificar o signatario que existem documentos a serem assinados"""

    url = f"https://sandbox.clicksign.com/api/v3/envelopes/{id_envelope}/signers/{id_signatario}/notifications"

    payload = "{\"data\":{\"type\":\"notifications\",\"attributes\":{\"email_customization\":{\"subject\":\"Qualquer Coisa\",\"head\":\"Qualquer Coisa\",\"greeting\":\"Qualquer Coisa\",\"principal\":\"Qualquer Coisa\",\"button\":\"Qualquer Coisa\",\"final\":\"Qualquer Coisa\",\"align\":\"justify\",\"show_token\":true,\"show_qrcode\":true,\"show_details\":true}}}}"


    response = requests.post(url, data= payload, headers=headers)
    if response.status_code == 200:
        print("Configuração de notificação finalizada")
        print(response.status_code)
    else:
        print("Erro ao notificar Signatario Status:", response.status_code, response.text)


def listar_requisitos():
    url = f"https://sandbox.clicksign.com/api/v3/envelopes/{id_envelope}/requirements"
    response = requests.get(url, headers=headers)
    data = response.json()

    print("IDs dos requisitos:")
    for req in data["data"]:
        print(req["id"])
        return req["id"]
    return None


def ver_requirement():
    url = f"https://sandbox.clicksign.com/api/v3/envelopes/{id_envelope}/requirements/{requirement_id}"
    response = requests.get(url, headers=headers)
    print(response.json())


if __name__ == "__main__":
    #Cria o envelope e o documento salvando seus IDs
    id_envelope = criar_envelope()
    id_documento = criar_documento()
    print("id Documento: ", id_documento)

    #Cria e adiciona signatario no documento criado salvando seu ID
    id_signatario = adicionar_signatario()
    print("id Signatario",id_signatario)

    #Cria requisito de autenticação e qualificação no documento, vinculando signatário e documento
    criar_requisito()
    requirement_id = listar_requisitos()
    ver_requirement()
    #Ativa o envelope
    detalhes_envelope()
    ativar_envelope()
    notificar_signatario()
