#!/bin/bash
echo "Starting CE V2 Diagram Cropping (Tight OpenCV Bounds)..."
/Users/anglil/.gemini/antigravity/scratch/anglil.github.io/venv/bin/python3 extract_diagram_crops_ce2.py

echo "Starting VLM Diagram Validation (Qwen2.5-VL)..."
/Users/anglil/.gemini/antigravity/scratch/anglil.github.io/venv/bin/python3 vlm_classify_ce.py

echo "Starting Qwen2.5-VL Cohesive Transcription..."
/Users/anglil/.gemini/antigravity/scratch/anglil.github.io/venv/bin/python3 transcribe_ce2.py

echo "Starting CE Diagram Injection..."
/Users/anglil/.gemini/antigravity/scratch/anglil.github.io/venv/bin/python3 insert_diagrams_ce.py

echo "Full CE V2 redo complete!"
