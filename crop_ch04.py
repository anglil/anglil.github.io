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

# ch04_page_001.png
extract_rect("ch04_page_001.png", "topic_shm_addition_2.png", 0.50, 0.15, 0.80, 0.28)
extract_rect("ch04_page_001.png", "topic_shm_addition_n.png", 0.45, 0.38, 0.80, 0.55)

# ch04_page_006.png
extract_rect("ch04_page_006.png", "topic_positive_crystal.png", 0.10, 0.85, 0.35, 0.98)
extract_rect("ch04_page_006.png", "topic_negative_crystal.png", 0.60, 0.85, 0.85, 0.98)

# ch04_page_007.png
extract_rect("ch04_page_007.png", "topic_polarization_1.png", 0.65, 0.32, 0.90, 0.44)
extract_rect("ch04_page_007.png", "topic_polarization_2.png", 0.65, 0.50, 0.85, 0.62)

print("Done")
