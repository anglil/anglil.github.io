import os
import fitz
import cv2
import numpy as np
import glob
from bs4 import BeautifulSoup

print("1. Cleaning up images dir...")
img_dir = "college-electrical-engineering/images"
for f in glob.glob(os.path.join(img_dir, "*.png")):
    os.remove(f)

pdfs = [
    ("notes/circuits principles, experiments, and semiconductors.pdf", "ch01", "Circuits Principles, Experiments, and Semiconductors"),
    ("notes/communication circuits.pdf", "ch02", "Communication Circuits"),
    ("notes/antennae.pdf", "ch03", "Antennae"),
    ("notes/digital electronics.pdf", "ch04", "Digital Electronics")
]

kernel = np.ones((10, 10), np.uint8)
chapter_html_content = { "ch01": "", "ch02": "", "ch03": "", "ch04": "" }

print("2. Processing pages (Diagrams only, extracting cached text)...")
temp_image_path = os.path.join(img_dir, "temp_page.png")

for i, (pdf_path, ch_id, title) in enumerate(pdfs):
    doc = fitz.open(pdf_path)
    
    # Extract existing text from HTML to avoid 4 hour OCR/Translation
    with open(f"college-electrical-engineering/{ch_id}.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    pages = soup.find_all('div', class_='page-content')
    if len(pages) != len(doc):
        print(f"Warning: Page count mismatch for {ch_id}. HTML has {len(pages)}, PDF has {len(doc)}. Using min.")
    
    print(f"Processing {ch_id}: {title} ({len(doc)} pages)...")
    
    for page_num in range(min(len(doc), len(pages))):
        print(f"  Page {page_num + 1}/{len(doc)}")
        
        # Get cached text
        page_html = pages[page_num]
        p_tags = page_html.find_all('p')
        formatted_text = "".join([str(p) + "\n" for p in p_tags])
        
        # Generate image for CV
        page = doc.load_page(page_num)
        pix = page.get_pixmap(dpi=150)
        pix.save(temp_image_path)
        
        # --- Diagram Extraction ---
        img = cv2.imread(temp_image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Canny edge detection
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
        contours, hierarchy = cv2.findContours(closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        height, width = img.shape[:2]
        page_area = width * height
        diag_count = 0
        diagram_html = ""
        
        if hierarchy is not None:
            hierarchy = hierarchy[0]
            for idx, c in enumerate(contours):
                if hierarchy[idx][3] == -1: # Outer contour
                    x, y, w, h = cv2.boundingRect(c)
                    area = w * h
                    aspect_ratio = float(w) / h if h > 0 else 0
                    area_pct = area / page_area
                    
                    if 0.05 < area_pct < 0.40 and w < 0.90 * width and h > 50 and 0.3 < aspect_ratio < 4.0:
                        margin = 15
                        x1 = max(0, x - margin)
                        y1 = max(0, y - margin)
                        x2 = min(width, x + w + margin)
                        y2 = min(height, y + h + margin)
                        
                        cropped = img[y1:y2, x1:x2]
                        diag_count += 1
                        out_name = f"crop_{ch_id}_page_{page_num+1:03d}_{diag_count}.png"
                        cv2.imwrite(os.path.join(img_dir, out_name), cropped)
                        diagram_html += f'    <img src="images/{out_name}" class="page-img diagram-img" style="max-width:80%; height:auto; display:block; margin: 20px auto; border: 1px solid #ccc; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" alt="Extracted Diagram">\n'

        chapter_html_content[ch_id] += f"<div class='page-content'>\n{formatted_text}\n{diagram_html}</div>\n<hr style='margin: 40px 0;'>\n"
        
if os.path.exists(temp_image_path):
    os.remove(temp_image_path)

print("3. Rebuilding HTML chapters...")
for i, (pdf_path, ch_id, title) in enumerate(pdfs):
    ch_num = i + 1
    html_head = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Chapter {ch_num}: {title} | College Electrical Engineering</title>
  <link rel="stylesheet" href="style.css">
  <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
  <script>
      window.MathJax = {{
          tex: {{
              inlineMath: [["$", "$"], ["\\\\(", "\\\\)"]],
              displayMath: [["$$", "$$"], ["\\\\[", "\\\\]"]],
              macros: {{
                  bm: ["\\\\boldsymbol{{#1}}", 1]
              }}
          }}
      }};
  </script>
  <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
<body>

<button id="menu-toggle" onclick="document.getElementById('sidebar').classList.toggle('open')">☰</button>

<aside id="sidebar">
  <div class="book-title">College Electrical Eng<span>Angli Liu</span></div>
  <nav>
    <ul>
      <li><a href="index.html">Table of Contents</a></li>
      <li><div class="part-label">Contents</div></li>
      <li><a href="ch01.html"{' class="active"' if ch_num == 1 else ''}>Chapter 1: Circuits & Semiconductors</a></li>
      <li><a href="ch02.html"{' class="active"' if ch_num == 2 else ''}>Chapter 2: Communication Circuits</a></li>
      <li><a href="ch03.html"{' class="active"' if ch_num == 3 else ''}>Chapter 3: Antennae</a></li>
      <li><a href="ch04.html"{' class="active"' if ch_num == 4 else ''}>Chapter 4: Digital Electronics</a></li>
    </ul>
  </nav>
</aside>

<main id="content">
  <div class="chapter-header">
    <h1>Chapter {ch_num}</h1>
    <h2 class="chapter-title">{title}</h2>
  </div>
"""
    html_tail = """
</main>
</body>
</html>
"""
    full_html = html_head + chapter_html_content[ch_id] + html_tail
    with open(f"college-electrical-engineering/{ch_id}.html", "w", encoding="utf-8") as f:
        f.write(full_html)

print("Done!")
