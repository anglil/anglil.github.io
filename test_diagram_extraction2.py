import cv2
import numpy as np

page_path = 'college-electrical-engineering/images/ch01_page_004.png'
img = cv2.imread(page_path)
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
        
kernel = np.ones((40, 40), np.uint8)
closed = cv2.morphologyEx(diagram_mask, cv2.MORPH_CLOSE, kernel)
contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

height, width = img.shape[:2]
page_area = width * height

print(f"Page size: {width}x{height} (Area: {page_area})")
count = 0
for i, c in enumerate(contours):
    x, y, w, h = cv2.boundingRect(c)
    area = w * h
    aspect_ratio = float(w) / h if h > 0 else 0
    area_pct = area / page_area
    
    # NEW Heuristics:
    if 0.02 < area_pct < 0.35 and w < 0.85 * width and 0.3 < aspect_ratio < 3.0:
        print(f"✅ ACCEPTED: w={w}, h={h}, area_pct={area_pct*100:.2f}%, aspect={aspect_ratio:.2f}")
        count += 1
    else:
        print(f"❌ REJECTED: w={w}, h={h}, area_pct={area_pct*100:.2f}%, aspect={aspect_ratio:.2f}")

print(f"Total accepted: {count}")
