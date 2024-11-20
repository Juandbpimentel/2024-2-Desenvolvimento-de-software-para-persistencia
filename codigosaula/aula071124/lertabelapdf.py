import tabula

# Extrai todas as tabelas de um pdf para uma lista de DataFrames
tables = tabula.read_pdf("table.pdf",pages="all")

# Exibe a primeira tabela
print(tables[0])

