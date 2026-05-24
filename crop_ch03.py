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

# ch03_page_004.png
extract_rect("ch03_page_004.png", "topic_dielectric_reflection.png", 0.02, 0.17, 0.18, 0.26)
extract_rect("ch03_page_004.png", "topic_n_wave_graph.png", 0.05, 0.46, 0.28, 0.65)
extract_rect("ch03_page_004.png", "topic_p_wave_graph.png", 0.48, 0.46, 0.68, 0.65)

# ch03_page_006.png
extract_rect("ch03_page_006.png", "topic_conductor_reflection.png", 0.02, 0.18, 0.18, 0.26)

# ch03_page_007.png
extract_rect("ch03_page_007.png", "topic_n_wave_vectors.png", 0.02, 0.15, 0.15, 0.28)
extract_rect("ch03_page_007.png", "topic_p_wave_vectors.png", 0.02, 0.65, 0.15, 0.76)

# ch03_page_009.png
extract_rect("ch03_page_009.png", "topic_bremsstrahlung.png", 0.72, 0.36, 0.82, 0.44)
extract_rect("ch03_page_009.png", "topic_synchrotron.png", 0.77, 0.40, 0.95, 0.48)

print("Done")
