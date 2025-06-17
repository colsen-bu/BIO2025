#!/usr/bin/env python3
"""
Script to edit an existing blog post
"""

import os
import sys
import re
from datetime import datetime

def get_existing_posts():
    """Get list of existing posts"""
    posts = []
    posts_dir = "posts"
    drafts_dir = "drafts"
    
    # Check posts directory for HTML files
    if os.path.exists(posts_dir):
        for filename in os.listdir(posts_dir):
            if filename.endswith('.html') and filename != 'post-template.html':
                filepath = os.path.join(posts_dir, filename)
                # Only add if file actually exists and is readable
                if os.path.isfile(filepath) and os.access(filepath, os.R_OK):
                    slug = filename[:-5]  # Remove .html extension
                    posts.append(('published', slug, filepath))
    
    # Check drafts directory for markdown files
    if os.path.exists(drafts_dir):
        for filename in os.listdir(drafts_dir):
            if filename.endswith('.md') and filename != 'README.md':
                filepath = os.path.join(drafts_dir, filename)
                # Only add if file actually exists and is readable
                if os.path.isfile(filepath) and os.access(filepath, os.R_OK):
                    slug = filename[:-3]  # Remove .md extension
                    posts.append(('draft', slug, filepath))
    
    return posts

def extract_title_from_html(filepath):
    """Extract title from HTML file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            # Look for <h1> tag in the article
            match = re.search(r'<article[^>]*>.*?<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
            if match:
                return match.group(1).strip()
    except Exception:
        pass
    return None

def extract_title_from_markdown(filepath):
    """Extract title from markdown file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            # Look for title in frontmatter
            frontmatter_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
            if frontmatter_match:
                frontmatter = frontmatter_match.group(1)
                title_match = re.search(r'^title:\s*(.+)$', frontmatter, re.MULTILINE)
                if title_match:
                    return title_match.group(1).strip()
            
            # Look for first # header
            header_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            if header_match:
                return header_match.group(1).strip()
    except Exception:
        pass
    return None

def list_posts():
    """List all existing posts"""
    posts = get_existing_posts()
    
    if not posts:
        print("No existing posts found.")
        return None
    
    print("\nExisting posts:")
    print("-" * 50)
    
    valid_posts = []
    for i, (status, slug, filepath) in enumerate(posts, 1):
        # Double-check that file still exists
        if not os.path.exists(filepath):
            continue
            
        if status == 'published':
            title = extract_title_from_html(filepath)
        else:
            title = extract_title_from_markdown(filepath)
        
        title_display = title if title else slug
        status_display = "📝 DRAFT" if status == 'draft' else "✅ PUBLISHED"
        
        print(f"{len(valid_posts)+1:2d}. {status_display} - {title_display}")
        print(f"    Slug: {slug}")
        print(f"    File: {filepath}")
        print()
        
        valid_posts.append((status, slug, filepath))
    
    if not valid_posts:
        print("No valid posts found.")
        return None
    
    return valid_posts

def open_post_for_editing(post_info):
    """Open a post for editing"""
    status, slug, filepath = post_info
    
    # Verify file still exists
    if not os.path.exists(filepath):
        print(f"❌ Error: File {filepath} no longer exists.")
        print("The file may have been deleted. Please run the edit command again for an updated list.")
        return
    
    print(f"\nOpening {filepath} for editing...")
    
    # Use VS Code to open the file
    os.system(f'code "{filepath}"')
    
    print(f"\n✅ Opened {filepath} in VS Code")
    
    if status == 'draft':
        print(f"\n💡 Tips for editing:")
        print(f"   • This is a draft markdown file")
        print(f"   • Edit the content as needed")
        print(f"   • Use 'Publish Post' task to convert to HTML when ready")
        print(f"   • Or use the Rich Editor for WYSIWYG editing")
    else:
        print(f"\n💡 Tips for editing:")
        print(f"   • This is a published HTML file")
        print(f"   • Edit the content directly in the HTML")
        print(f"   • Changes will be live when you commit to GitHub")
        print(f"   • Consider editing the markdown version in drafts/ instead")

def main():
    if len(sys.argv) > 1:
        # If slug provided as argument, try to find and edit that post
        target_slug = sys.argv[1]
        posts = get_existing_posts()
        
        for status, slug, filepath in posts:
            if slug == target_slug:
                open_post_for_editing((status, slug, filepath))
                return
        
        print(f"❌ Post with slug '{target_slug}' not found.")
        print("\nAvailable posts:")
        list_posts()
        return
    
    # Interactive mode
    print("🖋️  Edit Existing Blog Post")
    print("=" * 40)
    
    posts = list_posts()
    if not posts:
        return
    
    try:
        choice = input(f"\nEnter post number to edit (1-{len(posts)}): ").strip()
        
        if not choice:
            print("No selection made.")
            return
        
        index = int(choice) - 1
        if 0 <= index < len(posts):
            open_post_for_editing(posts[index])
        else:
            print("❌ Invalid selection.")
    
    except (ValueError, KeyboardInterrupt):
        print("\n👋 Cancelled.")

if __name__ == "__main__":
    main()
