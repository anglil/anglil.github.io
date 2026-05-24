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
    
    # p2_page_041.png
    crop_image(
        os.path.join(base_dir, "p2_page_041.png"),
        os.path.join(output_dir, "exp_ohmmeter.png"),
        (110, 460, 520, 610)
    )
    
    # p2_page_042.png
    crop_image(
        os.path.join(base_dir, "p2_page_042.png"),
        os.path.join(output_dir, "exp_simple_pendulum.png"),
        (240, 530, 470, 750)
    )
    
    # p2_page_043.png
    crop_image(
        os.path.join(base_dir, "p2_page_043.png"),
        os.path.join(output_dir, "exp_refractive_index.png"),
        (220, 490, 600, 710)
    )
    crop_image(
        os.path.join(base_dir, "p2_page_043.png"),
        os.path.join(output_dir, "exp_double_slit.png"),
        (210, 840, 850, 970)
    )
    
    # p2_page_044.png
    crop_image(
        os.path.join(base_dir, "p2_page_044.png"),
        os.path.join(output_dir, "exp_momentum.png"),
        (220, 570, 570, 760)
    )
