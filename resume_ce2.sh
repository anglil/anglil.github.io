#!/bin/bash
echo "Resuming Qwen2.5-VL Cohesive Transcription from ch04..."
/Users/anglil/.gemini/antigravity/scratch/anglil.github.io/venv/bin/python3 transcribe_ce2.py

echo "Starting CE Diagram Injection..."
/Users/anglil/.gemini/antigravity/scratch/anglil.github.io/venv/bin/python3 insert_diagrams_ce.py

echo "Full CE V2 redo complete!"
