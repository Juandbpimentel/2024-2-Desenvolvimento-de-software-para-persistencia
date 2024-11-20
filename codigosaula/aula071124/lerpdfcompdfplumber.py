import pdfplumber

with pdfplumber.open("table.pdf") as pdf:
    for page in pdf.pages:
        print(page.extract_text())
