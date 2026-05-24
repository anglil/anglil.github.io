import ssl
try:
    ssl._create_default_https_context = ssl._create_unverified_context
except AttributeError:
    pass

import os
import cv2
import glob
import re
import urllib.request
import json
import numpy as np
from PIL import Image
import torch
from pix2tex.cli import LatexOCR
import Vision
from Foundation import NSURL

# Initialize models
print("Initializing LatexOCR...")
model = LatexOCR()
print("LatexOCR initialized.")

import time

def translate_text(text, target_language="en", max_retries=3):
    """Translates text using Google Translate's free API endpoint, with fallback."""
    if not text.strip(): return ""
    
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=" + target_language + "&dt=t&q=" + urllib.parse.quote(text)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    for attempt in range(max_retries):
        try:
            response = urllib.request.urlopen(req, context=ctx, timeout=5)
            result = json.loads(response.read().decode('utf-8'))
            return "".join([sentence[0] for sentence in result[0]])
        except Exception as e:
            print(f"Google Translate failed on attempt {attempt+1}: {e}", flush=True)
            time.sleep(2)
            
    print("Falling back to MyMemory...", flush=True)
    try:
        url_mm = f"https://api.mymemory.translated.net/get?q={urllib.parse.quote(text)}&langpair=zh|{target_language}"
        req_mm = urllib.request.Request(url_mm, headers={'User-Agent': 'Mozilla/5.0'})
        response_mm = urllib.request.urlopen(req_mm, context=ctx, timeout=5)
        result_mm = json.loads(response_mm.read().decode('utf-8'))
        return result_mm['responseData']['translatedText']
    except Exception as e:
        print(f"MyMemory failed: {e}", flush=True)
        return text

def perform_mac_ocr(image_path):
    """Returns a list of dictionaries with text, full_bbox, and chinese_bboxes."""
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
                top_candidate = candidates[0]
                text = top_candidate.string()
                
                # Find all Chinese character ranges
                chinese_ranges = []
                # Include Chinese chars and punctuation
                for match in re.finditer(r'[\u4e00-\u9fff，。：；！？、“”‘’（）【】《》]+', text):
                    chinese_ranges.append(match.span())
                
                char_boxes = []
                for start, end in chinese_ranges:
                    try:
                        ns_range = Vision.NSMakeRange(start, end - start)
                        box, err = top_candidate.boundingBoxForRange_error_(ns_range, None)
                        if box:
                            rect = box.boundingBox()
                            char_boxes.append({
                                "rect": rect,
                                "string": text[start:end]
                            })
                    except Exception as e:
                        pass
                
                text_blocks.append({
                    "full_text": text,
                    "full_bbox": observation.boundingBox(),
                    "chinese_data": char_boxes
                })
                
    request = Vision.VNRecognizeTextRequest.alloc().initWithCompletionHandler_(recognition_handler)
    request.setRecognitionLevel_(Vision.VNRequestTextRecognitionLevelAccurate)
    request.setRecognitionLanguages_(["zh-Hans", "zh-Hant", "en-US"])
    request.setUsesLanguageCorrection_(True)
    
    request_handler.performRequests_error_([request], None)
    return text_blocks

def sanitize_latex(latex_str):
    # Basic cleanup to remove hallucinatory commands that break MathJax
    latex_str = latex_str.replace(r"\operatorname", "")
    latex_str = re.sub(r'\\operatorname\{.*?\}', '', latex_str)
    # Remove weird text blocks that pix2tex hallucinated
    latex_str = re.sub(r'\\text\{[^\}]*[\u4e00-\u9fff]+[^\}]*\}', '', latex_str)
    return latex_str.strip()

def process_page(page_img_path, output_images_dir, chapter_name):
    print(f"Processing {page_img_path}...", flush=True)
    img = cv2.imread(page_img_path)
    if img is None: return []
    H, W = img.shape[:2]
    
    # 1. OCR
    ocr_blocks = perform_mac_ocr(page_img_path)
    
    # 2. Extract Chinese strings and mask them
    masked_img = img.copy()
    elements = [] # Will hold text, math, diagrams to sort by Y
    
    texts_to_translate = []
    
    for block in ocr_blocks:
        chinese_phrases = []
        full_y_center = int((1.0 - block["full_bbox"].origin.y - (block["full_bbox"].size.height / 2)) * H)
        
        for c_data in block["chinese_data"]:
            rect = c_data["rect"]
            x = int(rect.origin.x * W)
            y = int((1.0 - rect.origin.y - rect.size.height) * H)
            w = int(rect.size.width * W)
            h = int(rect.size.height * H)
            
            # Mask the Chinese characters with white
            cv2.rectangle(masked_img, (max(0, x-2), max(0, y-2)), (min(W, x+w+2), min(H, y+h+2)), (255, 255, 255), -1)
            
            chinese_phrases.append(c_data["string"])
            
        combined_chinese = " ".join(chinese_phrases)
        if combined_chinese.strip():
            texts_to_translate.append(combined_chinese.strip())
            elements.append({
                "type": "text",
                "y": full_y_center,
                "content_idx": len(texts_to_translate) - 1
            })
            
    # Batch translation
    if texts_to_translate:
        bulk_text = " | ".join(texts_to_translate)
        translated_bulk = translate_text(bulk_text)
        translated_chunks = [chunk.strip() for chunk in translated_bulk.split("|")]
        # Fallback if split didn't work perfectly
        if len(translated_chunks) != len(texts_to_translate):
            # Slow fallback
            translated_chunks = [translate_text(t) for t in texts_to_translate]
            
        for el in elements:
            if el["type"] == "text":
                el["content"] = translated_chunks[el["content_idx"]]
                
    # 3. Contour Detection on MASKED image
    gray = cv2.cvtColor(masked_img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    dilated = cv2.dilate(edges, kernel, iterations=2)
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    base_name = os.path.splitext(os.path.basename(page_img_path))[0]
    diag_idx = 1
    
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        area = w * h
        if area < 1000: continue # Noise
        
        y_center = y + h // 2
        crop = img[y:y+h, x:x+w]
        
        # Heuristic: Diagrams are usually large. Math is small.
        # But wait, math can be long. 
        # A circuit diagram usually has a large bounding box height (> 150)
        if h > 150 or w > 800:
            # Diagram! Save screenshot (from the MASKED image so it has no Chinese text!)
            crop_masked = masked_img[y:y+h, x:x+w]
            img_filename = f"{chapter_name}_{base_name}_diag_{diag_idx}.png"
            img_filepath = os.path.join(output_images_dir, img_filename)
            cv2.imwrite(img_filepath, crop_masked)
            
            elements.append({
                "type": "diagram",
                "y": y_center,
                "src": f"images/{img_filename}"
            })
            diag_idx += 1
        else:
            # Math equation! (Apple Vision didn't grab it because it's non-Chinese, and we didn't mask it)
            # Use original crop for pix2tex to read the math symbols
            # Convert to PIL for pix2tex
            pil_img = Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))
            try:
                latex = model(pil_img)
                latex = sanitize_latex(latex)
                if latex:
                    elements.append({
                        "type": "math",
                        "y": y_center,
                        "content": latex
                    })
            except Exception as e:
                print("Pix2tex error:", e)
                
    # Sort elements by Y coordinate to preserve document flow
    elements.sort(key=lambda e: e["y"])
    return elements

def build_chapter(chapter_name):
    print(f"Building {chapter_name}...")
    base_dir = "/Users/anglil/.gemini/antigravity/scratch/anglil.github.io/college-electrical-engineering"
    images_dir = os.path.join(base_dir, "images")
    
    page_files = sorted(glob.glob(os.path.join(images_dir, f"crop_{chapter_name}_page_*.png")))
    if not page_files: return
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{chapter_name} - College Electrical Engineering</title>
    <script>
      MathJax = {{
        tex: {{
          inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
          displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]
        }},
        svg: {{ fontCache: 'global' }}
      }};
    </script>
    <script type="text/javascript" id="MathJax-script" async
      src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js">
    </script>
    <style>
        body {{ font-family: 'Georgia', serif; line-height: 1.8; color: #333; max-width: 800px; margin: 0 auto; padding: 2rem; background-color: #fcfcfc; }}
        p {{ margin-bottom: 1.2rem; font-size: 1.1rem; }}
        .diagram-container {{ text-align: center; margin: 2rem 0; padding: 1rem; background-color: white; border: 1px solid #eee; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }}
        .diagram-container img {{ max-width: 100%; height: auto; }}
        .math-container {{ text-align: center; margin: 1.5rem 0; overflow-x: auto; font-size: 1.2rem; }}
        h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 0.5rem; }}
        .nav-link {{ display: inline-block; margin-top: 2rem; color: #3498db; text-decoration: none; font-weight: bold; }}
        .nav-link:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <h1>{chapter_name.upper()}</h1>
"""

    for page_path in page_files:
        elements = process_page(page_path, images_dir, chapter_name)
        for el in elements:
            if el["type"] == "text":
                html_content += f"    <p>{el['content']}</p>\n"
            elif el["type"] == "math":
                html_content += f"    <div class=\"math-container\">\n$${el['content']}$$\n    </div>\n"
            elif el["type"] == "diagram":
                html_content += f"    <div class=\"diagram-container\">\n        <img src=\"{el['src']}\" alt=\"Diagram\">\n    </div>\n"
                
    html_content += """
    <a href="index.html" class="nav-link">&larr; Back to Table of Contents</a>
</body>
</html>
"""
    
    html_path = os.path.join(base_dir, f"{chapter_name}.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Saved {html_path}")

def main():
    print("Starting main...")
    chapters = ["ch01", "ch02", "ch03", "ch04"]
    for ch in chapters:
        print(f"Starting chapter {ch}")
        build_chapter(ch)

if __name__ == "__main__":
    print("Initializing LatexOCR...")
    try:
        main()
    except Exception as e:
        print(f"Main error: {e}")
