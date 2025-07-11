import pandas as pd
import streamlit as st
from datetime import date, datetime, timedelta

PERC_COMISSAO = 0.05
COLUNAS_ANALISE = ["loja", "vendedor", "produto", "cliente_nome", "Forma_pagamento"]
COLUNAS_NUMERICAS = ["preco", "comissao"]
FUNCOES_AGREGADA = {"soma": "sum", "contagem": "count"}

caminhos_datasets = "datasets"

df_compra = pd.read_csv(f"{caminhos_datasets}/compra_data.csv", sep=';', decimal=",", index_col= 0, parse_dates=True)
df_produto = pd.read_csv(f"{caminhos_datasets}/produtos.csv", sep=";", decimal=",")
df_loja = pd.read_csv(f"{caminhos_datasets}/lojas.csv", sep=";", decimal=",")

df_produto = df_produto.rename(columns={"nome": "produto"})
df_compra = df_compra.reset_index()

df_compra = pd.merge(left=df_compra,
                     right=df_produto[["produto", "preco"]],
                     on="produto",
                     how="left")
df_compra = df_compra.set_index("data")
df_compra['comissao'] = df_compra["preco"] * PERC_COMISSAO
print(df_compra.columns)
indice_dinamico = st.sidebar.multiselect("Selecione os indices", COLUNAS_ANALISE)
colunas_filtradas = [c for c in COLUNAS_ANALISE if not c in indice_dinamico]
coluna_dinamica = st.sidebar.multiselect("Selecione as colunas", colunas_filtradas)
valor_analise = st.sidebar.selectbox("Selecionar a métrica", COLUNAS_NUMERICAS)
metrica_analise = st.sidebar.selectbox("Selecionar a metrica", list(FUNCOES_AGREGADA.keys()))


if len(indice_dinamico) > 0 and len(coluna_dinamica) > 0:
    metrica = FUNCOES_AGREGADA[metrica_analise]
    compras_dinamica = pd.pivot_table(
        df_compra,
        index=indice_dinamico,
        columns=coluna_dinamica,
        values=valor_analise,
        aggfunc=metrica
    )

    compras_dinamica["TOTAL_GERAL"] = compras_dinamica.sum(axis=1)
    compras_dinamica.loc["TOTAL_GERAL"] = compras_dinamica.sum(axis=0).to_list()

    st.dataframe(compras_dinamica)