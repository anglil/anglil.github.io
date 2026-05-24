import os
import fitz
import cv2
import numpy as np
import glob
import pytesseract
from PIL import Image
from deep_translator import GoogleTranslator

print("1. Cleaning up images dir...")
img_dir = "college-electrical-engineering/images"
os.makedirs(img_dir, exist_ok=True)
for f in glob.glob(os.path.join(img_dir, "*.png")):
    os.remove(f)

print("2. Extracting pages from PDF...")
pdfs = [
    ("notes/circuits principles, experiments, and semiconductors.pdf", "ch01", "Circuits Principles, Experiments, and Semiconductors"),
    ("notes/communication circuits.pdf", "ch02", "Communication Circuits"),
    ("notes/antennae.pdf", "ch03", "Antennae"),
    ("notes/digital electronics.pdf", "ch04", "Digital Electronics")
]

chapters_data = {}

for pdf_path, ch_id, title in pdfs:
    doc = fitz.open(pdf_path)
    pages_info = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(dpi=150)
        img_filename = f"{ch_id}_page_{page_num+1:03d}.png"
        img_path = os.path.join(img_dir, img_filename)
        pix.save(img_path)
        pages_info.append(img_path)
    chapters_data[ch_id] = {"title": title, "pages": pages_info}

print("3. Extracting diagrams using advanced heuristics and running OCR...")
kernel = np.ones((40, 40), np.uint8)
translator = GoogleTranslator(source='zh-CN', target='en')

def translate_chunk(text):
    if not text.strip(): return ""
    try:
        # Translator has a character limit, but these pages won't hit it
        return translator.translate(text)
    except Exception as e:
        print("Translation error:", e)
        return text

# We will store the generated content for each chapter
chapter_html_content = {
    "ch01": "",
    "ch02": "",
    "ch03": "",
    "ch04": ""
}

for ch_id, data in chapters_data.items():
    print(f"Processing {ch_id}...")
    for page_path in data["pages"]:
        filename = os.path.basename(page_path)
        img = cv2.imread(page_path)
        if img is None: continue
        
        # --- Diagram Extraction ---
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 10)
        
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh, connectivity=8)
        diagram_mask = np.zeros_like(thresh)
        
        for i in range(1, num_labels):
            w = stats[i, cv2.CC_STAT_WIDTH]
            h = stats[i, cv2.CC_STAT_HEIGHT]
            area = stats[i, cv2.CC_STAT_AREA]
            if w > 50 or h > 50 or area > 400:
                diagram_mask[labels == i] = 255
                
        closed = cv2.morphologyEx(diagram_mask, cv2.MORPH_CLOSE, kernel)
        contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        height, width = img.shape[:2]
        page_area = width * height
        
        diag_count = 0
        diagram_html = ""
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            area = w * h
            aspect_ratio = float(w) / h if h > 0 else 0
            area_pct = area / page_area
            
            if 0.02 < area_pct < 0.40 and w < 0.85 * width and 0.3 < aspect_ratio < 3.0:
                margin = 20
                x1 = max(0, x - margin)
                y1 = max(0, y - margin)
                x2 = min(width, x + w + margin)
                y2 = min(height, y + h + margin)
                
                cropped = img[y1:y2, x1:x2]
                diag_count += 1
                out_name = f"crop_{ch_id}_{filename[:-4]}_{diag_count}.png"
                cv2.imwrite(os.path.join(img_dir, out_name), cropped)
                diagram_html += f'    <img src="images/{out_name}" class="page-img diagram-img" style="max-width:80%; height:auto; display:block; margin: 20px auto; border: 1px solid #ccc; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" alt="Extracted Diagram">\n'

        # --- OCR & Translation ---
        pil_img = Image.open(page_path)
        try:
            raw_text = pytesseract.image_to_string(pil_img, lang='chi_sim')
        except Exception as e:
            print(f"OCR failed for {filename}:", e)
            raw_text = ""
            
        print(f"  OCR extracted {len(raw_text)} chars from {filename}")
        
        # Implement a custom timeout for translation to prevent hanging
        import signal
        def handler(signum, frame):
            raise Exception("Translation timed out")
        
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(5) # 5 seconds timeout per page
        
        try:
            translated_text = translate_chunk(raw_text)
        except Exception as e:
            print(f"  Translation failed/timed out for {filename}")
            translated_text = "[Translation Unavailable / Timed out]"
        finally:
            signal.alarm(0)
        
        # Format the translated text

        formatted_text = ""
        for line in translated_text.split('\n'):
            line = line.strip()
            if line:
                formatted_text += f"<p>{line}</p>\n"
                
        # Append to chapter content
        chapter_html_content[ch_id] += f"<div class='page-content'>\n{formatted_text}\n{diagram_html}</div>\n<hr style='margin: 40px 0;'>\n"
        
print("4. Deleting full pages...")
pages = sorted(glob.glob(os.path.join(img_dir, 'ch*_page_*.png')))
for page_path in pages:
    os.remove(page_path)

print("5. Rebuilding HTML chapters...")
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
