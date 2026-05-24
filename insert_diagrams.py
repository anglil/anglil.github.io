import glob
import os
import re
import shutil
from bs4 import BeautifulSoup

os.makedirs("college-electrical-engineering/images/diagrams", exist_ok=True)

diagrams = glob.glob("diagram_crops/*.png")
diagrams.sort()

for diag in diagrams:
    basename = os.path.basename(diag)
    shutil.copy(diag, f"college-electrical-engineering/images/diagrams/{basename}")

for ch_num in range(1, 5):
    html_file = f"college-electrical-engineering/ch{ch_num:02d}.html"
    if not os.path.exists(html_file): continue
    
    with open(html_file, 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')
        
    inserted = 0
    for diag in diagrams:
        basename = os.path.basename(diag)
        match = re.match(r'crop_ch(\d+)_page_(\d+)_', basename)
        if match:
            ch_id = int(match.group(1))
            if ch_id == ch_num:
                page_id = int(match.group(2))
                # Insert into the page div
                page_div = soup.find('div', id=f"page-{page_id}")
                if page_div:
                    img_tag = soup.new_tag('img', src=f"images/diagrams/{basename}", attrs={'class': 'diagram'})
                    page_div.append(img_tag)
                    inserted += 1
                    
    with open(html_file, 'w') as f:
        f.write(str(soup))
        
    print(f"Inserted {inserted} diagrams into {html_file}")
