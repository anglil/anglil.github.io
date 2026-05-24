from mlx_vlm import load, generate
model, processor = load("mlx-community/Qwen2.5-VL-7B-Instruct-4bit")
prompt_text = "Extract text from this image."
prompt_fmt = f"<|im_start|>system\nYou are a helpful assistant.<|im_end|>\n<|im_start|>user\n<|vision_start|><|image_pad|><|vision_end|>{prompt_text}<|im_end|>\n<|im_start|>assistant\n"
img_path = "temp_page_ch01.jpg"
response = generate(model, processor, prompt=prompt_fmt, image=img_path, verbose=False, max_tokens=100)
print("OUTPUT:", response.text.strip())
