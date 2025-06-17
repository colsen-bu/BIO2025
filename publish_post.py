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
    """Convert markdown to HTML (improved implementation)"""
    html = markdown_content
    
    # Process in order of complexity to avoid conflicts
    
    # Code blocks first (to protect them from other processing)
    html = re.sub(r'```(\w+)?\n(.*?)\n```', r'<pre><code>\2</code></pre>', html, flags=re.DOTALL)
    
    # Images with captions (must come before regular images)
    html = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)\s*\n\*([^*]+)\*', 
                  r'<figure>\n    <img src="\2" alt="\1" />\n    <figcaption>\3</figcaption>\n</figure>', html)
    
    # Regular images
    html = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1" />', html)
    
    # Links (after images to avoid conflicts)
    html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html)
    
    # Headers
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    
    # Bold and italic (be more specific with patterns)
    html = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', html)
    
    # Inline code
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
    
    # Blockquotes
    html = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', html, flags=re.MULTILINE)
    
    # Unordered lists
    lines = html.split('\n')
    in_list = False
    processed_lines = []
    
    for line in lines:
        if re.match(r'^- .+', line):
            if not in_list:
                processed_lines.append('<ul>')
                in_list = True
            processed_lines.append(re.sub(r'^- (.+)', r'    <li>\1</li>', line))
        else:
            if in_list:
                processed_lines.append('</ul>')
                in_list = False
            processed_lines.append(line)
    
    if in_list:
        processed_lines.append('</ul>')
    
    html = '\n'.join(processed_lines)
    
    # Ordered lists
    lines = html.split('\n')
    in_list = False
    processed_lines = []
    
    for line in lines:
        if re.match(r'^\d+\. .+', line):
            if not in_list:
                processed_lines.append('<ol>')
                in_list = True
            processed_lines.append(re.sub(r'^\d+\. (.+)', r'    <li>\1</li>', line))
        else:
            if in_list:
                processed_lines.append('</ol>')
                in_list = False
            processed_lines.append(line)
    
    if in_list:
        processed_lines.append('</ol>')
    
    html = '\n'.join(processed_lines)
    
    # Paragraphs (split by double newlines, wrap non-tag lines)
    paragraphs = html.split('\n\n')
    processed = []
    for p in paragraphs:
        p = p.strip()
        if p:
            # Don't wrap if it's already a block element
            if not re.match(r'^<(h[1-6]|ul|ol|li|blockquote|pre|figure|img)', p):
                # Don't wrap if it contains only block elements
                if not re.match(r'^<[^>]+>.*</[^>]+>$', p, re.DOTALL):
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
    """Add the new post to index.html at the top (newest first)"""
    
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

'''
    
    # Find the post-list div and insert the new post right after the comment
    # This ensures new posts always appear at the top
    post_list_pattern = r'(<!-- Posts will be listed here chronologically -->\s*\n)'
    replacement = f'\\1\n{new_post_item}'
    
    content = re.sub(post_list_pattern, replacement, content)
    
    # If the pattern above didn't work, try the fallback method
    if '<!-- Posts will be listed here chronologically -->' in content and new_post_item.strip() not in content:
        content = content.replace(
            '            <!-- Posts will be listed here chronologically -->',
            f'            <!-- Posts will be listed here chronologically -->\n\n{new_post_item}'
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
