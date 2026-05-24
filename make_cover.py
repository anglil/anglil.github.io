import sys
from PIL import Image, ImageDraw, ImageFont

img_path = "/Users/anglil/.gemini/antigravity/brain/259fcaf8-bb02-464b-8be5-339e21f479ec/soviet_math_cover_bg_1779032972929.png"
img = Image.open(img_path)

# Crop the book cover. The background is roughly #8E8F8D (142, 143, 141)
# We can find the bounding box by looking for pixels that differ from this background
bg = Image.new(img.mode, img.size, img.getpixel((0, 0)))
diff = Image.composite(img, bg, img) # This doesn't help. Let's just crop based on color difference
# Better way: getbbox of the difference from background
from PIL import ImageChops
diff = ImageChops.difference(img, bg)
bbox = diff.getbbox()

if bbox:
    img = img.crop(bbox)
else:
    print("Could not find bounding box, using full image")

# The image is now the cropped book cover
# We need to add text. 
draw = ImageDraw.Draw(img)
width, height = img.size

# Try to load a nice serif font, fallback to default if not found
try:
    title_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf", int(width * 0.12))
    author_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf", int(width * 0.05))
except:
    title_font = ImageFont.load_default()
    author_font = ImageFont.load_default()

title_text = "COLLEGE PHYSICS"
author_text = "Angli Liu"
location_text = "San Mateo"

# Calculate text sizes using textbbox
title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
title_w = title_bbox[2] - title_bbox[0]
title_h = title_bbox[3] - title_bbox[1]

author_bbox = draw.textbbox((0, 0), author_text, font=author_font)
author_w = author_bbox[2] - author_bbox[0]

loc_bbox = draw.textbbox((0, 0), location_text, font=author_font)
loc_w = loc_bbox[2] - loc_bbox[0]

# Draw title at top (around 15% down)
title_y = int(height * 0.12)
title_x = (width - title_w) / 2
# Soviet style faded red text: #A43F3F or dark grey #333333
draw.text((title_x, title_y), title_text, font=title_font, fill=(50, 50, 50, 255))

# Draw author and location at the bottom (around 85% down)
# The user wants "just my name and San Mateo besides the title"
# Wait, "besides the title" might mean literally next to it or just on the cover along with the title.
# Let's put it under the title, aligned nicely
author_y = title_y + title_h + int(height * 0.02)
author_x = (width - author_w) / 2
draw.text((author_x, author_y), author_text, font=author_font, fill=(100, 100, 100, 255))

loc_y = author_y + (author_bbox[3] - author_bbox[1]) + int(height * 0.01)
loc_x = (width - loc_w) / 2
draw.text((loc_x, loc_y), location_text, font=author_font, fill=(100, 100, 100, 255))

out_path = "college-physics/images/kdp_cover.jpg"
img.convert("RGB").save(out_path, quality=95)
print(f"Saved cover to {out_path}")
