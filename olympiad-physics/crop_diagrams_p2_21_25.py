import os
from PIL import Image

def crop_image(input_path, output_path, crop_box):
    try:
        img = Image.open(input_path)
        cropped_img = img.crop(crop_box)
        cropped_img.save(output_path)
        print(f"Successfully cropped and saved {output_path}")
    except Exception as e:
        print(f"Error processing {input_path}: {e}")

if __name__ == "__main__":
    base_dir = "/Users/anglil/.gemini/antigravity/brain/259fcaf8-bb02-464b-8be5-339e21f479ec/scratch/pdf_pages"
    output_dir = "/Users/anglil/.gemini/antigravity/scratch/anglil.github.io/olympiad-physics/images"
    
    os.makedirs(output_dir, exist_ok=True)
    
    # p2_page_024.png - Neutron Gravity Interferometer
    # Top view
    crop_image(
        os.path.join(base_dir, "p2_page_024.png"),
        os.path.join(output_dir, "topic_neutron_interferometer_top.png"),
        (90, 240, 680, 420)
    )
    # 3D view
    crop_image(
        os.path.join(base_dir, "p2_page_024.png"),
        os.path.join(output_dir, "topic_neutron_interferometer_3d.png"),
        (160, 420, 680, 560)
    )
    
    # p2_page_025.png - Michelson-Morley
    # Top diagram
    crop_image(
        os.path.join(base_dir, "p2_page_025.png"),
        os.path.join(output_dir, "topic_michelson_morley_1.png"),
        (30, 150, 450, 310)
    )
    # Middle diagram
    crop_image(
        os.path.join(base_dir, "p2_page_025.png"),
        os.path.join(output_dir, "topic_michelson_morley_2.png"),
        (50, 330, 450, 470)
    )
