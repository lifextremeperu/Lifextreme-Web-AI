import re

with open('seo-metatags.html', 'r', encoding='utf-8') as f:
    seo_content = f.read()

start_idx = seo_content.find('<!-- Meta Tags')
seo_content = seo_content[start_idx:]

with open('index.html', 'r', encoding='utf-8') as f:
    index_content = f.read()

new_seo_block = '\n    <link rel="llms-txt" href="/llms.txt">\n' + seo_content

index_content = re.sub(
    r'<meta name="description" content="Lifextreme.*?<meta name="llm-context" content=".*?">',
    new_seo_block,
    index_content,
    flags=re.DOTALL
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index_content)
print('Injection successful!')
