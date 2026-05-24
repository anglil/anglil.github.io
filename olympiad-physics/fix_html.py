with open("travel_book_final.md", "r") as f:
    text = f.read()

text = text.replace("<u>", "").replace("</u>", "")

with open("travel_book_final.md", "w") as f:
    f.write(text)
print("Removed u tags")
