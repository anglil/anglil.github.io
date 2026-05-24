import os
import glob
import time
import cv2
import numpy as np
import fitz
import Quartz
import Vision
from Foundation import NSURL
from deep_translator import GoogleTranslator
from pix2tex.cli import LatexOCR
from PIL import Image

print("Initializing pix2tex model...")
try:
    math_model = LatexOCR()
except Exception as e:
    print(f"Failed to load pix2tex model: {e}")
    math_model = None

print("1. Cleaning up images dir...")
img_dir = "college-electrical-engineering/images"
os.makedirs(img_dir, exist_ok=True)
for f in glob.glob(os.path.join(img_dir, "crop_*.png")):
    os.remove(f)

pdfs = [
    ("notes/circuits principles, experiments, and semiconductors.pdf", "ch01", "Circuits Principles, Experiments, and Semiconductors"),
    ("notes/communication circuits.pdf", "ch02", "Communication Circuits"),
    ("notes/antennae.pdf", "ch03", "Antennae"),
    ("notes/digital electronics.pdf", "ch04", "Digital Electronics")
]

translator = GoogleTranslator(source='zh-CN', target='en')

def translate_chunk_with_backoff(text, max_retries=3):
    if not text.strip(): return ""
    for attempt in range(max_retries):
        try:
            return translator.translate(text)
        except Exception as e:
            wait_time = 2 ** attempt
            time.sleep(wait_time)
    return text

def perform_mac_ocr(image_path, W, H):
    url = NSURL.fileURLWithPath_(image_path)
    request_handler = Vision.VNImageRequestHandler.alloc().initWithURL_options_(url, None)
    
    text_blocks = []
    
    def recognition_handler(request, error):
        if error: return
        observations = request.results()
        if not observations: return
        for observation in observations:
            candidates = observation.topCandidates_(1)
            if candidates:
                text = candidates[0].string()
                bbox = observation.boundingBox()
                x = bbox.origin.x * W
                y = (1.0 - bbox.origin.y - bbox.size.height) * H
                w = bbox.size.width * W
                h = bbox.size.height * H
                text_blocks.append({
                    "type": "text",
                    "content": text,
                    "y": y,
                    "x": x,
                    "w": w,
                    "h": h
                })
                
    request = Vision.VNRecognizeTextRequest.alloc().initWithCompletionHandler_(recognition_handler)
    request.setRecognitionLevel_(Vision.VNRequestTextRecognitionLevelAccurate)
    request.setRecognitionLanguages_(["zh-Hans", "zh-Hant", "en-US"])
    request.setUsesLanguageCorrection_(True)
    
    request_handler.performRequests_error_([request], None)
    return text_blocks

kernel = np.ones((5, 5), np.uint8)
chapter_html_content = { "ch01": "", "ch02": "", "ch03": "", "ch04": "" }

temp_image_path = os.path.join(img_dir, "temp_page.png")

for i, (pdf_path, ch_id, title) in enumerate(pdfs):
    doc = fitz.open(pdf_path)
    print(f"Processing {ch_id}: {title} ({len(doc)} pages)...")
    
    for page_num in range(len(doc)):
        print(f"  Page {page_num + 1}/{len(doc)}")
        page = doc.load_page(page_num)
        pix = page.get_pixmap(dpi=150)
        pix.save(temp_image_path)
        
        img = cv2.imread(temp_image_path)
        H, W = img.shape[:2]
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
        contours, hierarchy = cv2.findContours(closed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        page_area = W * H
        content_blocks = []
        diag_count = 0
        
        if hierarchy is not None:
            hierarchy = hierarchy[0]
            for idx, c in enumerate(contours):
                if hierarchy[idx][3] == -1: 
                    x, y, w, h = cv2.boundingRect(c)
                    area = w * h
                    area_pct = area / page_area
                    
                    if area_pct > 0.01 and area_pct < 0.6 and w > 50 and h > 20:
                        margin = 10
                        x1 = max(0, x - margin)
                        y1 = max(0, y - margin)
                        x2 = min(W, x + w + margin)
                        y2 = min(H, y + h + margin)
                        
                        # Heuristic: Diagrams are typically large, equations are smaller
                        is_diagram = (w > 0.5 * W) or (h > 200)
                        
                        cropped = img[y1:y2, x1:x2]
                        
                        if is_diagram:
                            diag_count += 1
                            out_name = f"crop_{ch_id}_page_{page_num+1:03d}_{diag_count}.png"
                            cv2.imwrite(os.path.join(img_dir, out_name), cropped)
                            
                            content_blocks.append({
                                "type": "image",
                                "src": f"images/{out_name}",
                                "y": y,
                                "x": x,
                                "w": w,
                                "h": h
                            })
                        else:
                            # It's math, run pix2tex
                            if math_model:
                                pil_img = Image.fromarray(cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB))
                                try:
                                    latex = math_model(pil_img)
                                    content_blocks.append({
                                        "type": "math",
                                        "content": latex,
                                        "y": y,
                                        "x": x,
                                        "w": w,
                                        "h": h
                                    })
                                except:
                                    pass

        text_blocks = perform_mac_ocr(temp_image_path, W, H)
        
        filtered_text_blocks = []
        for tb in text_blocks:
            is_inside_content = False
            for cb in content_blocks:
                cx = tb["x"] + 10 
                cy = tb["y"] + tb["h"]/2
                if cb["x"] < cx < cb["x"] + cb["w"] and cb["y"] < cy < cb["y"] + cb["h"]:
                    is_inside_content = True
                    break
            
            garbage_chars = set("!@#$%^&*()_+={}[]|\\;:'\\\"<>,.?/")
            num_garbage = sum(1 for c in tb["content"] if c in garbage_chars)
            if len(tb["content"]) > 0 and (num_garbage / len(tb["content"])) > 0.5:
                is_inside_content = True 
                
            if not is_inside_content:
                filtered_text_blocks.append(tb)
        
        all_blocks = content_blocks + filtered_text_blocks
        all_blocks.sort(key=lambda b: b["y"])
        
        page_html = ""
        current_text_paragraph = ""
        
        for block in all_blocks:
            if block["type"] == "text":
                current_text_paragraph += block["content"] + " "
            else:
                if current_text_paragraph.strip():
                    translated = translate_chunk_with_backoff(current_text_paragraph.strip())
                    page_html += f"<p>{translated}</p>\n"
                    current_text_paragraph = ""
                
                if block["type"] == "image":
                    page_html += f'<div style="text-align: center; margin: 20px 0;"><img src="{block["src"]}" alt="Diagram" style="max-width: 80%; height: auto; border: 1px solid #ccc; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"></div>\n'
                elif block["type"] == "math":
                    page_html += f'<div style="text-align: center; margin: 15px 0; overflow-x: auto;">\n$${block["content"]}$$\n</div>\n'
                    
        if current_text_paragraph.strip():
            translated = translate_chunk_with_backoff(current_text_paragraph.strip())
            page_html += f"<p>{translated}</p>\n"
            
        chapter_html_content[ch_id] += f"<div class='page-content'>\n{page_html}\n</div>\n<hr style='margin: 40px 0;'>\n"

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
