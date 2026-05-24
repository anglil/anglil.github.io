import sys
import os
import fitz  # PyMuPDF
from PIL import Image
from mlx_vlm import load, generate
import mlx.core as mx

def process_pdfs():
    model_path = 'mlx-community/Qwen2-VL-2B-Instruct-4bit'
    print(f'Loading model from {model_path}...')
    model, processor = load(model_path)
    print('Model loaded successfully.')
    
    pdfs = [
        ("notes/circuits principles, experiments, and semiconductors.pdf", "ch01"),
        ("notes/communication circuits.pdf", "ch02"),
        ("notes/antennae.pdf", "ch03"),
        ("notes/digital electronics.pdf", "ch04")
    ]
    
    prompt_text = "Read all text and math in this image. Translate the handwritten Chinese text to coherent English prose. Format math using LaTeX $$...$$. Do not repeat sentences. Stop generating when you have translated all the text on the page."
    
    for pdf_path, ch_name in pdfs:
        if not os.path.exists(pdf_path):
            print(f"Skipping {pdf_path}, not found.")
            continue
            
        print(f"Processing {pdf_path} -> {ch_name}.html")
        doc = fitz.open(pdf_path)
        
        html_content = [
            '<!DOCTYPE html>',
            '<html lang="en">',
            '<head>',
            '  <meta charset="UTF-8">',
            '  <meta name="viewport" content="width=device-width, initial-scale=1.0">',
            f'  <title>{ch_name} | College Electrical Engineering</title>',
            '  <link rel="stylesheet" href="style.css">',
            '  <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>',
            '  <script>',
            '      window.MathJax = {',
            '          tex: {',
            '              inlineMath: [["$", "$"], ["\\\\(", "\\\\)"]],',
            '              displayMath: [["$$", "$$"], ["\\\\[", "\\\\]"]],',
            '              macros: {',
            '                  bm: ["\\\\boldsymbol{#1}", 1]',
            '              }',
            '          }',
            '      };',
            '  </script>',
            '  <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>',
            '</head>',
            '<body>',
            '<button id="menu-toggle" onclick="document.getElementById(\'sidebar\').classList.toggle(\'open\')">☰</button>',
            '<aside id="sidebar">',
            '  <div class="book-title">College Electrical Engineering<span>Angli Liu</span></div>',
            '  <nav>',
            '    <ul>',
            '      <li><a href="index.html">Table of Contents</a></li>',
            '      <li><div class="part-label">Contents</div></li>',
            '      <li><a href="ch01.html">Chapter 1: Circuits Principles</a></li>',
            '      <li><a href="ch02.html">Chapter 2: Communication Circuits</a></li>',
            '      <li><a href="ch03.html">Chapter 3: Antennae</a></li>',
            '      <li><a href="ch04.html">Chapter 4: Digital Electronics</a></li>',
            '    </ul>',
            '  </nav>',
            '</aside>',
            '<main id="content">',
            '  <div class="chapter-header">',
            f'    <h1>Chapter {ch_name[-2:]}</h1>',
            f'    <h2 class="chapter-title">{pdf_path.split("/")[-1].replace(".pdf", "").title()}</h2>',
            '  </div>'
        ]
        
        for page_num in range(len(doc)):
            print(f"  Page {page_num+1}/{len(doc)}")
            page = doc.load_page(page_num)
            pix = page.get_pixmap(dpi=150)
            
            tmp_img = f"tmp_{ch_name}_{page_num}.png"
            pix.save(tmp_img)
            
            messages = [
                {'role': 'user', 'content': [{'type': 'image'}, {'type': 'text', 'text': prompt_text}]}
            ]
            prompt = processor.apply_chat_template(messages, add_generation_prompt=True)
            
            try:
                response = generate(
                    model, 
                    processor, 
                    prompt=prompt,
                    image=tmp_img,
                    max_tokens=600,
                    repetition_penalty=1.05,
                    temperature=0.1,
                    verbose=False
                )
                transcribed = response.text.strip()
                print(f"    Transcribed {len(transcribed)} characters.")
                
                html_content.append(f'  <div class="page" id="page-{page_num+1}">')
                for line in transcribed.split('\n'):
                    line = line.strip()
                    if line:
                        if line.startswith('$$'):
                            html_content.append(f'    <p>{line}</p>')
                        else:
                            html_content.append(f'    <p>{line}</p>')
                html_content.append('  </div><hr/>')
                
            except Exception as e:
                print(f"    Error on page {page_num+1}: {e}")
                
            if os.path.exists(tmp_img):
                os.remove(tmp_img)
                
        html_content.append('</main>')
        html_content.append('</body>')
        html_content.append('</html>')
        
        with open(f"college-electrical-engineering/{ch_name}.html", "w") as f:
            f.write('\n'.join(html_content))
            
        print(f"Finished {ch_name}.html")

if __name__ == '__main__':
    process_pdfs()
