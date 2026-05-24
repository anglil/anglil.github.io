import cv2
import numpy as np
import os
import glob

# Test on one page
page_path = 'college-electrical-engineering/images/ch01_page_004.png'
img = cv2.imread(page_path)
if img is not None:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 10)
    
    # 1. Remove small components (text characters)
    # Find all connected components
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh, connectivity=8)
    
    # Create a mask to draw only large components (diagram parts)
    diagram_mask = np.zeros_like(thresh)
    
    # stats format: [x, y, w, h, area]
    for i in range(1, num_labels): # skip background 0
        w = stats[i, cv2.CC_STAT_WIDTH]
        h = stats[i, cv2.CC_STAT_HEIGHT]
        area = stats[i, cv2.CC_STAT_AREA]
        
        # A typical text character is small. A diagram has long lines, large boxes, etc.
        # If a component is larger than a typical character (e.g., w > 60 or h > 60 or area > 500)
        if w > 50 or h > 50 or area > 400:
            diagram_mask[labels == i] = 255
            
    # 2. Group the remaining large components
    # We use morphological close to connect the diagram parts that might be broken
    kernel = np.ones((40, 40), np.uint8)
    closed = cv2.morphologyEx(diagram_mask, cv2.MORPH_CLOSE, kernel)
    
    # 3. Find contours of the grouped diagram parts
    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    height, width = img.shape[:2]
    page_area = width * height
    
    print(f"Page size: {width}x{height} (Area: {page_area})")
    for i, c in enumerate(contours):
        x, y, w, h = cv2.boundingRect(c)
        area = w * h
        print(f"Contour {i}: w={w}, h={h}, area={area}, area_pct={area/page_area*100:.2f}%")
else:
    print("Image not found")
