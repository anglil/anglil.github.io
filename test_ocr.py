import fitz
import pytesseract
from PIL import Image
import os

pdf_path = "notes/circuits principles, experiments, and semiconductors.pdf"
doc = fitz.open(pdf_path)
page = doc.load_page(3) # 4th page
pix = page.get_pixmap(dpi=150)
img_path = "test_page_4.png"
pix.save(img_path)

img = Image.open(img_path)

# Try english first, then chinese
try:
    text_en = pytesseract.image_to_string(img, lang='eng')
    print("--- English OCR ---")
    print(text_en[:500])
except Exception as e:
    print("English OCR failed:", e)

try:
    text_chi = pytesseract.image_to_string(img, lang='chi_sim')
    print("\n--- Chinese OCR ---")
    print(text_chi[:500])
except Exception as e:
    print("Chinese OCR failed:", e)

os.remove(img_path)
