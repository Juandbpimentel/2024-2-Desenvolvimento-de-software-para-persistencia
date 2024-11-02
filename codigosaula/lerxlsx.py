import pandas as pd

dfs = pd.read_excel('planilhadepessoas.xlsx',sheet_name=None)

print(dfs.keys())
print(dfs['pessoas'])

for nomeAba, aba in dfs.items():
    print('\n\n')
    print(nomeAba)
    print(aba)
