import time

from clicksign_api.services.planilha import ler_multas
from pathlib import Path
from clicksign_api.services.envelope import criar_envelope
from clicksign_api.services.signatario import adicionar_signatario
from clicksign_api.services.requisitos import criar_requisitos
from clicksign_api.services.documento import criar_documento
from clicksign_api.services.envelope import ativar_envelope


def main():
    base_dir = Path(__file__).resolve().parent
    caminho_planilha = base_dir / "teste_clicksign.xlsx"

    multas = ler_multas(caminho_planilha)

    print(f"Total de multas para enviar: {len(multas)}")

    for multa in multas:
        nome_envelope = f"Multa{multa['AIT']}- {multa['motorista']}"

        print(f"Nome do envelope: {nome_envelope}")

        envelope_id,envelope_name = criar_envelope(nome_envelope)

        signer_id = adicionar_signatario(
            envelope_id = envelope_id,
            nome= multa['motorista'],
            email="viniciusgueimis@gmail.com",
        )
        print(f"Signer id: {signer_id}")

        document_id = criar_documento(
            envelope_id=envelope_id,
            multa=multa
        )

        print(f"Document ID: {document_id}")

        requirement_assinatura_id, requirement_autenticacao_id = criar_requisitos(
            envelope_id = envelope_id,
            document_id=document_id,
            signer_id = signer_id,
        )

        print(f"Requirement assinatura ID: {requirement_assinatura_id}")
        print(f"Requirement autenticação ID: {requirement_autenticacao_id}")

        time.sleep(5)
        envelope_ativado = ativar_envelope(envelope_id)
        print(f"Envelope ativado? : {envelope_ativado}")


        print(f"AIT: {multa['AIT']} ")
        print(f"Motorista: {multa['motorista']} ")
        print(f"Telefone: {multa['telefone']}")
        print(f"Placa: {multa['placa']}")
        print(f"Valor: {multa['valor']}")
        print(f"CPF: {multa['cpf']}")
        print(f"Parcelas: {multa['PARCELAS']}")

if __name__ == "__main__":
    main()