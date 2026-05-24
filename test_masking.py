import cv2
import Vision
from Foundation import NSURL
import numpy as np
import re

def perform_mac_ocr(image_path):
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
                for match in re.finditer(r'[\u4e00-\u9fff]+', text):
                    chinese_ranges.append(match.span())
                
                char_boxes = []
                for start, end in chinese_ranges:
                    try:
                        # NSRange takes location and length
                        ns_range = Vision.NSMakeRange(start, end - start)
                        # Get bounding box for this range
                        box, err = top_candidate.boundingBoxForRange_error_(ns_range, None)
                        if box:
                            # The box is in the coordinate space of the image
                            # Note: VNRectangleObservation is returned, we need its boundingBox
                            rect = box.boundingBox()
                            char_boxes.append(rect)
                    except Exception as e:
                        print("Error getting range:", e)
                
                text_blocks.append({
                    "text": text,
                    "chinese_boxes": char_boxes
                })
                
    request = Vision.VNRecognizeTextRequest.alloc().initWithCompletionHandler_(recognition_handler)
    request.setRecognitionLevel_(Vision.VNRequestTextRecognitionLevelAccurate)
    request.setRecognitionLanguages_(["zh-Hans", "zh-Hant", "en-US"])
    request.setUsesLanguageCorrection_(True)
    
    request_handler.performRequests_error_([request], None)
    return text_blocks

img_path = "college-electrical-engineering/images/crop_ch01_page_048_1.png"
img = cv2.imread(img_path)
H, W = img.shape[:2]

blocks = perform_mac_ocr(img_path)

for b in blocks:
    text = b["text"]
    print(f"TEXT: {text}")
    for box in b["chinese_boxes"]:
        x = int(box.origin.x * W)
        y = int((1.0 - box.origin.y - box.size.height) * H)
        w = int(box.size.width * W)
        h = int(box.size.height * H)
        print(f"  CHINESE BOX: x={x}, y={y}, w={w}, h={h}")
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

cv2.imwrite("college-electrical-engineering/images/test_masking2.png", img)
print("Saved test_masking2.png")
