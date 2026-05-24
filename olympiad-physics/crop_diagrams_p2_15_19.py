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
    # Define paths
    base_dir = "/Users/anglil/.gemini/antigravity/brain/259fcaf8-bb02-464b-8be5-339e21f479ec/scratch/pdf_pages"
    output_dir = "/Users/anglil/.gemini/antigravity/scratch/anglil.github.io/olympiad-physics/images"
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Pendulum
    crop_image(
        os.path.join(base_dir, "p2_page_016.png"),
        os.path.join(output_dir, "topic_massive_pendulum.png"),
        (60, 680, 250, 880) # left, top, right, bottom
    )
    
    # 2. Compton scattering
    crop_image(
        os.path.join(base_dir, "p2_page_017.png"),
        os.path.join(output_dir, "topic_compton_scattering.png"),
        (600, 680, 880, 820)
    )
    
    # 3. Coordinate system
    crop_image(
        os.path.join(base_dir, "p2_page_018.png"),
        os.path.join(output_dir, "topic_special_em_field.png"),
        (250, 200, 700, 420)
    )
