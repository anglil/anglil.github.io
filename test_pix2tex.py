import sys
from PIL import Image
from pix2tex.cli import LatexOCR

def main():
    img_path = sys.argv[1] if len(sys.argv) > 1 else "college-electrical-engineering/images/crop_ch01_page_001_1.png"
    print(f"Loading model and testing image: {img_path}")
    try:
        model = LatexOCR()
        img = Image.open(img_path)
        latex = model(img)
        print("RESULT LaTeX:")
        print(latex)
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    main()
