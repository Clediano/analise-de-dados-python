"""Versão alternativa da análise usando pandas (Requisito Opcional RO1).

Lê o mesmo transacoes.csv, aplica as mesmas regras de validação da solução
nativa, agrupa por mês com groupby e compara as métricas com relatorio.json.
"""

import json

import pandas as pd

ARQUIVO_CSV = "transacoes.csv"
ARQUIVO_JSON = "relatorio.json"
TIPOS_VALIDOS = {"credito", "debito"}
TOLERANCIA = 0.01


def carregar_dados(caminho=ARQUIVO_CSV):
    """Lê o CSV com pd.read_csv mantendo todas as colunas como texto."""
    return pd.read_csv(caminho, dtype=str, keep_default_na=False)


def limpar_dados(df):
    """Aplica as regras de validação e retorna apenas as linhas válidas."""
    df = df.apply(lambda coluna: coluna.str.strip())
    df["id_num"] = pd.to_numeric(df["id"], errors="coerce")
    df["valor_num"] = pd.to_numeric(df["valor"], errors="coerce")
    df["data_dt"] = pd.to_datetime(df["data"], format="%Y-%m-%d", errors="coerce")
    df["tipo"] = df["tipo"].str.lower()

    validas = (
        df["id_num"].notna()
        & (df["id_num"] % 1 == 0)
        & (df["cliente_id"] != "")
        & df["data_dt"].notna()
        & df["tipo"].isin(TIPOS_VALIDOS)
        & (df["valor_num"] > 0)
    )
    limpo = df[validas].drop_duplicates(subset="id_num", keep="first").copy()
    limpo["mes"] = limpo["data_dt"].dt.strftime("%Y-%m")
    return limpo


def calcular_resumo(df):
    """Agrupa por mês e calcula as métricas mensais."""
    df = df.assign(
        credito=df["valor_num"].where(df["tipo"] == "credito", 0.0),
        debito=df["valor_num"].where(df["tipo"] == "debito", 0.0),
    )
    resumo = df.groupby("mes").agg(
        quantidade=("valor_num", "count"),
        total_credito=("credito", "sum"),
        total_debito=("debito", "sum"),
        media=("valor_num", "mean"),
        maior_valor=("valor_num", "max"),
        menor_valor=("valor_num", "min"),
    )
    resumo["saldo"] = resumo["total_credito"] - resumo["total_debito"]
    colunas = ["quantidade", "total_credito", "total_debito", "saldo",
               "media", "maior_valor", "menor_valor"]
    return resumo[colunas].round(2)


def comparar_com_nativo(resumo, caminho_json=ARQUIVO_JSON):
    """Compara as métricas do pandas com as do relatorio.json gerado pela solução nativa."""
    try:
        with open(caminho_json, encoding="utf-8") as arquivo:
            nativo = json.load(arquivo)["resumo_mensal"]
    except FileNotFoundError:
        print(f"Arquivo '{caminho_json}' não encontrado. Execute a solução nativa antes.")
        return False

    diferencas = []
    if sorted(nativo) != sorted(resumo.index):
        diferencas.append(f"meses diferentes: {sorted(nativo)} x {list(resumo.index)}")
    for mes, linha in resumo.iterrows():
        metricas_nativas = nativo.get(mes, {})
        for metrica, valor_pandas in linha.items():
            valor_nativo = metricas_nativas.get(metrica)
            if isinstance(valor_nativo, dict):
                valor_nativo = valor_nativo["valor"]
            if valor_nativo is None or abs(valor_nativo - valor_pandas) > TOLERANCIA:
                diferencas.append(f"{mes}/{metrica}: nativo={valor_nativo} pandas={valor_pandas}")

    if diferencas:
        print("Divergências encontradas:")
        for diferenca in diferencas:
            print(" -", diferenca)
        return False
    print("Resultados idênticos aos da solução nativa ✔")
    return True


def main():
    bruto = carregar_dados()
    limpo = limpar_dados(bruto)
    print(f"Linhas lidas: {len(bruto)} | Válidas: {len(limpo)} | Inválidas: {len(bruto) - len(limpo)}")
    resumo = calcular_resumo(limpo)
    print()
    print(resumo.to_string())
    print()
    comparar_com_nativo(resumo)
    return resumo


if __name__ == "__main__":
    main()
