# My Blog

A simple, barebones HTML blog website that supports static media like images and timelapse videos.

## Features

- Clean, responsive design
- Support for images and videos
- Easy to edit and maintain
- GitHub Pages ready
- Mobile-friendly

## How to Add New Blog Posts

### Method 1: Add to index.html (Recommended for simple blogs)

1. Open `index.html`
2. Find the `<section id="blog-posts">` section
3. Add a new `<article class="post">` before the existing posts
4. Use this template:

```html
<article class="post">
    <header>
        <h2>Your Post Title</h2>
        <p class="post-meta">Published on <time datetime="YYYY-MM-DD">Month Day, Year</time></p>
    </header>
    <div class="post-content">
        <p>Your post content here...</p>
        
        <!-- To add an image -->
        <figure>
            <img src="media/images/your-image.jpg" alt="Description" />
            <figcaption>Image caption</figcaption>
        </figure>
        
        <!-- To add a video -->
        <figure>
            <video controls width="100%">
                <source src="media/videos/your-video.mp4" type="video/mp4">
                Your browser does not support the video tag.
            </video>
            <figcaption>Video caption</figcaption>
        </figure>
    </div>
</article>
```

### Method 2: Create separate post files (For larger blogs)

1. Create a new HTML file in the `posts/` directory
2. Use the template provided in `posts/post-template.html`
3. Link to it from the main page

## Adding Media

### Images
- Add your images to `media/images/`
- Supported formats: JPG, PNG, GIF, WebP
- Reference them with: `media/images/filename.jpg`

### Videos
- Add your videos to `media/videos/`
- Supported formats: MP4, WebM, OGV
- Keep file sizes reasonable for web loading
- Reference them with: `media/videos/filename.mp4`

## GitHub Pages Setup

1. Push this repository to GitHub
2. Go to your repository settings
3. Scroll down to "Pages" section
4. Select "Deploy from a branch"
5. Choose "main" branch and "/ (root)" folder
6. Your blog will be available at `https://yourusername.github.io/repository-name`

## Local Development

Simply open `index.html` in your web browser to preview your blog locally.

## File Structure

```
mcvc_blog/
├── index.html          # Main blog page
├── styles.css          # Styling
├── media/
│   ├── images/         # Store your images here
│   └── videos/         # Store your videos here
├── posts/              # Individual post files (optional)
└── README.md           # This file
```

## Tips

- Keep image file sizes under 1MB for faster loading
- Use descriptive filenames for your media
- Always include alt text for images
- Test your blog locally before pushing to GitHub
- Consider compressing videos before uploading
