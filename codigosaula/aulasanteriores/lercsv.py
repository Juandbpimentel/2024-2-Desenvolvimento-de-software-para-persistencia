import pandas as pd

df = pd.read_csv('pessoas.csv')

print(df)
for coluna in df:
    print(coluna)
