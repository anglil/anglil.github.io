import re
from deep_translator import GoogleTranslator

# Open the raw markdown
with open("travel_raw.md", "r") as f:
    lines = f.readlines()

translator = GoogleTranslator(source='it', target='en')

out_lines = []
is_italian_section = False
current_italian_article_lines = []

def translate_chunk(text):
    if not text.strip(): return text
    # GoogleTranslator has a 5000 char limit
    try:
        return translator.translate(text)
    except Exception as e:
        print("Translation error:", e)
        return text

def process_italian_article(lines):
    print("Translating article...")
    # join lines
    full_text = "".join(lines)
    # The header is the first line
    header_match = re.match(r'(# \*\*)(.*?)(\*\*)', lines[0])
    if header_match:
        it_title = header_match.group(2)
        en_title = translate_chunk(it_title)
        lines_to_translate = lines[1:]
    else:
        en_title = "English Translation"
        lines_to_translate = lines
        
    en_body = []
    # Translate paragraph by paragraph to maintain markdown and avoid limit
    for line in lines_to_translate:
        if line.startswith("<img") or line.startswith("style="):
            en_body.append(line)
        elif line.strip() == "":
            en_body.append(line)
        else:
            en_body.append(translate_chunk(line) + "\n")
            
    return f"\n# **{en_title} (English Translation)**\n\n" + "".join(en_body)

for line in lines:
    if "# **Un Viaggio al Lago Tahoe e a Sacramento**" in line:
        is_italian_section = True
        
    if is_italian_section:
        if line.startswith("# **") and len(current_italian_article_lines) > 0:
            # End of an Italian article, process it
            out_lines.extend(current_italian_article_lines)
            out_lines.append(process_italian_article(current_italian_article_lines))
            current_italian_article_lines = []
            
        current_italian_article_lines.append(line)
    else:
        out_lines.append(line)

# process the last article
if len(current_italian_article_lines) > 0:
    out_lines.extend(current_italian_article_lines)
    out_lines.append(process_italian_article(current_italian_article_lines))

with open("travel_book_final.md", "w") as f:
    f.writelines(out_lines)

print("Translation and formatting complete.")
