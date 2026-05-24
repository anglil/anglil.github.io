from mlx_vlm import load
from mlx_vlm.prompt_utils import apply_chat_template

model, processor = load("mlx-community/Qwen2.5-VL-7B-Instruct-4bit")
prompt = "Extract text."
messages = [{"role": "user", "content": "<|vision_start|><|image_pad|><|vision_end|>" + prompt}]
prompt_fmt = apply_chat_template(processor, model.config, messages, add_generation_prompt=True)
print(repr(prompt_fmt))
