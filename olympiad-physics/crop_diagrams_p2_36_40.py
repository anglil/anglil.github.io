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
    
    # p2_page_037.png
    crop_image(
        os.path.join(base_dir, "p2_page_037.png"),
        os.path.join(output_dir, "exp_spring_elongation.png"),
        (150, 800, 750, 970)
    )
    
    # p2_page_038.png
    crop_image(
        os.path.join(base_dir, "p2_page_038.png"),
        os.path.join(output_dir, "exp_parallelogram_rule.png"),
        (260, 680, 480, 830)
    )
    
    # p2_page_039.png
    crop_image(
        os.path.join(base_dir, "p2_page_039.png"),
        os.path.join(output_dir, "exp_newtons_laws.png"),
        (90, 180, 470, 300)
    )
    crop_image(
        os.path.join(base_dir, "p2_page_039.png"),
        os.path.join(output_dir, "exp_work_energy.png"),
        (130, 670, 830, 950)
    )
    
    # p2_page_040.png
    crop_image(
        os.path.join(base_dir, "p2_page_040.png"),
        os.path.join(output_dir, "exp_resistivity_circuit.png"),
        (170, 820, 400, 950)
    )
