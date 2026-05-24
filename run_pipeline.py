import os
import fitz
import cv2
import numpy as np
import glob

print("1. Cleaning up images dir...")
img_dir = "college-electrical-engineering/images"
os.makedirs(img_dir, exist_ok=True)
for f in glob.glob(os.path.join(img_dir, "*.png")):
    os.remove(f)

print("2. Extracting pages from PDF...")
pdfs = [
    ("notes/circuits principles, experiments, and semiconductors.pdf", "ch01"),
    ("notes/communication circuits.pdf", "ch02"),
    ("notes/antennae.pdf", "ch03"),
    ("notes/digital electronics.pdf", "ch04")
]

for pdf_path, ch_id in pdfs:
    doc = fitz.open(pdf_path)
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(dpi=150)
        img_path = os.path.join(img_dir, f"{ch_id}_page_{page_num+1:03d}.png")
        pix.save(img_path)

print("3. Extracting diagrams using advanced heuristics...")
pages = sorted(glob.glob(os.path.join(img_dir, 'ch*_page_*.png')))
kernel = np.ones((40, 40), np.uint8)

for page_path in pages:
    filename = os.path.basename(page_path)
    ch_id = filename.split('_')[0]
    img = cv2.imread(page_path)
    if img is None: continue
        
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 10)
    
    # 1. Remove small components (text characters)
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh, connectivity=8)
    diagram_mask = np.zeros_like(thresh)
    
    for i in range(1, num_labels):
        w = stats[i, cv2.CC_STAT_WIDTH]
        h = stats[i, cv2.CC_STAT_HEIGHT]
        area = stats[i, cv2.CC_STAT_AREA]
        if w > 50 or h > 50 or area > 400:
            diagram_mask[labels == i] = 255
            
    # 2. Group the remaining large components
    closed = cv2.morphologyEx(diagram_mask, cv2.MORPH_CLOSE, kernel)
    
    # 3. Find contours
    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    height, width = img.shape[:2]
    page_area = width * height
    
    diag_count = 0
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        area = w * h
        aspect_ratio = float(w) / h if h > 0 else 0
        area_pct = area / page_area
        
        # Stricter Heuristics
        # - Between 2% and 40% of the page
        # - Width is less than 85% of page width (to avoid full paragraphs)
        # - Aspect ratio is balanced (0.3 to 3.0)
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

print("4. Deleting full pages...")
for page_path in pages:
    os.remove(page_path)

print("5. Rebuilding HTML chapters...")
import rebuild_chapters
print("Done!")
