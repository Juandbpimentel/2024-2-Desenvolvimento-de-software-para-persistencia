import pandas as pd
import matplotlib.pyplot as plt
# o csv tem o formato seguinte Data,Produto,Quantidade,Preco_Unitario

df = pd.read_csv("vendas.csv")
df["Total_Vendas"] = df["Quantidade"] * df["Preco_Unitario"]
totalVendas = df.groupby('Produto')['Total_Vendas'].sum()
totalVendas.plot(kind='bar')
totalVendas.head()

totalVendas.plot(kind='bar', figsize=(10, 6))
plt.title('Total de Vendas por Produto')
plt.xlabel('Produtos')
plt.ylabel('Total de Vendas')
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
plt.tight_layout()  # Adjust layout to prevent overlapping elements
plt.show()

df["Data"] = pd.to_datetime(df["Data"], dayfirst=True)
mascara = (df["Data"].dt.year == 2023) & (df["Data"].dt.month == 1)
vendas_janeiro_2023 = df.loc[mascara]
vendas_janeiro_2023.to_csv("vendas_janeiro.csv", index=False)
vendas_janeiro_2023.head()

with pd.ExcelWriter("total_vendas_produto.xlsx") as writer:
    produtos = vendas_janeiro_2023.groupby(['Produto'])['Produto']
    for produto in produtos.unique():
        produto = str(produto).replace('[','').replace(']','').replace('\'','')
        vendas_do_produto = vendas_janeiro_2023[vendas_janeiro_2023.Produto.isin([produto])]
        vendas_do_produto.to_excel(
            writer,
            sheet_name=produto,
            index=False
        )

dfTotalVendas = pd.read_excel("total_vendas_produto.xlsx", sheet_name=None)
dfTotalVendas['Produto A']