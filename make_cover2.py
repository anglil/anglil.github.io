import sys
from PIL import Image, ImageDraw, ImageFont

img_path = "/Users/anglil/.gemini/antigravity/brain/259fcaf8-bb02-464b-8be5-339e21f479ec/soviet_math_cover_bg_1779032972929.png"
img = Image.open(img_path)

# Crop the book cover by removing margins
width, height = img.size
left = int(width * 0.16)
top = int(height * 0.06)
right = int(width * 0.84)
bottom = int(height * 0.94)
img = img.crop((left, top, right, bottom))

draw = ImageDraw.Draw(img)
width, height = img.size

try:
    # Try different fallback paths for mac
    title_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf", int(width * 0.12))
    author_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf", int(width * 0.05))
except:
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", int(width * 0.12))
        author_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", int(width * 0.05))
    except:
        title_font = ImageFont.load_default()
        author_font = ImageFont.load_default()

title_text = "COLLEGE PHYSICS"
author_text = "Angli Liu"
location_text = "San Mateo"

def draw_centered_text(text, font, y, color):
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    x = (width - w) / 2
    draw.text((x, y), text, font=font, fill=color)
    return h

title_y = int(height * 0.12)
title_h = draw_centered_text(title_text, title_font, title_y, (50, 50, 50, 255))

author_y = title_y + title_h + int(height * 0.02)
author_h = draw_centered_text(author_text, author_font, author_y, (80, 80, 80, 255))

loc_y = author_y + author_h + int(height * 0.01)
draw_centered_text(location_text, author_font, loc_y, (80, 80, 80, 255))

out_path = "college-physics/images/kdp_cover.jpg"
img.convert("RGB").save(out_path, quality=95)
print(f"Saved cover to {out_path}")
