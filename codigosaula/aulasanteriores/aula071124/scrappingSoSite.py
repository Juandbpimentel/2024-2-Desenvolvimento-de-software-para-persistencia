from bs4 import BeautifulSoup
import requests

# Conexão com a página e extração do título
response = requests.get("https://quotes.toscrape.com/")
doc = BeautifulSoup(response.content, "html.parser")
title = doc.title.string

# Exemplo de impressão do título
print("Título:", title)

