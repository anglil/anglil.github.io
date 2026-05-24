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
    
    # p2_page_026.png - Fizeau and Foucault
    crop_image(
        os.path.join(base_dir, "p2_page_026.png"),
        os.path.join(output_dir, "topic_fizeau_wheel.png"),
        (100, 160, 850, 390)
    )
    crop_image(
        os.path.join(base_dir, "p2_page_026.png"),
        os.path.join(output_dir, "topic_foucault_mirror.png"),
        (30, 770, 900, 980)
    )
    
    # p2_page_027.png - Michelson
    crop_image(
        os.path.join(base_dir, "p2_page_027.png"),
        os.path.join(output_dir, "topic_michelson_prism.png"),
        (50, 340, 900, 520)
    )
    
    # p2_page_028.png - Damped spring
    crop_image(
        os.path.join(base_dir, "p2_page_028.png"),
        os.path.join(output_dir, "topic_damped_spring.png"),
        (120, 160, 450, 260)
    )
