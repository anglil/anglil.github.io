import glob
import os
import re
from bs4 import BeautifulSoup
from mlx_lm import load, generate

def has_chinese(text):
    return any('\u4e00' <= char <= '\u9fff' for char in text)

def run():
    model_path = 'mlx-community/Qwen2.5-1.5B-Instruct-4bit'
    print(f'Loading {model_path}...', flush=True)
    model, tokenizer = load(model_path)
    
    html_files = glob.glob("college-electrical-engineering/*.html")
    html_files.sort()
    for f_path in html_files:
        if not re.search(r'ch0[1-4]\.html', f_path):
            continue
            
        print(f"Processing {f_path}...", flush=True)
        
        with open(f_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            
        pages = soup.find_all('div', class_='page')
        modified = False
        for i, page in enumerate(pages):
            
            # Extract raw text from all <p> tags
            text_blocks = []
            for p in page.find_all('p'):
                text_blocks.append(p.get_text())
            original_text = '\n'.join(text_blocks).strip()
            
            if not original_text or original_text == '$$':
                continue
                
            if not has_chinese(original_text):
                continue
                
            print(f"  Translating Page {i+1}/{len(pages)}...", flush=True)
                
            prompt = f"""You are a helpful assistant. Translate any Chinese text in the following notes into English prose. If it is already in English, leave it as is. Do NOT translate or modify any LaTeX math formulas (text inside $$...$$ or $...$); preserve them exactly. Ensure proper HTML formatting by wrapping paragraphs in <p> tags, but DO NOT wrap lines of a multiline $$...$$ block in separate <p> tags! A multiline $$ block must stay together.

Notes to translate:
{original_text}

Output ONLY the translated and HTML formatted text, nothing else. Do not output markdown blocks like ```html."""

            messages = [{"role": "user", "content": prompt}]
            prompt_fmt = tokenizer.apply_chat_template(messages, add_generation_prompt=True, tokenize=False)
            
            response = generate(
                model, 
                tokenizer, 
                prompt=prompt_fmt, 
                max_tokens=1500, 
                verbose=False
            )
            
            translated_html = response.strip()
            if translated_html.startswith('```html'):
                translated_html = translated_html[7:]
            if translated_html.startswith('```'):
                translated_html = translated_html[3:]
            if translated_html.endswith('```'):
                translated_html = translated_html[:-3]
                
            # Replace contents (but keep diagrams if they exist)
            diagrams = page.find_all('img', class_='diagram')
            page.clear()
            page.append(BeautifulSoup(translated_html, 'html.parser'))
            for diag in diagrams:
                page.append(diag)
                
            modified = True
            
        # Save back the HTML file
        if modified:
            with open(f_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"Saved {f_path}", flush=True)
        else:
            print(f"No changes in {f_path}", flush=True)
            
run()
