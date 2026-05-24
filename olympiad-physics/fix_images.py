import re

with open("travel_book_final.md", "r") as f:
    content = f.read()

# Replace multi-line <img ... /> tags with markdown images
# Pattern matches <img src="URL" ... /> across multiple lines
pattern = r'<img\s+src="([^"]+)"[^>]*>'
new_content = re.sub(pattern, r'![](\1)', content, flags=re.IGNORECASE)

with open("travel_book_final.md", "w") as f:
    f.write(new_content)

print("Images fixed!")
