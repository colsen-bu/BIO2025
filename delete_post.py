#!/usr/bin/env python3
"""
Script to delete a blog post and update the index
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
                slug = filename[:-5]  # Remove .html extension
                posts.append(('published', slug, os.path.join(posts_dir, filename)))
    
    # Check drafts directory for markdown files
    if os.path.exists(drafts_dir):
        for filename in os.listdir(drafts_dir):
            if filename.endswith('.md') and filename != 'README.md':
                slug = filename[:-3]  # Remove .md extension
                posts.append(('draft', slug, os.path.join(drafts_dir, filename)))
    
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
    
    for i, (status, slug, filepath) in enumerate(posts, 1):
        if status == 'published':
            title = extract_title_from_html(filepath)
        else:
            title = extract_title_from_markdown(filepath)
        
        title_display = title if title else slug
        status_display = "📝 DRAFT" if status == 'draft' else "✅ PUBLISHED"
        
        print(f"{i:2d}. {status_display} - {title_display}")
        print(f"    Slug: {slug}")
        print(f"    File: {filepath}")
        print()
    
    return posts

def update_index_after_deletion(deleted_slug):
    """Update index.html after deleting a post"""
    index_file = "index.html"
    
    if not os.path.exists(index_file):
        print(f"⚠️  Warning: {index_file} not found, cannot update index.")
        return
    
    try:
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove the post entry from the index
        # Look for the article post-item pattern that contains the specific post
        pattern = rf'            <article class="post-item">.*?<a href="posts/{re.escape(deleted_slug)}\.html"[^>]*>.*?</article>\s*'
        updated_content = re.sub(pattern, '', content, flags=re.DOTALL)
        
        # If the first pattern didn't work, try a more flexible approach
        if f'posts/{deleted_slug}.html' in updated_content:
            # Split by articles and filter out the one containing our slug
            articles = re.split(r'(<article class="post-item">.*?</article>)', content, flags=re.DOTALL)
            filtered_articles = []
            for part in articles:
                if f'posts/{deleted_slug}.html' not in part:
                    filtered_articles.append(part)
            updated_content = ''.join(filtered_articles)
        
        # Clean up any extra whitespace left behind
        updated_content = re.sub(r'\n\s*\n\s*\n', '\n\n', updated_content)
        
        # Also clean up any standalone empty lines around the deleted content
        updated_content = re.sub(r'(\n\s*){3,}', '\n\n', updated_content)
        
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"✅ Updated {index_file}")
        
    except Exception as e:
        print(f"❌ Error updating {index_file}: {e}")

def delete_post(post_info):
    """Delete a post and associated files"""
    status, slug, filepath = post_info
    
    if status == 'published':
        title = extract_title_from_html(filepath)
    else:
        title = extract_title_from_markdown(filepath)
    
    title_display = title if title else slug
    
    print(f"\n🗑️  Delete Post")
    print(f"   Title: {title_display}")
    print(f"   Slug: {slug}")
    print(f"   Status: {status.upper()}")
    print(f"   File: {filepath}")
    
    # Confirm deletion
    confirm = input(f"\n⚠️  Are you sure you want to delete this post? Type 'DELETE' to confirm: ").strip()
    
    if confirm != 'DELETE':
        print("❌ Deletion cancelled.")
        return
    
    files_to_delete = []
    
    # Add the main file
    files_to_delete.append(filepath)
    
    # If deleting a published post, also look for corresponding draft
    if status == 'published':
        draft_path = os.path.join('drafts', f'{slug}.md')
        if os.path.exists(draft_path):
            files_to_delete.append(draft_path)
    
    # If deleting a draft, also look for corresponding published post
    if status == 'draft':
        published_path = os.path.join('posts', f'{slug}.html')
        if os.path.exists(published_path):
            files_to_delete.append(published_path)
    
    # Delete files
    deleted_files = []
    for file_path in files_to_delete:
        try:
            os.remove(file_path)
            deleted_files.append(file_path)
            print(f"🗑️  Deleted: {file_path}")
        except Exception as e:
            print(f"❌ Error deleting {file_path}: {e}")
    
    if deleted_files:
        # Update index if we deleted a published post
        if status == 'published' or any(f.endswith('.html') for f in deleted_files):
            update_index_after_deletion(slug)
        
        print(f"\n✅ Successfully deleted post: {title_display}")
        print(f"   Files removed: {len(deleted_files)}")
        
        if status == 'published':
            print(f"\n💡 Don't forget to:")
            print(f"   • Commit the changes to git")
            print(f"   • Push to GitHub to update the live blog")
    else:
        print(f"\n❌ No files were deleted.")

def main():
    if len(sys.argv) > 1:
        # If slug provided as argument, try to find and delete that post
        target_slug = sys.argv[1]
        posts = get_existing_posts()
        
        for status, slug, filepath in posts:
            if slug == target_slug:
                delete_post((status, slug, filepath))
                return
        
        print(f"❌ Post with slug '{target_slug}' not found.")
        print("\nAvailable posts:")
        list_posts()
        return
    
    # Interactive mode
    print("🗑️  Delete Blog Post")
    print("=" * 40)
    
    posts = list_posts()
    if not posts:
        return
    
    try:
        choice = input(f"\nEnter post number to delete (1-{len(posts)}): ").strip()
        
        if not choice:
            print("No selection made.")
            return
        
        index = int(choice) - 1
        if 0 <= index < len(posts):
            delete_post(posts[index])
        else:
            print("❌ Invalid selection.")
    
    except (ValueError, KeyboardInterrupt):
        print("\n👋 Cancelled.")

if __name__ == "__main__":
    main()
