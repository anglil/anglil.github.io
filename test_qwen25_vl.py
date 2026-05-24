from mlx_vlm import load, generate
from mlx_vlm.prompt_utils import apply_chat_template

model_path = "mlx-community/Qwen2.5-VL-7B-Instruct-4bit"
print(f"Loading {model_path}...")
model, processor = load(model_path)
print("Loaded successfully!")
