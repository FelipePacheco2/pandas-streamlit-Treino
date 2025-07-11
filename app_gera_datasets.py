import random, names
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path


pasta_datasets = Path(__file__).parent / 'datasets'
pasta_datasets.mkdir(parents=True, exist_ok=True)

LOJAS = [ 
    {"estados": "SP", "cidade": "São Paulo",
     "vendedores":["Ana Oliveira", "Lucas Pereira"]},
    {"estados": "MG", "cidade": "Belo Horizonte",
    "vendedores":["Carlos Silva", "Fernanda Costa"]},
    {"estados": "RJ", "cidade": "Rio de Janeiro",
    "vendedores":["Juliana Almeida", "Pedro Souza"]},
    {"estados": "RS", "cidade": "Porto Alegre",
    "vendedores":["Maria Gomes", "Roberto Ferreira"]},
    {"estados": "SC", "cidade": "Florianopolis",
    "vendedores":["Gabriela Santos", "Thiago Lima"]},
]

PRODUTOS = [
    {"nome": "Smartphone Samsung Galaxy", 'id': 0, "preco": 2500},
    {"nome": "Notebook Dell Inspiron", 'id': 1, "preco": 4500},
    {"nome": "Tablet Apple Ipad", 'id': 2, "preco": 3000},
    {"nome": "Smartwatch Garmin", 'id': 3, "preco": 1200},
    {"nome": "Fones de ouvido Sony", 'id': 4, "preco": 600},
]

FORMA_PGTO = ["Cartão de credito", "Boleto", "Pix", "Dinheiro"]
GENERO_CLIENTE = ["male", "female"]

compras = []

for _ in range(2000):
    loja = random.choice(LOJAS)
    vendedor = random.choice(loja["vendedores"])
    produtos = random.choice(PRODUTOS)
    hora_compra = datetime.now() - timedelta(
        days=random.randint(1, 365),
        hours=random.randint(-5, 5),
        minutes=random.randint(-30, 30)
    )
    genero_cliente = random.choice(GENERO_CLIENTE)
    nome_cliente = names.get_full_name(genero_cliente)
    forma_pgto = random.choice(FORMA_PGTO)

    compras.append({
        "data": hora_compra,
        "id_compra": 0,
        "loja": loja["cidade"],
        "vendedor": vendedor,
        "produto": produtos["nome"],
        "cliente_nome": nome_cliente,
        "cliente_genero": genero_cliente.replace("female", "feminino").replace("male", "masculino"),
        "Forma_pagamento": forma_pgto
    })

    df_compras = pd.DataFrame(compras).set_index("data").sort_index()
    df_compras["id_compra"] = [i for i in range(len(df_compras))]

    df_lojas = pd.DataFrame(LOJAS)
    df_produtos = pd.DataFrame(PRODUTOS)


#gera em csv
df_lojas.to_csv(pasta_datasets / "lojas.csv", decimal=",", sep=";")
df_produtos.to_csv(pasta_datasets / "Produtos", decimal=",", sep=";")
df_compras.to_csv(pasta_datasets / "compras.csv", decimal=",", sep=";")

#gera em planilhas excel
df_lojas.to_excel(pasta_datasets / "lojas.xlsx")
df_produtos.to_excel(pasta_datasets / "produtos.xlsx")
df_compras.to_excel(pasta_datasets / "compras.xlsx")