import base64
from pathlib import Path


basedir = Path(__file__).resolve().parent.parent
caminho = basedir / "Documento" / "documento.pdf"


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

gerar_base64_pdf()