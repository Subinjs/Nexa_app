# PWA Icon Setup

To complete the PWA setup, you need to create two icon files:

## Required Icons:
- `icon-192.png` (192x192 pixels)
- `icon-512.png` (512x512 pixels)

## Quick Way to Create Icons:

### Option 1: Online Generator
1. Go to https://favicon.io/favicon-generator/
2. Create a simple icon with "NEXA" text
3. Download and rename to `icon-192.png` and `icon-512.png`

### Option 2: Use Any Logo
1. Get your NEXA logo/brand image
2. Use https://www.iloveimg.com/resize-image to create:
   - One at 192x192px (save as icon-192.png)
   - One at 512x512px (save as icon-512.png)
3. Place both files in the root folder with index.html

### Option 3: Temporary Placeholder
You can temporarily disable icons by removing the `icons` array from manifest.json (the app will still work, just won't have a custom icon when installed).

## After Adding Icons:
The app will be fully installable on mobile devices and desktop browsers!
