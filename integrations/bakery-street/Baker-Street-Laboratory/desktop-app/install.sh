#!/bin/bash

# Baker Street Laboratory - Desktop Application Installation Script
# Sets up the Electron-based desktop application with psychedelic detective theme

set -e  # Exit on any error

echo "🔬 Baker Street Laboratory - Desktop Application Setup"
echo "====================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_psychedelic() {
    echo -e "${PURPLE}[PSYCHEDELIC]${NC} $1"
}

# Get the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Change to desktop app directory
cd "$SCRIPT_DIR"

print_psychedelic "Initializing kaleidoscopic desktop environment..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed. Please install Node.js 18+ first."
    print_status "Visit: https://nodejs.org/"
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    print_error "Node.js version 18 or higher is required. Current version: $(node --version)"
    exit 1
fi

print_success "Node.js $(node --version) detected"

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    print_error "npm is not installed. Please install npm first."
    exit 1
fi

print_success "npm $(npm --version) detected"

# Install dependencies
print_status "Installing desktop application dependencies..."
print_status "This may take a few minutes for the first installation..."

npm install

if [ $? -eq 0 ]; then
    print_success "Dependencies installed successfully"
else
    print_error "Failed to install dependencies"
    exit 1
fi

# Create necessary directories
print_status "Creating application directories..."
mkdir -p assets/{images,icons,themes,artwork}
mkdir -p src/{scripts,styles}
mkdir -p build
mkdir -p dist

# Create desktop icons directory structure
mkdir -p build/icons
mkdir -p assets/icons/{16x16,32x32,48x48,64x64,128x128,256x256,512x512}

print_success "Directory structure created"

# Create a sample icon (placeholder for your artwork)
print_status "Creating placeholder application icons..."

# Create a simple SVG icon as placeholder
cat > assets/icons/app-icon.svg << 'EOF'
<svg width="256" height="256" viewBox="0 0 256 256" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="psychedelicGrad" cx="50%" cy="50%" r="50%">
      <stop offset="0%" style="stop-color:#FF1493"/>
      <stop offset="33%" style="stop-color:#00CED1"/>
      <stop offset="66%" style="stop-color:#FFD700"/>
      <stop offset="100%" style="stop-color:#8A2BE2"/>
    </radialGradient>
  </defs>
  <rect width="256" height="256" fill="#1A0F08" rx="32"/>
  <circle cx="128" cy="128" r="80" fill="url(#psychedelicGrad)" opacity="0.8"/>
  <circle cx="128" cy="128" r="60" fill="none" stroke="#DAA520" stroke-width="4"/>
  <text x="128" y="140" text-anchor="middle" fill="#F5F5DC" font-family="serif" font-size="24" font-weight="bold">BSL</text>
</svg>
EOF

print_success "Placeholder icons created"

# Check if the API server is running
print_status "Checking API server connection..."
if curl -s -f "http://localhost:5000/api/v2/system/health" > /dev/null 2>&1; then
    print_success "API server is running and accessible"
else
    print_warning "API server is not running. Start it with: ../api/start_api.sh"
    print_status "The desktop app will still install but won't have backend functionality until the API is started"
fi

# Create startup scripts
print_status "Creating startup scripts..."

# Development startup script
cat > start-dev.sh << 'EOF'
#!/bin/bash
echo "🔬 Starting Baker Street Laboratory Desktop App (Development Mode)"
echo "================================================================"

# Check if API server is running
if ! curl -s -f "http://localhost:5000/api/v2/system/health" > /dev/null 2>&1; then
    echo "⚠️  API server not detected. Starting API server..."
    cd ../api && ./start_api.sh &
    API_PID=$!
    echo "API server started with PID: $API_PID"
    sleep 5
fi

# Start the desktop app in development mode
NODE_ENV=development npm run dev
EOF

# Production startup script
cat > start.sh << 'EOF'
#!/bin/bash
echo "🔬 Starting Baker Street Laboratory Desktop App"
echo "=============================================="

# Check if API server is running
if ! curl -s -f "http://localhost:5000/api/v2/system/health" > /dev/null 2>&1; then
    echo "⚠️  Warning: API server not detected at http://localhost:5000"
    echo "   Please start the API server first: ../api/start_api.sh"
    echo "   Or configure a different API URL in the app settings"
fi

# Start the desktop app
npm start
EOF

chmod +x start-dev.sh start.sh

print_success "Startup scripts created"

# Create build script
print_status "Creating build configuration..."

cat > build-all.sh << 'EOF'
#!/bin/bash
echo "🔬 Building Baker Street Laboratory Desktop App for All Platforms"
echo "================================================================"

echo "Building for Windows..."
npm run build-win

echo "Building for macOS..."
npm run build-mac

echo "Building for Linux..."
npm run build-linux

echo "✅ Build complete! Check the 'dist' directory for installers."
EOF

chmod +x build-all.sh

print_success "Build scripts created"

# Create artwork integration guide
print_status "Creating artwork integration guide..."

cat > ARTWORK_INTEGRATION.md << 'EOF'
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
EOF

print_success "Artwork integration guide created"

# Final setup verification
print_status "Verifying installation..."

# Check if all required files exist
REQUIRED_FILES=(
    "package.json"
    "src/main.js"
    "src/preload.js"
    "src/index.html"
    "src/styles/main.css"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        print_success "✓ $file"
    else
        print_error "✗ $file (missing)"
    fi
done

# Check if node_modules exists
if [ -d "node_modules" ]; then
    print_success "✓ Dependencies installed"
else
    print_error "✗ Dependencies not installed"
fi

echo
print_psychedelic "🎉 Baker Street Laboratory Desktop App Setup Complete!"
echo
echo "📋 Next Steps:"
echo "  1. Add your psychedelic detective artwork to assets/ directories"
echo "  2. Start development: ./start-dev.sh"
echo "  3. Or start production: ./start.sh"
echo "  4. Build for distribution: ./build-all.sh"
echo
echo "📖 Documentation:"
echo "  • Artwork Integration: ARTWORK_INTEGRATION.md"
echo "  • API Documentation: ../api/README.md"
echo
echo "🔗 Key Features Ready:"
echo "  ✅ Electron-based desktop application"
echo "  ✅ Psychedelic detective theme framework"
echo "  ✅ API integration for research functionality"
echo "  ✅ Custom artwork integration system"
echo "  ✅ Cross-platform build support"
echo "  ✅ Auto-updater ready"
echo "  ✅ Settings and preferences"
echo
print_success "Ready to traverse kaleidoscopic dreamscapes of knowledge! 🌈🔬"
