import re

with open("travel_book_final.md", "r") as f:
    content = f.read()

# Replace ![](URL) with ![](URL){width=3.5in}
pattern = r'!\[\]\(([^\)]+)\)(?!\{width=)'
new_content = re.sub(pattern, r'![](\1){width=3.5in}', content)

with open("travel_book_final.md", "w") as f:
    f.write(new_content)

print("Images shrunk to 3.5in!")
