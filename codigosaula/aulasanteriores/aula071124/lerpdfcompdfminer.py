from pdfminer.high_level import extract_text

text = extract_text("table.pdf")
print(text)