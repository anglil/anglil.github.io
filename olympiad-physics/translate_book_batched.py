import re
from deep_translator import GoogleTranslator

with open("travel_raw.md", "r") as f:
    lines = f.readlines()

translator = GoogleTranslator(source='it', target='en')

out_lines = []
is_italian_section = False
current_italian_article_lines = []

def translate_chunks(texts):
    # Join into chunks of max 4000 chars
    chunks = []
    curr_chunk = ""
    for text in texts:
        if len(curr_chunk) + len(text) > 4000:
            chunks.append(curr_chunk)
            curr_chunk = text + "\n"
        else:
            curr_chunk += text + "\n"
    if curr_chunk:
        chunks.append(curr_chunk)
        
    translated = []
    for chunk in chunks:
        if not chunk.strip(): continue
        try:
            res = translator.translate(chunk)
            translated.append(res + "\n")
        except Exception as e:
            print("Translation error:", e)
            translated.append(chunk + "\n")
            
    return "".join(translated)

def process_italian_article(lines):
    print("Translating article...")
    # The header is the first line
    header_match = re.match(r'(# \*\*)(.*?)(\*\*)', lines[0])
    if header_match:
        it_title = header_match.group(2)
        en_title = translate_chunks([it_title]).strip()
        lines_to_translate = lines[1:]
    else:
        en_title = "English Translation"
        lines_to_translate = lines
        
    en_body = []
    curr_text_block = []
    
    for line in lines_to_translate:
        if line.startswith("<img") or line.startswith("style="):
            if curr_text_block:
                en_body.append(translate_chunks(curr_text_block))
                curr_text_block = []
            en_body.append(line)
        elif line.strip() == "":
            if curr_text_block:
                en_body.append(translate_chunks(curr_text_block))
                curr_text_block = []
            en_body.append(line)
        else:
            curr_text_block.append(line.strip())
            
    if curr_text_block:
        en_body.append(translate_chunks(curr_text_block))
            
    return f"\n# **{en_title} (English Translation)**\n\n" + "".join(en_body)

for line in lines:
    if "# **Un Viaggio al Lago Tahoe e a Sacramento**" in line:
        is_italian_section = True
        
    if is_italian_section:
        if line.startswith("# **") and len(current_italian_article_lines) > 0:
            out_lines.extend(current_italian_article_lines)
            out_lines.append(process_italian_article(current_italian_article_lines))
            current_italian_article_lines = []
            
        current_italian_article_lines.append(line)
    else:
        out_lines.append(line)

if len(current_italian_article_lines) > 0:
    out_lines.extend(current_italian_article_lines)
    out_lines.append(process_italian_article(current_italian_article_lines))

with open("travel_book_final.md", "w") as f:
    f.writelines(out_lines)

print("Translation and formatting complete.")
