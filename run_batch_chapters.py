import os
import sys
import re
import fitz  # PyMuPDF
import cv2
import numpy as np
import mlx.core as mx
from mlx_vlm import load, generate
from mlx_vlm.prompt_utils import apply_chat_template

# Configuration for each chapter
CONFIG = {
    'communication': {
        'pdf_path': 'notes/communication circuits.pdf',
        'start_idx': 0,
        'id_prefix': 'comm',
        'insert_comment': '<!-- INSERT COMMUNICATION PAGES HERE -->'
    },
    'antennae': {
        'pdf_path': 'notes/antennae.pdf',
        'start_idx': 1,
        'id_prefix': 'ant',
        'insert_comment': '<!-- INSERT ANTENNAE PAGES HERE -->'
    },
    'digital': {
        'pdf_path': 'notes/digital electronics.pdf',
        'start_idx': 1,
        'id_prefix': 'dig',
        'insert_comment': '<!-- INSERT DIGITAL PAGES HERE -->'
    }
}

def append_page_to_html(chapter_key, page_num, page_html):
    html_path = 'college-electrical-engineering/index.html'
    if not os.path.exists(html_path):
        print(f"Error: {html_path} does not exist.")
        return False
        
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    cfg = CONFIG[chapter_key]
    marker = f'id="{cfg["id_prefix"]}-page-{page_num}"'
    if marker in content:
        print(f"Page {page_num} of {chapter_key} already in index.html, skipping append.")
        return False
        
    comment_marker = cfg['insert_comment']
    if comment_marker in content:
        parts = content.split(comment_marker, 1)
        new_content = parts[0] + page_html + '\n    ' + comment_marker + parts[1]
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Appended Page {page_num} of {chapter_key} to index.html successfully.")
        return True
    else:
        print(f"Error: Could not find insert marker {comment_marker} in index.html.")
        return False

def check_resumed_page(chapter_key, page_num):
    html_path = 'college-electrical-engineering/index.html'
    if not os.path.exists(html_path):
        return False
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    cfg = CONFIG[chapter_key]
    return f'id="{cfg["id_prefix"]}-page-{page_num}"' in content

def run_batch(chapter_key):
    if chapter_key not in CONFIG:
        print(f"Error: Invalid chapter key '{chapter_key}'")
        return
        
    cfg = CONFIG[chapter_key]
    pdf_path = cfg['pdf_path']
    start_idx = cfg['start_idx']
    id_prefix = cfg['id_prefix']
    
    output_dir = "college-electrical-engineering"
    images_dir = os.path.join(output_dir, "images")
    os.makedirs(images_dir, exist_ok=True)
    
    print(f"Starting batch for {chapter_key} using {pdf_path}")
    print("Loading mlx-community/Qwen2.5-VL-7B-Instruct-4bit...")
    model_path = "mlx-community/Qwen2.5-VL-7B-Instruct-4bit"
    model, processor = load(model_path)
    print("Model loaded successfully.")
    
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    print(f"Opened PDF: {pdf_path}. Total pages: {total_pages}")
    
    for page_idx in range(start_idx, total_pages):
        page_num = page_idx + 1
        print(f"\n--- Processing Page {page_num}/{total_pages} (index {page_idx}) ---")
        
        if check_resumed_page(chapter_key, page_num):
            print(f"Page {page_num} already processed. Skipping.")
            continue
            
        # 1. Render page at 150 DPI
        page = doc.load_page(page_idx)
        pix = page.get_pixmap(dpi=150)
        temp_img_path = f"temp_page_process_{chapter_key}.png"
        pix.save(temp_img_path)
        
        # 2. Contour detection for diagram crops
        img = cv2.imread(temp_img_path)
        if img is None:
            print(f"Error: Failed to read rendered page {page_num} image.")
            continue
            
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 110, 255, cv2.THRESH_BINARY_INV)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
        dilated = cv2.dilate(thresh, kernel, iterations=2)
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        contours_sorted = sorted(contours, key=lambda c: cv2.boundingRect(c)[1])
        
        candidates = []
        for cnt in contours_sorted:
            x, y, w, h = cv2.boundingRect(cnt)
            area = w * h
            aspect_ratio = w / float(h)
            
            if area > (img.shape[0] * img.shape[1] * 0.8):
                continue
                
            if area > 12000 and aspect_ratio < 10 and h > 80:
                candidates.append((x, y, w, h))
                
        print(f"Found {len(candidates)} candidate diagram regions on Page {page_num}.")
        
        # 3. Classify candidates using VLM
        saved_diagrams = []
        diag_count = 1
        for idx, (x, y, w, h) in enumerate(candidates):
            pad = 10
            x1 = max(0, x - pad)
            y1 = max(0, y - pad)
            x2 = min(img.shape[1], x + w + pad)
            y2 = min(img.shape[0], y + h + pad)
            
            crop = img[y1:y2, x1:x2]
            crop_path = f"temp_candidate_crop_{chapter_key}.png"
            cv2.imwrite(crop_path, crop)
            
            prompt_text = 'Is this image purely lines of handwritten text and equations? Or does it contain circuit drawings (like circles with signs/arrows, coordinate axes, brackets) or graphs? Answer strictly with TEXT or DIAGRAM.'
            messages = [{'role': 'user', 'content': '<|vision_start|><|image_pad|><|vision_end|>' + prompt_text}]
            prompt_fmt = apply_chat_template(processor, model.config, messages, add_generation_prompt=True)
            
            try:
                response = generate(model, processor, prompt=prompt_fmt, image=crop_path, verbose=False, max_tokens=10)
                ans = response.text.strip().upper()
                if 'DIAGRAM' in ans and 'TEXT' not in ans:
                    dest_filename = f"{id_prefix}_page_{page_num}_diag_{diag_count}.png"
                    dest_path = os.path.join(images_dir, dest_filename)
                    cv2.imwrite(dest_path, crop)
                    saved_diagrams.append(dest_filename)
                    print(f"  [DIAGRAM] Candidate {idx} verified as diagram. Saved as {dest_filename}.")
                    diag_count += 1
                else:
                    print(f"  [TEXT] Candidate {idx} classified as text. Ignored.")
            except Exception as e:
                print(f"  Error classifying candidate {idx}: {e}")
            finally:
                if os.path.exists(crop_path):
                    os.remove(crop_path)
                    
        # 4. Transcribe and Translate the Page
        print(f"Transcribing and translating Page {page_num}...")
        prompt_transcribe = """Extract all text and mathematical formulas from this handwritten note. Translate all Chinese text to fluent, coherent English prose. Do not include any Chinese in your output. Preserve all mathematical LaTeX formulas exactly as written (wrapped in $$...$$ for block math or $...$ for inline math). Do not hallucinate or repeat text. Output only the extracted English text and math.
        """
        if len(saved_diagrams) > 0:
            prompt_transcribe += f"\nSince this page contains exactly {len(saved_diagrams)} diagrams, please insert placeholders like [DIAGRAM 1], [DIAGRAM 2], etc. in the exact places in the text where they appear contextually, in order from top to bottom."
            
        messages = [{'role': 'user', 'content': '<|vision_start|><|image_pad|><|vision_end|>' + prompt_transcribe}]
        prompt_fmt = apply_chat_template(processor, model.config, messages, add_generation_prompt=True)
        
        transcribed = ""
        try:
            response = generate(model, processor, prompt=prompt_fmt, image=temp_img_path, verbose=False, max_tokens=1500)
            transcribed = response.text.strip()
        except Exception as e:
            print(f"Error transcribing page {page_num}: {e}")
            
        # 5. Clean up VLM output and format HTML
        transcribed = transcribed.replace('<|box_start|>', '').replace('<|box_end|>', '').replace('<|quad_start|>', '').replace('<|quad_end|>', '')
        if transcribed.startswith('```'):
            transcribed = '\n'.join(transcribed.split('\n')[1:])
        if transcribed.endswith('```'):
            transcribed = transcribed[:-3]
            
        transcribed = re.sub(r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}', '', transcribed, flags=re.DOTALL)
        
        used_diagrams = set()
        for idx, diag_file in enumerate(saved_diagrams):
            diag_idx = idx + 1
            placeholder = f"[DIAGRAM {diag_idx}]"
            img_tag = f'\n  <div class="figure"><img src="images/{diag_file}" class="diagram" alt="Page {page_num} Diagram {diag_idx}" /></div>\n'
            if placeholder in transcribed:
                transcribed = transcribed.replace(placeholder, img_tag)
                used_diagrams.add(diag_file)
            elif f"DIAGRAM {diag_idx}" in transcribed:
                transcribed = transcribed.replace(f"DIAGRAM {diag_idx}", img_tag)
                used_diagrams.add(diag_file)
                
        blocks = transcribed.split('\n\n')
        html_blocks = []
        for block in blocks:
            block = block.strip()
            if not block:
                continue
            if block.startswith('###'):
                html_blocks.append(f'  <h3>{block.replace("###", "").strip()}</h3>')
            elif block.startswith('##'):
                html_blocks.append(f'  <h2>{block.replace("##", "").strip()}</h2>')
            elif '<img' in block:
                html_blocks.append(block)
            else:
                html_blocks.append(f'  <p>{block}</p>')
                
        for diag_file in saved_diagrams:
            if diag_file not in used_diagrams:
                html_blocks.append(f'\n  <div class="figure"><img src="images/{diag_file}" class="diagram" alt="Page {page_num} Fallback Diagram" /></div>\n')
                
        page_html = f'\n  <div class="page" id="{id_prefix}-page-{page_num}">\n  <div style="font-size:0.85rem; color:var(--accent-bright); font-weight:600; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:1rem; border-bottom: 1px solid var(--border); padding-bottom:0.3rem;">Page {page_num}</div>\n' + '\n'.join(html_blocks) + '\n  </div>\n  <hr />\n'
        
        # 6. Append to index.html
        append_page_to_html(chapter_key, page_num, page_html)
        
        if os.path.exists(temp_img_path):
            os.remove(temp_img_path)
            
        mx.clear_cache()
        print(f"Completed Page {page_num} successfully.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_batch_chapters.py <communication|antennae|digital>")
        sys.exit(1)
    run_batch(sys.argv[1])
