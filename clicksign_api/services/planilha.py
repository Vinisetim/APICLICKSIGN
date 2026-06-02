import pandas as pd
COLUNAS_OBRIGATORIAS = [
    "AIT",
    "motorista",
    "matricula",
    "telefone",
    "placa",
    "data_infracao",
    "valor",
    "cpf",
    "PARCELAS",
    "status_vale"
]

def ler_multas(caminho_planilha):
    """Le a planilha e retorna as linhas com a coluna status_vale == não enviado"""

    #leitura do excel
    df = pd.read_excel(caminho_planilha, engine="openpyxl")

    #validar colunas obrigatórias
    for coluna in COLUNAS_OBRIGATORIAS:
        if coluna not in df.columns:
            raise ValueError(f"Coluna obrigatória não encontrada: {coluna}")

    #filtro dos que devem ser enviados
    df_filtrado = df[df["status_vale"] == "Não enviado"]

    #remove linhas que não possuem dados nas colunas:
    df_filtrado = df_filtrado.dropna(subset=[
        "AIT",
        "motorista",
        "telefone"
    ])

    multas = df_filtrado.to_dict(orient="records")

    return multas