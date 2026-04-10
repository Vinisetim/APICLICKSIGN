import requests
import base64
from pathlib import Path
#---------------- Variáveis Globais ----------------#
url_envelope = "https://sandbox.clicksign.com/api/v3/envelopes"

headers = {
    "accept": "application/json",
    "content-type": "application/vnd.api+json",
    "authorization": "a49cd34f-17b1-414a-b622-ea8c54829e5c",
}

basedir= Path(__file__).resolve().parent
arquivo = basedir / "Documento" / "documento.docx"


#criar envelopoes
def criar_envelope():
    """"Essa função vai criar o envelope (atribuir valores variáveis)"""
    payload = "{\"data\":{\"type\":\"envelopes\",\"attributes\":{\"name\":\"Envelope de Teste\",\"locale\":\"pt-BR\",\"auto_close\":true,\"remind_interval\":3,\"block_after_refusal\":false}}}"
    response = requests.post(url_envelope, data=payload, headers=headers)
    if response.status_code == 201:
        print("Envelope criado")
    elif response.status_code == 400:
        print("Erro ao criar o envelope")


def obter_id_envelope():
    """Função necessária para guardar o ID do envelope"""
    #obtém os dados do envelope
    response = requests.get(url_envelope, headers=headers)
    #guarda esses dados em json
    envelopes = response.json()
    print(envelopes)

    #guarda a chave data
    data = envelopes["data"]

    if data and len(data) > 0:
        envelope_id = data[0]["id"]
        return envelope_id
    else:
        return None


def ativar_envelope(envelope_id):
    url = f"https://sandbox.clicksign.com/api/v3/envelopes/{envelope_id}/activate"
    response = requests.post(url, headers=headers)
    if response.status_code == 202:
        print("Envelope ativo")
    else:
        print("Erro ao ativar o envelope")

    # url_ativar = f"https://sandbox.clicksign.com/api/v3/envelopes/{envelope_id}"
    # payload = "{\"data\":{\"type\":\"envelopes\",\"attributes\":{\"status\":\"running\",\"name\":\"autodeinfracao\",\"locale\":\"pt-BR\",\"auto_close\":true},\"id\":123}}"
    # response = requests.post(url_ativar, data = payload, headers = headers)
    # if response.status_code == 200:
    #     print("Envelope ativo e Rodando")
    # else :
    #     print("Erro ao ativar o rodando")

def gerar_base64():
    """Converte o arquivo a ser assinado em B64"""
    with open(arquivo, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def criar_documento():
    """Cria o documento no envelope, visualiza o documento do envelope"""
    url = f"https://sandbox.clicksign.com/api/v3/envelopes/{obter_id_envelope()}/documents"
    payload ={
        "data":{
            "type":"documents",
            "attributes":{
                "filename" : "Multa.pdf",
                "content_base64": gerar_base64(),
            }
        }
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 201:
        print("Documento no envelope")
    else:
        print("Erro ao criar o documento")
    

if arquivo.exists():
    print("Arquivo carregado")
else: print("Arquivo inexistente")
criar_envelope()
criar_documento()
ativar_envelope(obter_id_envelope())