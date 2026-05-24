import os
from PIL import Image

in_dir = 'college-physics/images'
out_dir = 'college-physics/images'

def extract_rect(img_name, out_name, x0_pct, y0_pct, x1_pct, y1_pct):
    in_path = os.path.join(in_dir, img_name)
    out_path = os.path.join(out_dir, out_name)
    try:
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
    except Exception as e:
        print(f"Error processing {img_name}: {e}")

extract_rect("ch05_page_002.png", "topic_spatial_coherence.png", 0.05, 0.08, 0.55, 0.28)
extract_rect("ch05_page_003.png", "topic_young_double_slit.png", 0.05, 0.20, 0.55, 0.32)
extract_rect("ch05_page_004.png", "topic_equal_thickness_wedge.png", 0.05, 0.18, 0.35, 0.28)
extract_rect("ch05_page_004.png", "topic_air_wedge.png", 0.05, 0.45, 0.35, 0.58)
extract_rect("ch05_page_005.png", "topic_equal_inclination.png", 0.05, 0.15, 0.30, 0.30)
extract_rect("ch05_page_006.png", "topic_single_slit.png", 0.05, 0.40, 0.50, 0.62)
extract_rect("ch05_page_006.png", "topic_phasor_single_slit.png", 0.05, 0.62, 0.30, 0.72)
extract_rect("ch05_page_007.png", "topic_circular_aperture.png", 0.10, 0.35, 0.35, 0.55) # Adjusted y0 from 0.48 to 0.35
extract_rect("ch05_page_009.png", "topic_xray_point.png", 0.10, 0.32, 0.45, 0.45)
extract_rect("ch05_page_009.png", "topic_xray_plane.png", 0.10, 0.45, 0.45, 0.60)
extract_rect("ch05_page_010.png", "topic_reflection_refraction_coords.png", 0.55, 0.15, 0.95, 0.35)
extract_rect("ch05_page_012.png", "topic_brewster_angle.png", 0.25, 0.25, 0.55, 0.45)
extract_rect("ch05_page_014.png", "topic_crystal_wave_surfaces.png", 0.05, 0.05, 0.65, 0.20)
extract_rect("ch05_page_014.png", "topic_huygens_birefringence.png", 0.10, 0.25, 0.45, 0.40)
extract_rect("ch05_page_014.png", "topic_polarizing_prisms.png", 0.05, 0.45, 0.95, 0.60)
extract_rect("ch05_page_014.png", "topic_waveplate.png", 0.05, 0.62, 0.65, 0.78)
extract_rect("ch05_page_015.png", "topic_analyzer_polarizer.png", 0.05, 0.15, 0.35, 0.32)

print("Done")
