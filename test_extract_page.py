import fitz
import os

pdf_path = "notes/circuits principles, experiments, and semiconductors.pdf"
doc = fitz.open(pdf_path)
page = doc.load_page(3) # 4th page
pix = page.get_pixmap(dpi=150)
pix.save("college-electrical-engineering/images/ch01_page_004.png")
print("Saved ch01_page_004.png")
