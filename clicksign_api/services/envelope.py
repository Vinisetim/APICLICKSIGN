import requests
from clicksign_api.config import BASE_URL, HEADERS

def criar_envelope(nome_envelope):
    """Função para criar um novo envelo na clicksign, inicio do fluxo"""
    url = f"{BASE_URL}/envelopes"

    payload = {
        "data": {
            "type": "envelopes",
            "attributes": {
                "name": nome_envelope,
                "locale": "pt-BR",
                "auto_close": True,
                "remind_interval": 3,
                "block_after_refusal": False
            }
        }
    }

    response = requests.post(url, json=payload, headers=HEADERS)

    #Se o status code for 201
    if response.status_code == 201:
        #Guarda o campo id que vem pelo response.json
        identificador = response.json()["data"]["id"]

        #o mesmo para o nome
        name = response.json()["data"]["attributes"]["name"]

        #print para debug
        print(f"Envelope com o nome {nome_envelope} com o id {identificador} criado com sucesso")

        #retorno de variaveis para uso em outras funções
        return identificador, name

    #em outros status.code:
    print("Erro ao criar envelope:", response.status_code, response.text)
    return None

def ativar_envelope(envelope_id):
    """Função para atualizar o status do envelpe de 'draft' para 'Runing' """

    url = f"{BASE_URL}/envelopes/{envelope_id}"
    payload = {
        "data":{
            "id": envelope_id,
            "type": "envelopes",
            "attributes": {
                "status": "running"
            }
        }
    }

    response = requests.put(url, json=payload, headers=HEADERS)

    if response.status_code in [200, 201]:
        print(f"Envelope Ativado com sucesso: {envelope_id}")
        return True #retorna true para verificação

    else:
        print("Erro ao ativar envelope")
        print(f"status code: {response.status_code}")
        print(f"texto resposta: {response.text}")
        return False