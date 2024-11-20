from PyPDF2 import PdfReader

reader = PdfReader("table.pdf")
for page in reader.pages:
    print(page.extract_text())
