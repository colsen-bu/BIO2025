#!/usr/bin/env python3
"""
Simple blog post generator for BIO2025 Blog
Usage: python new_post.py "Post Title"
"""

import os
import sys
import re
from datetime import datetime

def slugify(text):
    """Convert title to URL-friendly slug"""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'\s+', '-', text)
    text = text.strip('-')
    return text

def create_post(title):
    """Create a new blog post file and update index.html"""
    
    # Generate filename
    slug = slugify(title)
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{slug}.html"
    filepath = os.path.join("posts", filename)
    
    # Generate post content
    post_content = f'''<!DOCTYPE html>
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
                <p class="post-meta">{datetime.now().strftime("%B %d, %Y")}</p>
            </header>
            <div class="post-content">
                <p>Write your post content here...</p>
                
                <!-- Example image -->
                <!--
                <figure>
                    <img src="../media/images/your-image.jpg" alt="Description" />
                    <figcaption>Image caption</figcaption>
                </figure>
                -->
                
                <!-- Example video -->
                <!--
                <figure>
                    <video controls width="100%">
                        <source src="../media/videos/your-video.mp4" type="video/mp4">
                        Your browser does not support the video tag.
                    </video>
                    <figcaption>Video caption</figcaption>
                </figure>
                -->
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
    
    # Write the post file
    with open(filepath, 'w') as f:
        f.write(post_content)
    
    # Update index.html
    update_index(title, filename, date_str)
    
    print(f"✅ Created new post: {filepath}")
    print(f"📝 Edit the content in VS Code, then commit and push to publish!")
    print(f"🔗 Will be available at: posts/{filename}")

def update_index(title, filename, date_str):
    """Add the new post to index.html"""
    
    # Read current index.html
    with open('index.html', 'r') as f:
        content = f.read()
    
    # Create new post item
    formatted_date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%B %d, %Y")
    new_post_item = f'''            <article class="post-item">
                <h3><a href="posts/{filename}">{title}</a></h3>
                <p class="post-meta">{formatted_date}</p>
                <p class="post-excerpt">Write a brief excerpt here...</p>
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
    
    print(f"📋 Updated index.html with new post listing")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python new_post.py \"Post Title\"")
        sys.exit(1)
    
    title = sys.argv[1]
    create_post(title)
