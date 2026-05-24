import sys
import Quartz
import Vision
from Foundation import NSURL

def perform_ocr(image_path):
    url = NSURL.fileURLWithPath_(image_path)
    
    # Create the request handler
    request_handler = Vision.VNImageRequestHandler.alloc().initWithURL_options_(url, None)
    
    # Define an array to hold the results
    extracted_text = []
    
    def recognition_handler(request, error):
        if error:
            print(f"Error: {error}")
            return
            
        observations = request.results()
        if not observations:
            return
            
        for observation in observations:
            # We want the top candidate
            candidates = observation.topCandidates_(1)
            if candidates:
                extracted_text.append(candidates[0].string())
                
    # Create the request
    request = Vision.VNRecognizeTextRequest.alloc().initWithCompletionHandler_(recognition_handler)
    
    # Set to accurate recognition
    request.setRecognitionLevel_(Vision.VNRequestTextRecognitionLevelAccurate)
    
    # Try multiple languages
    request.setRecognitionLanguages_(["zh-Hans", "zh-Hant", "en-US"])
    request.setUsesLanguageCorrection_(True)
    
    # Perform the request
    try:
        request_handler.performRequests_error_([request], None)
    except Exception as e:
        print(f"Failed to perform OCR: {e}")
        return ""
        
    return "\n".join(extracted_text)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <image_path>")
        sys.exit(1)
        
    image_path = sys.argv[1]
    text = perform_ocr(image_path)
    print("--- Extracted Text ---")
    print(text)
