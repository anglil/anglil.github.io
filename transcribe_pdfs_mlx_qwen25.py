import fitz  # PyMuPDF
from mlx_vlm import load, generate
from mlx_vlm.prompt_utils import apply_chat_template
import os

def transcribe_pdfs():
    print("Loading mlx-community/Qwen2.5-VL-7B-Instruct-4bit...")
    model_path = "mlx-community/Qwen2.5-VL-7B-Instruct-4bit"
    model, processor = load(model_path)
    
    # Process only ch01 to ch04 PDFs mapping
    pdf_files = [
        ("notes/circuits principles, experiments, and semiconductors.pdf", "ch01"),
        ("notes/communication circuits.pdf", "ch02"),
        ("notes/antennae.pdf", "ch03"),
        ("notes/digital electronics.pdf", "ch04")
    ]
    
    output_dir = "college-electrical-engineering"
    os.makedirs(output_dir, exist_ok=True)
    
    for pdf_path, ch_name in pdf_files:
        if not os.path.exists(pdf_path):
            print(f"Skipping {pdf_path}, file not found.")
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
            '<main class="content">'
        ]
        
        for page_num in range(len(doc)):
            print(f"  Transcribing page {page_num + 1}/{len(doc)}...", flush=True)
            page = doc.load_page(page_num)
            pix = page.get_pixmap(dpi=150)
            
            img_path = f"temp_page_{ch_name}.jpg"
            pix.save(img_path)
            
            prompt = """Extract all text and mathematical formulas from this handwritten note. Translate all Chinese text to fluent, coherent English prose. Do not include any Chinese in your output. Preserve all mathematical LaTeX formulas exactly as written (wrapped in $$...$$ for block math or $...$ for inline math). Do not hallucinate or repeat text. Output only the extracted English text and math."""
            
            messages = [
                {
                    "role": "user",
                    "content": "<|vision_start|><|image_pad|><|vision_end|>" + prompt
                }
            ]
            
            prompt_fmt = apply_chat_template(processor, model.config, messages, add_generation_prompt=True)            
            try:
                response = generate(model, processor, prompt=prompt_fmt, image=img_path, verbose=False, max_tokens=1500)
                transcribed = response.text.strip()
            except Exception as e:
                print(f"Error on page {page_num}: {e}")
                transcribed = ""
                
            # Clean up artifacts if any
            transcribed = transcribed.replace('<|box_start|>', '').replace('<|box_end|>', '').replace('<|quad_start|>', '').replace('<|quad_end|>', '')
            if transcribed.startswith('```'):
                transcribed = '\n'.join(transcribed.split('\n')[1:])
            if transcribed.endswith('```'):
                transcribed = transcribed[:-3]
            
            html_content.append(f'  <div class="page" id="page-{page_num + 1}">')
            
            # Wrap paragraphs, but avoid breaking $$ blocks.
            # A simple approach: split by \n\n instead of \n, so multiline math blocks stay intact!
            blocks = transcribed.split('\n\n')
            for block in blocks:
                block = block.strip()
                if block:
                    html_content.append(f'    <p>{block}</p>')
                    
            html_content.append('  </div><hr>')
            
            # Write to file progressively
            with open(f"{output_dir}/{ch_name}.html", 'w', encoding='utf-8') as f:
                f.write('\n'.join(html_content) + '\n</main>\n</body>\n</html>')
                
        print(f"Finished {ch_name}.html\n")
        
    print("Done transcribing all PDFs.")

transcribe_pdfs()
