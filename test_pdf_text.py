import fitz

pdf_path = "notes/circuits principles, experiments, and semiconductors.pdf"
doc = fitz.open(pdf_path)
page = doc.load_page(3) # 4th page
text = page.get_text()
print("Extracted text length:", len(text))
print("Text snippet:", repr(text[:200]))
