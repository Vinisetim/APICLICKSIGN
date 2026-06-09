import pandas as pd

#Definas as colunas que são necessárias
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
    """Lê a planilha e retorna as linhas com a coluna status_vale == não enviado"""

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

    #trasforma em dicionário e retorna esse dicionário
    multas = df_filtrado.to_dict(orient="records")
    return multas

def campo_vazio(valor):
    """Trata campos sem valor"""
    if valor is None:
        return True

    valor_texto = str(valor).strip()

    if valor_texto is None:
        return True

    return False

def validar_multa_processavel(multa):
    """Valida se a linha tem informação suficiente para ser enviada"""
    campos_obrigatorios = [
        "AIT",
        "motorista",
        "telefone",
        "cpf",
        "valor",
        "status_vale",
    ]

    campos_faltando = []

    #Para cada campo faltando, adiciona a lista
    for campo in campos_obrigatorios:
        if campo not in multa or campo_vazio(multa[campo]):
            campos_faltando.append(campo)

    #Se a lista de campos faltando tem valor, retorna false
    if campos_faltando:
        return False, campos_faltando

    #Se o status do vale for diferente de "Não enviado", retorna false
    if str(multa["status_vale"]) != "Não enviado":
        return False, ["Status do vale diferente de Não Enviado"]

    #Se passar todas as verificações, retorna true e uma lista vazia
    return True, []

def atualizar_status_vale(caminho_planilha, ait, novo_status):
    """Função para mudar o valor da coluna de status_vale. Deve ser acionada por ultimo sempre"""
    df = pd.read_excel(caminho_planilha, engine="openpyxl")

    #Muda o status da linha que tem o valor do AIT igual o do ait do loop
    filtro = df["AIT"].astype(str) == str(ait)

    if not filtro.any():
        print(f"Nenhuma linha encontrada para o AIT: {ait}")
        return  False

    #define a linha pelo filtro e muda o valor
    df.loc[filtro, "status_vale"] = novo_status

    df.to_excel(caminho_planilha, index=False, engine="openpyxl")

    print(f"Status do vale atualizado para {novo_status}`")

    #Retorna true para verificação
    return True


