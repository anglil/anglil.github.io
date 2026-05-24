import cv2
import glob
import os
import shutil

os.makedirs('filtered_diagrams', exist_ok=True)
crops = glob.glob('college-electrical-engineering/images/crop_*.png')
print(f"Total crops: {len(crops)}")

diagram_count = 0
for crop in crops:
    img = cv2.imread(crop)
    if img is None: continue
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
    
    # Don't dilate much, just enough to connect characters or lines
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    dilated = cv2.dilate(thresh, kernel, iterations=1)
    
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    is_diagram = False
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        
        # If a single continuous contour takes up more than 30% of the crop's width AND 30% of its height, it's likely a diagram (e.g. a long wire, a box, a circle).
        # Handwritten text characters are typically much smaller compared to the crop width.
        if w > img.shape[1] * 0.4 and h > img.shape[0] * 0.4:
            is_diagram = True
            break
            
    if is_diagram:
        shutil.copy(crop, f"filtered_diagrams/{os.path.basename(crop)}")
        diagram_count += 1
        
print(f"Found {diagram_count} diagrams!")
