import fitz
from mlx_vlm import load, generate
import mlx.core as mx

def test():
    model_path = 'mlx-community/Qwen2-VL-2B-Instruct-4bit'
    model, processor = load(model_path)
    
    pdf_path = "notes/circuits principles, experiments, and semiconductors.pdf"
    doc = fitz.open(pdf_path)
    page = doc.load_page(5) # Find a page with a diagram
    pix = page.get_pixmap(dpi=150)
    pix.save("test_diag.png")
    
    prompt_text = "Find all circuit diagrams and illustrations in the image. Return their bounding boxes in <|box_start|>(ymin,xmin),(ymax,xmax)<|box_end|> format."
    
    messages = [{'role': 'user', 'content': [{'type': 'image'}, {'type': 'text', 'text': prompt_text}]}]
    prompt = processor.apply_chat_template(messages, add_generation_prompt=True)
    
    response = generate(model, processor, prompt=prompt, image="test_diag.png", max_tokens=200, verbose=False)
    print("--- RESULT ---")
    print(response.text)
    print("--------------")

test()
