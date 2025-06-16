# BIO2025 Blog

A minimal, barebones HTML blog inspired by [ssi.inc](https://ssi.inc/) that supports static media like images and timelapse videos.

## Features

- Extremely minimal design inspired by ssi.inc
- Individual HTML files for each post
- Support for images and videos
- Easy publishing workflow from VS Code
- GitHub Pages ready
- Mobile-friendly

## Quick Start - Creating New Posts

### Method 1: Using VS Code Tasks (Recommended)

1. Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
2. Type "Tasks: Run Task"
3. Select "New Blog Post"
4. Enter your post title
5. Edit the generated HTML file in `posts/`
6. Use "Publish Blog" task to push to GitHub

### Method 2: Using the Python Script

```bash
python3 new_post.py "Your Post Title"
```

This will:
- Create a new HTML file in `posts/` directory
- Update `index.html` with the post listing
- Generate a clean template ready for editing

### Method 3: Manual Creation

1. Copy `posts/post-template.html`
2. Rename it to your post slug (e.g., `my-new-post.html`)
3. Edit the content
4. Add a listing to `index.html`

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
