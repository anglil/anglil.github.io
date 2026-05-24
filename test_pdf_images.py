import fitz
doc = fitz.open("notes/circuits principles, experiments, and semiconductors.pdf")
print("Total pages:", len(doc))
for i in range(5):
    page = doc.load_page(i)
    images = page.get_images()
    print(f"Page {i} has {len(images)} images.")
