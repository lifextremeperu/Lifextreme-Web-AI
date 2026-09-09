import os
import json
import glob

def build_index():
    blog_dir = os.path.join('data', 'blog', 'geo_seo')
    output_file = os.path.join('data', 'blog', 'index.json')
    
    if not os.path.exists(blog_dir):
        print(f"Directory {blog_dir} does not exist.")
        return

    articles = []
    
    for filepath in glob.glob(os.path.join(blog_dir, '*.md')):
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
            title = "Sin título"
            summary = "..."
            
            # Simple extraction: First line starting with # is title, next non-empty is summary
            for line in lines:
                line = line.strip()
                if line.startswith('#') and title == "Sin título":
                    title = line.replace('#', '').strip()
                elif line and title != "Sin título" and summary == "...":
                    if not line.startswith('#'):
                        summary = line[:150] + "..."
                        break
            
            slug = os.path.basename(filepath)
            
            articles.append({
                "id": slug,
                "title": title,
                "summary": summary,
                "date": "2026-09-08",
                "file": f"/data/blog/geo_seo/{slug}",
                "author": "Lifextreme AI"
            })
            
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(articles, f, indent=4, ensure_ascii=False)
        
    print(f"Blog index built successfully with {len(articles)} articles!")

if __name__ == '__main__':
    build_index()
