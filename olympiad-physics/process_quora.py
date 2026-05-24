import json
import os
import re
import urllib.request
from bs4 import BeautifulSoup
from markdownify import markdownify as md

with open("raw_quora_content.json", "r") as f:
    data = json.load(f)

if not os.path.exists("travel_images"):
    os.makedirs("travel_images")

book_md = f"# Chasing Horizons: Footprints in the Clouds\n\n**Angli Liu**\n\n---\n\n"
image_count = 0

for i, post in enumerate(data):
    html = post["html"]
    if not html:
        continue
        
    soup = BeautifulSoup(html, "html.parser")
    
    # Download images and replace src
    for img in soup.find_all("img"):
        src = img.get("src")
        # Quora sometimes uses data-src for lazy loading
        if img.has_attr("data-src") and "http" in img["data-src"]:
            src = img["data-src"]
            
        if src and src.startswith("http"):
            try:
                # Need to download
                ext = src.split(".")[-1].split("?")[0]
                if ext not in ["jpg", "png", "jpeg", "webp", "gif"]:
                    ext = "jpg"
                
                image_count += 1
                img_path = f"travel_images/img_{i}_{image_count}.{ext}"
                
                req = urllib.request.Request(src, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=10) as response, open(img_path, "wb") as out_file:
                    out_file.write(response.read())
                    
                img["src"] = img_path
            except Exception as e:
                print(f"Failed to download image {src}: {e}")
                
    # Remove script tags
    for script in soup(["script", "style"]):
        script.decompose()

    # Convert to markdown
    markdown_text = md(str(soup), heading_style="ATX")
    
    # Clean up empty links and excessive newlines
    markdown_text = re.sub(r'\[\s*\]\([^\)]+\)', '', markdown_text)
    markdown_text = re.sub(r'\n{3,}', '\n\n', markdown_text)
    
    title_text = post["title"].split(" - ")[0]
    
    book_md += f"## {title_text}\n\n"
    book_md += markdown_text.strip() + "\n\n---\n\n"
    print(f"Processed post {i+1}")

with open("raw_travel_book.md", "w") as f:
    f.write(book_md)
print(f"Done! Wrote raw_travel_book.md with {image_count} images.")
