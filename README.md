# BIO2025 Blog

A minimal blog that supports static media like images and timelapse videos. Write in **Markdown**, publish to **HTML**.

## Features

- Extremely minimal design inspired by ssi.inc
- **Write in Markdown** (much easier than HTML!)
- Individual HTML files for each post  
- Support for images and videos
- Easy publishing workflow from VS Code
- GitHub Pages ready
- Mobile-friendly

## Quick Start - Creating New Posts

### Method 1: Using VS Code Tasks (Recommended)

1. Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
2. Type "Tasks: Run Task"
3. Select **"New Blog Post (Markdown)"**
4. Enter your post title → Creates `.md` file in `drafts/`
5. **Edit the Markdown file** (use `Cmd+Shift+V` to preview!)
6. When ready: Run **"Publish Post"** task → Converts to HTML
7. Use **"Push Blog to GitHub"** task to publish live

### Method 2: Using Command Line

```bash
# Create new post
python3 new_post.py "Your Post Title"

# Edit the .md file in drafts/ (much easier than HTML!)

# Publish when ready
python3 publish_post.py your-post-slug

# Push to GitHub
git add . && git commit -m "New post" && git push
```

## Why This Is Better

**Before:** Writing HTML by hand 😰
```html
<p>This is <strong>bold</strong> text with a <a href="link">link</a></p>
```

**Now:** Writing Markdown 😍  
```markdown
This is **bold** text with a [link](link)
```

## Adding Media

### Images
- Add your images to `media/images/`
- Reference with: `../media/images/filename.jpg` (from post files)
- Use the figure/figcaption structure for best styling

### Videos
- Add your videos to `media/videos/`
- Reference with: `../media/videos/filename.mp4` (from post files)
- Keep file sizes reasonable for web loading

## Publishing Workflow

1. **Create** a new post (using VS Code task or script)
2. **Edit** the post content in the generated HTML file
3. **Preview** locally (use "Preview Blog" task or open `index.html`)
4. **Publish** using the "Publish Blog" task or manually:
   ```bash
   git add .
   git commit -m "New blog post: Your Title"
   git push origin main
   ```

## Local Preview

Use the VS Code task "Preview Blog" or run:
```bash
python3 -m http.server 8000
```
Then visit `http://localhost:8000`

## File Structure

```
mcvc_blog/
├── index.html          # Post listing page
├── styles.css          # Minimal styling
├── new_post.py         # Post generator script
├── .vscode/
│   └── tasks.json      # VS Code tasks for easy workflow
├── media/
│   ├── images/         # Store your images here
│   └── videos/         # Store your videos here
├── posts/              # Individual post HTML files
│   ├── post-template.html
│   └── welcome.html
└── README.md
```

## Design Philosophy

This blog follows the ultra-minimal aesthetic of sites like ssi.inc:
- Clean typography
- Lots of white space
- Black text on white background
- Simple underlined links
- No unnecessary styling or decorations
- Focus on content

## Tips

- Keep post titles concise and descriptive
- Write compelling excerpts for the homepage
- Use descriptive alt text for images
- Test locally before publishing
- Consider compressing large media files
