import streamlit as st
import pandas as pd

caminho_compras = "datasets/compras.csv"
df_compra = pd.read_csv(caminho_compras, sep=";", decimal=",", index_col=0)

colunas = list(df_compra.columns)
colunas_selecionadas = st.sidebar.multiselect("Selecione as colunas:", colunas, colunas)

col1, col2 = st.sidebar.columns(2)
col_filtro = col1.selectbox("Selecione a coluna", 
               [c for c in colunas if c not in["id_compra"]])
valor_filtro = col2.selectbox("Selecione um valor:",
                              list(df_compra[col_filtro].unique()))

st_filtrar = col1.button("Filtrar")
St_limpar = col2.button("Limpar")

if st_filtrar:
    st.dataframe(df_compra.loc[df_compra[col_filtro] == valor_filtro, colunas_selecionadas])
elif St_limpar:
    st.dataframe(df_compra[colunas_selecionadas])
else:
    st.dataframe(df_compra[colunas_selecionadas])
