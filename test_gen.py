from mlx_vlm import load, generate
from mlx_vlm.prompt_utils import apply_chat_template
model, processor = load("mlx-community/Qwen2.5-VL-7B-Instruct-4bit")
prompt_fmt = "This is a prompt"
img_path = "temp_page_ch01.jpg"
# We just pass prompt_fmt, img_path positionally!
print("Trying to generate...")
try:
    generate(model, processor, prompt_fmt, [img_path], verbose=False, max_tokens=10)
    print("Success")
except Exception as e:
    print("Error:", e)
