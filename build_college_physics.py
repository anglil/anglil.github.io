import fitz
import os

pdfs = [
    ("notes/thermodynamics.pdf", "Thermodynamics"),
    ("notes/quantum mechanics.pdf", "Quantum Mechanics"),
    ("notes/electromagnetics.pdf", "Electromagnetics"),
    ("notes/optics_1.pdf", "Optics I"),
    ("notes/optics_2.pdf", "Optics II")
]

chapters = []

for i, (pdf_path, title) in enumerate(pdfs):
    ch_num = i + 1
    ch_id = f"ch{ch_num:02d}"
    print(f"Processing {title}...")
    
    doc = fitz.open(pdf_path)
    img_tags = []
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        # 150 DPI is usually good for legibility without being too huge
        pix = page.get_pixmap(dpi=150)
        img_filename = f"{ch_id}_page_{page_num+1:03d}.png"
        img_path = os.path.join("college-physics/images", img_filename)
        pix.save(img_path)
        img_tags.append(f'<img src="images/{img_filename}" class="page-img" alt="Page {page_num+1}">')
        
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Chapter {ch_num}: {title} | College Physics</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>

<button id="menu-toggle" onclick="document.getElementById('sidebar').classList.toggle('open')">☰</button>

<aside id="sidebar">
  <div class="book-title">College Physics<span>Angli Liu</span></div>
  <nav>
    <ul>
      <li><a href="index.html">Table of Contents</a></li>
      <li><div class="part-label">Contents</div></li>
      <li><a href="ch01.html"{' class="active"' if ch_num == 1 else ''}>Chapter 1: Thermodynamics</a></li>
      <li><a href="ch02.html"{' class="active"' if ch_num == 2 else ''}>Chapter 2: Quantum Mechanics</a></li>
      <li><a href="ch03.html"{' class="active"' if ch_num == 3 else ''}>Chapter 3: Electromagnetics</a></li>
      <li><a href="ch04.html"{' class="active"' if ch_num == 4 else ''}>Chapter 4: Optics I</a></li>
      <li><a href="ch05.html"{' class="active"' if ch_num == 5 else ''}>Chapter 5: Optics II</a></li>
    </ul>
  </nav>
</aside>

<main id="content">
  <div class="chapter-header">
    <h1>Chapter {ch_num}</h1>
    <h2 class="chapter-title">{title}</h2>
  </div>
  <div class="pages-container">
    """ + "\n    ".join(img_tags) + """
  </div>
</main>
</body>
</html>
"""
    with open(f"college-physics/{ch_id}.html", "w") as f:
        f.write(html_content)

print("All chapters built!")
