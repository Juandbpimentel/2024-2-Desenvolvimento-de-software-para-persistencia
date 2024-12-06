import pytesseract
from PIL import Image

# Carregar a imagem
image = Image.open("image.jpg")

# Extrair texto da imagem
text = pytesseract.image_to_string(image)
print("Texto extraído:", text)
