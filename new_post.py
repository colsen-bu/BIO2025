#!/usr/bin/env python3
"""
Enhanced blog post generator for BIO2025 Blog with Markdown support
Usage: 
  python3 new_post.py "Post Title"           # Creates markdown file for writing
  python3 publish_post.py post-slug          # Converts markdown to HTML and publishes
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
    """Create a new markdown file for writing"""
    
    # Generate filename
    slug = slugify(title)
    md_filename = f"{slug}.md"
    md_filepath = os.path.join("drafts", md_filename)
    
    # Create drafts directory if it doesn't exist
    os.makedirs("drafts", exist_ok=True)
    
    # Generate markdown content
    post_content = f'''---
title: {title}
date: {datetime.now().strftime("%Y-%m-%d")}
excerpt: Write a brief excerpt here that will appear on the homepage...
---

# {title}

Write your post content here in **Markdown**! Much easier than HTML.

## Adding Images

You can reference images like this:
```
![Alt text](../media/images/your-image.jpg)
*Image caption goes here*
```

## Adding Videos

For videos, you'll need to use HTML (but just for the video tag):
```html
<figure>
    <video controls width="100%">
        <source src="../media/videos/your-video.mp4" type="video/mp4">
        Your browser does not support the video tag.
    </video>
    <figcaption>Video caption</figcaption>
</figure>
```

## Markdown Benefits

- **Bold text** and *italic text*
- [Links](https://example.com) 
- Lists (like this one!)
- Code blocks with syntax highlighting
- > Blockquotes
- Tables, headers, and more!

Much easier than writing HTML by hand!

---

**Instructions:**
1. Edit this file in VS Code with nice Markdown preview
2. When ready to publish, run: `python3 publish_post.py {slug}`
3. The script will convert to HTML and update your blog
'''
    
    # Write the markdown file
    with open(md_filepath, 'w') as f:
        f.write(post_content)
    
    print(f"✅ Created new post draft: {md_filepath}")
    print(f"📝 Edit the Markdown file in VS Code (much easier than HTML!)")
    print(f"� When ready to publish, run: python3 publish_post.py {slug}")
    print(f"💡 Tip: Use Cmd+Shift+V to preview Markdown in VS Code")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 new_post.py \"Post Title\"")
        print("This creates a Markdown file for easy writing.")
        print("Use publish_post.py to convert to HTML when ready.")
        sys.exit(1)
    
    title = sys.argv[1]
    create_post(title)
