import cv2
import numpy as np
import fitz
import os
import shutil

def extract_diagrams(pdf_files, output_dir="college-computer-engineering/images_v2"):
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    
    for pdf_path, ch_name in pdf_files:
        if not os.path.exists(pdf_path):
            print(f"Skipping {pdf_path}, file not found.")
            continue
            
        doc = fitz.open(pdf_path)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap(dpi=150)
            
            img_path = f"temp_ce_page.png"
            pix.save(img_path)
            
            img = cv2.imread(img_path)
            if img is None: continue
            
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Use tighter thresholding and dilation to avoid merging text
            thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 5)
            
            # Smaller kernel to prevent text blocks from merging with diagrams
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
            dilated = cv2.dilate(thresh, kernel, iterations=2)
            
            contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            diagram_count = 0
            for cnt in contours:
                x, y, w, h = cv2.boundingRect(cnt)
                area = w * h
                
                # Filter out obvious text lines (very wide and short)
                aspect_ratio = w / float(h)
                
                if area > 8000 and aspect_ratio < 10:
                    # Expand the bounding box slightly, but carefully
                    pad = 10
                    x1 = max(0, x - pad)
                    y1 = max(0, y - pad)
                    x2 = min(img.shape[1], x + w + pad)
                    y2 = min(img.shape[0], y + h + pad)
                    
                    diagram = img[y1:y2, x1:x2]
                    ch_num = int(ch_name.replace('ch', ''))
                    out_name = f"crop_ch{ch_num:02d}_page_{page_num+1:03d}_{diagram_count}.png"
                    cv2.imwrite(os.path.join(output_dir, out_name), diagram)
                    diagram_count += 1
                    
        print(f"Finished crops for {ch_name}")

if __name__ == "__main__":
    pdf_files = [
        ("notes/c.pdf", "ch01"),
        ("notes/c++.pdf", "ch02"),
        ("notes/computer architecture.pdf", "ch03"),
        ("notes/computer networks.pdf", "ch04"),
        ("notes/computer networks 2.pdf", "ch05")
    ]
    extract_diagrams(pdf_files)
