#!/bin/bash
echo "Starting Qwen2.5-VL-7B-Instruct-4bit Transcription..."
/Users/anglil/.gemini/antigravity/scratch/anglil.github.io/venv/bin/python3 transcribe_pdfs_mlx_qwen25.py
echo "Starting Diagram Injection..."
/Users/anglil/.gemini/antigravity/scratch/anglil.github.io/venv/bin/python3 insert_diagrams.py
echo "Full redo complete!"
