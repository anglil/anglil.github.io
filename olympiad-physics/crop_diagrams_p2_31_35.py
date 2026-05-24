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
    
    # p2_page_035.png - Brachistochrone
    crop_image(
        os.path.join(base_dir, "p2_page_035.png"),
        os.path.join(output_dir, "topic_brachistochrone.png"),
        (150, 270, 600, 430)
    )
