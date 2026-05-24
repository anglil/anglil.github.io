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

extract_rect("ch02_page_001.png", "topic_blackbody.png", 0.52, 0.16, 0.68, 0.23)
extract_rect("ch02_page_001.png", "topic_photoelectric.png", 0.20, 0.24, 0.42, 0.40)
extract_rect("ch02_page_001.png", "topic_compton.png", 0.46, 0.25, 0.77, 0.38)
extract_rect("ch02_page_001.png", "topic_franck_hertz.png", 0.24, 0.42, 0.47, 0.48)
extract_rect("ch02_page_001.png", "topic_davisson.png", 0.20, 0.52, 0.38, 0.59)
extract_rect("ch02_page_001.png", "topic_stern_gerlach_1.png", 0.18, 0.70, 0.44, 0.76)
extract_rect("ch02_page_001.png", "topic_stern_gerlach_2.png", 0.55, 0.70, 0.81, 0.76)

print("Done")
