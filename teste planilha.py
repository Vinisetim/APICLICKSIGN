from clicksign_api.services.planilha import ler_multas
from pathlib import Path


def main():
    base_dir = Path(__file__).resolve().parent
    caminho_planilha = base_dir / "teste_clicksign.xlsx"

    multas = ler_multas(caminho_planilha)

    print(f"Total de multas para enviar: {len(multas)}")

    for multa in multas:
        print(f"AIT: {multa['AIT']} ")
        print(f"Motorista: {multa['motorista']} ")
        print(f"Telefone: {multa['telefone']}")
        print(f"Placa: {multa['placa']}")
        print(f"Valor: {multa['valor']}")
        print(f"CPF: {multa['cpf']}")
        print(f"Parcelas: {multa['PARCELAS']}")

if __name__ == "__main__":
    main()