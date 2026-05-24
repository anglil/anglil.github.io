import sys
import fitz
import Quartz
import Vision
from Foundation import NSURL
from deep_translator import GoogleTranslator

def perform_mac_ocr(image_path):
    url = NSURL.fileURLWithPath_(image_path)
    request_handler = Vision.VNImageRequestHandler.alloc().initWithURL_options_(url, None)
    extracted_text = []
    def recognition_handler(request, error):
        if error:
            print(f"Error: {error}")
            return
        observations = request.results()
        if not observations: return
        for observation in observations:
            candidates = observation.topCandidates_(1)
            if candidates:
                extracted_text.append(candidates[0].string())
                
    request = Vision.VNRecognizeTextRequest.alloc().initWithCompletionHandler_(recognition_handler)
    request.setRecognitionLevel_(Vision.VNRequestTextRecognitionLevelAccurate)
    request.setRecognitionLanguages_(["zh-Hans", "zh-Hant", "en-US"])
    request.setUsesLanguageCorrection_(True)
    
    try:
        request_handler.performRequests_error_([request], None)
    except Exception as e:
        print(f"Failed to perform OCR: {e}")
        return ""
    return "\n".join(extracted_text)

translator = GoogleTranslator(source='zh-CN', target='en')

doc = fitz.open("notes/circuits principles, experiments, and semiconductors.pdf")
page = doc.load_page(3) # Page 4 (the one we tested)
pix = page.get_pixmap(dpi=150)
pix.save("preview_page.png")

print("--- NATIVE MACOS VISION OCR OUTPUT ---")
chinese_text = perform_mac_ocr("preview_page.png")
print(chinese_text)

print("\n--- GOOGLE TRANSLATE OUTPUT ---")
english_text = translator.translate(chinese_text)
print(english_text)
