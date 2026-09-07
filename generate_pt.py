import shutil

shutil.copy("en/index.html", "pt/index.html")

with open("pt/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Make necessary adjustments for PT
content = content.replace('data-en.js', 'data-pt.js')
content = content.replace('lang="en"', 'lang="pt"')

with open("pt/index.html", "w", encoding="utf-8") as f:
    f.write(content)
print("pt/index.html generated successfully!")
