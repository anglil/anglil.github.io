import os
import re

html_files = [
    "college-physics/ch01.html",
    "college-physics/ch02.html",
    "college-physics/ch03.html",
    "college-physics/ch04.html",
    "college-physics/ch05.html"
]

all_content = []

for filepath in html_files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Extract everything inside <main id="content"> ... </main>
    # Using regex with DOTALL to match across newlines
    match = re.search(r'<main id="content">(.*?)</main>', content, re.DOTALL)
    if match:
        main_content = match.group(1).strip()
        all_content.append(f"<div class='chapter-content'>\n{main_content}\n</div>")
    else:
        # Fallback to <div class="container"> for ch05 if it's there
        match = re.search(r'<div class="container">(.*?)</div>\s*</body>', content, re.DOTALL)
        if match:
            main_content = match.group(1).strip()
            all_content.append(f"<div class='chapter-content'>\n{main_content}\n</div>")
        else:
            print(f"Warning: Could not extract content from {filepath}")

# Wrap it in a single HTML document
final_html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>College Physics</title>
  <style>
    /* Basic KDP styles */
    body { font-family: serif; line-height: 1.5; padding: 2em; }
    h1, h2, h3 { text-align: left; }
    .chapter-header { text-align: center; margin-bottom: 2em; page-break-before: always; }
    .chapter-content { page-break-before: always; }
    .diagram-container { text-align: center; margin: 1em 0; }
    .diagram-caption { font-size: 0.9em; font-style: italic; }
    img { max-width: 100%; height: auto; }
  </style>
</head>
<body>
  <div style="text-align: center; margin-top: 20%; page-break-after: always;">
    <h1>College Physics</h1>
    <h2>Angli Liu</h2>
  </div>
""" + "\n".join(all_content) + "\n</body>\n</html>"

output_path = "college-physics/kdp_manuscript.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(final_html)

print(f"Wrote {output_path}")
