from mlx_vlm import load
model, processor = load("mlx-community/Qwen2.5-VL-7B-Instruct-4bit")
print(hasattr(model, 'config'))
