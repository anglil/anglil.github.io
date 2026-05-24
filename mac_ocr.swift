import Cocoa
import Vision

guard CommandLine.arguments.count == 2 else {
    print("Usage: \(CommandLine.arguments[0]) <image_path>")
    exit(1)
}

let imagePath = CommandLine.arguments[1]
guard let image = NSImage(contentsOfFile: imagePath),
      let cgImage = image.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
    print("Could not load image")
    exit(1)
}

let requestHandler = VNImageRequestHandler(cgImage: cgImage, options: [:])
let request = VNRecognizeTextRequest { (request, error) in
    if let error = error {
        print("Error: \(error)")
        return
    }
    
    guard let observations = request.results as? [VNRecognizedTextObservation] else {
        return
    }
    
    for observation in observations {
        guard let topCandidate = observation.topCandidates(1).first else { continue }
        print(topCandidate.string)
    }
}

request.recognitionLanguages = ["zh-Hans", "zh-Hant", "en-US"]
request.usesLanguageCorrection = true

do {
    try requestHandler.perform([request])
} catch {
    print("Failed to perform OCR: \(error)")
}
