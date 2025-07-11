import pandas as pd
import streamlit as st
from datetime import date, datetime, timedelta

caminhos_datasets = "datasets"

df_compra = pd.read_csv(f"{caminhos_datasets}/compra_data.csv", sep=';', decimal=",", index_col= 0, parse_dates=True)
df_produto = pd.read_csv(f"{caminhos_datasets}/produtos.csv", sep=";", decimal=",")
df_loja = pd.read_csv(f"{caminhos_datasets}/lojas.csv", sep=";", decimal=",")

#renomear coluna
df_produto = df_produto.rename(columns={"nome": "produto"})

df_compra = df_compra.reset_index()

#concatenar colunas
df_compra = pd.merge(left=df_compra,
                     right=df_produto[["preco", "produto"]],
                     on="produto",
                     how="left")

df_compra = df_compra.set_index("data")
df_compra['comissao'] = df_compra["preco"] * 0.05

data_default = df_compra.index[-1].date()
data_inicio = st.sidebar.date_input("Data Inicio", data_default - timedelta(days=6))
data_final = st.sidebar.date_input("Data Final", data_default)

#filtropara datas
df_compra_filter = df_compra[(df_compra.index.date >= data_inicio) & 
                             (df_compra.index.date < data_final + timedelta(days=1))]

st.markdown("# Número Gerais")
col1, col2 = st.columns(2)

valor_compras = df_compra_filter["preco"].sum()
valor_compras = f"R$ {valor_compras:.2f}"

#filtrando valor e quantidade de produtos referente a data selecionadas
col1.metric("Valor de compras no periodo", valor_compras)
col2.metric("Quantidade de compras no periodo", df_compra_filter["preco"].count())

st.divider()
principal_loja = df_compra_filter["loja"].value_counts().index[0]
st.markdown(f"# Loja Destaque: {principal_loja}")

col21, col22 = st.columns(2)

#filtrando valor e quantidade
valor_compras_loja = df_compra_filter[df_compra_filter["loja"] == principal_loja]["preco"].sum()
valor_compras = f"R$ {valor_compras_loja:.2f}"

quantide_compras_loja = df_compra_filter[df_compra_filter["loja"] == principal_loja]["preco"].count()

#tela
col21.metric("Valor de compras no periodo", valor_compras_loja)
col22.metric("Quantidade de compras no periodo", quantide_compras_loja)

st.divider()

#melhor vendedor
principal_vendedor = df_compra_filter["vendedor"].value_counts().index[0]
st.markdown(f"# Principal Vendedor: {principal_vendedor}")

valor_compra_vendedor = df_compra_filter[df_compra_filter["vendedor"] == principal_vendedor]["preco"].sum()
valor_compra_vendedor = f"R$ {valor_compra_vendedor:.2f}"

valor_comissao = df_compra_filter[df_compra_filter["vendedor"] == principal_vendedor]["comissao"].sum()
valor_comissao = f"R$ {valor_comissao:.2f}"

col31, col32 = st.columns(2)
col31.metric(f"Valor de compras no periodo:", valor_compra_vendedor)
col32.metric(f"Comissão no periodo", valor_comissao)