import sys
from mlx_vlm import load, generate
import mlx.core as mx

model_path = 'mlx-community/Qwen2-VL-2B-Instruct-4bit'
model, processor = load(model_path)

messages = [
    {'role': 'user', 'content': [{'type': 'image'}, {'type': 'text', 'text': 'Read all text in the image. Translate Chinese text to English. Output only the translation.'}]}
]
prompt = processor.apply_chat_template(messages, add_generation_prompt=True)

try:
    response = generate(
        model, 
        processor, 
        prompt=prompt,
        image='test_tmp.png',
        max_tokens=1000,
        verbose=False
    )
    print("--- RESULT ---")
    print(response.text.strip())
    print("--------------")
except Exception as e:
    print(f"Error: {e}")
