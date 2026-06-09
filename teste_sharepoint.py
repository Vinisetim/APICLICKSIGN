from pathlib import Path

from clicksign_api.services.sharepoint import baixar_planilha_sharepoint

def main():
    base_dir = Path(__file__).resolve().parent
    destino = base_dir / "downloads" / "Teste_clicksign_sharepoint.xlsx"

    caminho_baixado = baixar_planilha_sharepoint(destino)

    print(f"Arquiv baixado em: {caminho_baixado}")

if __name__ == "__main__":
    main()

