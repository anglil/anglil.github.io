import glob
import os
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import torch
import shutil

print("Loading CLIP...")
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

os.makedirs('diagram_crops_ce', exist_ok=True)
crops = glob.glob('college-computer-engineering/images/crop_*.png')
print(f"Processing {len(crops)} crops...")

labels = ["handwritten text, Chinese characters, notes, equations, math formulas", "plot, graph, figure, table, diagram, chart, hand-drawn illustration, sketch"]

diagram_count = 0
batch_size = 16
for i in range(0, len(crops), batch_size):
    batch_paths = crops[i:i+batch_size]
    images = []
    valid_paths = []
    for p in batch_paths:
        try:
            images.append(Image.open(p).convert("RGB"))
            valid_paths.append(p)
        except Exception:
            pass
            
    if not images:
        continue
        
    inputs = processor(text=labels, images=images, return_tensors="pt", padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        
    logits_per_image = outputs.logits_per_image
    probs = logits_per_image.softmax(dim=1)
    
    for j, prob in enumerate(probs):
        if prob[1] > 0.20: # 20% confidence it's a diagram/plot/illustration
            shutil.copy(valid_paths[j], f"diagram_crops_ce/{os.path.basename(valid_paths[j])}")
            diagram_count += 1
            
print(f"Found {diagram_count} diagrams!")
