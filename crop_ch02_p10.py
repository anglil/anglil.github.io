import os
from PIL import Image

in_dir = 'college-physics/images'
out_dir = 'college-physics/images'

def extract_rect(img_name, out_name, x0_pct, y0_pct, x1_pct, y1_pct):
    in_path = os.path.join(in_dir, img_name)
    out_path = os.path.join(out_dir, out_name)
    img = Image.open(in_path)
    width, height = img.size
    box = (
        int(width * x0_pct),
        int(height * y0_pct),
        int(width * x1_pct),
        int(height * y1_pct)
    )
    cropped = img.crop(box)
    cropped.save(out_path)
    print(f"Saved {out_path}")

extract_rect("ch02_page_010.png", "topic_square_transmission.png", 0.25, 0.10, 0.40, 0.16)
extract_rect("ch02_page_010.png", "topic_delta_well.png", 0.15, 0.22, 0.28, 0.28)
extract_rect("ch02_page_010.png", "topic_delta_barrier.png", 0.10, 0.85, 0.25, 0.92)

print("Done")
