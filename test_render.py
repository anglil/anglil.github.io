import fitz

doc = fitz.open('notes/thermodynamics.pdf')
page = doc.load_page(0)
pix = page.get_pixmap()
pix.save("test_page_0.png")
print("Saved test_page_0.png successfully!")
