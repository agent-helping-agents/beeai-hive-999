# Baker Street Laboratory - Assets Directory

🎨 **Custom Artwork and Visual Assets Management**

This directory contains all visual assets for the Baker Street Laboratory application interfaces, organized for easy integration across desktop, mobile, and web applications.

## 📁 Directory Structure

```
assets/
├── images/           # Raster images (PNG, JPG, WebP)
│   ├── backgrounds/  # Background images and textures
│   ├── detective/    # Detective-themed artwork
│   ├── research/     # Research-related imagery
│   └── ui/          # UI elements and components
├── svg/             # Vector graphics (SVG)
│   ├── icons/       # Scalable icons
│   ├── logos/       # Brand logos and marks
│   └── illustrations/ # Custom illustrations
├── icons/           # Application icons (various sizes)
│   ├── app/         # Main application icons
│   ├── toolbar/     # Toolbar and menu icons
│   └── status/      # Status and notification icons
├── fonts/           # Custom fonts and typography
│   ├── detective/   # Detective/mystery themed fonts
│   └── modern/      # Modern, clean fonts
└── themes/          # Color schemes and themes
    ├── detective/   # Dark detective theme
    ├── laboratory/  # Scientific laboratory theme
    └── modern/      # Modern clean theme
```

## 🎨 Design Guidelines

### Color Palette

#### Detective Theme
- **Primary**: `#2C1810` (Dark Brown)
- **Secondary**: `#8B4513` (Saddle Brown)
- **Accent**: `#DAA520` (Goldenrod)
- **Text**: `#F5F5DC` (Beige)
- **Background**: `#1A1A1A` (Near Black)

#### Laboratory Theme
- **Primary**: `#0F4C75` (Dark Blue)
- **Secondary**: `#3282B8` (Blue)
- **Accent**: `#BBE1FA` (Light Blue)
- **Text**: `#0F3460` (Dark Blue)
- **Background**: `#FFFFFF` (White)

### Typography
- **Headers**: Serif fonts for detective theme, Sans-serif for modern
- **Body**: Clean, readable fonts
- **Code**: Monospace fonts for technical content

### Icon Style
- **Size**: 16px, 24px, 32px, 48px, 64px, 128px, 256px
- **Style**: Consistent line weight and corner radius
- **Format**: SVG for scalability, PNG for complex icons

## 🖼️ Asset Integration

### Using with VSCodium Extensions

#### SVG Preview (`jock.svg`)
- Edit SVG files with live preview
- Perfect for creating custom detective-themed icons
- Real-time visual feedback

#### Image Preview (`kisstkondoros.vscode-gutter-preview`)
- Hover over image paths to see thumbnails
- Verify artwork loads correctly in code
- Quick asset verification

#### Draw.io Integration (`hediet.vscode-drawio`)
- Create UI mockups and wireframes
- Design app layouts with custom artwork
- Export designs as SVG/PNG

### File Naming Conventions

```
# Images
detective_silhouette_512x512.png
research_background_1920x1080.jpg
magnifying_glass_icon_64x64.png

# SVG Icons
icon_search.svg
logo_baker_street.svg
illustration_detective_work.svg

# Fonts
DetectiveSerif-Regular.ttf
LaboratoryMono-Bold.woff2
```

## 🚀 Integration Examples

### Desktop Application (Electron)
```javascript
// In your Electron app
const iconPath = path.join(__dirname, 'assets/icons/app/baker_street_256x256.png');
const backgroundImage = path.join(__dirname, 'assets/images/backgrounds/detective_office.jpg');
```

### Mobile Application (Flutter)
```dart
// In your Flutter app
Image.asset('assets/images/detective/magnifying_glass.png')
SvgPicture.asset('assets/svg/icons/search.svg')
```

### Web Interface
```css
/* CSS integration */
.detective-theme {
    background-image: url('../assets/images/backgrounds/vintage_paper.jpg');
    color: #F5F5DC;
}

.research-icon {
    background-image: url('../assets/svg/icons/research.svg');
}
```

### API Integration
```python
# Serve assets through API
@app.route('/assets/<path:filename>')
def serve_asset(filename):
    return send_from_directory('assets', filename)
```

## 🎯 Asset Optimization

### Automated Optimization
```bash
# Image optimization
optipng assets/images/**/*.png
jpegoptim assets/images/**/*.jpg

# SVG optimization
svgo assets/svg/**/*.svg
```

### Responsive Images
```html
<!-- Multiple sizes for different screens -->
<img src="assets/images/logo_256.png" 
     srcset="assets/images/logo_128.png 1x, 
             assets/images/logo_256.png 2x"
     alt="Baker Street Laboratory">
```

## 🔧 Development Workflow

### 1. Asset Creation
- Create artwork in your preferred design tool
- Export in multiple formats and sizes
- Follow naming conventions

### 2. Integration Testing
- Use VSCodium extensions for preview
- Test in different application contexts
- Verify responsive behavior

### 3. Optimization
- Compress images without quality loss
- Optimize SVGs for web delivery
- Generate multiple sizes as needed

### 4. Documentation
- Update this README with new assets
- Document color codes and usage
- Maintain style guide consistency

## 📱 Platform-Specific Assets

### Desktop (Electron)
- App icons: 16x16 to 512x512 PNG
- Tray icons: 16x16, 32x32 PNG
- Window icons: 32x32, 48x48 PNG

### Mobile (Flutter)
- App icons: 1024x1024 PNG (iOS), 512x512 PNG (Android)
- Splash screens: Various resolutions
- Adaptive icons: Foreground + Background

### Web
- Favicon: 16x16, 32x32, 48x48 ICO/PNG
- Apple touch icons: 180x180 PNG
- Open Graph images: 1200x630 PNG

## 🎨 Custom Artwork Integration

### Detective Theme Elements
- Magnifying glass icons
- Vintage paper textures
- Sherlock Holmes silhouettes
- Victorian-era design elements
- Mystery/investigation imagery

### Laboratory Theme Elements
- Scientific equipment icons
- Clean, modern layouts
- Research-focused imagery
- Data visualization elements
- Academic/professional styling

### Usage in Applications
```javascript
// Theme switching
const themes = {
    detective: {
        background: 'assets/images/backgrounds/detective_office.jpg',
        primaryColor: '#2C1810',
        font: 'DetectiveSerif'
    },
    laboratory: {
        background: 'assets/images/backgrounds/clean_lab.jpg',
        primaryColor: '#0F4C75',
        font: 'LaboratoryMono'
    }
};
```

---

**🔬 Ready to create stunning visual experiences for Baker Street Laboratory!** 🎨✨
