import os
import re
import glob

html_files = glob.glob("college-electrical-engineering/*.html")
for f in html_files:
    with open(f, 'r') as file:
        content = file.read()
    
    # Remove Qwen grounding boxes
    content = re.sub(r'<\|box_start\|>.*?<\|box_end\|>', '', content)
    # Remove empty p tags that might be left behind
    content = re.sub(r'<p>\s*</p>', '', content)
    
    with open(f, 'w') as file:
        file.write(content)
    print(f"Cleaned {f}")
