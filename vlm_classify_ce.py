import glob
import os
import shutil
from mlx_vlm import load, generate
from mlx_vlm.prompt_utils import apply_chat_template

def classify_diagrams():
    print("Loading mlx-community/Qwen2.5-VL-7B-Instruct-4bit...")
    model_path = "mlx-community/Qwen2.5-VL-7B-Instruct-4bit"
    model, processor = load(model_path)
    
    crops = glob.glob('college-computer-engineering/images_v2/crop_*.png')
    crops.sort()
    
    output_dir = 'diagram_crops_ce2'
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Processing {len(crops)} crops for strict diagram validation...")
    
    prompt_text = "Look at this cropped image from a handwritten notebook. Is this image primarily a structural diagram, flowchart, graph, circuit, or illustration? Answer strictly with the single word 'DIAGRAM' if it is. If it is primarily just lines of handwritten text, mathematical equations, code, or a notebook cover, answer strictly with the single word 'TEXT'."
    
    diagram_count = 0
    for img_path in crops:
        messages = [
            {
                "role": "user",
                "content": "<|vision_start|><|image_pad|><|vision_end|>" + prompt_text
            }
        ]
        
        prompt_fmt = apply_chat_template(processor, model.config, messages, add_generation_prompt=True)            
        try:
            response = generate(model, processor, prompt=prompt_fmt, image=img_path, verbose=False, max_tokens=10)
            answer = response.text.strip().upper()
            
            # Clean up artifacts if any
            answer = answer.replace('<|box_start|>', '').replace('<|box_end|>', '')
            
            if 'DIAGRAM' in answer and 'TEXT' not in answer:
                shutil.copy(img_path, f"{output_dir}/{os.path.basename(img_path)}")
                diagram_count += 1
                print(f"[DIAGRAM] {img_path}")
            else:
                print(f"[TEXT] {img_path} (Answer: {answer})")
        except Exception as e:
            print(f"Error classifying {img_path}: {e}")
            
    print(f"\nFound {diagram_count} perfectly validated diagrams!")

if __name__ == "__main__":
    classify_diagrams()
