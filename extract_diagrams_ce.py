import cv2
import numpy as np
import fitz
import os

def extract_diagrams_from_page(pdf_path, page_num, output_dir="extracted_diagrams"):
    os.makedirs(output_dir, exist_ok=True)
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_num)
    pix = page.get_pixmap(dpi=150)
    
    img_path = "temp_page.png"
    pix.save(img_path)
    
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Adaptive thresholding might be better for handwritten notes
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    
    # Dilate heavily to merge everything in a block
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 20))
    dilated = cv2.dilate(thresh, kernel, iterations=3)
    
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    img_annotated = img.copy()
    diagram_count = 0
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        area = w * h
        # We just want to see what it's finding
        if area > 10000:
            cv2.rectangle(img_annotated, (x, y), (x+w, y+h), (0, 255, 0), 2)
            diagram = img[y:y+h, x:x+w]
            cv2.imwrite(f"{output_dir}/crop_p{page_num}_{diagram_count}.png", diagram)
            diagram_count += 1
                
    cv2.imwrite(f"{output_dir}/annotated_p{page_num}.png", img_annotated)
    print(f"Found {diagram_count} blocks > 10000px on page {page_num}.")

extract_diagrams_from_page("notes/circuits principles, experiments, and semiconductors.pdf", 5)
