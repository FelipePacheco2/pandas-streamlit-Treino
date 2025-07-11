from datetime import datetime
import streamlit as st
import pandas as pd

caminho_datasets = "pandas-streamlit-Treino/datasets"

df_compras = pd.read_csv(f"{caminho_datasets}/compra_data.csv", sep=";", decimal=",", index_col=0)
df_lojas = pd.read_csv(f"{caminho_datasets}/lojas.csv", sep=";", decimal=",", index_col=0)
df_produtos = pd.read_csv(f"{caminho_datasets}/produtos.csv", sep=";", decimal=",", index_col=0)

df_lojas["Cidade/estados"] = df_lojas["cidade"] + '/' + df_lojas['estados']
lista_loja = df_lojas["Cidade/estados"].to_list()
loja_selecionadas = st.sidebar.selectbox("Selecione a loja:", lista_loja)

lista_vendedores = df_lojas.loc[df_lojas["Cidade/estados"] == loja_selecionadas, "vendedores"].iloc[0]
lista_vendedores = lista_vendedores.strip("][").replace("'", " ").split(", ")
vendedores_select = st.sidebar.selectbox("Selecionar Vendedor:", lista_vendedores)

#criando ambas para selecionar
list_produtos = df_produtos["nome"].to_list()

produtos_select = st.sidebar.selectbox("Selecione o produto: ", list_produtos)
nome_cliente = st.sidebar.text_input("Nome do Cliente")
genero_select = st.sidebar.selectbox("Genero do Cliente:", ["masculino", "feminino"])
pgto_select = st.sidebar.selectbox("Forma de pagamento:", ["Cartão de credito", "Boleto", "Pix", "Dinheiro"])


#adicionar compras
if st.sidebar.button("Adicionar Nova Compra"):
    lista_adicionar = [df_compras["id_compra"].max() + 1 if not df_compras.empty else 1,
                       loja_selecionadas,
                       vendedores_select,
                       produtos_select,
                       nome_cliente,
                       genero_select,
                       pgto_select
                       ]
        
    df_compras.loc[datetime.now()] = lista_adicionar
    df_compras.to_csv(f"{caminho_datasets}/compra_data", index=False, decimal=",", sep=";")
    st.success("Compra adicionada")
st.dataframe(df_compras)