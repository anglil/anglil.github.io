import fitz
from mlx_vlm import load, generate
from PIL import Image

doc = fitz.open("notes/circuits principles, experiments, and semiconductors.pdf")
page = doc.load_page(4) # 5th page has diagrams
pix = page.get_pixmap(dpi=150)
img_path = "temp_page_ch01_p5.jpg"
pix.save(img_path)

model, processor = load("mlx-community/Qwen2.5-VL-7B-Instruct-4bit")
prompt_text = "Extract all text, mathematical formulas, and diagrams from this handwritten note. Translate all Chinese text to fluent, coherent English prose. Preserve all mathematical LaTeX formulas exactly as written (wrapped in $$...$$ for block math or $...$ for inline math). For each diagram, plot, or illustration, output a placeholder like <diagram box_2d=[ymin, xmin, ymax, xmax]>. Do not hallucinate or repeat text. Output only the extracted English text, math, and diagram placeholders."
prompt_fmt = f"<|im_start|>system\nYou are a helpful assistant.<|im_end|>\n<|im_start|>user\n<|vision_start|><|image_pad|><|vision_end|>{prompt_text}<|im_end|>\n<|im_start|>assistant\n"
response = generate(model, processor, prompt=prompt_fmt, image=img_path, verbose=False, max_tokens=1500)
print("OUTPUT:", response.text.strip())
