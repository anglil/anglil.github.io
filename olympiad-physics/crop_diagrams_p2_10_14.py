import os
from PIL import Image

in_dir = '/Users/anglil/.gemini/antigravity/brain/259fcaf8-bb02-464b-8be5-339e21f479ec/scratch/pdf_pages'
out_dir = '/Users/anglil/.gemini/antigravity/scratch/anglil.github.io/olympiad-physics/images'

if not os.path.exists(out_dir):
    os.makedirs(out_dir)

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

# p2_page_011.png - Magnetohydrodynamic Generator
extract_rect("p2_page_011.png", "topic_mhd_generator.png", 0.15, 0.28, 0.75, 0.47)

# p2_page_012.png - Self-Inductance of Two Parallel Wires
extract_rect("p2_page_012.png", "topic_parallel_wires_inductance.png", 0.2, 0.12, 0.7, 0.25)

# p2_page_013.png - Conductor Reaching Electrostatic Equilibrium
extract_rect("p2_page_013.png", "topic_electrostatic_equilibrium.png", 0.25, 0.12, 0.7, 0.25)

# p2_page_014.png - Light Propagation in Optical Fibers
extract_rect("p2_page_014.png", "topic_optical_fiber_1.png", 0.18, 0.12, 0.75, 0.25)
extract_rect("p2_page_014.png", "topic_optical_fiber_2.png", 0.15, 0.67, 0.7, 0.82)

# p2_page_015.png - Acceleration Equivalent Gravitational Field
extract_rect("p2_page_015.png", "topic_accel_equiv_gravity.png", 0.2, 0.26, 0.55, 0.36)

print("Done")
