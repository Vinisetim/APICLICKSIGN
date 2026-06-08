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

def campo_vazio(valor):
    if valor is None:
        return True

    valor_texto = str(valor).strip()

    if valor_texto is None:
        return True

    return False

def validar_multa_processavel(multa):
    campos_obrigatorios = [
        "AIT",
        "motorista",
        "telefone",
        "cpf",
        "valor",
        "status_vale",
    ]

    campos_faltando = []

    for campo in campos_obrigatorios:
        if campo not in multa or campo_vazio(multa[campo]):
            campos_faltando.append(campo)

    if campos_faltando:
        return False, campos_faltando

    if str(multa["status_vale"]) != "Não enviado":
        return False, ["Status do vale diferente de Não Enviado"]

    return True, []

def atualizar_status_vale(caminho_planilha, ait, novo_status):
    df = pd.read_excel(caminho_planilha, engine="openpyxl")

    filtro = df["AIT"].astype(str) == str(ait)

    if not filtro.any():
        print(f"Nenhuma linha encontrada para o AIT: {ait}")
        return  False

    df.loc[filtro, "status_vale"] = novo_status

    df.to_excel(caminho_planilha, index=False, engine="openpyxl")

    print(f"Status do vale atualizado para {novo_status}`")

    return True


