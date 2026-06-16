#!/bin/bash
echo "=== Starting Communication Circuits Batch ==="
./venv/bin/python run_batch_chapters.py communication
echo "=== Starting Antennae Batch ==="
./venv/bin/python run_batch_chapters.py antennae
echo "=== Starting Digital Electronics Batch ==="
./venv/bin/python run_batch_chapters.py digital
echo "=== All Batches Completed ==="
