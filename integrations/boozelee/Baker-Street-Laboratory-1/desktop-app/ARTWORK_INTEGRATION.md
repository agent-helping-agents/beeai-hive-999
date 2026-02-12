# Baker Street Laboratory - Artwork Integration Guide

## 🎨 Integrating Your Psychedelic Detective Artwork

This desktop application is designed to showcase your amazing psychedelic detective artwork. Here's how to integrate your custom visuals:

### 1. Main Logo/Branding
- Replace `assets/icons/app-icon.svg` with your psychedelic Holmes logo
- Recommended size: 256x256px minimum, scalable SVG preferred
- The logo appears in the header and as the application icon

### 2. Background Artwork
- Add your kaleidoscopic dreamscape images to `assets/images/backgrounds/`
- Supported formats: PNG, JPG, WebP, SVG
- Recommended resolution: 1920x1080px or higher
- Update `src/styles/psychedelic.css` to reference your backgrounds

### 3. Icon Set
- Create a complete icon set in `assets/icons/` with sizes:
  - 16x16, 32x32, 48x48, 64x64, 128x128, 256x256, 512x512
- Use your psychedelic detective theme colors and style
- Icons are used for the taskbar, dock, and window decorations

### 4. UI Elements
- Add custom UI graphics to `assets/images/ui/`
- Examples: buttons, borders, decorative elements
- The CSS framework in `src/styles/` is ready to integrate these

### 5. Theme Assets
- Store theme-specific artwork in `assets/themes/psychedelic/`
- Include: color palettes, patterns, textures
- The theme system will automatically load these

### 6. Integration Steps
1. Add your artwork files to the appropriate directories
2. Update the CSS files to reference your artwork
3. Modify `src/index.html` to include your custom elements
4. Test with `npm run dev`
5. Build with `npm run build`

### 7. CSS Classes for Artwork
The framework provides these classes for your artwork:
- `.artwork-container` - Main container with effects
- `.artwork-frame` - Psychedelic border frame
- `.custom-artwork` - Responsive artwork display
- `.psychedelic-gradient` - Animated gradient backgrounds

### 8. JavaScript Integration
Use the psychedelic effects API in `src/scripts/psychedelic-effects.js`:
- `PsychedelicEffects.setArtwork(imagePath)` - Set background artwork
- `PsychedelicEffects.enableParticles()` - Enable particle effects
- `PsychedelicEffects.animateColors()` - Animate color schemes

Your artwork will transform this desktop app into a truly immersive psychedelic detective experience! 🌈🔍
