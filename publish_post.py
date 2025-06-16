#!/usr/bin/env python3
"""
Publish script for BIO2025 Blog - converts Markdown to HTML
Usage: python3 publish_post.py post-slug
"""

import os
import sys
import re
from datetime import datetime

def parse_frontmatter(content):
    """Parse YAML frontmatter from markdown content"""
    if not content.startswith('---'):
        return {}, content
    
    lines = content.split('\n')
    frontmatter = {}
    content_start = 0
    
    for i, line in enumerate(lines[1:], 1):
        if line == '---':
            content_start = i + 1
            break
        if ':' in line:
            key, value = line.split(':', 1)
            frontmatter[key.strip()] = value.strip()
    
    return frontmatter, '\n'.join(lines[content_start:])

def markdown_to_html(markdown_content):
    """Convert markdown to HTML (basic implementation)"""
    html = markdown_content
    
    # Headers
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    
    # Bold and italic
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    
    # Links
    html = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', html)
    
    # Images (convert to figure/figcaption)
    html = re.sub(r'!\[(.+?)\]\((.+?)\)\n\*(.+?)\*', 
                  r'<figure>\n    <img src="\2" alt="\1" />\n    <figcaption>\3</figcaption>\n</figure>', html)
    html = re.sub(r'!\[(.+?)\]\((.+?)\)', r'<img src="\2" alt="\1" />', html)
    
    # Code blocks
    html = re.sub(r'```(\w+)?\n(.*?)\n```', r'<pre><code>\2</code></pre>', html, flags=re.DOTALL)
    html = re.sub(r'`(.+?)`', r'<code>\1</code>', html)
    
    # Blockquotes
    html = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', html, flags=re.MULTILINE)
    
    # Lists
    html = re.sub(r'^- (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'(<li>.*</li>)', r'<ul>\n\1\n</ul>', html, flags=re.DOTALL)
    
    # Paragraphs (split by double newlines, wrap non-tag lines)
    paragraphs = html.split('\n\n')
    processed = []
    for p in paragraphs:
        p = p.strip()
        if p and not p.startswith('<') and not p.endswith('>'):
            p = f'<p>{p}</p>'
        processed.append(p)
    
    return '\n\n'.join(processed)

def publish_post(slug):
    """Convert markdown to HTML and publish"""
    
    md_filepath = os.path.join("drafts", f"{slug}.md")
    html_filepath = os.path.join("posts", f"{slug}.html")
    
    if not os.path.exists(md_filepath):
        print(f"❌ Draft not found: {md_filepath}")
        print("💡 Run: python3 new_post.py \"Your Title\" to create a draft first")
        sys.exit(1)
    
    # Read markdown file
    with open(md_filepath, 'r') as f:
        content = f.read()
    
    # Parse frontmatter
    frontmatter, markdown_content = parse_frontmatter(content)
    
    title = frontmatter.get('title', 'Untitled')
    date_str = frontmatter.get('date', datetime.now().strftime("%Y-%m-%d"))
    excerpt = frontmatter.get('excerpt', 'No excerpt provided...')
    
    # Convert markdown to HTML
    html_content = markdown_to_html(markdown_content)
    
    # Generate full HTML page
    formatted_date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%B %d, %Y")
    
    full_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - BIO2025 Blog</title>
    <link rel="stylesheet" href="../styles.css">
</head>
<body>
    <header>
        <h1><a href="../index.html" style="text-decoration: none; color: inherit;">BIO2025 Blog</a></h1>
    </header>

    <main>
        <article class="post">
            <header>
                <h1>{title}</h1>
                <p class="post-meta">{formatted_date}</p>
            </header>
            <div class="post-content">
{html_content}
            </div>
        </article>
        
        <nav class="post-navigation">
            <a href="../index.html">← Back to Blog</a>
        </nav>
    </main>

    <footer>
        <p>&copy; 2025 BIO2025 Blog</p>
    </footer>
</body>
</html>'''
    
    # Write HTML file
    with open(html_filepath, 'w') as f:
        f.write(full_html)
    
    # Update index.html
    update_index(title, f"{slug}.html", date_str, excerpt)
    
    print(f"✅ Published post: {html_filepath}")
    print(f"📋 Updated index.html with post listing")
    print(f"🚀 Ready to commit and push!")

def update_index(title, filename, date_str, excerpt):
    """Add the new post to index.html"""
    
    # Read current index.html
    with open('index.html', 'r') as f:
        content = f.read()
    
    # Create new post item
    formatted_date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%B %d, %Y")
    new_post_item = f'''            <article class="post-item">
                <h3><a href="posts/{filename}">{title}</a></h3>
                <p class="post-meta">{formatted_date}</p>
                <p class="post-excerpt">{excerpt}</p>
            </article>

            <!-- Add new posts here - newest first -->'''
    
    # Replace the comment line with new post + comment
    content = content.replace(
        '            <!-- Add new posts here - newest first -->',
        new_post_item
    )
    
    # Write back to index.html
    with open('index.html', 'w') as f:
        f.write(content)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 publish_post.py post-slug")
        print("Example: python3 publish_post.py my-awesome-post")
        sys.exit(1)
    
    slug = sys.argv[1]
    publish_post(slug)
