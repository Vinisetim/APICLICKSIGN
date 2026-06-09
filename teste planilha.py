import time
from clicksign_api.services.planilha import ler_multas, validar_multa_processavel, atualizar_status_vale
from pathlib import Path
from clicksign_api.services.envelope import criar_envelope
from clicksign_api.services.signatario import adicionar_signatario
from clicksign_api.services.requisitos import criar_requisitos
from clicksign_api.services.documento import criar_documento
from clicksign_api.services.envelope import ativar_envelope
from clicksign_api.config import EMAIL_TESTE
from clicksign_api.services.notificacao import notificar

def main():
    """fUNÇÃO PARA EXECUTAR AS REQUISIÇÕES PARA CADA LINHA DA PLANILHA"""

    #Indica o caminho da planilha (local)
    base_dir = Path(__file__).resolve().parent
    caminho_planilha = base_dir / "teste_clicksign.xlsx"

    #contagem de multas para enviar
    multas = ler_multas(caminho_planilha)
    print(f"Total de multas para enviar: {len(multas)}")

    #Para cada multa da lista...
    for multa in multas:
        #Verifica se tem os campos suficientes para executar
        pode_processar, motivo = validar_multa_processavel(multa)
        if not pode_processar:
            #Se não da um aviso e continua o loop
            print(f"Pulando AIT {multa.get('AIT')} - motivo: {motivo}")
            continue

        #variavel concatenada para nome do envelope
        nome_envelope = f"Multa{multa['AIT']}- {multa['motorista']}"
        print(f"Nome do envelope: {nome_envelope}")

        #Chama a função de criar envelopes e usa o retorno para duas variáveis que serão chave nas próximas funções
        envelope_id,envelope_name = criar_envelope(nome_envelope)

        #Adiciona 1 signatário para o envelope em questão, sendo o signatário identificado pelo seu NOME e EMAIL
        signer_id = adicionar_signatario(
            envelope_id = envelope_id,
            nome= multa['motorista'],
            email=EMAIL_TESTE,
        )
        print(f"Signer id: {signer_id}")

        #Usa o template da clicksign para criar o documento desse signatário e guarda o seu ID
        document_id = criar_documento(
            envelope_id=envelope_id,
            multa=multa
        )
        print(f"Document ID: {document_id}")

        #Linka um requisisto de assinatura e um de autenticação ao signatário, envelepe e ao documento
        requirement_assinatura_id, requirement_autenticacao_id = criar_requisitos(
            envelope_id = envelope_id,
            document_id=document_id,
            signer_id = signer_id,
        )
        print(f"Requirement assinatura ID: {requirement_assinatura_id}")
        print(f"Requirement autenticação ID: {requirement_autenticacao_id}")

        #aguarda 5 seg
        time.sleep(5)
        #Ativa o envelope e avisa com True or False
        envelope_ativado = ativar_envelope(envelope_id)
        print(f"Envelope ativado? : {envelope_ativado}")

        if envelope_ativado:
        #Se for ativado envia notificação
                signatario_notificado = notificar(
                    envelope_id = envelope_id,
                    signer_id = signer_id,
                )
                print(f"Signatario notificado? : {signatario_notificado}")
                if signatario_notificado:
                    #Se foi notificado atualiza o status do Vale
                    atualizar_status_vale(
                        caminho_planilha=caminho_planilha,
                        ait=multa['AIT'],
                        novo_status="Enviado"
                    )

    #Printa informações da planilha. Apenas para debug
        print(f"AIT: {multa['AIT']} ")
        print(f"Motorista: {multa['motorista']} ")
        print(f"Telefone: {multa['telefone']}")
        print(f"Placa: {multa['placa']}")
        print(f"Valor: {multa['valor']}")
        print(f"CPF: {multa['cpf']}")
        print(f"Parcelas: {multa['PARCELAS']}")

#Executa a função se estiver nesse arquivo
if __name__ == "__main__":
    main()