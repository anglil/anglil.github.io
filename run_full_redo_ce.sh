#!/bin/bash
echo "Starting CE Diagram Cropping..."
/Users/anglil/.gemini/antigravity/scratch/anglil.github.io/venv/bin/python3 extract_diagram_crops_ce.py

echo "Starting CLIP Classification..."
/Users/anglil/.gemini/antigravity/scratch/anglil.github.io/venv/bin/python3 clip_classify_ce.py

echo "Starting Qwen2.5-VL-7B-Instruct-4bit Transcription for CE..."
/Users/anglil/.gemini/antigravity/scratch/anglil.github.io/venv/bin/python3 transcribe_ce.py

echo "Starting CE Diagram Injection..."
/Users/anglil/.gemini/antigravity/scratch/anglil.github.io/venv/bin/python3 insert_diagrams_ce.py

echo "Full CE redo complete!"
