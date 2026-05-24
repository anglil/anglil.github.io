import fitz
import os

pdfs = [
    ("notes/circuits principles, experiments, and semiconductors.pdf", "Circuits Principles, Experiments, and Semiconductors"),
    ("notes/communication circuits.pdf", "Communication Circuits"),
    ("notes/antennae.pdf", "Antennae"),
    ("notes/digital electronics.pdf", "Digital Electronics")
]

os.makedirs("college-electrical-engineering/images", exist_ok=True)

for i, (pdf_path, title) in enumerate(pdfs):
    ch_num = i + 1
    ch_id = f"ch{ch_num:02d}"
    print(f"Processing {title}...")
    
    doc = fitz.open(pdf_path)
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        # 150 DPI is standard
        pix = page.get_pixmap(dpi=150)
        img_filename = f"{ch_id}_page_{page_num+1:03d}.png"
        img_path = os.path.join("college-electrical-engineering/images", img_filename)
        pix.save(img_path)

print("All diagrams extracted!")
