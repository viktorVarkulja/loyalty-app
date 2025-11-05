# PWA Icons

This folder should contain the PWA icons for the application.

## Required Files

- `icon-192x192.png` - 192x192 pixels
- `icon-512x512.png` - 512x512 pixels
- `favicon.ico` - 32x32 pixels
- `apple-touch-icon.png` - 180x180 pixels

## Design

The icon should feature:
- Purple gradient background (#667eea to #764ba2)
- White star icon in the center
- Rounded corners (100px radius for 512px size)

## How to Generate Icons

You can use the `icon.svg` file and convert it to PNG using:

### Option 1: Using ImageMagick
```bash
# Install ImageMagick first
convert -background none -resize 192x192 icon.svg icon-192x192.png
convert -background none -resize 512x512 icon.svg icon-512x512.png
convert -background none -resize 180x180 icon.svg apple-touch-icon.png
convert -background none -resize 32x32 icon.svg favicon.ico
```

### Option 2: Using Online Tools
- Visit https://realfavicongenerator.net/
- Upload the icon.svg file
- Download and extract all generated icons to this folder

### Option 3: Using Inkscape
```bash
inkscape icon.svg --export-png=icon-192x192.png --export-width=192 --export-height=192
inkscape icon.svg --export-png=icon-512x512.png --export-width=512 --export-height=512
```

## For Development

For now, you can create simple placeholder images or the vite-plugin-pwa will handle it automatically during build.
